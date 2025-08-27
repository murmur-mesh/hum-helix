from faster_whisper import WhisperModel
import time

# all this stuff is a hacked together script for testing purposes

totalTimeStart = time.perf_counter()
print("Loading model")
start = time.perf_counter()

# models
#   tiny, tiny.en,
#   base, base.en,
#   small, small.en, distil-small.en,
#   medium, medium.en, distil-medium.en,
#   large-v1, large-v2, large-v3, large, distil-large-v2, distil-large-v3,
#   large-v3-turbo, or turbo),


# will fix this later and start benchmarking - this is a placeholder hack
# gpu
model = WhisperModel(
    "distil-medium.en", "cuda", compute_type="float16", download_root="/models"
)
# cpu
# model = WhisperModel("large-v3-turbo", "cpu", compute_type="int8", cpu_threads=8)
end = time.perf_counter()
print(f"Model loaded in {end - start:.2f} seconds")

print("Segmenting")
start = time.perf_counter()
segments, info = model.transcribe(
    "test2.wav", beam_size=1, vad_filter=False, word_timestamps=False
)
end = time.perf_counter()

print(f"Segmentation completed in {end - start:.2f} seconds")

print("Transcribing Segments")

start = time.perf_counter()
for segment in segments:
    print(segment.text)
end = time.perf_counter()

print(f"Segment Transcription completed in {end - start:.2f} seconds")
totalTimeEnd = time.perf_counter()
print(f"Total time taken: {totalTimeEnd - totalTimeStart:.2f} seconds")
