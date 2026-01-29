'use client';

import { usePathname } from 'next/navigation';
import Link from 'next/link';
import AuthWrapper, { useLogout } from './AuthWrapper';

// Pages where we should hide the navigation
const HIDE_NAV_PATHS = ['/login'];

interface AppShellProps {
  children: React.ReactNode;
}

export default function AppShell({ children }: AppShellProps) {
  const pathname = usePathname();
  const logout = useLogout();
  const hideNav = HIDE_NAV_PATHS.includes(pathname);

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
