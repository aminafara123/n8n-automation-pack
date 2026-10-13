PY ?= python3
.PHONY: install test validate run

install:
	$(PY) -m pip install -r requirements.txt

test:
	$(PY) -m pytest -q

# human-readable per-file report
validate:
	$(PY) validate.py

# nothing to serve offline; the "run" is validating the pack is import-ready
run: validate
