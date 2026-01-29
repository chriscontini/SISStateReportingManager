"use client";

import { useEffect, useState, useMemo } from "react";
import Link from "next/link";

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

type SortField = "rank" | "name" | "abbreviation" | "total_score";
type SortDirection = "asc" | "desc";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function RankingsPage() {
  const [data, setData] = useState<RankingsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [calculating, setCalculating] = useState(false);
  const [showWeightConfig, setShowWeightConfig] = useState(false);
  const [editedWeights, setEditedWeights] = useState<Record<number, number>>({});
  const [savingWeights, setSavingWeights] = useState(false);

  // Sorting state
  const [sortField, setSortField] = useState<SortField>("rank");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  // Filtering state
  const [minScore, setMinScore] = useState<number>(0);
  const [searchQuery, setSearchQuery] = useState("");

  const fetchRankings = async () => {
    try {
      const response = await fetch(`${API_URL}/api/rankings`);
      if (!response.ok) {
        throw new Error("Failed to fetch rankings");
      }
      const result = await response.json();
      setData(result);
      // Initialize edited weights
      const weights: Record<number, number> = {};
      result.factors.forEach((f: RankingFactor) => {
        weights[f.id] = f.weight;
      });
      setEditedWeights(weights);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRankings();
  }, []);

  const handleCalculateScores = async (useAi: boolean) => {
    setCalculating(true);
    try {
      const response = await fetch(`${API_URL}/api/rankings/calculate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ use_ai: useAi }),
      });
      if (!response.ok) {
        throw new Error("Failed to calculate scores");
      }
      // Refresh rankings after calculation
      await fetchRankings();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Calculation failed");
    } finally {
      setCalculating(false);
    }
  };

  const handleSaveWeights = async () => {
    setSavingWeights(true);
    try {
      for (const factor of data?.factors || []) {
        if (editedWeights[factor.id] !== factor.weight) {
          await fetch(`${API_URL}/api/rankings/factors/${factor.id}`, {
            method: "PATCH",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ weight: editedWeights[factor.id] }),
          });
        }
      }
      await fetchRankings();
      setShowWeightConfig(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save weights");
    } finally {
      setSavingWeights(false);
    }
  };

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection(field === "total_score" ? "desc" : "asc");
    }
  };

  const sortedAndFilteredRankings = useMemo(() => {
    if (!data?.rankings) return [];

    return data.rankings
      .filter((state) => {
        const matchesScore = state.total_score >= minScore;
        const matchesSearch =
          searchQuery === "" ||
          state.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
          state.abbreviation.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesScore && matchesSearch;
      })
      .sort((a, b) => {
        let comparison = 0;
        switch (sortField) {
          case "rank":
            comparison = a.rank - b.rank;
            break;
          case "name":
            comparison = a.name.localeCompare(b.name);
            break;
          case "abbreviation":
            comparison = a.abbreviation.localeCompare(b.abbreviation);
            break;
          case "total_score":
            comparison = a.total_score - b.total_score;
            break;
        }
        return sortDirection === "asc" ? comparison : -comparison;
      });
  }, [data?.rankings, sortField, sortDirection, minScore, searchQuery]);

  const SortHeader = ({ field, children }: { field: SortField; children: React.ReactNode }) => (
    <th
      className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider cursor-pointer hover:bg-zinc-100 dark:hover:bg-zinc-800"
      onClick={() => handleSort(field)}
    >
      <div className="flex items-center gap-1">
        {children}
        {sortField === field && (
          <span>{sortDirection === "asc" ? "↑" : "↓"}</span>
        )}
      </div>
    </th>
  );

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-zinc-500 dark:text-zinc-400">Loading rankings...</div>
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
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">State Rankings</h1>
          <p className="text-zinc-600 dark:text-zinc-400 mt-2">
            States ranked by expansion viability based on weighted scoring factors
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => handleCalculateScores(false)}
            disabled={calculating}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
          >
            {calculating ? "Calculating..." : "Calculate Scores"}
          </button>
          <Link
            href="/rankings/methodology"
            className="px-4 py-2 bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-white rounded-md hover:bg-zinc-300 dark:hover:bg-zinc-600 text-sm"
          >
            Methodology
          </Link>
        </div>
      </div>

      {!hasScores && (
        <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg p-4">
          <p className="text-yellow-800 dark:text-yellow-200 font-medium">No scores calculated yet</p>
          <p className="text-yellow-700 dark:text-yellow-300 text-sm mt-1">
            Click &quot;Calculate Scores&quot; to generate rankings based on the configured factors.
          </p>
        </div>
      )}

      {/* Ranking Factors with Weight Configuration */}
      {data?.factors && data.factors.length > 0 && (
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="flex justify-between items-center mb-3">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">Ranking Factors</h2>
            <button
              onClick={() => setShowWeightConfig(!showWeightConfig)}
              className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400"
            >
              {showWeightConfig ? "Hide Configuration" : "Configure Weights"}
            </button>
          </div>

          {showWeightConfig ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {data.factors.map((factor) => (
                  <div key={factor.id} className="bg-zinc-50 dark:bg-zinc-900 rounded-md p-3">
                    <label className="block text-sm font-medium text-zinc-900 dark:text-white mb-1">
                      {factor.name}
                    </label>
                    <input
                      type="number"
                      min="0"
                      max="10"
                      step="0.5"
                      value={editedWeights[factor.id] || 0}
                      onChange={(e) =>
                        setEditedWeights({
                          ...editedWeights,
                          [factor.id]: parseFloat(e.target.value) || 0,
                        })
                      }
                      className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white"
                    />
                    {factor.description && (
                      <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{factor.description}</p>
                    )}
                  </div>
                ))}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleSaveWeights}
                  disabled={savingWeights}
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 text-sm"
                >
                  {savingWeights ? "Saving..." : "Save Weights"}
                </button>
                <button
                  onClick={() => setShowWeightConfig(false)}
                  className="px-4 py-2 bg-zinc-200 dark:bg-zinc-700 text-zinc-900 dark:text-white rounded-md hover:bg-zinc-300 dark:hover:bg-zinc-600 text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {data.factors.map((factor) => (
                <div key={factor.id} className="bg-zinc-50 dark:bg-zinc-900 rounded-md p-3">
                  <div className="flex justify-between items-start">
                    <span className="text-sm font-medium text-zinc-900 dark:text-white">{factor.name}</span>
                    <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded">
                      Weight: {factor.weight}
                    </span>
                  </div>
                  {factor.description && (
                    <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">{factor.description}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Filters */}
      <div className="flex flex-wrap gap-4 items-center">
        <div>
          <label className="block text-xs text-zinc-500 dark:text-zinc-400 mb-1">Search</label>
          <input
            type="text"
            placeholder="Search states..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm w-48"
          />
        </div>
        <div>
          <label className="block text-xs text-zinc-500 dark:text-zinc-400 mb-1">Min Score</label>
          <input
            type="number"
            min="0"
            value={minScore}
            onChange={(e) => setMinScore(parseFloat(e.target.value) || 0)}
            className="px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white text-sm w-24"
          />
        </div>
      </div>

      {/* Rankings Table */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 overflow-hidden">
        <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
          <thead className="bg-zinc-50 dark:bg-zinc-900">
            <tr>
              <SortHeader field="rank">Rank</SortHeader>
              <SortHeader field="name">State</SortHeader>
              <SortHeader field="abbreviation">Abbr</SortHeader>
              <SortHeader field="total_score">
                <span className="text-right w-full">Total Score</span>
              </SortHeader>
              <th className="px-6 py-3 text-right text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
            {sortedAndFilteredRankings.map((state) => (
              <tr key={state.id} className="hover:bg-zinc-50 dark:hover:bg-zinc-700/50">
                <td className="px-6 py-4 whitespace-nowrap text-sm text-zinc-500 dark:text-zinc-400">
                  {state.rank}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-zinc-900 dark:text-white">
                  <Link href={`/states/${state.id}`} className="hover:text-blue-600 dark:hover:text-blue-400">
                    {state.name}
                  </Link>
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
                <td className="px-6 py-4 whitespace-nowrap text-sm text-right">
                  <Link
                    href={`/states/${state.id}`}
                    className="text-blue-600 hover:text-blue-800 dark:text-blue-400"
                  >
                    Details
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="text-sm text-zinc-500 dark:text-zinc-400">
        Showing {sortedAndFilteredRankings.length} of {data?.rankings.length || 0} states
      </div>
    </div>
  );
}
