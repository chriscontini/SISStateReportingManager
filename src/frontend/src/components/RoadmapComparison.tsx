'use client';

import { useState, useEffect } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

interface Roadmap {
  id: number;
  state_id: number;
  name: string;
  total_months: number;
  total_effort_hours: number;
  peak_fte: number;
  baseline_state: string;
  start_date: string;
  end_date: string;
  status: string;
  state?: {
    id: number;
    name: string;
    abbreviation: string;
  };
}

interface Phase {
  id: number;
  name: string;
  phase_number: number;
  duration_months: number;
  effort_hours: number;
  fte_required: number;
}

interface RoadmapComparison {
  roadmap: Roadmap;
  phases: Phase[];
}

interface RoadmapComparisonProps {
  roadmaps: Roadmap[];
  onClose?: () => void;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function RoadmapComparison({
  roadmaps,
  onClose,
}: RoadmapComparisonProps) {
  const [selectedRoadmaps, setSelectedRoadmaps] = useState<number[]>(
    roadmaps.slice(0, 2).map((r) => r.id)
  );
  const [comparisonData, setComparisonData] = useState<RoadmapComparison[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedRoadmaps.length >= 2) {
      fetchComparisonData();
    }
  }, [selectedRoadmaps]);

  const fetchComparisonData = async () => {
    setLoading(true);
    try {
      const data: RoadmapComparison[] = [];
      for (const roadmapId of selectedRoadmaps) {
        const roadmap = roadmaps.find((r) => r.id === roadmapId);
        if (roadmap) {
          const res = await fetch(`${API_URL}/api/roadmaps/${roadmap.state_id}/phases`);
          if (res.ok) {
            const phases = await res.json();
            data.push({ roadmap, phases });
          }
        }
      }
      setComparisonData(data);
    } catch (error) {
      console.error('Error fetching comparison data:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleRoadmap = (id: number) => {
    if (selectedRoadmaps.includes(id)) {
      if (selectedRoadmaps.length > 2) {
        setSelectedRoadmaps(selectedRoadmaps.filter((r) => r !== id));
      }
    } else if (selectedRoadmaps.length < 4) {
      setSelectedRoadmaps([...selectedRoadmaps, id]);
    }
  };

  // Prepare chart data
  const timelineData = comparisonData.map((item, index) => ({
    name: item.roadmap.state?.abbreviation || item.roadmap.name,
    months: item.roadmap.total_months,
    fill: COLORS[index % COLORS.length],
  }));

  const effortData = comparisonData.map((item, index) => ({
    name: item.roadmap.state?.abbreviation || item.roadmap.name,
    hours: item.roadmap.total_effort_hours,
    fill: COLORS[index % COLORS.length],
  }));

  const fteData = comparisonData.map((item, index) => ({
    name: item.roadmap.state?.abbreviation || item.roadmap.name,
    peakFTE: item.roadmap.peak_fte,
    fill: COLORS[index % COLORS.length],
  }));

  // Phase comparison
  const phaseNames = ['Discovery & Planning', 'Development - Core', 'Development - Integration', 'Testing & QA', 'Certification', 'Pilot & Rollout'];
  const phaseComparisonData = phaseNames.map((phaseName) => {
    const entry: Record<string, number | string> = { phase: phaseName.replace('Development - ', '').replace(' & ', '/') };
    comparisonData.forEach((item) => {
      const phase = item.phases.find((p) => p.name === phaseName);
      const key = item.roadmap.state?.abbreviation || 'State';
      entry[key] = phase?.duration_months || 0;
    });
    return entry;
  });

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow-lg">
      <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-700 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
            Roadmap Comparison
          </h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            Compare implementation timelines across states
          </p>
        </div>
        {onClose && (
          <button
            onClick={onClose}
            className="text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        )}
      </div>

      <div className="p-6 space-y-6">
        {/* State Selection */}
        <div>
          <label className="block text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
            Select States to Compare (2-4)
          </label>
          <div className="flex flex-wrap gap-2">
            {roadmaps.map((roadmap) => (
              <button
                key={roadmap.id}
                onClick={() => toggleRoadmap(roadmap.id)}
                className={`px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                  selectedRoadmaps.includes(roadmap.id)
                    ? 'bg-blue-600 text-white'
                    : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-600'
                }`}
              >
                {roadmap.state?.abbreviation || roadmap.name}
              </button>
            ))}
          </div>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : comparisonData.length >= 2 ? (
          <>
            {/* Summary Table */}
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
                <thead>
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                      Metric
                    </th>
                    {comparisonData.map((item, index) => (
                      <th
                        key={item.roadmap.id}
                        className="px-4 py-3 text-left text-xs font-medium uppercase"
                        style={{ color: COLORS[index % COLORS.length] }}
                      >
                        {item.roadmap.state?.name || item.roadmap.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-500 dark:text-zinc-400">Timeline</td>
                    {comparisonData.map((item) => (
                      <td key={item.roadmap.id} className="px-4 py-3 text-sm font-medium text-zinc-900 dark:text-white">
                        {item.roadmap.total_months} months
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-500 dark:text-zinc-400">Total Effort</td>
                    {comparisonData.map((item) => (
                      <td key={item.roadmap.id} className="px-4 py-3 text-sm font-medium text-zinc-900 dark:text-white">
                        {item.roadmap.total_effort_hours.toLocaleString()} hours
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-500 dark:text-zinc-400">Peak FTE</td>
                    {comparisonData.map((item) => (
                      <td key={item.roadmap.id} className="px-4 py-3 text-sm font-medium text-zinc-900 dark:text-white">
                        {item.roadmap.peak_fte}
                      </td>
                    ))}
                  </tr>
                  <tr>
                    <td className="px-4 py-3 text-sm text-zinc-500 dark:text-zinc-400">Baseline</td>
                    {comparisonData.map((item) => (
                      <td key={item.roadmap.id} className="px-4 py-3 text-sm font-medium text-zinc-900 dark:text-white">
                        {item.roadmap.baseline_state}
                      </td>
                    ))}
                  </tr>
                </tbody>
              </table>
            </div>

            {/* Timeline Comparison Chart */}
            <div>
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3">
                Timeline Comparison
              </h3>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={timelineData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" unit=" mo" />
                    <YAxis type="category" dataKey="name" width={50} />
                    <Tooltip formatter={(value) => [`${value} months`, 'Timeline']} />
                    <Bar dataKey="months" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Effort Comparison Chart */}
            <div>
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3">
                Effort Comparison
              </h3>
              <div className="h-48">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={effortData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" />
                    <YAxis type="category" dataKey="name" width={50} />
                    <Tooltip formatter={(value) => [`${(value as number).toLocaleString()} hours`, 'Effort']} />
                    <Bar dataKey="hours" fill="#10b981" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Phase Duration Comparison */}
            <div>
              <h3 className="text-sm font-semibold text-zinc-900 dark:text-white mb-3">
                Phase Duration Comparison
              </h3>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={phaseComparisonData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="phase" tick={{ fontSize: 10 }} angle={-15} textAnchor="end" height={60} />
                    <YAxis label={{ value: 'Months', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    {comparisonData.map((item, index) => (
                      <Bar
                        key={item.roadmap.id}
                        dataKey={item.roadmap.state?.abbreviation || 'State'}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Recommendation */}
            {comparisonData.length > 0 && (
              <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-green-900 dark:text-green-100 mb-2">
                  Recommendation
                </h3>
                {(() => {
                  const sorted = [...comparisonData].sort(
                    (a, b) => a.roadmap.total_months - b.roadmap.total_months
                  );
                  const fastest = sorted[0];
                  return (
                    <p className="text-sm text-green-800 dark:text-green-200">
                      <strong>{fastest.roadmap.state?.name || fastest.roadmap.name}</strong> has the
                      shortest implementation timeline at{' '}
                      <strong>{fastest.roadmap.total_months} months</strong> with{' '}
                      <strong>{fastest.roadmap.total_effort_hours.toLocaleString()} hours</strong> of
                      total effort. This makes it the recommended first expansion target among the
                      compared states.
                    </p>
                  );
                })()}
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12 text-zinc-500 dark:text-zinc-400">
            Select at least 2 states to compare roadmaps.
          </div>
        )}
      </div>
    </div>
  );
}
