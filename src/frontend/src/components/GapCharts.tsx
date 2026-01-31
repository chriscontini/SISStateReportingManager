'use client';

import dynamic from 'next/dynamic';

// Dynamically import Recharts to avoid SSR issues
const PieChart = dynamic(
  () => import('recharts').then((mod) => mod.PieChart),
  { ssr: false }
);
const Pie = dynamic(
  () => import('recharts').then((mod) => mod.Pie),
  { ssr: false }
);
const Cell = dynamic(
  () => import('recharts').then((mod) => mod.Cell),
  { ssr: false }
);
const BarChart = dynamic(
  () => import('recharts').then((mod) => mod.BarChart),
  { ssr: false }
);
const Bar = dynamic(
  () => import('recharts').then((mod) => mod.Bar),
  { ssr: false }
);
const XAxis = dynamic(
  () => import('recharts').then((mod) => mod.XAxis),
  { ssr: false }
);
const YAxis = dynamic(
  () => import('recharts').then((mod) => mod.YAxis),
  { ssr: false }
);
const Tooltip = dynamic(
  () => import('recharts').then((mod) => mod.Tooltip),
  { ssr: false }
);
const ResponsiveContainer = dynamic(
  () => import('recharts').then((mod) => mod.ResponsiveContainer),
  { ssr: false }
);
const Legend = dynamic(
  () => import('recharts').then((mod) => mod.Legend),
  { ssr: false }
);

interface Gap {
  category: string;
  severity: string;
  effort_hours: number;
}

interface GapChartProps {
  gaps: Gap[];
}

const CATEGORY_COLORS: Record<string, string> = {
  enrollment: '#3B82F6',    // blue
  attendance: '#10B981',    // green
  grades: '#8B5CF6',        // purple
  special_ed: '#F59E0B',    // amber
  assessments: '#EF4444',   // red
  staff: '#6366F1',         // indigo
  discipline: '#EC4899',    // pink
  ell: '#14B8A6',           // teal
  cte: '#F97316',           // orange
  reporting: '#84CC16',     // lime
  integration: '#06B6D4',   // cyan
  certification: '#A855F7', // purple
  early_childhood: '#22C55E', // green
};

const SEVERITY_COLORS: Record<string, string> = {
  critical: '#EF4444',  // red
  major: '#F59E0B',     // amber
  minor: '#22C55E',     // green
};

export function GapCategoryChart({ gaps }: GapChartProps) {
  // Group gaps by category
  const categoryData = gaps.reduce((acc, gap) => {
    const existing = acc.find(item => item.name === gap.category);
    if (existing) {
      existing.value++;
      existing.effort += gap.effort_hours;
    } else {
      acc.push({
        name: gap.category,
        value: 1,
        effort: gap.effort_hours,
        color: CATEGORY_COLORS[gap.category] || '#6B7280',
      });
    }
    return acc;
  }, [] as { name: string; value: number; effort: number; color: string }[]);

  // Sort by value
  categoryData.sort((a, b) => b.value - a.value);

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
        Gaps by Category
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={categoryData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={100}
            label={({ name, value }) => `${name}: ${value}`}
            labelLine={false}
          >
            {categoryData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            formatter={(value, name, props) => [
              `${value} gaps (${props.payload.effort.toLocaleString()} hrs)`,
              name
            ]}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function GapSeverityChart({ gaps }: GapChartProps) {
  // Group gaps by severity
  const severityData = gaps.reduce((acc, gap) => {
    const existing = acc.find(item => item.name === gap.severity);
    if (existing) {
      existing.value++;
      existing.effort += gap.effort_hours;
    } else {
      acc.push({
        name: gap.severity,
        value: 1,
        effort: gap.effort_hours,
        color: SEVERITY_COLORS[gap.severity] || '#6B7280',
      });
    }
    return acc;
  }, [] as { name: string; value: number; effort: number; color: string }[]);

  // Sort by severity level
  const severityOrder = { critical: 0, major: 1, minor: 2 };
  severityData.sort((a, b) =>
    (severityOrder[a.name as keyof typeof severityOrder] || 3) -
    (severityOrder[b.name as keyof typeof severityOrder] || 3)
  );

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
        Gaps by Severity
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={severityData} layout="vertical">
          <XAxis type="number" />
          <YAxis dataKey="name" type="category" width={80} />
          <Tooltip
            formatter={(value, name, props) => [
              `${value} gaps (${props.payload.effort.toLocaleString()} hrs)`,
              'Count'
            ]}
          />
          <Bar dataKey="value" name="Gaps">
            {severityData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function GapEffortByCategory({ gaps }: GapChartProps) {
  // Group effort by category
  const categoryData = gaps.reduce((acc, gap) => {
    const existing = acc.find(item => item.category === gap.category);
    if (existing) {
      existing.hours += gap.effort_hours;
      existing.count++;
    } else {
      acc.push({
        category: gap.category,
        hours: gap.effort_hours,
        count: 1,
      });
    }
    return acc;
  }, [] as { category: string; hours: number; count: number }[]);

  // Sort by hours
  categoryData.sort((a, b) => b.hours - a.hours);

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
        Effort by Category
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={categoryData}>
          <XAxis
            dataKey="category"
            tick={{ fontSize: 10 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis />
          <Tooltip
            formatter={(value) => [`${value.toLocaleString()} hours`, 'Effort']}
          />
          <Bar dataKey="hours" fill="#3B82F6" name="Hours" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

interface StateComparisonData {
  state: string;
  totalEffort: number;
  criticalGaps: number;
  totalGaps: number;
}

interface StateComparisonChartProps {
  data: StateComparisonData[];
}

export function StateComparisonChart({ data }: StateComparisonChartProps) {
  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
        State Comparison
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <XAxis dataKey="state" />
          <YAxis yAxisId="left" orientation="left" stroke="#3B82F6" />
          <YAxis yAxisId="right" orientation="right" stroke="#EF4444" />
          <Tooltip />
          <Legend />
          <Bar yAxisId="left" dataKey="totalEffort" fill="#3B82F6" name="Effort (hrs)" />
          <Bar yAxisId="right" dataKey="criticalGaps" fill="#EF4444" name="Critical Gaps" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
