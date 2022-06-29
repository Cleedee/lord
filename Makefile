status:
	peewee-db --directory=migrations --database=sqlite:///database.db status
upgrade:
	peewee-db --directory=migrations --database=sqlite:///database.db upgrade
revision:
	peewee-db --directory=migrations --database=sqlite:///database.db revision "$(message)"
upgrade-fake:
	peewee-db --directory=migrations --database=sqlite:///database.db upgrade target=$(target) fake=$(fake)
