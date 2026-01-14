from database import SessionLocal
from models import Contacto
from typing import List, Dict, Optional, Any

class ContactoRepository:
    @staticmethod
    def guardar(name: str, telephone: str, email: Optional[str]) -> Contacto:
        with SessionLocal() as session:
            nuevo = Contacto(name=name, telephone=telephone, email=email)
            session.add(nuevo)
            session.commit()
            return nuevo

    @staticmethod
    def obtener_todos() -> List[Dict[str, Any]]:
        with SessionLocal() as session:
            contactos = session.query(Contacto).all()
            return [contacto.to_dict() for contacto in contactos]

    @staticmethod
    def actualizar(id: int, name: str, telephone: str, email: Optional[str]) -> None:
        with SessionLocal() as session:
            contacto = session.query(Contacto).get(id)
            if contacto:
                contacto.name = name
                contacto.telephone = telephone
                contacto.email = email
                session.commit()

    @staticmethod
    def eliminar(id: int) -> None:
        with SessionLocal() as session:
            contacto = session.query(Contacto).get(id)
            if contacto:
                session.delete(contacto)
                session.commit()