'use client';

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

interface Phase {
  id: number;
  name: string;
  phase_number: number;
  duration_months: number;
  effort_hours: number;
  fte_required: number;
  start_month: number;
  end_month: number;
}

interface ResourceAllocationProps {
  phases: Phase[];
  totalEffortHours: number;
  peakFTE: number;
  totalMonths: number;
}

// Skill requirements by phase
const PHASE_SKILLS: Record<string, string[]> = {
  'Discovery & Planning': [
    'Business Analyst',
    'Solution Architect',
    'Project Manager',
    'State Liaison',
  ],
  'Development - Core': [
    'Senior Backend Developer',
    'Database Engineer',
    'API Developer',
    'QA Engineer',
  ],
  'Development - Integration': [
    'Integration Specialist',
    'API Developer',
    'Security Engineer',
    'Technical Writer',
  ],
  'Testing & QA': [
    'QA Lead',
    'Test Automation Engineer',
    'Performance Tester',
    'UAT Coordinator',
  ],
  'Certification': [
    'Compliance Specialist',
    'Documentation Specialist',
    'QA Engineer',
    'State Liaison',
  ],
  'Pilot & Rollout': [
    'Implementation Specialist',
    'Trainer',
    'Support Engineer',
    'Customer Success Manager',
  ],
};

export default function ResourceAllocation({
  phases,
  totalEffortHours,
  peakFTE,
  totalMonths,
}: ResourceAllocationProps) {
  // Transform phases for chart
  const chartData = phases.map((phase) => ({
    name: phase.name.replace('Development - ', 'Dev: ').replace(' & ', '/'),
    FTE: phase.fte_required,
    hours: phase.effort_hours,
    months: phase.duration_months,
  }));

  // Calculate average FTE
  const avgFTE = phases.length > 0
    ? Math.round(phases.reduce((sum, p) => sum + p.fte_required * p.duration_months, 0) / totalMonths * 10) / 10
    : 0;

  // Calculate monthly breakdown
  const monthlyData = [];
  for (let month = 1; month <= totalMonths; month++) {
    const activePhases = phases.filter(
      (p) => month >= p.start_month && month <= p.end_month
    );
    const monthFTE = activePhases.reduce((sum, p) => sum + p.fte_required, 0);
    monthlyData.push({
      month: `M${month}`,
      FTE: monthFTE,
    });
  }

  return (
    <div className="space-y-6">
      {/* Summary Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
          <div className="text-sm text-blue-600 dark:text-blue-400">Total Effort</div>
          <div className="text-2xl font-bold text-blue-900 dark:text-blue-100">
            {totalEffortHours.toLocaleString()}
          </div>
          <div className="text-xs text-blue-600 dark:text-blue-400">hours</div>
        </div>
        <div className="bg-green-50 dark:bg-green-900/20 rounded-lg p-4">
          <div className="text-sm text-green-600 dark:text-green-400">Peak Team Size</div>
          <div className="text-2xl font-bold text-green-900 dark:text-green-100">
            {peakFTE}
          </div>
          <div className="text-xs text-green-600 dark:text-green-400">FTE</div>
        </div>
        <div className="bg-purple-50 dark:bg-purple-900/20 rounded-lg p-4">
          <div className="text-sm text-purple-600 dark:text-purple-400">Average Team</div>
          <div className="text-2xl font-bold text-purple-900 dark:text-purple-100">
            {avgFTE}
          </div>
          <div className="text-xs text-purple-600 dark:text-purple-400">FTE</div>
        </div>
        <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4">
          <div className="text-sm text-orange-600 dark:text-orange-400">Duration</div>
          <div className="text-2xl font-bold text-orange-900 dark:text-orange-100">
            {totalMonths}
          </div>
          <div className="text-xs text-orange-600 dark:text-orange-400">months</div>
        </div>
      </div>

      {/* FTE by Phase Chart */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
          Team Size by Phase
        </h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="name"
                tick={{ fontSize: 10 }}
                angle={-15}
                textAnchor="end"
                height={60}
              />
              <YAxis label={{ value: 'FTE', angle: -90, position: 'insideLeft' }} />
              <Tooltip
                content={({ active, payload }) => {
                  if (active && payload && payload.length) {
                    const data = payload[0].payload;
                    return (
                      <div className="bg-white dark:bg-zinc-800 p-2 border border-zinc-200 dark:border-zinc-600 rounded shadow">
                        <p className="font-semibold">{data.name}</p>
                        <p className="text-sm">FTE: {data.FTE}</p>
                        <p className="text-sm">Hours: {data.hours.toLocaleString()}</p>
                        <p className="text-sm">Duration: {data.months} months</p>
                      </div>
                    );
                  }
                  return null;
                }}
              />
              <Bar dataKey="FTE" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Monthly FTE Timeline */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
          Monthly Team Size
        </h3>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={monthlyData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" tick={{ fontSize: 10 }} />
              <YAxis label={{ value: 'FTE', angle: -90, position: 'insideLeft' }} />
              <Tooltip />
              <Bar dataKey="FTE" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Skill Requirements by Phase */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
        <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
          Skill Requirements by Phase
        </h3>
        <div className="space-y-4">
          {phases.map((phase) => {
            const skills = PHASE_SKILLS[phase.name] || ['General Staff'];
            return (
              <div key={phase.id} className="border-l-4 border-blue-500 pl-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-medium text-zinc-900 dark:text-white">
                      {phase.name}
                    </h4>
                    <p className="text-sm text-zinc-500 dark:text-zinc-400">
                      Months {phase.start_month}-{phase.end_month} ({phase.fte_required} FTE)
                    </p>
                  </div>
                  <span className="text-sm font-medium text-blue-600 dark:text-blue-400">
                    {phase.effort_hours.toLocaleString()} hours
                  </span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {skills.map((skill) => (
                    <span
                      key={skill}
                      className="px-2 py-1 text-xs bg-zinc-100 dark:bg-zinc-700 text-zinc-700 dark:text-zinc-300 rounded"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* LA Benchmark Comparison */}
      <div className="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
        <h3 className="text-lg font-semibold text-amber-900 dark:text-amber-100 mb-2">
          LA Benchmark Comparison
        </h3>
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <div className="text-amber-700 dark:text-amber-300">LA Effort</div>
            <div className="font-bold text-amber-900 dark:text-amber-100">15,000 hours</div>
          </div>
          <div>
            <div className="text-amber-700 dark:text-amber-300">LA Duration</div>
            <div className="font-bold text-amber-900 dark:text-amber-100">30 months</div>
          </div>
          <div>
            <div className="text-amber-700 dark:text-amber-300">LA Team</div>
            <div className="font-bold text-amber-900 dark:text-amber-100">5 FTE avg</div>
          </div>
        </div>
        <div className="mt-3 pt-3 border-t border-amber-200 dark:border-amber-800">
          <div className="text-sm text-amber-700 dark:text-amber-300">
            This roadmap is{' '}
            <span className="font-bold text-amber-900 dark:text-amber-100">
              {Math.round((totalEffortHours / 15000) * 100)}%
            </span>{' '}
            of LA effort and{' '}
            <span className="font-bold text-amber-900 dark:text-amber-100">
              {Math.round((totalMonths / 30) * 100)}%
            </span>{' '}
            of LA duration.
          </div>
        </div>
      </div>
    </div>
  );
}
