from peewee import *

#db = SqliteDatabase('people.db')
db = MySQLDatabase('myapp', user='root', password='toor', host='localhost', port=3306)

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db

class Pet(Model):
    owner = ForeignKeyField(Person, backref='pets')
    name = CharField()
    animal_type = CharField()

    class Meta:
        database = db

db.connect()
db.create_tables([Person, Pet])


