import datetime
from peewee import *

db = SqliteDatabase('filton.db')


# simple utility function to create tables
def create_tables():
    with db:
        db.create_tables([Message])


class Message(Model):
    author_name = CharField()
    email = CharField()
    message = TextField()
    created = DateTimeField(default=datetime.datetime.now())
    deleted = BooleanField(default=False)

    class Meta:
        database = db
