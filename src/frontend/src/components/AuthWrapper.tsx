'use client';

import { useEffect, useState } from 'react';
import { useRouter, usePathname } from 'next/navigation';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Pages that don't require authentication
const PUBLIC_PATHS = ['/login'];

interface AuthWrapperProps {
  children: React.ReactNode;
}

export default function AuthWrapper({ children }: AuthWrapperProps) {
  const router = useRouter();
  const pathname = usePathname();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

  useEffect(() => {
    async function checkAuth() {
      // Skip auth check for public pages
      if (PUBLIC_PATHS.includes(pathname)) {
        setIsAuthenticated(true);
        return;
      }

      const token = localStorage.getItem('auth_token');

      if (!token) {
        setIsAuthenticated(false);
        router.push('/login');
        return;
      }

      try {
        const response = await fetch(`${API_URL}/api/auth/status`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const data = await response.json();
          if (data.authenticated) {
            setIsAuthenticated(true);
            return;
          }
        }

        // Token invalid or expired
        localStorage.removeItem('auth_token');
        setIsAuthenticated(false);
        router.push('/login');
      } catch {
        // API error - allow access but may need to re-auth later
        setIsAuthenticated(true);
      }
    }

    checkAuth();
  }, [pathname, router]);

  // Show loading while checking auth
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-zinc-50 dark:bg-zinc-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-zinc-500 dark:text-zinc-400">Loading...</p>
        </div>
      </div>
    );
  }

  // Not authenticated and not on login page
  if (!isAuthenticated && !PUBLIC_PATHS.includes(pathname)) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-zinc-50 dark:bg-zinc-900">
        <div className="text-zinc-500 dark:text-zinc-400">Redirecting to login...</div>
      </div>
    );
  }

  return <>{children}</>;
}

// Hook to get current auth token
export function useAuthToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('auth_token');
}

// Hook to logout
export function useLogout() {
  const router = useRouter();

  return async () => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      try {
        await fetch(`${API_URL}/api/auth/logout`, {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
      } catch {
        // Ignore logout errors
      }
    }
    localStorage.removeItem('auth_token');
    router.push('/login');
  };
}
