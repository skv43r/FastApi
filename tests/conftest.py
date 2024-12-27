from datetime import datetime, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from application.backend.main import app
from application.backend.models import Service, Trainer, TimeSlot

# URL для тестовой базы данных
TEST_DATABASE_URL = "postgresql://postgres:Worldof123@localhost/test_db"

# Создаем движок и сессию
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Фикстура для настройки базы данных
@pytest.fixture(scope="function")
def test_session():
    SQLModel.metadata.drop_all(bind=engine)
    SQLModel.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # Добавление тестовых данных
    service1 = Service(name="Test Service 1", duration=60, description="Description 1", price=1000, type="individual")
    service2 = Service(name="Test Service 2", duration=30, description="Description 2", price=500, type="group")
    trainer1 = Trainer(name="Test Trainer 1", specialization="Yoga")
    trainer2 = Trainer(name="Test Trainer 2", specialization="Fitness")

    session.add_all([service1, service2, trainer1, trainer2])
    session.commit()

    tomorrow = datetime.now() + timedelta(days=1)
    timeslot1 = TimeSlot(trainer_id=trainer1.id, service_id=service1.id, dates=tomorrow.date(), times=tomorrow.time(), available=True)
    timeslot2 = TimeSlot(trainer_id=trainer2.id, service_id=service2.id, dates=tomorrow.date(), times=tomorrow.time(), available=True)

    session.add_all([timeslot1, timeslot2])
    session.commit()

    yield session
    session.close()

@pytest.fixture(scope="function")
def test_client(test_session):
    def override_session():
        return test_session
    app.dependency_overrides[TestingSessionLocal] = override_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides[TestingSessionLocal] = None
