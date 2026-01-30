'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import AppShell from '@/components/AppShell';

interface State {
  id: number;
  name: string;
  abbreviation: string;
}

interface Article {
  id: number;
  state_id: number;
  title: string;
  category: string;
  tags: string[];
  state?: State;
}

interface KnowledgeStats {
  total_articles: number;
  categories: string[];
  articles_by_state: Record<number, number>;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const CATEGORY_COLORS: Record<string, string> = {
  reporting: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
  assessment: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
  integration: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
  certification: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
  special_education: 'bg-pink-100 text-pink-800 dark:bg-pink-900/30 dark:text-pink-300',
  implementation: 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-300',
};

export default function KnowledgePage() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [stats, setStats] = useState<KnowledgeStats | null>(null);
  const [states, setStates] = useState<State[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedState, setSelectedState] = useState<string>('');
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  useEffect(() => {
    fetchData();
  }, []);

  useEffect(() => {
    if (searchQuery.length >= 2) {
      searchArticles();
    } else {
      fetchArticles();
    }
  }, [searchQuery, selectedState, selectedCategory]);

  const fetchData = async () => {
    try {
      const [statesRes, statsRes] = await Promise.all([
        fetch(`${API_URL}/api/states`),
        fetch(`${API_URL}/api/knowledge/stats`),
      ]);

      if (statesRes.ok) {
        const statesData = await statesRes.json();
        setStates(statesData);
      }

      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }

      await fetchArticles();
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchArticles = async () => {
    try {
      let url = `${API_URL}/api/knowledge/articles?limit=50`;
      if (selectedState) url += `&state_id=${selectedState}`;
      if (selectedCategory) url += `&category=${selectedCategory}`;

      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setArticles(data);
      }
    } catch (error) {
      console.error('Error fetching articles:', error);
    }
  };

  const searchArticles = async () => {
    try {
      let url = `${API_URL}/api/knowledge/search?q=${encodeURIComponent(searchQuery)}`;
      if (selectedState) url += `&state_id=${selectedState}`;
      if (selectedCategory) url += `&category=${selectedCategory}`;

      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        setArticles(data);
      }
    } catch (error) {
      console.error('Error searching articles:', error);
    }
  };

  const getCategoryColor = (category: string) => {
    return CATEGORY_COLORS[category] || 'bg-zinc-100 text-zinc-800 dark:bg-zinc-700 dark:text-zinc-300';
  };

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
            Knowledge Base
          </h1>
          <p className="mt-2 text-zinc-600 dark:text-zinc-400">
            State reporting documentation, requirements, and implementation guides
          </p>
        </div>

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Articles</div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {stats.total_articles}
              </div>
            </div>
            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Categories</div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {stats.categories.length}
              </div>
            </div>
            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
              <div className="text-sm text-zinc-500 dark:text-zinc-400">States Covered</div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {Object.keys(stats.articles_by_state).length}
              </div>
            </div>
          </div>
        )}

        {/* Search and Filters */}
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div>
              <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                Search
              </label>
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search articles..."
                className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
              />
            </div>

            {/* State Filter */}
            <div>
              <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                Filter by State
              </label>
              <select
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
              >
                <option value="">All States</option>
                {states.map((state) => (
                  <option key={state.id} value={state.id}>
                    {state.name} ({state.abbreviation})
                  </option>
                ))}
              </select>
            </div>

            {/* Category Filter */}
            <div>
              <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-1">
                Filter by Category
              </label>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="w-full px-3 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
              >
                <option value="">All Categories</option>
                {stats?.categories.map((category) => (
                  <option key={category} value={category}>
                    {category.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {/* Articles Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {articles.map((article) => (
            <Link
              key={article.id}
              href={`/knowledge/${article.id}`}
              className="bg-white dark:bg-zinc-800 rounded-lg shadow hover:shadow-md transition-shadow p-4"
            >
              <div className="flex items-start justify-between mb-2">
                <span className={`px-2 py-1 text-xs font-medium rounded ${getCategoryColor(article.category)}`}>
                  {article.category.replace(/_/g, ' ')}
                </span>
                {article.state && (
                  <span className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
                    {article.state.abbreviation}
                  </span>
                )}
              </div>

              <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-2 line-clamp-2">
                {article.title}
              </h3>

              {article.tags.length > 0 && (
                <div className="flex flex-wrap gap-1 mt-3">
                  {article.tags.slice(0, 3).map((tag) => (
                    <span
                      key={tag}
                      className="px-2 py-0.5 text-xs bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-400 rounded"
                    >
                      {tag}
                    </span>
                  ))}
                  {article.tags.length > 3 && (
                    <span className="px-2 py-0.5 text-xs text-zinc-500 dark:text-zinc-400">
                      +{article.tags.length - 3} more
                    </span>
                  )}
                </div>
              )}
            </Link>
          ))}
        </div>

        {articles.length === 0 && (
          <div className="text-center py-12 bg-white dark:bg-zinc-800 rounded-lg shadow">
            <p className="text-zinc-500 dark:text-zinc-400">
              {searchQuery ? 'No articles found matching your search.' : 'No knowledge articles yet.'}
            </p>
          </div>
        )}
      </div>
    </AppShell>
  );
}
