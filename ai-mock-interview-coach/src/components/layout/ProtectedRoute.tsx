import React from "react";
import { Navigate, Outlet, useLocation } from "react-router-dom";
import { useAuth } from "@/features/auth/AuthProvider";
import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/lib/supabase/client";
import { Loader2 } from "lucide-react";

export const ProtectedRoute: React.FC = () => {
  const { user, loading: authLoading } = useAuth();
  const location = useLocation();

  const { data: profile, isLoading: profileLoading } = useQuery({
    queryKey: ["profile", user?.id],
    queryFn: async () => {
      if (!user) return null;
      const { data, error } = await supabase.from('profiles').select('onboarding_completed').eq('id', user.id).single();
      if (error && error.code !== 'PGRST116') {
        // PGRST116 is multiple or no rows. It's fine if no profile exists yet just after register.
        throw error;
      }
      return data;
    },
    enabled: !!user,
  });

  if (authLoading || (user && profileLoading)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Handle onboarding redirects
  const isOnboardingRoute = location.pathname === "/onboarding";
  const hasCompletedOnboarding = profile?.onboarding_completed;

  if (!hasCompletedOnboarding && !isOnboardingRoute) {
    return <Navigate to="/onboarding" replace />;
  }

  if (hasCompletedOnboarding && isOnboardingRoute) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Outlet />;
};
