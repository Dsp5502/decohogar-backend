from peewee import *

from ..database import database

from datetime import datetime

from .client_model import Client
from .frequency_payments import FrequencyPayment


class Sale(Model):
    client_id = ForeignKeyField(Client, backref='sales')
    created_at = DateTimeField(default=datetime.now)
    total_price = FloatField()
    frequency_payment_id = ForeignKeyField(
        FrequencyPayment, backref='sales')

    class Meta:
        database = database
        table_name = 'sales'

    def __str__(self):
        return self.name
