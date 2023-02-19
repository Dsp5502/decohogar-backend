
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from ..schemas import UserRequestModel, UserResponseModel, RoleRequestModel, UserRolesResponseModel

from ..models import User, Role, UserRoles

from ..common import get_current_user, has_roles

router = APIRouter(prefix='/users')


@router.post('/create_user', response_model=UserResponseModel)
async def create_user(user: UserRequestModel):
    if User.select().where(User.username == user.username).exists():
        raise HTTPException(409, 'El usuario ya existe')

    if not Role.select().where(Role.name == user.role).exists():
        raise HTTPException(404, 'El rol no existe')

    hash_password = User.create_password(user.password)
    user_created = User.create(
        username=user.username,
        password=hash_password
    )
    role = Role.select().where(Role.name == user.role).first()
    UserRoles.create(
        user=user_created.id,
        role=role
    )
    user_created.role = role
    return user_created


@router.post('/add_role', response_model=UserRolesResponseModel)
async def add_role(role: RoleRequestModel, userRole: User = Depends(has_roles(['admin']))):

    user = User.get(User.id == userRole.id)
    role = Role.get(Role.id == role.rol_id)
    if UserRoles.select().where(UserRoles.user == user.id, UserRoles.role == role.id).exists():
        raise HTTPException(409, 'El usuario ya tiene ese rol')

    UserRoles.create(user=user, role=role)
    user_roles = UserRoles.select().where(UserRoles.user == user.id)
    user_roles = [user_role.role.name for user_role in user_roles]
    return {
        'user': user.username,
        'role': user_roles
    }


# Ruta protegida que requiere un usuario con el rol "admin"
@router.get('/admin')
async def admin_route(userRole: User = Depends(has_roles(['admin']))):
    print(f'userRole: {userRole.__dict__}')
    return {'message': 'Bienvenido Administrador'}
