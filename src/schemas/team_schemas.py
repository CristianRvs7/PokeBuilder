from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TeamCreate(BaseModel):
    team_name : str = Field(...,min_length=1, max_length=50)
    description : str = Field(..., max_length=250)
    format : str = Field(..., max_length=50)
    
class TeamResponse(BaseModel):
    id : int
    team_name : str
    description : str
    format : str
    created_at : datetime
    
    model_config = {
        'from_attributes' : True
    }

class TeamUpdate(BaseModel):
    team_name : Optional[str] = Field(None, min_length= 1, max_length=50)
    description : Optional[str] = Field(None, max_length=250)
    format : Optional[str] = Field(None, max_length=50)