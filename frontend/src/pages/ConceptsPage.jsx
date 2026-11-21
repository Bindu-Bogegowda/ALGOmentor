import React, { useState, useEffect } from 'react';
import { 
  BookOpen, 
  Search, 
  PlayCircle, 
  CheckCircle, 
  Clock, 
  Code2, 
  Copy, 
  Check, 
  Sparkles, 
  Video, 
  ExternalLink,
  ChevronRight,
  Layers,
  ArrowRight,
  ArrowLeft,
  Play,
  Pause,
  RotateCcw,
  AlertTriangle,
  HelpCircle,
  Award,
  Target,
  Compass,
  X,
  Zap,
  Cpu,
  Filter,
  Eye
} from 'lucide-react';
import { api } from '../services/api';

// Helper to extract clean YouTube embed and watch URLs
function getYouTubeDetails(url) {
  if (!url) return { videoId: '', embedUrl: '', watchUrl: '' };
  let videoId = '';
  if (url.includes('/embed/')) {
    videoId = url.split('/embed/')[1]?.split('?')[0]?.split('&')[0];
  } else if (url.includes('watch?v=')) {
    videoId = url.split('watch?v=')[1]?.split('&')[0];
  } else if (url.includes('youtu.be/')) {
    videoId = url.split('youtu.be/')[1]?.split('?')[0];
  } else {
    videoId = url;
  }
  return {
    videoId,
    embedUrl: `https://www.youtube-nocookie.com/embed/${videoId}?rel=0&modestbranding=1&enablejsapi=1`,
    watchUrl: `https://www.youtube.com/watch?v=${videoId}`
  };
}

