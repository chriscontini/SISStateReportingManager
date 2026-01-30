'use client';

import { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import Link from 'next/link';
import AuthWrapper, { useLogout } from './AuthWrapper';

// Pages where we should hide the navigation
const HIDE_NAV_PATHS = ['/login'];

interface AppShellProps {
  children: React.ReactNode;
}

// Dark mode icons
function SunIcon() {
  return (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
    </svg>
  );
}

function MoonIcon() {
  return (
    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
    </svg>
  );
}

export default function AppShell({ children }: AppShellProps) {
  const pathname = usePathname();
  const logout = useLogout();
  const hideNav = HIDE_NAV_PATHS.includes(pathname);
  const [darkMode, setDarkMode] = useState(false);
  const [mounted, setMounted] = useState(false);

  // Load dark mode preference from localStorage on mount
  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem('darkMode');
    if (stored !== null) {
      setDarkMode(stored === 'true');
    } else {
      // Check system preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      setDarkMode(prefersDark);
    }
  }, []);

  // Apply dark mode class to document
  useEffect(() => {
    if (mounted) {
      if (darkMode) {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      localStorage.setItem('darkMode', String(darkMode));
    }
  }, [darkMode, mounted]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <AuthWrapper>
      {!hideNav && (
        <nav className="border-b border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex items-center">
                <Link
                  href="/dashboard"
                  className="text-xl font-bold text-zinc-900 dark:text-white"
                >
                  SIS State Manager
                </Link>
              </div>
              <div className="flex items-center space-x-4">
                <Link
                  href="/dashboard"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname === '/dashboard'
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  Dashboard
                </Link>
                <Link
                  href="/states"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname.startsWith('/states')
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  States
                </Link>
                <Link
                  href="/rankings"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname.startsWith('/rankings')
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  Rankings
                </Link>
                <Link
                  href="/compare"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname === '/compare'
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  Compare
                </Link>
                <Link
                  href="/gap-analysis"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname.startsWith('/gap-analysis')
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  Gap Analysis
                </Link>
                <Link
                  href="/roadmap"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname.startsWith('/roadmap')
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  Roadmap
                </Link>
                <Link
                  href="/knowledge"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname.startsWith('/knowledge')
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  Knowledge
                </Link>
                <Link
                  href="/chat"
                  className={`px-3 py-2 rounded-md text-sm font-medium ${
                    pathname.startsWith('/chat')
                      ? 'bg-zinc-100 text-zinc-900 dark:bg-zinc-800 dark:text-white'
                      : 'text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800'
                  }`}
                >
                  Chat
                </Link>
                <button
                  onClick={toggleDarkMode}
                  className="p-2 rounded-md text-zinc-700 hover:text-zinc-900 hover:bg-zinc-100 dark:text-zinc-300 dark:hover:text-white dark:hover:bg-zinc-800"
                  aria-label={darkMode ? 'Switch to light mode' : 'Switch to dark mode'}
                >
                  {mounted && (darkMode ? <SunIcon /> : <MoonIcon />)}
                </button>
                <button
                  onClick={logout}
                  className="px-3 py-2 rounded-md text-sm font-medium text-red-600 hover:text-red-700 hover:bg-red-50 dark:text-red-400 dark:hover:text-red-300 dark:hover:bg-red-900/20"
                >
                  Logout
                </button>
              </div>
            </div>
          </div>
        </nav>
      )}
      <main className={hideNav ? '' : 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8'}>
        {children}
      </main>
    </AuthWrapper>
  );
}
