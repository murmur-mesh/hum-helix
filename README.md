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

### REST and WebSocket API

See `/docs/API.md`

## Early Status

Right now this project is _very_ **early** and **experimenal**.

Consists a minimal fastAPI HTTP REST server wrapped around faster-whisper with minimal capabilities. Also includes an in progress benchmark harness for faster_whisper, with a light visualization layer with pandas and streamlit for yaml data.

Named `hum-helix` to fit inside a suite of local AI tools centered around audio first design. Project names may change over time.

## Benchmark Tool

Not yet integrated with server api.

See `/docs/BENCHMARKS.md` for old script details

## contributions

As you can see this project is in early stage experimental areas, not quite ready for contributions or formal git flow, but feel free to dive into the mess.

Development is currently just a main -> dev -> feature branch style with no formal merging. Just hacking it together right now!
