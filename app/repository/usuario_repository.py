# app/repository/usuario_repository.py
from sqlalchemy.orm import Session
from models import Usuario as UsuarioModel


class UsuarioRepository:
    
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, usuario_id: int):
        return self.db.query(UsuarioModel).filter(UsuarioModel.id_usuario == usuario_id).first()
    
    def get_by_email(self, email: str):
        return self.db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    
    def get_all(self):
        return self.db.query(UsuarioModel).all()