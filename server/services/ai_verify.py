from openai import OpenAI
import os
import base64
import requests
from .ipfs_service import ipfs_service

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", ""))

class AIVerifyService:
    async def verify_selfie(self, selfie_data: bytes, nft_metadata_uri: str) -> dict:
        try:
            metadata_url = ipfs_service.get_ipfs_url(nft_metadata_uri)
            metadata_response = requests.get(metadata_url)
            
            if metadata_response.status_code != 200:
                return {
                    "verified": False,
                    "status": "error",
                    "reason": "Failed to fetch NFT metadata"
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
            
            selfie_base64 = base64.b64encode(selfie_data).decode('utf-8')
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """You are a security system verifying if a selfie matches the person in an NFT ticket image. 

Compare the two images and determine:
1. If they show the same person
2. The confidence level of the match

Respond with ONLY one of these exact phrases:
- "VERIFIED" if the faces match with high confidence
- "SUSPICIOUS" if there's some similarity but uncertain
- "DENIED" if the faces clearly don't match or can't be properly compared

Consider facial features, but account for different lighting, angles, and expressions."""
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
                                    "url": ticket_image_url,
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=300
            )
            
            result_text = response.choices[0].message.content.strip().upper()
            
            if "VERIFIED" in result_text:
                status = "verified"
                verified = True
            elif "SUSPICIOUS" in result_text:
                status = "suspicious"
                verified = False
            else:
                status = "denied"
                verified = False
            
            return {
                "verified": verified,
                "status": status,
                "reason": result_text,
                "confidence": "high" if verified else "low"
            }
            
        except Exception as e:
            print(f"AI verification error: {e}")
            return {
                "verified": False,
                "status": "error",
                "reason": f"Verification failed: {str(e)}"
            }

ai_verify_service = AIVerifyService()
