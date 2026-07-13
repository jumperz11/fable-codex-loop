.PHONY: help init freeze verify doctor doctor-example test validate

help:
	@echo "JudgeLoop"
	@echo ""
	@echo "  make init            Set up docs/ memory in the current repo"
	@echo "  make freeze          Lock the current gate with SHA-256"
	@echo "  make verify          Verify every frozen gate lock"
	@echo "  make doctor          Check if repo memory is ready for a build block"
	@echo "  make doctor-example  Validate the bundled example run"
	@echo "  make test            Run invariant regression tests"
	@echo "  make validate        Validate package links, skill metadata, and scripts"

init:
	python3 scripts/init.py .

freeze:
	python3 scripts/gates.py freeze .

verify:
	python3 scripts/gates.py verify .

doctor:
	python3 scripts/doctor.py .

doctor-example:
	python3 scripts/doctor.py examples/demo-run/repo

test:
	python3 -m unittest discover -s tests -p 'test_*.py' -v

validate:
	python3 scripts/doctor.py examples/demo-run/repo
	npm --prefix examples/demo-run/repo test
	python3 -m py_compile scripts/doctor.py scripts/gates.py scripts/init.py tests/validate_repo.py tests/test_judgeloop.py bin/judgeloop
	python3 -m unittest discover -s tests -p 'test_*.py' -v
	python3 tests/validate_repo.py
	python3 bin/judgeloop verify examples/demo-run/repo
	python3 bin/judgeloop doctor examples/demo-run/repo
