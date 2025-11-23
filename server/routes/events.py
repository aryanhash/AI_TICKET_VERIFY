from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from models.event import EventCreate
from database import events_collection, users_collection
from services.ipfs_service import ipfs_service
from datetime import datetime
from bson import ObjectId
from typing import Optional

router = APIRouter(prefix="/events", tags=["events"])

@router.post("")
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    venue: str = Form(...),
    ticket_price: float = Form(...),
    total_supply: int = Form(...),
    organizer_address: str = Form(...),
    image: UploadFile = File(...)
):
    user = users_collection.find_one({"wallet_address": organizer_address.lower()})
    if not user or not user.get("is_organizer", False):
        raise HTTPException(status_code=403, detail="Only organizers can create events")
    
    image_data = await image.read()
    image_uri = await ipfs_service.upload_file(image_data, image.filename or "event_image.jpg")
    
    if not image_uri:
        raise HTTPException(status_code=500, detail="Failed to upload image to IPFS")
    
    event_data = {
        "title": title,
        "description": description,
        "date": datetime.fromisoformat(date.replace('Z', '+00:00')),
        "venue": venue,
        "image_url": image_uri,
        "ticket_price": ticket_price,
        "total_supply": total_supply,
        "sold_count": 0,
        "organizer_address": organizer_address.lower(),
        "created_at": datetime.utcnow()
    }
    
    result = events_collection.insert_one(event_data)
    event_data["_id"] = str(result.inserted_id)
    
    return {"message": "Event created", "event_id": str(result.inserted_id), "event": event_data}

@router.get("")
async def get_events():
    events = list(events_collection.find())
    for event in events:
        event["_id"] = str(event["_id"])
        event["date"] = event["date"].isoformat()
        event["created_at"] = event["created_at"].isoformat()
    return events

@router.get("/{event_id}")
async def get_event(event_id: str):
    try:
        event = events_collection.find_one({"_id": ObjectId(event_id)})
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        
        event["_id"] = str(event["_id"])
        event["date"] = event["date"].isoformat()
        event["created_at"] = event["created_at"].isoformat()
        return event
    except:
        raise HTTPException(status_code=400, detail="Invalid event ID")
