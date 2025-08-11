from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db
from app.models.user import User
from fastapi import HTTPException, status, Header
from app.auth.jwt_utils import decode_access_token


from app.core.logging_config import setup_logger
logger = setup_logger(__name__)


async def get_current_user_jwt(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Retrieve the current authenticated user based on a JWT access
        token from the Authorization header.
    Args:
        authorization (str): The Authorization header containing the
            JWT token in the format "Bearer <token>".
        db (AsyncSession): The asynchronous database session dependency.
    Returns:
        User: The authenticated user instance.
    Raises:
        HTTPException: If the Authorization header is missing, the token
            is invalid, or the user does not exist.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not exist")
    return user


async def get_optional_user_jwt(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db)
) -> User | None:
    """
    Retrieve an optional authenticated user from a JWT in the Authorization header.
    This function attempts to extract and decode a JWT from the "Authorization" header
    of the incoming request. If the header is missing, malformed, or the token is invalid,
    it returns None. Otherwise, it fetches the corresponding user from the database.
    Args:
        authorization (str, optional): The Authorization header value,
            expected in the format "Bearer <token>".
        db (AsyncSession): The asynchronous database session dependency.
    Returns:
        User | None: The authenticated User object if the token is valid
            and the user exists, otherwise None.
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        return None
    user_id = int(payload["sub"])
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    return user
