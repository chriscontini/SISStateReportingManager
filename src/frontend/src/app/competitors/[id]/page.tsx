"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

interface CompetitorStrength {
  category: string;
  rating: number;
  description: string | null;
  is_strength: boolean;
}

interface StatePresence {
  state_id: number;
  state_name: string;
  state_abbrev: string;
  presence_level: string;
  market_share_percent: number | null;
  district_count: number | null;
  is_certified: boolean;
}

interface Competitor {
  id: number;
  name: string;
  description: string | null;
  competitor_type: string;
  headquarters: string | null;
  website: string | null;
  founded_year: number | null;
  employee_count: string | null;
  total_states: number;
  total_districts: number | null;
  total_students: number | null;
  primary_product: string | null;
  has_state_reporting: boolean;
  has_lms: boolean;
  has_assessment: boolean;
  strengths: CompetitorStrength[];
  state_presence: StatePresence[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const presenceLevelColors: Record<string, string> = {
  dominant: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  strong: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  moderate: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  minimal: "bg-zinc-100 text-zinc-800 dark:bg-zinc-700 dark:text-zinc-300",
};

function RatingBar({ rating, label }: { rating: number; label: string }) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-sm text-zinc-600 dark:text-zinc-400 w-32 capitalize">
        {label.replace("_", " ")}
      </span>
      <div className="flex-1 bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
        <div
          className="bg-blue-600 h-2 rounded-full"
          style={{ width: `${(rating / 5) * 100}%` }}
        />
      </div>
      <span className="text-sm font-medium text-zinc-900 dark:text-white w-8">
        {rating}/5
      </span>
    </div>
  );
}

