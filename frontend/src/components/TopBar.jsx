import React from 'react';
import { Search, Bell, Menu, Flame } from 'lucide-react';

export default function TopBar({ 
  user, 
  onTriggerAI, 
  onOpenMobileSidebar,
  searchQuery,
  setSearchQuery,
  onNavigate
}) {
  const userInitial = user?.full_name ? user.full_name[0].toUpperCase() : (user?.username ? user.username[0].toUpperCase() : 'B');

  return (
    <header style={{
      height: '66px',
      position: 'sticky',
      top: 0,
      backgroundColor: 'var(--bg-secondary)',
      borderBottom: '1px solid var(--border-subtle)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '0 1.75rem',
      zIndex: 30,
      transition: 'background-color 0.25s ease'
    }}>
      {/* Mobile hamburger + Wide Search Input */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flex: 1, maxWidth: '580px' }}>
        <button
          onClick={onOpenMobileSidebar}
          style={{
            display: 'none',
            background: 'none',
            border: 'none',
            color: 'var(--text-primary)',
            cursor: 'pointer',
            padding: '4px'
          }}
          className="mobile-hamburger"
        >
          <Menu size={22} />
        </button>

        <div style={{
          position: 'relative',
          width: '100%',
          display: 'flex',
          alignItems: 'center'
        }}>
          <Search 
            size={16} 
            style={{ 
              position: 'absolute', 
              left: '14px', 
              color: '#94A3B8',
              pointerEvents: 'none'
            }} 
          />
          <input
            type="text"
            placeholder="Search concepts, algorithms or problems..."
            value={searchQuery || ''}
            onChange={(e) => setSearchQuery && setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '0.6rem 1rem 0.6rem 2.5rem',
              borderRadius: '999px',
              border: '1px solid var(--border-subtle)',
              backgroundColor: 'var(--bg-primary)',
              color: 'var(--text-primary)',
              fontSize: '0.84rem',
              outline: 'none',
              transition: 'border-color 0.2s ease, box-shadow 0.2s ease'
            }}
            onFocus={(e) => {
              e.target.style.borderColor = '#4F46E5';
              e.target.style.boxShadow = '0 0 0 3px rgba(79, 70, 229, 0.12)';
            }}
            onBlur={(e) => {
              e.target.style.borderColor = 'var(--border-subtle)';
              e.target.style.boxShadow = 'none';
            }}
          />
        </div>
      </div>

      {/* Right side: Streak Pill + Notification Bell with Badge & User Initial Avatar */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
        {/* Streak Pill Badge */}
        <button
          onClick={() => onNavigate && onNavigate('streaks')}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '0.4rem 0.85rem',
            borderRadius: '999px',
            backgroundColor: '#FEF3C7',
            border: '1px solid #FDE68A',
            color: '#B45309',
            fontSize: '0.78rem',
            fontWeight: 800,
            cursor: 'pointer',
            transition: 'transform 0.15s ease'
          }}
          onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.04)'}
          onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
          title="Open Activity Heatmap & Streaks"
        >
          <Flame size={15} style={{ fill: '#F59E0B', color: '#D97706' }} />
          <span>7 Day Streak</span>
        </button>

        {/* Notification Bell with Red Badge '3' (from Screenshot) */}
        <div style={{ position: 'relative', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--text-secondary)',
            transition: 'background-color 0.15s ease'
          }}>
            <Bell size={19} style={{ color: '#475569' }} />
          </div>
          
          <span style={{
            position: 'absolute',
            top: '4px',
            right: '4px',
            width: '16px',
            height: '16px',
            borderRadius: '50%',
            backgroundColor: '#EF4444',
            color: '#FFFFFF',
            fontSize: '0.62rem',
            fontWeight: 800,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '2px solid var(--bg-secondary)'
          }}>
            3
          </span>
        </div>

        {/* User Avatar Circle with letter 'B' (from Screenshot) */}
        <div 
          onClick={() => onNavigate && onNavigate('profile')}
          style={{
            width: '38px',
            height: '38px',
            borderRadius: '50%',
            backgroundColor: '#1E1B4B',
            color: '#FFFFFF',
            fontWeight: 700,
            fontSize: '0.92rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            boxShadow: '0 2px 8px rgba(30, 27, 75, 0.25)',
            border: '2px solid #FFFFFF'
          }}
          title={user?.full_name || 'Learner Profile'}
        >
          {userInitial}
        </div>
      </div>
    </header>
  );
}
