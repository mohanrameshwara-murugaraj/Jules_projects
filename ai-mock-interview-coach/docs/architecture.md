# Architecture

The application is built on a fully serverless, free-tier compatible stack:

- **Frontend:** React + TypeScript + Vite, deployed on Cloudflare Pages.
- **Backend / Database:** Supabase (PostgreSQL, Supabase Auth).
- **Functions:** Supabase Edge Functions for handling sensitive Gemini API calls.
- **AI Processing:** Google Gemini API (via Edge Functions) and browser-side Whisper (Transformers.js) for speech-to-text.

## Flow
Microphone -> browser recording -> local Whisper transcription -> transcript -> Supabase Edge Function -> Gemini -> Validated JSON feedback -> Supabase DB.