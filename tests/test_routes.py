from sqlmodel import select
from application.backend.models import Service, Trainer, TimeSlot

# Тесты
def test_get_trainers(test_client):
    response = test_client.get("/api/trainers")
    assert response.status_code == 200
    trainers = response.json()
    assert isinstance(trainers, list)
    assert len(trainers) >= 2  # Проверяем, что есть хотя бы два тренера
    assert trainers[0]["name"] == "Test Trainer 1"  # Проверяем имя первого тренера


def test_get_services(test_client):
    response = test_client.get("/api/services")
    assert response.status_code == 200
    services = response.json()
    assert isinstance(services, list)
    assert len(services) >= 2
    assert services[0]["name"] == "Test Service 1"

def test_get_timeslots(test_client, test_session):
    # Создаем временной слот для теста
    trainer = test_session.execute(select(Trainer)).scalars().first()
    service = test_session.execute(select(Service)).scalars().first()
    
    # Проверяем, что тренер и услуга существуют
    assert trainer is not None, "Тренер не найден"
    assert service is not None, "Услуга не найдена"

    timeslot = test_session.query(TimeSlot).filter(
        TimeSlot.trainer_id == trainer.id, TimeSlot.service_id == service.id
    ).first()

    assert timeslot is not None, "Таймслот не найден"

    response = test_client.get("/api/timeslots", params={
        "service_id": service.id,
        "trainerId": trainer.id,
        "date": timeslot.dates
    })

    assert response.status_code == 200
    timeslots = response.json()
    assert isinstance(timeslots, list)
    assert len(timeslots) > 0
    assert timeslots[0]["trainer_id"] == trainer.id  # Проверяем, что данные о тренере совпадают
    assert timeslots[0]["service_id"] == service.id  # Проверяем, что данные о сервисе совпадают