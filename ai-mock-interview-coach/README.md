# AI Mock Interview Coach

An autonomous, free-tier AI Mock Interview Coach. This application helps software engineering job seekers practice technical and behavioral interviews by presenting role-specific questions, recording spoken answers, transcribing answers locally using Whisper, and evaluating them using the Gemini AI API via Supabase Edge Functions.

## Features
- Local, browser-side audio transcription (Whisper via Transformers.js).
- Serverless backend and database using Supabase.
- AI evaluation via Google Gemini API (free tier) from Supabase Edge Functions.
- Secure, free-tier compatible deployment (Cloudflare Pages).
- Comprehensive performance and behavioral feedback.

## Prerequisites
- Node.js (v18+)
- Supabase Free Account
- Google AI Studio API Key (Gemini)
- Cloudflare Account

## Local Development
1. Clone the repository and `npm install`.
2. Copy `.env.example` to `.env.local` and populate values.
3. Start the dev server: `npm run dev`.
