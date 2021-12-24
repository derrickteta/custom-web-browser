from peewee import *
import datetime

db = SqliteDatabase("database.db")


class BaseModel(Model):
    class Meta:
        database = db


class Folder(BaseModel):
    name = CharField()
    parent = ForeignKeyField("self", null=True, backref="children")


class Bookmark(Folder):
    pass


class History(BaseModel):
    date = DateTimeField(default=datetime.date.today)


class Link(BaseModel):
    text = CharField()
    link = CharField()
    history = ForeignKeyField(History, null=True, backref="links")
    bookmark = ForeignKeyField(History, null=True, backref="bookmarks")
    time = DateTimeField(default=datetime.datetime.now)
