import React, { useState, useEffect } from 'react';
import { 
  Map, 
  Layers, 
  Brain, 
  Cpu, 
  Code2, 
  GitFork, 
  Sliders, 
  Terminal, 
  CheckCircle, 
  Lock, 
  Clock, 
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { api } from '../services/api';

const STREAM_ICONS = {
  dsa: Layers,
  aiml: Brain,
  dl: Cpu,
  daa: Code2,
  graph: GitFork,
  optimization: Sliders,
  computational: Terminal
};

export default function RoadmapsPage({ onNavigate, onSelectLesson }) {
  const [streams, setStreams] = useState([]);
  const [activeStreamId, setActiveStreamId] = useState('dsa');
  const [activeLevel, setActiveLevel] = useState('All');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStreams();
  }, []);

  async function loadStreams() {
    try {
      const data = await api.listRoadmaps();
      setStreams(data);
    } catch (err) {
      console.error('Failed to load roadmap streams:', err);
    } finally {
      setLoading(false);
    }
  }

  const activeStream = streams.find(s => s.id === activeStreamId) || streams[0];
  const levels = ['All', 'Beginner', 'Intermediate', 'Advanced', 'Master'];

  const filteredTopics = (activeStream?.topics || []).filter(t => {
    if (activeLevel === 'All') return true;
    return t.level.toLowerCase() === activeLevel.toLowerCase();
  });

  if (loading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
        <Sparkles size={32} className="pulse-glow" style={{ color: 'var(--accent-cyan)' }} />
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.75rem' }}>
      {/* Header */}
      <div>
        <h1 style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
          Multi-Disciplinary Algorithm Roadmaps
        </h1>
        <p style={{ fontSize: '0.92rem', color: 'var(--text-secondary)' }}>
          Explore foundational and cutting-edge algorithm disciplines across Beginner, Intermediate, Advanced, and Master tiers.
        </p>
      </div>

      {/* Stream Tabs Bar */}
      <div style={{
        display: 'flex',
        gap: '0.75rem',
        overflowX: 'auto',
        paddingBottom: '0.5rem'
      }}>
        {streams.map((s) => {
          const Icon = STREAM_ICONS[s.id] || Map;
          const isSelected = s.id === activeStreamId;
          return (
            <button
              key={s.id}
              onClick={() => { setActiveStreamId(s.id); setActiveLevel('All'); }}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.6rem',
                padding: '0.65rem 1.1rem',
                borderRadius: '12px',
                border: isSelected ? '1px solid var(--accent-cyan)' : '1px solid var(--border-subtle)',
                backgroundColor: isSelected ? 'rgba(56, 189, 248, 0.12)' : 'var(--bg-card)',
                color: isSelected ? 'var(--accent-cyan)' : 'var(--text-secondary)',
                fontWeight: isSelected ? 700 : 500,
                fontSize: '0.86rem',
                cursor: 'pointer',
                whiteSpace: 'nowrap',
                transition: 'all 0.2s'
              }}
            >
              <Icon size={16} />
              <span>{s.title.split(' ')[0]} {s.title.includes('DSA') ? '(DSA)' : ''}</span>
              <span style={{
                fontSize: '0.72rem',
                padding: '0.1rem 0.4rem',
                borderRadius: '999px',
                backgroundColor: isSelected ? 'var(--accent-cyan)' : 'var(--border-subtle)',
                color: isSelected ? '#000' : 'var(--text-muted)',
                fontWeight: 700
              }}>
                {s.user_completion_pct}%
              </span>
            </button>
          );
        })}
      </div>

      {/* Active Stream Overview Hero */}
      {activeStream && (
        <div className="card-glass" style={{ padding: '1.75rem 2rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
            <div>
              <span className="badge badge-cyan" style={{ marginBottom: '0.5rem' }}>
                {activeStream.category.toUpperCase()} STREAM
              </span>
              <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'var(--text-primary)', marginTop: '0.35rem' }}>
                {activeStream.title}
              </h2>
              <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '0.35rem', maxWidth: '750px' }}>
                {activeStream.description}
              </p>
            </div>
            <div style={{
              display: 'flex',
              gap: '1.5rem',
              backgroundColor: 'var(--bg-primary)',
              padding: '0.85rem 1.25rem',
              borderRadius: '12px',
              border: '1px solid var(--border-subtle)'
            }}>
              <div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Estimated Effort</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--text-primary)' }}>{activeStream.total_hours_estimate} hrs</div>
              </div>
              <div>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 600 }}>Curriculum Progress</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>{activeStream.user_completion_pct}%</div>
              </div>
            </div>
          </div>

          {/* Level Filter Buttons */}
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', borderTop: '1px solid var(--border-subtle)', paddingTop: '1.25rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', marginRight: '0.5rem' }}>Filter Level:</span>
            {levels.map(lvl => (
              <button
                key={lvl}
                onClick={() => setActiveLevel(lvl)}
                style={{
                  padding: '0.35rem 0.85rem',
                  borderRadius: '8px',
                  border: activeLevel === lvl ? '1px solid var(--accent-cyan)' : '1px solid var(--border-subtle)',
                  backgroundColor: activeLevel === lvl ? 'var(--accent-cyan)' : 'var(--bg-primary)',
                  color: activeLevel === lvl ? '#000000' : 'var(--text-secondary)',
                  fontSize: '0.8rem',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                {lvl}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Topics Progression Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '1.25rem' }}>
        {filteredTopics.map((topic, idx) => {
          const isDone = topic.is_completed;
          const isUnlocked = topic.is_unlocked;
          return (
            <div
              key={topic.id}
              className="card-glass"
              style={{
                padding: '1.5rem',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                opacity: isUnlocked ? 1 : 0.6,
                border: isDone ? '1px solid rgba(16, 185, 129, 0.4)' : undefined
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <span className={`badge ${
                    topic.level === 'Beginner' ? 'badge-easy' :
                    topic.level === 'Intermediate' ? 'badge-cyan' :
                    topic.level === 'Advanced' ? 'badge-medium' : 'badge-hard'
                  }`}>
                    {topic.level}
                  </span>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    {isDone ? (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--accent-emerald)', fontSize: '0.78rem', fontWeight: 700 }}>
                        <CheckCircle size={15} /> Completed
                      </span>
                    ) : isUnlocked ? (
                      <span style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 600 }}>
                        Unlocked
                      </span>
                    ) : (
                      <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                        <Lock size={14} /> Locked
                      </span>
                    )}
                  </div>
                </div>

                <h3 style={{ fontSize: '1.15rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: '0.4rem' }}>
                  {topic.title}
                </h3>
                <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', lineHeight: 1.5, marginBottom: '1rem' }}>
                  {topic.description}
                </p>
              </div>

              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '0.85rem' }}>
                  <span style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Clock size={13} /> {topic.estimated_minutes} mins
                  </span>
                  <span>Milestone: <strong>{topic.milestone_tag}</strong></span>
                </div>

                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <button
                    onClick={() => onNavigate('concepts')}
                    disabled={!isUnlocked}
                    className="btn-primary"
                    style={{ flex: 1, justifyContent: 'center', fontSize: '0.82rem', padding: '0.55rem' }}
                  >
                    Study Lesson <ArrowRight size={14} />
                  </button>
                  <button
                    onClick={() => onNavigate('practice')}
                    className="btn-secondary"
                    style={{ fontSize: '0.82rem', padding: '0.55rem 0.85rem' }}
                  >
                    Practice
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
