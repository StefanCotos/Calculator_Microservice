from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.request import RequestRecord
from app.services.math_service import MathService
from app.schemas.math_schema import (
    PowRequest,
    FactorialRequest,
    FibonacciRequest,
    MathResponse
)

router = APIRouter()
service = MathService()


@router.post("/pow", response_model=MathResponse)
async def power(payload: PowRequest, db: AsyncSession = Depends(get_db)):
    result = service.power(payload.x, payload.y)
    expr = f"pow({payload.x}, {payload.y})"

    await db.merge(RequestRecord(expression=expr, result=str(result)))
    await db.commit()

    return {
        "input": {"x": payload.x, "y": payload.y},
        "result": result
    }


@router.post("/fibonacci", response_model=MathResponse)
async def fibonacci(payload: FibonacciRequest, db: AsyncSession = Depends(get_db)):
    result = service.fibonacci(payload.n)
    expr = f"fibonacci({payload.n})"

    await db.merge(RequestRecord(expression=expr, result=str(result)))
    await db.commit()

    return {
        "input": {"n": payload.n},
        "result": result
    }


@router.post("/factorial", response_model=MathResponse)
async def factorial(payload: FactorialRequest, db: AsyncSession = Depends(get_db)):
    result = service.factorial(payload.n)
    expr = f"factorial({payload.n})"

    await db.merge(RequestRecord(expression=expr, result=str(result)))
    await db.commit()

    return {
        "input": {"n": payload.n},
        "result": result
    }
