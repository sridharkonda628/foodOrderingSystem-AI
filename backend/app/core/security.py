"""
Cryptographic and Authentication Utilities.

Use Case:
- Password hashing and verification using bcrypt.
- JSON Web Token (JWT) creation, encoding, and decoding for secure user session management.
"""

from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Union
import bcrypt
from jose import JWTError, jwt
from app.core.config import settings


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain text password against a stored bcrypt hash.

    Use Case:
    - Called during user login (`AuthService.login`) to validate supplied credentials.

    Parameters:
    - plain_password: The raw password string submitted by the user.
    - hashed_password: The bcrypt hash stored in the database.

    Returns:
    - True if password matches the hash, False otherwise.
    """
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Generates a secure salt and bcrypt hash for a plain text password.

    Use Case:
    - Called during user registration (`AuthService.register`) or database seeding
      to ensure plaintext passwords are never stored in the database.

    Parameters:
    - password: The raw password string to hash.

    Returns:
    - The salted bcrypt hash string.
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def create_access_token(
    subject: Union[str, Any],
    role: str,
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Creates a cryptographically signed JWT access token.

    Use Case:
    - Generated upon successful registration or login to authenticate subsequent API requests.

    Parameters:
    - subject: The user ID (sub claim) stored in the token.
    - role: The user role (e.g. 'admin' or 'customer') for authorization checks.
    - expires_delta: Optional custom token expiration time window.

    Returns:
    - Encoded JWT token string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "role": role,
        "iat": datetime.now(timezone.utc)
    }
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodes and validates a signed JWT access token.

    Use Case:
    - Invoked by the `get_current_user` FastAPI dependency to authenticate incoming requests.

    Parameters:
    - token: The raw JWT string from the HTTP Authorization header.

    Returns:
    - Dictionary payload containing 'sub', 'role', 'exp' if valid; None if expired or invalid.
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        return None
