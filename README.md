# hum-helix

Hacked together python stt service using faster-whisper.

Named `hum-helix` to fit inside a suite of local AI tools centered around audio first design. Project names may change over time.

## current status

Using `benchmark.py` to run gpu transcription and time benchmarks for various models. Uses a custom yaml config to load benchmark settings, and creates various `faster-whisper` setups to test.

Writes the yaml output to a static directory in the host machine running docker, currently:

`/opt/hum-helix/benchmark-*.db.yaml`

Where `*` is a datetime stamp mostly just to make it somewhat unique.

Using `rsync` to get the results from the host machine.

Currently that is the workflow to run test on a remote machine with a gpu over ssh with a docker context.

## next up

Build a visualization script for consuming benchmark results.

## long term

A brief overview of the possible future:

- stt whisper (faster-whisper library) wrapped in fast api inside docker
- stream audio to fast api server from web front end
- chunk, convert, and combine results for accuracy and real time speed
- later stream output results in smalller chunks for testing
- respond to different modes for higher accuracy vs slower speed, and real time uses

May look into possibly running a small inference model to test intent, maybe in a rolling way, in order to pick up tool usage, possibly preload or prepare services.
