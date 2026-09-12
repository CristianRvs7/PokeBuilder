from pydantic import BaseModel, Field
from typing import Optional

class MemberCreate(BaseModel):
    pokemon_name : str = Field(..., max_length=50)
    slot : int = Field(..., ge=1, le=6)
    ability : Optional[str] = Field(None, max_length=30)
    item : Optional[str] = Field(None, max_length=30)
    nature : Optional[str] = Field(None, max_length=30)
    tera_type : Optional[str] = Field(None, max_length=30)
    
class MemberResponse(BaseModel):
    id: int
    pokemon_id: int
    pokemon_name: str
    slot: int
    ability: str | None
    item: str | None
    nature: str | None
    tera_type: str | None

class MemberUpdate(BaseModel):
    slot: Optional[int] = Field(None, ge=1, le=6)
    ability: Optional[str] = Field(None, max_length=30)
    item: Optional[str] = Field(None, max_length=30)
    nature: Optional[str] = Field(None, max_length=30)
    tera_type: Optional[str] = Field(None, max_length=30)
    
class MemberFullView(BaseModel):
    pokemon_name : Optional[str] = Field(None, max_length=50)
    slot : Optional[int] = Field(None, ge=1, le=6)
    nature : Optional[str] = Field(None, max_length=30)
    ability : Optional[str] = Field(None, max_length=30)
    item : Optional[str] = Field(None, max_length=30)
    movslot1 : Optional[str] = Field(None)
    movslot2 : Optional[str] = Field(None)
    movslot3 : Optional[str] = Field(None)
    movslot4 : Optional[str] = Field(None)
    
    model_config = {
            "from_attributes": True
        }