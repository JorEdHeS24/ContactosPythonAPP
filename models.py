from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from typing import Dict, Union

Base = declarative_base()

class Contacto(Base):
    __tablename__ = 'contactos'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    telephone = Column(String(20), nullable=False)
    email = Column(String(100))
    
    def to_dict(self) -> Dict[str, Union[str, int]]:
        return {
            'id': self.id,
            'name': self.name,
            'telephone': self.telephone,
            'email': self.email
        }
    
    def __str__(self) -> str:
        return f"(id={self.id}, nombre={self.name}, telefono={self.telephone}, email={self.email})"
    
    def __repr__(self) -> str:
        return self.__str__()