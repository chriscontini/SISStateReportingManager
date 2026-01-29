'use client';

interface TierBadgeProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

/**
 * Calculates tier based on total weighted score.
 * Tier 1: > 70 (top candidates) - Green
 * Tier 2: 50-70 (potential) - Yellow
 * Tier 3: < 50 (low priority) - Red
 */
export function getTier(score: number): 1 | 2 | 3 {
  if (score > 70) return 1;
  if (score >= 50) return 2;
  return 3;
}

export function getTierLabel(tier: 1 | 2 | 3): string {
  switch (tier) {
    case 1:
      return 'Tier 1';
    case 2:
      return 'Tier 2';
    case 3:
      return 'Tier 3';
  }
}

export function getTierDescription(tier: 1 | 2 | 3): string {
  switch (tier) {
    case 1:
      return 'Top Candidate';
    case 2:
      return 'Potential';
    case 3:
      return 'Low Priority';
  }
}

export default function TierBadge({ score, size = 'md', showLabel = true }: TierBadgeProps) {
  const tier = getTier(score);

  const sizeClasses = {
    sm: 'text-xs px-2 py-0.5',
    md: 'text-sm px-2.5 py-1',
    lg: 'text-base px-3 py-1.5',
  };

  const colorClasses = {
    1: 'bg-green-100 text-green-800 border-green-200',
    2: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    3: 'bg-red-100 text-red-800 border-red-200',
  };

  return (
    <span
      className={`inline-flex items-center rounded-full font-medium border ${sizeClasses[size]} ${colorClasses[tier]}`}
      title={getTierDescription(tier)}
    >
      <span
        className={`w-2 h-2 rounded-full mr-1.5 ${
          tier === 1 ? 'bg-green-500' : tier === 2 ? 'bg-yellow-500' : 'bg-red-500'
        }`}
      />
      {showLabel ? getTierLabel(tier) : getTierDescription(tier)}
    </span>
  );
}
