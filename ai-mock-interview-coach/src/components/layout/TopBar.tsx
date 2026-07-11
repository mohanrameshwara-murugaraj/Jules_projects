import React, { useState } from "react";
import { Menu, Bell, User as UserIcon, LogOut, Settings, Shield } from "lucide-react";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { useAuth } from "@/features/auth/AuthProvider";
import { cn } from "@/lib/utils";
import { NavLink } from "react-router-dom";

// Note: Duplicate links for mobile menu
const links = [
  { name: "Dashboard", href: "/dashboard" },
  { name: "Start Interview", href: "/interviews/new" },
  { name: "Practice", href: "/practice" },
  { name: "History", href: "/history" },
  { name: "Analytics", href: "/analytics" },
];

export const TopBar: React.FC = () => {
  const { user, signOut } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const initial = user?.email ? user.email.charAt(0).toUpperCase() : "U";

  return (
    <>
      <header className="h-16 bg-white border-b border-border flex items-center justify-between px-4 md:px-8 sticky top-0 z-30">
        <div className="flex items-center">
          <button
            className="md:hidden p-2 -ml-2 text-muted-foreground hover:bg-secondary rounded-md"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            <Menu className="h-5 w-5" />
          </button>
          {mobileMenuOpen && (
             <span className="ml-2 font-semibold text-foreground md:hidden">AI Coach</span>
          )}
        </div>

        <div className="flex items-center gap-4">
          <button className="text-muted-foreground hover:text-foreground relative p-1">
            <Bell className="h-5 w-5" />
            <span className="absolute top-0 right-0 w-2 h-2 bg-primary rounded-full"></span>
          </button>

          <DropdownMenu.Root>
            <DropdownMenu.Trigger asChild>
              <button className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center font-semibold focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2">
                {initial}
              </button>
            </DropdownMenu.Trigger>

            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="min-w-[200px] bg-white rounded-md p-1 shadow-md border border-border mt-2 mr-2 z-50 animate-in fade-in-80 zoom-in-95"
                sideOffset={5}
              >
                <DropdownMenu.Label className="px-2 py-2 text-sm font-semibold text-foreground border-b border-border mb-1">
                  My Account
                </DropdownMenu.Label>

                <DropdownMenu.Item className="px-2 py-2 text-sm text-foreground flex items-center gap-2 rounded-sm hover:bg-secondary cursor-pointer outline-none">
                  <UserIcon className="h-4 w-4 text-muted-foreground" />
                  Profile
                </DropdownMenu.Item>
                <DropdownMenu.Item className="px-2 py-2 text-sm text-foreground flex items-center gap-2 rounded-sm hover:bg-secondary cursor-pointer outline-none">
                  <Shield className="h-4 w-4 text-muted-foreground" />
                  Privacy
                </DropdownMenu.Item>
                <DropdownMenu.Item className="px-2 py-2 text-sm text-foreground flex items-center gap-2 rounded-sm hover:bg-secondary cursor-pointer outline-none">
                  <Settings className="h-4 w-4 text-muted-foreground" />
                  Settings
                </DropdownMenu.Item>

                <DropdownMenu.Separator className="h-px bg-border my-1" />

                <DropdownMenu.Item
                  onClick={signOut}
                  className="px-2 py-2 text-sm text-destructive flex items-center gap-2 rounded-sm hover:bg-destructive/10 cursor-pointer outline-none"
                >
                  <LogOut className="h-4 w-4" />
                  Sign out
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>
      </header>

      {/* Mobile Navigation Drawer */}
      {mobileMenuOpen && (
        <div className="fixed inset-0 z-40 bg-black/50 md:hidden" onClick={() => setMobileMenuOpen(false)}>
          <div
            className="fixed inset-y-0 left-0 w-64 bg-white shadow-lg flex flex-col animate-in slide-in-from-left"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="p-4 border-b border-border font-bold text-lg">AI Coach</div>
            <nav className="flex-1 p-4 space-y-2 overflow-y-auto">
              {links.map((link) => (
                <NavLink
                  key={link.href}
                  to={link.href}
                  onClick={() => setMobileMenuOpen(false)}
                  className={({ isActive }) =>
                    cn(
                      "block px-3 py-2 rounded-md text-sm font-medium transition-colors",
                      isActive
                        ? "bg-primary/10 text-primary"
                        : "text-muted-foreground hover:bg-secondary hover:text-foreground"
                    )
                  }
                >
                  {link.name}
                </NavLink>
              ))}
            </nav>
          </div>
        </div>
      )}
    </>
  );
};