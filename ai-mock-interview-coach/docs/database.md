# Database

The database uses Supabase PostgreSQL.

All access is governed by Row-Level Security (RLS) policies to ensure users can only access their own data. Primary keys use UUIDs.
Tables include profiles, interview_sessions, session_questions, feedback, and topic_mastery.