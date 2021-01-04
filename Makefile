PYTHON = python3
PIP = pip3

lint:
	pylint src/ tests/

install:
	 $(PIP) install -r requirements.txt

test:
	${PYTHON} -m pytest tests/ -v

clean:
	find . -type f -name \*.pyc -exec rm {} \;
