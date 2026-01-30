'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Gap {
  id: number;
  gap_code: string;
  name: string;
  description: string | null;
  category: string;
  severity: string;
  effort_hours: number;
  complexity: string;
  baseline_feature: string | null;
  status: string;
}

interface GapAnalysis {
  id: number;
  state_id: number;
  baseline_state: string;
  analysis_status: string;
  total_gaps: number;
  critical_gaps: number;
  major_gaps: number;
  minor_gaps: number;
  total_effort_hours: number;
  development_hours: number;
  testing_hours: number;
  certification_hours: number;
  projected_months: number;
  executive_summary: string | null;
  recommendation: string | null;
  risk_assessment: string | null;
  gaps: Gap[];
}

interface State {
  id: number;
  name: string;
  abbreviation: string;
}

function SeverityBadge({ severity }: { severity: string }) {
  const colors: Record<string, string> = {
    critical: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-400',
    major: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    minor: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded capitalize ${colors[severity] || 'bg-zinc-100 text-zinc-800'}`}>
      {severity}
    </span>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    identified: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    in_progress: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
    completed: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    deferred: 'bg-zinc-100 text-zinc-800 dark:bg-zinc-700 dark:text-zinc-400',
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded capitalize ${colors[status] || 'bg-zinc-100 text-zinc-800'}`}>
      {status.replace('_', ' ')}
    </span>
  );
}

function ComplexityBadge({ complexity }: { complexity: string }) {
  const colors: Record<string, string> = {
    low: 'text-green-600 dark:text-green-400',
    medium: 'text-yellow-600 dark:text-yellow-400',
    high: 'text-orange-600 dark:text-orange-400',
    very_high: 'text-red-600 dark:text-red-400',
  };

  return (
    <span className={`text-sm capitalize ${colors[complexity] || 'text-zinc-600'}`}>
      {complexity.replace('_', ' ')}
    </span>
  );
}

