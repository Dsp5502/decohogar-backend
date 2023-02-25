
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from ..schemas import UserRequestModel, UserResponseModel, RoleRequestModel, UserRolesResponseModel

from ..models import User, Role, UserRoles

from ..common import has_roles

from ..services import UserService

router = APIRouter(prefix='/users')


@router.post('/create_user', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    user_created = UserService. create_user_service(user)
    return user_created


@router.post('/add_role', response_model=UserRolesResponseModel)
async def add_role(role: RoleRequestModel, userRole: User = Depends(has_roles(['admin']))):

    user, user_roles = UserService.user_roles_service(role, userRole)
    return {
        'user': user.username,
        'role': user_roles
    }
