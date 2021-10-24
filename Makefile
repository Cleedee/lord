status:
	peewee-db --directory=migrations --database=sqlite:///database.db status
upgrade:
	peewee-db --directory=migrations --database=sqlite:///database.db upgrade
