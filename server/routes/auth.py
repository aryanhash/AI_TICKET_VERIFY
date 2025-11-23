from fastapi import APIRouter, HTTPException
from server.models.user import UserCreate
from server.database import users_collection
from server.services.blockchain import blockchain_service
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/wallet")
async def wallet_login(user_data: UserCreate):
    if not blockchain_service.verify_signature(
        user_data.message,
        user_data.signature,
        user_data.wallet_address
    ):
        raise HTTPException(status_code=401, detail="Invalid signature")
    
    existing_user = users_collection.find_one({"wallet_address": user_data.wallet_address.lower()})
    
    if not existing_user:
        new_user = {
            "wallet_address": user_data.wallet_address.lower(),
            "is_organizer": False,
            "created_at": datetime.utcnow()
        }
        users_collection.insert_one(new_user)
        return {"message": "User created", "wallet_address": user_data.wallet_address.lower(), "is_organizer": False}
    
    return {
        "message": "Login successful",
        "wallet_address": existing_user["wallet_address"],
        "is_organizer": existing_user.get("is_organizer", False)
    }

@router.post("/make-organizer/{wallet_address}")
async def make_organizer(wallet_address: str):
    result = users_collection.update_one(
        {"wallet_address": wallet_address.lower()},
        {"$set": {"is_organizer": True}}
    )
    
    if result.modified_count > 0:
        return {"message": "User is now an organizer"}
    
    raise HTTPException(status_code=404, detail="User not found")
