import Link from "next/link";

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center py-12">
        <h1 className="text-4xl font-bold text-zinc-900 dark:text-white mb-4">
          SIS State Reporting Manager
        </h1>
        <p className="text-lg text-zinc-600 dark:text-zinc-400 max-w-2xl mx-auto">
          AI-powered state expansion planning tool for Student Information System
          vendors. Research, rank, and plan your expansion into new state markets.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
        <Link
          href="/states"
          className="group p-6 bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 hover:border-blue-500 dark:hover:border-blue-400 transition-colors"
        >
          <h2 className="text-2xl font-semibold text-zinc-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400">
            States
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400">
            Browse all 50 US states with their Department of Education websites
            and reporting requirements.
          </p>
        </Link>

        <Link
          href="/rankings"
          className="group p-6 bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 hover:border-blue-500 dark:hover:border-blue-400 transition-colors"
        >
          <h2 className="text-2xl font-semibold text-zinc-900 dark:text-white mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400">
            Rankings
          </h2>
          <p className="text-zinc-600 dark:text-zinc-400">
            View states ranked by expansion viability based on development effort,
            market opportunity, and technical fit.
          </p>
        </Link>
      </div>

      <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-6 max-w-4xl mx-auto">
        <h3 className="text-lg font-semibold text-blue-900 dark:text-blue-100 mb-2">
          About This Tool
        </h3>
        <p className="text-blue-800 dark:text-blue-200 text-sm">
          This application helps SIS vendors identify the best states for market
          expansion by analyzing reporting requirements, competitive landscape,
          and alignment with existing capabilities. Powered by AI research and
          analysis.
        </p>
      </div>
    </div>
  );
}
