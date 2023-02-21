from peewee import *

from ..database import database


from datetime import datetime


class FrequencyPayment(Model):
    name = CharField(max_length=50, unique=True)
    description = CharField(max_length=100)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = database
        table_name = 'frequency_payments'

    def __str__(self):
        return self.name