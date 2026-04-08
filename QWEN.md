# LORD - Projeto de Jogo Lord of the Rings LCG

## Visão Geral do Projeto

**LORD** é uma aplicação Python para jogar o card game **Lord of the Rings: Living Card Game (LCG)** no console interativo do Python. O projeto permite importar decks, cenários e gerenciar partidas do jogo de cartas.

### Tecnologias Principais

- **Python 3.12+**
- **Poetry** para gerenciamento de dependências
- **Peewee ORM** para banco de dados SQLite
- **Rich** para interface de terminal formatada
- **BeautifulSoup4** e **Requests** para scraping de dados
- **Tornado** para servidor web (possível interface futura)
- **PyJSONQ** para consultas JSON

### Arquitetura

O projeto segue uma arquitetura orientada a objetos com:

1. **Camada de Modelo** (`lord/bases.py`, `lord/concretas.py`):
   - Classes base para cartas do jogo (Hero, Aliado, Evento, Acessório, etc.)
   - Classes para cartas de cenário (Inimigo, Localidade, Missão, etc.)
   - Implementação do padrão Observer para reatividade

2. **Camada de Dados** (`lord/database.py`, `lord/repository.py`):
   - Modelos Peewee para persistência (Card, Deck, Slot, Game, Scenario)
   - Repositório para operações de banco de dados

3. **Camada de Carregamento** (`lord/loader.py`):
   - Funções para carregar decks de jogadores e cenários do banco de dados

4. **Utilitários** (`lord/utils.py`, `lord/scrap.py`):
   - Funções auxiliares para conversão de dados e scraping

## Estrutura do Projeto

```
lord/
├── lord/
│   ├── __init__.py       # Classes principais do jogo (Carta, Jogo, Jogador, etc.)
│   ├── bases.py          # Classes abstratas (Observador, Sujeito)
│   ├── concretas.py      # Implementações concretas (JogoConcreto, CartaConcreta)
│   ├── database.py       # Modelos Peewee ORM
│   ├── repository.py     # Funções de acesso ao banco de dados
│   ├── loader.py         # Carregamento de decks e cenários
│   ├── utils.py          # Utilitários e helpers
│   ├── scrap.py          # Scraping de dados externos
│   ├── packs.py          # Definições de pacotes/cenários
│   ├── jsonqueries.py    # Consultas JSON
│   ├── efeitos.py        # Efeitos de cartas
│   └── settings.py       # Configurações do projeto
├── scripts/
│   ├── play.py           # Script principal para iniciar o jogo
│   └── lord-cli          # Interface de linha de comando
├── tests/
│   ├── test_concretas.py
│   ├── test_decks.py
│   ├── test_encontros.py
│   ├── test_model.py
│   └── test_setups.py
├── migrations/           # Migrations do banco de dados
├── run.sh                # Script para iniciar o console interativo
├── Makefile              # Comandos de migration
└── pyproject.toml        # Configuração Poetry
```

## Instalação e Configuração

### Pré-requisitos

- Python 3.12 ou superior
- Poetry instalado

### Instalação das Dependências

```bash
poetry install
```

### Configuração do Banco de Dados

```bash
# Criar tabelas do banco de dados
poetry run python lord/database.py

# Verificar status das migrations
make status

# Aplicar migrations
make upgrade

# Criar nova migration
make revision message="descrição da migration"
```

## Comandos Principais

### Executar o Jogo

```bash
# Iniciar console interativo do Python com o jogo
./run.sh
# ou
poetry run python -i scripts/play.py
```

### Comandos do Makefile

| Comando | Descrição |
|---------|-----------|
| `make status` | Verificar status das migrations |
| `make upgrade` | Aplicar migrations pendentes |
| `make revision message="..."` | Criar nova migration |
| `make upgrade-fake target=X fake=Y` | Aplicar migration específica como fake |

### Executar Testes

```bash
poetry run pytest
```

## Uso no Console Interativo

Após iniciar o console com `./run.sh`, os seguintes objetos estão disponíveis:

```python
from lord import Colecao, Jogo

# Criar coleção e jogo
colecao = Colecao()
jogo = Jogo(colecao)

# Preparar jogador com deck
jogador = jogo.preparar_jogador('Nome Jogador', codigo_deck)

# Embaralhar deck
jogador.embaralhar_deck()

# Comprar mão inicial
jogador.comprar_mao_inicial()

# Escolher cenário
jogo.enfrentar_cenario('nome do cenário')
```

## Classes Principais

### Cartas do Jogador

- `Hero` - Heróis com atributos (threat, willpower, attack, defense, health)
- `Aliado` - Cartas aliadas
- `Evento` - Cartas de evento
- `Acessorio` - Acessórios/equipamentos
- `MissaoParalela` - Missões paralelas (player side quests)
- `Contrato` - Contratos

### Cartas de Cenário

- `Inimigo` - Inimigos com custo de engajamento
- `Localidade` - Localizações exploráveis
- `Missao` - Cartas de missão principal
- `Infortunio` - Treachery cards
- `Objetivo` - Cartas objetivo
- `ObjetivoAliado` - Aliados objetivo

### Gerenciamento do Jogo

- `Jogo` - Classe principal do jogo com áreas (deck de encontro, área de ameaça, etc.)
- `Jogador` - Representa um jogador com mão, heróis, mesa, recursos
- `Baralho` - Gerenciamento de decks
- `Area` / `AreaAmeaca` - Áreas de jogo

## Banco de Dados

### Tabelas Principais

| Tabela | Descrição |
|--------|-----------|
| `Card` | Cartas do jogo (atributos, tipo, esfera) |
| `Deck` | Decks de jogadores |
| `Slot` | Slots de cartas nos decks (heroes, cards, sideslots) |
| `Game` | Partidas ativas/salvas |
| `Scenario` | Cartas de cenário/encontro |

## Desenvolvimento

### Convenções de Código

- **Nomenclatura**: Português para variáveis e métodos, mantendo consistência com o domínio do jogo
- **Tipagem**: Type hints utilizados em várias funções
- **Estilo**: Uso de `rich` para output formatado no terminal

### Padrões de Projeto

- **Observer**: Implementado em `bases.py` para reatividade entre cartas e jogo
- **Repository**: Camada de abstração de dados em `repository.py`

### Adicionar Novas Funcionalidades

1. Criar classes de cartas em `lord/__init__.py` se necessário
2. Adicionar modelos de banco de dados em `lord/database.py`
3. Implementar funções de repositório em `lord/repository.py`
4. Adicionar testes em `tests/`

## TODO (do arquivo TODO.txt)

- [x] Base de dados para salvar decks, cartas e partidas (Peewee + SQLite)
- [x] Importar cartas de decks de encontro
- [ ] Implementar padrão Observador para cartas de objetivo
- [ ] Oferecer dicas para próximos passos

## Links e Recursos

- [RingsDB](https://ringsdb.com/) - Fonte para importação de decks
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) - Formato do CHANGELOG.md
- [Semantic Versioning](https://semver.org/spec/v2.0.0.html) - Versionamento do projeto
