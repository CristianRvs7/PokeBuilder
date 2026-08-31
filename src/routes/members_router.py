from fastapi import APIRouter, HTTPException, Depends
from src.services.pokeapi import get_pokemon_from_pokeapi
from src.models.db_schema import Team, TeamMember
from src.core.security import get_current_user
from sqlalchemy.orm import Session
from src.database.db_config import get_db
from src.schemas.members_schemas import MemberCreate, MemberResponse, MemberUpdate

router = APIRouter()

@router.get('/pokemon/{name_or_id}')
def get_pokemon(name_or_id: str):
    pokemon = get_pokemon_from_pokeapi(name_or_id)

    if not pokemon:
        raise HTTPException(
            status_code=404,
            detail="Pokemon not found"
        )

    return pokemon

@router.post('/{team_id}/members', status_code=201)
def add_a_member(member_data : MemberCreate, team_id : int, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    team = db.query(Team).filter(Team.user_id == current_user.id, Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=404,
            detail= 'Team not found'
        )
    pokemon_data = get_pokemon_from_pokeapi(str(member_data.pokemon_name))
    try:
        new_member = TeamMember(
            team_id = team.id,
            pokemon_id = pokemon_data['id'],
            pokemon_name = pokemon_data['name'],
            slot = member_data.slot,
            ability = member_data.ability,
            item = member_data.item,
            nature = member_data.nature,
            tera_type = member_data.tera_type)
        db.add(new_member)
        db.commit()
        db.refresh(new_member) 
        return new_member
    except Exception as error:
        db.rollback()
        print(error)
        raise HTTPException(
            status_code=500,
            detail='Error, please check the information'
        )
        

@router.get('/{team_id}/members', response_model= list[MemberResponse], status_code=200)
def get_team_members(team_id : int, current_user = Depends(get_current_user), db : Session = Depends(get_db)):
    team = db.query(Team).filter(Team.user_id == current_user.id, Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=404,
            detail='Team not found'
        )
    members = db.query(TeamMember).filter(TeamMember.team_id == team_id).order_by(TeamMember.slot).all()
    
    return members

@router.delete('/{team_id}/members/{member_slot}', status_code=204)
def delete_member(team_id : int, member_slot : int, current_user = Depends(get_current_user), db : Session = Depends(get_db)):
    team = db.query(Team).filter(Team.user_id == current_user.id, Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=404,
            detail='Team not found'
        )
    team_member = db.query(TeamMember).filter(TeamMember.team_id == team.id, TeamMember.slot == member_slot).first()
    if not team_member:
                raise HTTPException(
            status_code=404,
            detail='Member not found'
        )
    db.delete(team_member)
    db.commit()

@router.patch(
    "/{team_id}/member/{member_slot}",
    response_model=MemberResponse,
    status_code=200
)
def team_member_update(team_id: int,member_slot: int,member_new_data: MemberUpdate,current_user=Depends(get_current_user),db: Session=Depends(get_db)):
    team = db.query(Team).filter(Team.user_id == current_user.id,Team.id == team_id).first()
    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    team_member = db.query(TeamMember).filter(TeamMember.team_id == team.id,TeamMember.slot == member_slot).first()
    if not team_member:
        raise HTTPException(
            status_code=404,
            detail="Member not found")
    update_data = member_new_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(team_member, field, value)
    db.commit()
    db.refresh(team_member)
    return team_member 