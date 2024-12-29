from datetime import datetime, timedelta
from sqlmodel import select
from utils.models import *

def test_get_trainers(test_client):
    response = test_client.get("/api/admin/trainers")
    assert response.status_code == 200
    trainers = response.json()
    assert isinstance(trainers, list)
    assert len(trainers) >= 2
    assert trainers[0]["name"] == "Test Trainer 1"

def test_add_trainer(test_client):
    data = {
        "name": "Test Trainer 3",
        "description": "Test Trainer 3 description",
        "specialization": "Test Trainer 3 specialization",
        "photo": "Test Trainer 3 photo"
    }
    response = test_client.post("/api/admin/trainer/add", json=data)

    json_response = response.json()
    assert "trainer_id" in json_response

def test_add_trainer_without_parametrs(test_client):
    data = {
        "description": "Test Trainer 3 description",
        "specialization": "Test Trainer 3 specialization",
        "photo": "Test Trainer 3 photo"
    }
    response = test_client.post("/api/admin/trainer/add", json=data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Имя и Специализация обязательны"}

def test_add_existing_trainer(test_client, test_session):
    existing_trainer = {
        "name": "Test Trainer 1",
        "specialization": "Yoga"
    }
    response = test_client.post("/api/admin/trainer/add", json=existing_trainer)
    assert response.status_code == 400
    assert response.json() == {"detail": "Тренер уже существует"}
    
def test_get_services(test_client):
    response = test_client.get("/api/admin/services")
    assert response.status_code == 200
    services = response.json()
    assert isinstance(services, list)
    assert len(services) >= 2
    assert services[0]["name"] == "Test Service 1"
