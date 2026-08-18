from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserOut
from app.schemas.common import APIResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=APIResponse[TokenResponse], status_code=status.HTTP_201_CREATED)
async def register(
    data: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    user, token = await AuthService.register(db, data)
    user_out = UserOut.model_validate(user)
    return APIResponse(
        success=True,
        data=TokenResponse(access_token=token, token_type="bearer", user=user_out),
        message="Registration successful"
    )


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(
    data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    user, token = await AuthService.login(db, data)
    user_out = UserOut.model_validate(user)
    return APIResponse(
        success=True,
        data=TokenResponse(access_token=token, token_type="bearer", user=user_out),
        message="Login successful"
    )


@router.get("/me", response_model=APIResponse[UserOut])
async def get_me(
    current_user: User = Depends(get_current_user)
):
    user_out = UserOut.model_validate(current_user)
    return APIResponse(
        success=True,
        data=user_out,
        message="User profile retrieved"
    )
