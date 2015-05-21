run:
	gulp & 
	foreman run python run.py \
		--env=.env

test:
	nosetests tests/ \
		-sv \
		--with-coverage \
		--cover-package=app \
		--cover-erase 

test_travis:
	psql -c 'drop database if exists screener_test;' -U postgres
	psql -c 'create database screener_test;' -U postgres
	make test

new_db:
	rm -rf ./migrations
	python db.py db init
	python db.py db migrate
	python db.py db upgrade

migrate:
	python db.py db migrate

upgrade:
	python db.py db upgrade

deploy_static:
	gulp build
	python ./upload_assets.py

deploy:
	make deploy_static
	git push heroku master
