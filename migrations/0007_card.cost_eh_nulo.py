"""
card.cost eh nulo
date created: 2022-06-28 02:31:01.753639
"""


def upgrade(migrator):
    migrator.drop_not_null('card', 'cost')


def downgrade(migrator):
    migrator.add_not_null('card', 'cost')
