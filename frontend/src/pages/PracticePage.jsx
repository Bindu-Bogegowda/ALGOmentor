import React, { useState, useEffect, useRef } from 'react';
import { 
  Code2, 
  Search, 
  Play, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  Sparkles, 
  HelpCircle, 
  Bookmark, 
  Bot, 
  Terminal, 
  Check, 
  RotateCcw,
  Send,
  MessageSquare,
  Lightbulb,
  Copy,
  ChevronRight,
  ChevronDown,
  Layers,
  Zap,
  CornerDownLeft,
  X,
  Maximize2,
  Minimize2
} from 'lucide-react';
import { api } from '../services/api';

export default function PracticePage({ onTriggerAI, initialProblemSlug, initialLanguage = 'java' }) {
  const [problems, setProblems] = useState([]);
  const [selectedProblem, setSelectedProblem] = useState(null);
  const [language, setLanguage] = useState(initialLanguage || 'java'); // 'java' (default) or 'python'
  const [code, setCode] = useState('');
  const [customInput, setCustomInput] = useState('');
  const [useCustomInput, setUseCustomInput] = useState(false);
  
  // Execution states
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [execResult, setExecResult] = useState(null);
  const [activeTab, setActiveTab] = useState('testcases'); // 'testcases', 'output', 'hints', 'chat'

  // Unlimited Progressive Hint System
  const [hintLevel, setHintLevel] = useState(0);
  const [hints, setHints] = useState({}); // { [level: number]: { title: string, content: string } }
  const [loadingHint, setLoadingHint] = useState(false);
  const [expandedHints, setExpandedHints] = useState({});

  // AI Coding Assistant Chat
  const [chatMessages, setChatMessages] = useState([
    {
      id: 1,
      role: 'assistant',
      content: "👋 Hello! I'm your AI Algorithm Mentor. Ask me any question while coding—like why your solution fails a test case, how to handle boundary edge cases, or how to write it in Java step-by-step!",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [chatSessionId, setChatSessionId] = useState(null);
  const [copiedCodeIdx, setCopiedCodeIdx] = useState(null);
  const [showSideChat, setShowSideChat] = useState(false);
  const chatBottomRef = useRef(null);

  // Filters
  const [search, setSearch] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState('All');
  const [filterTopic, setFilterTopic] = useState('All');

  useEffect(() => {
    loadProblems();
  }, []);

  useEffect(() => {
    if (chatBottomRef.current) {
      chatBottomRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatMessages, activeTab, showSideChat]);

  async function loadProblems() {
    try {
      const data = await api.listProblems();
      setProblems(data);
      if (data.length > 0) {
        const targetSlug = initialProblemSlug && data.some(p => p.slug === initialProblemSlug) 
          ? initialProblemSlug 
          : data[0].slug;
        selectProblem(targetSlug, initialLanguage || 'java');
      }
    } catch (err) {
      console.error('Failed to load problems:', err);
    }
  }

  async function selectProblem(slug, langOverride) {
    try {
      const p = await api.getProblem(slug);
      setSelectedProblem(p);
      const currentLang = langOverride || language || 'java';
      setCode(currentLang === 'java' 
        ? (p.starter_code_java || p.starter_code_python) 
        : (p.starter_code_python || p.starter_code_java));
      setExecResult(null);
      setHintLevel(p.highest_hint_level_used || 0);
      setHints({});
      setExpandedHints({});
      setActiveTab('testcases');
      // Reset chat for new problem
      setChatSessionId(null);
      setChatMessages([
        {
          id: Date.now(),
          role: 'assistant',
          content: `👋 Ready to solve **${p.title}**! You're coding in ${currentLang === 'java' ? 'Java ☕' : 'Python 🐍'}. Let me know if you need hints, edge-case checks, or debugging tips.`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } catch (err) {
      console.error('Failed to load problem detail:', err);
    }
  }

  function handleLanguageChange(newLang) {
    setLanguage(newLang);
    if (selectedProblem) {
      setCode(newLang === 'java' 
        ? (selectedProblem.starter_code_java || selectedProblem.starter_code_python) 
        : (selectedProblem.starter_code_python || selectedProblem.starter_code_java));
    }
  }

  async function handleRun() {
    if (!selectedProblem || running) return;
    setRunning(true);
    setActiveTab('output');
    try {
      const res = await api.runCode(
        code, 
        language, 
        selectedProblem.id, 
        useCustomInput ? customInput : null
      );
      setExecResult(res);
      // Auto-notify AI chat if there is an error
      if (res.stderr || res.status === 'Wrong Answer' || res.status === 'Error') {
        const autoNotice = {
          id: Date.now(),
          role: 'assistant',
          content: `⚠️ Your code returned **${res.status}** with ${res.passed_tests || 0}/${res.total_tests || 0} test cases passed. Click **"Why is my code failing?"** below or ask me to debug it!`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        };
        setChatMessages(prev => [...prev, autoNotice]);
      }
    } catch (err) {
      setExecResult({
        status: 'Error',
        stderr: err.message || 'Execution failed',
        test_results: []
      });
    } finally {
      setRunning(false);
    }
  }

  async function handleSubmit() {
    if (!selectedProblem || submitting) return;
    setSubmitting(true);
    setActiveTab('output');
    try {
      const res = await api.submitCode(code, language, selectedProblem.id);
      setExecResult(res);
      if (res.status === 'Accepted') {
        setSelectedProblem(prev => ({ ...prev, status: 'Solved' }));
        setProblems(prev => prev.map(p => p.id === selectedProblem.id ? { ...p, status: 'Solved' } : p));
        setChatMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            role: 'assistant',
            content: `🎉 Outstanding work! All test cases passed with runtime **${res.runtime_ms} ms**! Would you like to review time/space complexity optimizations or move to the next challenge?`,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      } else {
        setChatMessages(prev => [
          ...prev,
          {
            id: Date.now(),
            role: 'assistant',
            content: `❌ Submission verdict: **${res.status}** (${res.passed_tests}/${res.total_tests} passed). Need help identifying the failing edge case?`,
            timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
          }
        ]);
      }
    } catch (err) {
      setExecResult({
        status: 'Error',
        stderr: err.message || 'Submission failed',
        test_results: []
      });
    } finally {
      setSubmitting(false);
    }
  }

  // UNLIMITED Progressive Hint Fetcher
  async function fetchProgressiveHint(targetLevel, includeCode = false) {
    if (!selectedProblem || loadingHint) return;
    setLoadingHint(true);
    try {
      const res = await api.getHint(
        selectedProblem.id, 
        targetLevel, 
        includeCode ? code : null
      );
      setHints(prev => ({
        ...prev,
        [targetLevel]: {
          title: res.title || `Level ${targetLevel} Hint`,
          content: res.content
        }
      }));
      setExpandedHints(prev => ({ ...prev, [targetLevel]: true }));
      setHintLevel(prev => Math.max(prev, targetLevel));
      setActiveTab('hints');
    } catch (err) {
      console.error('Failed to fetch hint:', err);
    } finally {
      setLoadingHint(false);
    }
  }

  function handleUnlockNextHint() {
    const nextLevel = Object.keys(hints).length + 1;
    fetchProgressiveHint(nextLevel, nextLevel >= 4);
  }

  function handleRequestAICustomHint() {
    const nextLevel = Object.keys(hints).length + 1;
    fetchProgressiveHint(nextLevel, true);
  }

  // AI Chat Assistant
  async function handleSendMessage(customPrompt = null) {
    const promptToSend = customPrompt || chatInput;
    if (!promptToSend.trim() || chatLoading) return;

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: promptToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setChatMessages(prev => [...prev, userMsg]);
    if (!customPrompt) setChatInput('');
    setChatLoading(true);

    try {
      const res = await api.sendTutorMessage({
        session_id: chatSessionId,
        message: promptToSend,
        context_page: 'practice',
        current_code: code,
        problem_title: selectedProblem ? selectedProblem.title : null,
        error_message: execResult?.stderr || (execResult?.status !== 'Accepted' ? `Status: ${execResult?.status}` : null)
      });

      if (res.session_id) {
        setChatSessionId(res.session_id);
      }

      const assistantMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: res.reply,
        codeSuggestion: res.code_suggestion,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setChatMessages(prev => [...prev, assistantMsg]);
    } catch (err) {
      setChatMessages(prev => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: `⚠️ Failed to reach AI mentor: ${err.message || 'Please check your connection and try again.'}`,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        }
      ]);
    } finally {
      setChatLoading(false);
    }
  }

  function handleCopySnippet(snippet, idx) {
    navigator.clipboard.writeText(snippet);
    setCopiedCodeIdx(idx);
    setTimeout(() => setCopiedCodeIdx(null), 2000);
  }

  async function handleBookmark() {
    if (!selectedProblem) return;
    try {
      const res = await api.toggleBookmark(selectedProblem.slug);
      setSelectedProblem(prev => ({ ...prev, is_bookmarked: res.is_bookmarked }));
      setProblems(prev => prev.map(p => p.id === selectedProblem.id ? { ...p, is_bookmarked: res.is_bookmarked } : p));
    } catch (err) {
      console.error('Bookmark error:', err);
    }
  }

  // Filter problems
  const filteredProblems = problems.filter(p => {
    const matchesSearch = !search || 
      p.title.toLowerCase().includes(search.toLowerCase()) || 
      (p.topic && p.topic.toLowerCase().includes(search.toLowerCase()));
    const matchesDifficulty = filterDifficulty === 'All' || p.difficulty === filterDifficulty;
    const matchesTopic = filterTopic === 'All' || p.topic === filterTopic;
    return matchesSearch && matchesDifficulty && matchesTopic;
  });

  const uniqueTopics = ['All', ...new Set(problems.map(p => p.topic).filter(Boolean))];

  // Helper color for hints
  const getHintBadgeColor = (lvl) => {
    switch (Number(lvl)) {
      case 1: return { color: '#38bdf8', bg: 'rgba(56, 189, 248, 0.15)', border: 'rgba(56, 189, 248, 0.3)' };
      case 2: return { color: '#c084fc', bg: 'rgba(192, 132, 252, 0.15)', border: 'rgba(192, 132, 252, 0.3)' };
      case 3: return { color: '#fbbf24', bg: 'rgba(251, 191, 36, 0.15)', border: 'rgba(251, 191, 36, 0.3)' };
      case 4: return { color: '#34d399', bg: 'rgba(52, 211, 153, 0.15)', border: 'rgba(52, 211, 153, 0.3)' };
      case 5: return { color: '#60a5fa', bg: 'rgba(96, 165, 250, 0.15)', border: 'rgba(96, 165, 250, 0.3)' };
      case 6: return { color: '#f43f5e', bg: 'rgba(244, 63, 94, 0.15)', border: 'rgba(244, 63, 94, 0.3)' };
      default: return { color: '#f472b6', bg: 'rgba(244, 114, 182, 0.15)', border: 'rgba(244, 114, 182, 0.3)' };
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', minHeight: '85vh', paddingBottom: '2rem' }}>
      
      {/* Top Banner / Problem Bar */}
      <div className="card-glass" style={{
        padding: '0.85rem 1.25rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '0.75rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: '8px',
            backgroundColor: 'rgba(56, 189, 248, 0.15)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--accent-cyan)'
          }}>
            <Code2 size={20} />
          </div>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <h2 style={{ fontSize: '1.15rem', fontWeight: 800, margin: 0, color: '#f8fafc' }}>
                {selectedProblem ? selectedProblem.title : 'Loading Problem...'}
              </h2>
              {selectedProblem && (
                <>
                  <span className={`badge ${
                    selectedProblem.difficulty === 'Easy' ? 'badge-easy' : 
                    selectedProblem.difficulty === 'Medium' ? 'badge-medium' : 'badge-hard'
                  }`}>
                    {selectedProblem.difficulty}
                  </span>
                  <span style={{
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    padding: '2px 8px',
                    borderRadius: '4px',
                    backgroundColor: 'rgba(148, 163, 184, 0.1)',
                    color: '#94a3b8'
                  }}>
                    {selectedProblem.topic}
                  </span>
                </>
              )}
            </div>
            <div style={{ fontSize: '0.75rem', color: '#94a3b8', display: 'flex', gap: '12px', marginTop: '2px' }}>
              <span>Target Time: <strong style={{ color: 'var(--accent-cyan)' }}>{selectedProblem?.expected_time_complexity || 'O(N)'}</strong></span>
              <span>•</span>
              <span>Target Space: <strong style={{ color: '#c084fc' }}>{selectedProblem?.expected_space_complexity || 'O(1)'}</strong></span>
            </div>
          </div>
        </div>

        {/* Action Controls & AI Tutor Button */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {selectedProblem && (
            <button
              onClick={handleBookmark}
              className="btn-glass"
              style={{
                padding: '0.45rem 0.75rem',
                fontSize: '0.8rem',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                color: selectedProblem.is_bookmarked ? 'var(--accent-amber)' : 'var(--text-muted)'
              }}
              title="Bookmark for Revision"
            >
              <Bookmark size={14} fill={selectedProblem.is_bookmarked ? 'currentColor' : 'none'} />
              <span>{selectedProblem.is_bookmarked ? 'Saved' : 'Save'}</span>
            </button>
          )}

          {/* Side-by-side AI Mentor Drawer Toggle */}
          <button
            onClick={() => {
              setShowSideChat(!showSideChat);
              if (!showSideChat) setActiveTab('chat');
            }}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: showSideChat ? '1px solid var(--accent-cyan)' : '1px solid rgba(56, 189, 248, 0.3)',
              backgroundColor: showSideChat ? 'rgba(56, 189, 248, 0.2)' : 'rgba(56, 189, 248, 0.1)',
              color: 'var(--accent-cyan)',
              fontSize: '0.82rem',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              transition: 'all 0.2s ease'
            }}
          >
            <Bot size={15} />
            <span>AI Code Mentor</span>
            <span style={{
              width: '8px',
              height: '8px',
              borderRadius: '50%',
              backgroundColor: '#10b981',
              boxShadow: '0 0 8px #10b981'
            }} />
          </button>
        </div>
      </div>

      {/* Main Workspace Layout (Left: Problem Statement & Problem Bank | Center: Code Editor & Console | Right Optional: AI Chat) */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: showSideChat 
          ? '320px 1fr 360px' 
          : '360px 1fr',
        gap: '1rem',
        alignItems: 'stretch'
      }}>
        
        {/* Left Column: Problem Details & Problem List */}
        <div className="card-glass" style={{
          display: 'flex',
          flexDirection: 'column',
          maxHeight: 'calc(100vh - 180px)',
          overflow: 'hidden'
        }}>
          {/* Problem Selector Bar */}
          <div style={{
            padding: '0.75rem',
            borderBottom: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-card)'
          }}>
            <div style={{ position: 'relative', marginBottom: '0.5rem' }}>
              <Search size={14} style={{ position: 'absolute', left: '10px', top: '50%', transform: 'translateY(-50%)', color: 'var(--text-muted)' }} />
              <input
                type="text"
                placeholder="Search practice problems..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.4rem 0.5rem 0.4rem 2rem',
                  borderRadius: '6px',
                  border: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-primary)',
                  color: 'var(--text-primary)',
                  fontSize: '0.8rem',
                  outline: 'none'
                }}
              />
            </div>
            
            <div style={{ display: 'flex', gap: '6px' }}>
              <select
                value={filterDifficulty}
                onChange={(e) => setFilterDifficulty(e.target.value)}
                style={{
                  flex: 1,
                  padding: '0.3rem 0.4rem',
                  borderRadius: '6px',
                  border: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-primary)',
                  color: 'var(--text-primary)',
                  fontSize: '0.75rem',
                  outline: 'none'
                }}
              >
                <option value="All">All Difficulties</option>
                <option value="Easy">Easy</option>
                <option value="Medium">Medium</option>
                <option value="Hard">Hard</option>
              </select>

              <select
                value={filterTopic}
                onChange={(e) => setFilterTopic(e.target.value)}
                style={{
                  flex: 1,
                  padding: '0.3rem 0.4rem',
                  borderRadius: '6px',
                  border: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-primary)',
                  color: 'var(--text-primary)',
                  fontSize: '0.75rem',
                  outline: 'none'
                }}
              >
                {uniqueTopics.map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
          </div>

          {/* Problem Selector Dropdown / Quick Switcher */}
          <div style={{
            maxHeight: '140px',
            overflowY: 'auto',
            borderBottom: '1px solid var(--border-subtle)',
            backgroundColor: '#0a0f1d'
          }}>
            {filteredProblems.map(p => (
              <div
                key={p.id}
                onClick={() => selectProblem(p.slug)}
                style={{
                  padding: '0.5rem 0.75rem',
                  cursor: 'pointer',
                  borderLeft: selectedProblem?.id === p.id ? '3px solid var(--accent-cyan)' : '3px solid transparent',
                  backgroundColor: selectedProblem?.id === p.id ? 'rgba(56, 189, 248, 0.1)' : 'transparent',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  fontSize: '0.78rem'
                }}
              >
                <span style={{
                  fontWeight: selectedProblem?.id === p.id ? 700 : 500,
                  color: selectedProblem?.id === p.id ? '#f8fafc' : '#94a3b8',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  maxWidth: '220px'
                }}>
                  {p.title}
                </span>
                <span className={`badge ${
                  p.difficulty === 'Easy' ? 'badge-easy' : p.difficulty === 'Medium' ? 'badge-medium' : 'badge-hard'
                }`} style={{ fontSize: '0.65rem', padding: '1px 6px' }}>
                  {p.difficulty}
                </span>
              </div>
            ))}
          </div>

          {/* Problem Statement Content */}
          {selectedProblem ? (
            <div style={{
              flex: 1,
              overflowY: 'auto',
              padding: '1.25rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1.25rem'
            }}>
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                  Description:
                </h4>
                <div style={{
                  fontSize: '0.88rem',
                  lineHeight: 1.6,
                  color: 'var(--text-primary)',
                  whiteSpace: 'pre-wrap'
                }}>
                  {selectedProblem.description}
                </div>
              </div>

              {/* Constraints */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                  Constraints:
                </h4>
                <div style={{
                  backgroundColor: 'var(--bg-primary)',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '1px solid var(--border-subtle)',
                  fontFamily: 'Consolas, monospace',
                  fontSize: '0.82rem',
                  color: 'var(--text-secondary)',
                  whiteSpace: 'pre-wrap'
                }}>
                  {selectedProblem.constraints}
                </div>
              </div>

              {/* Examples */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.5rem' }}>
                  Examples:
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                  {(selectedProblem.examples || []).map((ex, i) => (
                    <div key={i} style={{
                      backgroundColor: 'var(--bg-primary)',
                      padding: '0.85rem',
                      borderRadius: '8px',
                      border: '1px solid var(--border-subtle)',
                      fontSize: '0.82rem',
                      fontFamily: 'Consolas, monospace'
                    }}>
                      <div><strong style={{ color: 'var(--text-muted)' }}>Input: </strong><span style={{ color: 'var(--text-primary)' }}>{ex.input}</span></div>
                      <div><strong style={{ color: 'var(--text-muted)' }}>Output: </strong><span style={{ color: 'var(--accent-cyan)' }}>{ex.output}</span></div>
                      {ex.explanation && (
                        <div style={{ color: 'var(--text-muted)', marginTop: '4px', fontFamily: 'system-ui' }}>
                          Explanation: {ex.explanation}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div style={{ textAlign: 'center', color: 'var(--text-muted)', marginTop: '4rem' }}>
              Select a problem from the practice bank to begin.
            </div>
          )}
        </div>

        {/* Center Column: Code Editor & Execution Runner Console */}
        <div className="card-glass" style={{
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          minHeight: 'calc(100vh - 180px)'
        }}>
          {/* Editor Header Bar (Language, Hints, Run, Submit) */}
          <div style={{
            padding: '0.75rem 1rem',
            borderBottom: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-card)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '0.5rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
              <select
                value={language}
                onChange={(e) => handleLanguageChange(e.target.value)}
                style={{
                  padding: '0.35rem 0.65rem',
                  borderRadius: '6px',
                  border: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-primary)',
                  color: 'var(--text-primary)',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  outline: 'none'
                }}
              >
                <option value="java">☕ Java 17 (JDK)</option>
                <option value="python">🐍 Python 3.13</option>
              </select>

              {/* Progressive Hints Counter Button (UNLIMITED) */}
              <button
                onClick={() => setActiveTab('hints')}
                style={{
                  padding: '0.35rem 0.65rem',
                  borderRadius: '6px',
                  border: '1px solid rgba(245, 158, 11, 0.3)',
                  backgroundColor: 'rgba(245, 158, 11, 0.1)',
                  color: 'var(--accent-amber)',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px'
                }}
              >
                <Lightbulb size={14} />
                <span>Hints ({Object.keys(hints).length} Unlocked)</span>
              </button>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <button
                onClick={handleRun}
                disabled={running || submitting}
                className="btn-secondary"
                style={{ padding: '0.45rem 0.85rem', fontSize: '0.82rem' }}
              >
                <Play size={14} /> {running ? 'Running...' : 'Run Code'}
              </button>

              <button
                onClick={handleSubmit}
                disabled={running || submitting}
                className="btn-primary"
                style={{ padding: '0.45rem 1rem', fontSize: '0.82rem' }}
              >
                <Send size={14} /> {submitting ? 'Submitting...' : 'Submit'}
              </button>
            </div>
          </div>

          {/* Code Textarea Area */}
          <div style={{ flex: 1, minHeight: '300px', position: 'relative', backgroundColor: '#070b14' }}>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck="false"
              style={{
                width: '100%',
                height: '100%',
                padding: '1rem',
                backgroundColor: 'transparent',
                color: '#f8fafc',
                fontFamily: 'Consolas, Monaco, monospace',
                fontSize: '0.9rem',
                lineHeight: 1.5,
                border: 'none',
                outline: 'none',
                resize: 'none',
                tabSize: 4
              }}
            />
          </div>

          {/* Console / Output Tabs Drawer */}
          <div style={{
            height: '290px',
            borderTop: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-secondary)',
            display: 'flex',
            flexDirection: 'column'
          }}>
            {/* Tabs Header */}
            <div style={{
              display: 'flex',
              borderBottom: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-card)',
              padding: '0 0.5rem'
            }}>
              {[
                { id: 'testcases', label: 'Test Cases' },
                { id: 'output', label: 'Console Output' },
                { id: 'hints', label: `💡 Progressive Hints (${Object.keys(hints).length})` },
                { id: 'chat', label: '💬 AI Code Mentor' }
              ].map(tab => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  style={{
                    padding: '0.55rem 0.9rem',
                    border: 'none',
                    borderBottom: activeTab === tab.id ? '2px solid var(--accent-cyan)' : '2px solid transparent',
                    backgroundColor: 'transparent',
                    color: activeTab === tab.id ? 'var(--accent-cyan)' : 'var(--text-muted)',
                    fontSize: '0.82rem',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  {tab.label}
                </button>
              ))}
            </div>

            {/* TAB 1: Sample Test Cases & Custom Input */}
            {activeTab === 'testcases' && (
              <div style={{ flex: 1, padding: '1rem', overflowY: 'auto' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
                  <input
                    type="checkbox"
                    id="customInpCheck"
                    checked={useCustomInput}
                    onChange={(e) => setUseCustomInput(e.target.checked)}
                  />
                  <label htmlFor="customInpCheck" style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', cursor: 'pointer' }}>
                    Use Custom Input
                  </label>
                </div>

                {useCustomInput ? (
                  <textarea
                    placeholder="Enter custom test input..."
                    value={customInput}
                    onChange={(e) => setCustomInput(e.target.value)}
                    style={{
                      width: '100%',
                      height: '110px',
                      padding: '0.65rem',
                      borderRadius: '8px',
                      border: '1px solid var(--border-subtle)',
                      backgroundColor: 'var(--bg-primary)',
                      color: 'var(--text-primary)',
                      fontFamily: 'Consolas, monospace',
                      fontSize: '0.85rem',
                      outline: 'none'
                    }}
                  />
                ) : (
                  <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                    {(selectedProblem?.sample_test_cases || []).map((tc, idx) => (
                      <div key={idx} style={{
                        padding: '0.75rem',
                        borderRadius: '8px',
                        backgroundColor: 'var(--bg-primary)',
                        border: '1px solid var(--border-subtle)',
                        fontSize: '0.8rem',
                        fontFamily: 'Consolas, monospace'
                      }}>
                        <div style={{ fontWeight: 700, color: 'var(--accent-cyan)', marginBottom: '4px' }}>Case {idx + 1}</div>
                        <div><strong style={{ color: 'var(--text-muted)' }}>Input:</strong> {tc.input}</div>
                        <div><strong style={{ color: 'var(--text-muted)' }}>Expected:</strong> {tc.expected_output}</div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* TAB 2: Console Output & Test Results */}
            {activeTab === 'output' && (
              <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {execResult ? (
                  <>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <span className={`badge ${
                          execResult.status === 'Accepted' || execResult.status === 'Success' ? 'badge-easy' : 'badge-hard'
                        }`}>
                          {execResult.status}
                        </span>
                        <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                          Passed: <strong>{execResult.passed_tests} / {execResult.total_tests}</strong> test cases
                        </span>
                      </div>
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                        Runtime: <strong>{execResult.runtime_ms} ms</strong>
                      </span>
                    </div>

                    {/* Test Results Badges */}
                    {execResult.test_results?.length > 0 && (
                      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                        {execResult.test_results.map(tr => (
                          <div key={tr.test_case_id} style={{
                            padding: '0.35rem 0.65rem',
                            borderRadius: '6px',
                            backgroundColor: tr.passed ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
                            border: `1px solid ${tr.passed ? 'rgba(16, 185, 129, 0.3)' : 'rgba(244, 63, 94, 0.3)'}`,
                            color: tr.passed ? 'var(--accent-emerald)' : 'var(--accent-rose)',
                            fontSize: '0.75rem',
                            fontWeight: 700
                          }}>
                            Case {tr.test_case_id}: {tr.passed ? 'Passed ✓' : 'Failed ✗'}
                          </div>
                        ))}
                      </div>
                    )}

                    {/* Stdout / Error Details */}
                    {execResult.stderr && (
                      <pre style={{
                        padding: '0.65rem',
                        borderRadius: '6px',
                        backgroundColor: 'rgba(244, 63, 94, 0.1)',
                        color: 'var(--accent-rose)',
                        fontSize: '0.78rem',
                        fontFamily: 'Consolas, monospace',
                        margin: 0,
                        whiteSpace: 'pre-wrap'
                      }}>
                        {execResult.stderr}
                      </pre>
                    )}

                    {/* AI Feedback Banner if failed */}
                    {execResult.ai_feedback && (
                      <div style={{
                        padding: '0.75rem',
                        borderRadius: '8px',
                        backgroundColor: 'rgba(168, 85, 247, 0.1)',
                        border: '1px solid rgba(168, 85, 247, 0.3)',
                        color: 'var(--text-primary)',
                        fontSize: '0.82rem',
                        lineHeight: 1.5
                      }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--accent-purple)', fontWeight: 700, marginBottom: '2px' }}>
                          <Bot size={14} /> AI Debugger Feedback:
                        </div>
                        {execResult.ai_feedback}
                      </div>
                    )}
                  </>
                ) : (
                  <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>
                    Click "Run Code" to test against sample cases, or "Submit" to evaluate all hidden cases.
                  </div>
                )}
              </div>
            )}

            {/* TAB 3: UNLIMITED PROGRESSIVE HINT SYSTEM */}
            {activeTab === 'hints' && (
              <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
                  <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                    Progressive hints provide hints from conceptual clue to code skeleton, edge cases, and personalized AI tips:
                  </div>

                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      onClick={handleUnlockNextHint}
                      disabled={loadingHint}
                      className="btn-primary"
                      style={{ padding: '0.35rem 0.85rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '5px' }}
                    >
                      <Lightbulb size={13} />
                      <span>{loadingHint ? 'Unlocking...' : `Unlock Level ${Object.keys(hints).length + 1} Hint`}</span>
                    </button>

                    <button
                      onClick={handleRequestAICustomHint}
                      disabled={loadingHint}
                      style={{
                        padding: '0.35rem 0.85rem',
                        fontSize: '0.78rem',
                        borderRadius: '8px',
                        border: '1px solid rgba(192, 132, 252, 0.4)',
                        backgroundColor: 'rgba(192, 132, 252, 0.15)',
                        color: '#c084fc',
                        fontWeight: 700,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '5px'
                      }}
                    >
                      <Sparkles size={13} />
                      <span>Ask AI for Code Hint</span>
                    </button>
                  </div>
                </div>

                {/* Render All Unlocked Progressive Hints */}
                {Object.keys(hints).length === 0 ? (
                  <div style={{
                    padding: '2rem',
                    textAlign: 'center',
                    backgroundColor: 'var(--bg-primary)',
                    borderRadius: '10px',
                    border: '1px dashed var(--border-subtle)',
                    color: '#94a3b8'
                  }}>
                    <Lightbulb size={28} style={{ color: '#fbbf24', margin: '0 auto 0.5rem auto' }} />
                    <div style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', marginBottom: '4px' }}>
                      No Hints Unlocked Yet
                    </div>
                    <p style={{ fontSize: '0.8rem', margin: 0, maxWidth: '400px', marginInline: 'auto' }}>
                      Click <strong>"Unlock Level 1 Hint"</strong> above to reveal conceptual clues without spoiling the solution. Hints are unlimited!
                    </p>
                  </div>
                ) : (
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {Object.entries(hints)
                      .sort(([a], [b]) => Number(a) - Number(b))
                      .map(([lvl, hintData]) => {
                        const styleCfg = getHintBadgeColor(lvl);
                        const isExpanded = expandedHints[lvl] !== false;
                        return (
                          <div
                            key={lvl}
                            style={{
                              borderRadius: '10px',
                              backgroundColor: 'var(--bg-primary)',
                              border: `1px solid ${styleCfg.border}`,
                              overflow: 'hidden'
                            }}
                          >
                            <div
                              onClick={() => setExpandedHints(prev => ({ ...prev, [lvl]: !isExpanded }))}
                              style={{
                                padding: '0.65rem 0.85rem',
                                display: 'flex',
                                justifyContent: 'space-between',
                                alignItems: 'center',
                                cursor: 'pointer',
                                backgroundColor: styleCfg.bg
                              }}
                            >
                              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <span style={{
                                  fontSize: '0.72rem',
                                  fontWeight: 800,
                                  color: styleCfg.color,
                                  textTransform: 'uppercase'
                                }}>
                                  Level {lvl}
                                </span>
                                <strong style={{ fontSize: '0.85rem', color: '#f8fafc' }}>
                                  {hintData.title}
                                </strong>
                              </div>
                              <span style={{ color: styleCfg.color }}>
                                {isExpanded ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
                              </span>
                            </div>

                            {isExpanded && (
                              <div style={{ padding: '0.85rem', fontSize: '0.84rem', lineHeight: 1.6, color: 'var(--text-primary)' }}>
                                <pre style={{
                                  margin: 0,
                                  fontFamily: hintData.content.includes('{') || hintData.content.includes('//') ? 'Consolas, monospace' : 'system-ui',
                                  whiteSpace: 'pre-wrap',
                                  fontSize: '0.82rem',
                                  color: '#e2e8f0'
                                }}>
                                  {hintData.content}
                                </pre>
                              </div>
                            )}
                          </div>
                        );
                      })}
                  </div>
                )}
              </div>
            )}

            {/* TAB 4: IN-CONSOLE AI CODE MENTOR CHAT BOX */}
            {activeTab === 'chat' && (
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
                {/* Chat Messages Log */}
                <div style={{ flex: 1, padding: '0.75rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                  {chatMessages.map((msg, idx) => (
                    <div
                      key={msg.id || idx}
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start',
                        maxWidth: '92%',
                        alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start'
                      }}
                    >
                      <div style={{
                        padding: '0.65rem 0.85rem',
                        borderRadius: '10px',
                        backgroundColor: msg.role === 'user' ? 'rgba(56, 189, 248, 0.15)' : '#0f172a',
                        border: `1px solid ${msg.role === 'user' ? 'rgba(56, 189, 248, 0.3)' : '#1e293b'}`,
                        color: msg.role === 'user' ? '#f8fafc' : '#e2e8f0',
                        fontSize: '0.82rem',
                        lineHeight: 1.5,
                        whiteSpace: 'pre-wrap'
                      }}>
                        {msg.role === 'assistant' && (
                          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-cyan)', fontWeight: 700, marginBottom: '4px', fontSize: '0.75rem' }}>
                            <Bot size={13} />
                            <span>AI Algorithm Mentor</span>
                            <span style={{ color: '#64748b', fontWeight: 400, marginLeft: 'auto' }}>{msg.timestamp}</span>
                          </div>
                        )}
                        <div>{msg.content}</div>

                        {msg.codeSuggestion && (
                          <div style={{ marginTop: '0.5rem', backgroundColor: '#070b14', padding: '0.5rem', borderRadius: '6px', border: '1px solid #1e293b' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                              <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Suggested Code:</span>
                              <button
                                onClick={() => handleCopySnippet(msg.codeSuggestion, idx)}
                                style={{ background: 'none', border: 'none', color: 'var(--accent-cyan)', fontSize: '0.7rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '3px' }}
                              >
                                {copiedCodeIdx === idx ? <Check size={11} /> : <Copy size={11} />}
                                <span>{copiedCodeIdx === idx ? 'Copied' : 'Copy'}</span>
                              </button>
                            </div>
                            <pre style={{ margin: 0, fontFamily: 'monospace', fontSize: '0.78rem', color: '#10b981' }}>
                              {msg.codeSuggestion}
                            </pre>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                  {chatLoading && (
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-cyan)', fontSize: '0.78rem', padding: '0.5rem' }}>
                      <Sparkles size={14} className="pulse-glow" />
                      <span>AI Mentor is analyzing your code and response...</span>
                    </div>
                  )}
                  <div ref={chatBottomRef} />
                </div>

                {/* Quick In-Context Prompt Pills */}
                <div style={{
                  padding: '0.4rem 0.75rem',
                  display: 'flex',
                  gap: '6px',
                  overflowX: 'auto',
                  borderTop: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-primary)'
                }}>
                  {[
                    "Why is my code failing?",
                    "What edge cases am I missing?",
                    "Explain step-by-step in Java",
                    "How to optimize time complexity?",
                    "Give me a hint without giving answer"
                  ].map((chip, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSendMessage(chip)}
                      disabled={chatLoading}
                      style={{
                        padding: '2px 8px',
                        borderRadius: '999px',
                        border: '1px solid #334155',
                        backgroundColor: '#0f172a',
                        color: '#94a3b8',
                        fontSize: '0.72rem',
                        cursor: 'pointer',
                        whiteSpace: 'nowrap',
                        transition: 'all 0.15s ease'
                      }}
                      onMouseEnter={(e) => { e.currentTarget.style.color = 'var(--accent-cyan)'; e.currentTarget.style.borderColor = 'var(--accent-cyan)'; }}
                      onMouseLeave={(e) => { e.currentTarget.style.color = '#94a3b8'; e.currentTarget.style.borderColor = '#334155'; }}
                    >
                      {chip}
                    </button>
                  ))}
                </div>

                {/* Chat Input Bar */}
                <div style={{
                  padding: '0.5rem 0.75rem',
                  borderTop: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-card)',
                  display: 'flex',
                  gap: '8px'
                }}>
                  <input
                    type="text"
                    placeholder="Ask AI Mentor anything while coding (e.g. 'why is my pointer off by one?')..."
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
                    style={{
                      flex: 1,
                      padding: '0.45rem 0.75rem',
                      borderRadius: '8px',
                      border: '1px solid var(--border-subtle)',
                      backgroundColor: 'var(--bg-primary)',
                      color: 'var(--text-primary)',
                      fontSize: '0.82rem',
                      outline: 'none'
                    }}
                  />
                  <button
                    onClick={() => handleSendMessage()}
                    disabled={!chatInput.trim() || chatLoading}
                    className="btn-primary"
                    style={{ padding: '0.45rem 0.85rem', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <Send size={13} />
                    <span>Send</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: OPTIONAL SIDE-BY-SIDE DEDICATED AI CHAT DRAWER */}
        {showSideChat && (
          <div className="card-glass" style={{
            display: 'flex',
            flexDirection: 'column',
            height: 'calc(100vh - 180px)',
            overflow: 'hidden',
            border: '1px solid rgba(56, 189, 248, 0.3)'
          }}>
            {/* Header */}
            <div style={{
              padding: '0.75rem 1rem',
              backgroundColor: 'var(--bg-card)',
              borderBottom: '1px solid var(--border-subtle)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Bot size={18} style={{ color: 'var(--accent-cyan)' }} />
                <div>
                  <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#f8fafc' }}>
                    AI Code Companion
                  </div>
                  <div style={{ fontSize: '0.7rem', color: '#10b981' }}>
                    ● Active on {selectedProblem?.title}
                  </div>
                </div>
              </div>

              <button
                onClick={() => setShowSideChat(false)}
                style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}
              >
                <X size={16} />
              </button>
            </div>

            {/* Side Chat Messages Log */}
            <div style={{
              flex: 1,
              padding: '0.85rem',
              overflowY: 'auto',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem'
            }}>
              {chatMessages.map((msg, idx) => (
                <div
                  key={msg.id || idx}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start',
                    maxWidth: '94%',
                    alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start'
                  }}
                >
                  <div style={{
                    padding: '0.65rem 0.85rem',
                    borderRadius: '10px',
                    backgroundColor: msg.role === 'user' ? 'rgba(56, 189, 248, 0.15)' : '#0f172a',
                    border: `1px solid ${msg.role === 'user' ? 'rgba(56, 189, 248, 0.3)' : '#1e293b'}`,
                    color: msg.role === 'user' ? '#f8fafc' : '#e2e8f0',
                    fontSize: '0.82rem',
                    lineHeight: 1.5,
                    whiteSpace: 'pre-wrap'
                  }}>
                    {msg.role === 'assistant' && (
                      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: 'var(--accent-cyan)', fontWeight: 700, marginBottom: '4px', fontSize: '0.75rem' }}>
                        <Bot size={13} />
                        <span>AI Mentor</span>
                        <span style={{ color: '#64748b', fontWeight: 400, marginLeft: 'auto' }}>{msg.timestamp}</span>
                      </div>
                    )}
                    <div>{msg.content}</div>

                    {msg.codeSuggestion && (
                      <div style={{ marginTop: '0.5rem', backgroundColor: '#070b14', padding: '0.5rem', borderRadius: '6px', border: '1px solid #1e293b' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                          <span style={{ fontSize: '0.7rem', color: '#94a3b8' }}>Code Fix:</span>
                          <button
                            onClick={() => handleCopySnippet(msg.codeSuggestion, idx)}
                            style={{ background: 'none', border: 'none', color: 'var(--accent-cyan)', fontSize: '0.7rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '3px' }}
                          >
                            {copiedCodeIdx === idx ? <Check size={11} /> : <Copy size={11} />}
                            <span>{copiedCodeIdx === idx ? 'Copied' : 'Copy'}</span>
                          </button>
                        </div>
                        <pre style={{ margin: 0, fontFamily: 'monospace', fontSize: '0.76rem', color: '#10b981' }}>
                          {msg.codeSuggestion}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {chatLoading && (
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--accent-cyan)', fontSize: '0.78rem', padding: '0.5rem' }}>
                  <Sparkles size={14} className="pulse-glow" />
                  <span>Thinking...</span>
                </div>
              )}
              <div ref={chatBottomRef} />
            </div>

            {/* Quick Chips in Side Drawer */}
            <div style={{
              padding: '0.4rem 0.65rem',
              display: 'flex',
              gap: '4px',
              overflowX: 'auto',
              borderTop: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-primary)'
            }}>
              {[
                "Why is my code failing?",
                "Edge cases?",
                "Java example",
                "Optimize O(N)"
              ].map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => handleSendMessage(chip)}
                  disabled={chatLoading}
                  style={{
                    padding: '2px 7px',
                    borderRadius: '999px',
                    border: '1px solid #334155',
                    backgroundColor: '#0f172a',
                    color: '#94a3b8',
                    fontSize: '0.7rem',
                    cursor: 'pointer',
                    whiteSpace: 'nowrap'
                  }}
                >
                  {chip}
                </button>
              ))}
            </div>

            {/* Input Bar */}
            <div style={{
              padding: '0.5rem 0.65rem',
              borderTop: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-card)',
              display: 'flex',
              gap: '6px'
            }}>
              <input
                type="text"
                placeholder="Ask mentor while coding..."
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => { if (e.key === 'Enter') handleSendMessage(); }}
                style={{
                  flex: 1,
                  padding: '0.4rem 0.65rem',
                  borderRadius: '6px',
                  border: '1px solid var(--border-subtle)',
                  backgroundColor: 'var(--bg-primary)',
                  color: 'var(--text-primary)',
                  fontSize: '0.8rem',
                  outline: 'none'
                }}
              />
              <button
                onClick={() => handleSendMessage()}
                disabled={!chatInput.trim() || chatLoading}
                className="btn-primary"
                style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem' }}
              >
                <Send size={12} />
              </button>
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
