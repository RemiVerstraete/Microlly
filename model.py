from peewee import *
from flask_peewee.db import Database
from flask_security import UserMixin
import datetime, json

database = SqliteDatabase("data.sqlite3")

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel, UserMixin):
    username = CharField(unique=True)
    first_name = CharField()
    last_name = CharField()
    email = TextField(unique=True, index=True)
    password = TextField()

class Publication(BaseModel):
    title = CharField(index=True)
    body = TextField()
    creation_date = DateTimeField(default=datetime.datetime.now)
    update_date = DateTimeField(default=datetime.datetime.now)
    author = ForeignKeyField(User, backref="publications")

def create_tables():
    with database:
        database.create_tables([User, Publication, ])

def drop_tables():
    with database:
        database.drop_tables([User, Publication, ])