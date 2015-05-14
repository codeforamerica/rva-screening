run:
	foreman start web \
		--env=.env

new_db:
	rm -rf ./migrations
	python db.py db init
	python db.py db migrate
	python db.py db upgrade

migrate:
	python db.py db migrate

upgrade:
	python db.py db upgrade
