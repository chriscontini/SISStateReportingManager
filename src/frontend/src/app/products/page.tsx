"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

interface ProductFeature {
  id: number;
  name: string;
  category: string;
  complexity: string;
  is_state_specific: boolean;
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
  feature_count: number;
  features: ProductFeature[];
}

interface ProductSummary {
  total_products: number;
  hub_count: number;
  spoke_count: number;
  total_features: number;
  states_analyzed: number;
  product_fit_averages: { product: string; avg_fit: number | null }[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const categoryColors: Record<string, string> = {
  sis: "bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300",
  lms: "bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300",
  assessment: "bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300",
  special_ed: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300",
  finance: "bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300",
  hr: "bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-300",
  transportation: "bg-teal-100 text-teal-800 dark:bg-teal-900/30 dark:text-teal-300",
};

const complexityColors: Record<string, string> = {
  low: "text-green-600 dark:text-green-400",
  medium: "text-yellow-600 dark:text-yellow-400",
  high: "text-red-600 dark:text-red-400",
};

export default function ProductsPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [summary, setSummary] = useState<ProductSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const [productsRes, summaryRes] = await Promise.all([
          fetch(`${API_URL}/api/products`),
          fetch(`${API_URL}/api/products/summary`),
        ]);

        if (!productsRes.ok || !summaryRes.ok) {
          throw new Error("Failed to fetch product data");
        }

        const productsData = await productsRes.json();
        const summaryData = await summaryRes.json();

        setProducts(productsData.products);
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
        <div className="text-zinc-500 dark:text-zinc-400">Loading products...</div>
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

  const hubProduct = products.find((p) => p.product_type === "hub");
  const spokeProducts = products.filter((p) => p.product_type === "spoke");

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
          Product Portfolio
        </h1>
        <p className="text-zinc-600 dark:text-zinc-400 mt-2">
          Hub &amp; Spoke product alignment for state expansion
        </p>
      </div>

      {/* Summary Cards */}
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Products</div>
            <div className="text-2xl font-bold text-zinc-900 dark:text-white">
              {summary.total_products}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Hub (Core SIS)</div>
            <div className="text-2xl font-bold text-purple-600 dark:text-purple-400">
              {summary.hub_count}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Spoke Products</div>
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">
              {summary.spoke_count}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Features</div>
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">
              {summary.total_features}
            </div>
          </div>
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4">
            <div className="text-sm text-zinc-500 dark:text-zinc-400">States Analyzed</div>
            <div className="text-2xl font-bold text-orange-600 dark:text-orange-400">
              {summary.states_analyzed}
            </div>
          </div>
        </div>
      )}

      {/* Hub Product */}
      {hubProduct && (
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 dark:from-purple-900/20 dark:to-blue-900/20 rounded-lg border border-purple-200 dark:border-purple-800 p-6">
          <div className="flex items-center gap-2 mb-2">
            <span className="bg-purple-600 text-white text-xs px-2 py-1 rounded">HUB</span>
            <h2 className="text-xl font-bold text-zinc-900 dark:text-white">
              {hubProduct.name}
            </h2>
          </div>
          <p className="text-zinc-600 dark:text-zinc-400 mb-4">
            {hubProduct.description}
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div>
              <span className="text-sm text-zinc-500 dark:text-zinc-400">States</span>
              <p className="font-semibold text-zinc-900 dark:text-white">{hubProduct.total_states}</p>
            </div>
            <div>
              <span className="text-sm text-zinc-500 dark:text-zinc-400">Districts</span>
              <p className="font-semibold text-zinc-900 dark:text-white">{hubProduct.total_districts?.toLocaleString() || "N/A"}</p>
            </div>
            <div>
              <span className="text-sm text-zinc-500 dark:text-zinc-400">Features</span>
              <p className="font-semibold text-zinc-900 dark:text-white">{hubProduct.feature_count}</p>
            </div>
            <div>
              <span className="text-sm text-zinc-500 dark:text-zinc-400">Since</span>
              <p className="font-semibold text-zinc-900 dark:text-white">{hubProduct.launch_year || "N/A"}</p>
            </div>
          </div>
          <Link
            href={`/products/${hubProduct.id}`}
            className="inline-flex items-center text-purple-600 hover:text-purple-800 dark:text-purple-400 dark:hover:text-purple-300"
          >
            View Details →
          </Link>
        </div>
      )}

      {/* Spoke Products */}
      <div>
        <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
          Spoke Products ({spokeProducts.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {spokeProducts.map((product) => (
            <Link
              key={product.id}
              href={`/products/${product.id}`}
              className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-4 hover:border-blue-500 dark:hover:border-blue-400 transition-colors"
            >
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-semibold text-zinc-900 dark:text-white">
                  {product.name}
                </h3>
                <span className={`text-xs px-2 py-0.5 rounded ${categoryColors[product.category || ""] || "bg-zinc-100 text-zinc-800 dark:bg-zinc-700 dark:text-zinc-300"}`}>
                  {product.category?.replace("_", " ") || "General"}
                </span>
              </div>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-3 line-clamp-2">
                {product.description || "No description available"}
              </p>
              <div className="flex flex-wrap gap-2 mb-3">
                <span className="text-xs bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-300 px-2 py-1 rounded">
                  {product.feature_count} features
                </span>
                <span className="text-xs bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-300 px-2 py-1 rounded">
                  {product.total_states} states
                </span>
                <span className={`text-xs px-2 py-1 rounded ${complexityColors[product.integration_complexity]}`}>
                  {product.integration_complexity} integration
                </span>
              </div>
              <div className="border-t border-zinc-200 dark:border-zinc-700 pt-2">
                <div className="flex justify-between items-center text-sm">
                  <span className="text-zinc-500 dark:text-zinc-400">Pricing</span>
                  <span className="text-zinc-900 dark:text-white capitalize">
                    {product.pricing_tier || "Standard"}
                  </span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>

      {/* Product Fit Averages */}
      {summary && summary.product_fit_averages.length > 0 && (
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-4">
            Average Fit Scores by Product
          </h2>
          <div className="space-y-3">
            {summary.product_fit_averages
              .filter((p) => p.avg_fit !== null)
              .sort((a, b) => (b.avg_fit || 0) - (a.avg_fit || 0))
              .map((item) => (
                <div key={item.product} className="flex items-center gap-4">
                  <span className="w-40 text-sm text-zinc-700 dark:text-zinc-300 truncate">
                    {item.product.replace("OnCourse ", "")}
                  </span>
                  <div className="flex-1 bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
                    <div
                      className="bg-blue-600 h-2 rounded-full"
                      style={{ width: `${((item.avg_fit || 0) / 10) * 100}%` }}
                    />
                  </div>
                  <span className="w-12 text-sm font-medium text-zinc-900 dark:text-white text-right">
                    {item.avg_fit}/10
                  </span>
                </div>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
