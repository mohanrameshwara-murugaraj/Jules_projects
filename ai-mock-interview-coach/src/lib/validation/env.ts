import { z } from "zod";

export const envSchema = z.object({
  VITE_APP_NAME: z.string().default("AI Mock Interview Coach"),
  VITE_APP_URL: z.string().url(),
  VITE_SUPABASE_URL: z.string().url(),
  VITE_SUPABASE_ANON_KEY: z.string().min(1),
  VITE_WHISPER_MODEL: z.string().default("onnx-community/whisper-tiny.en"),
  VITE_MAX_RECORDING_SECONDS: z.coerce.number().default(180),
  VITE_MAX_QUESTIONS_PER_SESSION: z.coerce.number().default(5),
});

const _env = envSchema.safeParse(import.meta.env);

if (!_env.success) {
  console.error("❌ Invalid environment variables:", _env.error.format());
  throw new Error("Invalid environment variables");
}

export const env = _env.data;