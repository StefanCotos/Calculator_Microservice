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
async def power(payload: PowRequest,
                db: AsyncSession = Depends(get_db),
                user: User = Depends(get_current_user)):
    """
        Calculates the power of a number and saves the
            expression and result in the database.
        Args:
            payload (PowRequest): Object containing the
                values x (base) and y (exponent).
            db (AsyncSession, optional): The asynchronous
                session for interacting with the database.
            user (User, optional): The currently authenticated user.
        Returns:
            dict: A dictionary containing the input values
                and the calculation result.
    """
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
async def fibonacci(payload: FibonacciRequest,

                    db: AsyncSession = Depends(get_db),
                    user: User = Depends(get_current_user)):
    """
        Calculates the n-th term in the Fibonacci sequence
            based on the value received in the payload.
        Args:
            payload (FibonacciRequest): Object containing the
                value 'n' for which the Fibonacci term is calculated.
            db (AsyncSession, optional): The asynchronous
                database session, automatically injected.
            user (User, optional): The currently authenticated
                user, automatically injected.
        Returns:
            dict: A dictionary containing the input
                value and the calculation result.
        Side effects:
            Saves the expression and calculation result in the
                database, associated with the current user.
    """
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
async def factorial(payload: FactorialRequest,

                    db: AsyncSession = Depends(get_db),
                    user: User = Depends(get_current_user)):
    """
        Calculates the factorial of a given number and records
            the request in the database.
        Args:
            payload (FactorialRequest): The request payload containing
                the integer 'n' for which the factorial is to be calculated.
            db (AsyncSession, optional): The asynchronous database session dependency.
            user (User, optional): The currently authenticated user dependency.
        Returns:
            dict: A dictionary containing the input value
                and the calculated factorial result.
        Raises:
            Any exceptions raised by the service.factorial
                function or database operations.
        Side Effects:
            Persists a new RequestRecord in the database with
                the expression, result, and user information.
    """
    result = service.factorial(payload.n)
    expr = f"factorial({payload.n})"

    record = RequestRecord(expression=expr, result=str(result), user=user)
    db.add(record)
    await db.commit()

    return {
        "input": {"n": payload.n},
        "result": result
    }
