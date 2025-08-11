from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt
from app.db.session import get_db
from app.models.user import User
from app.auth.jwt_utils import create_access_token
from fastapi.responses import JSONResponse
from app.auth.utils import get_current_user_jwt

from app.core.logging_config import setup_logger
logger = setup_logger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    """
    Handles the HTTP request for the user registration form.
    Args:
        request (Request): The incoming HTTP request object.
    Returns:
        TemplateResponse: Renders and returns the 'register.html'
            template with the request context.
    """

    logger.info("Rendering registration form.")

    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Attempting to register user: {username}")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user:
        return JSONResponse({"error": "Username deja folosit."}, status_code=409)

    hashed_pw = bcrypt.hash(password)
    new_user = User(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()

    logger.info(f"User {username} registered successfully.")

    return JSONResponse({"success": True})


@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """
    Renders the login form template.
    Args:
        request (Request): The incoming HTTP request object.
    Returns:
        TemplateResponse: The rendered 'login.html'
            template with the request context.
    """

    logger.info("Rendering login form.")

    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Attempting to log in user: {username}")

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(password, user.hashed_password):
        return JSONResponse({"error": "Date invalide."}, status_code=401)

    access_token = create_access_token({"sub": str(user.id)})
    response = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    return response


@router.get("/me")
async def get_me(user: User = Depends(get_current_user_jwt)):
    return {
        "id": user.id,
        "username": user.username,
        "created_at": user.created_at
    }
