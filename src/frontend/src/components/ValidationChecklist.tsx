'use client';

import { useState } from 'react';

interface ChecklistItem {
  id: string;
  category: string;
  title: string;
  description: string;
}

const CHECKLIST_ITEMS: ChecklistItem[] = [
  {
    id: 'rank-1',
    category: 'Ranking Methodology',
    title: 'All 9 ranking factors reviewed',
    description: 'Development Effort, District Structure, Avg District Size, Market Opportunity, Technical Fit, Certification, Competitive Landscape, Geographic Proximity, Hub Alignment',
  },
  {
    id: 'rank-2',
    category: 'Ranking Methodology',
    title: 'Factor weights validated',
    description: 'Development Effort weight (3.0) is primary; other weights reflect business priorities',
  },
  {
    id: 'rank-3',
    category: 'Ranking Methodology',
    title: 'LA benchmark confirmed',
    description: 'LA expansion success (6x ARPU, parish model) validates ranking model',
  },
  {
    id: 'gap-1',
    category: 'Gap Analysis',
    title: 'Baseline selection appropriate',
    description: 'NJ baseline for fragmented districts, LA baseline for county-based models',
  },
  {
    id: 'gap-2',
    category: 'Gap Analysis',
    title: 'State-specific requirements identified',
    description: 'PIMS (PA), PEIMS/TSDS (TX), MSDE (MD) gaps documented',
  },
  {
    id: 'gap-3',
    category: 'Gap Analysis',
    title: 'Critical gaps reviewed',
    description: 'All critical gaps have been reviewed for accuracy and completeness',
  },
  {
    id: 'effort-1',
    category: 'Effort Estimates',
    title: 'Effort estimates based on LA benchmark',
    description: 'LA: 30 months, 15,000 hours, 5 FTE serves as reference',
  },
  {
    id: 'effort-2',
    category: 'Effort Estimates',
    title: 'Complexity multipliers applied',
    description: 'Low (0.7x), Medium (1.0x), High (1.5x), Very High (2.0x)',
  },
  {
    id: 'effort-3',
    category: 'Effort Estimates',
    title: 'Buffer included in timeline',
    description: 'Projected timelines include contingency buffer',
  },
  {
    id: 'data-1',
    category: 'Data Quality',
    title: 'NCES data current',
    description: '2022-2023 NCES CCD data used for district/student counts',
  },
  {
    id: 'data-2',
    category: 'Data Quality',
    title: 'DOE websites verified',
    description: 'State DOE URLs and reporting system names are current',
  },
];

export default function ValidationChecklist() {
  const [checkedItems, setCheckedItems] = useState<Set<string>>(new Set());
  const [notes, setNotes] = useState<Record<string, string>>({});

  const toggleItem = (id: string) => {
    const newChecked = new Set(checkedItems);
    if (newChecked.has(id)) {
      newChecked.delete(id);
    } else {
      newChecked.add(id);
    }
    setCheckedItems(newChecked);
  };

  const updateNote = (id: string, note: string) => {
    setNotes({ ...notes, [id]: note });
  };

  const categories = [...new Set(CHECKLIST_ITEMS.map(item => item.category))];
  const progress = Math.round((checkedItems.size / CHECKLIST_ITEMS.length) * 100);

  const handleExport = () => {
    const exportData = CHECKLIST_ITEMS.map(item => ({
      category: item.category,
      item: item.title,
      completed: checkedItems.has(item.id) ? 'Yes' : 'No',
      notes: notes[item.id] || '',
    }));

    const headers = ['Category', 'Item', 'Completed', 'Notes'];
    const rows = exportData.map(row => [row.category, row.item, row.completed, row.notes]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => `"${cell.replace(/"/g, '""')}"`).join(',')),
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `validation_checklist_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  return (
    <div className="bg-white dark:bg-zinc-800 rounded-lg shadow">
      <div className="px-6 py-4 border-b border-zinc-200 dark:border-zinc-700 flex justify-between items-center">
        <div>
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
            Validation Checklist
          </h2>
          <p className="text-sm text-zinc-500 dark:text-zinc-400">
            Stakeholder review of rankings and gap analysis
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div className="w-32 bg-zinc-200 dark:bg-zinc-700 rounded-full h-2">
              <div
                className="bg-green-500 h-2 rounded-full transition-all"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <span className="text-sm font-medium text-zinc-900 dark:text-white">
              {progress}%
            </span>
          </div>
          <button
            onClick={handleExport}
            className="px-3 py-1.5 text-sm font-medium text-zinc-700 bg-white border border-zinc-300 rounded-md hover:bg-zinc-50 dark:bg-zinc-700 dark:text-zinc-300 dark:border-zinc-600 dark:hover:bg-zinc-600"
          >
            Export
          </button>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {categories.map(category => (
          <div key={category}>
            <h3 className="text-sm font-semibold text-zinc-900 dark:text-white uppercase tracking-wider mb-3">
              {category}
            </h3>
            <div className="space-y-3">
              {CHECKLIST_ITEMS.filter(item => item.category === category).map(item => (
                <div
                  key={item.id}
                  className={`p-4 rounded-lg border ${
                    checkedItems.has(item.id)
                      ? 'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800'
                      : 'bg-zinc-50 border-zinc-200 dark:bg-zinc-900/50 dark:border-zinc-700'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <input
                      type="checkbox"
                      id={item.id}
                      checked={checkedItems.has(item.id)}
                      onChange={() => toggleItem(item.id)}
                      className="mt-1 h-4 w-4 rounded border-zinc-300 text-green-600 focus:ring-green-500"
                    />
                    <div className="flex-1">
                      <label
                        htmlFor={item.id}
                        className={`font-medium ${
                          checkedItems.has(item.id)
                            ? 'text-green-800 dark:text-green-200'
                            : 'text-zinc-900 dark:text-white'
                        }`}
                      >
                        {item.title}
                      </label>
                      <p className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
                        {item.description}
                      </p>
                      <input
                        type="text"
                        placeholder="Add notes..."
                        value={notes[item.id] || ''}
                        onChange={(e) => updateNote(item.id, e.target.value)}
                        className="mt-2 w-full px-3 py-1.5 text-sm border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white placeholder-zinc-400"
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {progress === 100 && (
        <div className="px-6 py-4 bg-green-50 dark:bg-green-900/20 border-t border-green-200 dark:border-green-800">
          <p className="text-green-800 dark:text-green-200 font-medium text-center">
            All validation items completed! Ready for stakeholder sign-off.
          </p>
        </div>
      )}
    </div>
  );
}
