import React from 'react';
import { 
  Home, 
  BookOpen, 
  Network, 
  Box, 
  Code2, 
  Sparkles, 
  BarChart2, 
  Settings, 
  ChevronRight,
  Sun,
  Moon,
  Trophy,
  ArrowRight,
  Flame
} from 'lucide-react';

const NAV_ITEMS = [
  { id: 'dashboard', label: 'Dashboard', icon: Home },
  { id: 'concepts', label: 'Learn Concepts', icon: BookOpen },
  { id: 'roadmaps', label: 'Algorithms', icon: Network, hasChevron: true },
  { id: 'visualizations', label: 'Visualizer', icon: Box },
  { id: 'practice', label: 'Practice', icon: Code2 },
  { id: 'ai-tutor', label: 'AI Mentor', icon: Sparkles },
  { id: 'streaks', label: 'Activity Heatmap', icon: Flame, isHighlight: true },
  { id: 'progress', label: 'Progress', icon: BarChart2 },
  { id: 'profile', label: 'Profile', icon: Settings },
];

export default function Sidebar({ 
  currentPage, 
  setCurrentPage, 
  theme, 
  setTheme, 
  user, 
  onOpenAuth, 
  onLogout,
  mobileOpen,
  setMobileOpen
}) {
  const isLight = theme === 'light';

  return (
    <>
      {/* Mobile backdrop */}
      {mobileOpen && (
        <div 
          onClick={() => setMobileOpen(false)}
          style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(0,0,0,0.5)',
            zIndex: 40,
            backdropFilter: 'blur(4px)'
          }}
        />
      )}

      <aside style={{
        position: 'fixed',
        top: 0,
        bottom: 0,
        left: 0,
        width: '260px',
        backgroundColor: isLight ? '#FFFFFF' : '#0B1120',
        borderRight: isLight ? '1px solid #E2E8F0' : '1px solid #1E293B',
        display: 'flex',
        flexDirection: 'column',
        zIndex: 50,
        transition: 'transform 0.3s ease, background-color 0.25s ease',
        transform: mobileOpen ? 'translateX(0)' : undefined,
        boxShadow: isLight ? '4px 0 20px rgba(0, 0, 0, 0.02)' : 'none'
      }}>
        {/* Brand Header */}
        <div style={{
          padding: '1.5rem 1.4rem 1.25rem 1.4rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.2rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '10px',
              background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: '#ffffff',
              fontWeight: 800,
              fontSize: '1rem',
              letterSpacing: '-0.05em',
              boxShadow: '0 4px 10px rgba(79, 70, 229, 0.35)'
            }}>
              &lt;/&gt;
            </div>
            <div>
              <div style={{ 
                fontWeight: 800, 
                fontSize: '1.25rem', 
                letterSpacing: '-0.03em', 
                color: isLight ? '#1E1B4B' : '#F8FAFC' 
              }}>
                Algo<span style={{ color: '#4F46E5' }}>Mentor</span>
              </div>
              <div style={{ 
                fontSize: '0.68rem', 
                color: isLight ? '#64748B' : '#94A3B8', 
                fontWeight: 600,
                letterSpacing: '0.04em'
              }}>
                Learn • Practice • Excel
              </div>
            </div>
          </div>
        </div>

        {/* Navigation Items */}
        <div style={{
          flex: 1,
          overflowY: 'auto',
          padding: '0.5rem 0.85rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.35rem'
        }}>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = currentPage === item.id;

            return (
              <button
                key={item.id}
                onClick={() => {
                  setCurrentPage(item.id);
                  if (setMobileOpen) setMobileOpen(false);
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.85rem',
                  padding: '0.7rem 0.95rem',
                  borderRadius: '12px',
                  border: 'none',
                  backgroundColor: isActive 
                    ? (isLight ? '#EDE9FE' : 'rgba(79, 70, 229, 0.2)') 
                    : 'transparent',
                  color: isActive 
                    ? '#4F46E5' 
                    : (isLight ? '#475569' : '#94A3B8'),
                  fontWeight: isActive ? 700 : 500,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  textAlign: 'left',
                  transition: 'all 0.15s ease',
                  position: 'relative'
                }}
                onMouseEnter={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.backgroundColor = isLight ? '#F1F5F9' : 'rgba(255, 255, 255, 0.05)';
                  }
                }}
                onMouseLeave={(e) => {
                  if (!isActive) {
                    e.currentTarget.style.backgroundColor = 'transparent';
                  }
                }}
              >
                {/* Active Left Indicator Bar */}
                {isActive && (
                  <div style={{
                    position: 'absolute',
                    left: 0,
                    top: '20%',
                    bottom: '20%',
                    width: '3.5px',
                    borderRadius: '0 4px 4px 0',
                    backgroundColor: '#4F46E5'
                  }} />
                )}

                <Icon 
                  size={19} 
                  style={{ 
                    color: isActive ? '#4F46E5' : (isLight ? '#64748B' : '#94A3B8'),
                    strokeWidth: isActive ? 2.2 : 1.8 
                  }} 
                />
                
                <span style={{ flex: 1 }}>{item.label}</span>

                {item.isHighlight && (
                  <span style={{
                    fontSize: '0.65rem',
                    fontWeight: 800,
                    padding: '2px 7px',
                    borderRadius: '999px',
                    backgroundColor: '#10B981',
                    color: '#FFFFFF',
                    boxShadow: '0 2px 6px rgba(16, 185, 129, 0.4)'
                  }}>
                    365d
                  </span>
                )}

                {item.hasChevron && (
                  <ChevronRight size={15} style={{ opacity: 0.5, color: isLight ? '#64748B' : '#94A3B8' }} />
                )}
              </button>
            );
          })}
        </div>

        {/* Sidebar Footer Cards */}
        <div style={{
          padding: '0.85rem 0.85rem 1.25rem 0.85rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.85rem'
        }}>
          {/* Keep Learning Streak Box (from Screenshot) */}
          <div style={{
            padding: '1.15rem 1rem',
            borderRadius: '16px',
            background: isLight 
              ? 'linear-gradient(180deg, #FEF3C7 0%, #FFFBEB 100%)' 
              : 'linear-gradient(180deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%)',
            border: isLight ? '1px solid #FDE68A' : '1px solid rgba(245, 158, 11, 0.3)',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            textAlign: 'center',
            boxShadow: '0 4px 12px rgba(245, 158, 11, 0.08)'
          }}>
            <div style={{
              fontSize: '1.8rem',
              marginBottom: '0.35rem',
              lineHeight: 1
            }}>
              🏆
            </div>
            
            <div style={{
              fontWeight: 800,
              fontSize: '0.95rem',
              color: isLight ? '#92400E' : '#FCD34D',
              marginBottom: '0.2rem'
            }}>
              Keep Learning!
            </div>
            
            <div style={{
              fontSize: '0.74rem',
              color: isLight ? '#B45309' : '#FDE68A',
              marginBottom: '0.75rem',
              fontWeight: 500
            }}>
              You're on a 7 day streak!
            </div>

            <button
              onClick={() => setCurrentPage('streaks')}
              style={{
                width: '100%',
                padding: '0.5rem 0.8rem',
                borderRadius: '999px',
                border: 'none',
                backgroundColor: '#4F46E5',
                color: '#ffffff',
                fontSize: '0.78rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.4rem',
                cursor: 'pointer',
                boxShadow: '0 3px 8px rgba(79, 70, 229, 0.3)',
                transition: 'transform 0.15s ease'
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.02)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
            >
              <span>View Heatmap</span>
              <ArrowRight size={13} />
            </button>
          </div>

          {/* Light / Dark Segmented Theme Switch (from Screenshot) */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            padding: '3px',
            borderRadius: '999px',
            backgroundColor: isLight ? '#F1F5F9' : '#0F172A',
            border: isLight ? '1px solid #E2E8F0' : '1px solid #1E293B'
          }}>
            <button
              onClick={() => setTheme('light')}
              style={{
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.35rem',
                padding: '0.42rem 0.6rem',
                borderRadius: '999px',
                border: 'none',
                backgroundColor: isLight ? '#FFFFFF' : 'transparent',
                color: isLight ? '#1E1B4B' : '#94A3B8',
                fontSize: '0.76rem',
                fontWeight: isLight ? 700 : 500,
                cursor: 'pointer',
                boxShadow: isLight ? '0 2px 6px rgba(0, 0, 0, 0.08)' : 'none',
                transition: 'all 0.2s ease'
              }}
            >
              <Sun size={13} style={{ color: isLight ? '#F59E0B' : '#94A3B8' }} />
              <span>Light</span>
            </button>

            <button
              onClick={() => setTheme('dark')}
              style={{
                flex: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.35rem',
                padding: '0.42rem 0.6rem',
                borderRadius: '999px',
                border: 'none',
                backgroundColor: !isLight ? '#1E293B' : 'transparent',
                color: !isLight ? '#F8FAFC' : '#64748B',
                fontSize: '0.76rem',
                fontWeight: !isLight ? 700 : 500,
                cursor: 'pointer',
                boxShadow: !isLight ? '0 2px 6px rgba(0, 0, 0, 0.3)' : 'none',
                transition: 'all 0.2s ease'
              }}
            >
              <Moon size={13} style={{ color: !isLight ? '#818CF8' : '#94A3B8' }} />
              <span>Dark</span>
            </button>
          </div>
        </div>
      </aside>
    </>
  );
}
