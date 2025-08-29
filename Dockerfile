
# cuda stuff for ctranslate 2
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# minimal tools + ffmpeg (dont really need ffmpeg for faster-whisper
RUN apt-get update && apt-get install -y curl ca-certificates ffmpeg && rm -rf /var/lib/apt/lists/*

# uv for python and dependencies
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app
COPY . . 

EXPOSE 8000

# COPY pyproject.toml uv.lock ./      
RUN uv sync --frozen --python 3.12 --no-dev || uv sync --python 3.12 --no-dev
RUN uv pip install -e .


# run test file
# CMD ["uv", "run", "--python", "3.12", "python", "src/benchmarks/scripts/benchmark.py"]

# start the server with pyproject.toml script
CMD ["uv", "run", "start"]