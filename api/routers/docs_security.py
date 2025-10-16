import secrets

from config import settings
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html

security = HTTPBasic()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, settings.SWAGGER_USERNAME)
    correct_password = secrets.compare_digest(
        credentials.password, settings.SWAGGER_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Basic"},
        )


def setup_docs(app: FastAPI):
    @app.get("/docs", include_in_schema=False)
    async def get_documentation(credentials: HTTPBasicCredentials = Depends(authenticate)):
        return get_swagger_ui_html(openapi_url="/openapi.json", title="Docs")

    @app.get("/redoc", include_in_schema=False)
    async def get_redoc(credentials: HTTPBasicCredentials = Depends(authenticate)):
        return get_redoc_html(openapi_url="/openapi.json", title="ReDoc")

    @app.get("/openapi.json", include_in_schema=False)
    async def openapi(credentials: HTTPBasicCredentials = Depends(authenticate)):
        return get_openapi(title=app.title, version="1.0.0", routes=app.routes)
