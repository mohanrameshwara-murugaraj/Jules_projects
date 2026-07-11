import React from "react";

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-white border-r border-gray-200 hidden md:block">
      <div className="p-4 border-b border-gray-200">
        <h1 className="text-xl font-bold text-gray-900">AI Coach</h1>
      </div>
      <nav className="p-4 space-y-2">
        <a href="#" className="block p-2 text-gray-700 hover:bg-gray-100 rounded-md">Dashboard</a>
        <a href="#" className="block p-2 text-gray-700 hover:bg-gray-100 rounded-md">Interviews</a>
        <a href="#" className="block p-2 text-gray-700 hover:bg-gray-100 rounded-md">History</a>
      </nav>
    </aside>
  );
};