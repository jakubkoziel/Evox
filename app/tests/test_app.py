import pytest
from fastapi import Depends

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from ..database import Base, get_db
from ..main import app
from .. import security

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



def test_create_user():
    response = client.post(
        "/messages/",
        json={"content": "New content"},
        headers={"Authorization": security.API_KEY}
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["content"] == "New content"
    assert "id" in data
    message_id = data["id"]

    response = client.get(f"/messages/{message_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["content"] == "New content"
    assert data["counter"] == 1




from app.services.message import create
from app import schemas

def test_delete_message():
    message = create(schemas.Message(content="New content"),  next(get_db()))
    _id = message.id

    response = client.delete(
        f"/messages/{_id}", headers={"Authorization": security.API_KEY}
    )

    assert response.status_code == 200

    next(get_db()).commit()

    # with pytest.raises(MessageNotFoundException):
    #     services.messages.get_by_id(db=db, _id=_id)


