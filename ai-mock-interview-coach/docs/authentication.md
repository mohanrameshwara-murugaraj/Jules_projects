# Authentication

Authentication is handled securely via Supabase Auth using email and password.

Supabase manages JWT sessions and refresh tokens. No custom JWT handling or raw token storage in `localStorage` is used; we rely entirely on the official Supabase client.