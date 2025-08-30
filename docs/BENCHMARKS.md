# Benchmark Tool

### Not yet implemented with the server, and Dockerfile no longer builds this.

Using `src/hum_helix/benchmarks/scripts/benchmark.py` to run gpu transcription and time benchmarks for various models. Uses a custom yaml config to load benchmark settings, and creates various [faster-whisper](https://github.com/SYSTRAN/faster-whisper) setups to test.

Writes the yaml output to a static directory in the host machine running docker, currently:

`/opt/hum-helix/benchmark-*.db.yaml`

Where `*` is a datetime stamp mostly just to make it somewhat unique.

Using `rsync` to get the results from the host machine.

Heres an example of the current workflow (when working with Docker, currently being moved to server flow):

```bash
docker coxtent use v1 # v1 my local ssh context
docker compose up --build # or without --build to rerun test

# makefile sync-bench-results localy rsync:
rsync -avz --progress v1:/opt/hum-helix/benchmark-*.db.yaml ./src/benchmarks/results/
```

## Benchmark Results Visualization

Very bare streamlit pandas table vizualization exists to average metrics and sort them easily.

After gathering yaml results in `src/hum_helix/benchmarks/results/` you can view them aggegated by running:

```bash
uv run streamlit run src/hum_helix/benchmarks/viz/dashboard.py
```

## Domain Terms

Terms to refactor and expand code with so it fits benchmarking domain, providing consistenty in communication. Will integrate later when relevant.

- **benchmark** - thing you want to measure in specific conditions
- **system under test** (sut) - whats system is being measured
- **workload** - input and operations the SUT works with
- **benchmark definition** - spec of the benchmark
- **run config** - parameters for one specific benchmark run
- **runner** - script that runs a benchmark
- **harness** - ochestration around the runner
- **trial or iteration** - one execution of a run config
- **run** - set of trials executed together
- **metrics** - what you record when you measure
- **artifacts** - files produced from a run
- **results** - structured record for a run or trial
- **baseline** - reference result to compare against
- **regessionr or improvement** - change vs baseline given a tolerance or threshhold
- **provenance** - everything needed to reproduce the test

May not use all these terms, they are included here for future reference when refactoring a benchmark system. This should be implemented more fully one the system becomes robust, wrapped in api (or standalone cli?), not hacked, but an actual final usable system.
