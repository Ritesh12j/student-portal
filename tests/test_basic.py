from app import create_app
from app.extensions import db
import tempfile, os
import pytest

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}"
    })
    with app.app_context():
        db.create_all()
    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json() == {"status": "ok"}

def test_add_and_list(client):
    r = client.post("/students", json={"name":"Alice","email":"alice@example.com","course":"BCA"})
    assert r.status_code == 201
    res = client.get("/students")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list)
    assert data[0]["name"] == "Alice"
