'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues with Recharts
const TopStatesBarChart = dynamic(() => import('@/components/TopStatesBarChart'), {
  ssr: false,
  loading: () => <div className="h-64 flex items-center justify-center text-zinc-500">Loading chart...</div>,
});

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface State {
  id: number;
  name: string;
  abbreviation: string;
}

interface RankedState {
  state: State;
  total_score: number;
  rank: number;
}

interface DashboardStats {
  totalStates: number;
  statesAnalyzed: number;
  topStates: RankedState[];
  avgScore: number;
}

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchDashboardData() {
      try {
        // Fetch rankings data
        const rankingsRes = await fetch(`${API_URL}/api/rankings`);
        if (!rankingsRes.ok) throw new Error('Failed to fetch rankings');
        const rankingsData = await rankingsRes.json();

        // Fetch states count
        const statesRes = await fetch(`${API_URL}/api/states`);
        if (!statesRes.ok) throw new Error('Failed to fetch states');
        const statesData = await statesRes.json();

        // Calculate stats
        const rankings = rankingsData.rankings || [];
        const statesWithScores = rankings.filter((r: RankedState) => r.total_score > 0);
        const avgScore = statesWithScores.length > 0
          ? statesWithScores.reduce((sum: number, r: RankedState) => sum + r.total_score, 0) / statesWithScores.length
          : 0;

        setStats({
          totalStates: statesData.length || 50,
          statesAnalyzed: statesWithScores.length,
          topStates: rankings.slice(0, 10),
          avgScore: Math.round(avgScore * 10) / 10,
        });
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    }

    fetchDashboardData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-gray-500">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
          Error: {error}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-2xl font-bold text-gray-900">
              State Expansion Dashboard
            </h1>
            <nav className="flex space-x-4">
              <Link href="/states" className="text-gray-600 hover:text-gray-900">
                States
              </Link>
              <Link href="/rankings" className="text-gray-600 hover:text-gray-900">
                Rankings
              </Link>
              <Link href="/compare" className="text-gray-600 hover:text-gray-900">
                Compare
              </Link>
            </nav>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* Total States Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">
              Total States
            </div>
            <div className="mt-2 text-3xl font-bold text-gray-900">
              {stats?.totalStates || 50}
            </div>
            <div className="mt-1 text-sm text-gray-500">
              All US states tracked
            </div>
          </div>

          {/* States Analyzed Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">
              States Analyzed
            </div>
            <div className="mt-2 text-3xl font-bold text-blue-600">
              {stats?.statesAnalyzed || 0}
            </div>
            <div className="mt-1 text-sm text-gray-500">
              With calculated scores
            </div>
          </div>

          {/* Average Score Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">
              Average Score
            </div>
            <div className="mt-2 text-3xl font-bold text-green-600">
              {stats?.avgScore || 0}
            </div>
            <div className="mt-1 text-sm text-gray-500">
              Across all analyzed states
            </div>
          </div>

          {/* Top Recommendation Card */}
          <div className="bg-white rounded-lg shadow p-6">
            <div className="text-sm font-medium text-gray-500 uppercase tracking-wide">
              Top Recommendation
            </div>
            <div className="mt-2 text-3xl font-bold text-purple-600">
              {stats?.topStates?.[0]?.state?.abbreviation || 'N/A'}
            </div>
            <div className="mt-1 text-sm text-gray-500">
              Score: {stats?.topStates?.[0]?.total_score?.toFixed(1) || 'N/A'}
            </div>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Top States Widget - Takes 2 columns */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">
                Top 10 Recommended States
              </h2>
              <p className="text-sm text-gray-500">
                Based on development effort and market opportunity
              </p>
            </div>
            <div className="p-6">
              {stats?.topStates && stats.topStates.length > 0 ? (
                <>
                  {/* Bar Chart */}
                  <div className="mb-6">
                    <TopStatesBarChart
                      states={stats.topStates.map(item => ({
                        name: item.state.name,
                        abbreviation: item.state.abbreviation,
                        total_score: item.total_score,
                      }))}
                      height={300}
                    />
                  </div>

                  {/* List */}
                  <div className="space-y-3">
                  {stats.topStates.map((item, index) => (
                    <Link
                      key={item.state.id}
                      href={`/states/${item.state.id}`}
                      className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                          index < 3 ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                        }`}>
                          {index + 1}
                        </span>
                        <div>
                          <div className="font-medium text-gray-900">
                            {item.state.name}
                          </div>
                          <div className="text-sm text-gray-500">
                            {item.state.abbreviation}
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="font-bold text-gray-900">
                          {item.total_score.toFixed(1)}
                        </div>
                        <div className="text-xs text-gray-500">score</div>
                      </div>
                    </Link>
                  ))}
                  </div>
                </>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p>No rankings calculated yet.</p>
                  <Link href="/rankings" className="text-blue-600 hover:underline mt-2 inline-block">
                    Go to Rankings to calculate scores
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions Widget */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-semibold text-gray-900">
                Quick Actions
              </h2>
            </div>
            <div className="p-6 space-y-4">
              <Link
                href="/rankings"
                className="block w-full text-center bg-blue-600 text-white rounded-lg px-4 py-3 font-medium hover:bg-blue-700 transition-colors"
              >
                View Full Rankings
              </Link>
              <Link
                href="/compare"
                className="block w-full text-center bg-white border border-gray-300 text-gray-700 rounded-lg px-4 py-3 font-medium hover:bg-gray-50 transition-colors"
              >
                Compare States
              </Link>
              <Link
                href="/rankings/methodology"
                className="block w-full text-center bg-white border border-gray-300 text-gray-700 rounded-lg px-4 py-3 font-medium hover:bg-gray-50 transition-colors"
              >
                View Methodology
              </Link>
            </div>

            {/* Top 3 Recommendations */}
            <div className="px-6 py-4 border-t border-gray-200">
              <h3 className="text-sm font-semibold text-gray-900 uppercase tracking-wide mb-4">
                Priority Targets
              </h3>
              {stats?.topStates?.slice(0, 3).map((item, index) => (
                <div key={item.state.id} className="flex items-center justify-between py-2">
                  <span className="flex items-center space-x-2">
                    <span className={`w-2 h-2 rounded-full ${
                      index === 0 ? 'bg-green-500' : index === 1 ? 'bg-yellow-500' : 'bg-orange-500'
                    }`} />
                    <span className="text-sm font-medium">{item.state.name}</span>
                  </span>
                  <span className="text-sm text-gray-500">{item.total_score.toFixed(1)}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Analysis Status */}
        <div className="mt-8 bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">
              Analysis Progress
            </h2>
          </div>
          <div className="p-6">
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">States with scores</span>
                <span className="font-medium">{stats?.statesAnalyzed || 0} / {stats?.totalStates || 50}</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                  style={{ width: `${((stats?.statesAnalyzed || 0) / (stats?.totalStates || 50)) * 100}%` }}
                />
              </div>
            </div>
            <p className="text-sm text-gray-500">
              {stats?.statesAnalyzed === 0
                ? 'No states analyzed yet. Go to Rankings and click "Calculate Scores" to begin analysis.'
                : stats?.statesAnalyzed === stats?.totalStates
                  ? 'All states have been analyzed!'
                  : `${(stats?.totalStates || 50) - (stats?.statesAnalyzed || 0)} states remaining to be analyzed.`
              }
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}
