from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class User(BaseModel):
    wallet_address: str
    is_organizer: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class UserCreate(BaseModel):
    wallet_address: str
    signature: str
    message: str
