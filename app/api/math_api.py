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
from app.auth.utils import get_current_user
from app.models.user import User

router = APIRouter()
service = MathService()


@router.post("/pow", response_model=MathResponse)
async def power(payload: PowRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = service.power(payload.x, payload.y)
    expr = f"pow({payload.x}, {payload.y})"

    record = RequestRecord(expression=expr, result=str(result), user=user)
    db.add(record)
    await db.commit()

    return {
        "input": {"x": payload.x, "y": payload.y},
        "result": result
    }


@router.post("/fibonacci", response_model=MathResponse)
async def fibonacci(payload: FibonacciRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = service.fibonacci(payload.n)
    expr = f"fibonacci({payload.n})"

    record = RequestRecord(expression=expr, result=str(result), user=user)
    db.add(record)
    await db.commit()

    return {
        "input": {"n": payload.n},
        "result": result
    }


@router.post("/factorial", response_model=MathResponse)
async def factorial(payload: FactorialRequest, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    result = service.factorial(payload.n)
    expr = f"factorial({payload.n})"

    record = RequestRecord(expression=expr, result=str(result), user=user)
    db.add(record)
    await db.commit()

    return {
        "input": {"n": payload.n},
        "result": result
    }
