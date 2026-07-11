import React from "react";
import { Menu } from "lucide-react";

export const TopBar: React.FC = () => {
  return (
    <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-4">
      <div className="flex items-center">
        <button className="md:hidden p-2 text-gray-500 hover:bg-gray-100 rounded-md">
          <Menu className="h-6 w-6" />
        </button>
      </div>
      <div className="flex items-center space-x-4">
        {/* User profile / actions will go here */}
        <div className="w-8 h-8 bg-blue-600 rounded-full text-white flex items-center justify-center font-bold">
          U
        </div>
      </div>
    </header>
  );
};