export default function CompetitorDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [competitor, setCompetitor] = useState<Competitor | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchCompetitor() {
      try {
        const response = await fetch(`${API_URL}/api/competitors/${params.id}`);
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error("Competitor not found");
          }
          throw new Error("Failed to fetch competitor");
        }
        const data = await response.json();
        setCompetitor(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    if (params.id) {
      fetchCompetitor();
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-zinc-500 dark:text-zinc-400">Loading competitor...</div>
      </div>
    );
  }

  if (error || !competitor) {
    return (
      <div className="space-y-4">
        <button
          onClick={() => router.back()}
          className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
        >
          ← Back to Competitors
        </button>
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">Error: {error}</p>
        </div>
      </div>
    );
  }

  const strengths = competitor.strengths.filter((s) => s.is_strength);
  const weaknesses = competitor.strengths.filter((s) => !s.is_strength);

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/competitors"
        className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 inline-flex items-center"
      >
        ← Back to Competitors
      </Link>

      {/* Header */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <div className="flex justify-between items-start">
          <div>
            <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
              {competitor.name}
            </h1>
            <div className="flex items-center gap-3 mt-2">
              <span
                className={`text-sm px-3 py-1 rounded-full ${
                  competitor.competitor_type === "national"
                    ? "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300"
                    : competitor.competitor_type === "regional"
                    ? "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300"
                    : "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300"
                }`}
              >
                {competitor.competitor_type.charAt(0).toUpperCase() + competitor.competitor_type.slice(1)} Vendor
              </span>
              {competitor.headquarters && (
                <span className="text-zinc-500 dark:text-zinc-400">
                  HQ: {competitor.headquarters}
                </span>
              )}
            </div>
          </div>
          {competitor.website && (
            <a
              href={competitor.website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
            >
              Visit Website →
            </a>
          )}
        </div>
        <p className="mt-4 text-zinc-600 dark:text-zinc-400">
          {competitor.description || "No description available"}
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">States Served</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {competitor.total_states}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Districts</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {competitor.total_districts?.toLocaleString() || "N/A"}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Students Served</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {competitor.total_students?.toLocaleString() || "N/A"}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Founded</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {competitor.founded_year || "N/A"}
          </div>
        </div>
      </div>

      {/* Product Features */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
          Product Features
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="flex items-center gap-2">
            <span
              className={`w-3 h-3 rounded-full ${
                competitor.has_state_reporting ? "bg-green-500" : "bg-zinc-300 dark:bg-zinc-600"
              }`}
            />
            <span className="text-zinc-700 dark:text-zinc-300">State Reporting</span>
          </div>
          <div className="flex items-center gap-2">
            <span
              className={`w-3 h-3 rounded-full ${
                competitor.has_lms ? "bg-green-500" : "bg-zinc-300 dark:bg-zinc-600"
              }`}
            />
            <span className="text-zinc-700 dark:text-zinc-300">LMS</span>
          </div>
          <div className="flex items-center gap-2">
            <span
              className={`w-3 h-3 rounded-full ${
                competitor.has_assessment ? "bg-green-500" : "bg-zinc-300 dark:bg-zinc-600"
              }`}
            />
            <span className="text-zinc-700 dark:text-zinc-300">Assessment</span>
          </div>
          {competitor.primary_product && (
            <div className="col-span-2 md:col-span-1">
              <span className="text-sm text-zinc-500 dark:text-zinc-400">Primary Product:</span>
              <span className="ml-2 text-zinc-900 dark:text-white">{competitor.primary_product}</span>
            </div>
          )}
        </div>
      </div>

      {/* Strengths & Weaknesses */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
          <h2 className="text-xl font-semibold text-green-600 dark:text-green-400 mb-4">
            Strengths
          </h2>
          <div className="space-y-3">
            {strengths.length > 0 ? (
              strengths.map((strength) => (
                <div key={strength.category}>
                  <RatingBar rating={strength.rating} label={strength.category} />
                  {strength.description && (
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 ml-35">
                      {strength.description}
                    </p>
                  )}
                </div>
              ))
            ) : (
              <p className="text-zinc-500 dark:text-zinc-400">No strengths data available</p>
            )}
          </div>
        </div>

        {/* Weaknesses */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
          <h2 className="text-xl font-semibold text-red-600 dark:text-red-400 mb-4">
            Weaknesses
          </h2>
          <div className="space-y-3">
            {weaknesses.length > 0 ? (
              weaknesses.map((weakness) => (
                <div key={weakness.category}>
                  <RatingBar rating={weakness.rating} label={weakness.category} />
                  {weakness.description && (
                    <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1 ml-35">
                      {weakness.description}
                    </p>
                  )}
                </div>
              ))
            ) : (
              <p className="text-zinc-500 dark:text-zinc-400">No weaknesses data available</p>
            )}
          </div>
        </div>
      </div>

      {/* State Presence */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
          State Presence ({competitor.state_presence?.length || 0} states)
        </h2>
        {competitor.state_presence && competitor.state_presence.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
            {competitor.state_presence
              .sort((a, b) => {
                const order = { dominant: 0, strong: 1, moderate: 2, minimal: 3 };
                return (order[a.presence_level as keyof typeof order] || 4) -
                       (order[b.presence_level as keyof typeof order] || 4);
              })
              .map((presence) => (
                <Link
                  key={presence.state_id}
                  href={`/states/${presence.state_id}`}
                  className="flex items-center justify-between p-3 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg hover:bg-zinc-100 dark:hover:bg-zinc-700 transition-colors"
                >
                  <div>
                    <div className="font-medium text-zinc-900 dark:text-white">
                      {presence.state_name}
                    </div>
                    {presence.market_share_percent && (
                      <div className="text-xs text-zinc-500 dark:text-zinc-400">
                        {presence.market_share_percent}% market share
                      </div>
                    )}
                  </div>
                  <span
                    className={`text-xs px-2 py-1 rounded ${presenceLevelColors[presence.presence_level]}`}
                  >
                    {presence.presence_level}
                  </span>
                </Link>
              ))}
          </div>
        ) : (
          <p className="text-zinc-500 dark:text-zinc-400">No state presence data available</p>
        )}
      </div>
    </div>
  );
}
