import httpx
import json
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

PINATA_API_KEY = os.getenv("PINATA_API_KEY", "")
PINATA_SECRET_API_KEY = os.getenv("PINATA_SECRET_API_KEY", "")
PINATA_JWT = os.getenv("PINATA_JWT", "")

PINATA_PIN_FILE_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"
PINATA_PIN_JSON_URL = "https://api.pinata.cloud/pinning/pinJSONToIPFS"

class IPFSService:
    def __init__(self):
        self.headers = {}
        if PINATA_JWT:
            self.headers["Authorization"] = f"Bearer {PINATA_JWT}"
        elif PINATA_API_KEY and PINATA_SECRET_API_KEY:
            self.headers["pinata_api_key"] = PINATA_API_KEY
            self.headers["pinata_secret_api_key"] = PINATA_SECRET_API_KEY
    
    async def upload_file(self, file_data: bytes, filename: str) -> Optional[str]:
        if not self.headers:
            print("Warning: IPFS credentials not configured. Using mock IPFS hash.")
            return f"ipfs://QmMockHash{hash(file_data) % 10000}/{filename}"
        
        try:
            files = {
                'file': (filename, file_data, 'application/octet-stream')
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    PINATA_PIN_FILE_URL,
                    files=files,
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    ipfs_hash = response.json()['IpfsHash']
                    return f"ipfs://{ipfs_hash}"
                else:
                    print(f"IPFS upload error: {response.text}")
                    raise Exception(f"IPFS upload failed with status {response.status_code}")
        except Exception as e:
            print(f"IPFS upload exception: {e}")
            raise Exception(f"Failed to upload to IPFS: {str(e)}")
    
    async def upload_json(self, metadata: dict) -> Optional[str]:
        if not self.headers:
            print("Warning: IPFS credentials not configured. Using mock IPFS hash.")
            return f"ipfs://QmMockMetadata{hash(json.dumps(metadata)) % 10000}"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    PINATA_PIN_JSON_URL,
                    json={
                        "pinataContent": metadata,
                        "pinataMetadata": {
                            "name": "NFT Ticket Metadata"
                        }
                    },
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    ipfs_hash = response.json()['IpfsHash']
                    return f"ipfs://{ipfs_hash}"
                else:
                    print(f"IPFS JSON upload error: {response.text}")
                    raise Exception(f"IPFS JSON upload failed with status {response.status_code}")
        except Exception as e:
            print(f"IPFS JSON upload exception: {e}")
            raise Exception(f"Failed to upload metadata to IPFS: {str(e)}")
    
    def get_ipfs_url(self, ipfs_uri: str) -> str:
        if not ipfs_uri:
            return ""
        
        if ipfs_uri.startswith("ipfs://"):
            ipfs_hash = ipfs_uri.replace("ipfs://", "").strip()
            # Handle mock hashes (for testing without Pinata)
            if "Mock" in ipfs_hash or "QmMock" in ipfs_hash:
                # For mock hashes, we can't fetch from IPFS
                # Return empty string so the verification can handle it gracefully
                print(f"Warning: Mock IPFS hash detected: {ipfs_hash}")
                return ""
            # Use multiple IPFS gateways for better reliability
            # Try Pinata first, then public gateways
            return f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        elif ipfs_uri.startswith("http://") or ipfs_uri.startswith("https://"):
            # Already an HTTP URL
            return ipfs_uri
        else:
            # Assume it's just a hash, prepend gateway
            return f"https://gateway.pinata.cloud/ipfs/{ipfs_uri}"

ipfs_service = IPFSService()
