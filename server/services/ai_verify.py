from openai import OpenAI
import os
import base64
import httpx
from dotenv import load_dotenv
from .ipfs_service import ipfs_service

# Load environment variables from .env file
load_dotenv()

# AI Provider Configuration
AI_PROVIDER = os.getenv("AI_PROVIDER", "openai").lower()  # "openai", "gemini", "claude", or "huggingface"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")  # Optional, but recommended for higher limits
AI_MODEL = os.getenv("AI_MODEL", "")  # Override model if needed

# Initialize client based on provider
client = None
if AI_PROVIDER == "gemini" and GEMINI_API_KEY:
    # Use Gemini API with OpenAI-compatible endpoint
    client = OpenAI(
        api_key=GEMINI_API_KEY,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = AI_MODEL or "gemini-2.0-flash-exp"
elif AI_PROVIDER == "claude" and CLAUDE_API_KEY:
    # Use Claude API (Anthropic)
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=CLAUDE_API_KEY)
        model = AI_MODEL or "claude-3-5-sonnet-20241022"
    except ImportError:
        print("Warning: anthropic package not installed. Install with: pip install anthropic")
        client = None
        model = None
elif AI_PROVIDER == "huggingface":
    # Hugging Face Inference API (free tier available)
    client = "huggingface"  # Special marker for Hugging Face
    model = AI_MODEL or "Salesforce/blip-image-captioning-base"  # Can use vision models
elif OPENAI_API_KEY:
    # Use OpenAI - ensure we're using the latest API format
    client = OpenAI(api_key=OPENAI_API_KEY)
    # Use gpt-4o for vision, or gpt-4o-mini for cost efficiency
    model = AI_MODEL or os.getenv("OPENAI_MODEL", "gpt-4o")
else:
    model = None

