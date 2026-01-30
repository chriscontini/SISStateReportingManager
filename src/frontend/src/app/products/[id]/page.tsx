"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";

interface ProductFeature {
  id: number;
  name: string;
  description: string | null;
  category: string;
  complexity: string;
  is_state_specific: boolean;
  customization_effort: number;
}

interface StateFit {
  state_id: number;
  state_name: string;
  state_abbrev: string;
  fit_score: number;
  gap_count: number;
  synergy_score: number;
}

interface Product {
  id: number;
  name: string;
  description: string | null;
  product_type: string;
  category: string | null;
  is_core: boolean;
  launch_year: number | null;
  total_states: number;
  total_districts: number | null;
  integration_complexity: string;
  pricing_tier: string | null;
  features: ProductFeature[];
  state_fits: StateFit[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const categoryColors: Record<string, string> = {
  core: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  reporting: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  integration: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  analytics: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  compliance: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  automation: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-300",
};

const complexityColors: Record<string, string> = {
  low: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  medium: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  high: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
};

function FitScoreBadge({ score }: { score: number }) {
  let color = "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300";
  if (score >= 8) {
    color = "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300";
  } else if (score >= 6.5) {
    color = "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300";
  }

  return (
    <span className={`text-sm px-2 py-1 rounded ${color}`}>
      {score.toFixed(1)}/10
    </span>
  );
}

export default function ProductDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProduct() {
      try {
        const response = await fetch(`${API_URL}/api/products/${params.id}`);
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error("Product not found");
          }
          throw new Error("Failed to fetch product");
        }
        const data = await response.json();
        setProduct(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    if (params.id) {
      fetchProduct();
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-zinc-500 dark:text-zinc-400">Loading product...</div>
      </div>
    );
  }

  if (error || !product) {
    return (
      <div className="space-y-4">
        <button
          onClick={() => router.back()}
          className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
        >
          ← Back to Products
        </button>
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">Error: {error}</p>
        </div>
      </div>
    );
  }

  const coreFeatures = product.features.filter((f) => f.category === "core");
  const otherFeatures = product.features.filter((f) => f.category !== "core");

  return (
    <div className="space-y-6">
      {/* Back link */}
      <Link
        href="/products"
        className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 inline-flex items-center"
      >
        ← Back to Products
      </Link>

      {/* Header */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <div className="flex justify-between items-start">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span
                className={`text-xs px-2 py-1 rounded ${
                  product.product_type === "hub"
                    ? "bg-purple-600 text-white"
                    : "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300"
                }`}
              >
                {product.product_type.toUpperCase()}
              </span>
              {product.is_core && (
                <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
                  Core Product
                </span>
              )}
            </div>
            <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
              {product.name}
            </h1>
          </div>
          <div className="text-right">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Pricing Tier</div>
            <div className="text-lg font-semibold text-zinc-900 dark:text-white capitalize">
              {product.pricing_tier || "Standard"}
            </div>
          </div>
        </div>
        <p className="mt-4 text-zinc-600 dark:text-zinc-400">
          {product.description || "No description available"}
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">States</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {product.total_states}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Districts</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {product.total_districts?.toLocaleString() || "N/A"}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Features</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {product.features.length}
          </div>
        </div>
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
          <div className="text-sm text-zinc-500 dark:text-zinc-400">Launch Year</div>
          <div className="text-2xl font-bold text-zinc-900 dark:text-white">
            {product.launch_year || "N/A"}
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
          Features ({product.features.length})
        </h2>

        {coreFeatures.length > 0 && (
          <div className="mb-6">
            <h3 className="text-sm font-medium text-zinc-500 dark:text-zinc-400 mb-3">
              Core Features
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {coreFeatures.map((feature) => (
                <div
                  key={feature.id}
                  className="p-3 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg"
                >
                  <div className="flex justify-between items-start">
                    <span className="font-medium text-zinc-900 dark:text-white">
                      {feature.name}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded ${complexityColors[feature.complexity]}`}>
                      {feature.complexity}
                    </span>
                  </div>
                  {feature.is_state_specific && (
                    <span className="text-xs text-orange-600 dark:text-orange-400">
                      State-specific customization required
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {otherFeatures.length > 0 && (
          <div>
            <h3 className="text-sm font-medium text-zinc-500 dark:text-zinc-400 mb-3">
              Additional Features
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {otherFeatures.map((feature) => (
                <div
                  key={feature.id}
                  className="p-3 bg-zinc-50 dark:bg-zinc-700/50 rounded-lg"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <span className="font-medium text-zinc-900 dark:text-white">
                        {feature.name}
                      </span>
                      <span className={`ml-2 text-xs px-2 py-0.5 rounded ${categoryColors[feature.category] || "bg-zinc-100 dark:bg-zinc-600"}`}>
                        {feature.category}
                      </span>
                    </div>
                    <span className={`text-xs px-2 py-0.5 rounded ${complexityColors[feature.complexity]}`}>
                      {feature.complexity}
                    </span>
                  </div>
                  {feature.is_state_specific && (
                    <span className="text-xs text-orange-600 dark:text-orange-400">
                      State-specific ({feature.customization_effort}h)
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* State Fit Analysis */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
          State Fit Analysis ({product.state_fits?.length || 0} states)
        </h2>
        {product.state_fits && product.state_fits.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
              <thead>
                <tr>
                  <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                    State
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                    Fit Score
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                    Gaps
                  </th>
                  <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                    Synergy
                  </th>
                  <th className="px-4 py-3 text-right text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
                {product.state_fits.map((fit) => (
                  <tr key={fit.state_id} className="hover:bg-zinc-50 dark:hover:bg-zinc-700/50">
                    <td className="px-4 py-3 whitespace-nowrap">
                      <Link
                        href={`/states/${fit.state_id}`}
                        className="font-medium text-zinc-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400"
                      >
                        {fit.state_name}
                      </Link>
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap">
                      <FitScoreBadge score={fit.fit_score} />
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-zinc-600 dark:text-zinc-400">
                      {fit.gap_count} gaps
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-zinc-600 dark:text-zinc-400">
                      {fit.synergy_score?.toFixed(1) || "N/A"}
                    </td>
                    <td className="px-4 py-3 whitespace-nowrap text-right">
                      <Link
                        href={`/states/${fit.state_id}`}
                        className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 text-sm"
                      >
                        View State
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-zinc-500 dark:text-zinc-400">No state fit analysis data available</p>
        )}
      </div>
    </div>
  );
}
