'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import dynamic from 'next/dynamic';
import GanttChart from '@/components/GanttChart';

const ResourceAllocation = dynamic(() => import('@/components/ResourceAllocation'), { ssr: false });
const RoadmapComparison = dynamic(() => import('@/components/RoadmapComparison'), { ssr: false });

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface Phase {
  id: number;
  phase_number: number;
  name: string;
  description: string | null;
  start_month: number;
  duration_months: number;
  end_month: number;
  effort_hours: number;
  fte_required: number;
  status: string;
  progress_percent: number;
  deliverables: string | null;
}

interface Milestone {
  id: number;
  name: string;
  description: string | null;
  milestone_type: string;
  target_month: number;
  target_date: string | null;
  status: string;
}

interface Roadmap {
  id: number;
  state_id: number;
  name: string;
  description: string | null;
  status: string;
  start_date: string | null;
  end_date: string | null;
  total_months: number;
  total_effort_hours: number;
  peak_fte: number;
  baseline_state: string;
  phases: Phase[];
  milestones: Milestone[];
}

interface RoadmapSummary {
  id: number;
  state_id: number;
  state_name: string;
  state_abbreviation: string;
  name: string;
  status: string;
  total_months: number;
  total_effort_hours: number;
  progress_percent: number;
}

interface State {
  id: number;
  name: string;
  abbreviation: string;
}

function StatusBadge({ status }: { status: string }) {
  const colors: Record<string, string> = {
    draft: 'bg-zinc-100 text-zinc-800 dark:bg-zinc-700 dark:text-zinc-300',
    active: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    completed: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
    on_hold: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
  };

  return (
    <span className={`px-2 py-1 text-xs font-medium rounded capitalize ${colors[status] || 'bg-zinc-100 text-zinc-800'}`}>
      {status.replace('_', ' ')}
    </span>
  );
}

type TabType = 'timeline' | 'resources' | 'comparison';