export default function GapAnalysisDetailPage() {
  const params = useParams();
  const stateId = params.id as string;

  const [analysis, setAnalysis] = useState<GapAnalysis | null>(null);
  const [state, setState] = useState<State | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categoryFilter, setCategoryFilter] = useState<string>('all');
  const [severityFilter, setSeverityFilter] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'severity' | 'effort' | 'category'>('severity');

  useEffect(() => {
    async function fetchData() {
      try {
        const token = localStorage.getItem('auth_token');

        // Fetch state info
        const stateRes = await fetch(`${API_URL}/api/states/${stateId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (stateRes.ok) {
          setState(await stateRes.json());
        }

        // Fetch gap analysis
        const analysisRes = await fetch(`${API_URL}/api/gap-analysis/${stateId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (analysisRes.ok) {
          setAnalysis(await analysisRes.json());
        } else if (analysisRes.status === 404) {
          setError('No gap analysis found for this state. Run analysis first.');
        } else {
          setError('Failed to load gap analysis');
        }
      } catch {
        setError('Failed to connect to API');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [stateId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error || !analysis) {
    return (
      <div className="space-y-4">
        <Link
          href="/gap-analysis"
          className="text-blue-600 hover:text-blue-800 dark:text-blue-400"
        >
          Back to Gap Analysis
        </Link>
        <div className="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400">
          {error || 'No data found'}
        </div>
      </div>
    );
  }

  // Get unique categories
  const categories = [...new Set(analysis.gaps.map(g => g.category))].sort();

  // Filter and sort gaps
  let filteredGaps = analysis.gaps;

  if (categoryFilter !== 'all') {
    filteredGaps = filteredGaps.filter(g => g.category === categoryFilter);
  }

  if (severityFilter !== 'all') {
    filteredGaps = filteredGaps.filter(g => g.severity === severityFilter);
  }

  const severityOrder = { critical: 0, major: 1, minor: 2 };
  filteredGaps = [...filteredGaps].sort((a, b) => {
    if (sortBy === 'severity') {
      return (severityOrder[a.severity as keyof typeof severityOrder] || 3) -
             (severityOrder[b.severity as keyof typeof severityOrder] || 3);
    } else if (sortBy === 'effort') {
      return b.effort_hours - a.effort_hours;
    } else {
      return a.category.localeCompare(b.category);
    }
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-start">
        <div>
          <Link
            href="/gap-analysis"
            className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400 mb-2 inline-block"
          >
            Back to Gap Analysis
          </Link>
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-white">
            {state?.name || `State ${stateId}`} Gap Analysis
          </h1>
          <p className="text-zinc-600 dark:text-zinc-400">
            Compared against {analysis.baseline_state} baseline
          </p>
        </div>
        <span className={`px-3 py-1 text-sm font-medium rounded-full ${
          analysis.analysis_status === 'completed'
            ? 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400'
            : 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400'
        }`}>
          {analysis.analysis_status}
        </span>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Gaps</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {analysis.total_gaps}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Critical Gaps</div>
          <div className="text-2xl font-bold text-red-600 dark:text-red-400">
            {analysis.critical_gaps}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Effort</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {analysis.total_effort_hours.toLocaleString()} hrs
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Timeline</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {analysis.projected_months} months
          </div>
        </div>
      </div>

      {/* Effort Breakdown */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
          Effort Breakdown
        </h2>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Development</div>
            <div className="text-xl font-bold text-zinc-900 dark:text-white">
              {analysis.development_hours.toLocaleString()} hrs
            </div>
            <div className="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2 mt-2">
              <div
                className="bg-blue-600 h-2 rounded-full"
                style={{ width: `${(analysis.development_hours / analysis.total_effort_hours) * 100}%` }}
              ></div>
            </div>
          </div>
          <div>
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Testing</div>
            <div className="text-xl font-bold text-zinc-900 dark:text-white">
              {analysis.testing_hours.toLocaleString()} hrs
            </div>
            <div className="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2 mt-2">
              <div
                className="bg-green-600 h-2 rounded-full"
                style={{ width: `${(analysis.testing_hours / analysis.total_effort_hours) * 100}%` }}
              ></div>
            </div>
          </div>
          <div>
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Certification</div>
            <div className="text-xl font-bold text-zinc-900 dark:text-white">
              {analysis.certification_hours.toLocaleString()} hrs
            </div>
            <div className="w-full bg-zinc-200 dark:bg-zinc-700 rounded-full h-2 mt-2">
              <div
                className="bg-purple-600 h-2 rounded-full"
                style={{ width: `${(analysis.certification_hours / analysis.total_effort_hours) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      {analysis.executive_summary && (
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
            Executive Summary
          </h2>
          <pre className="text-sm text-zinc-700 dark:text-zinc-300 whitespace-pre-wrap font-sans">
            {analysis.executive_summary}
          </pre>
        </div>
      )}

      {/* Recommendation */}
      {analysis.recommendation && (
        <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-4">
            Recommendation
          </h2>
          <pre className="text-sm text-blue-800 dark:text-blue-200 whitespace-pre-wrap font-sans">
            {analysis.recommendation}
          </pre>
        </div>
      )}

      {/* Risk Assessment */}
      {analysis.risk_assessment && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-6">
          <h2 className="text-lg font-semibold text-yellow-900 dark:text-yellow-100 mb-4">
            Risk Assessment
          </h2>
          <pre className="text-sm text-yellow-800 dark:text-yellow-200 whitespace-pre-wrap font-sans">
            {analysis.risk_assessment}
          </pre>
        </div>
      )}

      {/* Gaps List */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow">
        <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-700">
          <div className="flex flex-wrap justify-between items-center gap-4">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
              Identified Gaps ({filteredGaps.length})
            </h2>
            <div className="flex gap-2">
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="px-3 py-1 text-sm border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
              >
                <option value="all">All Categories</option>
                {categories.map(cat => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
              <select
                value={severityFilter}
                onChange={(e) => setSeverityFilter(e.target.value)}
                className="px-3 py-1 text-sm border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
              >
                <option value="all">All Severities</option>
                <option value="critical">Critical</option>
                <option value="major">Major</option>
                <option value="minor">Minor</option>
              </select>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as 'severity' | 'effort' | 'category')}
                className="px-3 py-1 text-sm border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
              >
                <option value="severity">Sort by Severity</option>
                <option value="effort">Sort by Effort</option>
                <option value="category">Sort by Category</option>
              </select>
            </div>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
            <thead className="bg-zinc-50 dark:bg-zinc-900/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Gap
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Category
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Severity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Complexity
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Effort
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-zinc-800 divide-y divide-zinc-200 dark:divide-zinc-700">
              {filteredGaps.map((gap) => (
                <tr key={gap.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-700/50">
                  <td className="px-6 py-4">
                    <div className="text-sm font-medium text-zinc-900 dark:text-white">
                      {gap.name}
                    </div>
                    <div className="text-xs text-zinc-500 dark:text-zinc-400">
                      {gap.gap_code}
                    </div>
                    {gap.description && (
                      <div className="text-xs text-zinc-500 dark:text-zinc-400 mt-1 max-w-md">
                        {gap.description}
                      </div>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-600 dark:text-zinc-400 capitalize">
                    {gap.category.replace('_', ' ')}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <SeverityBadge severity={gap.severity} />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <ComplexityBadge complexity={gap.complexity} />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-900 dark:text-white">
                    {gap.effort_hours} hrs
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <StatusBadge status={gap.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
