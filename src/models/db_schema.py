from src.database.db_config import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_admin = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    teams = relationship('Team', back_populates='user', cascade='all, delete-orphan')

class Team(Base):
    __tablename__ = 'teams'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    team_name =  Column(String(50), nullable=False)
    description = Column(String(250))
    format = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    user = relationship('User', back_populates='teams')
    members = relationship('TeamMember', back_populates='team', cascade='all, delete-orphan')
    
class TeamMember(Base):
    __tablename__ = 'team_members'
    id =  Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('teams.id', ondelete='CASCADE'), nullable=False)
    pokemon_id = Column(Integer, nullable=False)
    pokemon_name = Column(String(50), nullable=False)
    slot = Column(Integer, nullable=False)
    ability = Column(String(30))
    item = Column(String(30))
    nature = Column(String(30))
    tera_type = Column(String(30))

    team = relationship('Team', back_populates='members')
    moves = relationship('PokemonMove', back_populates='team_member', cascade='all, delete-orphan')
    evs = relationship('PokemonEVs', back_populates='team_member', cascade='all, delete-orphan', uselist=False)
    ivs = relationship('PokemonIVs', back_populates='team_member', cascade='all, delete-orphan', uselist=False)
    
    __table_args__ = (CheckConstraint('slot BETWEEN 1 AND 6', name='chk_team_member_slot'),
                      UniqueConstraint('team_id', 'slot', name='uq_team_member_slot'),
                      UniqueConstraint('team_id', 'pokemon_id', name='uq_team_pokemon'))
    
class PokemonMove(Base):
    __tablename__ = 'pokemon_moves'
    id = Column(Integer, primary_key=True, index=True)
    team_member_id = Column(Integer, ForeignKey('team_members.id', ondelete='CASCADE'), nullable=False)
    move_name = Column(String(50), nullable=False)
    slot = Column(Integer, nullable=False)
    
    team_member = relationship('TeamMember', back_populates='moves')
    
    __table_args__ = (CheckConstraint('slot BETWEEN 1 AND 4', name= 'chk_pokemon_move_slot'),
                      UniqueConstraint('team_member_id', 'slot', name='uq_pokemon_move_slot'),
                      UniqueConstraint('team_member_id', 'move_name', name='uq_pokemon_move'))
    
class PokemonEVs(Base):
    __tablename__ = 'pokemon_evs'
    id = Column(Integer, primary_key=True, index=True)
    team_member_id = Column(Integer, ForeignKey('team_members.id', ondelete='CASCADE'), unique=True, nullable=False)
    hp = Column(Integer, nullable=False, default=0)
    attack = Column(Integer, nullable=False, default=0)
    defense = Column(Integer, nullable=False, default=0)
    sp_attack = Column(Integer, nullable=False, default=0)
    sp_defense = Column(Integer, nullable=False, default=0)
    speed = Column(Integer, nullable=False, default=0)
    
    team_member = relationship('TeamMember', back_populates='evs')
    
    __table_args__ = (CheckConstraint('''hp BETWEEN 0 AND 252 
                                        AND attack BETWEEN 0 AND 252
                                        AND defense BETWEEN 0 AND 252
                                        AND sp_attack BETWEEN 0 AND 252
                                        AND sp_defense BETWEEN 0 AND 252
                                        AND speed BETWEEN 0 AND 252''', name ='chk_valid_evs'),
                      CheckConstraint('(hp + attack + defense + sp_attack + sp_defense + speed) <= 510', name='chk_total_evs'))

class PokemonIVs(Base):
    __tablename__ = 'pokemon_ivs'
    id = Column(Integer, primary_key=True, index=True)
    team_member_id = Column(Integer, ForeignKey('team_members.id', ondelete='CASCADE'), unique=True, nullable=False)
    hp = Column(Integer, nullable=False, default=0)
    attack = Column(Integer, nullable=False, default=0)
    defense = Column(Integer, nullable=False, default=0)
    sp_attack = Column(Integer, nullable=False, default=0)
    sp_defense = Column(Integer, nullable=False, default=0)
    speed = Column(Integer, nullable=False, default=0)
    
    team_member = relationship('TeamMember', back_populates='ivs')
    
    __table_args__ = (CheckConstraint('''hp BETWEEN 0 AND 31 
                                        AND attack BETWEEN 0 AND 31
                                        AND defense BETWEEN 0 AND 31
                                        AND sp_attack BETWEEN 0 AND 31
                                        AND sp_defense BETWEEN 0 AND 31
                                        AND speed BETWEEN 0 AND 31''', name ='chk_valid_ivs'),)