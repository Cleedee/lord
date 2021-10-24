"""
criar tabela game
date created: 2021-10-23 01:23:59.022458
"""


def upgrade(migrator):
    with migrator.create_table('game') as table:
        table.primary_key('id')
        table.int('nplayers', default = 1)
        table.int('rounds', default = 1)
        table.bool('active', default = False)


def downgrade(migrator):
    migrator.drop_table('game')
