import React from "react";

export const Onboarding: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 p-4">
      <div className="max-w-2xl w-full bg-white p-8 rounded-lg shadow-sm border border-gray-100">
        <h1 className="text-2xl font-bold mb-6">Welcome! Let's get you set up.</h1>
        <p className="text-gray-500 mb-8">Tell us about your experience to personalize your coaching.</p>
        <button className="bg-primary text-white py-2 px-4 rounded-md hover:bg-primary/90 transition-colors">
          Complete Onboarding
        </button>
      </div>
    </div>
  );
};