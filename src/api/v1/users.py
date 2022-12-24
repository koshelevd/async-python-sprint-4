from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from api.depends import get_current_user, get_user_service
from db.tables import User
from dto.links_schemas import UserStatusEntity
from dto.users_schemas import TokenSchema, UserDTO, UserResponseEntity
from services import UserService

router = APIRouter(prefix="/user")


@router.post(
    "/signin",
    response_model=TokenSchema,
    summary="Create access and refresh tokens for user",
)
async def login(
    data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(get_user_service),
):
    """Create access and refresh tokens for user."""
    return await user_service.signin(data.username, data.password)


@router.post(
    "/signup",
    response_model=UserResponseEntity,
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    data: UserDTO,
    user_service: UserService = Depends(get_user_service),
):
    """Register new user."""
    user = await user_service.signup(data.email, data.password)
    return user


@router.get(
    "/status", response_model=list[UserStatusEntity], summary="Get user status"
)
async def get_user_status(
    user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
):
    """Get user status."""
    return await user_service.get_user_status(user)
