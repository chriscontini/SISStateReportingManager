'use client';

import { useState, useEffect, useRef } from 'react';
import AppShell from '@/components/AppShell';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  citations?: number[];
  created_at: string;
}

interface Session {
  id: number;
  title: string;
  state_filter: string | null;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  messages: Message[];
}

interface State {
  id: number;
  name: string;
  abbreviation: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const SUGGESTED_PROMPTS = [
  "What are Pennsylvania's PIMS reporting requirements?",
  "Compare Texas PEIMS with New Jersey SMART reporting",
  "What certification is needed for Maryland?",
  "Explain the LA parish-based district model",
  "What data elements are required for attendance reporting?",
];

export default function ChatPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [currentSession, setCurrentSession] = useState<Session | null>(null);
  const [states, setStates] = useState<State[]>([]);
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState('');
  const [stateFilter, setStateFilter] = useState<string>('');
  const [showSidebar, setShowSidebar] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    fetchInitialData();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [currentSession?.messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const fetchInitialData = async () => {
    try {
      const [sessionsRes, statesRes] = await Promise.all([
        fetch(`${API_URL}/api/chat/sessions`),
        fetch(`${API_URL}/api/states`),
      ]);

      if (sessionsRes.ok) {
        const data = await sessionsRes.json();
        setSessions(data.sessions || []);
      }

      if (statesRes.ok) {
        const data = await statesRes.json();
        setStates(data);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const createNewSession = async () => {
    try {
      const res = await fetch(`${API_URL}/api/chat/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: 'New Chat',
          state_filter: stateFilter || null,
        }),
      });

      if (res.ok) {
        const session = await res.json();
        const newSession: Session = {
          ...session,
          messages: [],
        };
        setSessions((prev) => [newSession, ...prev]);
        setCurrentSession(newSession);
      }
    } catch (error) {
      console.error('Error creating session:', error);
    }
  };

  const loadSession = async (sessionId: number) => {
    try {
      const res = await fetch(`${API_URL}/api/chat/sessions/${sessionId}`);
      if (res.ok) {
        const session = await res.json();
        setCurrentSession(session);
        if (session.state_filter) {
          setStateFilter(session.state_filter);
        }
      }
    } catch (error) {
      console.error('Error loading session:', error);
    }
  };

  const deleteSession = async (sessionId: number) => {
    try {
      const res = await fetch(`${API_URL}/api/chat/sessions/${sessionId}`, {
        method: 'DELETE',
      });

      if (res.ok) {
        setSessions((prev) => prev.filter((s) => s.id !== sessionId));
        if (currentSession?.id === sessionId) {
          setCurrentSession(null);
        }
      }
    } catch (error) {
      console.error('Error deleting session:', error);
    }
  };

  const sendMessage = async () => {
    if (!message.trim() || sending) return;

    // Create session if needed
    let session = currentSession;
    if (!session) {
      try {
        const res = await fetch(`${API_URL}/api/chat/sessions`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title: message.slice(0, 50),
            state_filter: stateFilter || null,
          }),
        });

        if (res.ok) {
          session = await res.json();
          session.messages = [];
          setSessions((prev) => [session!, ...prev]);
          setCurrentSession(session);
        } else {
          return;
        }
      } catch (error) {
        console.error('Error creating session:', error);
        return;
      }
    }

    // Add user message optimistically
    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: message,
      created_at: new Date().toISOString(),
    };

    setCurrentSession((prev) => ({
      ...prev!,
      messages: [...(prev?.messages || []), userMessage],
    }));

    const userInput = message;
    setMessage('');
    setSending(true);

    try {
      const res = await fetch(
        `${API_URL}/api/chat/sessions/${session!.id}/messages`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ content: userInput }),
        }
      );

      if (res.ok) {
        const assistantMessage = await res.json();
        setCurrentSession((prev) => ({
          ...prev!,
          messages: [...(prev?.messages || []), assistantMessage],
          title: prev?.messages.length === 1 ? userInput.slice(0, 50) : prev?.title || 'New Chat',
        }));

        // Update sessions list title
        setSessions((prev) =>
          prev.map((s) =>
            s.id === session!.id
              ? { ...s, title: userInput.slice(0, 50) + (userInput.length > 50 ? '...' : '') }
              : s
          )
        );
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // Add error message
      setCurrentSession((prev) => ({
        ...prev!,
        messages: [
          ...(prev?.messages || []),
          {
            id: Date.now(),
            role: 'assistant',
            content: 'Sorry, I encountered an error. Please try again.',
            created_at: new Date().toISOString(),
          },
        ],
      }));
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleSuggestedPrompt = (prompt: string) => {
    setMessage(prompt);
    inputRef.current?.focus();
  };

  if (loading) {
    return (
      <AppShell>
        <div className="flex items-center justify-center min-h-[400px]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
        </div>
      </AppShell>
    );
  }

  return (
    <AppShell>
      <div className="flex h-[calc(100vh-10rem)] gap-4">
        {/* Sidebar */}
        {showSidebar && (
          <div className="w-64 flex-shrink-0 bg-white dark:bg-zinc-800 rounded-lg shadow overflow-hidden flex flex-col">
            <div className="p-3 border-b border-zinc-200 dark:border-zinc-700">
              <button
                onClick={createNewSession}
                className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md font-medium text-sm"
              >
                + New Chat
              </button>
            </div>

            <div className="flex-1 overflow-y-auto">
              {sessions.map((session) => (
                <div
                  key={session.id}
                  className={`p-3 cursor-pointer border-b border-zinc-100 dark:border-zinc-700 hover:bg-zinc-50 dark:hover:bg-zinc-700 ${
                    currentSession?.id === session.id
                      ? 'bg-blue-50 dark:bg-blue-900/20'
                      : ''
                  }`}
                  onClick={() => loadSession(session.id)}
                >
                  <div className="flex items-start justify-between">
                    <span className="text-sm font-medium text-zinc-900 dark:text-white truncate flex-1">
                      {session.title}
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        deleteSession(session.id);
                      }}
                      className="ml-2 text-zinc-400 hover:text-red-500"
                    >
                      <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>
                  {session.state_filter && (
                    <span className="text-xs text-zinc-500 dark:text-zinc-400">
                      {session.state_filter}
                    </span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Main Chat Area */}
        <div className="flex-1 bg-white dark:bg-zinc-800 rounded-lg shadow flex flex-col overflow-hidden">
          {/* Header */}
          <div className="p-4 border-b border-zinc-200 dark:border-zinc-700 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowSidebar(!showSidebar)}
                className="p-2 hover:bg-zinc-100 dark:hover:bg-zinc-700 rounded"
              >
                <svg className="w-5 h-5 text-zinc-600 dark:text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
              <h1 className="text-lg font-semibold text-zinc-900 dark:text-white">
                {currentSession?.title || 'AI Assistant'}
              </h1>
            </div>

            <div className="flex items-center gap-2">
              <select
                value={stateFilter}
                onChange={(e) => setStateFilter(e.target.value)}
                className="px-3 py-1.5 text-sm border border-zinc-300 dark:border-zinc-600 rounded-md bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white"
              >
                <option value="">All States</option>
                {states.map((state) => (
                  <option key={state.id} value={state.abbreviation}>
                    {state.abbreviation}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {!currentSession?.messages.length && (
              <div className="h-full flex flex-col items-center justify-center text-center px-4">
                <div className="text-4xl mb-4">🤖</div>
                <h2 className="text-xl font-semibold text-zinc-900 dark:text-white mb-2">
                  State Reporting Assistant
                </h2>
                <p className="text-zinc-600 dark:text-zinc-400 mb-6 max-w-md">
                  Ask questions about state reporting requirements, compare states,
                  or get implementation guidance.
                </p>

                <div className="flex flex-wrap justify-center gap-2 max-w-2xl">
                  {SUGGESTED_PROMPTS.map((prompt, i) => (
                    <button
                      key={i}
                      onClick={() => handleSuggestedPrompt(prompt)}
                      className="px-3 py-2 text-sm bg-zinc-100 dark:bg-zinc-700 hover:bg-zinc-200 dark:hover:bg-zinc-600 rounded-lg text-zinc-700 dark:text-zinc-300 text-left"
                    >
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {currentSession?.messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-[80%] rounded-lg px-4 py-3 ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-zinc-100 dark:bg-zinc-700 text-zinc-900 dark:text-white'
                  }`}
                >
                  <div className="whitespace-pre-wrap text-sm">{msg.content}</div>
                  {msg.citations && msg.citations.length > 0 && (
                    <div className="mt-2 pt-2 border-t border-zinc-200 dark:border-zinc-600">
                      <span className="text-xs opacity-70">
                        Sources: {msg.citations.map((c) => `[${c}]`).join(', ')}
                      </span>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {sending && (
              <div className="flex justify-start">
                <div className="bg-zinc-100 dark:bg-zinc-700 rounded-lg px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div className="animate-pulse">Thinking</div>
                    <div className="flex gap-1">
                      <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                      <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                      <div className="w-2 h-2 bg-zinc-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-zinc-200 dark:border-zinc-700">
            <div className="flex gap-2">
              <textarea
                ref={inputRef}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask about state reporting requirements..."
                rows={1}
                className="flex-1 px-4 py-2 border border-zinc-300 dark:border-zinc-600 rounded-lg bg-white dark:bg-zinc-700 text-zinc-900 dark:text-white resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={sendMessage}
                disabled={!message.trim() || sending}
                className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-lg font-medium"
              >
                <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                </svg>
              </button>
            </div>
            <p className="mt-2 text-xs text-zinc-500 dark:text-zinc-400 text-center">
              Press Enter to send, Shift+Enter for new line
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
