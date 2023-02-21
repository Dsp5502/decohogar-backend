from pydantic import BaseModel, validator

from .response_model import ResponseModel


class ClientRequestModel(BaseModel):
    name: str
    direction: str
    phone: str
    email: str

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
    def phone_validator(cls, phone):
        if len(phone) < 3 or len(phone) > 50:
            raise ValueError(
                'El teléfono del cliente debe tener entre 3 y 50 caracteres')
        return phone

    @validator('email')
    def email_validator(cls, email):
        if len(email) < 3 or len(email) > 50:
            raise ValueError(
                'El email del cliente debe tener entre 3 y 50 caracteres')
        return email


class ClientResponseModel(ResponseModel):
    id: int
    name: str
    direction: str
    phone: str
    email: str
