from peewee import *

from ..database import database

from .user_model import User
from .sale_model import Sale

from datetime import datetime


class Payment(Model):
    sale_id = ForeignKeyField(Sale, backref='payments')
    created_at = DateTimeField(default=datetime.now)
    amount_paid = FloatField()
    user_created_id = ForeignKeyField(
        User, backref='payments_created')

    class Meta:
        database = database
        table_name = 'payments'

    def __str__(self):
        return self.name
