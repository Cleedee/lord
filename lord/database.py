from peewee import (SqliteDatabase, CharField, IntegerField, ForeignKeyField,
    BooleanField, Model, DateTimeField, TextField)

db = SqliteDatabase('database.db')

CENARIOS_CONJUNTOS = {
    'Passage Through Mirkwood' : [
        'Dol Guldur Orcs',
        'Passage Through Mirkwood',
        'Spiders of Mirkwood'
    ],
}

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
    text = TextField(null=True)
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
    cost = CharField(default=None,null=True)

    class Meta:
        database = db

    @property
    def is_ally(self) -> bool:
        return self.type_code == 'ally'

    @property
    def is_attachment(self) -> bool:
        return self.type_code == 'attachment'

    @property
    def is_event(self) -> bool:
        return self.type_code == 'event'

    @property
    def is_contract(self) -> bool:
        return self.type_code == 'contract'

    @property
    def is_treasure(self) -> bool:
        return self.type_code == 'treasure'

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

class Game(Model):

    nplayers = IntegerField(default=1)
    rounds = IntegerField(default=1)
    active = BooleanField(default=False)

    class Meta:
        database = db

class Scenario(Model):

    type_code = CharField()
    type_name = CharField()
    number = IntegerField()
    name = CharField()
    is_unique = BooleanField(default=False)
    text = TextField(null=True)
    shadow = TextField(null=True)
    pack_code = CharField() # Abbr
    pack_name = CharField() # Box
    threat = CharField(null=True)
    traits = CharField(null=True)
    keywords = CharField(null=True)
    willpower = IntegerField(default=0) # WP
    attack = TextField(null=True) # ATK
    defense = TextField(null=True) # DEF
    health = TextField(null=True) # HP  
    cycle = CharField(null=True)
    encounter_set = CharField(null=True)
    quest_points = CharField(null=True) # Quest
    victory = CharField(null=True)
    sequence = CharField(null=True) # Q#
    notes = TextField(null=True)
    count = CharField(null=True)
    engage = CharField(null=True)

    class Meta:
        database = db    

if __name__ == '__main__':
    db.connect()
    db.create_tables([Deck,Card,Slot, Game, Scenario])