class AIVerifyService:
    async def verify_selfie(self, selfie_data: bytes, nft_metadata_uri: str) -> dict:
        if not client:
            provider_name_map = {
                "gemini": "Gemini",
                "claude": "Claude",
                "huggingface": "Hugging Face",
                "openai": "OpenAI"
            }
            provider_name = provider_name_map.get(AI_PROVIDER, "AI")
            key_name_map = {
                "gemini": "GEMINI_API_KEY",
                "claude": "CLAUDE_API_KEY",
                "huggingface": "HUGGINGFACE_API_KEY (optional)",
                "openai": "OPENAI_API_KEY"
            }
            key_name = key_name_map.get(AI_PROVIDER, "API_KEY")
            return {
                "verified": False,
                "status": "error",
                "reason": f"{provider_name} API key not configured. Please set {key_name} in .env file"
            }
        
        if not model and AI_PROVIDER != "huggingface":
            return {
                "verified": False,
                "status": "error",
                "reason": "AI model not configured"
            }
        
        try:
            metadata_url = ipfs_service.get_ipfs_url(nft_metadata_uri)
            
            if not metadata_url:
                return {
                    "verified": False,
                    "status": "error",
                    "reason": "Invalid metadata URI (mock IPFS hash detected). Please use real IPFS or configure Pinata credentials."
                }
            
            print(f"Fetching metadata from: {metadata_url}")
            async with httpx.AsyncClient(timeout=30.0) as http_client:
                metadata_response = await http_client.get(metadata_url)
            
            if metadata_response.status_code != 200:
                print(f"Metadata fetch failed: {metadata_response.status_code} - {metadata_response.text}")
                return {
                    "verified": False,
                    "status": "error",
                    "reason": f"Failed to fetch NFT metadata (HTTP {metadata_response.status_code})"
                }
            
            metadata = metadata_response.json()
            ticket_image_uri = metadata.get("image", "")
            
            if not ticket_image_uri:
                return {
                    "verified": False,
                    "status": "error",
                    "reason": "No image found in NFT metadata"
                }
            
            ticket_image_url = ipfs_service.get_ipfs_url(ticket_image_uri)
            
            if not ticket_image_url:
                return {
                    "verified": False,
                    "status": "error",
                    "reason": "Invalid image URI (mock IPFS hash detected). Please use real IPFS or configure Pinata credentials."
                }
            
            print(f"Fetching ticket image from: {ticket_image_url}")
            
            selfie_base64 = base64.b64encode(selfie_data).decode('utf-8')
            
            # Fetch ticket image for providers that need base64
            async with httpx.AsyncClient(timeout=30.0) as http_client:
                ticket_image_response = await http_client.get(ticket_image_url)
                if ticket_image_response.status_code != 200:
                    return {
                        "verified": False,
                        "status": "error",
                        "reason": f"Failed to fetch ticket image (HTTP {ticket_image_response.status_code})"
                    }
                ticket_image_base64 = base64.b64encode(ticket_image_response.content).decode('utf-8')
            
            # Prepare image content based on provider
            if AI_PROVIDER == "claude":
                # Claude API format
                try:
                    response = client.messages.create(
                        model=model,
                        max_tokens=300,
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": """You are a security system verifying if a selfie matches the person in an NFT ticket image. 

Compare the two images carefully and determine if they show the SAME person.

IMPORTANT: You MUST respond with ONLY one of these exact words (nothing else):
- VERIFIED (if the faces match the same person)
- SUSPICIOUS (if there's some similarity but uncertain)
- DENIED (if the faces don't match or are different people)

Consider: facial structure, eye shape, nose, mouth, face shape, hair, skin tone, and distinctive features. Account for different lighting, angles, and expressions. Be accurate and fair - verify when the faces match, deny when they don't.

Your response must start with one of these three words: VERIFIED, SUSPICIOUS, or DENIED."""
                                    },
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/jpeg",
                                            "data": selfie_base64
                                        }
                                    },
                                    {
                                        "type": "image",
                                        "source": {
                                            "type": "base64",
                                            "media_type": "image/jpeg",
                                            "data": ticket_image_base64
                                        }
                                    }
                                ]
                            }
                        ]
                    )
                    result_text = (response.content[0].text if response.content else "").strip()
                except Exception as claude_error:
                    return {
                        "verified": False,
                        "status": "error",
                        "reason": f"Claude API error: {str(claude_error)}"
                    }
            elif AI_PROVIDER == "huggingface":
                # Hugging Face Inference API - using a vision-language model for image comparison
                try:
                    # Use a vision-language model that can analyze images
                    # Using BLIP-2 or similar model that supports visual question answering
                    hf_model = model or "Salesforce/blip2-opt-2.7b"
                    hf_url = f"https://api-inference.huggingface.co/models/{hf_model}"
                    
                    headers = {"Content-Type": "application/json"}
                    if HUGGINGFACE_API_KEY:
                        headers["Authorization"] = f"Bearer {HUGGINGFACE_API_KEY}"
                    
                    # Use visual question answering to compare faces
                    # We'll ask the model to compare the two images
                    async with httpx.AsyncClient(timeout=90.0) as http_client:
                        # First, get detailed descriptions of both images
                        prompt = "Describe the person in this image in detail, focusing on facial features, hair, and distinctive characteristics."
                        
                        # Analyze selfie
                        selfie_payload = {
                            "inputs": {
                                "image": f"data:image/jpeg;base64,{selfie_base64}",
                                "question": prompt
                            }
                        }
                        
                        # Analyze ticket image
                        ticket_payload = {
                            "inputs": {
                                "image": f"data:image/jpeg;base64,{ticket_image_base64}",
                                "question": prompt
                            }
                        }
                        
                        try:
                            # Try visual question answering approach
                            selfie_response = await http_client.post(
                                hf_url,
                                headers=headers,
                                json=selfie_payload
                            )
                            ticket_response = await http_client.post(
                                hf_url,
                                headers=headers,
                                json=ticket_payload
                            )
                            
                            if selfie_response.status_code == 200 and ticket_response.status_code == 200:
                                selfie_desc = selfie_response.json()
                                ticket_desc = ticket_response.json()
                                
                                # Extract text from responses
                                selfie_text = str(selfie_desc).lower() if isinstance(selfie_desc, dict) else str(selfie_desc).lower()
                                ticket_text = str(ticket_desc).lower() if isinstance(ticket_desc, dict) else str(ticket_desc).lower()
                                
                                # Use a more sophisticated comparison
                                # Check if both descriptions mention a person/face
                                has_person_selfie = any(word in selfie_text for word in ["person", "face", "man", "woman", "people", "human"])
                                has_person_ticket = any(word in ticket_text for word in ["person", "face", "man", "woman", "people", "human"])
                                
                                if not (has_person_selfie and has_person_ticket):
                                    result_text = "DENIED"
                                else:
                                    # Check for common facial features
                                    common_features = 0
                                    features_to_check = ["hair", "eyes", "nose", "mouth", "face", "skin", "beard", "mustache", "glasses", "smile", "cheek", "chin", "forehead"]
                                    
                                    for feature in features_to_check:
                                        if feature in selfie_text and feature in ticket_text:
                                            common_features += 1
                                    
                                    # Balanced threshold - require multiple matching features to verify
                                    # Need at least 3 matching facial features to verify
                                    if common_features >= 3:
                                        result_text = "VERIFIED"
                                    elif common_features >= 2:
                                        result_text = "SUSPICIOUS"
                                    else:
                                        result_text = "DENIED"
                            else:
                                # Fallback: use image-to-text model
                                hf_model_fallback = "Salesforce/blip-image-captioning-base"
                                hf_url_fallback = f"https://api-inference.huggingface.co/models/{hf_model_fallback}"
                                
                                selfie_payload_simple = {"inputs": f"data:image/jpeg;base64,{selfie_base64}"}
                                ticket_payload_simple = {"inputs": f"data:image/jpeg;base64,{ticket_image_base64}"}
                                
                                selfie_response = await http_client.post(hf_url_fallback, headers=headers, json=selfie_payload_simple)
                                ticket_response = await http_client.post(hf_url_fallback, headers=headers, json=ticket_payload_simple)
                                
                                if selfie_response.status_code == 200 and ticket_response.status_code == 200:
                                    selfie_desc = selfie_response.json()
                                    ticket_desc = ticket_response.json()
                                    
                                    # Extract generated text
                                    selfie_text = str(selfie_desc[0].get("generated_text", "")).lower() if isinstance(selfie_desc, list) else str(selfie_desc).lower()
                                    ticket_text = str(ticket_desc[0].get("generated_text", "")).lower() if isinstance(ticket_desc, list) else str(ticket_desc).lower()
                                    
                                    # Compare descriptions - more lenient approach
                                    common_words = set(selfie_text.split()) & set(ticket_text.split())
                                    total_words = max(len(selfie_text.split()), len(ticket_text.split()), 1)
                                    similarity = len(common_words) / total_words if total_words > 0 else 0
                                    
                                    # Check if both mention person/face
                                    has_person_selfie = any(word in selfie_text for word in ["person", "face", "man", "woman", "people", "human", "portrait"])
                                    has_person_ticket = any(word in ticket_text for word in ["person", "face", "man", "woman", "people", "human", "portrait"])
                                    
                                    # Balanced verification: require reasonable similarity
                                    if has_person_selfie and has_person_ticket:
                                        # Need at least 30% similarity OR at least 4 common words to verify
                                        if similarity >= 0.3 or len(common_words) >= 4:
                                            result_text = "VERIFIED"
                                        elif similarity >= 0.2 or len(common_words) >= 2:
                                            result_text = "SUSPICIOUS"
                                        else:
                                            result_text = "DENIED"
                                    elif similarity >= 0.4:
                                        # High similarity even without explicit person detection
                                        result_text = "VERIFIED"
                                    elif similarity >= 0.25:
                                        result_text = "SUSPICIOUS"
                                    else:
                                        result_text = "DENIED"
                                else:
                                    # If API fails, return error instead of denying
                                    error_code = selfie_response.status_code or ticket_response.status_code
                                    if error_code == 410:
                                        # Model removed/unavailable - return error
                                        raise Exception(f"Hugging Face model unavailable (410). The model endpoint has been removed. Please use a different AI provider (OpenAI, Gemini, or Claude) or update the model name in .env")
                                    else:
                                        print(f"Hugging Face API returned non-200 status. Selfie: {selfie_response.status_code}, Ticket: {ticket_response.status_code}")
                                        raise Exception(f"Hugging Face API error: HTTP {error_code}. Please check your API key or use a different AI provider.")
                                    
                        except Exception as api_error:
                            # If the model doesn't support the format, raise error
                            print(f"Hugging Face API format error: {api_error}")
                            raise Exception(f"Hugging Face API error: {str(api_error)}. Please use a different AI provider (OpenAI, Gemini, or Claude) for better face verification.")
                    
                except Exception as hf_error:
                    error_msg = str(hf_error)
                    print(f"Hugging Face API error: {hf_error}")
                    
                    # Check for rate limiting
                    if "429" in error_msg or "rate limit" in error_msg.lower():
                        return {
                            "verified": False,
                            "status": "error",
                            "reason": f"Hugging Face API rate limit exceeded. Please wait a moment and try again. Free tier has limits. For better face verification, consider using OpenAI, Gemini, or Claude instead."
                        }
                    
                    # Check for model unavailable (410)
                    if "410" in error_msg or "unavailable" in error_msg.lower() or "removed" in error_msg.lower():
                        return {
                            "verified": False,
                            "status": "error",
                            "reason": f"Hugging Face model unavailable. The model endpoint has been removed or is not available. Please configure a different AI provider (OpenAI, Gemini, or Claude) in your .env file for proper face verification. Hugging Face is not recommended for face verification."
                        }
                    
                    return {
                        "verified": False,
                        "status": "error",
                        "reason": f"Hugging Face API error: {error_msg}. For better face verification, please use OpenAI, Gemini, or Claude instead. Configure AI_PROVIDER and the corresponding API key in server/.env"
                    }
            elif AI_PROVIDER == "gemini":
                # Gemini format: data URIs for images
                image_content = [
                    {
                        "type": "text",
                        "text": """You are a security system verifying if a selfie matches the person in an NFT ticket image. 

Compare the two images carefully and determine if they show the SAME person.

IMPORTANT: You MUST respond with ONLY one of these exact words (nothing else):
- VERIFIED (if the faces match the same person)
- SUSPICIOUS (if there's some similarity but uncertain)
- DENIED (if the faces don't match or are different people)

Consider: facial structure, eye shape, nose, mouth, face shape, hair, skin tone, and distinctive features. Account for different lighting, angles, and expressions. Be accurate and fair - verify when the faces match, deny when they don't.

Your response must start with one of these three words: VERIFIED, SUSPICIOUS, or DENIED."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{selfie_base64}"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{ticket_image_base64}"
                        }
                    }
                ]
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": image_content
                        }
                    ],
                    max_tokens=300
                )
                
                result_text = (response.choices[0].message.content or "").strip()
            else:
                # OpenAI format (default)
                image_content = [
                    {
                        "type": "text",
                        "text": """You are a security system verifying if a selfie matches the person in an NFT ticket image. 

Compare the two images carefully and determine if they show the SAME person.

IMPORTANT: You MUST respond with ONLY one of these exact words (nothing else):
- VERIFIED (if the faces match the same person)
- SUSPICIOUS (if there's some similarity but uncertain)
- DENIED (if the faces don't match or are different people)

Consider: facial structure, eye shape, nose, mouth, face shape, hair, skin tone, and distinctive features. Account for different lighting, angles, and expressions. Be accurate and fair - verify when the faces match, deny when they don't.

Your response must start with one of these three words: VERIFIED, SUSPICIOUS, or DENIED."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{selfie_base64}",
                            "detail": "high"
                        }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{ticket_image_base64}",
                            "detail": "high"
                        }
                    }
                ]
                
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": image_content
                        }
                    ],
                    max_tokens=300
                )
                
                result_text = (response.choices[0].message.content or "").strip()
            
            # Parse result - look for keywords in the response
            result_text_upper = result_text.upper()
            print(f"AI Response (raw): {result_text}")
            print(f"AI Response (upper): {result_text_upper}")
            
            # Check for verified - be more lenient with matching
            if ("VERIFIED" in result_text_upper or 
                ("MATCH" in result_text_upper and ("SAME" in result_text_upper or "PERSON" in result_text_upper)) or
                ("YES" in result_text_upper and "SAME" in result_text_upper) or
                ("CONFIRM" in result_text_upper and "MATCH" in result_text_upper) or
                ("IDENTICAL" in result_text_upper) or
                ("THEY ARE THE SAME" in result_text_upper)):
                status = "verified"
                verified = True
                print("✅ Parsed as VERIFIED")
            # Check for suspicious
            elif ("SUSPICIOUS" in result_text_upper or 
                  "UNCERTAIN" in result_text_upper or 
                  ("SIMILAR" in result_text_upper and "NOT SURE" in result_text_upper) or
                  ("MAYBE" in result_text_upper and "MATCH" in result_text_upper)):
                status = "suspicious"
                verified = False
                print("⚠️ Parsed as SUSPICIOUS")
            # Check for denied
            elif ("DENIED" in result_text_upper or 
                  "DON'T MATCH" in result_text_upper or 
                  "DO NOT MATCH" in result_text_upper or
                  "DIFFERENT" in result_text_upper or 
                  "NOT MATCH" in result_text_upper or
                  "NOT THE SAME" in result_text_upper or
                  ("NO" in result_text_upper and "MATCH" in result_text_upper)):
                status = "denied"
                verified = False
                print("❌ Parsed as DENIED")
            else:
                # Default to denied if we can't parse the response
                print(f"⚠️ Warning: Could not parse AI response: {result_text}")
                print(f"   Defaulting to DENIED for security")
                status = "denied"
                verified = False
            
            return {
                "verified": verified,
                "status": status,
                "reason": result_text,
                "confidence": "high" if verified else "low"
            }
            
        except Exception as e:
            error_str = str(e)
            print(f"AI verification error: {e}")
            
            # Handle specific API errors
            provider_name_map = {
                "gemini": "Gemini",
                "claude": "Claude",
                "huggingface": "Hugging Face",
                "openai": "OpenAI"
            }
            provider_name = provider_name_map.get(AI_PROVIDER, "AI")
            if "insufficient_quota" in error_str or "429" in error_str or "quota" in error_str.lower() or "resource_exhausted" in error_str.lower():
                if AI_PROVIDER == "gemini":
                    return {
                        "verified": False,
                        "status": "error",
                        "reason": f"{provider_name} API quota exceeded. Check your quota at https://aistudio.google.com/app/apikey. Free tier has daily limits. Wait for reset or upgrade your plan."
                    }
                else:
                    return {
                        "verified": False,
                        "status": "error",
                        "reason": f"{provider_name} API quota exceeded. Please add credits to your OpenAI account or check your billing. Visit https://platform.openai.com/account/billing"
                    }
            elif "invalid_api_key" in error_str or "401" in error_str or "unauthorized" in error_str.lower():
                key_name_map = {
                    "gemini": "GEMINI_API_KEY",
                    "claude": "CLAUDE_API_KEY",
                    "huggingface": "HUGGINGFACE_API_KEY",
                    "openai": "OPENAI_API_KEY"
                }
                key_name = key_name_map.get(AI_PROVIDER, "API_KEY")
                return {
                    "verified": False,
                    "status": "error",
                    "reason": f"Invalid {provider_name} API key. Please check your {key_name} in the .env file."
                }
            elif "rate_limit" in error_str:
                return {
                    "verified": False,
                    "status": "error",
                    "reason": f"{provider_name} API rate limit exceeded. Please wait a moment and try again."
                }
            
            return {
                "verified": False,
                "status": "error",
                "reason": f"Verification failed: {error_str}"
            }

ai_verify_service = AIVerifyService()
