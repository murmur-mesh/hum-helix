from faster_whisper import WhisperModel
from contextlib import contextmanager
import yaml
import wave
from datetime import datetime
from benchmarks.scripts.timer import Timer


print("Running Benchmark Utility\n")

# note on path resolutions in this file:
# all paths are relative to the project root for docker
# in the future paths that work in both environments will be used
# but right its only ever run in docker anyways

# later used to make the file name somewhat unique
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

print("Loading benchmark config")
with open("./src/benchmarks/configs/benchmark.config.yaml", "r") as f:
    configs = yaml.safe_load(f)


print(f"Found {len(configs['benchmarks'])} benchmark configurations\n")
print("Starting Benchmarks\n")
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
            download_root=configs["download_root"],
        )
        config["load_time"] = t.lap

        segments, info = model.transcribe(
            f"./src/benchmarks/workloads/{config['audio_file']}",
            beam_size=config["beam_size"],
            vad_filter=config["vad_filter"],
            word_timestamps=config["word_timestamps"],
        )
        config["inference_time"] = t.lap

        config["transcription"] = ""
        for segment in segments:
            config["transcription"] += segment.text
        config["transcription_time"] = t.lap

    config["total_time"] = t.elapsed

    # get duration of wav file
    with wave.open(f"./src/benchmarks/workloads/{config['audio_file']}", "rb") as w:
        frames = w.getnframes()
        rate = w.getframerate()
        config["audio_duration"] = frames / float(rate)

    config["total_transcription_time"] = (
        config["transcription_time"] + config["inference_time"]
    )
    config["rtf"] = config["total_transcription_time"] / config["audio_duration"]

    print(
        f"\tBenchmark completed in {config["total_time"]:.3f} sec\n",
        f"\tRTF: {config['rtf']:.3f}\n",
        f"\tModel Work Time: \033[33m{config["total_transcription_time"]:.3f} sec\033[0m\n",
    )
    # append results to benchmark_results.yaml
    with open(f"./output/benchmark-{timestamp}.db.yaml", "a") as f:
        yaml.dump([config], f)

print("Done")
