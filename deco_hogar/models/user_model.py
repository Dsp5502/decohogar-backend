import hashlib

from peewee import *

from ..database import database

from datetime import datetime


class User(Model):
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=50)
    created_at = DateTimeField(default=datetime.now)

    class Meta:
        database = database
        table_name = 'users'

    def __str__(self):
        return self.username

    @classmethod
    def create_password(cls, password):
        h = hashlib.md5()
        h.update(password.encode('utf-8'))
        return h.hexdigest()

    @classmethod
    def authenticate(cls, username, password):
        user = cls.select().where(cls.username == username).first()
        roles = UserRoles.select().where(UserRoles.user == user.id)
        user.roles = [role.role for role in roles]
        if user and user.password == cls.create_password(password):
            return user
        return None


class Role(Model):
    name = CharField(max_length=50, unique=True)

    class Meta:
        database = database
        table_name = 'roles'

    def __str__(self):
        return self.name


class UserRoles(Model):
    user = ForeignKeyField(User, backref='roles')
    role = ForeignKeyField(Role, backref='users')

    class Meta:
        database = database
        table_name = 'user_roles'

    def __str__(self):
        return f'{self.user} - {self.role}'
