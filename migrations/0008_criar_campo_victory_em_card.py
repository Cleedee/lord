"""
criar campo victory em card
date created: 2022-07-15 02:50:27.964822
"""


def upgrade(migrator):
    migrator.add_column('card', 'victory', 'int', default=0)


def downgrade(migrator):
    migrator.drop_column('card', 'victory')
