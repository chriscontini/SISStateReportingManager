"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";

interface ScoreWithFactor {
  factor_name: string;
  factor_weight: number;
  score: number;
  weighted_score: number;
  notes: string | null;
}

interface NCESData {
  total_districts: number | null;
  total_schools: number | null;
  total_students: number | null;
  avg_district_size: number | null;
  data_year: string | null;
}

interface StateDetail {
  id: number;
  name: string;
  abbreviation: string;
  doe_website: string | null;
  total_score: number;
  rank: number | null;
  nces_data: NCESData | null;
  scores: ScoreWithFactor[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function StateDetailPage() {
  const params = useParams();
  const stateId = params.id as string;

  const [state, setState] = useState<StateDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchStateDetail() {
      try {
        const response = await fetch(`${API_URL}/api/states/${stateId}/detail`);
        if (!response.ok) {
          throw new Error("Failed to fetch state details");
        }
        const data = await response.json();
        setState(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    if (stateId) {
      fetchStateDetail();
    }
  }, [stateId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-zinc-500 dark:text-zinc-400">Loading state details...</div>
      </div>
    );
  }

  if (error || !state) {
    return (
      <div className="space-y-4">
        <Link href="/states" className="text-blue-600 hover:text-blue-800 dark:text-blue-400">
          &larr; Back to States
        </Link>
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">Error: {error || "State not found"}</p>
        </div>
      </div>
    );
  }

  const formatNumber = (num: number | null) => {
    if (num === null) return "N/A";
    return num.toLocaleString();
  };

  return (
    <div className="space-y-6">
      <Link href="/states" className="text-blue-600 hover:text-blue-800 dark:text-blue-400">
        &larr; Back to States
      </Link>

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
            {state.name} ({state.abbreviation})
          </h1>
          {state.doe_website && (
            <a
              href={state.doe_website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 text-sm"
            >
              {state.doe_website}
            </a>
          )}
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-green-600 dark:text-green-400">
            {state.total_score.toFixed(2)}
          </div>
          <div className="text-sm text-zinc-500 dark:text-zinc-400">
            Rank #{state.rank || "N/A"} of 50
          </div>
        </div>
      </div>

      {/* NCES Data */}
      {state.nces_data && (
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
            NCES Data {state.nces_data.data_year && `(${state.nces_data.data_year})`}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {formatNumber(state.nces_data.total_districts)}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Districts</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {formatNumber(state.nces_data.total_schools)}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Schools</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {formatNumber(state.nces_data.total_students)}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Students</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {state.nces_data.avg_district_size
                  ? Math.round(state.nces_data.avg_district_size).toLocaleString()
                  : "N/A"}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Avg District Size</div>
            </div>
          </div>
        </div>
      )}

      {/* Scores Breakdown */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
          Score Breakdown
        </h2>
        {state.scores.length > 0 ? (
          <div className="space-y-3">
            {state.scores
              .sort((a, b) => b.weighted_score - a.weighted_score)
              .map((score) => (
                <div
                  key={score.factor_name}
                  className="flex items-center justify-between p-3 bg-zinc-50 dark:bg-zinc-900 rounded-md"
                >
                  <div className="flex-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-zinc-900 dark:text-white">
                        {score.factor_name}
                      </span>
                      <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-0.5 rounded">
                        Weight: {score.factor_weight}
                      </span>
                    </div>
                    {score.notes && (
                      <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
                        {score.notes}
                      </p>
                    )}
                  </div>
                  <div className="text-right ml-4">
                    <div className="font-bold text-zinc-900 dark:text-white">
                      {score.score.toFixed(1)}
                    </div>
                    <div className="text-xs text-zinc-500 dark:text-zinc-400">
                      Weighted: {score.weighted_score.toFixed(2)}
                    </div>
                  </div>
                </div>
              ))}
          </div>
        ) : (
          <div className="text-center py-8 text-zinc-500 dark:text-zinc-400">
            No scores calculated yet. Run score calculation from the Rankings page.
          </div>
        )}
      </div>
    </div>
  );
}
