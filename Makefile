build:
	python3 -m venv .venv
	cd .venv/bin/ && source activate
	pip install -r requirements.txt
	docker-compose up

run:
	faust -A event_stream worker -l info
