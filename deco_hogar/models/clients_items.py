from peewee import *

from ..database import database

from .client_model import Client
from .items_model import Item
from .sale_model import Sale

from datetime import datetime


class ClientItem(Model):
    client_id = ForeignKeyField(Client, backref='items')
    item_id = ForeignKeyField(Item, backref='clients')
    quantity = IntegerField()
    created_at = DateTimeField(default=datetime.now)
    user_created_id = IntegerField()
    sale_id = ForeignKeyField(Sale, backref='items')

    class Meta:
        database = database
        table_name = 'clients_items'

    def __str__(self):
        return self.name
