from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from src.services.user_service import get_user_by_id
from src.database.db_config import get_db
import jwt
import os

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(get_db)):
    try:
        payload = jwt.decode(token,os.getenv("JWT_SECRET_KEY"),algorithms=[os.getenv("ALGORITHM")])
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(
             status_code=401,
             detail="Invalid Token")
        user = get_user_by_id(db, int(user_id))
        if user is None:
            raise HTTPException(status_code=401, detail='Invalid Token')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid Token')
    return user
    

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password : str) -> bool:
        return password_hash.verify(password, hashed_password)

def create_access_token(user_id : int) -> str:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    
    expiration = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    payload = {'sub' : str(user_id),'exp' : expiration}
    
    token = jwt.encode(payload, key=os.getenv('JWT_SECRET_KEY'), algorithm= os.getenv('ALGORITHM'))
    return token