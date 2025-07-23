from pydantic import BaseModel, Field


class PowRequest(BaseModel):
    x: float
    y: float


class FibonacciRequest(BaseModel):
    n: int = Field(..., ge=0, description="n must be ≥ 0")


class FactorialRequest(BaseModel):
    n: int = Field(..., ge=0, description="n must be ≥ 0")


class MathResponse(BaseModel):
    input: dict
    result: float | int | str
