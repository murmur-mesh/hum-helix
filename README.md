# hum-helix

hum-helix is a local first speech to text (stt) event service designed for distributed AI systems built on top of models like [faster-whisper](https://github.com/SYSTRAN/faster-whisper).

In its current form, it is a hacked together fastAPI wrapper, benchmarking tool, and Docker utility for faster-whisper, but is evolving into a realtime event node designed to work in orchestration with other event driven AI systems.

## Why hum-helix?

This project exists partly to learn by building, but also to fit the architecture vision of a local event driven AI pipeline.

- **Event drive by design**: communicate with other services and logic layers by emitting structured events through Redis, Kafka, and other message bus systems.
- **Model agnostic / swappable**: switch between various models
- **Observable**: built in Promethius metrics and a simple live dashboard for real time monitoring, optionally system level open telemetry integration.
- **Local-first**: docker ready, locally deployable on your own hardware.

## Getting Started

Run the small fastAPI server:

```bash
uv pip install -e .
uv run start
```

Docker:

```bash
docker compose up --build
```

### API

`POST /v1/models/load`

Body

```json
{
    "model":"medium.en",            # faster-whisper model strings
    "device": "cuda",               # or cpu
    "compute_type": "int8_float16", # or int8 / float16
    "download_root": "/models"      # optional
}
```

`POST /v1/models/unload`

Body

```json
{
  "model": "medium.en"   # faster-whisper model strings
}
```

`GET /v1/models/loaded`

returns

```json
{"models": []}   # array of loaded models (empty when none)
```

`GET /ping`

returns

```json
{ "status": "healthy" }
```

## Early Status

Right now this project is _very_ **early** and **experimenal**.

Consists a minimal fastAPI HTTP REST server wrapped around faster-whisper with minimal capabilities. Also includes an in progress benchmark harness for faster_whisper, with a light visualization layer with pandas and streamlit for yaml data.

Named `hum-helix` to fit inside a suite of local AI tools centered around audio first design. Project names may change over time.

## The Benchmark Utility

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

## contributions

As you can see this project is in early stage experimental areas, not quite ready for contributions or formal git flow, but feel free to dive into the mess.

Development is currently just a main -> dev -> feature branch style with no formal merging. Just hacking it together right now!
