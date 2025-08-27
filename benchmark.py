from faster_whisper import WhisperModel
from contextlib import contextmanager
import yaml
import wave
from timer import Timer


print("Running Benchmark Utility\n")
# load benchmark config file

print("Loading benchmark config")
with open("benchmark.config.yaml", "r") as f:
    configs = yaml.safe_load(f)


print(f"Found {len(configs['benchmarks'])} benchmark configurations\n")
print("Starting Benchmarks\n")
# loop over each benchmark config and run it
for config in configs["benchmarks"]:

    print(
        f"Running benchmark for model",
        f"\033[32m{config['model']}\033[0m",
        f"using \033[33m{config['device']}\033[0m",
        f"on file \033[34m{config['audio_file']}\033[0m",
    )
    with Timer() as t:
        model = WhisperModel(
            config["model"],
            config["device"],
            compute_type=config["compute_type"],
        )
        load_time = t.lap

        segments, info = model.transcribe(
            config["audio_file"],
            beam_size=config["beam_size"],
            vad_filter=config["vad_filter"],
            word_timestamps=config["word_timestamps"],
        )
        inference_time = t.lap

        transcription = ""
        for segment in segments:
            transcription += segment.text
        transcription_time = t.lap

    total_time = t.elapsed

    # get duration of wav file
    with wave.open(config["audio_file"], "rb") as w:
        frames = w.getnframes()
        rate = w.getframerate()
        duration = frames / float(rate)

    total_transcription_time = transcription_time + inference_time
    config["load_time"] = load_time
    config["inference_time"] = inference_time
    config["transcription_time"] = transcription_time
    config["total_time"] = total_time
    config["rtf"] = (inference_time + transcription_time) / duration
    config["total_transcription_time"] = total_transcription_time
    config["audio_duration"] = duration
    config["transcription"] = transcription
    print(
        f"\tBenchmark completed in {total_time:.3f} sec\n",
        f"\tRTF: {config['rtf']:.3f}\n",
        f"\tModel Work Time: \033[33m{total_transcription_time:.3f} sec\033[0m\n",
    )
    # append results to benchmark_results.yaml
    with open("benchmark.db.yaml", "a") as f:
        yaml.dump([config], f)

print("Done")
