from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context

SQL_ALCHEMY_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQL_ALCHEMY_URL,
    connect_args={"check_same_thread": False},
     poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
         yield db
    finally:
        db.close()

def override_get_current_user():
    return {"username": "bartuonder", "id": 1, "user_role": "admin"}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code!",
        description="Need to learn everyday!",
        priority=5,
        complete=False,
        owner=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield db
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM todos;"))
        conn.commit()



@pytest.fixture
def test_user():
    user = Users(
        username="bartuonder",
        email="bartuonder@gmail.com",
        first_name="Bartu",
        last_name="Onder",
        hashed_password=bcrypt_context.hash("test1234"),
        role="admin",
        phone_number="+1 555 555 555"
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM users;"))
        conn.commit()






