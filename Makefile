VENV        = venv
PYTHON     := ./$(VENV)/bin/python3
PIP        := ./$(VENV)/bin/pip
PRE_COMMIT := ./$(VENV)/bin/pre-commit

all: venv

.PHONY: venv
venv: $(VENV)/bin/activate

.PHONY: $(VENV/bin/activate)
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install --requirement requirements.txt

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

run: $(VENV)
	$(PYTHON) ./script.py
