run:
	cd ./src && exec poetry run uvicorn main:app --reload --host=${HOST} --port=${PORT}
