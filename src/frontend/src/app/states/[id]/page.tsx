"use client";

import { useEffect, useState, useRef } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import dynamic from "next/dynamic";
import TierBadge from "@/components/TierBadge";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Dynamic import for radar chart
const ScoreRadarChart = dynamic(() => import("@/components/ScoreRadarChart"), {
  ssr: false,
  loading: () => <div className="h-64 flex items-center justify-center text-zinc-500">Loading chart...</div>,
});

interface ScoreWithFactor {
  factor_name: string;
  factor_weight: number;
  score: number;
  weighted_score: number;
  notes: string | null;
}

interface NCESData {
  total_districts: number | null;
  total_schools: number | null;
  total_students: number | null;
  avg_district_size: number | null;
  data_year: string | null;
}

interface StateDetail {
  id: number;
  name: string;
  abbreviation: string;
  doe_website: string | null;
  total_score: number;
  rank: number | null;
  nces_data: NCESData | null;
  scores: ScoreWithFactor[];
}

interface StateAnalysis {
  id: number;
  state_id: number;
  analysis_tier: number;
  reporting_system_details: string | null;
  submission_requirements: string | null;
  data_elements_summary: string | null;
  major_competitors: string | null;
  competitor_market_share: string | null;
  competitive_advantages: string | null;
  certification_process: string | null;
  compliance_requirements: string | null;
  estimated_certification_time: string | null;
  key_challenges: string | null;
  recommended_approach: string | null;
  estimated_development_months: number | null;
  ai_model_used: string | null;
  analysis_confidence: number | null;
}

