import React from 'react';
import { Flame, Calendar, Award, CheckCircle2, Sparkles, TrendingUp, Info } from 'lucide-react';
import ActivityHeatmap from '../components/ActivityHeatmap';

export default function StreaksPage({ onNavigate }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header Banner */}
      <div className="card-glass" style={{
        padding: '1.75rem 2.25rem',
        background: 'linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(16, 185, 129, 0.08) 100%)',
        border: '1px solid rgba(245, 158, 11, 0.3)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1.25rem',
        borderRadius: '18px'
      }}>
        <div style={{ maxWidth: '640px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', color: 'var(--accent-amber)', fontSize: '0.82rem', fontWeight: 700, textTransform: 'uppercase', marginBottom: '0.35rem' }}>
            <Flame size={18} fill="var(--accent-amber)" /> Learning Cadence & Continuity
          </div>
          <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
            GitHub & LeetCode Style Activity Heatmap
          </h1>
          <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)', lineHeight: 1.5, margin: 0 }}>
            Every submitted code test, completed algorithm lesson, and interactive visualizer run contributes to your persistent learning streak.
          </p>
        </div>

        <div style={{
          padding: '0.85rem 1.25rem',
          backgroundColor: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid rgba(255, 255, 255, 0.08)',
          borderRadius: '12px',
          display: 'flex',
          flexDirection: 'column',
          gap: '4px',
          fontSize: '0.78rem',
          color: 'var(--text-secondary)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#10B981', fontWeight: 700 }}>
            <CheckCircle2 size={14} /> Real-Time Auto Sync
          </div>
          <span>Calendar squares darken automatically as you finish DSA activities.</span>
        </div>
      </div>

      {/* Full 365-Day Activity Heatmap */}
      <ActivityHeatmap isLight={false} onNavigate={onNavigate} />
    </div>
  );
}
