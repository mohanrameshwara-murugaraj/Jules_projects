# Local Transcription

Speech-to-text is performed locally in the user's browser using Transformers.js and the Whisper model (e.g., `onnx-community/whisper-tiny.en`).

- Execution occurs within a Web Worker.
- WebGPU is used where supported; fallback to WASM.
- Raw audio is never uploaded to the backend.