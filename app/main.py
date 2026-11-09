from typing import Annotated

from fastapi import Depends, FastAPI, Response, status
from sqlalchemy import Engine, text
from sqlalchemy.exc import SQLAlchemyError

from app.db import get_engine

app = FastAPI(title="TaskFlow API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready")
def readiness(response: Response, engine: Annotated[Engine, Depends(get_engine)]) -> dict[str, str]:
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unavailable"}
    return {"status": "ok"}
