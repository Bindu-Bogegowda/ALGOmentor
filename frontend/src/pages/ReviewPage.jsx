import React, { useState, useEffect } from 'react';
import { 
  CalendarCheck, 
  Sparkles, 
  CheckCircle2, 
  AlertTriangle, 
  ArrowRight, 
  Target, 
  Lightbulb, 
  BookmarkCheck,
  TrendingUp
} from 'lucide-react';
import { api } from '../services/api';

export default function ReviewPage({ onNavigate }) {
  const [review, setReview] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadReview();
  }, []);

  async function loadReview() {
    try {
      const data = await api.getDailyReview();
      setReview(data);
    } catch (err) {
      console.error('Failed to load daily performance review:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
        <Sparkles size={32} className="pulse-glow" style={{ color: 'var(--accent-purple)' }} />
      </div>
    );
  }

  const r = review || {
    review_date: '2026-11-20',
    overall_summary: 'Your algorithm telemetry demonstrates steady mastery across linear data structures.',
    strengths: ['Optimal Hash Map lookup', 'Clean Big-O derivations'],
    common_mistakes: ['Off-by-one boundary checks in while loops'],
    concepts_to_improve: ['Graph BFS queue state transitions'],
    recommended_revisions: ['Binary search loop invariants'],
    next_day_plan: ['Solve 1 Graph traversal problem'],
    achievable_targets: ['Unlock 6-day streak record'],
    metrics: { problems_attempted: 2, problems_solved: 2, accuracy: 100, active_minutes: 55 }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header Banner */}
      <div className="card-glass" style={{
        padding: '1.75rem 2rem',
        background: 'linear-gradient(135deg, rgba(147, 51, 234, 0.15) 0%, rgba(2, 132, 199, 0.12) 100%)',
        border: '1px solid rgba(168, 85, 247, 0.3)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        <div style={{ maxWidth: '650px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--accent-purple)', fontSize: '0.82rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '0.35rem' }}>
            <CalendarCheck size={18} /> Daily AI Performance Review ({r.review_date})
          </div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.5rem' }}>
            Algorithmic Diagnostic Synthesis
          </h1>
          <p style={{ fontSize: '0.95rem', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
            {r.overall_summary}
          </p>
        </div>

        <div style={{
          display: 'flex',
          gap: '1.25rem',
          backgroundColor: 'var(--bg-primary)',
          padding: '1rem 1.25rem',
          borderRadius: '12px',
          border: '1px solid var(--border-subtle)'
        }}>
          <div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Solved Today</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-emerald)' }}>
              {r.metrics.problems_solved || 0}
            </div>
          </div>
          <div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Active Time</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
              {r.metrics.active_minutes || 0}m
            </div>
          </div>
          <div>
            <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Accuracy</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--accent-purple)' }}>
              {r.metrics.accuracy || 100}%
            </div>
          </div>
        </div>
      </div>

      {/* The 7 Core Pillars of Daily Review */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '1.25rem' }}>
        {/* Pillar 2: Strengths (6 cols) */}
        <div className="card-glass" style={{ gridColumn: 'span 6', padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1rem' }}>
            <div style={{ padding: '6px', borderRadius: '8px', backgroundColor: 'rgba(16, 185, 129, 0.15)', color: 'var(--accent-emerald)' }}>
              <CheckCircle2 size={18} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              2. Areas of High Performance & Strengths
            </h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {(r.strengths || []).map((s, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(16, 185, 129, 0.08)',
                border: '1px solid rgba(16, 185, 129, 0.2)',
                fontSize: '0.88rem',
                color: 'var(--text-primary)'
              }}>
                ✓ {s}
              </div>
            ))}
          </div>
        </div>

        {/* Pillar 3: Common Mistakes (6 cols) */}
        <div className="card-glass" style={{ gridColumn: 'span 6', padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1rem' }}>
            <div style={{ padding: '6px', borderRadius: '8px', backgroundColor: 'rgba(244, 63, 94, 0.15)', color: 'var(--accent-rose)' }}>
              <AlertTriangle size={18} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              3. Common Mistakes & Sub-optimal Patterns
            </h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {(r.common_mistakes || []).map((m, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(244, 63, 94, 0.08)',
                border: '1px solid rgba(244, 63, 94, 0.2)',
                fontSize: '0.88rem',
                color: 'var(--text-primary)'
              }}>
                ⚠ {m}
              </div>
            ))}
          </div>
        </div>

        {/* Pillar 4 & 5: Concepts Needing Improvement & Recommended Revisions (6 cols) */}
        <div className="card-glass" style={{ gridColumn: 'span 6', padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1rem' }}>
            <div style={{ padding: '6px', borderRadius: '8px', backgroundColor: 'rgba(245, 158, 11, 0.15)', color: 'var(--accent-amber)' }}>
              <Lightbulb size={18} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              4 & 5. Concepts & Recommended Revisions
            </h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {(r.concepts_to_improve || []).map((c, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                borderRadius: '8px',
                backgroundColor: 'var(--bg-primary)',
                border: '1px solid var(--border-subtle)',
                fontSize: '0.88rem',
                color: 'var(--text-secondary)'
              }}>
                • <strong>Focus:</strong> {c}
              </div>
            ))}
            {(r.recommended_revisions || []).map((rev, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                borderRadius: '8px',
                backgroundColor: 'var(--bg-primary)',
                border: '1px solid var(--border-subtle)',
                fontSize: '0.88rem',
                color: 'var(--text-secondary)'
              }}>
                • <strong>Revision:</strong> {rev}
              </div>
            ))}
          </div>
        </div>

        {/* Pillar 6 & 7: Next Day Plan & Achievable Targets (6 cols) */}
        <div className="card-glass" style={{ gridColumn: 'span 6', padding: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem', marginBottom: '1rem' }}>
            <div style={{ padding: '6px', borderRadius: '8px', backgroundColor: 'rgba(56, 189, 248, 0.15)', color: 'var(--accent-cyan)' }}>
              <Target size={18} />
            </div>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
              6 & 7. Actionable Next Day Plan & Daily Targets
            </h3>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {(r.next_day_plan || []).map((plan, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(56, 189, 248, 0.08)',
                border: '1px solid rgba(56, 189, 248, 0.25)',
                fontSize: '0.88rem',
                color: 'var(--text-primary)'
              }}>
                🎯 <strong>Step:</strong> {plan}
              </div>
            ))}
            {(r.achievable_targets || []).map((target, idx) => (
              <div key={idx} style={{
                padding: '0.75rem',
                borderRadius: '8px',
                backgroundColor: 'rgba(168, 85, 247, 0.08)',
                border: '1px solid rgba(168, 85, 247, 0.25)',
                fontSize: '0.88rem',
                color: 'var(--text-primary)'
              }}>
                🏆 <strong>Target:</strong> {target}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
