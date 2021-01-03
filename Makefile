PYTHON = python3
PIP = pip3

lint:
	pylint src/

install:
	 $(PIP) install -r requirements.txt
