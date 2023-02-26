import os
import jwt

from typing import List

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPBearer

from .models import User

from datetime import datetime, timedelta


from dotenv import load_dotenv

load_dotenv()


# Constants

SECRET_KEY = os.getenv("SECRET_KEY")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth')
security = HTTPBearer()


def create_acces_token(user, days=7):
    data = {
        'user_id': user.id,
        'user_name': user.username,
        'roles': [role.name for role in user.roles],
        'exp': datetime.utcnow() + timedelta(days=days)
    }
    print(data)
    return jwt.encode(data, SECRET_KEY, algorithm='HS256')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:

    data = decode_access_token(token)
    if data is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token invalido',
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    user = User.select().where(User.id == data['user_id']).first()
    if user is None:
        raise HTTPException(404, detail='Usuario no encontrado')
    user.roles = [role for role in data['roles']]
    return user


def decode_access_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as err:
        return None


# Función de verificación de token y roles
async def get_current_user_roles(token: str = Depends(oauth2_scheme)) -> User:
    try:
        data = decode_access_token(token)
        if data is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Token invalido',
                                headers={"WWW-Authenticate": "Bearer"}
                                )
        roles = data['roles']
        if not roles:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Token invalido',
                                headers={"WWW-Authenticate": "Bearer"}
                                )
        return data
    except jwt.exceptions.DecodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Token invalido',
                            headers={"WWW-Authenticate": "Bearer"}
                            )


# Decorador de roles
def has_roles(roles: List[str]):
    async def check_roles(token: str = Depends(oauth2_scheme)):
        data = await get_current_user_roles(token)
        for role in roles:
            if role in data['roles']:
                user = User.select().where(User.id == data['user_id']).first()
                if user is None:
                    raise HTTPException(404, detail='Usuario no encontrado')
                user.roles = [role for role in data['roles']]
                return user
        raise HTTPException(
            status_code=403, detail='No tienes los permisos necesarios para acceder a esta ruta')
    return check_roles
