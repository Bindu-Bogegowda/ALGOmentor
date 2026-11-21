import React, { useState } from 'react';
import { Bug, Sparkles, Play, CheckCircle2, AlertTriangle, Code2, ArrowRight } from 'lucide-react';
import { api } from '../services/api';

export default function DebuggerPage({ onNavigate }) {
  const [code, setCode] = useState(`def find_pair(nums, target):
    # Student solution with off-by-one or missing boundary
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

# Test with nums = [3, 2, 4], target = 6`);
  const [errorInput, setErrorInput] = useState('Output mismatch: returned [0, 0] instead of [1, 2] because element was used twice.');
  const [analysis, setAnalysis] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);

  async function handleAnalyze() {
    setAnalyzing(true);
    try {
      const res = await api.analyzeCode({
        language: 'python',
        code: code,
        runtime_error: errorInput
      });
      setAnalysis(res);
    } catch (err) {
      console.error('Debug error:', err);
    } finally {
      setAnalyzing(false);
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Header */}
      <div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
          <span className="badge badge-purple">AI DIAGNOSTIC ENGINE</span>
        </div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
          Intelligent Code Debugger
        </h1>
        <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
          Identify syntax bugs, runtime tracebacks, logical inversions, and time/space complexity bottlenecks without spoiling answers.
        </p>
      </div>

      {/* Main Grid: Code + Error input on left, AI Diagnosis on right */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '1.5rem' }}>
        {/* Left Inputs (6 cols) */}
        <div style={{ gridColumn: 'span 6', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Code input */}
          <div className="card-glass" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <label style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-primary)' }}>
                Your Solution Code (Python / Java)
              </label>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Python</span>
            </div>
            <textarea
              value={code}
              onChange={(e) => setCode(e.target.value)}
              spellCheck="false"
              style={{
                width: '100%',
                height: '220px',
                padding: '0.85rem',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                backgroundColor: '#070b14',
                color: '#f8fafc',
                fontFamily: 'Consolas, monospace',
                fontSize: '0.85rem',
                lineHeight: 1.5,
                outline: 'none',
                resize: 'vertical'
              }}
            />
          </div>

          {/* Error Message / Traceback Input */}
          <div className="card-glass" style={{ padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            <label style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              Execution Traceback or Failed Test Output
            </label>
            <textarea
              value={errorInput}
              onChange={(e) => setErrorInput(e.target.value)}
              placeholder="Paste exception traceback or description of incorrect output..."
              style={{
                width: '100%',
                height: '90px',
                padding: '0.75rem',
                borderRadius: '8px',
                border: '1px solid var(--border-subtle)',
                backgroundColor: 'var(--bg-primary)',
                color: 'var(--text-primary)',
                fontSize: '0.82rem',
                outline: 'none',
                resize: 'none'
              }}
            />
            <button
              onClick={handleAnalyze}
              disabled={analyzing}
              className="btn-primary"
              style={{ justifyContent: 'center', marginTop: '0.35rem' }}
            >
              <Bug size={16} /> {analyzing ? 'Analyzing Code & Invariants...' : 'Run Intelligent Diagnosis'}
            </button>
          </div>
        </div>

        {/* Right Diagnosis Card (6 cols) */}
        <div style={{ gridColumn: 'span 6' }}>
          {analysis ? (
            <div className="card-glass" style={{ padding: '1.75rem', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <div style={{
                  padding: '8px',
                  borderRadius: '10px',
                  backgroundColor: 'rgba(244, 63, 94, 0.15)',
                  color: 'var(--accent-rose)'
                }}>
                  <AlertTriangle size={22} />
                </div>
                <div>
                  <span className="badge badge-hard">{analysis.error_type}</span>
                  <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '2px' }}>
                    {analysis.summary}
                  </h3>
                </div>
              </div>

              {/* 1. Why it happened */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  1. Root Cause (Why It Happened)
                </h4>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  {analysis.why_it_happened}
                </p>
              </div>

              {/* 2. How to fix */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-emerald)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  2. Targeted Rectification (How To Fix)
                </h4>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  {analysis.how_to_fix}
                </p>
              </div>

              {/* 3. Recommended Approach */}
              <div>
                <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-purple)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                  3. Optimal Algorithmic Approach
                </h4>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
                  {analysis.suggested_approach}
                </p>
              </div>

              {/* Pseudocode hint */}
              {analysis.pseudocode_hint && (
                <div>
                  <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-amber)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                    4. Structural Pseudocode Pattern
                  </h4>
                  <pre style={{
                    backgroundColor: '#050811',
                    padding: '0.85rem',
                    borderRadius: '8px',
                    border: '1px solid rgba(255,255,255,0.08)',
                    color: '#f59e0b',
                    fontSize: '0.82rem',
                    fontFamily: 'Consolas, monospace',
                    margin: 0,
                    lineHeight: 1.5
                  }}>
                    {analysis.pseudocode_hint}
                  </pre>
                </div>
              )}

              <button
                onClick={() => onNavigate('practice')}
                className="btn-secondary"
                style={{ justifyContent: 'center' }}
              >
                Apply Fix in Practice Bank <ArrowRight size={14} />
              </button>
            </div>
          ) : (
            <div className="card-glass" style={{
              padding: '3rem 2rem',
              textAlign: 'center',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              height: '100%',
              color: 'var(--text-muted)'
            }}>
              <Bug size={40} style={{ color: 'var(--accent-cyan)', marginBottom: '1rem', opacity: 0.6 }} />
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
                Awaiting Solution Code
              </h3>
              <p style={{ fontSize: '0.85rem', maxWidth: '380px', lineHeight: 1.5 }}>
                Paste your solution and any runtime traceback or output discrepancy on the left, then click <strong>Run Intelligent Diagnosis</strong>.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
