from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from fastapi import status


from .database import database as connection

from .models import User, Role, UserRoles
from .models import Client

from .routers import users, clients_router

from .common import create_acces_token

from .migrations import migrator

from peewee import CharField, DateTimeField, ForeignKeyField, Model

from playhouse.migrate import migrate


app = FastAPI(
    title="Deco-Hogar",
    description="API para el proyecto de Deco-Hogar",
    version="0.1.0",
)

api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(users.router)
api_v1.include_router(clients_router)


@api_v1.post('/auth')
async def auth(data: OAuth2PasswordRequestForm = Depends()):
    user = User.authenticate(data.username, data.password)
    if user:
        return {
            'access_token': create_acces_token(user),
            'token_type': 'Bearer'
        }
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Usuario o contraseña incorrectos',
                            headers={"WWW-Authenticate": "Bearer"}
                            )

app.include_router(api_v1)


@app.on_event("startup")
async def startup_event():
    if connection.is_closed():
        connection.connect()
        print("Starting up...")

    connection.create_tables([User, Role, UserRoles, Client])

    # migrate(migrator.add_column('clients', 'user_created_id',
    #         ForeignKeyField(User, backref='clients_created', field=User.id, default=1)))


@app.on_event("shutdown")
async def shutdown_event():
    if not connection.is_closed():
        connection.close()
        print("Shutting down...")


@app.get("/")
def read_root():
    return {"message": "Esta es un API para el proyecto de Deco-Hogar el cual va a contener CRUD de productos, usuarios, etc."}
