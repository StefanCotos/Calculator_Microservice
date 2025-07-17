from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.request import RequestRecord
import math
from fastapi.responses import JSONResponse
from sqlalchemy import select
from fastapi.responses import StreamingResponse
import csv
import io

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def calculator_page(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "result": None})


@router.post("/", response_class=HTMLResponse)
async def calculator_eval(
    request: Request,
    expression: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    result = None
    try:
        result = str(eval(expression, {"__builtins__": None},
                          {"math": math}))
    except Exception:
        result = "Eroare de calcul"

    await db.merge(RequestRecord(expression=expression, result=result))
    await db.commit()

    return templates.TemplateResponse("index.html",
                                      {"request": request,
                                       "result": result})


@router.get("/history", response_class=JSONResponse)
async def get_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RequestRecord).order_by(RequestRecord.timestamp.desc()).limit(15)
    )
    records = result.scalars().all()

    return [
        {"expression": r.expression, "result": r.result,
            "timestamp": r.timestamp.isoformat()}
        for r in records
    ]


@router.delete("/history")
async def delete_history(db: AsyncSession = Depends(get_db)):
    await db.execute(
        RequestRecord.__table__.delete()
    )
    await db.commit()
    return {"message": "Istoric șters cu succes."}


@router.get("/history/export")
async def export_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RequestRecord).order_by(RequestRecord.timestamp.desc())
    )
    records = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["expression", "result", "timestamp"])

    for record in records:
        writer.writerow([record.expression, record.result,
                        record.timestamp.isoformat()])

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=history.csv"}
    )
