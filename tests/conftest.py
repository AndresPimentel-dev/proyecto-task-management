import os
from pathlib import Path
import sys

# Asegurar que el directorio raíz del proyecto esté en sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from alembic import command  # noqa: E402
from alembic.config import Config  # noqa: E402
from dotenv import load_dotenv  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
import pytest  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

os.environ["DATABASE_URL"] = "sqlite:///./testbase.db"
os.environ["SECRET_KEY"] = (
    "askfgjdgasdfgkgasdkhfhjfgsdakhgasdhfjhasdgfjdafvgasdfhjhsafsjdsdavfokmasvbfkasdvfafiopj"
)
os.environ["access_token_expire_minutes"] = "30"

from app.database import get_db  # noqa: E402
from app.main import app  # noqa: E402

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
