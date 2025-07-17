from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import calculator, math_api
from app.db.session import init_db

app = FastAPI(title="Calculator Microservice")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(calculator.router)
app.include_router(math_api.router, prefix="/api")


@app.on_event("startup")
async def on_startup():
    await init_db()
