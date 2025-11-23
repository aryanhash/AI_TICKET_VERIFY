from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Ticket(BaseModel):
    token_id: int
    event_id: str
    owner_address: str
    metadata_uri: str
    qr_code_data: str
    minted_at: datetime = Field(default_factory=datetime.utcnow)
    
class TicketMintRequest(BaseModel):
    event_id: str
    wallet_address: str
    buyer_image_url: str
