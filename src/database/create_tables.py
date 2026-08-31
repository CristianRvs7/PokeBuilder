from src.database.db_config import Base, engine
from src.models.db_schema import User, Team, TeamMember, PokemonMove, PokemonEVs, PokemonIVs

Base.metadata.create_all(bind = engine)

print('Tablas creadas correctamente')