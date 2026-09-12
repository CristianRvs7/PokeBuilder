from pydantic import BaseModel, Field
from typing import Optional
from pydantic import BaseModel


class MovePreviewResponse(BaseModel):
    id: int
    name: str
    power: int | None
    accuracy: int | None
    pp: int | None
    damage_class: str
    type: str

    model_config = {
        "from_attributes": True
    }
    
class MoveFullResponse(BaseModel):
    id: int
    pokeapi_id: int
    name: str
    power: int | None
    accuracy: int | None
    pp: int | None
    damage_class: str
    type: str
    description: str

    model_config = {
        "from_attributes": True
    }
    
class MoveCreate(BaseModel):
    team_member_id : int = Field(...)
    move_id : int = Field(...)
    slot : int = Field(..., ge=1, le=4)

class MoveResponse(BaseModel):
    team_member_id : int
    move_id : int
    slot : int
    
    model_config = {
        "from_attributes": True
    }
    