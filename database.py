from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

ENGINE = create_engine('sqlite:///contacts.db')
SessionLocal = sessionmaker(bind=ENGINE)

def init_db() -> None:
    # Crea las tablas si no existen
    Base.metadata.create_all(ENGINE)