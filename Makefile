install:
	virtualenv venv; \
	source venv/bin/activate; \
	pip install -r requirements.txt; \


run:
	source venv/bin/activate; \
	python scripts/activity_collect/; \

test: