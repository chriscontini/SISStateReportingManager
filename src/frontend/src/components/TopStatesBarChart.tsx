'use client';

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts';
import { getTier } from './TierBadge';

interface RankedState {
  name: string;
  abbreviation: string;
  total_score: number;
}

interface TopStatesBarChartProps {
  states: RankedState[];
  maxStates?: number;
  height?: number;
}

const TIER_COLORS = {
  1: '#22c55e', // green
  2: '#eab308', // yellow
  3: '#ef4444', // red
};

export default function TopStatesBarChart({
  states,
  maxStates = 10,
  height = 400,
}: TopStatesBarChartProps) {
  if (!states || states.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-zinc-500">
        No ranking data available
      </div>
    );
  }

  // Take top N states and reverse for horizontal bar display
  const chartData = states
    .slice(0, maxStates)
    .map((state, index) => ({
      name: state.name,
      abbreviation: state.abbreviation,
      score: state.total_score,
      rank: index + 1,
      tier: getTier(state.total_score),
    }))
    .reverse(); // Reverse so #1 appears at top

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart
        data={chartData}
        layout="vertical"
        margin={{ top: 10, right: 30, left: 20, bottom: 10 }}
      >
        <XAxis
          type="number"
          domain={[0, 'dataMax']}
          tick={{ fill: '#6b7280', fontSize: 12 }}
          tickLine={false}
          axisLine={{ stroke: '#e5e7eb' }}
        />
        <YAxis
          type="category"
          dataKey="abbreviation"
          width={40}
          tick={{ fill: '#374151', fontSize: 12, fontWeight: 500 }}
          tickLine={false}
          axisLine={false}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: '#1f2937',
            border: 'none',
            borderRadius: '8px',
            color: '#fff',
          }}
          formatter={(value: number) => [`${value.toFixed(2)}`, 'Score']}
          labelFormatter={(label) => {
            const state = chartData.find(s => s.abbreviation === label);
            return state ? `#${state.rank} ${state.name}` : label;
          }}
        />
        <Bar dataKey="score" radius={[0, 4, 4, 0]} barSize={24}>
          {chartData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={TIER_COLORS[entry.tier]}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
}
