import glob, yaml
import pandas as pd
import streamlit as st
from pathlib import Path


st.set_page_config(layout="wide", page_title="Benchmark Dashboard")

# ./ refers to directory script is run from
# need some sort of path resultion in the future
files = sorted(glob.glob("./src/benchmarks/results/benchmark-*.db.yaml"))
print(files)
if not files:
    st.warning("No run result files found in src/benchmarks/results")
    st.stop()
else:
    st.success(f"Found {len(files)} run results.")


# form Dataframe from files
benchmark_results = []

for f in files:
    data = yaml.safe_load(Path(f).read_text())
    benchmark_results += data

df = pd.DataFrame(benchmark_results)


group_cols = ["model", "device", "beam_size", "audio_file"]
value_cols = ["total_transcription_time", "inference_time", "transcription_time", "rtf"]

for c in value_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")

view_five_seconds = df[df["audio_file"] == "5s.wav"]
view_thirty_seconds = df[df["audio_file"] == "30s.wav"]
agg_5 = view_five_seconds.groupby(group_cols, as_index=False)[value_cols].agg(
    **{f"avg_{c}": (c, "mean") for c in value_cols}
)
agg_30 = view_thirty_seconds.groupby(group_cols, as_index=False)[value_cols].agg(
    **{f"avg_{c}": (c, "mean") for c in value_cols}
)

st.subheader(f"Averages for 5s.wav")
st.dataframe(agg_5)

st.subheader(f"Averages for 30s.wav")
st.dataframe(agg_30)

st.subheader(f"All Data")
st.dataframe(df)
