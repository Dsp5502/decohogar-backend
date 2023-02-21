from peewee import MySQLDatabase, CharField
from playhouse.migrate import MySQLMigrator, migrate

from .database import database


migrator = MySQLMigrator(MySQLDatabase(
    'decohogar', user='root', password='Jazmin082355+',
    host='localhost', port=3306))
# Create a new column
email_field = CharField(max_length=50, unique=True)