// Polished Reusable YouTube Video Masterclass Component - Clicks directly to YouTube
function YouTubeMasterclassPlayer({ videoUrl, title, isModal = false }) {
  const { videoId, embedUrl, watchUrl } = getYouTubeDetails(videoUrl);
  const [isHovered, setIsHovered] = useState(false);
  const [thumbError, setThumbError] = useState(false);
  const targetUrl = watchUrl || "https://www.youtube.com";
  const thumbnailUrl = videoId ? `https://img.youtube.com/vi/${videoId}/hqdefault.jpg` : '';

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      gap: '0.75rem',
      backgroundColor: '#070b14',
      borderRadius: '14px',
      border: '1px solid #1e293b',
      overflow: 'hidden',
      padding: '1.25rem'
    }}>
      {/* Player Header with YouTube Badge & Direct External Button */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        flexWrap: 'wrap',
        gap: '0.5rem',
        paddingBottom: '0.75rem',
        borderBottom: '1px solid #1e293b'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '5px',
            backgroundColor: '#ef4444',
            color: '#ffffff',
            fontSize: '0.75rem',
            fontWeight: 800,
            padding: '3px 10px',
            borderRadius: '4px',
            letterSpacing: '0.02em'
          }}>
            <Play size={11} fill="#ffffff" /> YouTube Masterclass
          </span>
          <span style={{ fontSize: '0.92rem', fontWeight: 700, color: '#f8fafc' }}>
            {title || 'Concept Video Masterclass'}
          </span>
        </div>

        <a
          href={targetUrl}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            backgroundColor: '#ef4444',
            color: '#ffffff',
            padding: '6px 14px',
            borderRadius: '8px',
            fontSize: '0.8rem',
            fontWeight: 700,
            textDecoration: 'none',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
            boxShadow: '0 4px 12px rgba(239, 68, 68, 0.3)'
          }}
          onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#dc2626'}
          onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#ef4444'}
        >
          <span>Watch on YouTube</span>
          <ExternalLink size={13} />
        </a>
      </div>

      {/* NATIVE CLICKABLE ANCHOR LINK - CAN NEVER BE BLOCKED BY POPUP BLOCKERS */}
      <a
        href={targetUrl}
        target="_blank"
        rel="noopener noreferrer"
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        style={{
          display: 'block',
          position: 'relative',
          paddingBottom: isModal ? '56.25%' : '48%',
          height: 0,
          overflow: 'hidden',
          borderRadius: '10px',
          backgroundColor: '#0a0f1d',
          backgroundImage: 'radial-gradient(ellipse at center, rgba(30, 41, 59, 0.7) 0%, rgba(10, 15, 29, 0.95) 100%)',
          border: isHovered ? '2px solid #ef4444' : '1px solid #334155',
          cursor: 'pointer',
          textDecoration: 'none',
          transition: 'all 0.25s ease'
        }}
        title="Click here to watch this lecture directly on YouTube"
      >
        {/* Background Thumbnail Image with fallback */}
        {!thumbError && thumbnailUrl && (
          <img
            src={thumbnailUrl}
            alt={title}
            referrerPolicy="no-referrer"
            crossOrigin="anonymous"
            onError={() => setThumbError(true)}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              filter: isHovered ? 'brightness(0.9) scale(1.03)' : 'brightness(0.65)',
              transition: 'all 0.3s ease'
            }}
          />
        )}

        {/* Decorative Grid Patterns if thumbnail fails or behind it */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.3) 50%, rgba(0,0,0,0.6) 100%)',
          pointerEvents: 'none'
        }} />

        {/* Center YouTube Big Play Button */}
        <div style={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: isHovered ? 'translate(-50%, -50%) scale(1.15)' : 'translate(-50%, -50%) scale(1.0)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '10px',
          pointerEvents: 'none',
          transition: 'transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)'
        }}>
          <div style={{
            width: '68px',
            height: '48px',
            backgroundColor: '#ef4444',
            borderRadius: '14px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 8px 24px rgba(239, 68, 68, 0.6), 0 0 20px rgba(239, 68, 68, 0.4)'
          }}>
            <Play size={24} fill="#ffffff" color="#ffffff" style={{ marginLeft: '3px' }} />
          </div>
          <span style={{
            fontSize: '0.85rem',
            fontWeight: 800,
            color: '#ffffff',
            backgroundColor: 'rgba(0,0,0,0.75)',
            padding: '4px 12px',
            borderRadius: '999px',
            border: '1px solid rgba(255,255,255,0.2)',
            letterSpacing: '0.02em',
            boxShadow: '0 4px 12px rgba(0,0,0,0.5)'
          }}>
            ▶ Click to Watch on YouTube
          </span>
        </div>

        {/* Bottom Banner inside the Video */}
        <div style={{
          position: 'absolute',
          bottom: '12px',
          left: '14px',
          right: '14px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'flex-end',
          pointerEvents: 'none'
        }}>
          <div>
            <div style={{ fontSize: '0.72rem', color: '#cbd5e1', fontWeight: 600, textTransform: 'uppercase', marginBottom: '2px' }}>
              Full HD Video Lecture
            </div>
            <div style={{ fontSize: '0.88rem', color: '#ffffff', fontWeight: 700, textShadow: '0 2px 4px rgba(0,0,0,0.8)' }}>
              {title}
            </div>
          </div>
          <span style={{
            fontSize: '0.72rem',
            backgroundColor: 'rgba(0,0,0,0.8)',
            color: 'var(--accent-cyan)',
            padding: '3px 8px',
            borderRadius: '4px',
            border: '1px solid rgba(56, 189, 248, 0.4)',
            fontWeight: 700
          }}>
            HD 1080p ↗
          </span>
        </div>
      </a>

      {/* Helpful Action Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0.65rem 0.85rem',
        borderRadius: '8px',
        backgroundColor: '#0b1120',
        border: '1px solid #1e293b',
        fontSize: '0.78rem',
        color: '#94a3b8'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <Sparkles size={14} style={{ color: 'var(--accent-cyan)' }} />
          <span>Clicking anywhere on this card opens the lesson directly on YouTube.</span>
        </div>
        <a
          href={targetUrl}
          target="_blank"
          rel="noopener noreferrer"
          style={{
            color: 'var(--accent-cyan)',
            fontWeight: 700,
            fontSize: '0.78rem',
            textDecoration: 'none',
            display: 'flex',
            alignItems: 'center',
            gap: '4px'
          }}
        >
          <span>Open Link ↗</span>
        </a>
      </div>
    </div>
  );
}

// Mapping of PDF Roadmap sections to underlying lesson categories
const ROADMAP_CATEGORY_MAPPING = {
  'basic data structures': [
    'basic data structures',
    'arrays',
    'two-dimensional arrays and matrices',
    'strings',
    'linked lists',
    'stack',
    'queue and deque',
    'hashing'
  ],
  'tree data structures': [
    'tree data structures',
    'tries'
  ],
  'advanced data structures': [
    'advanced data structures',
    'complex data structures & indexing',
    'tries'
  ],
  'complex data structures & indexing': [
    'complex data structures & indexing'
  ],
  'problem solving techniques': [
    'problem solving techniques',
    'two pointers and sliding window',
    'prefix sum and difference arrays',
    'mathematical algorithms and number theory',
    'bit manipulation',
    'recursion and backtracking',
    'dynamic programming',
    'greedy algorithms',
    'advanced algorithmic techniques'
  ],
  'graph data structures': [
    'graph data structures'
  ],
  'algorithmic complexity': [
    'algorithmic complexity'
  ],
  'sorting algorithms': [
    'sorting algorithms'
  ],
  'search algorithms': [
    'search algorithms'
  ],
  'programming fundamentals': [
    'programming fundamentals'
  ]
};

const ROADMAP_CATEGORY_OPTIONS = [
  { label: 'All Categories', value: 'All Categories' },
  { label: 'Programming Fundamentals', value: 'Programming Fundamentals' },
  { label: 'Basic Data Structures', value: 'Basic Data Structures' },
  { label: 'Algorithmic Complexity', value: 'Algorithmic Complexity' },
  { label: 'Search Algorithms', value: 'Search Algorithms' },
  { label: 'Sorting Algorithms', value: 'Sorting Algorithms' },
  { label: 'Tree Data Structures', value: 'Tree Data Structures' },
  { label: 'Graph Data Structures', value: 'Graph Data Structures' },
  { label: 'Advanced Data Structures', value: 'Advanced Data Structures' },
  { label: 'Complex Data Structures & Indexing', value: 'Complex Data Structures & Indexing' },
  { label: 'Problem Solving Techniques', value: 'Problem Solving Techniques' },
  // Specific Subcategories for granular filtering
  { label: '── Specific Subtopics ──', value: '', disabled: true },
  { label: 'Arrays', value: 'Arrays' },
  { label: 'Two-Dimensional Arrays and Matrices', value: 'Two-Dimensional Arrays and Matrices' },
  { label: 'Strings', value: 'Strings' },
  { label: 'Linked Lists', value: 'Linked Lists' },
  { label: 'Stack', value: 'Stack' },
  { label: 'Queue and Deque', value: 'Queue and Deque' },
  { label: 'Hashing', value: 'Hashing' },
  { label: 'Two Pointers and Sliding Window', value: 'Two Pointers and Sliding Window' },
  { label: 'Prefix Sum and Difference Arrays', value: 'Prefix Sum and Difference Arrays' },
  { label: 'Dynamic Programming', value: 'Dynamic Programming' },
  { label: 'Greedy Algorithms', value: 'Greedy Algorithms' },
  { label: 'Recursion and Backtracking', value: 'Recursion and Backtracking' },
  { label: 'Bit Manipulation', value: 'Bit Manipulation' }
];

export default function ConceptsPage({ onNavigate, initialLessonId }) {
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);

  // View Mode: 'grid' (the 3-column card library) or 'lesson' (dedicated 11-section learning page)
  const [viewMode, setViewMode] = useState(initialLessonId ? 'lesson' : 'grid');
  const [selectedLesson, setSelectedLesson] = useState(null);

  // Filtering states
  const [search, setSearch] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('All Categories');
  const [difficultyFilter, setDifficultyFilter] = useState('All Difficulties');
  const [progressFilter, setProgressFilter] = useState('All Status'); // 'All Status', 'Not Started', 'In Progress', 'Mastered'

  // Video Walkthrough Modal
  const [videoModalLesson, setVideoModalLesson] = useState(null);

  // Dedicated Lesson View Interactive States
  const [activeLessonTab, setActiveLessonTab] = useState('overview'); // 'overview' | 'explanation' | 'dryrun' | 'code' | 'practice' | 'quiz' | 'connections'
  const [activeCodeLang, setActiveCodeLang] = useState('java');
  const [dryRunStep, setDryRunStep] = useState(0);
  const [isPlayingDryRun, setIsPlayingDryRun] = useState(false);
  const [revealedHints, setRevealedHints] = useState({});
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizResult, setQuizResult] = useState(null);
  const [submittingQuiz, setSubmittingQuiz] = useState(false);
  const [copiedCode, setCopiedCode] = useState(false);
  const [updatingProg, setUpdatingProg] = useState(false);

  useEffect(() => {
    loadLessons();
  }, []);

  useEffect(() => {
    if (initialLessonId && lessons.length > 0) {
      const match = lessons.find(l => l.id === initialLessonId);
      if (match) {
        openLesson(match.id);
      }
    }
  }, [initialLessonId, lessons.length]);

  // Dry run player auto-advance timer
  useEffect(() => {
    let timer = null;
    if (isPlayingDryRun && selectedLesson) {
      const steps = parseJsonSafe(selectedLesson.dry_run, []);
      if (steps.length > 0) {
        timer = setInterval(() => {
          setDryRunStep(prev => {
            if (prev >= steps.length - 1) {
              setIsPlayingDryRun(false);
              return prev;
            }
            return prev + 1;
          });
        }, 1800);
      }
    }
    return () => clearInterval(timer);
  }, [isPlayingDryRun, selectedLesson]);

  async function loadLessons() {
    try {
      const data = await api.listLessons();
      setLessons(data);
    } catch (err) {
      console.error('Failed to load lessons:', err);
    } finally {
      setLoading(false);
    }
  }

  async function openLesson(lessonId) {
    try {
      const detail = await api.getLesson(lessonId);
      setSelectedLesson(detail);
      setViewMode('lesson');
      setActiveCodeLang('java');
      setDryRunStep(0);
      setIsPlayingDryRun(false);
      setRevealedHints({});
      setQuizAnswers({});
      setQuizResult(null);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err) {
      console.error('Failed to load lesson detail:', err);
    }
  }

  function handleBackToGrid() {
    setViewMode('grid');
    setSelectedLesson(null);
  }

  async function toggleComplete() {
    if (!selectedLesson) return;
    setUpdatingProg(true);
    const newStatus = !selectedLesson.is_completed;
    try {
      await api.updateLessonProgress(selectedLesson.id, newStatus, 120);
      setSelectedLesson(prev => ({ 
        ...prev, 
        is_completed: newStatus,
        mastery_level: newStatus ? (prev.mastery_level === 'not_started' ? 'proficient' : prev.mastery_level) : 'not_started'
      }));
      setLessons(prev => prev.map(l => l.id === selectedLesson.id ? { 
        ...l, 
        is_completed: newStatus,
        mastery_level: newStatus ? (l.mastery_level === 'not_started' ? 'proficient' : l.mastery_level) : 'not_started'
      } : l));
    } catch (err) {
      console.error('Failed to update progress:', err);
    } finally {
      setUpdatingProg(false);
    }
  }

  async function handleQuizSubmit() {
    if (!selectedLesson) return;
    setSubmittingQuiz(true);
    try {
      const res = await api.submitLessonQuiz(selectedLesson.id, quizAnswers);
      setQuizResult(res);
      if (res.is_passed) {
        setSelectedLesson(prev => ({
          ...prev,
          is_completed: true,
          mastery_level: res.mastery_level,
          quiz_score: res.score_percent
        }));
        setLessons(prev => prev.map(l => l.id === selectedLesson.id ? {
          ...l,
          is_completed: true,
          mastery_level: res.mastery_level,
          quiz_score: res.score_percent
        } : l));
      }
    } catch (err) {
      console.error('Failed to submit quiz:', err);
    } finally {
      setSubmittingQuiz(false);
    }
  }

  function handleCopy(text) {
    navigator.clipboard.writeText(text);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  }

  function toggleHint(level) {
    setRevealedHints(prev => ({ ...prev, [level]: !prev[level] }));
  }

  function parseJsonSafe(jsonStr, fallback = []) {
    if (!jsonStr) return fallback;
    if (typeof jsonStr !== 'string') return jsonStr;
    try {
      return JSON.parse(jsonStr);
    } catch {
      return fallback;
    }
  }

  // Calculate category count dynamically
  function getCategoryCount(catVal) {
    if (!catVal || catVal === 'All Categories') return lessons.length;
    const catLower = catVal.toLowerCase();
    const allowed = ROADMAP_CATEGORY_MAPPING[catLower] || [catLower];
    return lessons.filter(l => allowed.includes((l.category || '').toLowerCase())).length;
  }

  // Filter lessons with hierarchical roadmap mapping
  const filteredLessons = lessons.filter(l => {
    // Search filter
    const matchesSearch = !search || 
      l.title.toLowerCase().includes(search.toLowerCase()) || 
      (l.summary && l.summary.toLowerCase().includes(search.toLowerCase())) ||
      (l.category && l.category.toLowerCase().includes(search.toLowerCase()));

    // Category filter with roadmap hierarchy support
    const catLower = (categoryFilter || '').toLowerCase();
    let matchesCategory = catLower === 'all categories';
    if (!matchesCategory) {
      const allowedCategories = ROADMAP_CATEGORY_MAPPING[catLower] || [catLower];
      const lessonCatLower = (l.category || '').toLowerCase();
      matchesCategory = allowedCategories.includes(lessonCatLower);
    }

    // Difficulty filter
    const matchesDifficulty = difficultyFilter === 'All Difficulties' || 
      (l.difficulty && l.difficulty.toLowerCase() === difficultyFilter.toLowerCase());

    // Progress filter
    let matchesProgress = true;
    if (progressFilter === 'Not Started') {
      matchesProgress = !l.is_completed && (!l.mastery_level || l.mastery_level === 'not_started');
    } else if (progressFilter === 'In Progress') {
      matchesProgress = l.mastery_level === 'learning' || (l.is_completed && l.mastery_level !== 'mastered');
    } else if (progressFilter === 'Mastered') {
      matchesProgress = l.mastery_level === 'mastered' || l.is_completed;
    }

    return matchesSearch && matchesCategory && matchesDifficulty && matchesProgress;
  });

  const completedCount = lessons.filter(l => l.is_completed).length;

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: '1rem' }}>
        <Sparkles size={36} className="pulse-glow" style={{ color: 'var(--accent-cyan)' }} />
        <span style={{ fontSize: '0.95rem', color: 'var(--text-muted)' }}>Loading AlgoMentor Concept Library...</span>
      </div>
    );
  }

  // ==============================================================
  // VIEW MODE 1: THE 3-COLUMN COMPACT DARK NAVY CARDS GRID
  // ==============================================================
  if (viewMode === 'grid') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', minHeight: '85vh', paddingBottom: '3rem' }}>
        
        {/* Header Section */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '0.25rem' }}>
                <h1 style={{ fontSize: '1.85rem', fontWeight: 800, color: '#f8fafc', margin: 0, letterSpacing: '-0.02em' }}>
                  Learn Concepts
                </h1>
                <span style={{
                  fontSize: '0.75rem',
                  fontWeight: 800,
                  padding: '3px 10px',
                  borderRadius: '999px',
                  backgroundColor: 'rgba(56, 189, 248, 0.15)',
                  color: 'var(--accent-cyan)',
                  border: '1px solid rgba(56, 189, 248, 0.3)'
                }}>
                  {lessons.length} Total Concepts
                </span>
              </div>
              <p style={{ fontSize: '0.88rem', color: '#94a3b8', margin: 0, maxWidth: '750px', lineHeight: 1.5 }}>
                Master the complete interconnected Data Structures & Algorithms learning library. Explore concepts with step-by-step visualizers, dry runs, production code, and mastery assessments.
              </p>
            </div>

            {/* Quick Completion Stats */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', padding: '0.6rem 1rem', borderRadius: '10px', backgroundColor: '#0f172a', border: '1px solid #1e293b' }}>
              <div>
                <div style={{ fontSize: '0.7rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Completed</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#10b981' }}>{completedCount} / {lessons.length}</div>
              </div>
              <div style={{ width: '1px', height: '30px', backgroundColor: '#334155' }} />
              <div>
                <div style={{ fontSize: '0.7rem', color: '#64748b', fontWeight: 600, textTransform: 'uppercase' }}>Progress</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>
                  {lessons.length > 0 ? Math.round((completedCount / lessons.length) * 100) : 0}%
                </div>
              </div>
            </div>
          </div>

          {/* Search & Filter Control Bar */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            flexWrap: 'wrap',
            padding: '0.85rem 1rem',
            borderRadius: '12px',
            backgroundColor: '#0b1120',
            border: '1px solid #1e293b',
            boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.2)'
          }}>
            {/* Search Input */}
            <div style={{ position: 'relative', flex: '1 1 240px', minWidth: '220px' }}>
              <Search size={15} style={{ position: 'absolute', left: '12px', top: '11px', color: '#64748b' }} />
              <input
                type="text"
                placeholder="Search concepts, algorithms, data structures..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem 0.75rem 0.5rem 2.25rem',
                  borderRadius: '8px',
                  border: '1px solid #334155',
                  backgroundColor: '#0f172a',
                  color: '#f8fafc',
                  fontSize: '0.82rem',
                  outline: 'none'
                }}
              />
            </div>

            {/* Category Dropdown */}
            <div style={{ minWidth: '180px', flex: '1 1 180px' }}>
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #334155',
                  backgroundColor: '#0f172a',
                  color: '#f8fafc',
                  fontSize: '0.82rem',
                  outline: 'none',
                  cursor: 'pointer'
                }}
              >
                {ROADMAP_CATEGORY_OPTIONS.map(opt => (
                  <option 
                    key={opt.value || opt.label} 
                    value={opt.value} 
                    disabled={opt.disabled}
                  >
                    {opt.disabled ? opt.label : `${opt.label} (${getCategoryCount(opt.value)})`}
                  </option>
                ))}
              </select>
            </div>

            {/* Difficulty Filter Dropdown */}
            <div style={{ minWidth: '130px' }}>
              <select
                value={difficultyFilter}
                onChange={(e) => setDifficultyFilter(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #334155',
                  backgroundColor: '#0f172a',
                  color: '#f8fafc',
                  fontSize: '0.82rem',
                  outline: 'none',
                  cursor: 'pointer'
                }}
              >
                <option value="All Difficulties">All Difficulties</option>
                <option value="Beginner">🟢 Beginner</option>
                <option value="Intermediate">🟠 Intermediate</option>
                <option value="Advanced">🔴 Advanced</option>
              </select>
            </div>

            {/* Progress Status Filter */}
            <div style={{ minWidth: '120px' }}>
              <select
                value={progressFilter}
                onChange={(e) => setProgressFilter(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.5rem 0.75rem',
                  borderRadius: '8px',
                  border: '1px solid #334155',
                  backgroundColor: '#0f172a',
                  color: '#f8fafc',
                  fontSize: '0.82rem',
                  outline: 'none',
                  cursor: 'pointer'
                }}
              >
                <option value="All Status">All Status</option>
                <option value="Not Started">Not Started</option>
                <option value="In Progress">In Progress</option>
                <option value="Mastered">Mastered ✓</option>
              </select>
            </div>

            {/* Reset Filters / Showing count */}
            {(search || categoryFilter !== 'All Categories' || difficultyFilter !== 'All Difficulties' || progressFilter !== 'All Status') && (
              <button
                onClick={() => {
                  setSearch('');
                  setCategoryFilter('All Categories');
                  setDifficultyFilter('All Difficulties');
                  setProgressFilter('All Status');
                }}
                style={{
                  padding: '0.45rem 0.75rem',
                  borderRadius: '8px',
                  border: '1px solid rgba(239, 68, 68, 0.3)',
                  backgroundColor: 'rgba(239, 68, 68, 0.1)',
                  color: '#f87171',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                Reset Filters
              </button>
            )}

            <span style={{ fontSize: '0.75rem', color: '#64748b', marginLeft: 'auto', fontWeight: 600 }}>
              Showing {filteredLessons.length} cards
            </span>
          </div>
        </div>

        {/* ============================================================== */}
        {/* RESPONSIVE THREE-COLUMN GRID OF COMPACT DARK NAVY CONCEPT CARDS */}
        {/* ============================================================== */}
        {filteredLessons.length > 0 ? (
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
            gap: '1.25rem'
          }}>
            {filteredLessons.map((concept) => {
              const diff = (concept.difficulty || 'Beginner').toLowerCase();
              return (
                <div
                  key={concept.id}
                  style={{
                    backgroundColor: '#0B1120',
                    border: '1px solid #1E293B',
                    borderRadius: '12px',
                    padding: '1.15rem',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.15)',
                    transition: 'border-color 0.2s ease, transform 0.2s ease',
                    position: 'relative'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.borderColor = 'rgba(56, 189, 248, 0.4)';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.borderColor = '#1E293B';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }}
                >
                  <div>
                    {/* Top Row: Category Name + Difficulty Badge */}
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                      <span style={{
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        color: 'var(--accent-cyan)',
                        letterSpacing: '0.04em',
                        textTransform: 'uppercase'
                      }}>
                        {concept.category || 'DSA'}
                      </span>

                      {/* Difficulty Level with appropriate green/orange/red colors */}
                      <span style={{
                        fontSize: '0.68rem',
                        fontWeight: 700,
                        padding: '2px 8px',
                        borderRadius: '6px',
                        backgroundColor: diff === 'beginner' ? 'rgba(16, 185, 129, 0.15)' :
                                         diff === 'intermediate' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: diff === 'beginner' ? '#10b981' :
                               diff === 'intermediate' ? '#f59e0b' : '#ef4444',
                        border: diff === 'beginner' ? '1px solid rgba(16, 185, 129, 0.3)' :
                                diff === 'intermediate' ? '1px solid rgba(245, 158, 11, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)'
                      }}>
                        {concept.difficulty || 'Beginner'}
                      </span>
                    </div>

                    {/* Prerequisite Information / Learning Sequence */}
                    <div style={{
                      fontSize: '0.72rem',
                      color: '#64748b',
                      marginBottom: '0.5rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '6px'
                    }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '4px', overflow: 'hidden' }}>
                        <span style={{ color: '#94a3b8', fontWeight: 600 }}>Prereq:</span>
                        <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                          {concept.prerequisites || 'None'}
                        </span>
                      </div>
                      <span style={{
                        fontSize: '0.64rem',
                        fontWeight: 700,
                        color: 'var(--accent-cyan)',
                        backgroundColor: 'rgba(56, 189, 248, 0.1)',
                        padding: '1px 6px',
                        borderRadius: '4px',
                        whiteSpace: 'nowrap',
                        border: '1px solid rgba(56, 189, 248, 0.2)'
                      }}>
                        Lvl {concept.level_number || 1}
                      </span>
                    </div>

                    {/* Concept Title */}
                    <h3 style={{
                      fontSize: '0.98rem',
                      fontWeight: 700,
                      color: '#f8fafc',
                      margin: '0 0 0.45rem 0',
                      lineHeight: 1.35,
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden'
                    }}>
                      {concept.title}
                    </h3>

                    {/* Short Description */}
                    <p style={{
                      fontSize: '0.8rem',
                      color: '#94a3b8',
                      lineHeight: 1.45,
                      margin: '0 0 1rem 0',
                      display: '-webkit-box',
                      WebkitLineClamp: 2,
                      WebkitBoxOrient: 'vertical',
                      overflow: 'hidden'
                    }}>
                      {concept.summary}
                    </p>
                  </div>

                  {/* 4 Action Buttons on Every Card */}
                  <div style={{
                    display: 'grid',
                    gridTemplateColumns: '1fr 1fr',
                    gap: '6px',
                    paddingTop: '0.65rem',
                    borderTop: '1px solid #1e293b'
                  }}>
                    {/* 1. Open Lessons */}
                    <button
                      onClick={() => openLesson(concept.id)}
                      style={{
                        padding: '0.45rem 0.5rem',
                        borderRadius: '6px',
                        border: '1px solid rgba(56, 189, 248, 0.4)',
                        backgroundColor: 'rgba(56, 189, 248, 0.1)',
                        color: 'var(--accent-cyan)',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '4px',
                        transition: 'background-color 0.15s ease'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = 'rgba(56, 189, 248, 0.2)'}
                      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'rgba(56, 189, 248, 0.1)'}
                    >
                      <BookOpen size={13} />
                      <span>Open Lessons</span>
                    </button>

                    {/* 2. Videos - Clicks Directly to YouTube */}
                    <button
                      onClick={() => {
                        const { watchUrl } = getYouTubeDetails(concept.video_url);
                        if (watchUrl) {
                          window.open(watchUrl, '_blank', 'noopener,noreferrer');
                        } else {
                          setVideoModalLesson(concept);
                        }
                      }}
                      style={{
                        padding: '0.45rem 0.5rem',
                        borderRadius: '6px',
                        border: '1px solid #334155',
                        backgroundColor: '#0f172a',
                        color: '#cbd5e1',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '4px',
                        transition: 'all 0.15s ease'
                      }}
                      onMouseEnter={(e) => { e.currentTarget.style.backgroundColor = '#ef4444'; e.currentTarget.style.color = '#ffffff'; e.currentTarget.style.borderColor = '#ef4444'; }}
                      onMouseLeave={(e) => { e.currentTarget.style.backgroundColor = '#0f172a'; e.currentTarget.style.color = '#cbd5e1'; e.currentTarget.style.borderColor = '#334155'; }}
                      title="Watch this lecture on YouTube"
                    >
                      <Video size={13} style={{ color: '#ef4444' }} />
                      <span>YouTube ↗</span>
                    </button>

                    {/* 3. Visualize */}
                    <button
                      onClick={() => onNavigate && onNavigate('visualizer', { algorithm: concept.visualization_algorithm || 'bubble_sort' })}
                      style={{
                        padding: '0.45rem 0.5rem',
                        borderRadius: '6px',
                        border: '1px solid #334155',
                        backgroundColor: '#0f172a',
                        color: '#cbd5e1',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '4px',
                        transition: 'background-color 0.15s ease'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#1e293b'}
                      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f172a'}
                    >
                      <Zap size={13} style={{ color: '#f59e0b' }} />
                      <span>Visualize</span>
                    </button>

                    {/* 4. Practice */}
                    <button
                      onClick={() => onNavigate && onNavigate('practice', { problem: concept.practice_problem_slug || 'two-sum', language: 'java' })}
                      style={{
                        padding: '0.45rem 0.5rem',
                        borderRadius: '6px',
                        border: '1px solid #334155',
                        backgroundColor: '#0f172a',
                        color: '#cbd5e1',
                        fontSize: '0.75rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '4px',
                        transition: 'background-color 0.15s ease'
                      }}
                      onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#1e293b'}
                      onMouseLeave={(e) => e.currentTarget.style.backgroundColor = '#0f172a'}
                    >
                      <Code2 size={13} style={{ color: '#10b981' }} />
                      <span>Practice</span>
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        ) : (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '4rem 2rem',
            borderRadius: '12px',
            backgroundColor: '#0B1120',
            border: '1px dashed #334155',
            color: '#94a3b8'
          }}>
            <Compass size={40} style={{ color: '#475569', marginBottom: '1rem' }} />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem' }}>No concepts found matching your filters</h3>
            <p style={{ fontSize: '0.85rem', color: '#64748b', margin: '0 0 1.25rem 0' }}>Try clearing the search query or changing category and difficulty filters.</p>
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap', justifyContent: 'center' }}>
              <button
                onClick={() => {
                  setSearch('');
                  setCategoryFilter('All Categories');
                  setDifficultyFilter('All Difficulties');
                  setProgressFilter('All Status');
                }}
                style={{
                  padding: '0.6rem 1.25rem',
                  borderRadius: '8px',
                  border: 'none',
                  backgroundColor: '#4F46E5',
                  color: '#ffffff',
                  fontSize: '0.84rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  boxShadow: '0 4px 12px rgba(79, 70, 229, 0.35)'
                }}
              >
                <RotateCcw size={15} />
                <span>Show All Concepts ({lessons.length || 87})</span>
              </button>
              <button
                onClick={() => loadLessons()}
                style={{
                  padding: '0.6rem 1rem',
                  borderRadius: '8px',
                  border: '1px solid #334155',
                  backgroundColor: '#0f172a',
                  color: '#94a3b8',
                  fontSize: '0.84rem',
                  fontWeight: 600,
                  cursor: 'pointer'
                }}
              >
                Reload Library
              </button>
            </div>
          </div>
        )}

        {/* Video Player Modal */}
        {videoModalLesson && (
          <div style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            backdropFilter: 'blur(8px)',
            zIndex: 1000,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '1.5rem'
          }}>
            <div style={{
              width: '100%',
              maxWidth: '850px',
              backgroundColor: '#0b1120',
              border: '1px solid #1e293b',
              borderRadius: '16px',
              padding: '1.25rem 1.5rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '1rem'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <Video size={18} style={{ color: '#ef4444' }} />
                  <span style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f8fafc' }}>
                    {videoModalLesson.video_title || videoModalLesson.title}
                  </span>
                </div>
                <button
                  onClick={() => setVideoModalLesson(null)}
                  style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}
                >
                  <X size={20} />
                </button>
              </div>

              <YouTubeMasterclassPlayer
                videoUrl={videoModalLesson.video_url}
                title={videoModalLesson.video_title || videoModalLesson.title}
                isModal={true}
              />

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px' }}>
                <button
                  onClick={() => {
                    const id = videoModalLesson.id;
                    setVideoModalLesson(null);
                    openLesson(id);
                  }}
                  className="btn-gradient"
                  style={{ padding: '0.45rem 1rem', fontSize: '0.8rem' }}
                >
                  Open Complete Lesson
                </button>
              </div>
            </div>
          </div>
        )}

      </div>
    );
  }

  // ==============================================================
  // VIEW MODE 2: DEDICATED 11-SECTION CONCEPT LEARNING PAGE
  // ==============================================================
  const dryRunSteps = selectedLesson ? parseJsonSafe(selectedLesson.dry_run, []) : [];
  const currentDryStep = dryRunSteps[dryRunStep] || null;
  const practiceQuestions = selectedLesson ? parseJsonSafe(selectedLesson.practice_questions, []) : [];
  const aiHints = selectedLesson ? parseJsonSafe(selectedLesson.ai_hints, []) : [];
  const quizQuestions = selectedLesson ? parseJsonSafe(selectedLesson.quiz_questions, []) : [];
  const conceptConnections = selectedLesson ? parseJsonSafe(selectedLesson.concept_connections, {}) : {};

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', minHeight: '85vh', paddingBottom: '3rem' }}>
      
      {/* Top Navigation & Status Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem',
        padding: '0.85rem 1.25rem',
        borderRadius: '12px',
        backgroundColor: '#0b1120',
        border: '1px solid #1e293b'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <button
            onClick={handleBackToGrid}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '0.4rem 0.85rem',
              borderRadius: '8px',
              border: '1px solid #334155',
              backgroundColor: '#0f172a',
              color: '#f8fafc',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              transition: 'background-color 0.15s ease'
            }}
          >
            <ArrowLeft size={14} />
            <span>Back to Concepts Library</span>
          </button>

          <span style={{ color: '#475569' }}>|</span>

          <span style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>
            {selectedLesson.category}
          </span>

          <span style={{
            fontSize: '0.68rem',
            padding: '2px 8px',
            borderRadius: '6px',
            backgroundColor: selectedLesson.difficulty === 'Beginner' ? 'rgba(16, 185, 129, 0.15)' :
                             selectedLesson.difficulty === 'Intermediate' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(239, 68, 68, 0.15)',
            color: selectedLesson.difficulty === 'Beginner' ? '#10b981' :
                   selectedLesson.difficulty === 'Intermediate' ? '#f59e0b' : '#ef4444',
            border: selectedLesson.difficulty === 'Beginner' ? '1px solid rgba(16, 185, 129, 0.3)' :
                    selectedLesson.difficulty === 'Intermediate' ? '1px solid rgba(245, 158, 11, 0.3)' : '1px solid rgba(239, 68, 68, 0.3)',
            fontWeight: 700
          }}>
            {selectedLesson.difficulty || 'Beginner'}
          </span>
        </div>

        {/* Action Controls & Prev/Next */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {selectedLesson.prev_lesson_id && (
            <button
              onClick={() => openLesson(selectedLesson.prev_lesson_id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                padding: '0.4rem 0.75rem',
                borderRadius: '6px',
                border: '1px solid #334155',
                backgroundColor: '#0f172a',
                color: '#cbd5e1',
                fontSize: '0.75rem',
                cursor: 'pointer'
              }}
              title="Previous Concept"
            >
              <ArrowLeft size={13} />
              <span>Prev</span>
            </button>
          )}

          {selectedLesson.next_lesson_id && (
            <button
              onClick={() => openLesson(selectedLesson.next_lesson_id)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                padding: '0.4rem 0.75rem',
                borderRadius: '6px',
                border: '1px solid #334155',
                backgroundColor: '#0f172a',
                color: '#cbd5e1',
                fontSize: '0.75rem',
                cursor: 'pointer'
              }}
              title="Next Concept"
            >
              <span>Next</span>
              <ArrowRight size={13} />
            </button>
          )}

          <button
            onClick={toggleComplete}
            disabled={updatingProg}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              padding: '0.4rem 0.85rem',
              borderRadius: '6px',
              border: selectedLesson.is_completed ? '1px solid #10b981' : '1px solid #334155',
              backgroundColor: selectedLesson.is_completed ? 'rgba(16, 185, 129, 0.15)' : '#0f172a',
              color: selectedLesson.is_completed ? '#10b981' : '#cbd5e1',
              fontSize: '0.76rem',
              fontWeight: 700,
              cursor: 'pointer'
            }}
          >
            <CheckCircle size={14} />
            <span>{selectedLesson.is_completed ? 'Mastered ✓' : 'Mark as Complete'}</span>
          </button>
        </div>
      </div>

      {/* Concept Title Header Banner */}
      <div style={{
        padding: '1.75rem 2rem',
        borderRadius: '16px',
        backgroundColor: '#0B1120',
        border: '1px solid #1E293B'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem', marginBottom: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.5rem' }}>
              <span style={{ fontSize: '0.72rem', fontWeight: 800, color: 'var(--accent-cyan)', textTransform: 'uppercase' }}>
                {selectedLesson.category}
              </span>
              <span style={{ color: '#475569' }}>·</span>
              <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                Prerequisites: <strong style={{ color: '#cbd5e1' }}>{selectedLesson.prerequisites || 'None'}</strong>
              </span>
            </div>
            <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#f8fafc', margin: '0 0 0.5rem 0' }}>
              {selectedLesson.title}
            </h1>
            <p style={{ fontSize: '0.92rem', color: '#94a3b8', margin: 0, maxWidth: '850px', lineHeight: 1.5 }}>
              {selectedLesson.summary}
            </p>
          </div>

          <div style={{ display: 'flex', gap: '8px' }}>
            <span style={{ fontSize: '0.76rem', padding: '4px 10px', borderRadius: '8px', backgroundColor: '#0f172a', border: '1px solid #334155', color: 'var(--accent-cyan)', fontWeight: 600 }}>
              ⏱ {selectedLesson.time_complexity}
            </span>
            <span style={{ fontSize: '0.76rem', padding: '4px 10px', borderRadius: '8px', backgroundColor: '#0f172a', border: '1px solid #334155', color: '#c084fc', fontWeight: 600 }}>
              💾 {selectedLesson.space_complexity}
            </span>
          </div>
        </div>

        {/* Section Tabs Bar */}
        <div style={{
          display: 'flex',
          gap: '4px',
          borderBottom: '1px solid #1e293b',
          paddingTop: '0.5rem',
          overflowX: 'auto'
        }}>
          {[
            { id: 'overview', label: '1. Introduction & Overview', icon: <BookOpen size={14} /> },
            { id: 'explanation', label: '2. Detailed Explanation', icon: <Layers size={14} /> },
            { id: 'dryrun', label: '3. Visualizer & Dry Run', icon: <PlayCircle size={14} /> },
            { id: 'code', label: '4. Code (Java & Python)', icon: <Code2 size={14} /> },
            { id: 'practice', label: '5. Practice & AI Hints', icon: <Target size={14} /> },
            { id: 'quiz', label: '6. Mastery Assessment', icon: <Award size={14} /> },
            { id: 'connections', label: '7. Concept Connections', icon: <Compass size={14} /> }
          ].map(tab => {
            const isActive = activeLessonTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveLessonTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '0.65rem 1rem',
                  border: 'none',
                  borderBottom: isActive ? '2px solid var(--accent-cyan)' : '2px solid transparent',
                  backgroundColor: 'transparent',
                  color: isActive ? 'var(--accent-cyan)' : '#94a3b8',
                  fontSize: '0.82rem',
                  fontWeight: isActive ? 700 : 500,
                  cursor: 'pointer',
                  whiteSpace: 'nowrap',
                  transition: 'all 0.15s ease'
                }}
              >
                {tab.icon}
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* SECTION 1 & 2: INTRODUCTION, WHY LEARN IT, PREREQUISITES, COMPLEXITY */}
      {activeLessonTab === 'overview' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* SECTION 1: Introduction */}
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Sparkles size={16} style={{ color: 'var(--accent-cyan)' }} />
              SECTION 1: Introduction & Fundamental Definition
            </h3>
            <p style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.7, margin: 0 }}>
              {selectedLesson.fundamental_explanation}
            </p>
          </div>

          {/* Why do we use it & Real-world applications */}
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B', borderLeft: '4px solid var(--accent-cyan)' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Compass size={16} style={{ color: 'var(--accent-cyan)' }} />
              Why Do We Use It? Real-World Applications
            </h3>
            <p style={{ fontSize: '0.88rem', color: '#cbd5e1', lineHeight: 1.6, margin: 0 }}>
              {selectedLesson.why_learn_it || selectedLesson.real_world_applications}
            </p>
          </div>

          {/* SECTION 2 & 7: Prerequisites & Complexity Analysis */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
            <div style={{ padding: '1.25rem', borderRadius: '12px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem' }}>
                SECTION 2: Prerequisites
              </h4>
              <p style={{ fontSize: '0.84rem', color: '#cbd5e1', margin: 0 }}>
                {selectedLesson.prerequisites || 'Basic Programming Logic'}
              </p>
            </div>

            <div style={{ padding: '1.25rem', borderRadius: '12px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
              <h4 style={{ fontSize: '0.9rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem' }}>
                SECTION 7: Complexity Analysis
              </h4>
              <div style={{ fontSize: '0.84rem', color: '#cbd5e1', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                <div><strong>Time Complexity:</strong> <span style={{ color: 'var(--accent-cyan)' }}>{selectedLesson.time_complexity}</span></div>
                <div><strong>Space Complexity:</strong> <span style={{ color: '#c084fc' }}>{selectedLesson.space_complexity}</span></div>
              </div>
            </div>
          </div>

          {/* Embedded Masterclass Video */}
          {selectedLesson.video_url && (
            <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Video size={16} style={{ color: '#ef4444' }} />
                SECTION 2: Curated Video Lecture Walkthrough
              </h3>
              <YouTubeMasterclassPlayer
                videoUrl={selectedLesson.video_url}
                title={selectedLesson.video_title || selectedLesson.title}
                isModal={false}
              />
            </div>
          )}
        </div>
      )}

      {/* SECTION 3: DETAILED EXPLANATION */}
      {activeLessonTab === 'explanation' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Layers size={18} style={{ color: '#10b981' }} />
              SECTION 3: Detailed Step-by-Step Explanation & Mechanics
            </h3>
            <div style={{ fontSize: '0.9rem', color: '#cbd5e1', lineHeight: 1.7, whiteSpace: 'pre-line' }}>
              {selectedLesson.core_theory || selectedLesson.step_by_step}
            </div>
          </div>

          {/* Common Mistakes & Edge Cases */}
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B', borderLeft: '4px solid #ef4444' }}>
            <h4 style={{ fontSize: '0.98rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <AlertTriangle size={16} style={{ color: '#ef4444' }} />
              Common Student Pitfalls & Edge Cases
            </h4>
            <div style={{ fontSize: '0.86rem', color: '#cbd5e1', lineHeight: 1.6, whiteSpace: 'pre-line' }}>
              {selectedLesson.common_mistakes || "1. Off-by-one index calculations on boundary loops.\n2. Omitting empty or single-element corner cases.\n3. Allocating extra memory unnecessarily."}
            </div>
          </div>
        </div>
      )}

      {/* SECTION 4 & 5: INTERACTIVE VISUALIZATION & DRY RUN */}
      {activeLessonTab === 'dryrun' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Section 4: Interactive Visualization Link */}
          <div style={{
            padding: '1.5rem',
            borderRadius: '14px',
            backgroundColor: '#0B1120',
            border: '1px solid #1E293B',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '1rem',
            background: 'linear-gradient(135deg, rgba(56, 189, 248, 0.08), rgba(168, 85, 247, 0.08))'
          }}>
            <div>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.25rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Cpu size={18} style={{ color: 'var(--accent-cyan)' }} />
                SECTION 4: Interactive Algorithm Visualizer
              </h3>
              <p style={{ fontSize: '0.84rem', color: '#94a3b8', margin: 0 }}>
                Launch the dedicated execution visualizer to inspect live animations with speed control, step play, and variable tracing.
              </p>
            </div>

            <button
              onClick={() => onNavigate && onNavigate('visualizer', { algorithm: selectedLesson.visualization_algorithm || 'bubble_sort' })}
              className="btn-gradient"
              style={{ display: 'flex', alignItems: 'center', gap: '6px', padding: '0.55rem 1.25rem', fontSize: '0.84rem' }}
            >
              <PlayCircle size={16} />
              Launch Interactive Visualizer
            </button>
          </div>

          {/* Section 5: Step-by-Step Dry Run Simulator */}
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
                <PlayCircle size={16} style={{ color: 'var(--accent-cyan)' }} />
                SECTION 5: Step-by-Step Dry Run Simulator
              </h3>

              {/* Controls */}
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <button
                  onClick={() => setDryRunStep(prev => Math.max(0, prev - 1))}
                  disabled={dryRunStep === 0}
                  className="btn-glass"
                  style={{ padding: '4px 10px', fontSize: '0.78rem' }}
                >
                  <ArrowLeft size={14} />
                </button>
                
                <button
                  onClick={() => setIsPlayingDryRun(!isPlayingDryRun)}
                  className="btn-glass"
                  style={{ padding: '4px 12px', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--accent-cyan)' }}
                >
                  {isPlayingDryRun ? <Pause size={14} /> : <Play size={14} />}
                  <span>{isPlayingDryRun ? 'Pause' : 'Auto Play'}</span>
                </button>

                <button
                  onClick={() => setDryRunStep(prev => Math.min(dryRunSteps.length - 1, prev + 1))}
                  disabled={dryRunStep >= dryRunSteps.length - 1}
                  className="btn-glass"
                  style={{ padding: '4px 10px', fontSize: '0.78rem' }}
                >
                  <ArrowRight size={14} />
                </button>

                <button
                  onClick={() => { setDryRunStep(0); setIsPlayingDryRun(false); }}
                  className="btn-glass"
                  style={{ padding: '4px 10px', fontSize: '0.78rem' }}
                  title="Reset"
                >
                  <RotateCcw size={14} />
                </button>
              </div>
            </div>

            {dryRunSteps.length > 0 ? (
              <div>
                {/* Step Pills */}
                <div style={{ display: 'flex', gap: '6px', marginBottom: '1.25rem', overflowX: 'auto', paddingBottom: '4px' }}>
                  {dryRunSteps.map((s, idx) => (
                    <button
                      key={idx}
                      onClick={() => setDryRunStep(idx)}
                      style={{
                        padding: '4px 10px',
                        borderRadius: '6px',
                        border: dryRunStep === idx ? '1px solid var(--accent-cyan)' : '1px solid #334155',
                        backgroundColor: dryRunStep === idx ? 'rgba(56, 189, 248, 0.2)' : '#0f172a',
                        color: dryRunStep === idx ? 'var(--accent-cyan)' : '#94a3b8',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        cursor: 'pointer'
                      }}
                    >
                      Step {s.step || idx + 1}
                    </button>
                  ))}
                </div>

                {/* Active Step Card */}
                {currentDryStep && (
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1rem' }}>
                    <div style={{ backgroundColor: '#0f172a', padding: '1.25rem', borderRadius: '10px', border: '1px solid #1e293b' }}>
                      <div style={{ fontSize: '0.72rem', fontWeight: 800, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                        Step {currentDryStep.step} Action
                      </div>
                      <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.75rem' }}>
                        {currentDryStep.action}
                      </div>
                      <p style={{ fontSize: '0.84rem', color: '#94a3b8', lineHeight: 1.6, margin: 0 }}>
                        {currentDryStep.notes}
                      </p>
                    </div>

                    <div style={{ backgroundColor: '#0f172a', padding: '1.25rem', borderRadius: '10px', border: '1px solid #1e293b' }}>
                      <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#c084fc', textTransform: 'uppercase', marginBottom: '0.75rem' }}>
                        Live Variable State & Memory Values
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        {currentDryStep.variables && Object.entries(currentDryStep.variables).map(([key, val]) => (
                          <div key={key} style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', backgroundColor: '#0b1120', borderRadius: '6px', fontFamily: 'monospace', fontSize: '0.82rem' }}>
                            <span style={{ color: 'var(--accent-cyan)' }}>{key}:</span>
                            <span style={{ color: '#10b981', fontWeight: 700 }}>{String(val)}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <p style={{ fontSize: '0.85rem', color: '#64748b' }}>Dry run sequence loading...</p>
            )}
          </div>
        </div>
      )}

      {/* SECTION 6: CODE IMPLEMENTATION (JAVA & PYTHON) */}
      {activeLessonTab === 'code' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', flexWrap: 'wrap', gap: '0.75rem' }}>
              <div style={{ display: 'flex', gap: '6px' }}>
                <button
                  onClick={() => setActiveCodeLang('java')}
                  style={{
                    padding: '0.45rem 1rem',
                    borderRadius: '6px',
                    border: activeCodeLang === 'java' ? '1px solid #f59e0b' : '1px solid #334155',
                    backgroundColor: activeCodeLang === 'java' ? 'rgba(245, 158, 11, 0.2)' : '#0f172a',
                    color: activeCodeLang === 'java' ? '#fbbf24' : '#94a3b8',
                    fontSize: '0.82rem',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                >
                  ☕ Java Solution (Primary)
                </button>
                <button
                  onClick={() => setActiveCodeLang('python')}
                  style={{
                    padding: '0.45rem 1rem',
                    borderRadius: '6px',
                    border: activeCodeLang === 'python' ? '1px solid var(--accent-cyan)' : '1px solid #334155',
                    backgroundColor: activeCodeLang === 'python' ? 'rgba(56, 189, 248, 0.15)' : '#0f172a',
                    color: activeCodeLang === 'python' ? 'var(--accent-cyan)' : '#94a3b8',
                    fontSize: '0.82rem',
                    fontWeight: 700,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                >
                  🐍 Python 3 Solution
                </button>
              </div>

              <div style={{ display: 'flex', gap: '8px' }}>
                <button
                  onClick={() => handleCopy(activeCodeLang === 'java' ? selectedLesson.java_code : selectedLesson.python_code)}
                  className="btn-glass"
                  style={{ padding: '0.35rem 0.75rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '4px' }}
                >
                  {copiedCode ? <Check size={14} style={{ color: '#10b981' }} /> : <Copy size={14} />}
                  <span>{copiedCode ? 'Copied!' : 'Copy Code'}</span>
                </button>

                <button
                  onClick={() => onNavigate && onNavigate('practice', { problem: selectedLesson.practice_problem_slug || 'two-sum', language: activeCodeLang || 'java' })}
                  className="btn-gradient"
                  style={{ padding: '0.35rem 0.9rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '4px' }}
                >
                  <Code2 size={14} />
                  <span>Open in Code Editor</span>
                </button>
              </div>
            </div>

            <div style={{
              backgroundColor: '#070b14',
              borderRadius: '10px',
              border: '1px solid #1e293b',
              padding: '1.25rem',
              overflowX: 'auto',
              fontFamily: 'Consolas, Monaco, "Courier New", monospace',
              fontSize: '0.86rem',
              lineHeight: 1.6,
              color: '#e2e8f0'
            }}>
              <pre style={{ margin: 0 }}>
                {activeCodeLang === 'java'
                  ? (selectedLesson.java_code || '// Java solution')
                  : (selectedLesson.python_code || selectedLesson.pseudocode || '# Python solution')
                }
              </pre>
            </div>
          </div>
        </div>
      )}

      {/* SECTION 8 & 9: PRACTICE PROBLEMS & 3-LEVEL AI HINTS */}
      {activeLessonTab === 'practice' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          {/* Section 8: Practice Problems */}
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Target size={16} style={{ color: 'var(--accent-cyan)' }} />
              SECTION 8: Coding Practice Bank (Easy → Medium → Hard)
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {practiceQuestions.map((q, idx) => (
                <div 
                  key={idx}
                  style={{
                    padding: '1rem 1.25rem',
                    backgroundColor: '#0f172a',
                    borderRadius: '10px',
                    border: '1px solid #1e293b',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    gap: '1rem'
                  }}
                >
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.35rem' }}>
                      <span style={{
                        fontSize: '0.7rem',
                        padding: '2px 8px',
                        borderRadius: '4px',
                        fontWeight: 700,
                        backgroundColor: q.difficulty === 'Basic' || q.difficulty === 'Beginner' ? 'rgba(16, 185, 129, 0.15)' :
                                         q.difficulty === 'Intermediate' ? 'rgba(245, 158, 11, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                        color: q.difficulty === 'Basic' || q.difficulty === 'Beginner' ? '#10b981' :
                               q.difficulty === 'Intermediate' ? '#f59e0b' : '#ef4444'
                      }}>
                        {q.difficulty}
                      </span>
                      <span style={{ fontSize: '0.92rem', fontWeight: 700, color: '#f8fafc' }}>
                        {q.title}
                      </span>
                    </div>
                    <p style={{ fontSize: '0.84rem', color: '#94a3b8', margin: 0, lineHeight: 1.5 }}>
                      {q.description}
                    </p>
                  </div>

                  <button
                    onClick={() => onNavigate && onNavigate('practice', { problem: selectedLesson.practice_problem_slug || 'two-sum', language: 'java' })}
                    className="btn-glass"
                    style={{ padding: '0.4rem 0.85rem', fontSize: '0.78rem', whiteSpace: 'nowrap', display: 'flex', alignItems: 'center', gap: '4px' }}
                  >
                    <span>Solve Challenge</span>
                    <ArrowRight size={13} />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Section 9: 3-Level AI Hints */}
          <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.5rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <HelpCircle size={16} style={{ color: '#c084fc' }} />
              SECTION 9: 3-Level Progressive AI Hints
            </h3>
            <p style={{ fontSize: '0.8rem', color: '#94a3b8', marginBottom: '1rem' }}>
              Solve without spoiling: reveal Level 1 for conceptual direction, Level 2 for invariant strategies, and Level 3 for pseudocode.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {aiHints.map((h) => {
                const isRevealed = revealedHints[h.level];
                return (
                  <div 
                    key={h.level}
                    style={{
                      backgroundColor: '#0f172a',
                      borderRadius: '10px',
                      border: isRevealed ? '1px solid #c084fc' : '1px solid #1e293b',
                      overflow: 'hidden'
                    }}
                  >
                    <button
                      onClick={() => toggleHint(h.level)}
                      style={{
                        width: '100%',
                        padding: '0.75rem 1rem',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        backgroundColor: 'transparent',
                        border: 'none',
                        color: '#f8fafc',
                        fontSize: '0.86rem',
                        fontWeight: 700,
                        cursor: 'pointer'
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <span style={{
                          fontSize: '0.68rem',
                          padding: '2px 6px',
                          borderRadius: '4px',
                          backgroundColor: 'rgba(192, 132, 252, 0.2)',
                          color: '#c084fc',
                          fontWeight: 800
                        }}>
                          LEVEL {h.level}
                        </span>
                        <span>{h.title}</span>
                      </div>
                      <span style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)' }}>
                        {isRevealed ? 'Hide Hint' : 'Reveal Hint'}
                      </span>
                    </button>

                    {isRevealed && (
                      <div style={{ padding: '0.75rem 1rem 1rem 1rem', borderTop: '1px solid #1e293b', fontSize: '0.86rem', color: '#cbd5e1', lineHeight: 1.6, backgroundColor: 'rgba(192, 132, 252, 0.05)' }}>
                        {h.hint}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* SECTION 11: MASTERY ASSESSMENT */}
      {activeLessonTab === 'quiz' && (
        <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
            <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', display: 'flex', alignItems: 'center', gap: '8px', margin: 0 }}>
              <Award size={18} style={{ color: '#10b981' }} />
              SECTION 11: Mastery Assessment & Concept Checkpoint
            </h3>
            <span style={{ fontSize: '0.75rem', color: '#94a3b8' }}>
              Threshold: {selectedLesson.mastery_threshold || 70}% to achieve Mastered status
            </span>
          </div>

          {quizResult && (
            <div style={{
              padding: '1rem',
              borderRadius: '10px',
              backgroundColor: quizResult.is_passed ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
              border: `1px solid ${quizResult.is_passed ? '#10b981' : '#ef4444'}`,
              marginBottom: '1.25rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.35rem' }}>
                {quizResult.is_passed ? (
                  <CheckCircle size={18} style={{ color: '#10b981' }} />
                ) : (
                  <AlertTriangle size={18} style={{ color: '#ef4444' }} />
                )}
                <span style={{ fontWeight: 800, fontSize: '0.95rem', color: '#f8fafc' }}>
                  Score: {quizResult.score_percent}% ({quizResult.correct_count}/{quizResult.total_questions} Correct)
                </span>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#cbd5e1', margin: 0 }}>
                {quizResult.feedback}
              </p>
              {quizResult.unlocked_next_lesson_id && (
                <button
                  onClick={() => openLesson(quizResult.unlocked_next_lesson_id)}
                  className="btn-gradient"
                  style={{ marginTop: '0.75rem', padding: '0.4rem 0.85rem', fontSize: '0.78rem', display: 'flex', alignItems: 'center', gap: '6px' }}
                >
                  <span>Advance to Next Concept</span>
                  <ArrowRight size={14} />
                </button>
              )}
            </div>
          )}

          {/* Quiz Questions */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            {quizQuestions.map((q, qIdx) => (
              <div 
                key={q.id || qIdx}
                style={{
                  padding: '1.25rem',
                  backgroundColor: '#0f172a',
                  borderRadius: '10px',
                  border: '1px solid #1e293b'
                }}
              >
                <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.75rem' }}>
                  Question {qIdx + 1}: {q.question}
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                  {q.options && q.options.map((opt, optIdx) => {
                    const isChosen = quizAnswers[String(qIdx)] === optIdx;
                    return (
                      <label
                        key={optIdx}
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          gap: '10px',
                          padding: '0.55rem 0.85rem',
                          borderRadius: '8px',
                          backgroundColor: isChosen ? 'rgba(56, 189, 248, 0.12)' : '#0b1120',
                          border: isChosen ? '1px solid var(--accent-cyan)' : '1px solid transparent',
                          cursor: 'pointer',
                          fontSize: '0.84rem',
                          color: isChosen ? '#f8fafc' : '#94a3b8'
                        }}
                      >
                        <input
                          type="radio"
                          name={`quiz_${qIdx}`}
                          checked={isChosen}
                          onChange={() => setQuizAnswers(prev => ({ ...prev, [String(qIdx)]: optIdx }))}
                          style={{ accentColor: 'var(--accent-cyan)' }}
                        />
                        <span>{opt}</span>
                      </label>
                    );
                  })}
                </div>
              </div>
            ))}

            <button
              onClick={handleQuizSubmit}
              disabled={submittingQuiz || quizQuestions.length === 0}
              className="btn-gradient"
              style={{
                padding: '0.65rem 1.4rem',
                fontSize: '0.88rem',
                fontWeight: 700,
                alignSelf: 'flex-start',
                display: 'flex',
                alignItems: 'center',
                gap: '8px'
              }}
            >
              <Award size={16} />
              <span>{submittingQuiz ? 'Grading Assessment...' : 'Submit & Check Mastery'}</span>
            </button>
          </div>
        </div>
      )}

      {/* SECTION 10: CONCEPT CONNECTIONS */}
      {activeLessonTab === 'connections' && (
        <div style={{ padding: '1.5rem', borderRadius: '14px', backgroundColor: '#0B1120', border: '1px solid #1E293B' }}>
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#f8fafc', marginBottom: '0.75rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Compass size={18} style={{ color: 'var(--accent-cyan)' }} />
            SECTION 10: Interconnected Concept Graph
          </h3>
          <p style={{ fontSize: '0.84rem', color: '#94a3b8', marginBottom: '1.25rem' }}>
            DSA is not a collection of disconnected tricks. See how this concept connects to prerequisite foundations and advanced applications:
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
            {/* Prerequisite Node */}
            <div style={{ padding: '1rem', backgroundColor: '#0f172a', borderRadius: '10px', border: '1px solid #1e293b' }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#c084fc', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                Prerequisite Foundation
              </div>
              <div style={{ fontSize: '0.86rem', color: '#cbd5e1' }}>
                {selectedLesson.prerequisites || 'Basic Programming Logic'}
              </div>
            </div>

            {/* Current Node */}
            <div style={{ padding: '1rem', backgroundColor: 'rgba(56, 189, 248, 0.08)', borderRadius: '10px', border: '1px solid var(--accent-cyan)' }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 800, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                Current Concept
              </div>
              <div style={{ fontSize: '0.92rem', fontWeight: 700, color: '#f8fafc' }}>
                {selectedLesson.title}
              </div>
            </div>

            {/* Next Step Node */}
            <div style={{ padding: '1rem', backgroundColor: '#0f172a', borderRadius: '10px', border: '1px solid #1e293b' }}>
              <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#10b981', textTransform: 'uppercase', marginBottom: '0.35rem' }}>
                Next Connected Master Topic
              </div>
              <div style={{ fontSize: '0.86rem', color: '#cbd5e1', marginBottom: '0.5rem' }}>
                {selectedLesson.next_lesson_title || 'Advanced Algorithmic Patterns'}
              </div>
              {selectedLesson.next_lesson_id && (
                <button
                  onClick={() => openLesson(selectedLesson.next_lesson_id)}
                  className="btn-glass"
                  style={{ padding: '2px 8px', fontSize: '0.72rem', display: 'flex', alignItems: 'center', gap: '4px', color: '#10b981' }}
                >
                  <span>Go to Concept</span>
                  <ArrowRight size={12} />
                </button>
              )}
            </div>
          </div>
        </div>
      )}

    </div>
  );
}
