# API for REST Server around faster-whisper

### REST practices

- resources use nouns
- make paths plural
- http methods for verbs
  - GET: read
  - POST: create or perform an action
  - DELETE: remove
  - PATCH: update (partially?)

Async pipelines might look like this:

- `202 Accepteted` with payload `{id, status}`
- Clients can poll with get using the `id`

## REST Endpoints

<details>
 <summary><code>GET /ping</code></summary>

#### Response

```json
{ "status": "healthy" }
```

</details>
<details>
 <summary><code>POST /v1/models/load</code></summary>

#### Body Format

```json
{
    "model":"medium.en",            # faster-whisper model strings
    "device": "cuda",               # or cpu
    "compute_type": "int8_float16", # or int8 / float16
    "download_root": "/models"      # optional
}
```

</details>

<details>
 <summary><code>POST /v1/models/unload</code></summary>

#### Body

```json
{ "model": "medium.en" }  # faster-whisper model strings
```

</details>
<details>
 <summary><code>GET /v1/models/loaded</code></summary>

#### Response

```json
{"models": []}   # array of loaded models (empty when none)
```

</details>

<details>
 <summary><code>POST /v1/audio/transcriptions</code></summary>

#### Simple wave file audio upload with form-data multipart upload

#### multipart/form-data

```bash
file: audio/wave mime content
```

#### response

```json
{ "text": "transcription of the audio file" }
```

</details>

## WebSocket streaming

For transcribing streaming audio:

`WS /v1/streams/transcribe`

Client could send

```
{type:"init" model, language?, vad, beam_size}
{type:"audio_chunk", sequence, pc|opus}
```

Server could emit:

```
{type:"partial", sequence, text}
{type:"segment", index, start, end, text}
{type:"final", text, segments:[]}
{type:"error", message}

```
