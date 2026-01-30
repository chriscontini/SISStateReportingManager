'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
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
  content: string;
  category: string;
  source_url: string | null;
  tags: string[];
  state?: State;
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

export default function KnowledgeArticlePage() {
  const params = useParams();
  const articleId = params.id;

  const [article, setArticle] = useState<Article | null>(null);
  const [relatedArticles, setRelatedArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (articleId) {
      fetchArticle();
      fetchRelatedArticles();
    }
  }, [articleId]);

  const fetchArticle = async () => {
    try {
      const res = await fetch(`${API_URL}/api/knowledge/articles/${articleId}`);
      if (res.ok) {
        const data = await res.json();
        setArticle(data);
      } else if (res.status === 404) {
        setError('Article not found');
      } else {
        setError('Failed to load article');
      }
    } catch (err) {
      console.error('Error fetching article:', err);
      setError('Failed to load article');
    } finally {
      setLoading(false);
    }
  };

  const fetchRelatedArticles = async () => {
    try {
      const res = await fetch(`${API_URL}/api/knowledge/articles/${articleId}/related`);
      if (res.ok) {
        const data = await res.json();
        setRelatedArticles(data);
      }
    } catch (err) {
      console.error('Error fetching related articles:', err);
    }
  };

  const getCategoryColor = (category: string) => {
    return CATEGORY_COLORS[category] || 'bg-zinc-100 text-zinc-800 dark:bg-zinc-700 dark:text-zinc-300';
  };

  const renderMarkdown = (content: string) => {
    // Simple markdown rendering
    const lines = content.split('\n');
    const elements: JSX.Element[] = [];
    let inCodeBlock = false;
    let codeContent: string[] = [];
    let inTable = false;
    let tableRows: string[][] = [];

    lines.forEach((line, index) => {
      // Code blocks
      if (line.startsWith('```')) {
        if (inCodeBlock) {
          elements.push(
            <pre key={`code-${index}`} className="bg-zinc-100 dark:bg-zinc-900 p-4 rounded-lg overflow-x-auto my-4 text-sm">
              <code>{codeContent.join('\n')}</code>
            </pre>
          );
          codeContent = [];
        }
        inCodeBlock = !inCodeBlock;
        return;
      }

      if (inCodeBlock) {
        codeContent.push(line);
        return;
      }

      // Tables
      if (line.startsWith('|')) {
        if (!inTable) {
          inTable = true;
          tableRows = [];
        }
        const cells = line.split('|').filter(c => c.trim() !== '');
        if (!line.includes('---')) {
          tableRows.push(cells.map(c => c.trim()));
        }
        return;
      } else if (inTable && line.trim() === '') {
        // End of table
        elements.push(
          <div key={`table-${index}`} className="overflow-x-auto my-4">
            <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
              <thead>
                <tr>
                  {tableRows[0]?.map((cell, i) => (
                    <th key={i} className="px-4 py-2 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                      {cell}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
                {tableRows.slice(1).map((row, rowIndex) => (
                  <tr key={rowIndex}>
                    {row.map((cell, cellIndex) => (
                      <td key={cellIndex} className="px-4 py-2 text-sm text-zinc-900 dark:text-white">
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
        inTable = false;
        tableRows = [];
      }

      if (inTable) return;

      // Headers
      if (line.startsWith('# ')) {
        elements.push(
          <h1 key={index} className="text-2xl font-bold text-zinc-900 dark:text-white mt-6 mb-4">
            {line.slice(2)}
          </h1>
        );
      } else if (line.startsWith('## ')) {
        elements.push(
          <h2 key={index} className="text-xl font-semibold text-zinc-900 dark:text-white mt-5 mb-3">
            {line.slice(3)}
          </h2>
        );
      } else if (line.startsWith('### ')) {
        elements.push(
          <h3 key={index} className="text-lg font-semibold text-zinc-900 dark:text-white mt-4 mb-2">
            {line.slice(4)}
          </h3>
        );
      }
      // Lists
      else if (line.match(/^\d+\.\s/)) {
        elements.push(
          <li key={index} className="ml-6 text-zinc-700 dark:text-zinc-300 list-decimal">
            {line.replace(/^\d+\.\s/, '')}
          </li>
        );
      } else if (line.startsWith('- ')) {
        elements.push(
          <li key={index} className="ml-6 text-zinc-700 dark:text-zinc-300 list-disc">
            {line.slice(2)}
          </li>
        );
      }
      // Empty lines
      else if (line.trim() === '') {
        elements.push(<div key={index} className="h-2" />);
      }
      // Regular paragraphs
      else {
        // Handle bold text
        const formattedLine = line.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        elements.push(
          <p
            key={index}
            className="text-zinc-700 dark:text-zinc-300 my-2"
            dangerouslySetInnerHTML={{ __html: formattedLine }}
          />
        );
      }
    });

    // Handle remaining table at end
    if (inTable && tableRows.length > 0) {
      elements.push(
        <div key="table-end" className="overflow-x-auto my-4">
          <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
            <thead>
              <tr>
                {tableRows[0]?.map((cell, i) => (
                  <th key={i} className="px-4 py-2 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                    {cell}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
              {tableRows.slice(1).map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {row.map((cell, cellIndex) => (
                    <td key={cellIndex} className="px-4 py-2 text-sm text-zinc-900 dark:text-white">
                      {cell}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      );
    }

    return elements;
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

  if (error || !article) {
    return (
      <AppShell>
        <div className="text-center py-12">
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-white mb-4">
            {error || 'Article not found'}
          </h1>
          <Link
            href="/knowledge"
            className="text-blue-600 hover:text-blue-800 dark:text-blue-400"
          >
            Back to Knowledge Base
          </Link>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="flex gap-8">
        {/* Main Content */}
        <div className="flex-1 max-w-4xl">
          {/* Breadcrumb */}
          <div className="mb-4">
            <Link
              href="/knowledge"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 text-sm"
            >
              &larr; Back to Knowledge Base
            </Link>
          </div>

          {/* Article Header */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6 mb-6">
            <div className="flex items-center gap-3 mb-4">
              <span className={`px-3 py-1 text-sm font-medium rounded ${getCategoryColor(article.category)}`}>
                {article.category.replace(/_/g, ' ')}
              </span>
              {article.state && (
                <Link
                  href={`/states/${article.state.id}`}
                  className="text-sm font-medium text-zinc-600 dark:text-zinc-400 hover:text-blue-600"
                >
                  {article.state.name} ({article.state.abbreviation})
                </Link>
              )}
            </div>

            <h1 className="text-3xl font-bold text-zinc-900 dark:text-white mb-4">
              {article.title}
            </h1>

            {/* Tags */}
            {article.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                {article.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-2 py-1 text-xs bg-zinc-100 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-400 rounded"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Source Link */}
            {article.source_url && (
              <div className="mt-4 pt-4 border-t border-zinc-200 dark:border-zinc-700">
                <a
                  href={article.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400"
                >
                  View Official Source &rarr;
                </a>
              </div>
            )}
          </div>

          {/* Article Content */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
            <div className="prose dark:prose-invert max-w-none">
              {renderMarkdown(article.content)}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="w-80 hidden lg:block">
          {/* Related Articles */}
          {relatedArticles.length > 0 && (
            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4 sticky top-4">
              <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
                Related Articles
              </h3>
              <div className="space-y-3">
                {relatedArticles.map((related) => (
                  <Link
                    key={related.id}
                    href={`/knowledge/${related.id}`}
                    className="block p-3 rounded-lg hover:bg-zinc-50 dark:hover:bg-zinc-700/50 transition-colors"
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <span className={`px-2 py-0.5 text-xs font-medium rounded ${getCategoryColor(related.category)}`}>
                        {related.category.replace(/_/g, ' ')}
                      </span>
                      {related.state && (
                        <span className="text-xs text-zinc-500 dark:text-zinc-400">
                          {related.state.abbreviation}
                        </span>
                      )}
                    </div>
                    <p className="text-sm font-medium text-zinc-900 dark:text-white line-clamp-2">
                      {related.title}
                    </p>
                  </Link>
                ))}
              </div>
            </div>
          )}

          {/* Quick Links */}
          {article.state && (
            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4 mt-4">
              <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
                Quick Links
              </h3>
              <div className="space-y-2">
                <Link
                  href={`/states/${article.state.id}`}
                  className="block text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400"
                >
                  View {article.state.abbreviation} State Details
                </Link>
                <Link
                  href={`/gap-analysis/${article.state.id}`}
                  className="block text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400"
                >
                  View {article.state.abbreviation} Gap Analysis
                </Link>
                <Link
                  href={`/knowledge?state_id=${article.state.id}`}
                  className="block text-sm text-blue-600 hover:text-blue-800 dark:text-blue-400"
                >
                  All {article.state.abbreviation} Articles
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}
