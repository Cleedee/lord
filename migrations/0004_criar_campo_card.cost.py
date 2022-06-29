"""
criar campo card.cost
date created: 2021-10-14 03:43:33.088375
"""


def upgrade(migrator):
    migrator.add_column('card', 'cost', 'char', max_length=255, null=True)


def downgrade(migrator):
    migrator.drop_column('card', 'cost', cascade=True)
