from fastapi import HTTPException

from ..models import User, Role, UserRoles

from ..schemas import UserRequestModel, RoleRequestModel


class UserService:

    @staticmethod
    def create_user_service(user: UserRequestModel):
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

    @staticmethod
    def user_roles_service(role: RoleRequestModel, userRole: User):
        user = User.get(User.id == userRole.id)
        role = Role.get(Role.id == role.rol_id)
        if UserRoles.select().where(UserRoles.user == user.id, UserRoles.role == role.id).exists():
            raise HTTPException(409, 'El usuario ya tiene ese rol')

        UserRoles.create(user=user, role=role)
        user_roles = UserRoles.select().where(UserRoles.user == user.id)
        user_roles = [user_role.role.name for user_role in user_roles]
        return user, user_roles
