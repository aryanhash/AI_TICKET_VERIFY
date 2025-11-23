from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Event(BaseModel):
    title: str
    description: str
    date: datetime
    venue: str
    image_url: str
    ticket_price: float
    total_supply: int
    sold_count: int = 0
    organizer_address: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class EventCreate(BaseModel):
    title: str
    description: str
    date: datetime
    venue: str
    ticket_price: float
    total_supply: int
