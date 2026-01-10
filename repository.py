from database import SessionLocal
from models import Contacto

class ContactoRepository:
    @staticmethod
    def guardar(nombre, telefono, email):
        with SessionLocal() as session:
            nuevo = Contacto(nombre=nombre, telefono=telefono, email=email)
            session.add(nuevo)
            session.commit()
            return nuevo

    @staticmethod
    def obtener_todos():
        with SessionLocal() as session:
            contactos = session.query(Contacto).all()
            return [contacto.to_dict() for contacto in contactos]