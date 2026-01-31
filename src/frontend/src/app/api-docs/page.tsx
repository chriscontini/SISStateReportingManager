'use client';

import Link from 'next/link';
import AppShell from '@/components/AppShell';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface EndpointDoc {
  method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  path: string;
  description: string;
  auth?: boolean;
  params?: string;
}

const ENDPOINTS: Record<string, EndpointDoc[]> = {
  'Authentication': [
    { method: 'POST', path: '/api/auth/login', description: 'Login with password', params: '{ "password": "string" }' },
    { method: 'GET', path: '/api/auth/me', description: 'Get current user info', auth: true },
  ],
  'States': [
    { method: 'GET', path: '/api/states', description: 'List all 50 states' },
    { method: 'GET', path: '/api/states/{id}', description: 'Get state by ID' },
    { method: 'GET', path: '/api/states/{id}/detail', description: 'Get state with full details' },
    { method: 'GET', path: '/api/states/{id}/analysis', description: 'Get deep analysis for state' },
    { method: 'GET', path: '/api/states/compare', description: 'Compare multiple states', params: '?ids=1,2,3' },
  ],
  'Rankings': [
    { method: 'GET', path: '/api/rankings', description: 'Get ranked state list' },
    { method: 'GET', path: '/api/rankings/factors', description: 'Get ranking factors and weights' },
    { method: 'POST', path: '/api/rankings/calculate', description: 'Trigger score calculation', auth: true },
    { method: 'PATCH', path: '/api/rankings/factors/{id}', description: 'Update factor weight', auth: true },
  ],
  'Gap Analysis': [
    { method: 'GET', path: '/api/gap-analysis/{state_id}', description: 'Get gap analysis for state' },
    { method: 'GET', path: '/api/gap-analysis/{state_id}/gaps', description: 'List all gaps for state' },
    { method: 'POST', path: '/api/gap-analysis/{state_id}/analyze', description: 'Run gap analysis', auth: true },
  ],
  'Roadmaps': [
    { method: 'GET', path: '/api/roadmaps/', description: 'List all roadmaps' },
    { method: 'GET', path: '/api/roadmaps/{state_id}', description: 'Get roadmap for state' },
    { method: 'GET', path: '/api/roadmaps/{state_id}/phases', description: 'Get roadmap phases' },
    { method: 'POST', path: '/api/roadmaps/{state_id}/generate', description: 'Generate roadmap', auth: true },
    { method: 'GET', path: '/api/roadmaps/compare', description: 'Compare roadmaps', params: '?state_ids=1,2' },
  ],
  'Knowledge Base': [
    { method: 'GET', path: '/api/knowledge/articles', description: 'List articles', params: '?state_id=1&category=reporting' },
    { method: 'GET', path: '/api/knowledge/articles/{id}', description: 'Get article by ID' },
    { method: 'GET', path: '/api/knowledge/search', description: 'Search articles', params: '?q=PIMS' },
    { method: 'GET', path: '/api/knowledge/categories', description: 'List categories' },
    { method: 'POST', path: '/api/knowledge/articles', description: 'Create article', auth: true },
  ],
  'System': [
    { method: 'GET', path: '/health', description: 'Health check with DB status' },
    { method: 'GET', path: '/api/admin/stats', description: 'System statistics' },
    { method: 'GET', path: '/', description: 'API information' },
  ],
};

const METHOD_COLORS: Record<string, string> = {
  GET: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  POST: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
  PUT: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
  PATCH: 'bg-orange-100 text-orange-800 dark:bg-orange-900/30 dark:text-orange-400',
  DELETE: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
};

export default function ApiDocsPage() {
  return (
    <AppShell>
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
            API Documentation
          </h1>
          <p className="mt-2 text-zinc-600 dark:text-zinc-400">
            REST API reference for SISStateReportingManager
          </p>
        </div>

        {/* Quick Links */}
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">
            Interactive Documentation
          </h2>
          <p className="text-sm text-blue-800 dark:text-blue-200 mb-3">
            For interactive API exploration with request testing:
          </p>
          <div className="flex gap-3">
            <a
              href={`${API_URL}/docs`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-blue-600 text-white rounded-md text-sm font-medium hover:bg-blue-700"
            >
              Swagger UI
            </a>
            <a
              href={`${API_URL}/redoc`}
              target="_blank"
              rel="noopener noreferrer"
              className="px-4 py-2 bg-white dark:bg-zinc-800 border border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300 rounded-md text-sm font-medium hover:bg-blue-50 dark:hover:bg-zinc-700"
            >
              ReDoc
            </a>
          </div>
        </div>

        {/* Authentication */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
            Authentication
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400 mb-4">
            Protected endpoints require a Bearer token in the Authorization header:
          </p>
          <pre className="bg-zinc-100 dark:bg-zinc-900 p-4 rounded-lg text-sm overflow-x-auto">
            <code>{`Authorization: Bearer <token>

# Login to get token:
POST /api/auth/login
Content-Type: application/json

{
  "password": "your-password"
}

# Response:
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}`}</code>
          </pre>
        </div>

        {/* Base URL */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">
            Base URL
          </h2>
          <code className="text-lg text-blue-600 dark:text-blue-400">
            {API_URL}
          </code>
        </div>

        {/* Endpoints */}
        {Object.entries(ENDPOINTS).map(([category, endpoints]) => (
          <div key={category} className="bg-white dark:bg-zinc-800 rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-700">
              <h2 className="text-xl font-semibold text-zinc-900 dark:text-white">
                {category}
              </h2>
            </div>
            <div className="divide-y divide-zinc-200 dark:divide-zinc-700">
              {endpoints.map((endpoint, idx) => (
                <div key={idx} className="px-6 py-4">
                  <div className="flex items-start gap-3">
                    <span className={`px-2 py-1 text-xs font-bold rounded ${METHOD_COLORS[endpoint.method]}`}>
                      {endpoint.method}
                    </span>
                    <div className="flex-1">
                      <code className="text-sm font-mono text-zinc-800 dark:text-zinc-200">
                        {endpoint.path}
                      </code>
                      {endpoint.auth && (
                        <span className="ml-2 px-2 py-0.5 text-xs bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-400 rounded">
                          Auth Required
                        </span>
                      )}
                      <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
                        {endpoint.description}
                      </p>
                      {endpoint.params && (
                        <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-500 font-mono">
                          {endpoint.params}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

        {/* Response Format */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
            Response Format
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400 mb-4">
            All responses are JSON. Errors follow this format:
          </p>
          <pre className="bg-zinc-100 dark:bg-zinc-900 p-4 rounded-lg text-sm overflow-x-auto">
            <code>{`{
  "error": true,
  "code": "NOT_FOUND",
  "message": "State not found",
  "detail": "State with ID '999' not found",
  "timestamp": "2026-01-30T12:00:00.000Z",
  "path": "/api/states/999"
}`}</code>
          </pre>
        </div>

        {/* Rate Limiting */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
            Rate Limiting
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400">
            API requests are not currently rate limited. For production deployments,
            configure rate limiting at the reverse proxy level (nginx, traefik).
          </p>
        </div>
      </div>
    </AppShell>
  );
}
