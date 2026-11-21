import React, { useState, useEffect, useMemo } from 'react';
import { 
  Flame, 
  Award, 
  Calendar, 
  CheckCircle2, 
  TrendingUp, 
  Code2, 
  BookOpen, 
  HelpCircle, 
  Sparkles,
  Info
} from 'lucide-react';
import { api } from '../services/api';

export default function ActivityHeatmap({ isLight = true, compact = false, onNavigate }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [hoveredDay, setHoveredDay] = useState(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    loadStreakCalendar();
  }, []);

  async function loadStreakCalendar() {
    try {
      const res = await api.getStreakCalendar();
      setData(res);
    } catch (err) {
      console.error('Failed to load activity heatmap calendar:', err);
    } finally {
      setLoading(false);
    }
  }

  // Color mapper for GitHub / LeetCode Green Contribution Levels (0 to 4)
  function getSquareColor(level) {
    if (isLight) {
      switch (level) {
        case 1: return '#9BE9A8'; // Light Green
        case 2: return '#40C463'; // Medium Green
        case 3: return '#30A14E'; // Green
        case 4: return '#216E39'; // Dark Forest Green
        default: return '#EBEDF0'; // Empty Grey
      }
    } else {
      switch (level) {
        case 1: return '#0E4429'; // Deep Green
        case 2: return '#006D32'; // Medium Emerald
        case 3: return '#26A641'; // Vibrant Green
        case 4: return '#39D353'; // Neon / Bright Green
        default: return '#1E293B'; // Dark Slate Grey
      }
    }
  }

  // Organize the 365 calendar days into 53 weekly columns (Sun - Sat)
  const { weeks, monthLabels } = useMemo(() => {
    if (!data?.calendar_days || data.calendar_days.length === 0) {
      return { weeks: [], monthLabels: [] };
    }

    const days = data.calendar_days;
    const weeklyColumns = [];
    const months = [];
    let currentWeek = [];
    let lastMonth = '';

    // Pad first week with empty cells if it doesn't start on Sunday
    const firstDate = new Date(days[0].date);
    const firstDayOfWeek = firstDate.getDay(); // 0 = Sun, 1 = Mon ...
    for (let p = 0; p < firstDayOfWeek; p++) {
      currentWeek.push(null);
    }

    days.forEach((day, index) => {
      const d = new Date(day.date);
      const monthName = d.toLocaleString('default', { month: 'short' });

      // Check if this week starts a new month
      if (monthName !== lastMonth) {
        months.push({
          name: monthName,
          weekIndex: weeklyColumns.length
        });
        lastMonth = monthName;
      }

      currentWeek.push(day);

      if (currentWeek.length === 7) {
        weeklyColumns.push(currentWeek);
        currentWeek = [];
      }
    });

    if (currentWeek.length > 0) {
      while (currentWeek.length < 7) {
        currentWeek.push(null);
      }
      weeklyColumns.push(currentWeek);
    }

    return { weeks: weeklyColumns, monthLabels: months };
  }, [data]);

  if (loading) {
    return (
      <div style={{
        padding: '2rem',
        borderRadius: '16px',
        backgroundColor: isLight ? '#FFFFFF' : '#0B1120',
        border: isLight ? '1px solid #E2E8F0' : '1px solid #1E293B',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '0.75rem',
        color: '#64748B'
      }}>
        <Sparkles size={20} className="pulse-glow" style={{ color: '#4F46E5' }} />
        <span style={{ fontSize: '0.88rem', fontWeight: 600 }}>Loading 365-day activity telemetry...</span>
      </div>
    );
  }

  const d = data || {
    current_streak: 7,
    longest_streak: 14,
    total_active_days: 22,
    total_problems_solved: 85,
    total_activities_year: 142,
    calendar_days: [],
    monthly_history: [],
    weekly_stats: { this_week_activities: 12, this_week_active_days: 5, completion_rate: 71.4 }
  };

  return (
    <div style={{
      backgroundColor: isLight ? '#FFFFFF' : '#0B1120',
      borderRadius: '18px',
      border: isLight ? '1px solid #E2E8F0' : '1px solid #1E293B',
      boxShadow: isLight ? '0 2px 8px rgba(0, 0, 0, 0.04)' : 'none',
      padding: compact ? '1.25rem 1.4rem' : '1.5rem 1.75rem',
      display: 'flex',
      flexDirection: 'column',
      gap: '1.25rem',
      position: 'relative'
    }}>
      {/* 1. Header with Stats & LeetCode/GitHub Badge */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.2rem' }}>
            <span style={{ fontSize: '1.1rem' }}>🟩</span>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 800, color: isLight ? '#1E1B4B' : '#F8FAFC', margin: 0 }}>
              Learning Activity & Streak Heatmap
            </h3>
            <span style={{
              fontSize: '0.72rem',
              fontWeight: 800,
              padding: '2px 8px',
              borderRadius: '999px',
              backgroundColor: isLight ? '#DCFCE7' : 'rgba(16, 185, 129, 0.15)',
              color: '#16A34A',
              border: isLight ? '1px solid #BBF7D0' : '1px solid rgba(16, 185, 129, 0.3)'
            }}>
              365 Days
            </span>
          </div>
          <p style={{ fontSize: '0.82rem', color: isLight ? '#64748B' : '#94A3B8', margin: 0 }}>
            {d.total_activities_year || 142} learning activities recorded across concepts, visualizers, quizzes, and code challenges.
          </p>
        </div>

        {/* 4 Summary Stat Pills (Streak, Longest, Active Days, Solved) */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          {/* Current Streak */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '0.45rem 0.85rem',
            borderRadius: '10px',
            backgroundColor: isLight ? '#FEF3C7' : 'rgba(245, 158, 11, 0.15)',
            border: isLight ? '1px solid #FDE68A' : '1px solid rgba(245, 158, 11, 0.3)'
          }}>
            <Flame size={16} style={{ color: '#D97706', fill: '#F59E0B' }} />
            <div>
              <div style={{ fontSize: '0.64rem', color: isLight ? '#92400E' : '#FCD34D', fontWeight: 700, textTransform: 'uppercase' }}>Streak</div>
              <div style={{ fontSize: '0.92rem', fontWeight: 800, color: isLight ? '#B45309' : '#F59E0B' }}>
                {d.current_streak} Days
              </div>
            </div>
          </div>

          {/* Longest Streak */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '0.45rem 0.85rem',
            borderRadius: '10px',
            backgroundColor: isLight ? '#EDE9FE' : 'rgba(99, 102, 241, 0.15)',
            border: isLight ? '1px solid #DDD6FE' : '1px solid rgba(99, 102, 241, 0.3)'
          }}>
            <Award size={16} style={{ color: '#6D28D9' }} />
            <div>
              <div style={{ fontSize: '0.64rem', color: isLight ? '#5B21B6' : '#C7D2FE', fontWeight: 700, textTransform: 'uppercase' }}>Best</div>
              <div style={{ fontSize: '0.92rem', fontWeight: 800, color: isLight ? '#6D28D9' : '#818CF8' }}>
                {d.longest_streak} Days
              </div>
            </div>
          </div>

          {/* Active Days */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '0.45rem 0.85rem',
            borderRadius: '10px',
            backgroundColor: isLight ? '#F0FDF4' : 'rgba(16, 185, 129, 0.15)',
            border: isLight ? '1px solid #BBF7D0' : '1px solid rgba(16, 185, 129, 0.3)'
          }}>
            <Calendar size={16} style={{ color: '#16A34A' }} />
            <div>
              <div style={{ fontSize: '0.64rem', color: isLight ? '#166534' : '#86EFAC', fontWeight: 700, textTransform: 'uppercase' }}>Active</div>
              <div style={{ fontSize: '0.92rem', fontWeight: 800, color: isLight ? '#15803D' : '#10B981' }}>
                {d.total_active_days} Days
              </div>
            </div>
          </div>

          {/* Problems Solved */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '0.45rem 0.85rem',
            borderRadius: '10px',
            backgroundColor: isLight ? '#F0F9FF' : 'rgba(56, 189, 248, 0.15)',
            border: isLight ? '1px solid #BAE6FD' : '1px solid rgba(56, 189, 248, 0.3)'
          }}>
            <Code2 size={16} style={{ color: '#0284C7' }} />
            <div>
              <div style={{ fontSize: '0.64rem', color: isLight ? '#0369A1' : '#7DD3FC', fontWeight: 700, textTransform: 'uppercase' }}>Solved</div>
              <div style={{ fontSize: '0.92rem', fontWeight: 800, color: isLight ? '#0284C7' : '#38BDF8' }}>
                {d.total_problems_solved}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 2. The 365-Day Contribution Grid (GitHub / LeetCode Style) */}
      <div style={{
        overflowX: 'auto',
        paddingBottom: '0.5rem',
        position: 'relative'
      }}>
        <div style={{ minWidth: '780px' }}>
          {/* Month Labels on top */}
          <div style={{
            display: 'flex',
            fontSize: '0.72rem',
            fontWeight: 700,
            color: isLight ? '#64748B' : '#94A3B8',
            marginBottom: '6px',
            paddingLeft: '28px',
            position: 'relative',
            height: '16px'
          }}>
            {monthLabels.map((m, idx) => (
              <span
                key={idx}
                style={{
                  position: 'absolute',
                  left: `${28 + m.weekIndex * 14.5}px`
                }}
              >
                {m.name}
              </span>
            ))}
          </div>

          {/* Matrix Container: Day Labels + Week Columns */}
          <div style={{ display: 'flex', gap: '3px', alignItems: 'flex-start' }}>
            {/* Day of Week Labels (Mon, Wed, Fri) */}
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '3px',
              fontSize: '0.64rem',
              fontWeight: 600,
              color: isLight ? '#94A3B8' : '#64748B',
              marginRight: '6px',
              marginTop: '13px'
            }}>
              <span style={{ height: '11px', lineHeight: '11px' }}>Mon</span>
              <span style={{ height: '11px', lineHeight: '11px', marginTop: '11px' }}>Wed</span>
              <span style={{ height: '11px', lineHeight: '11px', marginTop: '11px' }}>Fri</span>
            </div>

            {/* 53 Weekly Columns of 7 Day Squares */}
            <div style={{ display: 'flex', gap: '3.5px' }}>
              {weeks.map((week, wIdx) => (
                <div key={wIdx} style={{ display: 'flex', flexDirection: 'column', gap: '3.5px' }}>
                  {week.map((day, dIdx) => {
                    if (!day) {
                      return (
                        <div
                          key={`empty-${dIdx}`}
                          style={{
                            width: '11px',
                            height: '11px',
                            visibility: 'hidden'
                          }}
                        />
                      );
                    }

                    const bg = getSquareColor(day.level);

                    return (
                      <div
                        key={day.date}
                        onMouseEnter={(e) => {
                          const rect = e.currentTarget.getBoundingClientRect();
                          setHoveredDay(day);
                          setTooltipPos({
                            x: rect.left + rect.width / 2,
                            y: rect.top - 8
                          });
                        }}
                        onMouseLeave={() => setHoveredDay(null)}
                        style={{
                          width: '11.5px',
                          height: '11.5px',
                          borderRadius: '2.5px',
                          backgroundColor: bg,
                          border: isLight 
                            ? (day.level === 0 ? '1px solid #E2E8F0' : 'none')
                            : (day.level === 0 ? '1px solid #1E293B' : 'none'),
                          cursor: 'pointer',
                          transition: 'transform 0.15s ease, filter 0.15s ease'
                        }}
                        onMouseOver={(e) => {
                          e.currentTarget.style.transform = 'scale(1.25)';
                          e.currentTarget.style.zIndex = '10';
                        }}
                        onMouseOut={(e) => {
                          e.currentTarget.style.transform = 'scale(1)';
                          e.currentTarget.style.zIndex = '1';
                        }}
                      />
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Legend Footer (Less -> More Shades of Green) */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginTop: '1rem',
          paddingTop: '0.75rem',
          borderTop: isLight ? '1px solid #F1F5F9' : '1px solid #1E293B'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.74rem', color: isLight ? '#64748B' : '#94A3B8' }}>
            <span>Eligible activities: <strong>DSA Concepts</strong>, <strong>Visualizer Sessions</strong>, <strong>Code Solutions</strong> & <strong>Assessments</strong>.</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.72rem', color: isLight ? '#64748B' : '#94A3B8', fontWeight: 600 }}>
            <span>Less</span>
            {[0, 1, 2, 3, 4].map(lvl => (
              <div
                key={lvl}
                style={{
                  width: '11px',
                  height: '11px',
                  borderRadius: '2.5px',
                  backgroundColor: getSquareColor(lvl),
                  border: isLight && lvl === 0 ? '1px solid #E2E8F0' : 'none'
                }}
              />
            ))}
            <span>More</span>
          </div>
        </div>
      </div>

      {/* 3. Month-by-Month Activity History Section */}
      {!compact && d.monthly_history && d.monthly_history.length > 0 && (
        <div style={{
          backgroundColor: isLight ? '#F8FAFC' : '#0F172A',
          borderRadius: '14px',
          padding: '1rem 1.25rem',
          border: isLight ? '1px solid #E2E8F0' : '1px solid #1E293B',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.75rem'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '0.78rem', fontWeight: 800, color: isLight ? '#1E1B4B' : '#F8FAFC', textTransform: 'uppercase' }}>
              Month-by-Month Learning Frequency
            </span>
            <span style={{ fontSize: '0.72rem', color: '#10B981', fontWeight: 700 }}>
              Past 12 Months
            </span>
          </div>

          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(110px, 1fr))',
            gap: '0.65rem'
          }}>
            {d.monthly_history.map(m => (
              <div
                key={m.month_key}
                style={{
                  padding: '0.55rem 0.75rem',
                  borderRadius: '10px',
                  backgroundColor: isLight ? '#FFFFFF' : '#1E293B',
                  border: isLight ? '1px solid #E2E8F0' : '1px solid #334155',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px'
                }}
              >
                <div style={{ fontSize: '0.68rem', fontWeight: 700, color: '#64748B' }}>
                  {m.month_name}
                </div>
                <div style={{ fontSize: '0.98rem', fontWeight: 800, color: m.activity_count > 0 ? '#10B981' : isLight ? '#94A3B8' : '#64748B' }}>
                  {m.activity_count} <span style={{ fontSize: '0.68rem', fontWeight: 500 }}>acts</span>
                </div>
                <div style={{ fontSize: '0.65rem', color: '#94A3B8' }}>
                  {m.active_days} active days
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Floating Hover Tooltip */}
      {hoveredDay && (
        <div style={{
          position: 'fixed',
          left: `${tooltipPos.x}px`,
          top: `${tooltipPos.y}px`,
          transform: 'translate(-50%, -100%)',
          backgroundColor: '#0F172A',
          color: '#F8FAFC',
          padding: '0.6rem 0.85rem',
          borderRadius: '8px',
          boxShadow: '0 8px 20px rgba(0, 0, 0, 0.4)',
          border: '1px solid #334155',
          fontSize: '0.74rem',
          zIndex: 1000,
          pointerEvents: 'none',
          whiteSpace: 'nowrap',
          display: 'flex',
          flexDirection: 'column',
          gap: '3px'
        }}>
          <div style={{ fontWeight: 800, color: '#38BDF8' }}>
            {new Date(hoveredDay.date + 'T00:00:00').toLocaleDateString('en-US', {
              weekday: 'short',
              year: 'numeric',
              month: 'short',
              day: 'numeric'
            })}
          </div>

          <div style={{ fontWeight: 700, color: hoveredDay.count > 0 ? '#34D399' : '#94A3B8' }}>
            {hoveredDay.count > 0 
              ? `${hoveredDay.count} learning ${hoveredDay.count === 1 ? 'activity' : 'activities'} completed`
              : 'No activity recorded'
            }
          </div>

          {hoveredDay.details && hoveredDay.count > 0 && (
            <div style={{ fontSize: '0.68rem', color: '#CBD5E1', borderTop: '1px solid #334155', paddingTop: '3px', marginTop: '2px' }}>
              {hoveredDay.details.problems_solved > 0 && <div>• {hoveredDay.details.problems_solved} code problems solved</div>}
              {hoveredDay.details.concepts_completed > 0 && <div>• {hoveredDay.details.concepts_completed} concept lessons completed</div>}
              {hoveredDay.details.quizzes_passed > 0 && <div>• {hoveredDay.details.quizzes_passed} mastery quizzes passed</div>}
              {hoveredDay.details.visualizations_run > 0 && <div>• {hoveredDay.details.visualizations_run} visualizer sessions</div>}
              {hoveredDay.details.other_activities > 0 && <div>• {hoveredDay.details.other_activities} submissions / tests</div>}
            </div>
          )}
        </div>
      )}

    </div>
  );
}
