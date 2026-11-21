import React, { useState, useEffect } from 'react';
import { BarChart3, Clock, Code2, BookOpen, TrendingUp, Sparkles, PieChart } from 'lucide-react';
import { api } from '../services/api';

export default function AnalyticsPage() {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  async function loadAnalytics() {
    try {
      const data = await api.getWeeklyAnalytics();
      setAnalytics(data);
    } catch (err) {
      console.error('Failed to load weekly analytics:', err);
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

  const a = analytics || {
    total_weekly_hours: 4.5,
    active_days_count: 5,
    coding_time_pct: 65.0,
    concept_time_pct: 35.0,
    daily_breakdown: [
      { day: 'Mon', concept_hours: 0.3, coding_hours: 0.5, visualizer_hours: 0.2, problems_solved: 0 },
      { day: 'Tue', concept_hours: 0.5, coding_hours: 0.7, visualizer_hours: 0.2, problems_solved: 1 },
      { day: 'Wed', concept_hours: 0.2, coding_hours: 0.3, visualizer_hours: 0.1, problems_solved: 0 },
      { day: 'Thu', concept_hours: 0.6, coding_hours: 0.9, visualizer_hours: 0.3, problems_solved: 1 },
      { day: 'Fri', concept_hours: 0.4, coding_hours: 0.5, visualizer_hours: 0.1, problems_solved: 0 },
      { day: 'Sat', concept_hours: 0.8, coding_hours: 1.0, visualizer_hours: 0.4, problems_solved: 1 },
      { day: 'Sun', concept_hours: 0.2, coding_hours: 0.4, visualizer_hours: 0.1, problems_solved: 0 }
    ],
    topic_distribution: [
      { topic: 'Data Structures', hours: 2.4, percentage: 45 },
      { topic: 'Sorting & Searching', hours: 1.6, percentage: 30 },
      { topic: 'Graph Algorithms', hours: 0.8, percentage: 15 },
      { topic: 'Dynamic Programming', hours: 0.5, percentage: 10 }
    ],
    trend_comparison: '+18% increase in focused problem solving compared to previous week.'
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.35rem' }}>
          Weekly & Monthly Learning Analytics
        </h1>
        <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
          Detailed telemetry across concept study, coding execution, interactive visualizer steps, and weekly trends.
        </p>
      </div>

      {/* Top 3 Metric Cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem' }}>
        <div className="card-glass" style={{ padding: '1.5rem' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>TOTAL WEEKLY STUDY</div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
            {a.total_weekly_hours} <span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>hours</span>
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--accent-emerald)', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <TrendingUp size={14} /> {a.trend_comparison}
          </div>
        </div>

        <div className="card-glass" style={{ padding: '1.5rem' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>ACTIVE DAYS CADENCE</div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--accent-cyan)', marginBottom: '0.25rem' }}>
            {a.active_days_count} <span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>/ 7 days</span>
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            71% active day density this week
          </div>
        </div>

        <div className="card-glass" style={{ padding: '1.5rem' }}>
          <div style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.4rem' }}>TIME ALLOCATION RATIO</div>
          <div style={{ fontSize: '2.2rem', fontWeight: 800, color: 'var(--accent-purple)', marginBottom: '0.25rem' }}>
            {a.coding_time_pct}% <span style={{ fontSize: '1.1rem', color: 'var(--text-muted)' }}>Coding</span>
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
            {a.concept_time_pct}% Concept Foundations
          </div>
        </div>
      </div>

      {/* Daily Breakdown Stacked Bar Chart */}
      <div className="card-glass" style={{ padding: '1.75rem' }}>
        <h3 style={{ fontSize: '1.2rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.25rem' }}>
          Daily Hours Breakdown (Mon - Sun)
        </h3>
        <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: '1.5rem' }}>
          Light Blue: Concept Lessons | Deep Blue: Coding Practice | Purple: Visualizer Exploration
        </p>

        <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', height: '220px', padding: '0 1rem' }}>
          {a.daily_breakdown.map((d, i) => {
            const totalH = d.concept_hours + d.coding_hours + d.visualizer_hours;
            const heightPct = Math.min(100, (totalH / 2.5) * 100);
            return (
              <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', width: '48px' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: 'var(--text-muted)' }}>
                  {totalH.toFixed(1)}h
                </span>

                <div style={{
                  width: '100%',
                  height: '160px',
                  backgroundColor: 'rgba(255,255,255,0.03)',
                  borderRadius: '8px',
                  display: 'flex',
                  flexDirection: 'column-reverse',
                  overflow: 'hidden'
                }}>
                  {/* Coding hours */}
                  <div style={{
                    width: '100%',
                    height: `${(d.coding_hours / Math.max(0.1, totalH)) * heightPct}%`,
                    backgroundColor: '#0284c7'
                  }} title={`Coding: ${d.coding_hours}h`} />
                  {/* Concept hours */}
                  <div style={{
                    width: '100%',
                    height: `${(d.concept_hours / Math.max(0.1, totalH)) * heightPct}%`,
                    backgroundColor: '#38bdf8'
                  }} title={`Concepts: ${d.concept_hours}h`} />
                  {/* Visualizer hours */}
                  <div style={{
                    width: '100%',
                    height: `${(d.visualizer_hours / Math.max(0.1, totalH)) * heightPct}%`,
                    backgroundColor: '#a855f7'
                  }} title={`Visualizer: ${d.visualizer_hours}h`} />
                </div>

                <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-primary)' }}>{d.day}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
