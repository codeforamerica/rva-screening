install:
	npm install
	pip install -r ./requirements.txt

run:
	gulp & 
	foreman run python run.py \
		--env=.env

correr:
	gulp & 
	BABEL_DEFAULT_LOCALE='es_US' \
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
	make new_db
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
	git push spanish master

update_translations:
	pybabel extract -F app/babel.cfg -o app/messages.pot .
	pybabel update -i app/messages.pot -d app/translations

init_translationss:
	pybabel extract -F app/babel.cfg -o app/messages.pot .
	pybabel init -i app/messages.pot -d app/translations -l es_US

compile_translations:
	pybabel compile -d app/translations
