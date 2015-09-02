export PYTHONPATH := $(PYTHONPATH):$(shell pwd)

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

verify:
	flake8 add_data app tests

test:
	nosetests tests/ \
		-sv \
		--with-coverage \
		--cover-package=app \
		--cover-erase
	gulp build
	gulp test

new_db:
	rm -rf ./migrations
	python db.py db init
	python db.py db migrate
	python db.py db upgrade
	psql -d rva-screening -a -f app/audit_triggers.sql

data:
	python add_data/clear_db.py -local
	python add_data/add_mock_data.py

migrate:
	python db.py db migrate

upgrade:
	python db.py db upgrade

db_update:
	make migrate
	make upgrade

add_triggers:
	psql -d rva-screening -a -f app/audit_triggers.sql

deploy_static:
	gulp build
	python ./upload_assets.py

deploy:
	make deploy_static
	git push heroku master
	git push spanish master
	heroku run python add_data/clear_db.py
	heroku pg:psql < app/audit_triggers.sql
	heroku run python add_data/add_mock_data.py

update_translations:
	pybabel extract -F app/babel.cfg -o app/messages.pot .
	pybabel update -i app/messages.pot -d app/translations

init_translationss:
	pybabel extract -F app/babel.cfg -o app/messages.pot .
	pybabel init -i app/messages.pot -d app/translations -l es_US

compile_translations:
	pybabel compile -d app/translations
