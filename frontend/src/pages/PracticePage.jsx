import React, { useState, useEffect } from 'react';
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
  Send
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
  const [activeTab, setActiveTab] = useState('testcases'); // 'testcases', 'output', 'hints'

  // Hint system
  const [hintLevel, setHintLevel] = useState(0);
  const [hints, setHints] = useState({});
  const [loadingHint, setLoadingHint] = useState(false);

  // Filters
  const [search, setSearch] = useState('');
  const [filterDifficulty, setFilterDifficulty] = useState('All');
  const [filterTopic, setFilterTopic] = useState('All');

  useEffect(() => {
    loadProblems();
  }, []);

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
      setActiveTab('testcases');
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

  async function fetchHint(level) {
    if (!selectedProblem || loadingHint) return;
    setLoadingHint(true);
    try {
      const res = await api.getHint(selectedProblem.id, level);
      setHints(prev => ({ ...prev, [level]: res.content }));
      setHintLevel(Math.max(hintLevel, level));
    } catch (err) {
      console.error('Failed to fetch hint:', err);
    } finally {
      setLoadingHint(false);
    }
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
    const matchesSearch = p.title.toLowerCase().includes(search.toLowerCase()) || p.topic.toLowerCase().includes(search.toLowerCase());
    const matchesDiff = filterDifficulty === 'All' || p.difficulty.toLowerCase() === filterDifficulty.toLowerCase();
    const matchesTopic = filterTopic === 'All' || p.topic.toLowerCase() === filterTopic.toLowerCase();
    return matchesSearch && matchesDiff && matchesTopic;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', height: 'calc(100vh - 100px)' }}>
      {/* Top Filter Bar */}
      <div className="card-glass" style={{ padding: '0.75rem 1.25rem', display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '0.75rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flex: 1, minWidth: '240px' }}>
          <div style={{ position: 'relative', width: '100%', maxWidth: '280px' }}>
            <Search size={14} style={{ position: 'absolute', left: '10px', top: '10px', color: 'var(--text-muted)' }} />
            <input
              type="text"
              placeholder="Search problems or patterns..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              style={{
                width: '100%',
                padding: '0.45rem 0.75rem 0.45rem 2rem',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                backgroundColor: 'var(--bg-primary)',
                color: 'var(--text-primary)',
                fontSize: '0.82rem',
                outline: 'none'
              }}
            />
          </div>

          <div style={{ display: 'flex', gap: '4px' }}>
            {['All', 'Easy', 'Medium', 'Hard'].map(d => (
              <button
                key={d}
                onClick={() => setFilterDifficulty(d)}
                style={{
                  padding: '0.35rem 0.65rem',
                  borderRadius: '6px',
                  border: filterDifficulty === d ? '1px solid var(--accent-cyan)' : '1px solid var(--border-subtle)',
                  backgroundColor: filterDifficulty === d ? 'rgba(56, 189, 248, 0.15)' : 'var(--bg-primary)',
                  color: filterDifficulty === d ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                {d}
              </button>
            ))}
          </div>
        </div>

        {/* Selected Problem Pill Selector Dropdown */}
        <select
          value={selectedProblem?.slug || ''}
          onChange={(e) => selectProblem(e.target.value)}
          style={{
            padding: '0.45rem 0.85rem',
            borderRadius: '8px',
            border: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-primary)',
            color: 'var(--text-primary)',
            fontSize: '0.85rem',
            outline: 'none',
            fontWeight: 600,
            cursor: 'pointer'
          }}
        >
          {filteredProblems.map(p => (
            <option key={p.id} value={p.slug}>
              {p.status === 'Solved' ? '✓ ' : ''}{p.title} ({p.difficulty})
            </option>
          ))}
        </select>
      </div>

      {/* Main Split-Screen Coding Interface (Inspired by Image 2 PySchool.ai) */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1.15fr', gap: '1.25rem', flex: 1, minHeight: 0 }}>
        {/* Left Side: Problem Statement & Test Case Details */}
        <div className="card-glass" style={{
          padding: '1.5rem',
          display: 'flex',
          flexDirection: 'column',
          overflowY: 'auto'
        }}>
          {selectedProblem ? (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
                    <span className={`badge ${
                      selectedProblem.difficulty === 'Easy' ? 'badge-easy' :
                      selectedProblem.difficulty === 'Medium' ? 'badge-medium' : 'badge-hard'
                    }`}>
                      {selectedProblem.difficulty}
                    </span>
                    <span className="badge badge-purple">{selectedProblem.topic}</span>
                    <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                      Pattern: {selectedProblem.algorithmic_pattern}
                    </span>
                  </div>
                  <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--text-primary)' }}>
                    {selectedProblem.title}
                  </h2>
                </div>

                <button
                  onClick={handleBookmark}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: selectedProblem.is_bookmarked ? 'var(--accent-amber)' : 'var(--text-muted)',
                    cursor: 'pointer',
                    padding: '6px'
                  }}
                  title="Bookmark for Revision"
                >
                  <Bookmark size={20} fill={selectedProblem.is_bookmarked ? 'var(--accent-amber)' : 'none'} />
                </button>
              </div>

              {/* Problem Description */}
              <div style={{ fontSize: '0.9rem', color: 'var(--text-primary)', lineHeight: 1.6, whiteSpace: 'pre-wrap' }}>
                {selectedProblem.description}
              </div>

              {/* Constraints */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  Constraints:
                </h4>
                <div style={{
                  backgroundColor: 'var(--bg-primary)',
                  padding: '0.75rem',
                  borderRadius: '8px',
                  border: '1px solid var(--border-subtle)',
                  fontSize: '0.8rem',
                  fontFamily: 'Consolas, monospace',
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

        {/* Right Side: Code Editor & Execution Runner Console */}
        <div className="card-glass" style={{
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden'
        }}>
          {/* Editor Header Bar (Language, Hints, Run, Submit) */}
          <div style={{
            padding: '0.75rem 1rem',
            borderBottom: '1px solid var(--border-subtle)',
            backgroundColor: 'var(--bg-card)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between'
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

              {/* 3-Level Hint Trigger */}
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
                  gap: '4px'
                }}
              >
                <HelpCircle size={14} /> Hints ({hintLevel}/3)
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
          <div style={{ flex: 1, minHeight: '260px', position: 'relative', backgroundColor: '#070b14' }}>
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
            height: '240px',
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
                { id: 'hints', label: 'Progressive Hints' }
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

            {/* Tab 1: Sample Test Cases & Custom Input */}
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
                      height: '100px',
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

            {/* Tab 2: Console Output & Test Results */}
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

            {/* Tab 3: 3-Level Progressive Hint System */}
            {activeTab === 'hints' && (
              <div style={{ flex: 1, padding: '1rem', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
                  Unlock progressive clues without spoiling the entire solution:
                </div>

                {/* Level 1 Hint */}
                <div style={{ padding: '0.75rem', borderRadius: '8px', backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '0.85rem', color: 'var(--accent-cyan)' }}>Level 1: Conceptual Clue</strong>
                    {!hints[1] && (
                      <button
                        onClick={() => fetchHint(1)}
                        className="btn-secondary"
                        style={{ padding: '0.25rem 0.55rem', fontSize: '0.72rem' }}
                      >
                        Reveal Level 1
                      </button>
                    )}
                  </div>
                  {hints[1] && <p style={{ fontSize: '0.82rem', marginTop: '6px', color: 'var(--text-primary)' }}>{hints[1]}</p>}
                </div>

                {/* Level 2 Hint */}
                <div style={{ padding: '0.75rem', borderRadius: '8px', backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '0.85rem', color: 'var(--accent-purple)' }}>Level 2: Algorithmic Direction</strong>
                    {!hints[2] && (
                      <button
                        onClick={() => fetchHint(2)}
                        disabled={!hints[1]}
                        className="btn-secondary"
                        style={{ padding: '0.25rem 0.55rem', fontSize: '0.72rem', opacity: !hints[1] ? 0.5 : 1 }}
                      >
                        Reveal Level 2
                      </button>
                    )}
                  </div>
                  {hints[2] && <p style={{ fontSize: '0.82rem', marginTop: '6px', color: 'var(--text-primary)' }}>{hints[2]}</p>}
                </div>

                {/* Level 3 Hint */}
                <div style={{ padding: '0.75rem', borderRadius: '8px', backgroundColor: 'var(--bg-primary)', border: '1px solid var(--border-subtle)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <strong style={{ fontSize: '0.85rem', color: 'var(--accent-amber)' }}>Level 3: Pseudocode Blueprint</strong>
                    {!hints[3] && (
                      <button
                        onClick={() => fetchHint(3)}
                        disabled={!hints[2]}
                        className="btn-secondary"
                        style={{ padding: '0.25rem 0.55rem', fontSize: '0.72rem', opacity: !hints[2] ? 0.5 : 1 }}
                      >
                        Reveal Level 3
                      </button>
                    )}
                  </div>
                  {hints[3] && (
                    <pre style={{ fontSize: '0.8rem', marginTop: '6px', color: '#f59e0b', fontFamily: 'Consolas, monospace', whiteSpace: 'pre-wrap' }}>
                      {hints[3]}
                    </pre>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
