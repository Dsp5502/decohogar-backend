from peewee import *

from ..database import database

from .user_model import User


from datetime import datetime


class Item(Model):
    name = CharField(max_length=50, unique=True)
    price = FloatField()
    description = CharField(max_length=100)
    stock = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    user_created_id = ForeignKeyField(
        User, backref='items_created')

    class Meta:
        database = database
        table_name = 'items'

    def __str__(self):
        return self.name
