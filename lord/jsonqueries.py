from pyjsonq import JsonQ

SCENARIOS_FILE = 'lord/data/scenarios_all.json'



def encontra_cartas_conjunto_por_nome(nome_conjunto):
    qe = JsonQ(SCENARIOS_FILE)
    res = qe.where('encounter_set','=', nome_conjunto).get()
    return res

def encontra_carta_cenario_por_nome(nome):
    qe = JsonQ(SCENARIOS_FILE)
    res = qe.where('name','contains', nome).get()
    return res