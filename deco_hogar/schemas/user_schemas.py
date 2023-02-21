from pydantic import BaseModel, validator

from typing import List

from .response_model import ResponseModel


class RoleRequestModel(BaseModel):
    rol_id: int

    @validator('rol_id')
    def rol_id_validator(cls, rol_id):
        if rol_id != 1 and rol_id != 2:
            raise ValueError('Rol no válido')
        return rol_id


class RoleResponseModel(ResponseModel):
    name: str


class UserRequestModel(BaseModel):
    username: str
    password: str
    role: str

    @validator('username')
    def username_validator(cls, username):
        if len(username) < 3 or len(username) > 50:
            raise ValueError(
                'El nombre de usuario debe tener entre 3 y 50 caracteres')
        return username


class UserResponseModel(ResponseModel):
    id: int
    username: str
    role: RoleResponseModel


class UserRolesResponseModel(ResponseModel):
    user: str
    role: List[str]


class UserClientResponseModel(ResponseModel):
    id: int
    username: str
