"""
criar tabela scenariocard
date created: 2021-11-18 17:20:55.977655
"""


def upgrade(migrator):
    with migrator.create_table('scenariocard') as table:
        table.primary_key('id')
        table.int('code')
        table.char('name', max_length=255)
        table.char('type_name', max_length=255)
        table.text('text', null=True)
        table.text('shadow', null=True)
        table.char('pack_code', max_length=255)
        table.char('pack_name', max_length=255)
        table.char('traits', max_length=255, null=True)
        table.char('keywords', max_length=255, null=True)
        table.int('quantity')
        table.bool('is_unique')
        table.int('threat',null=True)
        table.int('health',null=True)
        table.int('attack',null=True)
        table.int('defense',null=True)        
        table.char('cycle', max_length=255)
        table.char('encounter', max_length=255)
        table.int('num_quest',null=True)
        table.int('quest',null=True)
        table.text('notes', null=True)
        table.int('victory', null=True)
        table.int('engage')




def downgrade(migrator):
    migrator.drop_table('scenariocard')
