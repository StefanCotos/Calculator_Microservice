from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.request import RequestRecord
from fastapi.responses import JSONResponse
from sqlalchemy import select
from fastapi.responses import StreamingResponse
import csv
import io
from app.auth.utils import get_optional_user_jwt
from app.models.user import User
from sqlalchemy import delete

from app.core.logging_config import setup_logger
logger = setup_logger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def calculator_page(request: Request):
    """
    Displays the main calculator page.
    Args:
        request (Request): The HTTP request object
            received from the client.
    Returns:
        TemplateResponse: The response containing the "index.html"
            HTML page and the context with the request.
    """

    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def calculator_eval(

    request: Request,
    expression: str = Form(...),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_optional_user_jwt)
):
    """
    Evaluates a mathematical expression received from the
        user and saves the result in the database.
    Args:
        request (Request): The current HTTP request object.
        expression (str): The mathematical expression
            entered by the user (received via form).
        db (AsyncSession): The asynchronous session for database interaction.
        user (User): The currently authenticated user.
    Returns:
        TemplateResponse: The HTML response containing the
            evaluation result.
    """

    logger.info(f"Evaluating expression: '{expression}' for user: {getattr(user, 'username', 'anonim')}")
    result = None
    try:
        result = str(eval(expression, {"__builtins__": None}, {
                     "math": __import__('math')}))
    except Exception:
        result = "Eroare de calcul"

    record = RequestRecord(expression=expression, result=result, user=user)
    db.add(record)
    await db.commit()

    logger.info(f"Expression '{expression}' evaluated with result: '{result}' for user: {getattr(user, 'username', 'anonim')}")

    return templates.TemplateResponse("index.html", {
        "request": request,
        "result": result,
    })


@router.get("/history", response_class=JSONResponse)
async def get_history(

    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_optional_user_jwt)
):
    """
    Retrieves the last 10 operations performed
        by the current user.
    Args:
        db (AsyncSession): The asynchronous
            session for database interaction.
        user (User): The currently authenticated user.
    Returns:
        list[dict]: A list of dictionaries containing
            the expression, result, and timestamp of each operation.
    """

    logger.info(f"Retrieving history for user: {getattr(user, 'username', 'anonim')}")

    query = select(RequestRecord).order_by(RequestRecord.timestamp.desc()).limit(10)

    if user:
        query = query.where(RequestRecord.user_id == user.id)
    else:
        query = query.where(RequestRecord.user_id.is_(None))

    result = await db.execute(query)
    records = result.scalars().all()

    logger.info(f"History retrieved for user: {getattr(user, 'username', 'anonim')}")

    return [
        {"expression": r.expression, "result": r.result,
            "timestamp": r.timestamp.isoformat()}
        for r in records
    ]


@router.delete("/history")
async def delete_history(

    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_optional_user_jwt)
):
    """
    Deletes the request history for the authenticated user.
    This function deletes all records from the RequestRecord
        table associated with the current user.
    If there is no authenticated user, records without
        user association will be deleted.
    Args:
        db (AsyncSession): The asynchronous database
            session, injected via Depends.
        user (User): The current user, obtained via
        Depends(get_current_user).
    Returns:
        dict: A message confirming the deletion of the history.
    """

    logger.info(f"Deleting history for user: {getattr(user, 'username', 'anonim')}")

    if user:
        stmt = delete(RequestRecord).where(RequestRecord.user_id == user.id)
    else:
        stmt = delete(RequestRecord).where(RequestRecord.user_id.is_(None))

    await db.execute(stmt)
    await db.commit()

    logger.info(f"History deleted for user: {getattr(user, 'username', 'anonim')}")

    return {"message": "Istoric șters."}


@router.get("/history/export")
async def export_history(

    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_optional_user_jwt)
):
    """
    Exports the calculation history performed by
        the current user as a CSV file.
    Args:
        db (AsyncSession): The asynchronous database
            session, injected via dependency.
        user (User): The currently authenticated user,
            injected via dependency.
    Returns:
        StreamingResponse: An HTTP response that streams
            the CSV file containing the expressions, results, and
                timestamps of the calculations performed by the current user.
    """

    logger.info(f"Exporting history for user: {getattr(user, 'username', 'anonim')}")

    stmt = select(RequestRecord).order_by(RequestRecord.timestamp.desc())

    if user:
        stmt = stmt.where(RequestRecord.user_id == user.id)
    else:
        stmt = stmt.where(RequestRecord.user_id.is_(None))

    result = await db.execute(stmt)
    records = result.scalars().all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["expression", "result", "timestamp"])

    for record in records:
        writer.writerow([record.expression,
                         record.result,
                         record.timestamp.isoformat()])

    logger.info(f"History exported for user: {getattr(user, 'username', 'anonim')}")

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=history.csv"}
    )
