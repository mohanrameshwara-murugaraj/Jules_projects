import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/lib/supabase/client";
import { useAuth } from "@/features/auth/AuthProvider";

export interface RecommendedPractice {
  category: string;
  reason: string;
  difficulty: string;
  duration: number;
}

export const useDashboardData = () => {
  const { user } = useAuth();

  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["dashboard-stats", user?.id],
    queryFn: async () => {
      if (!user) return null;
      try {
        const { error } = await supabase.from('profiles').select('*').eq('id', user.id).single();
        if (error) throw error;

        return {
          interviewsCompleted: 0,
          questionsAnswered: 0,
          averageScore: 0,
          practiceTimeMinutes: 0
        };
      } catch {
        return {
          interviewsCompleted: 0,
          questionsAnswered: 0,
          averageScore: 0,
          practiceTimeMinutes: 0
        };
      }
    },
    enabled: !!user,
  });

  const { data: performance, isLoading: performanceLoading } = useQuery({
    queryKey: ["dashboard-performance", user?.id],
    queryFn: async () => {
      return [];
    },
    enabled: !!user,
  });

  const { data: topicMastery, isLoading: masteryLoading } = useQuery({
    queryKey: ["dashboard-mastery", user?.id],
    queryFn: async () => {
      return [];
    },
    enabled: !!user,
  });

  const { data: recommended, isLoading: recommendedLoading } = useQuery({
    queryKey: ["dashboard-recommended", user?.id],
    queryFn: async (): Promise<RecommendedPractice | null> => {
      return null;
    },
    enabled: !!user,
  });

  const { data: recentInterviews, isLoading: recentInterviewsLoading } = useQuery({
    queryKey: ["dashboard-recent", user?.id],
    queryFn: async () => {
      return [];
    },
    enabled: !!user,
  });

  return {
    stats,
    performance,
    topicMastery,
    recommended,
    recentInterviews,
    isLoading: statsLoading || performanceLoading || masteryLoading || recommendedLoading || recentInterviewsLoading,
  };
};
