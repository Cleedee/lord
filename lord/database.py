from peewee import (SqliteDatabase, CharField, IntegerField, ForeignKeyField,
    BooleanField, Model, DateTimeField)

db = SqliteDatabase('database.db')

class Card(Model):
    code = IntegerField()
    pack_code = CharField()
    pack_name = CharField()
    type_code = CharField()
    type_name = CharField()
    sphere_code = CharField()
    position = IntegerField()
    name = CharField()
    traits = CharField(null=True)
    text = CharField(null=True)
    is_unique = BooleanField(default=False)
    threat = IntegerField(default=0)
    willpower = IntegerField(default=0)
    attack = IntegerField(default=0)
    defense = IntegerField(default=0)
    health = IntegerField(default=0)
    quantity = IntegerField(default=0)
    deck_limit = BooleanField(default=False)
    has_errata = BooleanField(default=False)
    url = CharField(default=False)
    imagesrc = CharField(default='')

    class Meta:
        database = db

class Deck(Model):
    name = CharField()
    date_creation = DateTimeField()
    date_update = DateTimeField()
    description_md = CharField(default='')
    user_id = IntegerField()
    version = CharField()
    is_published = BooleanField()
    starting_threat = IntegerField()

    class Meta:
        database = db

class Slot(Model):
    # slot_type H: Heroes, S: Slots, L: sideslots
    SLOT_HEROES = 'H'
    SLOT_SLOTS = 'S'
    SLOT_SIDESLOTS = 'L'

    slot_type = CharField(default=SLOT_SLOTS)
    deck = ForeignKeyField(Deck)
    card = ForeignKeyField(Card)
    quantity = IntegerField(default=1)

    class Meta:
        database = db    

if __name__ == '__main__':
    db.connect()
    db.create_tables([Deck,Card,Slot])