// Chat Widget Component
function StateChatWidget({ stateName, stateAbbr }: { stateName: string; stateAbbr: string }) {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const createSession = async () => {
    try {
      const response = await fetch(`${API_URL}/api/chat/sessions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: `Chat about ${stateName}`,
          state_filter: stateAbbr,
        }),
      });
      if (response.ok) {
        const data = await response.json();
        setSessionId(data.session_id);
        return data.session_id;
      }
    } catch (err) {
      console.error("Failed to create session:", err);
    }
    return null;
  };

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);

    try {
      let sid = sessionId;
      if (!sid) {
        sid = await createSession();
        if (!sid) throw new Error("Failed to create session");
      }

      const response = await fetch(`${API_URL}/api/chat/sessions/${sid}/messages`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: userMessage }),
      });

      if (response.ok) {
        const data = await response.json();
        setMessages((prev) => [...prev, { role: "assistant", content: data.content }]);
      } else {
        throw new Error("Failed to send message");
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I encountered an error. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    `What are ${stateAbbr}'s main reporting requirements?`,
    `Who are the major SIS competitors in ${stateAbbr}?`,
    `What certifications are needed for ${stateAbbr}?`,
  ];

  return (
    <>
      {/* Floating Chat Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-6 right-6 w-14 h-14 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg flex items-center justify-center z-50 transition-transform hover:scale-105"
        aria-label="Open chat"
      >
        {isOpen ? (
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        )}
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 w-96 h-[500px] bg-white dark:bg-zinc-900 rounded-lg shadow-xl border border-zinc-200 dark:border-zinc-700 flex flex-col z-50">
          {/* Header */}
          <div className="px-4 py-3 border-b border-zinc-200 dark:border-zinc-700 bg-blue-600 text-white rounded-t-lg">
            <h3 className="font-semibold">Ask about {stateName}</h3>
            <p className="text-xs text-blue-100">AI-powered state reporting assistant</p>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.length === 0 ? (
              <div className="text-center text-zinc-500 dark:text-zinc-400 text-sm py-4">
                <p className="mb-4">Ask questions about {stateName}'s state reporting requirements.</p>
                <div className="space-y-2">
                  {suggestedQuestions.map((q, i) => (
                    <button
                      key={i}
                      onClick={() => setInput(q)}
                      className="block w-full text-left px-3 py-2 text-xs bg-zinc-100 dark:bg-zinc-800 rounded-lg hover:bg-zinc-200 dark:hover:bg-zinc-700"
                    >
                      {q}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              messages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-3 py-2 text-sm ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-zinc-100 dark:bg-zinc-800 text-zinc-900 dark:text-white"
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))
            )}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-zinc-100 dark:bg-zinc-800 rounded-lg px-3 py-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" />
                    <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style={{ animationDelay: "0.1s" }} />
                    <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }} />
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input */}
          <div className="p-3 border-t border-zinc-200 dark:border-zinc-700">
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
                placeholder="Ask a question..."
                className="flex-1 px-3 py-2 text-sm border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-800 text-zinc-900 dark:text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={sendMessage}
                disabled={!input.trim() || loading}
                className="px-3 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default function StateDetailPage() {
  const params = useParams();
  const stateId = params.id as string;

  const [state, setState] = useState<StateDetail | null>(null);
  const [analysis, setAnalysis] = useState<StateAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "analysis">("overview");

  useEffect(() => {
    async function fetchStateData() {
      try {
        // Fetch state details
        const detailResponse = await fetch(`${API_URL}/api/states/${stateId}/detail`);
        if (!detailResponse.ok) {
          throw new Error("Failed to fetch state details");
        }
        const detailData = await detailResponse.json();
        setState(detailData);

        // Fetch analysis (may not exist)
        try {
          const analysisResponse = await fetch(`${API_URL}/api/states/${stateId}/analysis`);
          if (analysisResponse.ok) {
            const analysisData = await analysisResponse.json();
            setAnalysis(analysisData);
          }
        } catch {
          // Analysis not available - that's okay
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "An error occurred");
      } finally {
        setLoading(false);
      }
    }

    if (stateId) {
      fetchStateData();
    }
  }, [stateId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="text-zinc-500 dark:text-zinc-400">Loading state details...</div>
      </div>
    );
  }

  if (error || !state) {
    return (
      <div className="space-y-4">
        <Link href="/states" className="text-blue-600 hover:text-blue-800 dark:text-blue-400">
          &larr; Back to States
        </Link>
        <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
          <p className="text-red-800 dark:text-red-200">Error: {error || "State not found"}</p>
        </div>
      </div>
    );
  }

  const formatNumber = (num: number | null) => {
    if (num === null) return "N/A";
    return num.toLocaleString();
  };

  return (
    <div className="space-y-6">
      <Link href="/states" className="text-blue-600 hover:text-blue-800 dark:text-blue-400">
        &larr; Back to States
      </Link>

      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-zinc-900 dark:text-white">
            {state.name} ({state.abbreviation})
          </h1>
          {state.doe_website && (
            <a
              href={state.doe_website}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:text-blue-800 dark:text-blue-400 text-sm"
            >
              {state.doe_website}
            </a>
          )}
        </div>
        <div className="text-right">
          <div className="flex items-center gap-3 justify-end">
            <div className="text-3xl font-bold text-green-600 dark:text-green-400">
              {state.total_score.toFixed(2)}
            </div>
            {state.total_score > 0 && (
              <TierBadge score={state.total_score} size="lg" />
            )}
          </div>
          <div className="text-sm text-zinc-500 dark:text-zinc-400 mt-1">
            Rank #{state.rank || "N/A"} of 50
          </div>
        </div>
      </div>

      {/* NCES Data */}
      {state.nces_data && (
        <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
          <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
            NCES Data {state.nces_data.data_year && `(${state.nces_data.data_year})`}
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {formatNumber(state.nces_data.total_districts)}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Districts</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {formatNumber(state.nces_data.total_schools)}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Schools</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {formatNumber(state.nces_data.total_students)}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Students</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-zinc-900 dark:text-white">
                {state.nces_data.avg_district_size
                  ? Math.round(state.nces_data.avg_district_size).toLocaleString()
                  : "N/A"}
              </div>
              <div className="text-sm text-zinc-500 dark:text-zinc-400">Avg District Size</div>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      {analysis && (
        <div className="flex border-b border-zinc-200 dark:border-zinc-700">
          <button
            onClick={() => setActiveTab("overview")}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "overview"
                ? "border-blue-600 text-blue-600 dark:text-blue-400"
                : "border-transparent text-zinc-500 hover:text-zinc-700 dark:text-zinc-400"
            }`}
          >
            Overview
          </button>
          <button
            onClick={() => setActiveTab("analysis")}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === "analysis"
                ? "border-blue-600 text-blue-600 dark:text-blue-400"
                : "border-transparent text-zinc-500 hover:text-zinc-700 dark:text-zinc-400"
            }`}
          >
            Deep Analysis
            <span className="ml-2 text-xs bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-2 py-0.5 rounded-full">
              Tier {analysis.analysis_tier}
            </span>
          </button>
        </div>
      )}

      {activeTab === "overview" && (
        <>
          {/* Radar Chart */}
          {state.scores.length > 0 && (
            <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
              <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
                Score Visualization
              </h2>
              <ScoreRadarChart
                states={[
                  {
                    name: state.name,
                    abbreviation: state.abbreviation,
                    scores: state.scores.map(s => ({
                      factor_name: s.factor_name,
                      score: s.score,
                    })),
                    color: '#3b82f6',
                  },
                ]}
                height={350}
              />
            </div>
          )}

          {/* Scores Breakdown */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
              Score Breakdown
            </h2>
            {state.scores.length > 0 ? (
              <div className="space-y-3">
                {state.scores
                  .sort((a, b) => b.weighted_score - a.weighted_score)
                  .map((score) => (
                    <div
                      key={score.factor_name}
                      className="flex items-center justify-between p-3 bg-zinc-50 dark:bg-zinc-900 rounded-md"
                    >
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <span className="font-medium text-zinc-900 dark:text-white">
                            {score.factor_name}
                          </span>
                          <span className="text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-0.5 rounded">
                            Weight: {score.factor_weight}
                          </span>
                        </div>
                        {score.notes && (
                          <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1">
                            {score.notes}
                          </p>
                        )}
                      </div>
                      <div className="text-right ml-4">
                        <div className="font-bold text-zinc-900 dark:text-white">
                          {score.score.toFixed(1)}
                        </div>
                        <div className="text-xs text-zinc-500 dark:text-zinc-400">
                          Weighted: {score.weighted_score.toFixed(2)}
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            ) : (
              <div className="text-center py-8 text-zinc-500 dark:text-zinc-400">
                No scores calculated yet. Run score calculation from the Rankings page.
              </div>
            )}
          </div>
        </>
      )}

      {activeTab === "analysis" && analysis && (
        <div className="space-y-6">
          {/* Reporting System */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
              Reporting System Details
            </h2>
            {analysis.reporting_system_details && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">System Overview</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.reporting_system_details}
                </p>
              </div>
            )}
            {analysis.submission_requirements && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">Submission Requirements</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.submission_requirements}
                </p>
              </div>
            )}
            {analysis.data_elements_summary && (
              <div>
                <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">Data Elements</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.data_elements_summary}
                </p>
              </div>
            )}
          </div>

          {/* Competitive Intelligence */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
              Competitive Intelligence
            </h2>
            {analysis.major_competitors && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">Major Competitors</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.major_competitors}
                </p>
              </div>
            )}
            {analysis.competitor_market_share && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">Market Share</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.competitor_market_share}
                </p>
              </div>
            )}
            {analysis.competitive_advantages && (
              <div>
                <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">Competitive Analysis</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.competitive_advantages}
                </p>
              </div>
            )}
          </div>

          {/* Certification & Compliance */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
              Certification & Compliance
            </h2>
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                {analysis.certification_process && (
                  <div className="mb-4">
                    <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">Certification Process</h3>
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                      {analysis.certification_process}
                    </p>
                  </div>
                )}
                {analysis.estimated_certification_time && (
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-zinc-500">Estimated Timeline:</span>
                    <span className="text-sm font-medium text-zinc-900 dark:text-white">
                      {analysis.estimated_certification_time}
                    </span>
                  </div>
                )}
              </div>
              <div>
                {analysis.compliance_requirements && (
                  <div>
                    <h3 className="text-sm font-medium text-zinc-700 dark:text-zinc-300 mb-2">Compliance Requirements</h3>
                    <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                      {analysis.compliance_requirements}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Implementation Recommendations */}
          <div className="bg-white dark:bg-zinc-800 rounded-lg border border-zinc-200 dark:border-zinc-700 p-6">
            <h2 className="text-lg font-semibold text-zinc-900 dark:text-white mb-4">
              Implementation Insights
            </h2>
            {analysis.key_challenges && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-red-700 dark:text-red-400 mb-2">Key Challenges</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.key_challenges}
                </p>
              </div>
            )}
            {analysis.recommended_approach && (
              <div className="mb-4">
                <h3 className="text-sm font-medium text-green-700 dark:text-green-400 mb-2">Recommended Approach</h3>
                <p className="text-sm text-zinc-600 dark:text-zinc-400 whitespace-pre-line">
                  {analysis.recommended_approach}
                </p>
              </div>
            )}
            {analysis.estimated_development_months && (
              <div className="mt-4 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-blue-700 dark:text-blue-300">Estimated Development Time</span>
                  <span className="text-2xl font-bold text-blue-800 dark:text-blue-200">
                    {analysis.estimated_development_months} months
                  </span>
                </div>
              </div>
            )}
          </div>

          {/* Analysis Metadata */}
          <div className="text-xs text-zinc-400 dark:text-zinc-500 flex items-center gap-4">
            {analysis.ai_model_used && (
              <span>Analyzed by: {analysis.ai_model_used}</span>
            )}
            {analysis.analysis_confidence && (
              <span>Confidence: {(analysis.analysis_confidence * 100).toFixed(0)}%</span>
            )}
          </div>
        </div>
      )}

      {/* Chat Widget */}
      <StateChatWidget stateName={state.name} stateAbbr={state.abbreviation} />
    </div>
  );
}
