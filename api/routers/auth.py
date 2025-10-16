from config import get_db
from services import AuthService
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from schemas import LoginResponseSchema, AuthSchema

authentication = APIRouter()


@authentication.post('/auth/login/', response_model=LoginResponseSchema, summary="Autenticação")
def login(auth_data: AuthSchema, db: Session = Depends(get_db)):
    return AuthService(db).login(auth_data)
