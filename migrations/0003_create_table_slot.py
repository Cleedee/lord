"""
create table slot
date created: 2021-10-14 03:38:16.204093
"""


def upgrade(migrator):
    with migrator.create_table('slot') as table:
        table.primary_key('id')
        table.char('slot_type', max_length=255)
        table.foreign_key('AUTO', 'deck_id', on_delete=None, on_update=None, references='deck.id')
        table.foreign_key('AUTO', 'card_id', on_delete=None, on_update=None, references='card.id')
        table.int('quantity')


def downgrade(migrator):
    migrator.drop_table('slot')
