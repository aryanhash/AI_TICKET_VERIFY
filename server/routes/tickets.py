from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from server.models.ticket import TicketMintRequest
from server.database import tickets_collection, events_collection
from server.services.blockchain import blockchain_service
from server.services.ipfs_service import ipfs_service
from datetime import datetime
from bson import ObjectId
import json

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/mint")
async def mint_ticket(
    event_id: str = Form(...),
    wallet_address: str = Form(...),
    buyer_image: UploadFile = File(...)
):
    event = events_collection.find_one({"_id": ObjectId(event_id)})
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    if event["sold_count"] >= event["total_supply"]:
        raise HTTPException(status_code=400, detail="Event sold out")
    
    image_data = await buyer_image.read()
    buyer_image_uri = await ipfs_service.upload_file(image_data, buyer_image.filename)
    
    if not buyer_image_uri:
        raise HTTPException(status_code=500, detail="Failed to upload buyer image")
    
    metadata = {
        "name": f"{event['title']} - Ticket",
        "description": f"NFT Ticket for {event['title']} at {event['venue']}",
        "image": buyer_image_uri,
        "attributes": [
            {"trait_type": "Event", "value": event["title"]},
            {"trait_type": "Venue", "value": event["venue"]},
            {"trait_type": "Date", "value": event["date"].isoformat()},
            {"trait_type": "Price", "value": str(event["ticket_price"])}
        ],
        "event_id": event_id,
        "buyer_address": wallet_address.lower()
    }
    
    metadata_uri = await ipfs_service.upload_json(metadata)
    
    if not metadata_uri:
        raise HTTPException(status_code=500, detail="Failed to upload metadata")
    
    mint_result = await blockchain_service.mint_ticket(wallet_address, metadata_uri)
    
    if not mint_result.get("success"):
        raise HTTPException(status_code=500, detail=f"Minting failed: {mint_result.get('error')}")
    
    qr_data = json.dumps({
        "token_id": mint_result["token_id"],
        "event_id": event_id,
        "metadata_uri": metadata_uri
    })
    
    ticket_data = {
        "token_id": mint_result["token_id"],
        "event_id": event_id,
        "owner_address": wallet_address.lower(),
        "metadata_uri": metadata_uri,
        "qr_code_data": qr_data,
        "tx_hash": mint_result["tx_hash"],
        "minted_at": datetime.utcnow()
    }
    
    tickets_collection.insert_one(ticket_data)
    
    events_collection.update_one(
        {"_id": ObjectId(event_id)},
        {"$inc": {"sold_count": 1}}
    )
    
    return {
        "message": "Ticket minted successfully",
        "token_id": mint_result["token_id"],
        "tx_hash": mint_result["tx_hash"],
        "qr_code_data": qr_data,
        "metadata_uri": metadata_uri
    }

@router.get("/{wallet_address}")
async def get_user_tickets(wallet_address: str):
    blockchain_tickets = await blockchain_service.get_tickets_of_owner(wallet_address)
    
    tickets = list(tickets_collection.find({"owner_address": wallet_address.lower()}))
    
    for ticket in tickets:
        ticket["_id"] = str(ticket["_id"])
        ticket["minted_at"] = ticket["minted_at"].isoformat()
        
        event = events_collection.find_one({"_id": ObjectId(ticket["event_id"])})
        if event:
            ticket["event"] = {
                "title": event["title"],
                "venue": event["venue"],
                "date": event["date"].isoformat()
            }
    
    return {
        "tickets": tickets,
        "blockchain_tickets": blockchain_tickets
    }
