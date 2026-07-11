import React from "react";
import {
  LayoutDashboard,
  Mic,
  Dumbbell,
  History,
  BarChart,
  User,
  Shield
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { cn } from "@/lib/utils";

const links = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Start Interview", href: "/interviews/new", icon: Mic },
  { name: "Practice", href: "/practice", icon: Dumbbell },
  { name: "History", href: "/history", icon: History },
  { name: "Analytics", href: "/analytics", icon: BarChart },
];

const bottomLinks = [
  { name: "Profile", href: "/settings/profile", icon: User },
  { name: "Privacy", href: "/settings/privacy", icon: Shield },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-white border-r border-border hidden md:flex md:flex-col h-screen fixed sticky top-0">
      <div className="p-6 flex items-center gap-2">
        <div className="w-8 h-8 bg-primary rounded-md flex items-center justify-center text-white font-bold">
          <Mic size={18} />
        </div>
        <h1 className="text-lg font-semibold text-foreground tracking-tight">AI Coach</h1>
      </div>
      <nav className="flex-1 px-4 space-y-1 overflow-y-auto">
        {links.map((link) => (
          <NavLink
            key={link.href}
            to={link.href}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-secondary hover:text-foreground"
              )
            }
          >
            <link.icon size={18} />
            {link.name}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-border space-y-1">
        {bottomLinks.map((link) => (
          <NavLink
            key={link.href}
            to={link.href}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium transition-colors",
                isActive
                  ? "bg-primary/10 text-primary"
                  : "text-muted-foreground hover:bg-secondary hover:text-foreground"
              )
            }
          >
            <link.icon size={18} />
            {link.name}
          </NavLink>
        ))}
      </div>
    </aside>
  );
};