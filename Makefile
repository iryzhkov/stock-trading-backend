PYTHON = python3
PIP = pip3

lint:
	pylint src/ tests/

install:
	 $(PIP) install -r requirements.txt

test:
	${PYTHON} -m pytest tests/ -v

coverage:
	coverage erase
	coverage run -m pytest tests/
	coverage report --include "src/*"

clean:
	find . -type f -name \*.pyc -exec rm {} \;
