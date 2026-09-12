from fastapi import APIRouter, Depends, HTTPException
from src.schemas.moves_schemas import MovePreviewResponse, MoveCreate, MoveResponse, MoveFullResponse
from src.database.db_config import get_db
from sqlalchemy.orm import Session
from src.core.security import get_current_user
from src.models.db_schema import Moves, TeamMember, Team, PokemonMove
from src.services.pokeapi import get_pokemon_moves_from_pokeapi

router = APIRouter(prefix='/moves')

@router.get("/all",response_model=list[MovePreviewResponse],status_code=200)
def get_moves(search: str | None = None,db: Session = Depends(get_db)):
    query = db.query(Moves)
    if search:
        query = query.filter(Moves.name.ilike(f"%{search}%"))
    return (query.order_by(Moves.name).limit(50).all())

@router.get('/{pokemon}', response_model=list[MoveFullResponse], status_code=200)
def get_moves_from_pokemon(pokemon : str, db : Session = Depends(get_db)):
   moves = get_pokemon_moves_from_pokeapi(pokemon)
   get_moves = db.query(Moves).filter(Moves.name.in_(moves['moves'])).all()
   return get_moves

@router.post('/create', response_model=MoveResponse, status_code=201)
def create_move_set(move_data: MoveCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db),):
    team_member = db.query(TeamMember).filter(TeamMember.id == move_data.team_member_id).first() #Valida que el miembro del equipo comparta id
    if not team_member:
        raise HTTPException(
            status_code=404,
            detail='Pokemon not found in the team')
    validate = db.query(Team).filter(Team.id == team_member.team_id, Team.user_id == current_user.id).first() #Valida el ID del team y el current user
    if not validate:
        raise HTTPException(
            status_code=404,
            detail='That Pokemon is not in your team')
    validate_move = db.query(Moves).filter(Moves.id == move_data.move_id).first() #Valida que el movimiento este dentro de la tabla moves
    if not validate_move:
        raise HTTPException(
            status_code=404,
            detail='Movement not found')
    moves_data = get_pokemon_moves_from_pokeapi(team_member.pokemon_name)
    if not moves_data or "moves" not in moves_data:
        raise HTTPException(
            status_code=400,
            detail=f'Could not fetch moves for {team_member.pokemon_name} from PokeAPI')
    allowed_moves = [m.lower().replace('-', ' ') for m in moves_data["moves"]]
    target_move_name = validate_move.name.lower().replace('-', ' ')
    if target_move_name not in allowed_moves:
        raise HTTPException(
            status_code=400,
            detail=f'{team_member.pokemon_name} can not learn {validate_move.name}')
    current_moves = db.query(PokemonMove).filter(PokemonMove.team_member_id == team_member.id).all()
    if len(current_moves) >= 4:
        raise HTTPException(
            status_code=400,
            detail='This Pokemon already has 4 moves assigned')
    if any(m.move_id == move_data.move_id for m in current_moves):
        raise HTTPException(
            status_code=400,
            detail='Move already equipped on this Pokemon')
    if any(m.slot == move_data.slot for m in current_moves):
        raise HTTPException(
            status_code=400,
            detail=f'Slot {move_data.slot} is already occupied')
    new_pokemon_move = PokemonMove(
            team_member_id=move_data.team_member_id,
            move_id=move_data.move_id,
            slot=move_data.slot)
    db.add(new_pokemon_move)
    db.commit()
    db.refresh(new_pokemon_move)
    return new_pokemon_move