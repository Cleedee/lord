"""
criar tabela game
date created: 2021-10-23 01:23:59.022458
"""


def upgrade(migrator):
    with migrator.create_table('game') as table:
        table.primary_key('id')


def downgrade(migrator):
    pass
