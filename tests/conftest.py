import os
import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from alembic.config import Config
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from alembic import command

os.environ["TESTING"] = "true"
os.environ["DATABASE_URL"] = "sqlite:///./testbase.db"
os.environ["SECRET_KEY"] = (
    "askfgjdgasdfgkgasdkhfhjfgsdakhgasdhfjhasdgfjdafvgasdfhjhsafsjdsdavfokmasvbfkasdvfafiopj"
)
os.environ["access_token_expire_minutes"] = "30"

from app.database import get_db
from app.main import app

load_dotenv()

DB_URL = os.getenv("DATABASE_URL")
engine = create_engine(url=DB_URL, connect_args={"check_same_thread": False})
SessionTesting = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(autouse=True)
def create_tables():
    # usamos ahora las migraciones de alembic
    # para reemplazar el base.metadata.create_all()
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    yield
    command.downgrade(alembic_cfg, "base")


@pytest.fixture
def cliente():
    def get_db_test():
        db = SessionTesting()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = get_db_test
    yield TestClient(app)
    app.dependency_overrides.clear()
