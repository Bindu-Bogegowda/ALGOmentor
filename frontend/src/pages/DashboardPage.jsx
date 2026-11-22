import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  CheckCircle2, 
  Flame, 
  ArrowRight, 
  TrendingUp, 
  Sparkles, 
  Laptop, 
  Code, 
  Link2, 
  Layers, 
  Network, 
  Compass, 
  Grid, 
  Star, 
  Lock, 
  Check, 
  Lightbulb, 
  Rocket, 
  ChevronRight,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';
import ActivityHeatmap from '../components/ActivityHeatmap';

export default function DashboardPage({ user, onNavigate, onTriggerAI }) {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [perfTimeframe, setPerfTimeframe] = useState('1M'); // '1W', '1M', '3M'

  useEffect(() => {
    loadDashboard();
  }, [user]);

  async function loadDashboard() {
    try {
      const data = await api.getDashboardStats();
      setStats(data);
    } catch (err) {
      console.error('Failed to load dashboard stats:', err);
    } finally {
      setLoading(false);
    }
  }

  const s = stats || {
    welcome_message: `Welcome back, ${user?.full_name || user?.username || 'Learner'}! 👋`,
    user_name: user?.full_name || user?.username || 'Learner',
    current_roadmap: 'Data Structures & Algorithms',
    current_level: user?.difficulty_level || 'Beginner',
    concepts_completed: 0,
    total_concepts: 87,
    problems_solved: 0,
    problems_attempted: 0,
    total_problems: 120,
    current_streak: 0,
    longest_streak: 0,
    weekly_learning_hours: 0.0,
    mastery_percentage: 0.0,
    recommended_lessons: []
  };

  const completedConceptsCount = s.concepts_completed ?? 0;
  const problemsSolvedCount = s.problems_solved ?? 0;
  const currentStreakCount = s.current_streak ?? 0;
  const masteryPct = s.mastery_percentage ?? 0;

  const ROADMAP_STEPS = [
    { 
      id: 'step1', 
      title: 'Programming\nFundamentals', 
      icon: Laptop, 
      status: completedConceptsCount >= 1 ? 'completed' : 'current' 
    },
    { 
      id: 'step2', 
      title: 'Arrays &\nStrings', 
      icon: Code, 
      status: completedConceptsCount >= 3 ? 'completed' : completedConceptsCount >= 1 ? 'current' : 'locked' 
    },
    { 
      id: 'step3', 
      title: 'Linked\nLists', 
      icon: Link2, 
      status: completedConceptsCount >= 6 ? 'completed' : completedConceptsCount >= 3 ? 'current' : 'locked' 
    },
    { 
      id: 'step4', 
      title: 'Stacks &\nQueues', 
      icon: Layers, 
      status: completedConceptsCount >= 10 ? 'completed' : completedConceptsCount >= 6 ? 'current' : 'locked' 
    },
    { 
      id: 'step5', 
      title: 'Trees &\nGraphs', 
      icon: Network, 
      status: completedConceptsCount >= 15 ? 'completed' : completedConceptsCount >= 10 ? 'current' : 'locked' 
    },
    { 
      id: 'step6', 
      title: 'Greedy\nAlgorithms', 
      icon: Compass, 
      status: completedConceptsCount >= 20 ? 'completed' : completedConceptsCount >= 15 ? 'current' : 'locked' 
    },
    { 
      id: 'step7', 
      title: 'Dynamic\nProgramming', 
      icon: Grid, 
      status: completedConceptsCount >= 25 ? 'completed' : completedConceptsCount >= 20 ? 'current' : 'locked' 
    },
    { 
      id: 'step8', 
      title: 'Advanced\nAlgorithms', 
      icon: Star, 
      status: completedConceptsCount >= 30 ? 'completed' : completedConceptsCount >= 25 ? 'current' : 'locked' 
    },
  ];

  const RECOMMENDED_ITEMS = [
    {
      id: 'rec1',
      title: 'Dynamic Programming',
      subtitle: 'Master memoization & tabulation',
      color: '#3B82F6',
      iconBg: '#DBEAFE',
      type: 'dp'
    },
    {
      id: 'rec2',
      title: 'Binary Trees',
      subtitle: 'Learn tree traversals',
      color: '#10B981',
      iconBg: '#D1FAE5',
      type: 'tree'
    },
    {
      id: 'rec3',
      title: 'Graph Algorithms',
      subtitle: 'Explore BFS, DFS & shortest path',
      color: '#1E1B4B',
      iconBg: '#E0E7FF',
      type: 'graph'
    }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', paddingBottom: '2.5rem' }}>
      
      {/* ============================================================== */}
      {/* 1. HERO BANNER: Welcome back, Learner! 👋 */}
      {/* ============================================================== */}
      <div style={{
        position: 'relative',
        borderRadius: '20px',
        padding: '2rem 2.25rem',
        background: 'linear-gradient(135deg, #E0E7FF 0%, #DBEAFE 45%, #EFF6FF 100%)',
        border: '1px solid #BFDBFE',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        overflow: 'hidden',
        minHeight: '190px',
        boxShadow: '0 4px 15px rgba(219, 234, 254, 0.4)'
      }}>
        {/* Left Side Content */}
        <div style={{ maxWidth: '520px', zIndex: 2 }}>
          <h1 style={{ 
            fontSize: '1.95rem', 
            fontWeight: 800, 
            color: '#1E1B4B', 
            margin: '0 0 0.5rem 0',
            letterSpacing: '-0.02em'
          }}>
            {s.welcome_message || `Welcome back, ${user?.full_name || user?.username || 'Learner'}! 👋`}
          </h1>
          <p style={{ 
            fontSize: '0.94rem', 
            color: '#475569', 
            margin: '0 0 1.25rem 0',
            lineHeight: 1.5,
            fontWeight: 500
          }}>
            Sharpen your DSA skills with AlgoMentor and become a problem-solving expert!
          </p>

          <button
            onClick={() => onNavigate && onNavigate('concepts')}
            style={{
              padding: '0.65rem 1.4rem',
              borderRadius: '999px',
              border: 'none',
              backgroundColor: '#4F46E5',
              color: '#ffffff',
              fontSize: '0.88rem',
              fontWeight: 700,
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.5rem',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.35)',
              transition: 'transform 0.15s ease, box-shadow 0.15s ease'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-1px)';
              e.currentTarget.style.boxShadow = '0 6px 16px rgba(79, 70, 229, 0.45)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(79, 70, 229, 0.35)';
            }}
          >
            <span>Continue Learning</span>
            <ArrowRight size={15} />
          </button>
        </div>

        {/* Right Side 3D Illustrated Scene */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '1.5rem',
          zIndex: 2,
          position: 'relative'
        }}>
          {/* Floating Badge: Think Code Solve */}
          <div style={{
            padding: '0.65rem 0.95rem',
            borderRadius: '14px',
            backgroundColor: '#FFFFFF',
            boxShadow: '0 8px 20px rgba(0, 0, 0, 0.08)',
            border: '1px solid #E2E8F0',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            gap: '2px',
            transform: 'rotate(-4deg)'
          }}>
            <span style={{ fontSize: '1.3rem', lineHeight: 1 }}>💡</span>
            <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#1E1B4B', lineHeight: 1.2 }}>
              Think<br />Code<br />Solve
            </div>
          </div>

          {/* 3D Girl Developer at Laptop (Vector SVG Art) */}
          <div style={{ position: 'relative', width: '130px', height: '130px', display: 'flex', alignItems: 'flex-end', justifyContent: 'center' }}>
            {/* SVG 3D Developer Girl Avatar */}
            <svg viewBox="0 0 120 120" width="125" height="125" fill="none" xmlns="http://www.w3.org/2000/svg">
              {/* Hair Back */}
              <circle cx="60" cy="50" r="34" fill="#312E81" />
              <path d="M25 55C25 35 40 20 60 20C80 20 95 35 95 55C95 65 92 78 88 85C80 72 40 72 32 85C28 78 25 65 25 55Z" fill="#1E1B4B" />
              {/* Face */}
              <circle cx="60" cy="54" r="22" fill="#FCD34D" />
              {/* Hair Bangs */}
              <path d="M40 44C46 36 65 34 78 40C72 48 50 48 40 44Z" fill="#1E1B4B" />
              {/* Eyes & Smile */}
              <ellipse cx="53" cy="53" rx="2.5" ry="3" fill="#1E1B4B" />
              <ellipse cx="67" cy="53" rx="2.5" ry="3" fill="#1E1B4B" />
              <path d="M56 61C58 63 62 63 64 61" stroke="#B45309" strokeWidth="2" strokeLinecap="round" />
              {/* Purple Hoodie */}
              <path d="M36 84C36 74 46 72 60 72C74 72 84 74 84 84L88 110H32L36 84Z" fill="#6366F1" />
              {/* Laptop */}
              <rect x="36" y="94" width="48" height="24" rx="3" fill="#1E293B" />
              <rect x="39" y="96" width="42" height="18" rx="2" fill="#0F172A" />
              {/* Laptop Screen Code symbol */}
              <text x="60" y="109" textAnchor="middle" fill="#38BDF8" fontSize="10" fontWeight="bold">&lt;/&gt;</text>
              {/* Hands */}
              <circle cx="48" cy="106" r="4" fill="#FCD34D" />
              <circle cx="72" cy="106" r="4" fill="#FCD34D" />
            </svg>
          </div>

          {/* 3D Trending Growth Chart Graphic */}
          <div style={{
            padding: '0.75rem',
            borderRadius: '16px',
            backgroundColor: '#FFFFFF',
            boxShadow: '0 8px 20px rgba(0, 0, 0, 0.08)',
            border: '1px solid #E2E8F0',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <div style={{
              width: '42px',
              height: '36px',
              display: 'flex',
              alignItems: 'flex-end',
              gap: '4px'
            }}>
              <div style={{ width: '8px', height: '14px', borderRadius: '2px', backgroundColor: '#93C5FD' }} />
              <div style={{ width: '8px', height: '22px', borderRadius: '2px', backgroundColor: '#60A5FA' }} />
              <div style={{ width: '8px', height: '30px', borderRadius: '2px', backgroundColor: '#3B82F6' }} />
              <div style={{ width: '8px', height: '36px', borderRadius: '2px', backgroundColor: '#1D4ED8' }} />
            </div>
            <TrendingUp size={14} style={{ color: '#10B981', marginTop: '4px' }} />
          </div>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 2. ROW OF 4 STAT CARDS */}
      {/* ============================================================== */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(230px, 1fr))',
        gap: '1rem'
      }}>
        {/* Card 1: Concepts Completed */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '16px',
          padding: '1.25rem 1.35rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <div style={{
            width: '46px',
            height: '46px',
            borderRadius: '12px',
            backgroundColor: '#EDE9FE',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#7C3AED'
          }}>
            <BookOpen size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#1E1B4B', lineHeight: 1.1 }}>
              {completedConceptsCount}
            </div>
            <div style={{ fontSize: '0.8rem', color: '#64748B', fontWeight: 600, marginTop: '2px' }}>
              Concepts Completed
            </div>
            <div style={{ fontSize: '0.72rem', color: '#10B981', fontWeight: 700, marginTop: '2px' }}>
              {completedConceptsCount > 0 ? `↑ +${completedConceptsCount} completed` : 'Start your first concept'}
            </div>
          </div>
        </div>

        {/* Card 2: Problems Solved */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '16px',
          padding: '1.25rem 1.35rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          alignItems: 'center',
          gap: '1rem'
        }}>
          <div style={{
            width: '46px',
            height: '46px',
            borderRadius: '12px',
            backgroundColor: '#DCFCE7',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#16A34A'
          }}>
            <CheckCircle2 size={24} />
          </div>
          <div>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#1E1B4B', lineHeight: 1.1 }}>
              {problemsSolvedCount}
            </div>
            <div style={{ fontSize: '0.8rem', color: '#64748B', fontWeight: 600, marginTop: '2px' }}>
              Problems Solved
            </div>
            <div style={{ fontSize: '0.72rem', color: '#10B981', fontWeight: 700, marginTop: '2px' }}>
              {problemsSolvedCount > 0 ? `↑ +${problemsSolvedCount} solved` : 'Try your first problem'}
            </div>
          </div>
        </div>

        {/* Card 3: 7 Day Streak */}
        <div 
          onClick={() => {
            const el = document.getElementById('activity-heatmap-section');
            if (el) {
              el.scrollIntoView({ behavior: 'smooth' });
            } else if (onNavigate) {
              onNavigate('streaks');
            }
          }}
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '16px',
            padding: '1.25rem 1.35rem',
            border: '1px solid #E2E8F0',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
            display: 'flex',
            alignItems: 'center',
            gap: '1rem',
            cursor: 'pointer',
            transition: 'transform 0.15s ease, box-shadow 0.15s ease'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'translateY(-2px)';
            e.currentTarget.style.boxShadow = '0 6px 16px rgba(245, 158, 11, 0.15)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.04)';
          }}
          title="Click to view 365-day Learning Heatmap"
        >
          <div style={{
            width: '46px',
            height: '46px',
            borderRadius: '12px',
            backgroundColor: '#FEF3C7',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#D97706'
          }}>
            <Flame size={24} style={{ fill: '#F59E0B' }} />
          </div>
          <div>
            <div style={{ fontSize: '1.3rem', fontWeight: 800, color: '#1E1B4B', lineHeight: 1.1 }}>
              {currentStreakCount} Day Streak
            </div>
            <div style={{ fontSize: '0.78rem', color: '#64748B', fontWeight: 600, marginTop: '2px', display: 'flex', alignItems: 'center', gap: '3px' }}>
              <span>{currentStreakCount > 0 ? 'Keep it up!' : 'Start today!'}</span>
              <span style={{ color: '#D97706', fontWeight: 700 }}>• Heatmap →</span>
            </div>
            {/* 7 Orange streak pills (from Screenshot) */}
            <div style={{ display: 'flex', gap: '3px', marginTop: '6px' }}>
              {[1, 2, 3, 4, 5, 6, 7].map(day => (
                <div key={day} style={{
                  width: '12px',
                  height: '5px',
                  borderRadius: '999px',
                  backgroundColor: day <= currentStreakCount ? '#F59E0B' : '#CBD5E1'
                }} />
              ))}
            </div>
          </div>
        </div>

        {/* Card 4: Overall Progress (with Circular Progress Ring) */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '16px',
          padding: '1.15rem 1.35rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          alignItems: 'center',
          gap: '1.15rem'
        }}>
          {/* Circular Progress Ring */}
          <div style={{ position: 'relative', width: '56px', height: '56px', flexShrink: 0 }}>
            <svg viewBox="0 0 36 36" style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="#E2E8F0"
                strokeWidth="3.2"
              />
              <path
                d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="#0EA5E9"
                strokeWidth="3.2"
                strokeDasharray={`${Math.round(masteryPct)}, 100`}
                strokeLinecap="round"
              />
            </svg>
            <div style={{
              position: 'absolute',
              inset: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 800,
              fontSize: '0.85rem',
              color: '#1E1B4B'
            }}>
              {Math.round(masteryPct)}%
            </div>
          </div>

          <div>
            <div style={{ fontSize: '0.94rem', fontWeight: 800, color: '#1E1B4B' }}>
              Overall Progress
            </div>
            <button
              onClick={() => onNavigate && onNavigate('progress')}
              style={{
                marginTop: '4px',
                background: 'none',
                border: 'none',
                padding: 0,
                color: '#4F46E5',
                fontSize: '0.78rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '2px',
                cursor: 'pointer'
              }}
            >
              <span>View Details</span>
              <ArrowRight size={12} />
            </button>
          </div>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 3. MIDDLE ROW 1: LEARNING ROADMAP & AI MENTOR */}
      {/* ============================================================== */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 340px',
        gap: '1.25rem'
      }}>
        {/* Left Card: Learning Roadmap (Connected Journey) */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '18px',
          padding: '1.35rem 1.5rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          {/* Header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{
                width: '28px',
                height: '28px',
                borderRadius: '50%',
                backgroundColor: '#EDE9FE',
                color: '#4F46E5',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '0.95rem'
              }}>
                📍
              </div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#1E1B4B', margin: 0 }}>
                Learning Roadmap
              </h3>
            </div>

            <button
              onClick={() => onNavigate && onNavigate('roadmaps')}
              style={{
                background: 'none',
                border: 'none',
                color: '#4F46E5',
                fontSize: '0.8rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                cursor: 'pointer'
              }}
            >
              <span>View Full Roadmap</span>
              <ArrowRight size={13} />
            </button>
          </div>

          {/* Horizontal Stepper Timeline Track */}
          <div style={{
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            gap: '8px',
            overflowX: 'auto',
            paddingBottom: '0.5rem',
            position: 'relative'
          }}>
            {/* Connecting Horizontal Line Behind Icons */}
            <div style={{
              position: 'absolute',
              top: '16px',
              left: '20px',
              right: '20px',
              height: '2px',
              backgroundColor: '#E2E8F0',
              zIndex: 1
            }} />

            {ROADMAP_STEPS.map((step, idx) => {
              const Icon = step.icon;
              const isDone = step.status === 'completed';
              const isCurrent = step.status === 'current';
              const isLocked = step.status === 'locked';

              return (
                <div 
                  key={step.id} 
                  onClick={() => onNavigate && onNavigate('concepts')}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    flex: '1 1 80px',
                    minWidth: '78px',
                    zIndex: 2,
                    cursor: 'pointer'
                  }}
                >
                  {/* Status Indicator Icon (Checkmark / Target Bullseye / Lock) */}
                  <div style={{
                    width: '18px',
                    height: '18px',
                    borderRadius: '50%',
                    backgroundColor: isDone ? '#10B981' : isCurrent ? '#FFFFFF' : '#CBD5E1',
                    border: isCurrent ? '2px solid #4F46E5' : 'none',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    marginBottom: '0.65rem',
                    boxShadow: isCurrent ? '0 0 0 3px rgba(79, 70, 229, 0.2)' : 'none'
                  }}>
                    {isDone && <Check size={11} color="#ffffff" strokeWidth={3} />}
                    {isCurrent && <div style={{ width: '6px', height: '6px', borderRadius: '50%', backgroundColor: '#4F46E5' }} />}
                    {isLocked && <Lock size={9} color="#64748B" />}
                  </div>

                  {/* Step Card Box */}
                  <div style={{
                    width: '100%',
                    padding: '0.65rem 0.4rem',
                    borderRadius: '12px',
                    backgroundColor: isDone ? '#F0FDF4' : isCurrent ? '#FFFFFF' : '#F8FAFC',
                    border: isDone ? '1px solid #BBF7D0' : isCurrent ? '1.5px solid #4F46E5' : '1px solid #E2E8F0',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    textAlign: 'center',
                    gap: '6px',
                    boxShadow: isCurrent ? '0 4px 12px rgba(79, 70, 229, 0.12)' : 'none',
                    transition: 'transform 0.15s ease'
                  }}>
                    <div style={{
                      color: isDone ? '#16A34A' : isCurrent ? '#4F46E5' : '#94A3B8'
                    }}>
                      <Icon size={18} />
                    </div>
                    <div style={{
                      fontSize: '0.68rem',
                      fontWeight: 700,
                      color: isDone ? '#166534' : isCurrent ? '#1E1B4B' : '#64748B',
                      lineHeight: 1.25,
                      whiteSpace: 'pre-line'
                    }}>
                      {step.title}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Card: AI Mentor Card (from Screenshot) */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '18px',
          padding: '1.35rem 1.4rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          position: 'relative',
          overflow: 'hidden'
        }}>
          {/* Header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <Sparkles size={18} style={{ color: '#4F46E5' }} />
              <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#1E1B4B', margin: 0 }}>
                AI Mentor
              </h3>
            </div>
            <button
              onClick={onTriggerAI}
              style={{
                background: 'none',
                border: 'none',
                color: '#4F46E5',
                fontSize: '0.8rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '2px',
                cursor: 'pointer'
              }}
            >
              <span>Try Now</span>
              <ArrowRight size={13} />
            </button>
          </div>

          <p style={{ fontSize: '0.8rem', color: '#64748B', margin: '0 0 0.85rem 0', lineHeight: 1.45 }}>
            Get hints, analyze your code, and learn smarter!
          </p>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
            {/* 3 Bullets with Checkmarks */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.74rem', color: '#334155', fontWeight: 600 }}>
                <div style={{ width: '14px', height: '14px', borderRadius: '50%', backgroundColor: '#DCFCE7', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={9} color="#16A34A" strokeWidth={3} />
                </div>
                <span>Step-by-Step Hints</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.74rem', color: '#334155', fontWeight: 600 }}>
                <div style={{ width: '14px', height: '14px', borderRadius: '50%', backgroundColor: '#DCFCE7', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={9} color="#16A34A" strokeWidth={3} />
                </div>
                <span>Code Analysis</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.74rem', color: '#334155', fontWeight: 600 }}>
                <div style={{ width: '14px', height: '14px', borderRadius: '50%', backgroundColor: '#DCFCE7', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Check size={9} color="#16A34A" strokeWidth={3} />
                </div>
                <span>Concept Explanation</span>
              </div>
            </div>

            {/* 3D Cute AI Robot at Laptop Illustration */}
            <div style={{ width: '90px', height: '80px', position: 'relative' }}>
              <svg viewBox="0 0 100 90" width="90" height="80" fill="none" xmlns="http://www.w3.org/2000/svg">
                {/* Robot Head */}
                <rect x="25" y="10" width="50" height="38" rx="12" fill="#E0E7FF" stroke="#4F46E5" strokeWidth="2.5" />
                {/* Antenna */}
                <line x1="50" y1="10" x2="50" y2="3" stroke="#4F46E5" strokeWidth="2.5" strokeLinecap="round" />
                <circle cx="50" cy="3" r="3.5" fill="#6366F1" />
                {/* Eyes Screen */}
                <rect x="33" y="20" width="34" height="18" rx="6" fill="#1E1B4B" />
                <ellipse cx="43" cy="29" rx="3.5" ry="4" fill="#38BDF8" />
                <ellipse cx="57" cy="29" rx="3.5" ry="4" fill="#38BDF8" />
                {/* Robot Body */}
                <rect x="30" y="52" width="40" height="28" rx="8" fill="#EEF2FF" stroke="#6366F1" strokeWidth="2" />
                {/* Laptop */}
                <rect x="22" y="66" width="38" height="18" rx="2" fill="#1E293B" />
                <rect x="25" y="68" width="32" height="12" rx="1.5" fill="#38BDF8" />
                {/* Hands */}
                <circle cx="32" cy="74" r="3.5" fill="#818CF8" />
                <circle cx="50" cy="74" r="3.5" fill="#818CF8" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 3.5. GITHUB / LEETCODE STYLE LEARNING ACTIVITY HEATMAP (365 DAYS) */}
      {/* ============================================================== */}
      <div id="activity-heatmap-section">
        <ActivityHeatmap isLight={true} onNavigate={onNavigate} />
      </div>

      {/* ============================================================== */}
      {/* 4. MIDDLE ROW 2: YOUR PERFORMANCE, PROBLEM STATS & RECOMMENDED */}
      {/* ============================================================== */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1.15fr 1fr 1.15fr',
        gap: '1.25rem'
      }}>
        {/* Column 1: Your Performance (Curved Line Chart) */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '18px',
          padding: '1.35rem 1.4rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          {/* Header with 1W, 1M, 3M filter pills */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '1.1rem' }}>📊</span>
              <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#1E1B4B', margin: 0 }}>
                Your Performance
              </h3>
            </div>

            <div style={{
              display: 'flex',
              padding: '2px',
              borderRadius: '999px',
              backgroundColor: '#F1F5F9'
            }}>
              {['1W', '1M', '3M'].map(tf => (
                <button
                  key={tf}
                  onClick={() => setPerfTimeframe(tf)}
                  style={{
                    padding: '0.25rem 0.65rem',
                    borderRadius: '999px',
                    border: 'none',
                    backgroundColor: perfTimeframe === tf ? '#4F46E5' : 'transparent',
                    color: perfTimeframe === tf ? '#FFFFFF' : '#64748B',
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  {tf}
                </button>
              ))}
            </div>
          </div>

          {/* SVG Performance Line Graph */}
          <div style={{ position: 'relative', width: '100%', height: '140px' }}>
            <svg viewBox="0 0 300 130" style={{ width: '100%', height: '100%' }}>
              <defs>
                <linearGradient id="perfGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#6366F1" stopOpacity="0.25" />
                  <stop offset="100%" stopColor="#6366F1" stopOpacity="0.0" />
                </linearGradient>
              </defs>

              {/* Grid Horizontal Lines */}
              <line x1="40" y1="15" x2="290" y2="15" stroke="#F1F5F9" strokeWidth="1" />
              <line x1="40" y1="45" x2="290" y2="45" stroke="#F1F5F9" strokeWidth="1" />
              <line x1="40" y1="75" x2="290" y2="75" stroke="#F1F5F9" strokeWidth="1" />
              <line x1="40" y1="105" x2="290" y2="105" stroke="#F1F5F9" strokeWidth="1" />

              {/* Y Axis Labels */}
              <text x="32" y="18" textAnchor="end" fill="#94A3B8" fontSize="9" fontWeight="600">100%</text>
              <text x="32" y="48" textAnchor="end" fill="#94A3B8" fontSize="9" fontWeight="600">75%</text>
              <text x="32" y="78" textAnchor="end" fill="#94A3B8" fontSize="9" fontWeight="600">50%</text>
              <text x="32" y="108" textAnchor="end" fill="#94A3B8" fontSize="9" fontWeight="600">0%</text>

              {/* Gradient Area under curve */}
              <path
                d="M50 78 Q105 60 160 72 T270 54 L270 115 L50 115 Z"
                fill="url(#perfGrad)"
              />

              {/* Curved Line */}
              <path
                d="M50 78 Q105 60 160 72 T270 54"
                fill="none"
                stroke="#6366F1"
                strokeWidth="2.8"
                strokeLinecap="round"
              />

              {/* Data Points */}
              <circle cx="50" cy="78" r="4" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="2" />
              <circle cx="105" cy="65" r="4" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="2" />
              <circle cx="160" cy="72" r="4" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="2" />
              <circle cx="215" cy="80" r="4" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="2" />
              <circle cx="270" cy="54" r="5" fill="#4F46E5" stroke="#FFFFFF" strokeWidth="2.5" />

              {/* X Axis Labels */}
              <text x="50" y="125" textAnchor="middle" fill="#94A3B8" fontSize="9" fontWeight="600">Week 1</text>
              <text x="120" y="125" textAnchor="middle" fill="#94A3B8" fontSize="9" fontWeight="600">Week 2</text>
              <text x="195" y="125" textAnchor="middle" fill="#94A3B8" fontSize="9" fontWeight="600">Week 3</text>
              <text x="270" y="125" textAnchor="middle" fill="#94A3B8" fontSize="9" fontWeight="600">Week 4</text>
            </svg>

            {/* 68% Tooltip Badge on Week 4 (from Screenshot) */}
            <div style={{
              position: 'absolute',
              top: '14px',
              right: '8px',
              padding: '2px 8px',
              borderRadius: '999px',
              backgroundColor: '#4F46E5',
              color: '#FFFFFF',
              fontSize: '0.72rem',
              fontWeight: 800,
              boxShadow: '0 2px 6px rgba(79, 70, 229, 0.4)'
            }}>
              68%
            </div>
          </div>
        </div>

        {/* Column 2: Problem Statistics (Donut Chart) */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '18px',
          padding: '1.35rem 1.4rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          {/* Header */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '0.85rem' }}>
            <span style={{ fontSize: '1.1rem' }}>💼</span>
            <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#1E1B4B', margin: 0 }}>
              Problem Statistics
            </h3>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: '1rem' }}>
            {/* Donut Chart with 120 Total Center */}
            <div style={{ position: 'relative', width: '105px', height: '105px', flexShrink: 0 }}>
              <svg viewBox="0 0 36 36" style={{ width: '100%', height: '100%', transform: 'rotate(-90deg)' }}>
                {/* Background Ring */}
                <circle cx="18" cy="18" r="14" fill="none" stroke="#F1F5F9" strokeWidth="5.5" />
                {/* Green Easy: 42% (strokeDasharray: 36.9 88) */}
                <circle
                  cx="18"
                  cy="18"
                  r="14"
                  fill="none"
                  stroke="#10B981"
                  strokeWidth="5.5"
                  strokeDasharray="37 51"
                  strokeDashoffset="0"
                />
                {/* Orange Medium: 38% (strokeDasharray: 33.4 88) */}
                <circle
                  cx="18"
                  cy="18"
                  r="14"
                  fill="none"
                  stroke="#F59E0B"
                  strokeWidth="5.5"
                  strokeDasharray="33 55"
                  strokeDashoffset="-37"
                />
                {/* Coral Hard: 20% (strokeDasharray: 17.6 88) */}
                <circle
                  cx="18"
                  cy="18"
                  r="14"
                  fill="none"
                  stroke="#EF4444"
                  strokeWidth="5.5"
                  strokeDasharray="18 70"
                  strokeDashoffset="-70"
                />
              </svg>
              {/* Center 120 Total */}
              <div style={{
                position: 'absolute',
                inset: 0,
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                lineHeight: 1
              }}>
                <div style={{ fontSize: '1.15rem', fontWeight: 800, color: '#1E1B4B' }}>120</div>
                <div style={{ fontSize: '0.62rem', color: '#64748B', fontWeight: 600, marginTop: '2px' }}>Total</div>
              </div>
            </div>

            {/* Legend Breakdown */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.78rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#10B981' }} />
                  <span style={{ color: '#475569', fontWeight: 600 }}>Easy</span>
                </div>
                <span style={{ fontWeight: 700, color: '#1E1B4B' }}>50 (42%)</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.78rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#F59E0B' }} />
                  <span style={{ color: '#475569', fontWeight: 600 }}>Medium</span>
                </div>
                <span style={{ fontWeight: 700, color: '#1E1B4B' }}>45 (38%)</span>
              </div>

              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', fontSize: '0.78rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <div style={{ width: '8px', height: '8px', borderRadius: '50%', backgroundColor: '#EF4444' }} />
                  <span style={{ color: '#475569', fontWeight: 600 }}>Hard</span>
                </div>
                <span style={{ fontWeight: 700, color: '#1E1B4B' }}>25 (20%)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Column 3: Recommended for You */}
        <div style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '18px',
          padding: '1.35rem 1.4rem',
          border: '1px solid #E2E8F0',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between'
        }}>
          {/* Header */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '1.1rem' }}>💡</span>
              <h3 style={{ fontSize: '1rem', fontWeight: 800, color: '#1E1B4B', margin: 0 }}>
                Recommended for You
              </h3>
            </div>
            <button
              onClick={() => onNavigate && onNavigate('concepts')}
              style={{
                background: 'none',
                border: 'none',
                color: '#4F46E5',
                fontSize: '0.78rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '2px',
                cursor: 'pointer'
              }}
            >
              <span>View All</span>
              <ArrowRight size={12} />
            </button>
          </div>

          {/* Recommended List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {RECOMMENDED_ITEMS.map((item) => (
              <div 
                key={item.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  padding: '0.55rem 0.65rem',
                  borderRadius: '12px',
                  backgroundColor: '#F8FAFC',
                  border: '1px solid #E2E8F0',
                  gap: '8px'
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', minWidth: 0 }}>
                  <div style={{
                    width: '36px',
                    height: '36px',
                    borderRadius: '8px',
                    backgroundColor: item.iconBg,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: item.color,
                    flexShrink: 0
                  }}>
                    {item.type === 'dp' && <Grid size={18} />}
                    {item.type === 'tree' && <Network size={18} />}
                    {item.type === 'graph' && <Network size={18} />}
                  </div>
                  <div style={{ minWidth: 0 }}>
                    <div style={{
                      fontWeight: 700,
                      fontSize: '0.82rem',
                      color: '#1E1B4B',
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis'
                    }}>
                      {item.title}
                    </div>
                    <div style={{
                      fontSize: '0.7rem',
                      color: '#64748B',
                      whiteSpace: 'nowrap',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis'
                    }}>
                      {item.subtitle}
                    </div>
                  </div>
                </div>

                <button
                  onClick={() => onNavigate && onNavigate('concepts')}
                  style={{
                    padding: '0.35rem 0.75rem',
                    borderRadius: '8px',
                    border: 'none',
                    backgroundColor: '#4F46E5',
                    color: '#FFFFFF',
                    fontSize: '0.74rem',
                    fontWeight: 700,
                    display: 'flex',
                    alignItems: 'center',
                    gap: '2px',
                    cursor: 'pointer',
                    flexShrink: 0,
                    boxShadow: '0 2px 6px rgba(79, 70, 229, 0.25)'
                  }}
                >
                  <span>Start</span>
                  <ArrowRight size={11} />
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 5. BOTTOM BANNER: READY FOR A CHALLENGE? */}
      {/* ============================================================== */}
      <div style={{
        borderRadius: '18px',
        padding: '1.25rem 2rem',
        background: 'linear-gradient(135deg, #EEF2FF 0%, #EDE9FE 50%, #F5F3FF 100%)',
        border: '1px solid #DDD6FE',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        position: 'relative',
        overflow: 'hidden',
        boxShadow: '0 2px 10px rgba(237, 233, 254, 0.5)'
      }}>
        {/* Left Side: Rocket & Text */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', zIndex: 2 }}>
          <div style={{
            width: '46px',
            height: '46px',
            borderRadius: '14px',
            backgroundColor: '#FFFFFF',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.5rem',
            boxShadow: '0 4px 10px rgba(79, 70, 229, 0.15)'
          }}>
            🚀
          </div>

          <div>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 800, color: '#1E1B4B', margin: '0 0 2px 0' }}>
              Ready for a Challenge?
            </h3>
            <p style={{ fontSize: '0.84rem', color: '#64748B', margin: 0, fontWeight: 500 }}>
              Try today's curated problem set and boost your skills!
            </p>
          </div>
        </div>

        {/* Right Side: Start Practice Button & Mountain Graphic */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '2rem', zIndex: 2 }}>
          <button
            onClick={() => onNavigate && onNavigate('practice', { language: 'java' })}
            style={{
              padding: '0.65rem 1.4rem',
              borderRadius: '999px',
              border: 'none',
              backgroundColor: '#4F46E5',
              color: '#ffffff',
              fontSize: '0.85rem',
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              cursor: 'pointer',
              boxShadow: '0 4px 12px rgba(79, 70, 229, 0.35)',
              transition: 'transform 0.15s ease'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-1px)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}
          >
            <span>Start Practice</span>
            <ArrowRight size={14} />
          </button>

          {/* Illustrated Mountain with Summit Flag (from Screenshot) */}
          <div style={{ width: '85px', height: '55px', position: 'relative' }}>
            <svg viewBox="0 0 85 55" width="85" height="55" fill="none" xmlns="http://www.w3.org/2000/svg">
              {/* Back Mountain */}
              <polygon points="15,55 45,15 75,55" fill="#C7D2FE" />
              {/* Fore Mountain */}
              <polygon points="35,55 60,8 85,55" fill="#818CF8" />
              {/* Snow Peak */}
              <polygon points="53,20 60,8 67,20 60,17" fill="#FFFFFF" />
              {/* Red Summit Flag */}
              <line x1="60" y1="8" x2="60" y2="1" stroke="#EF4444" strokeWidth="1.5" />
              <polygon points="60,1 68,4 60,7" fill="#EF4444" />
            </svg>
          </div>
        </div>
      </div>

    </div>
  );
}
