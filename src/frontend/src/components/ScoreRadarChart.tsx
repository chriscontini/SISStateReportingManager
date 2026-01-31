'use client';

import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';

interface ScoreData {
  factor_name: string;
  score: number;
}

interface StateScores {
  name: string;
  abbreviation: string;
  scores: ScoreData[];
  color?: string;
}

interface ScoreRadarChartProps {
  states: StateScores[];
  width?: number;
  height?: number;
}

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export default function ScoreRadarChart({ states, width = 400, height = 400 }: ScoreRadarChartProps) {
  if (!states || states.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-zinc-500">
        No score data available
      </div>
    );
  }

  // Get all unique factor names
  const factorNames = new Set<string>();
  states.forEach(state => {
    state.scores.forEach(score => factorNames.add(score.factor_name));
  });

  // Transform data for Recharts
  const chartData = Array.from(factorNames).map(factorName => {
    const dataPoint: Record<string, string | number> = {
      factor: factorName,
      // Abbreviate long factor names
      factorShort: factorName.length > 15 ? factorName.slice(0, 12) + '...' : factorName,
    };

    states.forEach((state, index) => {
      const scoreData = state.scores.find(s => s.factor_name === factorName);
      dataPoint[state.abbreviation] = scoreData?.score || 0;
    });

    return dataPoint;
  });

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RadarChart data={chartData} cx="50%" cy="50%" outerRadius="80%">
        <PolarGrid stroke="#e5e7eb" />
        <PolarAngleAxis
          dataKey="factorShort"
          tick={{ fill: '#6b7280', fontSize: 11 }}
          tickLine={false}
        />
        <PolarRadiusAxis
          angle={30}
          domain={[0, 10]}
          tick={{ fill: '#9ca3af', fontSize: 10 }}
          tickCount={6}
        />

        {states.map((state, index) => (
          <Radar
            key={state.abbreviation}
            name={state.name}
            dataKey={state.abbreviation}
            stroke={state.color || COLORS[index % COLORS.length]}
            fill={state.color || COLORS[index % COLORS.length]}
            fillOpacity={0.2}
            strokeWidth={2}
          />
        ))}

        <Tooltip
          contentStyle={{
            backgroundColor: '#1f2937',
            border: 'none',
            borderRadius: '8px',
            color: '#fff',
          }}
          formatter={(value: number, name: string) => [
            `${value.toFixed(1)} / 10`,
            name,
          ]}
          labelFormatter={(label) => {
            // Find full factor name from abbreviated
            const fullData = chartData.find(d => d.factorShort === label);
            return fullData?.factor || label;
          }}
        />

        {states.length > 1 && (
          <Legend
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
        )}
      </RadarChart>
    </ResponsiveContainer>
  );
}
