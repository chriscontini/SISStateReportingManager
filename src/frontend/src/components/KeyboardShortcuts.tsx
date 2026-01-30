'use client';

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';

interface Shortcut {
  key: string;
  description: string;
  action: () => void;
  modifiers?: ('ctrl' | 'shift' | 'alt' | 'meta')[];
}

interface KeyboardShortcutsProviderProps {
  children: React.ReactNode;
}

// Global keyboard shortcuts
export function KeyboardShortcutsProvider({ children }: KeyboardShortcutsProviderProps) {
  const router = useRouter();
  const [showHelp, setShowHelp] = useState(false);

  const shortcuts: Shortcut[] = [
    { key: 'd', description: 'Go to Dashboard', action: () => router.push('/dashboard'), modifiers: ['alt'] },
    { key: 's', description: 'Go to States', action: () => router.push('/states'), modifiers: ['alt'] },
    { key: 'r', description: 'Go to Rankings', action: () => router.push('/rankings'), modifiers: ['alt'] },
    { key: 'c', description: 'Go to Compare', action: () => router.push('/compare'), modifiers: ['alt'] },
    { key: 'g', description: 'Go to Gap Analysis', action: () => router.push('/gap-analysis'), modifiers: ['alt'] },
    { key: 'm', description: 'Go to Roadmap', action: () => router.push('/roadmap'), modifiers: ['alt'] },
    { key: 'k', description: 'Go to Knowledge Base', action: () => router.push('/knowledge'), modifiers: ['alt'] },
    { key: 'a', description: 'Go to AI Chat', action: () => router.push('/chat'), modifiers: ['alt'] },
    { key: '?', description: 'Show keyboard shortcuts', action: () => setShowHelp(true), modifiers: ['shift'] },
  ];

  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    // Ignore if user is typing in an input
    if (
      event.target instanceof HTMLInputElement ||
      event.target instanceof HTMLTextAreaElement ||
      event.target instanceof HTMLSelectElement
    ) {
      return;
    }

    for (const shortcut of shortcuts) {
      const modifiersMatch = (shortcut.modifiers || []).every(mod => {
        switch (mod) {
          case 'ctrl': return event.ctrlKey;
          case 'shift': return event.shiftKey;
          case 'alt': return event.altKey;
          case 'meta': return event.metaKey;
          default: return false;
        }
      });

      if (modifiersMatch && event.key.toLowerCase() === shortcut.key.toLowerCase()) {
        event.preventDefault();
        shortcut.action();
        return;
      }
    }

    // Escape to close help modal
    if (event.key === 'Escape' && showHelp) {
      setShowHelp(false);
    }
  }, [shortcuts, showHelp]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  return (
    <>
      {children}
      {showHelp && (
        <KeyboardShortcutsModal
          shortcuts={shortcuts}
          onClose={() => setShowHelp(false)}
        />
      )}
    </>
  );
}

interface KeyboardShortcutsModalProps {
  shortcuts: Shortcut[];
  onClose: () => void;
}

function KeyboardShortcutsModal({ shortcuts, onClose }: KeyboardShortcutsModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white dark:bg-zinc-900 rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white">
            Keyboard Shortcuts
          </h2>
          <button
            onClick={onClose}
            className="text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="space-y-3">
          {shortcuts.map((shortcut, index) => (
            <div key={index} className="flex items-center justify-between">
              <span className="text-sm text-zinc-600 dark:text-zinc-400">
                {shortcut.description}
              </span>
              <kbd className="inline-flex items-center gap-1 px-2 py-1 text-xs font-mono bg-zinc-100 dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 rounded text-zinc-700 dark:text-zinc-300">
                {shortcut.modifiers?.map(mod => (
                  <span key={mod}>
                    {mod === 'alt' && '⌥'}
                    {mod === 'ctrl' && '⌃'}
                    {mod === 'shift' && '⇧'}
                    {mod === 'meta' && '⌘'}
                  </span>
                ))}
                <span>{shortcut.key.toUpperCase()}</span>
              </kbd>
            </div>
          ))}
        </div>

        <p className="mt-4 text-xs text-zinc-500 dark:text-zinc-500">
          Press <kbd className="px-1 py-0.5 bg-zinc-100 dark:bg-zinc-800 rounded">Esc</kbd> to close
        </p>
      </div>
    </div>
  );
}

// Hook for custom shortcuts in components
export function useKeyboardShortcut(
  key: string,
  callback: () => void,
  modifiers: ('ctrl' | 'shift' | 'alt' | 'meta')[] = []
) {
  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      // Ignore if user is typing in an input
      if (
        event.target instanceof HTMLInputElement ||
        event.target instanceof HTMLTextAreaElement ||
        event.target instanceof HTMLSelectElement
      ) {
        return;
      }

      const modifiersMatch = modifiers.every(mod => {
        switch (mod) {
          case 'ctrl': return event.ctrlKey;
          case 'shift': return event.shiftKey;
          case 'alt': return event.altKey;
          case 'meta': return event.metaKey;
          default: return false;
        }
      });

      if (modifiersMatch && event.key.toLowerCase() === key.toLowerCase()) {
        event.preventDefault();
        callback();
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [key, callback, modifiers]);
}
