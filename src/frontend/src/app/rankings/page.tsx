"use client";

import { useEffect, useState } from "react";

interface RankingFactor {
  id: number;
  name: string;
  weight: number;
  description: string | null;
}

interface StateRanking {
  id: number;
  name: string;
  abbreviation: string;
  total_score: number;
  rank: number;
}

interface RankingsResponse {
  rankings: StateRanking[];
  factors: RankingFactor[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function RankingsPage() {
  const [data, setData] = useState<RankingsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchRankings() {
      try {
        const response = await fetch(`${API_URL}/api/rankings`);
        if (!response.ok) {
          throw new Error("Failed to fetch rankings");
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    fetchRankings();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-zinc-500 dark:text-zinc-400">
          Loading rankings...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
        <p className="text-red-800 dark:text-red-200">Error: {error}</p>
        <p className="text-red-600 dark:text-red-400 text-sm mt-2">
          Make sure the backend API is running at {API_URL}
        </p>
      </div>
    );
  }

  const hasScores = data?.rankings.some((r) => r.total_score > 0);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
          State Rankings
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400 mt-2">
          States ranked by expansion viability based on weighted scoring factors
        </p>
      </div>

      {!hasScores && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <p className="text-yellow-800 dark:text-yellow-200 font-medium">
            No scores calculated yet
          </p>
          <p className="text-yellow-700 dark:text-yellow-300 text-sm mt-1">
            State rankings will be populated after AI research and scoring is
            completed in Sprint 2.
          </p>
        </div>
      )}

      {data?.factors && data.factors.length > 0 && (
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-3">
            Ranking Factors
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {data.factors.map((factor) => (
              <div
                key={factor.id}
                className="bg-zinc-50 dark:bg-zinc-900 rounded-md p-3"
              >
                <div className="flex justify-between items-start">
                  <span className="text-sm font-medium text-zinc-900 dark:text-white">
                    {factor.name}
                  </span>
                  <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                    Weight: {factor.weight}
                  </span>
                </div>
                {factor.description && (
                  <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
                    {factor.description}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 overflow-hidden">
        <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
          <thead className="bg-zinc-50 dark:bg-zinc-900">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                Rank
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                State
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                Abbreviation
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                Total Score
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
            {data?.rankings.map((state) => (
              <tr
                key={state.id}
                className="hover:bg-zinc-50 dark:hover:bg-zinc-700/50"
              >
                <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-500 dark:text-zinc-400">
                  {state.rank}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-zinc-900 dark:text-white">
                  {state.name}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-500 dark:text-zinc-400">
                  {state.abbreviation}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                  {state.total_score > 0 ? (
                    <span className="font-medium text-green-600 dark:text-green-400">
                      {state.total_score.toFixed(2)}
                    </span>
                  ) : (
                    <span className="text-zinc-400 dark:text-zinc-500">-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="text-sm text-zinc-500 dark:text-zinc-400">
        Showing {data?.rankings.length || 0} states
      </div>
    </div>
  );
}
