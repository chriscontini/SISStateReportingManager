'use client';

interface SkeletonProps {
  className?: string;
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
  animation?: 'pulse' | 'wave' | 'none';
}

export function Skeleton({
  className = '',
  variant = 'rectangular',
  width,
  height,
  animation = 'pulse',
}: SkeletonProps) {
  const baseClasses = 'bg-zinc-200 dark:bg-zinc-700';

  const animationClasses = {
    pulse: 'animate-pulse',
    wave: 'animate-shimmer',
    none: '',
  };

  const variantClasses = {
    text: 'rounded',
    circular: 'rounded-full',
    rectangular: 'rounded-md',
  };

  const style: React.CSSProperties = {};
  if (width) style.width = typeof width === 'number' ? `${width}px` : width;
  if (height) style.height = typeof height === 'number' ? `${height}px` : height;

  return (
    <div
      className={`${baseClasses} ${animationClasses[animation]} ${variantClasses[variant]} ${className}`}
      style={style}
    />
  );
}

// Pre-built skeleton components for common use cases

export function TableRowSkeleton({ columns = 5 }: { columns?: number }) {
  return (
    <tr className="border-b border-zinc-200 dark:border-zinc-700">
      {Array.from({ length: columns }).map((_, i) => (
        <td key={i} className="px-4 py-3">
          <Skeleton height={20} width={i === 0 ? '60%' : '80%'} />
        </td>
      ))}
    </tr>
  );
}

export function TableSkeleton({ rows = 5, columns = 5 }: { rows?: number; columns?: number }) {
  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow overflow-hidden">
      <div className="overflow-x-auto">
        <table className="min-w-full">
          <thead className="bg-zinc-50 dark:bg-zinc-900/50">
            <tr>
              {Array.from({ length: columns }).map((_, i) => (
                <th key={i} className="px-4 py-3">
                  <Skeleton height={16} width="70%" />
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {Array.from({ length: rows }).map((_, i) => (
              <TableRowSkeleton key={i} columns={columns} />
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export function CardSkeleton() {
  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
      <Skeleton height={24} width="50%" className="mb-4" />
      <Skeleton height={16} width="80%" className="mb-2" />
      <Skeleton height={16} width="60%" className="mb-4" />
      <div className="flex gap-2">
        <Skeleton height={32} width={80} />
        <Skeleton height={32} width={80} />
      </div>
    </div>
  );
}

export function StatCardSkeleton() {
  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
      <Skeleton height={14} width="40%" className="mb-2" />
      <Skeleton height={32} width="60%" className="mb-1" />
      <Skeleton height={12} width="50%" />
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-6">
      {/* Stats row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <StatCardSkeleton key={i} />
        ))}
      </div>

      {/* Main content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Chart area */}
        <div className="lg:col-span-2 bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
          <Skeleton height={24} width="40%" className="mb-6" />
          <Skeleton height={300} width="100%" />
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          <CardSkeleton />
          <CardSkeleton />
        </div>
      </div>
    </div>
  );
}

export function RankingsTableSkeleton() {
  return (
    <div className="space-y-4">
      {/* Header */}
      <div className="flex justify-between items-center">
        <Skeleton height={32} width={200} />
        <div className="flex gap-2">
          <Skeleton height={40} width={120} />
          <Skeleton height={40} width={150} />
        </div>
      </div>

      {/* Table */}
      <TableSkeleton rows={10} columns={6} />
    </div>
  );
}

export function RoadmapSkeleton() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
        <div className="flex justify-between items-start mb-6">
          <div>
            <Skeleton height={28} width={300} className="mb-2" />
            <Skeleton height={16} width={200} />
          </div>
          <Skeleton height={32} width={100} />
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i}>
              <Skeleton height={14} width="60%" className="mb-1" />
              <Skeleton height={28} width="80%" />
            </div>
          ))}
        </div>
      </div>

      {/* Gantt chart placeholder */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-6">
        <Skeleton height={24} width={150} className="mb-4" />
        <Skeleton height={200} width="100%" />
      </div>
    </div>
  );
}

export function ArticleCardSkeleton() {
  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
      <div className="flex justify-between items-start mb-3">
        <Skeleton height={20} width={80} />
        <Skeleton height={16} width={30} />
      </div>
      <Skeleton height={22} width="90%" className="mb-2" />
      <Skeleton height={22} width="60%" className="mb-3" />
      <div className="flex gap-1">
        <Skeleton height={20} width={50} />
        <Skeleton height={20} width={60} />
        <Skeleton height={20} width={40} />
      </div>
    </div>
  );
}

export function KnowledgeBaseSkeleton() {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <Skeleton height={36} width={200} className="mb-2" />
        <Skeleton height={20} width={350} />
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <StatCardSkeleton key={i} />
        ))}
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-zinc-800 rounded-lg shadow p-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i}>
              <Skeleton height={14} width={60} className="mb-1" />
              <Skeleton height={40} width="100%" />
            </div>
          ))}
        </div>
      </div>

      {/* Article grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {Array.from({ length: 6 }).map((_, i) => (
          <ArticleCardSkeleton key={i} />
        ))}
      </div>
    </div>
  );
}
