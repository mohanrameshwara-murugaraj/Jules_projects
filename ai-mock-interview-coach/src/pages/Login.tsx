import React from "react";

export const Login: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-sm border border-gray-100">
        <h1 className="text-2xl font-bold text-center mb-6">Sign in to AI Coach</h1>
        <p className="text-center text-gray-500 mb-8">Authentication is mocked in this view.</p>
        <button className="w-full bg-primary text-white py-2 rounded-md hover:bg-primary/90 transition-colors">
          Sign In
        </button>
      </div>
    </div>
  );
};