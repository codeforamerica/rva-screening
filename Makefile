run:
	gulp & 
	foreman run python run.py \
		--env=.env

new_db:
	rm -rf ./migrations
	python db.py db init
	python db.py db migrate
	python db.py db upgrade
	psql -d rva-screening -a -f app/audit_triggers.sql

migrate:
	python db.py db migrate

upgrade:
	python db.py db upgrade

add_triggers:
	psql -d rva-screening -a -f app/audit_triggers.sql

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
