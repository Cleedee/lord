"""
create table deck
date created: 2021-10-14 03:38:16.203810
"""


def upgrade(migrator):
    with migrator.create_table('deck') as table:
        table.primary_key('id')
        table.char('name', max_length=255)
        table.datetime('date_creation')
        table.datetime('date_update')
        table.char('description_md', max_length=255)
        table.int('user_id')
        table.char('version', max_length=255)
        table.bool('is_published')
        table.int('starting_threat')


def downgrade(migrator):
    migrator.drop_table('deck')
