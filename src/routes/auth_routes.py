from src.schemas.user_schemas import UserResponse, UserCreate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database.db_config import get_db
from src.models.db_schema import User
from fastapi.security import OAuth2PasswordRequestForm
from src.core.security import hash_password, verify_password, create_access_token, get_current_user
from src.services.user_service import get_user_by_username, get_user_by_email, get_user_by_identifier

router = APIRouter()

@router.post('/register', response_model=UserResponse, status_code=201)
def register_user(user_data: UserCreate, db : Session = Depends(get_db)):
    existing_username = get_user_by_username(db, user_data.username)   
    if existing_username:
        raise HTTPException(
            status_code=409,
            detail='Username already in use')    
    existing_email = get_user_by_email(db, user_data.email)
    if existing_email:
        raise HTTPException(
                    status_code=409,
                    detail='Email already in use')
    new_user = User(
        username = user_data.username,
        email = user_data.email,
        password_hash = hash_password(user_data.password))
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as error:
        db.rollback()
        print(error)
        raise HTTPException(
        status_code=500,
        detail= 'Error creating user'
        )

@router.post('/login', status_code=200)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = get_user_by_identifier(db, form_data.username)
    if existing_user:
        is_valid = verify_password(form_data.password, existing_user.password_hash)
        if not is_valid:
            raise HTTPException(
                status_code=401,
                detail='Invalid Credentials')

        token = create_access_token(existing_user.id)
        return {'access_token' : token, 'token_type' : 'bearer'}
    else:
        raise HTTPException(
            status_code=401,
            detail='Invalid Credentials')   

@router.get("/test-auth", response_model= UserResponse)
def test_auth(current_user = Depends(get_current_user)):
    return current_user