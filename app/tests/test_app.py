from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base, get_db
from ..main import app
from .. import security

from app.services import message as message_service
from app import schemas

# create connection to database designed for tests
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


db = next(override_get_db())
app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


## Test part
def test_create_message():
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


def test_get_message():
    message = message_service.create(schemas.Message(content="New content"), db)
    id = message.id

    response = client.get(
        f"/messages/{id}", headers={"Authorization": security.API_KEY}
    )

    assert response.status_code == 200

    data = response.json()
    assert data['content'] == 'New content'
    assert data['counter'] == 1


def test_delete_message():
    message = message_service.create(schemas.Message(content="New content"), db)
    id = message.id

    response = client.delete(
        f"/messages/{id}", headers={"Authorization": security.API_KEY}
    )

    assert response.status_code == 200

    data = response.json()
    assert data == {}


def test_delete_messege_not_found_exception():
    message = message_service.create(schemas.Message(content="New content"), db)
    id = message.id

    message_id = id + 1  # wrong id

    response = client.delete(
        f"/messages/{message_id}", headers={"Authorization": security.API_KEY}
    )

    assert response.status_code == 404

    data = response.json()
    assert data['detail'] == f'Message with id {message_id} not found.'


def test_put_message():
    message = message_service.create(schemas.Message(content="New content"), db)
    id = message.id

    response = client.put(
        f"/messages/{id}",
        json={"content": "updated content"},
        headers={"Authorization": security.API_KEY}
    )

    assert response.status_code == 200

    data = response.json()
    assert data['content'] == 'updated content'


def test_increase_counter_message():
    message = message_service.create(schemas.Message(content="TEST CONTENT"), db)
    id = message.id

    response = client.get(
        f"/messages/{id}", headers={"Authorization": security.API_KEY}
    )

    assert response.status_code == 200

    data = response.json()
    assert data['counter'] == 1

    response = client.get(
        f"/messages/{id}", headers={"Authorization": security.API_KEY}
    )

    assert response.status_code == 200

    data = response.json()
    assert data['counter'] == 2
