# AI Evaluation

AI feedback is provided by the Google Gemini free-tier API.

- Calls to Gemini are restricted to Supabase Edge Functions.
- The client only passes the user's transcript to the function.
- Prompts request strictly structured JSON.
- Feedback is validated using Zod prior to saving it in the database and returning it to the user.