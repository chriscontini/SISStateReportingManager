'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import TierBadge from '@/components/TierBadge';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface State {
  id: number;
  name: string;
  abbreviation: string;
}

interface NCESData {
  total_districts: number | null;
  total_schools: number | null;
  total_students: number | null;
  avg_district_size: number | null;
}

interface ScoreWithFactor {
  factor_name: string;
  factor_weight: number;
  score: number;
  weighted_score: number;
}

interface StateComparison {
  id: number;
  name: string;
  abbreviation: string;
  total_score: number;
  nces_data: NCESData | null;
  scores: ScoreWithFactor[];
  has_analysis: boolean;
}

export default function ComparePage() {
  const [allStates, setAllStates] = useState<State[]>([]);
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [comparison, setComparison] = useState<StateComparison[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch all states for dropdowns
  useEffect(() => {
    async function fetchStates() {
      try {
        const response = await fetch(`${API_URL}/api/states`);
        if (!response.ok) throw new Error('Failed to fetch states');
        const data = await response.json();
        setAllStates(data.states || data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load states');
      }
    }
    fetchStates();
  }, []);

  // Fetch comparison when selection changes
  useEffect(() => {
    async function fetchComparison() {
      if (selectedIds.length < 2) {
        setComparison(null);
        return;
      }

      setLoading(true);
      try {
        const idsParam = selectedIds.join(',');
        const response = await fetch(`${API_URL}/api/states/compare?ids=${idsParam}`);
        if (!response.ok) throw new Error('Failed to fetch comparison');
        const data = await response.json();
        setComparison(data.states);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Comparison failed');
      } finally {
        setLoading(false);
      }
    }
    fetchComparison();
  }, [selectedIds]);

  const handleStateSelect = (index: number, stateId: number) => {
    const newIds = [...selectedIds];
    if (stateId === 0) {
      newIds.splice(index, 1);
    } else {
      newIds[index] = stateId;
    }
    setSelectedIds(newIds.filter(id => id > 0));
  };

  const addStateSlot = () => {
    if (selectedIds.length < 5) {
      setSelectedIds([...selectedIds, 0]);
    }
  };

  const formatNumber = (num: number | null) => {
    if (num === null) return 'N/A';
    return num.toLocaleString();
  };

  // Get unique factor names across all compared states
  const getAllFactors = (): string[] => {
    if (!comparison) return [];
    const factors = new Set<string>();
    comparison.forEach(state => {
      state.scores.forEach(score => factors.add(score.factor_name));
    });
    return Array.from(factors);
  };

  const getScoreForFactor = (state: StateComparison, factorName: string): ScoreWithFactor | undefined => {
    return state.scores.find(s => s.factor_name === factorName);
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">Compare States</h1>
        <p className="text-zinc-600 dark:text-zinc-400 mt-2">
          Select 2-5 states to compare side-by-side
        </p>
      </div>

      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">{error}</p>
        </div>
      )}

      {/* State Selection */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">Select States</h2>
        <div className="flex flex-wrap gap-4 items-center">
          {[0, 1, 2, 3, 4].map((index) => {
            if (index > selectedIds.length) return null;
            if (index === selectedIds.length && index >= 2) {
              return (
                <button
                  key={`add-${index}`}
                  onClick={addStateSlot}
                  className="px-4 py-2 border-2 border-dashed border-zinc-300 dark:border-zinc-600 rounded-lg text-zinc-500 hover:border-blue-500 hover:text-blue-500 transition-colors"
                >
                  + Add State
                </button>
              );
            }
            return (
              <select
                key={index}
                value={selectedIds[index] || 0}
                onChange={(e) => handleStateSelect(index, parseInt(e.target.value))}
                className="px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white min-w-[200px]"
              >
                <option value={0}>Select a state...</option>
                {allStates
                  .filter(s => !selectedIds.includes(s.id) || selectedIds[index] === s.id)
                  .map(state => (
                    <option key={state.id} value={state.id}>
                      {state.name} ({state.abbreviation})
                    </option>
                  ))}
              </select>
            );
          })}
        </div>
      </div>

      {loading && (
        <div className="text-center py-8 text-zinc-500">Loading comparison...</div>
      )}

      {comparison && comparison.length >= 2 && (
        <>
          {/* Overview Comparison */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 overflow-hidden">
            <div className="p-4 border-b border-zinc-200 dark:border-zinc-700">
              <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">Overview</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-zinc-50 dark:bg-zinc-900">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-zinc-500">Metric</th>
                    {comparison.map(state => (
                      <th key={state.id} className="px-4 py-3 text-center text-sm font-medium text-zinc-900 dark:text-white">
                        <Link href={`/states/${state.id}`} className="hover:text-blue-600">
                          {state.name}
                        </Link>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-400">Total Score</td>
                    {comparison.map(state => (
                      <td key={state.id} className="px-4 py-3 text-center">
                        <div className="flex items-center justify-center gap-2">
                          <span className="text-lg font-bold text-green-600 dark:text-green-400">
                            {state.total_score.toFixed(2)}
                          </span>
                          {state.total_score > 0 && <TierBadge score={state.total_score} size="sm" />}
                        </div>
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-400">Districts</td>
                    {comparison.map(state => (
                      <td key={state.id} className="px-4 py-3 text-center text-sm text-zinc-900 dark:text-white">
                        {formatNumber(state.nces_data?.total_districts || null)}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-400">Schools</td>
                    {comparison.map(state => (
                      <td key={state.id} className="px-4 py-3 text-center text-sm text-zinc-900 dark:text-white">
                        {formatNumber(state.nces_data?.total_schools || null)}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-400">Students</td>
                    {comparison.map(state => (
                      <td key={state.id} className="px-4 py-3 text-center text-sm text-zinc-900 dark:text-white">
                        {formatNumber(state.nces_data?.total_students || null)}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-400">Avg District Size</td>
                    {comparison.map(state => (
                      <td key={state.id} className="px-4 py-3 text-center text-sm text-zinc-900 dark:text-white">
                        {state.nces_data?.avg_district_size
                          ? Math.round(state.nces_data.avg_district_size).toLocaleString()
                          : 'N/A'}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-400">Deep Analysis</td>
                    {comparison.map(state => (
                      <td key={state.id} className="px-4 py-3 text-center">
                        {state.has_analysis ? (
                          <span className="text-green-600 dark:text-green-400">Available</span>
                        ) : (
                          <span className="text-zinc-400">Not yet</span>
                        )}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Score Breakdown Comparison */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 overflow-hidden">
            <div className="p-4 border-b border-zinc-200 dark:border-zinc-700">
              <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">Score Breakdown by Factor</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-zinc-50 dark:bg-zinc-900">
                  <tr>
                    <th className="px-4 py-3 text-left text-sm font-medium text-zinc-500">Factor</th>
                    {comparison.map(state => (
                      <th key={state.id} className="px-4 py-3 text-center text-sm font-medium text-zinc-900 dark:text-white">
                        {state.abbreviation}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
                  {getAllFactors().map(factorName => (
                    <tr key={factorName}>
                      <td className="px-4 py-3 text-sm text-zinc-600 dark:text-zinc-400">
                        {factorName}
                      </td>
                      {comparison.map(state => {
                        const score = getScoreForFactor(state, factorName);
                        const maxScore = Math.max(
                          ...comparison.map(s => getScoreForFactor(s, factorName)?.score || 0)
                        );
                        const isMax = score && score.score === maxScore && maxScore > 0;

                        return (
                          <td key={state.id} className="px-4 py-3 text-center">
                            {score ? (
                              <span className={`font-medium ${isMax ? 'text-green-600 dark:text-green-400' : 'text-zinc-900 dark:text-white'}`}>
                                {score.score.toFixed(1)}
                              </span>
                            ) : (
                              <span className="text-zinc-400">-</span>
                            )}
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex gap-4">
            {comparison.map(state => (
              <Link
                key={state.id}
                href={`/states/${state.id}`}
                className="flex-1 text-center px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
              >
                View {state.abbreviation} Details
              </Link>
            ))}
          </div>
        </>
      )}

      {!comparison && selectedIds.length < 2 && (
        <div className="text-center py-12 text-zinc-500 dark:text-zinc-400">
          <p>Select at least 2 states to compare</p>
        </div>
      )}
    </div>
  );
}
