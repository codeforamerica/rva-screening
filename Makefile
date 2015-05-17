run:
	foreman run python run.py \
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


deploy_static:
	gulp build
	python ./upload_assets.py
