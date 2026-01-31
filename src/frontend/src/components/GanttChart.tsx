'use client';

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
}

interface Milestone {
  id: number;
  name: string;
  target_month: number;
  target_date: string | null;
  status: string;
  milestone_type: string;
}

interface GanttChartProps {
  phases: Phase[];
  milestones: Milestone[];
  totalMonths: number;
  onPhaseClick?: (phase: Phase) => void;
}

const PHASE_COLORS = [
  'bg-blue-500',
  'bg-green-500',
  'bg-purple-500',
  'bg-orange-500',
  'bg-pink-500',
  'bg-teal-500',
];

const STATUS_STYLES: Record<string, string> = {
  pending: 'opacity-60',
  in_progress: '',
  completed: 'opacity-90 border-2 border-green-600',
};

export default function GanttChart({
  phases,
  milestones,
  totalMonths,
  onPhaseClick,
}: GanttChartProps) {
  // Create month labels
  const months = Array.from({ length: totalMonths + 1 }, (_, i) => i);

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6 overflow-x-auto">
      {/* Timeline Header */}
      <div className="min-w-[800px]">
        <div className="flex border-b border-zinc-200 dark:border-zinc-700 pb-2 mb-4">
          <div className="w-48 flex-shrink-0 font-medium text-zinc-700 dark:text-zinc-300">
            Phase
          </div>
          <div className="flex-1 flex">
            {months.map((month) => (
              <div
                key={month}
                className="flex-1 text-center text-xs text-zinc-500 dark:text-zinc-400"
                style={{ minWidth: '40px' }}
              >
                {month % 3 === 0 ? `M${month}` : ''}
              </div>
            ))}
          </div>
        </div>

        {/* Phase Bars */}
        <div className="space-y-3">
          {phases.map((phase, index) => (
            <div key={phase.id} className="flex items-center group">
              <div
                className="w-48 flex-shrink-0 text-sm text-zinc-900 dark:text-white truncate pr-4 cursor-pointer hover:text-blue-600 dark:hover:text-blue-400"
                onClick={() => onPhaseClick?.(phase)}
                title={phase.name}
              >
                {phase.phase_number}. {phase.name}
              </div>
              <div className="flex-1 relative h-8">
                {/* Background grid */}
                <div className="absolute inset-0 flex">
                  {months.map((month) => (
                    <div
                      key={month}
                      className="flex-1 border-l border-zinc-100 dark:border-zinc-700"
                      style={{ minWidth: '40px' }}
                    />
                  ))}
                </div>

                {/* Phase bar */}
                <div
                  className={`absolute h-6 top-1 rounded-md ${PHASE_COLORS[index % PHASE_COLORS.length]} ${STATUS_STYLES[phase.status] || ''} cursor-pointer transition-transform hover:scale-y-110`}
                  style={{
                    left: `${(phase.start_month / totalMonths) * 100}%`,
                    width: `${(phase.duration_months / totalMonths) * 100}%`,
                    minWidth: '20px',
                  }}
                  onClick={() => onPhaseClick?.(phase)}
                  title={`${phase.name}: Month ${phase.start_month} - ${phase.end_month} (${phase.duration_months} months)`}
                >
                  {/* Progress overlay */}
                  {phase.progress_percent > 0 && (
                    <div
                      className="absolute inset-y-0 left-0 bg-black/20 rounded-l-md"
                      style={{ width: `${phase.progress_percent}%` }}
                    />
                  )}
                  <span className="absolute inset-0 flex items-center justify-center text-xs text-white font-medium">
                    {phase.duration_months}mo
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Milestones Row */}
        <div className="flex items-center mt-6 pt-4 border-t border-zinc-200 dark:border-zinc-700">
          <div className="w-48 flex-shrink-0 text-sm font-medium text-zinc-700 dark:text-zinc-300">
            Milestones
          </div>
          <div className="flex-1 relative h-8">
            {/* Background grid */}
            <div className="absolute inset-0 flex">
              {months.map((month) => (
                <div
                  key={month}
                  className="flex-1 border-l border-zinc-100 dark:border-zinc-700"
                  style={{ minWidth: '40px' }}
                />
              ))}
            </div>

            {/* Milestone markers */}
            {milestones.map((milestone) => (
              <div
                key={milestone.id}
                className={`absolute w-3 h-3 rounded-full transform -translate-x-1/2 top-2.5 ${
                  milestone.status === 'completed'
                    ? 'bg-green-500'
                    : milestone.status === 'missed'
                    ? 'bg-red-500'
                    : 'bg-yellow-500'
                } hover:scale-150 transition-transform cursor-pointer`}
                style={{
                  left: `${(milestone.target_month / totalMonths) * 100}%`,
                }}
                title={`${milestone.name} - Month ${milestone.target_month}`}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Legend */}
      <div className="mt-6 flex flex-wrap gap-4 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
          <span className="text-zinc-600 dark:text-zinc-400">Pending Milestone</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-green-500"></div>
          <span className="text-zinc-600 dark:text-zinc-400">Completed Milestone</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-red-500"></div>
          <span className="text-zinc-600 dark:text-zinc-400">Missed Milestone</span>
        </div>
      </div>
    </div>
  );
}
