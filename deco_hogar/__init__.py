from fastapi import APIRouter
from fastapi import FastAPI
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware


from .database import database as connection

from .models import User, Role, UserRoles
from .models import Client
from .models import Item, ClientItem, Sale
from .models import FrequencyPayment, Payment

from .routers import users, clients_router, items_router, sales_router

from .common import create_acces_token

from .migrations import migrator

from peewee import CharField, DateTimeField, ForeignKeyField, Model

from playhouse.migrate import migrate


app = FastAPI(
    title="Deco-Hogar",
    description="El proyecto DecoHogar cuenta con un API que permite crear y gestionar usuarios con roles de administrador o usuario, los cuales pueden autenticarse y crear clientes e items. Además, a partir de la creación de clientes e items, los usuarios pueden generar ventas. En el API, es posible realizar el CRUD (crear, leer, actualizar y eliminar) de estas funcionalidades. Si estás interesado en conocer más sobre el código del proyecto, puedes acceder al repositorio alojado en https://github.com/Dsp5502/decohogar-backend.",
    version="0.1.0",
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_v1 = APIRouter(prefix='/api/v1')

api_v1.include_router(users.router)
api_v1.include_router(clients_router)
api_v1.include_router(items_router)
api_v1.include_router(sales_router)


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

    connection.create_tables(
        [User, Role, UserRoles, Client, Item, ClientItem, Sale, FrequencyPayment, Payment])

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
