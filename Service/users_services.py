import bcrypt
from models.models_user import User
from sqlalchemy.orm import Session

class UsersService:
    def __init__(self, db: Session):
        self.db = db
        self.model = User 

    def _hash_password(self, password: str) -> str:
        """Genera un hash seguro de la contraseña"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def create_user(self, username, password):
        existing_user = self.db.query(User).filter_by(username=username).first()
        if existing_user:
            raise ValueError("El nombre de usuario ya existe")

        hashed_password = self._hash_password(password)
        new_user = User(username=username, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        return new_user

    def authenticate_user(self, username, password):
        user = self.db.query(self.model).filter_by(username=username).first()
        if user and self._verify_password(password, user.password):
            return user
        return None

    def get_all_users(self):
        return self.db.query(self.model).all()


    def get_user_by_id(self, user_id):
        return self.db.query(self.model).filter_by(id=user_id).first()


    def update_user(self, user_id, username=None, password=None):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if password:
            user.password = self._hash_password(password)
        self.db.commit()
        self.db.refresh(user)
        return user


    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        self.db.delete(user)
        self.db.commit()
        return True
