from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from database import verifications_collection, tickets_collection
from services.ai_verify import ai_verify_service
from services.blockchain import blockchain_service
from datetime import datetime
import json

router = APIRouter(prefix="/verify", tags=["verify"])

@router.post("")
async def verify_ticket(
    qr_data: str = Form(...),
    selfie: UploadFile = File(...)
):
    try:
        print(f"Verification request - QR data length: {len(qr_data)}")
        qr_info = json.loads(qr_data)
        token_id = qr_info.get("token_id")
        metadata_uri = qr_info.get("metadata_uri")
        
        if not token_id:
            raise HTTPException(status_code=400, detail="Missing token_id in QR code data")
        
        if metadata_uri is None:
            print(f"Metadata URI not in QR, fetching from blockchain for token {token_id}")
            metadata_uri = blockchain_service.get_token_uri(token_id)
        
        if not metadata_uri:
            raise HTTPException(status_code=400, detail=f"Could not find metadata URI for token {token_id}. Make sure the ticket was minted correctly.")
        
        print(f"Using metadata URI: {metadata_uri}")
        selfie_data = await selfie.read()
        print(f"Selfie uploaded: {len(selfie_data)} bytes")
        
        verification_result = await ai_verify_service.verify_selfie(selfie_data, metadata_uri)
        print(f"Verification result: {verification_result}")
        
        verification_record = {
            "token_id": token_id,
            "status": verification_result["status"],
            "verified": verification_result["verified"],
            "reason": verification_result.get("reason", ""),
            "verified_at": datetime.utcnow()
        }
        
        verifications_collection.insert_one(verification_record)
        
        return {
            "verified": verification_result["verified"],
            "status": verification_result["status"],
            "message": verification_result.get("reason", ""),
            "confidence": verification_result.get("confidence", "unknown")
        }
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid QR code data format. Expected JSON: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        print(f"Verification error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")

@router.get("/logs")
async def get_verification_logs():
    logs = list(verifications_collection.find().sort("verified_at", -1).limit(50))
    
    for log in logs:
        log["_id"] = str(log["_id"])
        log["verified_at"] = log["verified_at"].isoformat()
        
        ticket = tickets_collection.find_one({"token_id": log["token_id"]})
        if ticket:
            log["ticket_info"] = {
                "event_id": ticket.get("event_id"),
                "owner_address": ticket.get("owner_address")
            }
    
    return logs
