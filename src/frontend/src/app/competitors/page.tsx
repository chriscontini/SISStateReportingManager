"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface CompetitorStrength {
  category: string;
  rating: number;
  description: string | null;
  is_strength: boolean;
}

interface Competitor {
  id: number;
  name: string;
  description: string | null;
  competitor_type: string;
  headquarters: string | null;
  website: string | null;
  total_states: number;
  total_districts: number | null;
  total_students: number | null;
  primary_product: string | null;
  has_state_reporting: boolean;
  has_lms: boolean;
  has_assessment: boolean;
  strengths: CompetitorStrength[];
}

interface CompetitiveSummary {
  total_competitors: number;
  by_type: Record<string, number>;
  most_competitive_states: { state: string; abbrev: string; competitor_count: number }[];
  least_competitive_states: { state: string; abbrev: string; competitor_count: number }[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const typeColors: Record<string, string> = {
  national: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  regional: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  local: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
};

function RatingStars({ rating }: { rating: number }) {
  return (
    <div className="flex gap-0.5">
      {[1, 2, 3, 4, 5].map((star) => (
        <span
          key={star}
          className={star <= rating ? "text-yellow-500" : "text-zinc-300 dark:text-zinc-600"}
        >
          ★
        </span>
      ))}
    </div>
  );
}

export default function CompetitorsPage() {
  const [competitors, setCompetitors] = useState<Competitor[]>([]);
  const [summary, setSummary] = useState<CompetitiveSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedType, setSelectedType] = useState<string>("all");

  useEffect(() => {
    async function fetchData() {
      try {
        const [competitorsRes, summaryRes] = await Promise.all([
          fetch(`${API_URL}/api/competitors`),
          fetch(`${API_URL}/api/competitors/summary`),
        ]);

        if (!competitorsRes.ok || !summaryRes.ok) {
          throw new Error("Failed to fetch competitor data");
        }

        const competitorsData = await competitorsRes.json();
        const summaryData = await summaryRes.json();

        setCompetitors(competitorsData.competitors);
        setSummary(summaryData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-zinc-500 dark:text-zinc-400">Loading competitors...</div>
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

  const filteredCompetitors =
    selectedType === "all"
      ? competitors
      : competitors.filter((c) => c.competitor_type === selectedType);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
          Competitive Intelligence
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400 mt-2">
          SIS vendor competitive landscape analysis
        </p>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Competitors</div>
            <div className="text-2xl font-bold text-zinc-900 dark:text-white">
              {summary.total_competitors}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">National Vendors</div>
            <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {summary.by_type.national || 0}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Regional Vendors</div>
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {summary.by_type.regional || 0}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Local Vendors</div>
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              {summary.by_type.local || 0}
            </div>
          </div>
        </div>
      )}

      {/* Market Insights */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <h3 className="font-semibold text-zinc-900 dark:text-white mb-3">
              Most Competitive States
            </h3>
            <div className="space-y-2">
              {summary.most_competitive_states.slice(0, 5).map((state) => (
                <div key={state.abbrev} className="flex justify-between items-center">
                  <span className="text-zinc-700 dark:text-zinc-300">{state.state}</span>
                  <span className="text-sm bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300 px-2 py-0.5 rounded">
                    {state.competitor_count} vendors
                  </span>
                </div>
              ))}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <h3 className="font-semibold text-zinc-900 dark:text-white mb-3">
              Least Competitive States
            </h3>
            <div className="space-y-2">
              {summary.least_competitive_states.slice(0, 5).map((state) => (
                <div key={state.abbrev} className="flex justify-between items-center">
                  <span className="text-zinc-700 dark:text-zinc-300">{state.state}</span>
                  <span className="text-sm bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300 px-2 py-0.5 rounded">
                    {state.competitor_count} vendors
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Filter */}
      <div className="flex gap-2">
        <button
          onClick={() => setSelectedType("all")}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            selectedType === "all"
              ? "bg-zinc-900 text-white dark:bg-white dark:text-zinc-900"
              : "bg-zinc-100 text-zinc-700 hover:bg-zinc-200 dark:bg-zinc-800 dark:text-zinc-300 dark:hover:bg-zinc-700"
          }`}
        >
          All
        </button>
        <button
          onClick={() => setSelectedType("national")}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            selectedType === "national"
              ? "bg-purple-600 text-white"
              : "bg-purple-100 text-purple-700 hover:bg-purple-200 dark:bg-purple-900/30 dark:text-purple-300"
          }`}
        >
          National
        </button>
        <button
          onClick={() => setSelectedType("regional")}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            selectedType === "regional"
              ? "bg-blue-600 text-white"
              : "bg-blue-100 text-blue-700 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-300"
          }`}
        >
          Regional
        </button>
      </div>

      {/* Competitor Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCompetitors.map((competitor) => (
          <Link
            key={competitor.id}
            href={`/competitors/${competitor.id}`}
            className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4 hover:border-blue-500 dark:hover:border-blue-400 transition-colors"
          >
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-semibold text-zinc-900 dark:text-white">
                {competitor.name}
              </h3>
              <span className={`text-xs px-2 py-0.5 rounded ${typeColors[competitor.competitor_type]}`}>
                {competitor.competitor_type}
              </span>
            </div>
            <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3 line-clamp-2">
              {competitor.description || "No description available"}
            </p>
            <div className="flex flex-wrap gap-2 mb-3">
              <span className="text-xs bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-300 px-2 py-1 rounded">
                {competitor.total_states} states
              </span>
              {competitor.has_state_reporting && (
                <span className="text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 px-2 py-1 rounded">
                  State Reporting
                </span>
              )}
              {competitor.has_lms && (
                <span className="text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 px-2 py-1 rounded">
                  LMS
                </span>
              )}
            </div>
            {competitor.strengths.filter((s) => s.is_strength).length > 0 && (
              <div className="border-t border-zinc-200 dark:border-zinc-700 pt-2">
                <div className="text-xs text-zinc-500 dark:text-zinc-400 mb-1">Top Strengths:</div>
                <div className="space-y-1">
                  {competitor.strengths
                    .filter((s) => s.is_strength)
                    .slice(0, 2)
                    .map((strength) => (
                      <div key={strength.category} className="flex justify-between items-center">
                        <span className="text-xs text-zinc-600 dark:text-zinc-400 capitalize">
                          {strength.category.replace("_", " ")}
                        </span>
                        <RatingStars rating={strength.rating} />
                      </div>
                    ))}
                </div>
              </div>
            )}
          </Link>
        ))}
      </div>

      <div className="text-sm text-zinc-500 dark:text-zinc-400">
        Showing {filteredCompetitors.length} of {competitors.length} competitors
      </div>
    </div>
  );
}
