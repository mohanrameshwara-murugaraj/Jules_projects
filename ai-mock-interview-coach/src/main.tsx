import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AuthProvider } from "./features/auth/AuthProvider";
import { ProtectedRoute } from "./components/layout/ProtectedRoute";
import { Login } from "./pages/Login";
import { Onboarding } from "./pages/Onboarding";
import Dashboard from "./pages/Dashboard";
import App from "./App.tsx";
import "./index.css";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/onboarding" element={<Onboarding />} />

            <Route element={<ProtectedRoute />}>
              <Route path="/" element={<App />}>
                <Route index element={<Navigate to="/dashboard" replace />} />
                <Route path="dashboard" element={<Dashboard />} />
              </Route>
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  </StrictMode>
);