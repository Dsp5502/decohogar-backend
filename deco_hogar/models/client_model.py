from peewee import *

from ..database import database

from .user_model import User

from datetime import datetime


class Client(Model):
    name = CharField(max_length=50, unique=True)
    email = CharField(max_length=50, unique=True)
    direction = CharField(max_length=100)
    phone = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)
    user_created_id = ForeignKeyField(
        User, backref='clients_created', field='id', null=False)

    class Meta:
        database = database
        table_name = 'clients'

    def __str__(self):
        return self.name
