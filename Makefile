.PHONY: help init doctor doctor-example validate

help:
	@echo "Fable + Builder Loop"
	@echo ""
	@echo "  make init            Set up docs/ memory in the current repo"
	@echo "  make doctor          Check if repo memory is ready for a build block"
	@echo "  make doctor-example  Validate the bundled example run"
	@echo "  make validate        Validate package links, skill metadata, and scripts"

init:
	python3 scripts/init.py .

doctor:
	python3 scripts/doctor.py .

doctor-example:
	python3 scripts/doctor.py examples/demo-run/repo

validate:
	python3 scripts/doctor.py examples/demo-run/repo
	python3 -m py_compile scripts/doctor.py scripts/init.py tests/validate_repo.py
	python3 tests/validate_repo.py
