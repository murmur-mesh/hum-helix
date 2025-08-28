# hum-helix

hum-helix is a local first speech to text (stt) event service designed for distributed AI systems built on top of models like [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

In its current form, it is a hacked together python benchmarking tool and Docker utility for faster-whisper, but is evolving into a realtime event node designed to work in orchestration with other event driven AI systems.

## Why hum-helix?

This project exists partly to learn by building, but also to fit the architecture vision of a local event driven AI pipeline.

- **Event drive by design**: communicate with other services and logic layers by emitting structured events through Redis, Kafka, and other message bus systems.
- **Model agnostic / swappable**: switch between various models
- **Observable**: built in Promethius metrics and a simple live dashboard for real time monitoring.
- **Local-first**: docker ready, locally deployable on your own hardware.

## Current Status

Right now this project is _very_ **early** and **experimenal**.

Just a minimal benchmark harness around faster whisper and docker, with a light visualization layer.

The vision is to grow into a more polished service.

Named `hum-helix` to fit inside a suite of local AI tools centered around audio first design. Project names may change over time.

## The Benchmark Utility

Using `src/benchmarks/scripts/benchmark.py` to run gpu transcription and time benchmarks for various models. Uses a custom yaml config to load benchmark settings, and creates various [faster-whisper](https://github.com/SYSTRAN/faster-whisper) setups to test.

Writes the yaml output to a static directory in the host machine running docker, currently:

`/opt/hum-helix/benchmark-*.db.yaml`

Where `*` is a datetime stamp mostly just to make it somewhat unique.

Using `rsync` to get the results from the host machine.

Currently this is the workflow used to run tests on a remote machine with a gpu over ssh within a docker context.

Heres an example of the current workflow:

```bash
docker coxtent use v1 # v1 my local ssh context
docker compose up --build # or without --build to rerun test

# makefile sync-bench-results localy rsync:
rsync -avz --progress v1:/opt/hum-helix/benchmark-*.db.yaml ./src/benchmarks/results/
```

## Benchmark Results Visualization

Very bare streamlit pandas table vizualization exists to average metrics and sort them easily.

After gathering yaml results in `src/benchmarks/results/` you can view them aggegated by running:

```bash
uv run streamlit run src/benchmarks/viz/dashboard.py
```

## Benchmark domain terms

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

## setuptools alternatives

Don't really like setuptools egg artifacts, so these are options to explore:

- hatchling
- flit

## contributions

As you can see this project is in early stage experimental areas, not quite ready for contributions or formal git flow, but feel free to dive into the mess.

Development is currently just a main -> dev -> feature branch style with no formal merging. Just hacking it together right now!
