'use client';

import { useState, useEffect, useCallback } from 'react';

interface TourStep {
  target: string; // CSS selector
  title: string;
  content: string;
  placement?: 'top' | 'bottom' | 'left' | 'right';
}

interface OnboardingTourProps {
  steps: TourStep[];
  onComplete: () => void;
  storageKey?: string;
}

export default function OnboardingTour({
  steps,
  onComplete,
  storageKey = 'onboarding_completed',
}: OnboardingTourProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [isVisible, setIsVisible] = useState(false);
  const [targetRect, setTargetRect] = useState<DOMRect | null>(null);

  useEffect(() => {
    // Check if tour was already completed
    const completed = localStorage.getItem(storageKey);
    if (completed === 'true') {
      return;
    }
    setIsVisible(true);
  }, [storageKey]);

  useEffect(() => {
    if (!isVisible || currentStep >= steps.length) return;

    const step = steps[currentStep];
    const element = document.querySelector(step.target);

    if (element) {
      const rect = element.getBoundingClientRect();
      setTargetRect(rect);
      element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [currentStep, steps, isVisible]);

  const handleNext = useCallback(() => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      handleComplete();
    }
  }, [currentStep, steps.length]);

  const handlePrevious = useCallback(() => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  }, [currentStep]);

  const handleComplete = useCallback(() => {
    localStorage.setItem(storageKey, 'true');
    setIsVisible(false);
    onComplete();
  }, [storageKey, onComplete]);

  const handleSkip = useCallback(() => {
    handleComplete();
  }, [handleComplete]);

  if (!isVisible || currentStep >= steps.length) {
    return null;
  }

  const step = steps[currentStep];
  const placement = step.placement || 'bottom';

  // Calculate tooltip position
  const getTooltipStyle = (): React.CSSProperties => {
    if (!targetRect) {
      return {
        position: 'fixed',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)',
      };
    }

    const padding = 16;
    const tooltipWidth = 320;

    switch (placement) {
      case 'top':
        return {
          position: 'fixed',
          bottom: window.innerHeight - targetRect.top + padding,
          left: targetRect.left + targetRect.width / 2 - tooltipWidth / 2,
        };
      case 'bottom':
        return {
          position: 'fixed',
          top: targetRect.bottom + padding,
          left: targetRect.left + targetRect.width / 2 - tooltipWidth / 2,
        };
      case 'left':
        return {
          position: 'fixed',
          top: targetRect.top + targetRect.height / 2 - 60,
          right: window.innerWidth - targetRect.left + padding,
        };
      case 'right':
        return {
          position: 'fixed',
          top: targetRect.top + targetRect.height / 2 - 60,
          left: targetRect.right + padding,
        };
      default:
        return {
          position: 'fixed',
          top: targetRect.bottom + padding,
          left: targetRect.left + targetRect.width / 2 - tooltipWidth / 2,
        };
    }
  };

  return (
    <>
      {/* Overlay */}
      <div className="fixed inset-0 z-40 bg-black/50 pointer-events-none" />

      {/* Spotlight on target */}
      {targetRect && (
        <div
          className="fixed z-40 pointer-events-none"
          style={{
            top: targetRect.top - 4,
            left: targetRect.left - 4,
            width: targetRect.width + 8,
            height: targetRect.height + 8,
            boxShadow: '0 0 0 9999px rgba(0, 0, 0, 0.5)',
            borderRadius: '8px',
          }}
        />
      )}

      {/* Tooltip */}
      <div
        className="fixed z-50 w-80 bg-white dark:bg-zinc-800 rounded-lg shadow-2xl p-4"
        style={getTooltipStyle()}
      >
        {/* Progress indicator */}
        <div className="flex gap-1 mb-3">
          {steps.map((_, index) => (
            <div
              key={index}
              className={`h-1 flex-1 rounded-full ${
                index <= currentStep
                  ? 'bg-blue-600'
                  : 'bg-zinc-200 dark:bg-zinc-700'
              }`}
            />
          ))}
        </div>

        <h3 className="text-lg font-semibold text-zinc-900 dark:text-white mb-2">
          {step.title}
        </h3>
        <p className="text-sm text-zinc-600 dark:text-zinc-400 mb-4">
          {step.content}
        </p>

        <div className="flex items-center justify-between">
          <button
            onClick={handleSkip}
            className="text-sm text-zinc-500 hover:text-zinc-700 dark:text-zinc-400 dark:hover:text-zinc-200"
          >
            Skip tour
          </button>
          <div className="flex gap-2">
            {currentStep > 0 && (
              <button
                onClick={handlePrevious}
                className="px-3 py-1.5 text-sm font-medium text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-700 rounded"
              >
                Previous
              </button>
            )}
            <button
              onClick={handleNext}
              className="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded"
            >
              {currentStep < steps.length - 1 ? 'Next' : 'Finish'}
            </button>
          </div>
        </div>
      </div>
    </>
  );
}

// Pre-defined tour for the dashboard
export const dashboardTourSteps: TourStep[] = [
  {
    target: '[data-tour="dashboard-header"]',
    title: 'Welcome to SIS State Manager',
    content: 'This dashboard gives you an overview of your state expansion analysis progress.',
    placement: 'bottom',
  },
  {
    target: '[data-tour="state-rankings"]',
    title: 'State Rankings',
    content: 'View states ranked by expansion viability based on multiple factors like technical fit and market opportunity.',
    placement: 'right',
  },
  {
    target: '[data-tour="gap-analysis"]',
    title: 'Gap Analysis',
    content: 'Identify missing features and estimate development effort needed for each target state.',
    placement: 'left',
  },
  {
    target: '[data-tour="roadmap"]',
    title: 'Implementation Roadmaps',
    content: 'Generate phased implementation plans with timelines and milestones for state expansions.',
    placement: 'top',
  },
];

// Hook for triggering tour reset
export function useResetTour(storageKey: string = 'onboarding_completed') {
  return useCallback(() => {
    localStorage.removeItem(storageKey);
    window.location.reload();
  }, [storageKey]);
}
