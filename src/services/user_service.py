from src.database.db_config import get_db
from sqlalchemy.orm import Session
from src.models.db_schema import User
from sqlalchemy import or_

def get_user_by_username(db : Session, username : str):
    user = db.query(User).filter(User.username == username).first()
    return user

def get_user_by_email(db : Session, email : str):
    user = db.query(User).filter(User.email == email).first()
    return user

def get_user_by_identifier(db : Session, identifier : str):
    user = db.query(User).filter(or_(User.email == identifier, User.username == identifier)).first()
    return user

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()