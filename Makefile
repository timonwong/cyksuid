.PHONY: build-debug
build-debug:
	export CY_DEBUG=1; python setup.py build_ext --inplace --with-cython

.PHOHY: build
build:
	unset CY_DEBUG; python setup.py build_ext --inplace --with-cython

.PHONY: coverage
coverage: build-debug
	PYTHONPATH=. pytest -v --cov --cov-report=term --cov-report=xml:coverage.xml
	@for f in $(shell find cyksuid -type f -name "*.pyx"); do \
		echo "Annotating $${f}"; \
		cython -3 --annotate-coverage=coverage.xml $${f}; \
	done

.PHONY: test
test: build
	PYTHONPATH=. pytest -v

.PHONY: bench
bench: build
	pytest bench.py --benchmark-json bench.json && jq '.benchmarks[] | {name, "mean": .stats["mean"]} ' bench.json
