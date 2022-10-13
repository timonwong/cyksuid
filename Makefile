.PHONY: build
build:
	unset CYKSUID_DEBUG; python setup.py build_ext --inplace --with-cython

.PHONY: build-debug
build-debug:
	export CYKSUID_DEBUG=1; python setup.py build_ext --inplace --with-cython

.PHONY: coverage
coverage: build-debug
	PYTHONPATH=. pytest -v --cov --cov-report=term --cov-report=xml:coverage.xml
	@for f in $(shell find cyksuid -type f -name "*.pyx"); do \
		echo "Annotating $${f}"; \
		cython --cplus -3 --annotate-coverage=coverage.xml $${f}; \
	done

.PHONY: test
test: build
	PYTHONPATH=. pytest -v

.PHONY: bench
bench: build
	pip install svix-ksuid
	pytest bench.py --benchmark-group-by=func --benchmark-json bench.json
