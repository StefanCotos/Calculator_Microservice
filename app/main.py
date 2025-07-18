from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import calculator, math_api
from app.auth import routes
from app.db.session import init_db


async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="Calculator Microservice", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(calculator.router)
app.include_router(math_api.router, prefix="/api")
app.include_router(routes.router)
