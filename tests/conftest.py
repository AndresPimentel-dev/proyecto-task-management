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
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://postgres:postgres_test_password@localhost:5433/taskforge_test_db",
)
os.environ.setdefault(
    "SECRET_KEY",
    "askfgjdgasdfgkgasdkhfhjfgsdakhgasdhfjhasdgfjdafvgasdfhjhsafsjdsdavfokmasvbfkasdvfafiopj",
)
os.environ.setdefault("algorithm", "HS256")
os.environ.setdefault("access_token_expire_minutes", "30")

load_dotenv()

from app.config import settings
from app.database import get_db
from app.main import app

DB_URL = settings.DATABASE_URL
engine = create_engine(url=DB_URL)
SessionTesting = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(autouse=True)
def create_tables():
    # usamos ahora las migraciones de alembic en la base de datos postgres de pruebas
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
