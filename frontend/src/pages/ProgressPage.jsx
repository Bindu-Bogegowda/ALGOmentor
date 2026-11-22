import React, { useState, useEffect } from 'react';
import { Award, CheckCircle2, Code2, BookOpen, TrendingUp, Target, Sparkles, ArrowRight } from 'lucide-react';
import { api } from '../services/api';
import ActivityHeatmap from '../components/ActivityHeatmap';

export default function ProgressPage({ onNavigate }) {
  const [mastery, setMastery] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMastery();
  }, []);

  async function loadMastery() {
    try {
      const data = await api.getMastery();
      setMastery(data);
    } catch (err) {
      console.error('Failed to load mastery data:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
        <Sparkles size={32} className="pulse-glow" style={{ color: 'var(--accent-cyan)' }} />
      </div>
    );
  }

  const m = mastery || {
    total_concepts: 0,
    completed_concepts: 0,
    concept_completion_pct: 0.0,
    total_problems: 0,
    solved_problems: 0,
    attempted_problems: 0,
    unsolved_problems: 0,
    total_submissions: 0,
    accuracy_pct: 0.0,
    topic_breakdown: [],
    learning_consistency: 'Starting Journey'
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
          Progress & Algorithmic Mastery Tracker
        </h1>
        <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
          Real-time metrics, submission accuracy, and topic-wise competency benchmarks derived from actual database records.
        </p>
      </div>

      {/* 4 Core Quantitative Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
        <div className="card-glass" style={{ padding: '1.5rem' }}>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            CONCEPTS MASTERED
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
            {m.completed_concepts} <span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>/ {m.total_concepts}</span>
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--accent-cyan)', fontWeight: 600 }}>
            {m.concept_completion_pct}% Curriculum Covered
          </div>
        </div>

        <div className="card-glass" style={{ padding: '1.5rem' }}>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            PROBLEMS SOLVED
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--accent-emerald)', marginBottom: '0.35rem' }}>
            {m.solved_problems} <span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>/ {m.total_problems}</span>
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Attempted: {m.attempted_problems} • Remaining: {m.unsolved_problems}
          </div>
        </div>

        <div className="card-glass" style={{ padding: '1.5rem' }}>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            SUBMISSION ACCURACY
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--accent-purple)', marginBottom: '0.35rem' }}>
            {m.accuracy_pct}%
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Across {m.total_submissions} total code submissions
          </div>
        </div>

        <div className="card-glass" style={{ padding: '1.5rem' }}>
          <div style={{ fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
            LEARNING CONSISTENCY
          </div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--accent-amber)', marginBottom: '0.35rem' }}>
            {m.learning_consistency}
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            Active problem solving cadence
          </div>
        </div>
      </div>

      {/* Topic-Wise Mastery Progress Bars */}
      <div className="card-glass" style={{ padding: '1.75rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '1.25rem' }}>
          Topic-Wise Competency Breakdown
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {m.topic_breakdown.map((t, idx) => (
            <div key={idx} style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontWeight: 600, fontSize: '0.92rem', color: 'var(--text-primary)' }}>
                  {t.topic}
                </span>
                <span style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--accent-cyan)' }}>
                  {t.solved} / {t.total} ({t.percentage}%)
                </span>
              </div>
              <div style={{
                width: '100%',
                height: '8px',
                backgroundColor: 'rgba(255,255,255,0.06)',
                borderRadius: '999px',
                overflow: 'hidden'
              }}>
                <div style={{
                  width: `${t.percentage}%`,
                  height: '100%',
                  background: t.percentage === 100 
                    ? 'linear-gradient(90deg, #10b981 0%, #34d399 100%)' 
                    : 'linear-gradient(90deg, #0284c7 0%, #38bdf8 100%)',
                  borderRadius: '999px',
                  transition: 'width 0.8s ease'
                }} />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* GitHub/LeetCode Style Activity Calendar */}
      <ActivityHeatmap isLight={false} onNavigate={onNavigate} />
    </div>
  );
}
