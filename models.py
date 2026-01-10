from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Contacto(Base):
    __tablename__ = 'contactos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20), nullable=False)
    email = Column(String(100))
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email
        }
    
    def __str__(self):
        return f"(id={self.id}, nombre={self.nombre}, telefono={self.telefono}, email={self.email})"
    
    def __repr__(self):
        return self.__str__()