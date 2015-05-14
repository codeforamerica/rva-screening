run:
	foreman start web

migrate:
	python db.py db migrate

upgrade:
	python db.py db upgrade
