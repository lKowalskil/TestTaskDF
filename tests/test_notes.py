import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app.models import Note, NoteVersion
from app.services.ai_service import summarize_text

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def mock_summarize_text(text):
    return f"Mock summary: {text[:20]}..."

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[summarize_text] = mock_summarize_text

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_note():
    response = client.post(
        "/api/notes/",
        json={"title": "Test Note", "content": "This is a test note content."}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note content."
    assert "id" in data

def test_read_notes():
    response = client.post(
        "/api/notes/",
        json={"title": "Test Note 1", "content": "Content 1"}
    )
    
    response = client.get("/api/notes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["title"] == "Test Note 1"
    assert data[0]["content"] == "Content 1"

def test_update_note():
    response = client.post(
        "/api/notes/",
        json={"title": "Original Title", "content": "Original content"}
    )
    note_id = response.json()["id"]
    
    response = client.put(
        f"/api/notes/{note_id}",
        json={"title": "Updated Title", "content": "Updated content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"
    
    response = client.get(f"/api/notes/{note_id}")
    data = response.json()
    assert len(data["versions"]) == 2
    assert data["versions"][0]["version_number"] == 1
    assert data["versions"][1]["version_number"] == 2

def test_delete_note():
    response = client.post(
        "/api/notes/",
        json={"title": "Note to Delete", "content": "This will be deleted"}
    )
    note_id = response.json()["id"]
    
    response = client.delete(f"/api/notes/{note_id}")
    assert response.status_code == 204
    
    response = client.get(f"/api/notes/{note_id}")
    assert response.status_code == 404