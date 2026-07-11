# Security

- **Secrets:** API keys (e.g., Gemini) are stored only as Edge Function secrets, never on the frontend.
- **Data Access:** Enforced heavily via Supabase RLS policies.
- **Untrusted Input:** All inputs to Edge Functions (including the transcript) are treated as untrusted and validated with Zod. Prompt injection mitigations are employed.