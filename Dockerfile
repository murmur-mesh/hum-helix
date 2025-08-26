FROM python:3.12.10-slim
WORKDIR /app
COPY . .
RUN pip install uv && pip install faster-whisper
CMD ["python", "transcription-test.py"]
