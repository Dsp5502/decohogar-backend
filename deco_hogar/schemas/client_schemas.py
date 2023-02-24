import re

from pydantic import BaseModel, validator, EmailStr, ValidationError

from .response_model import ResponseModel


class MyValidationError(ValueError):
    def __init__(self, msg, loc):
        self.msg = msg
        self.loc = loc


class ClientRequestModel(BaseModel):
    name: str
    direction: str
    phone: str
    email: EmailStr

    @validator('name')
    def name_validator(cls, name):
        if len(name) < 3 or len(name) > 50:
            raise ValueError(
                'El nombre del cliente debe tener entre 3 y 50 caracteres')
        return name

    @validator('direction')
    def address_validator(cls, address):
        if len(address) < 3 or len(address) > 100:
            raise ValueError(
                'La dirección del cliente debe tener entre 3 y 100 caracteres')
        return address

    @validator('phone')
    def validate_phone(cls, phone):
        pattern = r'^\+?\d{7,15}$'
        if not re.match(pattern, phone):
            raise MyValidationError(
                msg=f'El número de teléfono no es válido debe tener  entre 7 a 15 digitos ', loc='phone')
        return phone

    @validator('email')
    def email_validator(cls, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("correo electrónico no válido")
        return email


class ClientResponseModel(ResponseModel):
    id: int
    name: str
    direction: str
    phone: str
    email: str
