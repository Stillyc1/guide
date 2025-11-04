import asyncio
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings

from api import router as api_router
from core.models import db_helper
from fixtures import create_test_data, reset_database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


main_app = FastAPI(
    lifespan=lifespan,
)
main_app.include_router(
    api_router,
    prefix=settings.api.prefix,
)


async def main():
    async for session in db_helper.session_getter():
        await reset_database(session)
        await create_test_data(session)


if __name__ == "__main__":
    # asyncio.run(main())
    uvicorn.run(
        app="main:main_app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
    )

# uvicorn main:main_app --host 127.0.0.1 --reload --- "Локальный старт"
# alembic init -t async alembic --- "инициализация alembic async"
# alembic revision --autogenerate -m "create Users model" --- "Создание миграций"
# alembic upgrade head --- "Применение миграций"
# alembic downgrade base \ -1 --- "откатить миграции до базовой \ до предыдущей"