export default function RoadmapPage() {
  const [roadmaps, setRoadmaps] = useState<RoadmapSummary[]>([]);
  const [selectedRoadmap, setSelectedRoadmap] = useState<Roadmap | null>(null);
  const [selectedPhase, setSelectedPhase] = useState<Phase | null>(null);
  const [states, setStates] = useState<State[]>([]);
  const [selectedStateId, setSelectedStateId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<TabType>('timeline');
  const [roadmapsForComparison, setRoadmapsForComparison] = useState<Array<{id: number; state_id: number; name: string; total_months: number; total_effort_hours: number; peak_fte: number; baseline_state: string; start_date: string; end_date: string; status: string; state?: {id: number; name: string; abbreviation: string}}>>([]);

  // Fetch available roadmaps
  useEffect(() => {
    async function fetchData() {
      try {
        const token = localStorage.getItem('auth_token');

        // Fetch states
        const statesRes = await fetch(`${API_URL}/api/states`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (statesRes.ok) {
          setStates(await statesRes.json());
        }

        // Fetch roadmaps
        const roadmapsRes = await fetch(`${API_URL}/api/roadmaps/`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (roadmapsRes.ok) {
          const data = await roadmapsRes.json();
          setRoadmaps(data);
          if (data.length > 0) {
            setSelectedStateId(data[0].state_id);
          }

          // Fetch full roadmap data for comparison
          const fullRoadmaps = [];
          for (const summary of data) {
            try {
              const fullRes = await fetch(`${API_URL}/api/roadmaps/${summary.state_id}`, {
                headers: { Authorization: `Bearer ${token}` },
              });
              if (fullRes.ok) {
                const fullData = await fullRes.json();
                fullRoadmaps.push({
                  id: fullData.id,
                  state_id: fullData.state_id,
                  name: fullData.name,
                  total_months: fullData.total_months,
                  total_effort_hours: fullData.total_effort_hours,
                  peak_fte: fullData.peak_fte,
                  baseline_state: fullData.baseline_state,
                  start_date: fullData.start_date,
                  end_date: fullData.end_date,
                  status: fullData.status,
                  state: {
                    id: summary.state_id,
                    name: summary.state_name,
                    abbreviation: summary.state_abbreviation,
                  },
                });
              }
            } catch {
              // Skip failed fetches
            }
          }
          setRoadmapsForComparison(fullRoadmaps);
        }
      } catch {
        setError('Failed to connect to API');
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, []);

  // Fetch selected roadmap details
  useEffect(() => {
    if (!selectedStateId) return;

    async function fetchRoadmap() {
      try {
        const token = localStorage.getItem('auth_token');
        const res = await fetch(`${API_URL}/api/roadmaps/${selectedStateId}`, {
          headers: { Authorization: `Bearer ${token}` },
        });

        if (res.ok) {
          setSelectedRoadmap(await res.json());
          setError(null);
        } else if (res.status === 404) {
          setSelectedRoadmap(null);
        }
      } catch {
        setError('Failed to fetch roadmap');
      }
    }

    fetchRoadmap();
  }, [selectedStateId]);

  const generateRoadmap = async () => {
    if (!selectedStateId) return;

    setGenerating(true);
    try {
      const token = localStorage.getItem('auth_token');
      const res = await fetch(`${API_URL}/api/roadmaps/${selectedStateId}/generate`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ force_regenerate: true }),
      });

      if (res.ok) {
        const data = await res.json();
        setSelectedRoadmap(data);

        // Refresh roadmaps list
        const listRes = await fetch(`${API_URL}/api/roadmaps/`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (listRes.ok) {
          setRoadmaps(await listRes.json());
        }
      } else {
        const err = await res.json();
        alert(err.detail || 'Failed to generate roadmap');
      }
    } catch {
      alert('Failed to generate roadmap');
    } finally {
      setGenerating(false);
    }
  };

  const handleExportCSV = () => {
    if (!selectedRoadmap) return;

    const headers = ['Phase', 'Start Month', 'Duration', 'End Month', 'Effort (hrs)', 'FTE', 'Status'];
    const rows = selectedRoadmap.phases.map(p => [
      p.name,
      p.start_month,
      p.duration_months,
      p.end_month,
      p.effort_hours,
      p.fte_required,
      p.status,
    ]);

    const csvContent = [
      `# ${selectedRoadmap.name}`,
      `# Total: ${selectedRoadmap.total_months} months, ${selectedRoadmap.total_effort_hours} hours`,
      '',
      headers.join(','),
      ...rows.map(row => row.join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `roadmap_${selectedRoadmap.name.replace(/\s+/g, '_')}.csv`;
    link.click();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-white">
            Implementation Roadmaps
          </h1>
          <p className="text-zinc-600 dark:text-zinc-400">
            Phased implementation plans for state expansions
          </p>
        </div>
        <div className="flex items-center gap-4">
          <select
            value={selectedStateId || ''}
            onChange={(e) => setSelectedStateId(Number(e.target.value))}
            className="px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
          >
            <option value="">Select a state...</option>
            {states.map((state) => (
              <option key={state.id} value={state.id}>
                {state.name} ({state.abbreviation})
              </option>
            ))}
          </select>
          <button
            onClick={generateRoadmap}
            disabled={!selectedStateId || generating}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {generating ? 'Generating...' : 'Generate Roadmap'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-800 rounded-lg p-4 dark:bg-red-900/20 dark:border-red-800 dark:text-red-400">
          {error}
        </div>
      )}

      {selectedRoadmap ? (
        <div className="space-y-6">
          {/* Roadmap Header */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-xl font-semibold text-zinc-900 dark:text-white">
                  {selectedRoadmap.name}
                </h2>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-1">
                  {selectedRoadmap.description}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <StatusBadge status={selectedRoadmap.status} />
                <button
                  onClick={handleExportCSV}
                  className="px-3 py-1.5 text-sm font-medium text-zinc-700 bg-white border border-zinc-300 rounded-md hover:bg-zinc-50 dark:bg-zinc-700 dark:text-zinc-300 dark:border-zinc-600 dark:hover:bg-zinc-600"
                >
                  Export CSV
                </button>
              </div>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mt-6">
              <div>
                <div className="text-sm text-zinc-500 dark:text-zinc-400">Timeline</div>
                <div className="text-xl font-bold text-zinc-900 dark:text-white">
                  {selectedRoadmap.total_months} months
                </div>
              </div>
              <div>
                <div className="text-sm text-zinc-500 dark:text-zinc-400">Total Effort</div>
                <div className="text-xl font-bold text-zinc-900 dark:text-white">
                  {selectedRoadmap.total_effort_hours.toLocaleString()} hrs
                </div>
              </div>
              <div>
                <div className="text-sm text-zinc-500 dark:text-zinc-400">Peak FTE</div>
                <div className="text-xl font-bold text-zinc-900 dark:text-white">
                  {selectedRoadmap.peak_fte}
                </div>
              </div>
              <div>
                <div className="text-sm text-zinc-500 dark:text-zinc-400">Start Date</div>
                <div className="text-lg font-semibold text-zinc-900 dark:text-white">
                  {selectedRoadmap.start_date || 'TBD'}
                </div>
              </div>
              <div>
                <div className="text-sm text-zinc-500 dark:text-zinc-400">End Date</div>
                <div className="text-lg font-semibold text-zinc-900 dark:text-white">
                  {selectedRoadmap.end_date || 'TBD'}
                </div>
              </div>
            </div>

            {/* Tab Navigation */}
            <div className="flex border-b border-zinc-200 dark:border-zinc-700 mt-6">
              <button
                onClick={() => setActiveTab('timeline')}
                className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px ${
                  activeTab === 'timeline'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-300'
                }`}
              >
                Timeline
              </button>
              <button
                onClick={() => setActiveTab('resources')}
                className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px ${
                  activeTab === 'resources'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-300'
                }`}
              >
                Resources
              </button>
              {roadmapsForComparison.length >= 2 && (
                <button
                  onClick={() => setActiveTab('comparison')}
                  className={`px-4 py-2 text-sm font-medium border-b-2 -mb-px ${
                    activeTab === 'comparison'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-300'
                  }`}
                >
                  Compare States
                </button>
              )}
            </div>
          </div>

          {/* Tab Content */}
          {activeTab === 'timeline' && (
            <>
              {/* Gantt Chart */}
              <GanttChart
                phases={selectedRoadmap.phases}
                milestones={selectedRoadmap.milestones}
                totalMonths={selectedRoadmap.total_months}
                onPhaseClick={setSelectedPhase}
              />

          {/* Phase Details Panel */}
          {selectedPhase && (
            <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
              <div className="flex justify-between items-start">
                <h3 className="text-lg font-semibold text-zinc-900 dark:text-white">
                  Phase {selectedPhase.phase_number}: {selectedPhase.name}
                </h3>
                <button
                  onClick={() => setSelectedPhase(null)}
                  className="text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-300"
                >
                  Close
                </button>
              </div>
              <p className="text-sm text-zinc-600 dark:text-zinc-400 mt-2">
                {selectedPhase.description}
              </p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                <div>
                  <div className="text-sm text-zinc-500 dark:text-zinc-400">Duration</div>
                  <div className="font-semibold text-zinc-900 dark:text-white">
                    {selectedPhase.duration_months} months
                  </div>
                </div>
                <div>
                  <div className="text-sm text-zinc-500 dark:text-zinc-400">Period</div>
                  <div className="font-semibold text-zinc-900 dark:text-white">
                    Month {selectedPhase.start_month} - {selectedPhase.end_month}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-zinc-500 dark:text-zinc-400">Effort</div>
                  <div className="font-semibold text-zinc-900 dark:text-white">
                    {selectedPhase.effort_hours.toLocaleString()} hrs
                  </div>
                </div>
                <div>
                  <div className="text-sm text-zinc-500 dark:text-zinc-400">FTE Required</div>
                  <div className="font-semibold text-zinc-900 dark:text-white">
                    {selectedPhase.fte_required}
                  </div>
                </div>
              </div>

              {selectedPhase.deliverables && (
                <div className="mt-4">
                  <div className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">
                    Deliverables
                  </div>
                  <div className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                    {selectedPhase.deliverables}
                  </div>
                </div>
              )}
            </div>
          )}

              {/* Milestones List */}
              <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
                <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
                  Milestones ({selectedRoadmap.milestones.length})
                </h3>
                <div className="space-y-3">
                  {selectedRoadmap.milestones.map((milestone) => (
                    <div
                      key={milestone.id}
                      className="flex items-center justify-between p-3 bg-zinc-50 dark:bg-zinc-900/50 rounded-lg"
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-3 h-3 rounded-full ${
                          milestone.status === 'completed' ? 'bg-green-500' :
                          milestone.status === 'missed' ? 'bg-red-500' : 'bg-yellow-500'
                        }`}></div>
                        <div>
                          <div className="font-medium text-zinc-900 dark:text-white">
                            {milestone.name}
                          </div>
                          <div className="text-xs text-zinc-500 dark:text-zinc-400">
                            {milestone.milestone_type} • Month {milestone.target_month}
                          </div>
                        </div>
                      </div>
                      <div className="text-sm text-zinc-600 dark:text-zinc-400">
                        {milestone.target_date}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}

          {/* Resources Tab */}
          {activeTab === 'resources' && (
            <ResourceAllocation
              phases={selectedRoadmap.phases}
              totalEffortHours={selectedRoadmap.total_effort_hours}
              peakFTE={selectedRoadmap.peak_fte}
              totalMonths={selectedRoadmap.total_months}
            />
          )}

          {/* Comparison Tab */}
          {activeTab === 'comparison' && roadmapsForComparison.length >= 2 && (
            <RoadmapComparison
              roadmaps={roadmapsForComparison}
              onClose={() => setActiveTab('timeline')}
            />
          )}
        </div>
      ) : selectedStateId ? (
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-8 text-center">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">
            No Roadmap Found
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400 mb-6">
            Generate a roadmap to see the implementation plan for this state.
          </p>
          <button
            onClick={generateRoadmap}
            disabled={generating}
            className="px-6 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {generating ? 'Generating...' : 'Generate Roadmap'}
          </button>
        </div>
      ) : (
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-8 text-center">
          <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">
            Select a State
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400">
            Choose a state from the dropdown to view or generate its implementation roadmap.
          </p>
        </div>
      )}

      {/* Roadmaps Summary Table */}
      {roadmaps.length > 0 && (
        <div className="bg-white dark:bg-zinc-800 rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-700">
            <h3 className="text-lg font-semibold text-zinc-900 dark:text-white">
              All Roadmaps
            </h3>
          </div>
          <table className="min-w-full divide-y divide-zinc-200 dark:divide-zinc-700">
            <thead className="bg-zinc-50 dark:bg-zinc-900/50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  State
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Timeline
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Effort
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Progress
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-zinc-500 dark:text-zinc-400 uppercase">
                  Status
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-200 dark:divide-zinc-700">
              {roadmaps.map((roadmap) => (
                <tr
                  key={roadmap.id}
                  className={`cursor-pointer hover:bg-zinc-50 dark:hover:bg-zinc-700/50 ${
                    selectedStateId === roadmap.state_id ? 'bg-blue-50 dark:bg-blue-900/20' : ''
                  }`}
                  onClick={() => setSelectedStateId(roadmap.state_id)}
                >
                  <td className="px-6 py-4 text-sm font-medium text-zinc-900 dark:text-white">
                    {roadmap.state_name} ({roadmap.state_abbreviation})
                  </td>
                  <td className="px-6 py-4 text-sm text-zinc-600 dark:text-zinc-400">
                    {roadmap.total_months} months
                  </td>
                  <td className="px-6 py-4 text-sm text-zinc-600 dark:text-zinc-400">
                    {roadmap.total_effort_hours.toLocaleString()} hrs
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
                        <div
                          className="bg-green-500 h-2 rounded-full"
                          style={{ width: `${roadmap.progress_percent}%` }}
                        />
                      </div>
                      <span className="text-xs text-zinc-600 dark:text-zinc-400">
                        {roadmap.progress_percent}%
                      </span>
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <StatusBadge status={roadmap.status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
