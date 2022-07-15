"""
criar campo quest em card
date created: 2022-07-15 03:04:57.917067
"""


def upgrade(migrator):
    migrator.add_column('card', 'quest', 'int', default=0)


def downgrade(migrator):
    migrator.drop_column('card', 'quest')
