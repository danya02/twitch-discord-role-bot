from peewee import *
import datetime

db = SqliteDatabase('./test.db')

class MyModel(Model):
    class Meta:
        database = db
        legacy_table_names = False

tables = []
def create_table(cls):
    tables.append(cls)
    return cls

@create_table
class Notification(MyModel):
    data = TextField()
    added_at = DateTimeField(default=datetime.datetime.now, index=True)

@create_table
class SubscriptionSecret(MyModel):
    twitch_id = CharField(unique=True)
    value = BlobField()

def init_db():
    db.connect()
    db.create_tables(tables)

def teardown_db():
    db.close()

