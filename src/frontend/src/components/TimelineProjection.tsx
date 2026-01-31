'use client';

interface Phase {
  name: string;
  duration: number;
  color: string;
}

interface TimelineProjectionProps {
  projectedMonths: number;
  developmentHours: number;
  testingHours: number;
  certificationHours: number;
  stateName: string;
}

export default function TimelineProjection({
  projectedMonths,
  developmentHours,
  testingHours,
  certificationHours,
  stateName,
}: TimelineProjectionProps) {
  const totalHours = developmentHours + testingHours + certificationHours;

  // Calculate phase durations proportionally
  const researchMonths = Math.ceil(projectedMonths * 0.1);
  const developmentMonths = Math.ceil(projectedMonths * (developmentHours / totalHours) * 0.8);
  const testingMonths = Math.ceil(projectedMonths * (testingHours / totalHours) * 0.8);
  const certificationMonths = Math.ceil(projectedMonths * (certificationHours / totalHours) * 0.8);

  const phases: Phase[] = [
    { name: 'Research & Planning', duration: researchMonths, color: 'bg-blue-500' },
    { name: 'Development', duration: developmentMonths, color: 'bg-green-500' },
    { name: 'Testing & QA', duration: testingMonths, color: 'bg-yellow-500' },
    { name: 'Certification', duration: certificationMonths, color: 'bg-purple-500' },
  ];

  const totalDuration = phases.reduce((sum, phase) => sum + phase.duration, 0);

  // Calculate milestone dates (from now)
  const startDate = new Date();
  let cumulativeMonths = 0;

  const milestones = phases.map((phase, index) => {
    const date = new Date(startDate);
    date.setMonth(date.getMonth() + cumulativeMonths);
    cumulativeMonths += phase.duration;
    return {
      ...phase,
      startDate: date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' }),
      endMonth: cumulativeMonths,
    };
  });

  const endDate = new Date(startDate);
  endDate.setMonth(endDate.getMonth() + totalDuration);

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-2">
        Implementation Timeline: {stateName}
      </h3>
      <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-6">
        Estimated {projectedMonths} months to completion
        ({startDate.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })} - {endDate.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })})
      </p>

      {/* Timeline Bar */}
      <div className="relative">
        <div className="flex h-8 rounded-lg overflow-hidden">
          {phases.map((phase, index) => (
            <div
              key={phase.name}
              className={`${phase.color} flex items-center justify-center text-xs text-white font-medium`}
              style={{ width: `${(phase.duration / totalDuration) * 100}%` }}
            >
              {phase.duration >= 2 && `${phase.duration}mo`}
            </div>
          ))}
        </div>

        {/* Milestone Markers */}
        <div className="flex justify-between mt-2">
          <span className="text-xs text-zinc-500 dark:text-zinc-400">Start</span>
          <span className="text-xs text-zinc-500 dark:text-zinc-400">
            Month {totalDuration}
          </span>
        </div>
      </div>

      {/* Phase Details */}
      <div className="mt-6 space-y-3">
        {milestones.map((milestone, index) => (
          <div key={milestone.name} className="flex items-center gap-4">
            <div className={`w-3 h-3 rounded-full ${milestone.color}`}></div>
            <div className="flex-1">
              <div className="flex justify-between">
                <span className="text-sm font-medium text-zinc-900 dark:text-white">
                  {milestone.name}
                </span>
                <span className="text-sm text-zinc-500 dark:text-zinc-400">
                  {milestone.duration} months
                </span>
              </div>
              <div className="text-xs text-zinc-500 dark:text-zinc-400">
                {milestone.startDate} - Month {milestone.endMonth}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* LA Benchmark Comparison */}
      <div className="mt-6 p-4 bg-zinc-50 dark:bg-zinc-900/50 rounded-lg">
        <h4 className="text-sm font-medium text-zinc-900 dark:text-white mb-2">
          LA Expansion Benchmark
        </h4>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <span className="text-zinc-500 dark:text-zinc-400">LA Timeline:</span>
            <span className="ml-2 text-zinc-900 dark:text-white">30 months</span>
          </div>
          <div>
            <span className="text-zinc-500 dark:text-zinc-400">LA Effort:</span>
            <span className="ml-2 text-zinc-900 dark:text-white">15,000 hours</span>
          </div>
          <div>
            <span className="text-zinc-500 dark:text-zinc-400">This Project:</span>
            <span className="ml-2 text-zinc-900 dark:text-white">{projectedMonths} months</span>
          </div>
          <div>
            <span className="text-zinc-500 dark:text-zinc-400">This Effort:</span>
            <span className="ml-2 text-zinc-900 dark:text-white">{totalHours.toLocaleString()} hours</span>
          </div>
        </div>
        <div className="mt-2 text-xs text-zinc-600 dark:text-zinc-400">
          {projectedMonths < 30 ? (
            <span className="text-green-600 dark:text-green-400">
              {30 - projectedMonths} months faster than LA benchmark
            </span>
          ) : projectedMonths > 30 ? (
            <span className="text-yellow-600 dark:text-yellow-400">
              {projectedMonths - 30} months longer than LA benchmark
            </span>
          ) : (
            <span>Same timeline as LA benchmark</span>
          )}
        </div>
      </div>
    </div>
  );
}
