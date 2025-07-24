from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from passlib.hash import bcrypt
from app.db.session import get_db
from app.models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Handles user registration by processing form data,
        checking for existing usernames,
    hashing the password, creating a new user in the
        database, and redirecting to the login page.
    Args:
        request (Request): The incoming HTTP request object.
        username (str): The username submitted via the registration form.
        password (str): The password submitted via the registration form.
        db (AsyncSession): The asynchronous database session dependency.
    Returns:
        TemplateResponse: If the username already exists,
            renders the registration page with an error message.
        RedirectResponse: If registration is successful,
            redirects the user to the login page.
    """
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user:
        return templates.TemplateResponse("register.html",
                                          {"request": request,
                                           "error": "Username deja folosit."})

    hashed_pw = bcrypt.hash(password)
    new_user = User(username=username, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()

    response = RedirectResponse("/login", status_code=302)
    return response


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

    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Handles user login by validating credentials and setting a session cookie.
    Args:
        request (Request): The incoming HTTP request object.
        username (str): The username submitted via form data.
        password (str): The password submitted via form data.
        db (AsyncSession): The asynchronous database session dependency.
    Returns:
        TemplateResponse: If authentication fails,
            renders the login page with an error message.
        RedirectResponse: If authentication succeeds,
            redirects to the home page and sets a user_id cookie.
    """
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if not user or not bcrypt.verify(password, user.hashed_password):
        return templates.TemplateResponse("login.html",
                                          {"request": request,
                                           "error": "Date invalide."})

    response = RedirectResponse("/", status_code=302)
    response.set_cookie("user_id", str(user.id))
    return response


@router.get("/logout")
async def logout():
    """
    Logs out the current user by deleting the
        'user_id' cookie and redirecting to the home page.
    Returns:
        RedirectResponse: A response object that redirects the user to the root
            URL ("/") with a 302 status code and removes the 'user_id' cookie.
    """

    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("user_id")
    return response
