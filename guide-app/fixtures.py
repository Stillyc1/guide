import sys

from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.activity import Activity
from core.models.building import Building
from core.models.organization import Organization
from core.models.phone_number import PhoneNumber
from core.models.organization_activities_table import organization_activities_table


async def create_test_data(db: AsyncSession):
    # Создание зданий
    building1 = Building(
        address="г. Москва, ул. Ленина, д. 1, офис 3",
        latitude=55.7558,
        longitude=37.6173
    )
    building2 = Building(
        address="г. Москва, ул. Тверская, д. 10, офис 12",
        latitude=55.7550,
        longitude=37.6174,
    )

    db.add(building1)
    db.add(building2)
    await db.flush()

    # Создание видов деятельности с вложенностью
    activity_cars = Activity(name="Автомобили", level=1)
    activity_cars_saloon = Activity(name="Легковые", parent=activity_cars, level=2)
    activity_cars_parts = Activity(name="Запчасти", parent=activity_cars_saloon, level=3)

    activity_food = Activity(name="Еда", level=1)
    activity_meat = Activity(name="Мясная продукция", parent=activity_food, level=2)
    activity_dairy = Activity(name="Молочная продукция", parent=activity_food, level=2)

    db.add(activity_cars)
    db.add(activity_cars_saloon)
    db.add(activity_cars_parts)
    db.add(activity_food)
    db.add(activity_meat)
    db.add(activity_dairy)
    await db.flush()

    # Создание организаций
    organization1 = Organization(name="ООО 'Рога и Копыта'", building=building1)
    organization2 = Organization(name="ФГУП 'Мясокомбинат'", building=building1)
    organization3 = Organization(name="Частное Унитарное Предприятие 'Молоко'", building=building2)

    db.add(organization1)
    db.add(organization2)
    db.add(organization3)
    await db.flush()

    # Создание номеров телефонов
    phone1 = PhoneNumber(number="2222222", organization=organization1)
    phone2 = PhoneNumber(number="89236661313", organization=organization2)
    phone3 = PhoneNumber(number="1234567", organization=organization3)

    db.add(phone1)
    db.add(phone2)
    db.add(phone3)
    await db.flush()

    # Связи многие-ко-многим через ассоциативную таблицу
    await db.execute(
        insert(organization_activities_table),
        [
            {"organization_id": organization1.id, "activity_id": activity_cars.id},
            {"organization_id": organization2.id, "activity_id": activity_meat.id},
            {"organization_id": organization3.id, "activity_id": activity_dairy.id},
            {"organization_id": organization1.id, "activity_id": activity_cars_saloon.id},
            {"organization_id": organization1.id, "activity_id": activity_cars_parts.id},
            {"organization_id": organization2.id, "activity_id": activity_cars.id},
        ],
    )

    # Сохранение всех изменений
    sys.stdout.write("Тестовые данные заполнены!\n")
    await db.commit()


async def reset_database(db: AsyncSession):
    # Очищаем таблицы в правильном порядке (с учётом внешних ключей)
    await db.execute(text("TRUNCATE TABLE phone_numbers CASCADE"))
    await db.execute(text("TRUNCATE TABLE organization_activities CASCADE"))
    await db.execute(text("TRUNCATE TABLE organizations CASCADE"))
    await db.execute(text("TRUNCATE TABLE activities CASCADE"))
    await db.execute(text("TRUNCATE TABLE buildings CASCADE"))

    sys.stdout.write("Тестовые данные удалены!\n")
    await db.commit()