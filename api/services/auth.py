from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories import AuthenticationRepository
from schemas import LoginResponseSchema, AuthSchema, UserProfileSchema


class AuthService:
    def __init__(self, db: Session):
        self.auth_repository = AuthenticationRepository(db)

    def login(self, auth_schema: AuthSchema) -> LoginResponseSchema:
        try:
            existing_user = self.auth_repository.verify_user(auth_schema)

            if not existing_user:
                raise HTTPException(status_code=status.BAD_REQUEST,
                                    detail='Email ou Senha incorretos.')

            access_token = self.auth_repository.create_access_token(
                data={'sub': existing_user.email})

            user_profile_schema = UserProfileSchema.model_validate(
                existing_user)

            return LoginResponseSchema(usuario=user_profile_schema, token=access_token, tipo_token='Bearer')
        except HTTPException as http_exc:
            raise http_exc
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Ocorreu um erro ao fazer login. {e}")
