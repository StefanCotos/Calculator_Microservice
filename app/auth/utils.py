from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.user import User

from app.logging_config import setup_logger
logger = setup_logger(__name__)


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """
    Asynchronously retrieves the current user from the request cookies.
    This function attempts to extract the 'user_id'
        from the request's cookies.
    If a 'user_id' is found, it queries the database
        for a user with the corresponding ID.
    If the user exists, it returns the User
        object; otherwise, it returns None.
    If no 'user_id' is present in the cookies or
        an exception occurs during the process,
    the function returns None.
    Args:
        request (Request): The incoming HTTP request containing cookies.
        db (AsyncSession, optional): The asynchronous database session dependency.
    Returns:
        User | None: The User object if found, otherwise None.
    """
    user_id = request.cookies.get("user_id")

    logger.debug(f"Attempting to retrieve user with ID: {user_id}")

    if not user_id:
        return None

    try:
        result = await db.execute(select(User).where(User.id == int(user_id)))
        user = result.scalar_one_or_none()
        logger.debug(f"User retrieved: {user}")
        return user
    except Exception:
        logger.error(f"Error retrieving user with ID: {user_id}")
        return None
