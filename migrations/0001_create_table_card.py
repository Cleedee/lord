"""
create table card
date created: 2021-10-14 03:38:16.203339
"""


def upgrade(migrator):
    with migrator.create_table('card') as table:
        table.primary_key('id')
        table.int('code')
        table.char('pack_code', max_length=255)
        table.char('pack_name', max_length=255)
        table.char('type_code', max_length=255)
        table.char('type_name', max_length=255)
        table.char('sphere_code', max_length=255)
        table.int('position')
        table.char('name', max_length=255)
        table.char('traits', max_length=255, null=True)
        table.char('text', max_length=255, null=True)
        table.bool('is_unique')
        table.int('threat')
        table.int('willpower')
        table.int('attack')
        table.int('defense')
        table.int('health')
        table.int('quantity')
        table.bool('deck_limit')
        table.bool('has_errata')
        table.char('url', max_length=255)
        table.char('imagesrc', max_length=255)


def downgrade(migrator):
    migrator.drop_table('card')
