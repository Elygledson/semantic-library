import bcrypt

from models import User
from http import HTTPStatus
from zoneinfo import ZoneInfo
from jwt import encode, decode
from sqlalchemy.orm import Session
from config import get_db, settings
from schemas import UserProfileSchema
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthenticationRepository:
    def __init__(self, db: Session):
        self.db = db

    @property
    def _entity(self):
        return User

    def create_access_token(self, data) -> str:
        to_encode = data.dict().copy() if hasattr(data, 'dict') else data.copy()
        expire = datetime.now(tz=ZoneInfo('UTC')) + \
            timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        encoded_jwt = encode(
            to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_user(self, data) -> User | None:
        user: User | None = self.db.query(self._entity).filter(
            self._entity.email == data.email
        ).first()

        if not user:
            return None

        password_attempt = data.password.encode('utf-8')
        stored_hash = user.password.encode('utf-8')
        if bcrypt.checkpw(password_attempt, stored_hash):
            return user
        return None

    @staticmethod
    def decode_token(credentials: str) -> dict:
        return decode(credentials, settings.SECRET_KEY, algorithms=[ALGORITHM])

    @staticmethod
    def get_current_user(token: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> UserProfileSchema:
        try:
            decoded_token = AuthenticationRepository.decode_token(
                token.credentials)

            email = decoded_token.get("sub")

            user: User | None = db.query(User).filter(
                User.email == email).first()

            if user is None:
                raise HTTPException(
                    status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado.")

            return UserProfileSchema.model_validate(user)
        except:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Acesso não autorizado.",
                headers={"WWW-Authenticate": "Bearer"},
            )
