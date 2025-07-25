from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import calculator, math_api
from app.auth import routes
from app.db.session import init_db

from app.core.logging_config import setup_logger
logger = setup_logger(__name__)


async def lifespan(app: FastAPI):
    """Lifespan event handler to initialize the database."""
    logger.info("Starting application and initializing database...")
    await init_db()
    logger.info("Database initialized successfully.")
    yield

app = FastAPI(title="Calculator Microservice", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(calculator.router)
app.include_router(math_api.router, prefix="/api")
app.include_router(routes.router)
