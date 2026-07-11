import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/features/auth/AuthProvider";

export const ProtectedRoute: React.FC = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  // Redirect unauthenticated users to login
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  // Onboarding completion checks will be added here later once we fetch profile
  // if (!profile?.onboarding_completed) {
  //   return <Navigate to="/onboarding" replace />;
  // }

  return <Outlet />;
};