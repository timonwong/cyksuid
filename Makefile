.PHONY: bench
bench:
	pytest bench.py --benchmark-json bench.json && jq '.benchmarks[] | {name, "mean": .stats["mean"]} ' bench.json
