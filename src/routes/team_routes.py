from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.db_schema import Team, User, TeamMember
from src.core.security import get_current_user
from src.database.db_config import get_db
from src.schemas.team_schemas import TeamCreate, TeamResponse, TeamUpdate

router = APIRouter(prefix='/teams')

@router.post('/create', response_model=TeamResponse, status_code=201)
def create_team( team_data : TeamCreate, db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
            new_team = Team(
            user_id = current_user.id,
            team_name = team_data.team_name,
            description = team_data.description,
            format = team_data.format
            )    
            db.add(new_team)
            db.commit()
            db.refresh(new_team)
            return new_team

@router.get("/", status_code=200)
def get_teams(current_user: User = Depends(get_current_user),db: Session = Depends(get_db)):
    teams = (db.query(Team).filter(Team.user_id == current_user.id).all())
    if not teams:
        return []
    teams_response = []
    for team in teams:
        members = (db.query(TeamMember).filter(TeamMember.team_id == team.id).order_by(TeamMember.slot).all())
        teams_response.append({
            "id": team.id,
            "team_name": team.team_name,
            "description": team.description,
            "format": team.format,
            "created_at": team.created_at,
            "members": [
                {
                    "id": member.id,
                    "pokemon_id": member.pokemon_id,
                    "pokemon_name": member.pokemon_name,
                    "slot": member.slot
                }
                for member in members
            ]
        })
    return teams_response

@router.get('/{team_id}', response_model=TeamResponse, status_code=200)
def get_team_by_id(team_id : int, current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    team = db.query(Team).filter(Team.user_id == current_user.id, Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=404,
            detail='Team not found'
        )
    return team

@router.patch('/edit/{team_id}', response_model=TeamResponse, status_code=200)
def edit_team_info(team_id : int, team_new_data : TeamUpdate, current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    team_data = db.query(Team).filter(Team.user_id == current_user.id, Team.id == team_id).first()
    if not team_data:
        raise HTTPException(
            status_code=404,
            detail='Team not found'
        )
    update_data = team_new_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(team_data, field, value)
    db.commit()
    db.refresh(team_data)
    return team_data

@router.delete('/{team_id}', status_code=204)
def delete_team(team_id : int, current_user = Depends(get_current_user), db : Session = Depends(get_db)):
    team = db.query(Team).filter(Team.user_id == current_user.id, Team.id == team_id).first()
    if not team:
        raise HTTPException(
        status_code=404,
        detail="Team not found"
    )
    db.delete(team)
    db.commit()