
# CUDA and cuDNN for CTranslate2
FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu22.04

# minimal tools + ffmpeg
RUN apt-get update && apt-get install -y curl ca-certificates ffmpeg && rm -rf /var/lib/apt/lists/*

# uv for python and dependencies
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY pyproject.toml uv.lock ./      
RUN uv sync --frozen --python 3.12 --no-dev || uv sync --python 3.12 --no-dev

COPY . .

# run test file
CMD ["uv", "run", "--python", "3.12", "python", "benchmark.py"]
