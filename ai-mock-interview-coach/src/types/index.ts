export type Profile = {
  id: string;
  email: string;
  full_name?: string;
  target_role?: string;
  seniority?: string;
  years_of_experience?: number;
  primary_programming_language?: string;
  preferred_difficulty?: string;
  preferred_categories?: string[];
  target_company?: string;
  interview_date?: string;
  onboarding_completed: boolean;
};

// Add other base types as needed
