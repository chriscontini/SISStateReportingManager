'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface GapAnalysisSummary {
  id: number;
  state_id: number;
  state_name: string;
  state_abbreviation: string;
  baseline_state: string;
  total_gaps: number;
  critical_gaps: number;
  total_effort_hours: number;
  projected_months: number;
}

function SeverityBadge({ count, type }: { count: number; type: 'critical' | 'major' | 'minor' }) {
  const colors = {
    critical: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    major: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    minor: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded ${colors[type]}`}>
      {count} {type}
    </span>
  );
}

function formatHours(hours: number): string {
  if (hours >= 1000) {
    return `${(hours / 1000).toFixed(1)}k`;
  }
  return hours.toString();
}

export default function GapAnalysisPage() {
  const [analyses, setAnalyses] = useState<GapAnalysisSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [runningAnalysis, setRunningAnalysis] = useState<number | null>(null);

  const fetchAnalyses = async () => {
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${API_URL}/api/gap-analysis/`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setAnalyses(data);
      } else if (response.status === 404) {
        setAnalyses([]);
      } else {
        setError('Failed to load gap analyses');
      }
    } catch {
      setError('Failed to connect to API');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalyses();
  }, []);

  const runAnalysis = async (stateId: number) => {
    setRunningAnalysis(stateId);
    try {
      const token = localStorage.getItem('auth_token');
      const response = await fetch(`${API_URL}/api/gap-analysis/${stateId}/analyze`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      if (response.ok) {
        await fetchAnalyses();
      } else {
        alert('Failed to run analysis');
      }
    } catch {
      alert('Failed to run analysis');
    } finally {
      setRunningAnalysis(null);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const topStates = analyses.slice(0, 3);
  const lowestEffort = analyses[0];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-white">
            Gap Analysis
          </h1>
          <p className="text-zinc-600 dark:text-zinc-400">
            Requirements gap analysis comparing target states to NJ/LA baselines
          </p>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400">
          {error}
        </div>
      )}

      {analyses.length === 0 ? (
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-8 text-center">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">
            No Gap Analyses Found
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400 mb-6">
            Run gap analysis on states to see requirements gaps and effort estimates.
          </p>
          <div className="space-y-2">
            <p className="text-sm text-zinc-500 dark:text-zinc-400">
              Use the API to run analysis:
            </p>
            <code className="block bg-zinc-100 dark:bg-zinc-700 p-3 rounded text-sm">
              POST /api/gap-analysis/{'{state_id}'}/analyze
            </code>
          </div>
        </div>
      ) : (
        <>
          {/* Recommendation Banner */}
          {lowestEffort && (
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-green-800 dark:text-green-300">
                    Recommended: {lowestEffort.state_name} ({lowestEffort.state_abbreviation})
                  </h3>
                  <p className="text-sm text-green-700 dark:text-green-400 mt-1">
                    Lowest effort at {lowestEffort.total_effort_hours.toLocaleString()} hours
                    ({lowestEffort.projected_months} months projected)
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Top 3 Summary Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {topStates.map((analysis, index) => (
              <Link
                key={analysis.id}
                href={`/gap-analysis/${analysis.state_id}`}
                className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6 hover:shadow-lg transition-shadow"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="text-sm text-zinc-500 dark:text-zinc-400">
                      #{index + 1} Recommended
                    </span>
                    <h3 className="text-lg font-semibold text-zinc-900 dark:text-white">
                      {analysis.state_name}
                    </h3>
                  </div>
                  <span className="text-2xl font-bold text-zinc-900 dark:text-white">
                    {analysis.state_abbreviation}
                  </span>
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm text-zinc-600 dark:text-zinc-400">Total Gaps</span>
                    <span className="font-medium text-zinc-900 dark:text-white">
                      {analysis.total_gaps}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-zinc-600 dark:text-zinc-400">Critical Gaps</span>
                    <SeverityBadge count={analysis.critical_gaps} type="critical" />
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-zinc-600 dark:text-zinc-400">Effort</span>
                    <span className="font-medium text-zinc-900 dark:text-white">
                      {analysis.total_effort_hours.toLocaleString()} hrs
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-zinc-600 dark:text-zinc-400">Timeline</span>
                    <span className="font-medium text-zinc-900 dark:text-white">
                      {analysis.projected_months} months
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm text-zinc-600 dark:text-zinc-400">Baseline</span>
                    <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                      {analysis.baseline_state}
                    </span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* Full Table */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg shadow overflow-hidden">
            <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-700">
              <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
                All Gap Analyses
              </h2>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
                <thead className="bg-zinc-50 dark:bg-zinc-900/50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                      State
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                      Baseline
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                      Gaps
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                      Critical
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                      Effort (hrs)
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                      Timeline
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-zinc-800 divide-y divide-zinc-200 dark:divide-zinc-700">
                  {analyses.map((analysis) => (
                    <tr key={analysis.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-700/50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <Link
                          href={`/gap-analysis/${analysis.state_id}`}
                          className="font-medium text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                        >
                          {analysis.state_name} ({analysis.state_abbreviation})
                        </Link>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-600 dark:text-zinc-400">
                        {analysis.baseline_state}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-900 dark:text-white">
                        {analysis.total_gaps}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <SeverityBadge count={analysis.critical_gaps} type="critical" />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-900 dark:text-white">
                        {analysis.total_effort_hours.toLocaleString()}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-900 dark:text-white">
                        {analysis.projected_months} mo
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <Link
                          href={`/gap-analysis/${analysis.state_id}`}
                          className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
                        >
                          View Details
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
