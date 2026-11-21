import React, { useState, useEffect, useRef } from 'react';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  ChevronRight, 
  ChevronLeft, 
  Sliders, 
  Sparkles,
  Layers, 
  Search, 
  GitFork, 
  Activity, 
  Maximize2,
  BookOpen,
  HelpCircle,
  CheckCircle2,
  Clock,
  ArrowRight,
  Code2,
  Cpu,
  Zap,
  Target,
  Award,
  AlertCircle
} from 'lucide-react';
import { api } from '../services/api';

// ==============================================================
// ALGORITHMS DIRECTORY ACROSS ALL DSA CATEGORIES
// ==============================================================
const ALGORITHMS_CATALOG = [
  // 1. Arrays & Strings
  {
    id: 'array_traversal',
    name: 'Array Contiguity & Traversal',
    category: 'Arrays',
    complexityTime: 'O(N)',
    complexitySpace: 'O(1)',
    whatIsIt: 'An array stores elements at contiguous (adjacent) physical memory addresses in RAM.',
    whyNeedIt: 'Contiguity gives CPUs lightning-fast O(1) random access via arithmetic offset math: address = base + index * size.',
    whereUsed: 'Database buffer pools, CPU memory caches, image pixel buffers, lookup tables.'
  },
  {
    id: 'binary_search',
    name: 'Binary Search (Halving Range)',
    category: 'Searching',
    complexityTime: 'O(log N)',
    complexitySpace: 'O(1)',
    whatIsIt: 'An efficient search algorithm that finds target items in a sorted collection by repeatedly dividing the search interval in half.',
    whyNeedIt: 'Searching 1 billion items with Linear Search takes ~1,000,000,000 checks. Binary Search takes only 30 checks!',
    whereUsed: 'Git bisect, database B-Tree index lookups, dictionary lookups, router IP routing tables.'
  },
  {
    id: 'bubble_sort',
    name: 'Bubble Sort (Step Comparisons & Swaps)',
    category: 'Sorting',
    complexityTime: 'O(N²)',
    complexitySpace: 'O(1)',
    whatIsIt: 'A foundational sorting algorithm that compares adjacent pairs and swaps them if out of order, floating large items to the end.',
    whyNeedIt: 'Perfect for learning algorithm invariants: after each pass k, the k-th largest element is guaranteed to be in its final position.',
    whereUsed: 'Educational foundations, small nearly-sorted datasets, graphics polygon raster sorting.'
  },
  {
    id: 'linked_list',
    name: 'Singly Linked List (Pointers & Nodes)',
    category: 'Linked Lists',
    complexityTime: 'O(N)',
    complexitySpace: 'O(N)',
    whatIsIt: 'A linear data structure where elements (nodes) are stored arbitrarily in heap memory, connected by forward pointer references.',
    whyNeedIt: 'Unlike arrays, linked lists can grow dynamically without allocating huge contiguous memory chunks or costly reallocations.',
    whereUsed: 'Operating system free memory blocks, LRU cache doubly-linked lists, undo/redo buffers.'
  },
  {
    id: 'stack_lifo',
    name: 'Stack (LIFO: Push, Pop & Peek)',
    category: 'Stacks & Queues',
    complexityTime: 'O(1)',
    complexitySpace: 'O(N)',
    whatIsIt: 'A Last-In, First-Out (LIFO) collection where insertions and removals occur exclusively at one end called the TOP.',
    whyNeedIt: 'Maintains state history so previous operations can be reversed in exact reverse chronological order.',
    whereUsed: 'JVM method call stack, browser back button history, syntax parser parentheses matching.'
  },
  {
    id: 'queue_fifo',
    name: 'Queue (FIFO: Front & Rear Pointers)',
    category: 'Stacks & Queues',
    complexityTime: 'O(1)',
    complexitySpace: 'O(N)',
    whatIsIt: 'A First-In, First-Out (FIFO) collection where elements enter at the REAR and leave from the FRONT.',
    whyNeedIt: 'Guarantees fairness: the first request received is always the first request processed without starvation.',
    whereUsed: 'Web server request queues, printer task buffers, Breadth-First Search (BFS) graph traversal.'
  },
  {
    id: 'tree_traversal',
    name: 'Binary Tree In-Order Traversal',
    category: 'Trees',
    complexityTime: 'O(N)',
    complexitySpace: 'O(H)',
    whatIsIt: 'A recursive tree traversal visiting nodes in the strict order: Left Subtree → Current Root → Right Subtree.',
    whyNeedIt: 'On a Binary Search Tree (BST), in-order traversal produces values in perfectly sorted non-decreasing order!',
    whereUsed: 'Expression syntax tree evaluation, database query planners, hierarchical file systems.'
  },
  {
    id: 'graph_bfs',
    name: 'Graph Breadth-First Search (BFS)',
    category: 'Graphs',
    complexityTime: 'O(V + E)',
    complexitySpace: 'O(V)',
    whatIsIt: 'A traversal that explores all immediate neighboring vertices at the present depth before moving to vertices at the next depth level.',
    whyNeedIt: 'Guarantees finding the shortest path (minimum edge count) between two vertices in unweighted graphs.',
    whereUsed: 'GPS navigation shortest routes, social network friend recommendations (Degrees of separation), web crawlers.'
  },
  {
    id: 'recursion_callstack',
    name: 'Recursion & Visual Call Stack',
    category: 'Recursion',
    complexityTime: 'O(N)',
    complexitySpace: 'O(N)',
    whatIsIt: 'A method where a function solves a problem by calling smaller instances of itself until reaching a base termination case.',
    whyNeedIt: 'Enables elegant divide-and-conquer solutions for tree traversals, sorting, and state space exploration.',
    whereUsed: 'Compilers, JSON serialization, merge sort, backtracking puzzles.'
  },
  {
    id: 'dp_fibonacci',
    name: 'Dynamic Programming (Tabulation Table)',
    category: 'Dynamic Programming',
    complexityTime: 'O(N)',
    complexitySpace: 'O(N)',
    whatIsIt: 'An optimization technique solving complex problems by breaking them down into simpler subproblems and storing results in a table.',
    whyNeedIt: 'Reduces catastrophic exponential O(2ⁿ) runtime down to fast linear O(N) by eliminating duplicate sub-tree work.',
    whereUsed: 'Bioinformatics DNA alignment, financial portfolio optimization, shortest path algorithms (Bellman-Ford).'
  }
];

// Speed definitions in ms per step
const SPEED_MODES = [
  { label: 'Very Slow', ms: 3500, desc: 'Paced for deep contemplation' },
  { label: 'Slow (Teacher)', ms: 2000, desc: 'Patient teacher default' },
  { label: 'Normal', ms: 1000, desc: 'Standard animation' },
  { label: 'Fast', ms: 400, desc: 'Quick overview' }
];

export default function VisualizerPage({ initialAlgorithm, onNavigate }) {
  const [selectedAlgoId, setSelectedAlgoId] = useState(initialAlgorithm || 'binary_search');
  const [selectedSpeedIndex, setSelectedSpeedIndex] = useState(1); // Default: Slow (Teacher) - 2000ms
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentStepIdx, setCurrentStepIdx] = useState(0);
  const [autoPauseOnKey, setAutoPauseOnKey] = useState(true);
  const [codeLang, setCodeLang] = useState('java'); // 'java' (default) or 'python'
  const [studentAnswer, setStudentAnswer] = useState(null);
  const [showAnswerFeedback, setShowAnswerFeedback] = useState(false);

  const currentAlgo = ALGORITHMS_CATALOG.find(a => a.id === selectedAlgoId) || ALGORITHMS_CATALOG[1];
  const speedObj = SPEED_MODES[selectedSpeedIndex];

  // Update selected algorithm when prop changes
  useEffect(() => {
    if (initialAlgorithm && ALGORITHMS_CATALOG.some(a => a.id === initialAlgorithm)) {
      setSelectedAlgoId(initialAlgorithm);
    }
  }, [initialAlgorithm]);

  // Steps generator
  const steps = getTeachingSteps(selectedAlgoId);
  const currentStep = steps[currentStepIdx] || steps[0];

  // Reset step whenever algorithm changes
  useEffect(() => {
    setCurrentStepIdx(0);
    setIsPlaying(false);
    setStudentAnswer(null);
    setShowAnswerFeedback(false);
  }, [selectedAlgoId]);

  // Animation Loop with Auto-Pause on Key Operations
  useEffect(() => {
    let timer = null;
    if (isPlaying) {
      timer = setInterval(() => {
        setCurrentStepIdx(prev => {
          const nextIdx = prev + 1;
          if (nextIdx >= steps.length) {
            setIsPlaying(false);
            try {
              api.logActivity('visualization_run', currentAlgo.name, { completed: true });
            } catch (e) {}
            return prev;
          }
          // If auto-pause is enabled and this is an important operation checkpoint
          if (autoPauseOnKey && steps[nextIdx]?.isKeyOperation) {
            setIsPlaying(false);
          }
          return nextIdx;
        });
      }, speedObj.ms);
    }
    return () => clearInterval(timer);
  }, [isPlaying, steps, speedObj.ms, autoPauseOnKey]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', paddingBottom: '3rem' }}>
      
      {/* ============================================================== */}
      {/* 1. TEACHER MODE HERO BAR & CONTROLS */}
      {/* ============================================================== */}
      <div style={{
        padding: '1.25rem 1.75rem',
        borderRadius: '16px',
        backgroundColor: '#FFFFFF',
        border: '1px solid #E2E8F0',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
        display: 'flex',
        flexDirection: 'column',
        gap: '1rem'
      }}>
        {/* Top line: Teacher Mode Header + Algorithm Selector Dropdown */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.25rem' }}>
              <span style={{
                fontSize: '0.72rem',
                fontWeight: 800,
                color: '#4F46E5',
                backgroundColor: '#EDE9FE',
                padding: '3px 10px',
                borderRadius: '999px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px'
              }}>
                <span>🎓</span>
                <span>Patient CS Teacher Mode</span>
              </span>
              <span style={{ fontSize: '0.75rem', color: '#10B981', fontWeight: 700 }}>
                • Step-by-Step Interactive Learning
              </span>
            </div>

            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#1E1B4B', margin: 0 }}>
              {currentAlgo.name}
            </h1>
          </div>

          {/* Algorithm Category Picker Dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#64748B' }}>Topic:</span>
            <select
              value={selectedAlgoId}
              onChange={(e) => setSelectedAlgoId(e.target.value)}
              style={{
                padding: '0.55rem 1rem',
                borderRadius: '10px',
                border: '1px solid #CBD5E1',
                backgroundColor: '#F8FAFC',
                color: '#1E1B4B',
                fontSize: '0.86rem',
                fontWeight: 700,
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {ALGORITHMS_CATALOG.map(a => (
                <option key={a.id} value={a.id}>
                  [{a.category}] {a.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Bottom line: Playback Controls & Speed Selector */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
          paddingTop: '0.75rem',
          borderTop: '1px solid #F1F5F9'
        }}>
          {/* Controls: Prev, Play/Pause, Next, Restart */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            {/* Play/Pause Button */}
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              style={{
                padding: '0.5rem 1.25rem',
                borderRadius: '10px',
                border: 'none',
                backgroundColor: isPlaying ? '#EF4444' : '#4F46E5',
                color: '#FFFFFF',
                fontSize: '0.84rem',
                fontWeight: 700,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
                boxShadow: isPlaying ? '0 2px 8px rgba(239, 68, 68, 0.3)' : '0 2px 8px rgba(79, 70, 229, 0.35)',
                transition: 'all 0.15s ease'
              }}
            >
              {isPlaying ? <Pause size={15} /> : <Play size={15} />}
              <span>{isPlaying ? 'Pause' : 'Play Teaching'}</span>
            </button>

            {/* Prev Step */}
            <button
              onClick={() => {
                setIsPlaying(false);
                setCurrentStepIdx(Math.max(0, currentStepIdx - 1));
              }}
              disabled={currentStepIdx === 0}
              style={{
                padding: '0.5rem 0.85rem',
                borderRadius: '10px',
                border: '1px solid #E2E8F0',
                backgroundColor: currentStepIdx === 0 ? '#F8FAFC' : '#FFFFFF',
                color: currentStepIdx === 0 ? '#CBD5E1' : '#475569',
                fontSize: '0.84rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                cursor: currentStepIdx === 0 ? 'not-allowed' : 'pointer'
              }}
              title="Step backward"
            >
              <ChevronLeft size={16} />
              <span>Previous</span>
            </button>

            {/* Next Step */}
            <button
              onClick={() => {
                setIsPlaying(false);
                const next = Math.min(steps.length - 1, currentStepIdx + 1);
                setCurrentStepIdx(next);
                if (next === steps.length - 1) {
                  try {
                    api.logActivity('visualization_run', currentAlgo.name, { completed: true });
                  } catch (e) {}
                }
              }}
              disabled={currentStepIdx >= steps.length - 1}
              style={{
                padding: '0.5rem 0.85rem',
                borderRadius: '10px',
                border: '1px solid #E2E8F0',
                backgroundColor: currentStepIdx >= steps.length - 1 ? '#F8FAFC' : '#FFFFFF',
                color: currentStepIdx >= steps.length - 1 ? '#CBD5E1' : '#475569',
                fontSize: '0.84rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                cursor: currentStepIdx >= steps.length - 1 ? 'not-allowed' : 'pointer'
              }}
              title="Advance single step"
            >
              <span>Next Step</span>
              <ChevronRight size={16} />
            </button>

            {/* Restart */}
            <button
              onClick={() => {
                setIsPlaying(false);
                setCurrentStepIdx(0);
                setStudentAnswer(null);
                setShowAnswerFeedback(false);
              }}
              style={{
                padding: '0.5rem 0.75rem',
                borderRadius: '10px',
                border: '1px solid #E2E8F0',
                backgroundColor: '#FFFFFF',
                color: '#64748B',
                cursor: 'pointer'
              }}
              title="Restart from beginning"
            >
              <RotateCcw size={15} />
            </button>
          </div>

          {/* Speed Presets & Auto-pause Checkbox */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
            {/* Auto-pause Checkbox */}
            <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', color: '#475569', fontWeight: 600, cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={autoPauseOnKey}
                onChange={(e) => setAutoPauseOnKey(e.target.checked)}
                style={{ accentColor: '#4F46E5', cursor: 'pointer' }}
              />
              <span>Pause on Important Decision</span>
            </label>

            {/* Speed Pills */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ fontSize: '0.74rem', color: '#64748B', fontWeight: 600, marginRight: '4px' }}>Speed:</span>
              <div style={{
                display: 'flex',
                padding: '3px',
                borderRadius: '999px',
                backgroundColor: '#F1F5F9',
                border: '1px solid #E2E8F0'
              }}>
                {SPEED_MODES.map((mode, i) => (
                  <button
                    key={mode.label}
                    onClick={() => setSelectedSpeedIndex(i)}
                    style={{
                      padding: '0.25rem 0.65rem',
                      borderRadius: '999px',
                      border: 'none',
                      backgroundColor: selectedSpeedIndex === i ? '#4F46E5' : 'transparent',
                      color: selectedSpeedIndex === i ? '#FFFFFF' : '#64748B',
                      fontSize: '0.74rem',
                      fontWeight: selectedSpeedIndex === i ? 700 : 500,
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                    title={mode.desc}
                  >
                    {mode.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Step Counter */}
            <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#1E1B4B' }}>
              Step <span style={{ color: '#4F46E5' }}>{currentStepIdx + 1}</span> of {steps.length}
            </div>
          </div>
        </div>
      </div>

      {/* ============================================================== */}
      {/* 2. THE MAIN VISUAL TEACHING STAGE & CODE SYNCHRONIZATION */}
      {/* ============================================================== */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.25fr 0.95fr', gap: '1.25rem' }}>
        
        {/* Left Column: Visual Canvas & Patient Teacher Callout */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* Main Visual Stage Box */}
          <div style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '18px',
            border: '1px solid #E2E8F0',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
            padding: '1.5rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            minHeight: '380px'
          }}>
            {/* Stage Title and Status Tag */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 800, color: '#1E1B4B', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                {currentStep.stageTitle || 'Execution Stage'}
              </div>

              {currentStep.isKeyOperation && (
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 800,
                  color: '#D97706',
                  backgroundColor: '#FEF3C7',
                  padding: '2px 8px',
                  borderRadius: '6px',
                  border: '1px solid #FDE68A'
                }}>
                  ⚠️ Key Algorithmic Decision
                </span>
              )}
            </div>

            {/* Custom Interactive Stage Renderer based on Category */}
            <div style={{
              flex: 1,
              backgroundColor: '#0B1120',
              borderRadius: '14px',
              border: '1px solid #1E293B',
              padding: '2rem 1.5rem',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative',
              overflow: 'hidden'
            }}>
              {renderVisualStructure(selectedAlgoId, currentStep)}
            </div>

            {/* Before / After State Footnote */}
            {currentStep.stateChangeNote && (
              <div style={{
                padding: '0.65rem 0.95rem',
                borderRadius: '10px',
                backgroundColor: '#F8FAFC',
                border: '1px solid #E2E8F0',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.78rem',
                color: '#475569'
              }}>
                <span style={{ fontWeight: 700, color: '#4F46E5' }}>State Transition:</span>
                <span>{currentStep.stateChangeNote}</span>
              </div>
            )}
          </div>

          {/* Teacher Explanation Callout ("Why did this happen?") */}
          <div style={{
            padding: '1.35rem 1.5rem',
            borderRadius: '16px',
            backgroundColor: '#FFFFFF',
            border: '1.5px solid #EDE9FE',
            boxShadow: '0 4px 12px rgba(79, 70, 229, 0.05)',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                backgroundColor: '#EDE9FE',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: '#4F46E5',
                fontSize: '1.1rem'
              }}>
                👨‍🏫
              </div>
              <div>
                <h4 style={{ margin: 0, fontSize: '0.98rem', fontWeight: 800, color: '#1E1B4B' }}>
                  Patient Teacher's Explanation
                </h4>
                <div style={{ fontSize: '0.72rem', color: '#64748B' }}>
                  Step {currentStepIdx + 1} • {currentStep.phaseName || 'Step Invariant'}
                </div>
              </div>
            </div>

            {/* Simple English Explanation */}
            <p style={{
              fontSize: '0.9rem',
              color: '#334155',
              lineHeight: 1.6,
              margin: 0,
              fontWeight: 500
            }}>
              {currentStep.teacherExplanation}
            </p>

            {/* "Why did this happen?" callout */}
            {currentStep.whyDidThisHappen && (
              <div style={{
                marginTop: '0.35rem',
                padding: '0.85rem 1rem',
                borderRadius: '12px',
                backgroundColor: '#F5F3FF',
                border: '1px solid #DDD6FE'
              }}>
                <div style={{ fontSize: '0.78rem', fontWeight: 800, color: '#6D28D9', marginBottom: '3px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <HelpCircle size={14} />
                  <span>Why did this happen?</span>
                </div>
                <div style={{ fontSize: '0.84rem', color: '#4C1D95', lineHeight: 1.5 }}>
                  {currentStep.whyDidThisHappen}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Code Synchronization, Variable Watcher & Interactive Try-It */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* Synchronized Code Implementation View (Java & Python) */}
          <div style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '18px',
            border: '1px solid #E2E8F0',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
            padding: '1.25rem 1.4rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}>
            {/* Header: Code Synchronizer + Language Toggle */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Code2 size={17} style={{ color: '#4F46E5' }} />
                <h4 style={{ margin: 0, fontSize: '0.92rem', fontWeight: 800, color: '#1E1B4B' }}>
                  Synchronized Code
                </h4>
              </div>

              {/* Language Pills: Java (Primary) vs Python */}
              <div style={{ display: 'flex', gap: '4px', backgroundColor: '#F1F5F9', padding: '2px', borderRadius: '8px' }}>
                <button
                  onClick={() => setCodeLang('java')}
                  style={{
                    padding: '0.2rem 0.65rem',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: codeLang === 'java' ? '#4F46E5' : 'transparent',
                    color: codeLang === 'java' ? '#FFFFFF' : '#64748B',
                    fontSize: '0.74rem',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  ☕ Java (Primary)
                </button>
                <button
                  onClick={() => setCodeLang('python')}
                  style={{
                    padding: '0.2rem 0.65rem',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: codeLang === 'python' ? '#4F46E5' : 'transparent',
                    color: codeLang === 'python' ? '#FFFFFF' : '#64748B',
                    fontSize: '0.74rem',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  🐍 Python
                </button>
              </div>
            </div>

            {/* Line-by-Line Code Viewer with Active Line Highlight */}
            <div style={{
              backgroundColor: '#0B1120',
              borderRadius: '12px',
              border: '1px solid #1E293B',
              padding: '0.85rem',
              fontFamily: 'Consolas, Monaco, "Courier New", monospace',
              fontSize: '0.8rem',
              lineHeight: 1.6,
              overflowX: 'auto',
              maxHeight: '230px',
              color: '#94A3B8'
            }}>
              {getCodeLines(selectedAlgoId, codeLang).map((line, idx) => {
                const lineNum = idx + 1;
                const isCurrentLine = currentStep.activeCodeLine === lineNum;
                return (
                  <div
                    key={lineNum}
                    style={{
                      display: 'flex',
                      padding: '2px 6px',
                      borderRadius: '4px',
                      backgroundColor: isCurrentLine ? 'rgba(79, 70, 229, 0.35)' : 'transparent',
                      borderLeft: isCurrentLine ? '3px solid #6366F1' : '3px solid transparent',
                      color: isCurrentLine ? '#F8FAFC' : '#94A3B8',
                      fontWeight: isCurrentLine ? 700 : 400
                    }}
                  >
                    <span style={{ width: '28px', color: '#475569', userSelect: 'none' }}>{lineNum}</span>
                    <span style={{ whiteSpace: 'pre' }}>{line}</span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Live Variable Watcher Grid */}
          <div style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '18px',
            border: '1px solid #E2E8F0',
            boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
            padding: '1.25rem 1.4rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '0.75rem' }}>
              <Cpu size={16} style={{ color: '#10B981' }} />
              <h4 style={{ margin: 0, fontSize: '0.92rem', fontWeight: 800, color: '#1E1B4B' }}>
                Live Variable Watcher
              </h4>
            </div>

            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(130px, 1fr))',
              gap: '0.65rem'
            }}>
              {Object.entries(currentStep.variables || {}).map(([key, val]) => (
                <div
                  key={key}
                  style={{
                    padding: '0.55rem 0.75rem',
                    borderRadius: '10px',
                    backgroundColor: '#F8FAFC',
                    border: '1px solid #E2E8F0',
                    display: 'flex',
                    flexDirection: 'column'
                  }}
                >
                  <span style={{ fontSize: '0.68rem', fontWeight: 700, color: '#64748B', textTransform: 'uppercase' }}>
                    {key}
                  </span>
                  <span style={{ fontSize: '0.95rem', fontWeight: 800, color: '#1E1B4B', marginTop: '2px', wordBreak: 'break-all' }}>
                    {String(val)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Interactive "Try It Yourself" Prediction Challenge */}
          {currentStep.interactiveTask && (
            <div style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '18px',
              border: '1.5px solid #FDE68A',
              boxShadow: '0 4px 14px rgba(245, 158, 11, 0.08)',
              padding: '1.25rem 1.4rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Target size={17} style={{ color: '#D97706' }} />
                <h4 style={{ margin: 0, fontSize: '0.92rem', fontWeight: 800, color: '#92400E' }}>
                  Try It Yourself: Test Your Understanding
                </h4>
              </div>

              <p style={{ fontSize: '0.84rem', color: '#78350F', margin: 0, fontWeight: 600 }}>
                {currentStep.interactiveTask.question}
              </p>

              {/* Options */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {currentStep.interactiveTask.options.map((opt, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setStudentAnswer(idx);
                      setShowAnswerFeedback(true);
                      try {
                        const isCorrect = idx === currentStep.interactiveTask.correctIdx;
                        api.logActivity('quiz_completed', currentAlgo.name, { score: isCorrect ? 100 : 0 });
                      } catch (e) {}
                    }}
                    style={{
                      padding: '0.55rem 0.85rem',
                      borderRadius: '8px',
                      border: studentAnswer === idx 
                        ? (idx === currentStep.interactiveTask.correctIdx ? '1.5px solid #10B981' : '1.5px solid #EF4444')
                        : '1px solid #E2E8F0',
                      backgroundColor: studentAnswer === idx
                        ? (idx === currentStep.interactiveTask.correctIdx ? '#DCFCE7' : '#FEE2E2')
                        : '#F8FAFC',
                      color: '#1E1B4B',
                      fontSize: '0.8rem',
                      fontWeight: 600,
                      textAlign: 'left',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease'
                    }}
                  >
                    {opt}
                  </button>
                ))}
              </div>

              {/* Feedback */}
              {showAnswerFeedback && (
                <div style={{
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  backgroundColor: studentAnswer === currentStep.interactiveTask.correctIdx ? '#DCFCE7' : '#FEE2E2',
                  border: studentAnswer === currentStep.interactiveTask.correctIdx ? '1px solid #86EFAC' : '1px solid #FCA5A5',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  color: studentAnswer === currentStep.interactiveTask.correctIdx ? '#166534' : '#991B1B'
                }}>
                  {studentAnswer === currentStep.interactiveTask.correctIdx 
                    ? `✓ Correct! ${currentStep.interactiveTask.explanation}`
                    : `✕ Not quite! ${currentStep.interactiveTask.explanation}`
                  }
                </div>
              )}
            </div>
          )}

        </div>
      </div>

      {/* ============================================================== */}
      {/* 3. 10-PART TEACHING SEQUENCE REFERENCE BAR */}
      {/* ============================================================== */}
      <div style={{
        backgroundColor: '#FFFFFF',
        borderRadius: '16px',
        padding: '1.25rem 1.5rem',
        border: '1px solid #E2E8F0',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '1.25rem'
      }}>
        {/* 1. What is this? */}
        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#4F46E5', textTransform: 'uppercase', marginBottom: '4px' }}>
            1. What is this concept?
          </div>
          <div style={{ fontSize: '0.84rem', color: '#475569', lineHeight: 1.5 }}>
            {currentAlgo.whatIsIt}
          </div>
        </div>

        {/* 2. Why do we need it? */}
        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#10B981', textTransform: 'uppercase', marginBottom: '4px' }}>
            2. Why do we need it?
          </div>
          <div style={{ fontSize: '0.84rem', color: '#475569', lineHeight: 1.5 }}>
            {currentAlgo.whyNeedIt}
          </div>
        </div>

        {/* 3. Where is it used? */}
        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#D97706', textTransform: 'uppercase', marginBottom: '4px' }}>
            3. Real-World Applications
          </div>
          <div style={{ fontSize: '0.84rem', color: '#475569', lineHeight: 1.5 }}>
            {currentAlgo.whereUsed}
          </div>
        </div>

        {/* 4. Complexity */}
        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#7C3AED', textTransform: 'uppercase', marginBottom: '4px' }}>
            4. Asymptotic Complexity
          </div>
          <div style={{ fontSize: '0.84rem', color: '#1E1B4B', fontWeight: 700, marginTop: '2px' }}>
            Time: <span style={{ color: '#4F46E5' }}>{currentAlgo.complexityTime}</span> • Space: <span style={{ color: '#10B981' }}>{currentAlgo.complexitySpace}</span>
          </div>
        </div>
      </div>

    </div>
  );
}

// ==============================================================
// CUSTOM VISUAL RENDERING ENGINES FOR EACH DATA STRUCTURE
// ==============================================================
function renderVisualStructure(algoId, step) {
  // 1. Binary Search
  if (algoId === 'binary_search') {
    const { array, low, high, mid, target, found } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2rem', width: '100%' }}>
        {/* Pointer Indicators Above Array */}
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {array?.map((val, idx) => {
            const isMid = mid === idx;
            const isLow = low === idx;
            const isHigh = high === idx;
            const isTargetMatch = found && isMid;
            const isEliminated = idx < low || idx > high;

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                {/* Pointer Label */}
                <div style={{ height: '22px', fontSize: '0.7rem', fontWeight: 800, display: 'flex', alignItems: 'center' }}>
                  {isMid && <span style={{ color: '#38BDF8', backgroundColor: 'rgba(56, 189, 248, 0.2)', padding: '1px 6px', borderRadius: '4px' }}>MID</span>}
                  {!isMid && isLow && <span style={{ color: '#10B981', backgroundColor: 'rgba(16, 185, 129, 0.2)', padding: '1px 6px', borderRadius: '4px' }}>LOW</span>}
                  {!isMid && isHigh && <span style={{ color: '#F59E0B', backgroundColor: 'rgba(245, 158, 11, 0.2)', padding: '1px 6px', borderRadius: '4px' }}>HIGH</span>}
                </div>

                {/* Arrow down pointer */}
                <div style={{ height: '14px', color: isMid ? '#38BDF8' : isLow ? '#10B981' : isHigh ? '#F59E0B' : 'transparent' }}>
                  {(isMid || isLow || isHigh) && '↓'}
                </div>

                {/* Box */}
                <div style={{
                  width: '46px',
                  height: '46px',
                  borderRadius: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '1rem',
                  backgroundColor: isTargetMatch 
                    ? '#10B981' 
                    : isMid 
                    ? 'rgba(56, 189, 248, 0.25)' 
                    : isEliminated 
                    ? 'rgba(15, 23, 42, 0.6)' 
                    : '#1E293B',
                  border: isTargetMatch 
                    ? '2.5px solid #10B981' 
                    : isMid 
                    ? '2.5px solid #38BDF8' 
                    : isEliminated 
                    ? '1px dashed #334155' 
                    : '1.5px solid #475569',
                  color: isEliminated ? '#475569' : '#F8FAFC',
                  opacity: isEliminated ? 0.35 : 1,
                  boxShadow: isMid ? '0 0 20px rgba(56, 189, 248, 0.4)' : isTargetMatch ? '0 0 20px rgba(16, 185, 129, 0.5)' : 'none',
                  transition: 'all 0.3s ease'
                }}>
                  {val}
                </div>

                {/* Index number */}
                <span style={{ fontSize: '0.72rem', color: isEliminated ? '#334155' : '#64748B' }}>[{idx}]</span>
              </div>
            );
          })}
        </div>

        {/* Search Target Banner */}
        <div style={{
          padding: '0.55rem 1.25rem',
          borderRadius: '999px',
          backgroundColor: 'rgba(56, 189, 248, 0.1)',
          border: '1px solid rgba(56, 189, 248, 0.3)',
          color: '#38BDF8',
          fontSize: '0.88rem',
          fontWeight: 700
        }}>
          Target: <strong>{target}</strong> • Active Search Interval: [index {low} ... {high}]
        </div>
      </div>
    );
  }

  // 2. Bubble Sort
  if (algoId === 'bubble_sort') {
    const { array, comparing, swapped, sorted } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'flex-end', gap: '14px', height: '180px' }}>
          {array?.map((val, idx) => {
            const isComparing = comparing?.includes(idx);
            const isSwapped = swapped?.includes(idx);
            const isSorted = sorted?.includes(idx);

            let barColor = '#38BDF8';
            if (isSorted) barColor = '#10B981';
            if (isComparing) barColor = '#F59E0B';
            if (isSwapped) barColor = '#EF4444';

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 800, color: isComparing || isSwapped ? '#F8FAFC' : '#94A3B8' }}>
                  {val}
                </span>

                <div style={{
                  width: '34px',
                  height: `${Math.max(25, val * 1.8)}px`,
                  backgroundColor: barColor,
                  borderRadius: '6px 6px 0 0',
                  boxShadow: isComparing || isSwapped ? `0 0 16px ${barColor}` : isSorted ? '0 0 12px rgba(16, 185, 129, 0.3)' : 'none',
                  transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
                }} />

                <span style={{ fontSize: '0.72rem', color: '#64748B' }}>[{idx}]</span>
              </div>
            );
          })}
        </div>

        {/* Legend */}
        <div style={{ display: 'flex', gap: '1.25rem', fontSize: '0.76rem', color: '#94A3B8' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <div style={{ width: '10px', height: '10px', borderRadius: '2px', backgroundColor: '#F59E0B' }} />
            <span>Comparing (j, j+1)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <div style={{ width: '10px', height: '10px', borderRadius: '2px', backgroundColor: '#EF4444' }} />
            <span>Swapping Out of Order</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
            <div style={{ width: '10px', height: '10px', borderRadius: '2px', backgroundColor: '#10B981' }} />
            <span>Locked in Sorted Position</span>
          </div>
        </div>
      </div>
    );
  }

  // 3. Singly Linked List
  if (algoId === 'linked_list') {
    const { nodes, currIndex } = step.data || {};
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
        {nodes?.map((node, idx) => {
          const isCurr = currIndex === idx;
          const isHead = idx === 0;

          return (
            <React.Fragment key={idx}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                {/* Pointer Tag */}
                <div style={{ height: '18px', fontSize: '0.7rem', fontWeight: 800 }}>
                  {isCurr && <span style={{ color: '#38BDF8' }}>CURRENT ↓</span>}
                  {!isCurr && isHead && <span style={{ color: '#10B981' }}>HEAD ↓</span>}
                </div>

                {/* Node with Data & Pointer Compartments */}
                <div style={{
                  display: 'flex',
                  borderRadius: '10px',
                  border: isCurr ? '2px solid #38BDF8' : '1.5px solid #475569',
                  backgroundColor: '#1E293B',
                  overflow: 'hidden',
                  boxShadow: isCurr ? '0 0 16px rgba(56, 189, 248, 0.4)' : 'none'
                }}>
                  {/* Data Box */}
                  <div style={{
                    padding: '0.65rem 0.85rem',
                    backgroundColor: isCurr ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                    color: '#F8FAFC',
                    fontWeight: 800,
                    fontSize: '0.95rem'
                  }}>
                    {node.val}
                  </div>
                  {/* Next Pointer Box */}
                  <div style={{
                    padding: '0.65rem 0.65rem',
                    backgroundColor: '#0F172A',
                    color: '#38BDF8',
                    fontSize: '0.75rem',
                    display: 'flex',
                    alignItems: 'center',
                    borderLeft: '1px solid #334155'
                  }}>
                    •
                  </div>
                </div>

                <span style={{ fontSize: '0.68rem', color: '#64748B' }}>Node {idx}</span>
              </div>

              {/* Arrow linking to next node */}
              {idx < nodes.length - 1 ? (
                <div style={{ color: '#38BDF8', fontSize: '1.2rem', fontWeight: 'bold' }}>
                  →
                </div>
              ) : (
                <div style={{ color: '#EF4444', fontSize: '0.75rem', fontWeight: 800 }}>
                  → NULL
                </div>
              )}
            </React.Fragment>
          );
        })}
      </div>
    );
  }

  // 4. Stack (LIFO)
  if (algoId === 'stack_lifo') {
    const { stackItems, topElement, action } = step.data || {};
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '2.5rem' }}>
        {/* Beaker Container */}
        <div style={{
          width: '120px',
          height: '220px',
          borderLeft: '3px solid #6366F1',
          borderRight: '3px solid #6366F1',
          borderBottom: '3px solid #6366F1',
          borderRadius: '0 0 14px 14px',
          padding: '8px',
          display: 'flex',
          flexDirection: 'column-reverse',
          gap: '6px',
          backgroundColor: 'rgba(99, 102, 241, 0.05)'
        }}>
          {stackItems?.map((item, idx) => (
            <div
              key={idx}
              style={{
                padding: '0.55rem',
                borderRadius: '8px',
                backgroundColor: item === topElement ? '#4F46E5' : '#1E293B',
                border: item === topElement ? '2px solid #818CF8' : '1px solid #334155',
                color: '#FFFFFF',
                fontWeight: 800,
                textAlign: 'center',
                fontSize: '0.88rem',
                boxShadow: item === topElement ? '0 0 12px rgba(99, 102, 241, 0.5)' : 'none'
              }}
            >
              {item}
            </div>
          ))}
        </div>

        {/* Pointer & Action Callout */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div style={{ color: '#818CF8', fontWeight: 800, fontSize: '0.9rem' }}>
            ← TOP Pointer (Always at latest pushed)
          </div>
          <div style={{
            padding: '0.6rem 1rem',
            borderRadius: '10px',
            backgroundColor: 'rgba(99, 102, 241, 0.15)',
            border: '1px solid #6366F1',
            color: '#A5B4FC',
            fontSize: '0.82rem',
            fontWeight: 700
          }}>
            Action: {action || 'Stack State'}
          </div>
          <div style={{ fontSize: '0.76rem', color: '#64748B' }}>
            Rule: Only TOP item can be popped or peeked (LIFO)
          </div>
        </div>
      </div>
    );
  }

  // 5. Queue (FIFO)
  if (algoId === 'queue_fifo') {
    const { queueItems, action } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        {/* Horizontal Tunnel */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          borderTop: '3px solid #10B981',
          borderBottom: '3px solid #10B981',
          padding: '12px 18px',
          minWidth: '320px',
          justifyContent: 'center'
        }}>
          {queueItems?.map((item, idx) => {
            const isFront = idx === 0;
            const isRear = idx === queueItems.length - 1;

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                <div style={{ height: '16px', fontSize: '0.68rem', fontWeight: 800 }}>
                  {isFront && <span style={{ color: '#10B981' }}>FRONT ↓</span>}
                  {isRear && !isFront && <span style={{ color: '#38BDF8' }}>REAR ↓</span>}
                </div>
                <div style={{
                  width: '44px',
                  height: '44px',
                  borderRadius: '8px',
                  backgroundColor: isFront ? '#059669' : '#1E293B',
                  border: isFront ? '2px solid #34D399' : '1px solid #334155',
                  color: '#FFFFFF',
                  fontWeight: 800,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.92rem'
                }}>
                  {item}
                </div>
              </div>
            );
          })}
        </div>

        {/* Labels: Enqueue at Rear -> Dequeue at Front */}
        <div style={{ display: 'flex', justifyContent: 'space-between', width: '380px', fontSize: '0.78rem', fontWeight: 700 }}>
          <span style={{ color: '#10B981' }}>← Dequeue (Removes from Front)</span>
          <span style={{ color: '#38BDF8' }}>Enqueue (Adds at Rear) →</span>
        </div>
      </div>
    );
  }

  // 6. Tree / Graph / Recursion / DP / Arrays default fallback
  return (
    <div style={{ textAlign: 'center', color: '#94A3B8' }}>
      <Sparkles size={36} style={{ color: '#38BDF8', marginBottom: '0.5rem' }} />
      <div style={{ fontSize: '0.92rem', color: '#F8FAFC', fontWeight: 700 }}>
        {step.data?.title || 'Interactive Visual Representation'}
      </div>
      <div style={{ fontSize: '0.8rem', marginTop: '4px' }}>
        {step.data?.subtitle || 'Observe how state transitions change step-by-step.'}
      </div>
    </div>
  );
}

// ==============================================================
// STEP-BY-STEP TEACHING TRACES (PATIENT CS TEACHER SEQUENCES)
// ==============================================================
function getTeachingSteps(algoId) {
  if (algoId === 'binary_search') {
    const arr = [4, 9, 15, 23, 38, 45, 56, 72, 88, 99];
    const target = 56;

    return [
      {
        stageTitle: 'Step 1: Problem Setup & Invariant Declaration',
        phaseName: 'Initial Interval',
        isKeyOperation: false,
        data: { array: arr, low: 0, high: arr.length - 1, mid: -1, target, found: false },
        teacherExplanation: `Welcome! We need to find target number ${target} inside a sorted array of ${arr.length} elements. In linear search, we would check index 0, then 1, then 2... but Binary Search allows us to eliminate half of the elements in each step! We set low pointer to 0 and high pointer to ${arr.length - 1}.`,
        whyDidThisHappen: 'Binary search requires a sorted array. Because the array is ordered, any element to the left of an index is strictly smaller, and any element to the right is strictly larger.',
        activeCodeLine: 2,
        variables: { low: 0, high: 9, target: 56, remainingRange: '10 elements' },
        stateChangeNote: 'Interval initialized: [0 to 9]. Entire array active.',
        interactiveTask: {
          question: 'Where should we inspect first to maximize efficiency?',
          options: [
            'Directly in the exact middle (mid = (low + high) / 2)',
            'At index 0 (the beginning)',
            'At index 9 (the end)'
          ],
          correctIdx: 0,
          explanation: 'Inspecting the middle element guarantees that regardless of whether the target is larger or smaller, we can eliminate half of the entire array!'
        }
      },
      {
        stageTitle: 'Step 2: Calculate Midpoint & First Comparison',
        phaseName: 'Midpoint Calculation',
        isKeyOperation: true,
        data: { array: arr, low: 0, high: 9, mid: 4, target, found: false },
        teacherExplanation: `We compute mid = (0 + 9) / 2 = index 4. The value at arr[4] is 38. Now, compare: Is 38 equal to our target 56? No. Is 38 less than 56? Yes! (38 < 56).`,
        whyDidThisHappen: 'Since 38 is smaller than 56, and all elements at or to the left of index 4 are ≤ 38, our target 56 CANNOT possibly exist at indices 0, 1, 2, 3, or 4.',
        activeCodeLine: 4,
        variables: { low: 0, high: 9, mid: 4, 'arr[mid]': 38, target: 56 },
        stateChangeNote: 'Compared arr[4] (38) with target (56). Left half is about to be eliminated.',
        interactiveTask: {
          question: 'What pointer should be updated next?',
          options: [
            'Move low to mid + 1 (discarding indices 0..4)',
            'Move high to mid - 1',
            'Keep low and high unchanged'
          ],
          correctIdx: 0,
          explanation: 'Since 38 < 56, the target must be in the right half. We update low = mid + 1 = 5.'
        }
      },
      {
        stageTitle: 'Step 3: Discard Left Half & Shift Search Interval',
        phaseName: 'Halving Search Space',
        isKeyOperation: false,
        data: { array: arr, low: 5, high: 9, mid: -1, target, found: false },
        teacherExplanation: 'Notice what just happened: We set low = mid + 1 = 5. Indices 0 through 4 are now greyed out and permanently eliminated from consideration. We just reduced our work by 50% in a single step!',
        whyDidThisHappen: 'Sorted array monotonicity guarantees that no element before index 5 can equal 56.',
        activeCodeLine: 8,
        variables: { low: 5, high: 9, target: 56, remainingRange: '5 elements (5..9)' },
        stateChangeNote: 'Left half discarded. Active interval is now [5 to 9].'
      },
      {
        stageTitle: 'Step 4: Second Midpoint Calculation',
        phaseName: 'Second Division',
        isKeyOperation: true,
        data: { array: arr, low: 5, high: 9, mid: 7, target, found: false },
        teacherExplanation: `Now in the remaining range [5..9], we calculate mid = (5 + 9) / 2 = index 7. The value at arr[7] is 72. Compare: Is 72 equal to 56? No. Is 72 greater than 56? Yes! (72 > 56).`,
        whyDidThisHappen: 'Because 72 is greater than our target 56, the target CANNOT exist at index 7 or any index to its right (8, 9).',
        activeCodeLine: 4,
        variables: { low: 5, high: 9, mid: 7, 'arr[mid]': 72, target: 56 },
        stateChangeNote: 'Compared arr[7] (72) with target (56). Right half is about to be eliminated.',
        interactiveTask: {
          question: 'What pointer must we update to discard the right half?',
          options: [
            'Move high to mid - 1 = 6',
            'Move low to mid + 1',
            'Set high to 0'
          ],
          correctIdx: 0,
          explanation: 'Target 56 is smaller than 72, so we narrow the right boundary: high = mid - 1 = 6.'
        }
      },
      {
        stageTitle: 'Step 5: Narrow Right Boundary',
        phaseName: 'Discard Right Half',
        isKeyOperation: false,
        data: { array: arr, low: 5, high: 6, mid: -1, target, found: false },
        teacherExplanation: 'We update high = mid - 1 = 6. Now indices 7, 8, and 9 are eliminated as well. Notice how small our active search window has become: only indices 5 and 6 remain!',
        whyDidThisHappen: 'We narrowed the search space from both sides using binary decisions.',
        activeCodeLine: 10,
        variables: { low: 5, high: 6, target: 56, remainingRange: '2 elements (5..6)' },
        stateChangeNote: 'Active interval narrowed to [5 to 6].'
      },
      {
        stageTitle: 'Step 6: Target Discovered & Terminate!',
        phaseName: 'Target Found',
        isKeyOperation: true,
        data: { array: arr, low: 5, high: 6, mid: 6, target, found: true },
        teacherExplanation: `We compute mid = (5 + 6) / 2 = 5 or 6. Let's check mid = 6. Value at arr[6] is 56! 56 == target (56). Match found! The algorithm returns index 6 with full success.`,
        whyDidThisHappen: 'Target matches arr[mid] exactly. The loop terminates immediately in O(log N) operations.',
        activeCodeLine: 6,
        variables: { resultIndex: 6, target: 56, totalComparisons: 3 },
        stateChangeNote: 'Target 56 confirmed at index [6]! Search complete in 3 comparisons.'
      }
    ];
  }

  if (algoId === 'bubble_sort') {
    const initial = [42, 15, 88, 23, 6];
    return [
      {
        stageTitle: 'Step 1: Introduction to Bubble Sort',
        phaseName: 'Initial State',
        isKeyOperation: false,
        data: { array: initial, comparing: [], swapped: [], sorted: [] },
        teacherExplanation: 'Bubble Sort works by stepping through the array from left to right, comparing adjacent neighbors. If the left neighbor is strictly greater than the right neighbor, they are out of order, so we swap them!',
        whyDidThisHappen: 'We need to sort [42, 15, 88, 23, 6] in ascending order.',
        activeCodeLine: 1,
        variables: { pass: 1, i: 0, j: 0 },
        stateChangeNote: 'Array loaded in original unsorted order.'
      },
      {
        stageTitle: 'Step 2: Compare Adjacent Elements [0] and [1]',
        phaseName: 'First Comparison',
        isKeyOperation: true,
        data: { array: [42, 15, 88, 23, 6], comparing: [0, 1], swapped: [], sorted: [] },
        teacherExplanation: 'Compare arr[0] (42) with arr[1] (15). Is 42 > 15? Yes! 42 is larger than 15, so they are out of order.',
        whyDidThisHappen: 'In an ascending sorted array, smaller values must precede larger ones.',
        activeCodeLine: 4,
        variables: { 'arr[j]': 42, 'arr[j+1]': 15, conditionMet: '42 > 15 (true)' },
        stateChangeNote: 'Detected inversion between index 0 and 1.',
        interactiveTask: {
          question: 'What must Bubble Sort do when arr[j] > arr[j+1]?',
          options: [
            'Swap arr[j] and arr[j+1]',
            'Delete arr[j]',
            'Skip to the end of the array'
          ],
          correctIdx: 0,
          explanation: 'We perform an in-place swap using a temporary variable so the smaller element moves left.'
        }
      },
      {
        stageTitle: 'Step 3: Execute In-Place Swap',
        phaseName: 'Swap Execution',
        isKeyOperation: false,
        data: { array: [15, 42, 88, 23, 6], comparing: [], swapped: [0, 1], sorted: [] },
        teacherExplanation: 'Swap complete! 15 and 42 have traded places. The array is now [15, 42, 88, 23, 6].',
        whyDidThisHappen: 'Temporary variable preserved 42 while 15 moved to index 0.',
        activeCodeLine: 5,
        variables: { 'arr[0]': 15, 'arr[1]': 42, didSwap: true },
        stateChangeNote: 'Indices [0, 1] swapped.'
      },
      {
        stageTitle: 'Step 4: Lock Heaviest Element into Final Sorted Position',
        phaseName: 'Pass 1 Complete',
        isKeyOperation: true,
        data: { array: [15, 42, 23, 6, 88], comparing: [], swapped: [], sorted: [4] },
        teacherExplanation: 'At the end of Pass 1, the largest value in the entire array (88) has bubbled up all the way to the final index [4]. It is now permanently locked into its sorted position (highlighted green)!',
        whyDidThisHappen: 'Because each swap moves the larger element rightward, the maximum element must end up at the last index.',
        activeCodeLine: 8,
        variables: { lockedElement: 88, sortedCount: 1 },
        stateChangeNote: 'Index 4 is locked in final position. Subsequent passes ignore it.'
      }
    ];
  }

  // Fallback for other algorithms
  return [
    {
      stageTitle: 'Step 1: Initialization',
      phaseName: 'Initial State',
      isKeyOperation: false,
      data: { title: 'State Setup', subtitle: 'Initializing data structure components' },
      teacherExplanation: 'Every algorithm begins by establishing invariants and defining initial pointers.',
      whyDidThisHappen: 'Clean state is mandatory for deterministic execution.',
      activeCodeLine: 1,
      variables: { state: 'Ready' }
    },
    {
      stageTitle: 'Step 2: First Core Operation',
      phaseName: 'Processing',
      isKeyOperation: true,
      data: { title: 'Executing Step', subtitle: 'Traversing elements' },
      teacherExplanation: 'We perform the primary operation and update memory references.',
      whyDidThisHappen: 'Algorithmic progression requires state mutation.',
      activeCodeLine: 3,
      variables: { progress: '50%' }
    },
    {
      stageTitle: 'Step 3: Completion & Invariant Check',
      phaseName: 'Termination',
      isKeyOperation: false,
      data: { title: 'Execution Complete', subtitle: 'All elements processed successfully' },
      teacherExplanation: 'Algorithm completed successfully with optimal asymptotic efficiency.',
      whyDidThisHappen: 'Base or boundary conditions satisfied.',
      activeCodeLine: 5,
      variables: { status: 'Finished' }
    }
  ];
}

// Line-by-Line Code Implementations
function getCodeLines(algoId, lang) {
  if (algoId === 'binary_search') {
    if (lang === 'java') {
      return [
        'public int binarySearch(int[] arr, int target) {',
        '    int low = 0, high = arr.length - 1;',
        '    while (low <= high) {',
        '        int mid = low + (high - low) / 2;',
        '        if (arr[mid] == target) {',
        '            return mid; // Target found!',
        '        } else if (arr[mid] < target) {',
        '            low = mid + 1; // Discard left half',
        '        } else {',
        '            high = mid - 1; // Discard right half',
        '        }',
        '    }',
        '    return -1; // Not found',
        '}'
      ];
    } else {
      return [
        'def binary_search(arr, target):',
        '    low, high = 0, len(arr) - 1',
        '    while low <= high:',
        '        mid = (low + high) // 2',
        '        if arr[mid] == target:',
        '            return mid  # Target found!',
        '        elif arr[mid] < target:',
        '            low = mid + 1  # Discard left',
        '        else:',
        '            high = mid - 1  # Discard right',
        '    return -1'
      ];
    }
  }

  if (algoId === 'bubble_sort') {
    if (lang === 'java') {
      return [
        'public void bubbleSort(int[] arr) {',
        '    int n = arr.length;',
        '    for (int i = 0; i < n - 1; i++) {',
        '        for (int j = 0; j < n - i - 1; j++) {',
        '            if (arr[j] > arr[j + 1]) {',
        '                int temp = arr[j];',
        '                arr[j] = arr[j + 1];',
        '                arr[j + 1] = temp; // Swap',
        '            }',
        '        }',
        '    }',
        '}'
      ];
    } else {
      return [
        'def bubble_sort(arr):',
        '    n = len(arr)',
        '    for i in range(n - 1):',
        '        for j in range(n - i - 1):',
        '            if arr[j] > arr[j + 1]:',
        '                arr[j], arr[j + 1] = arr[j + 1], arr[j]',
        '    return arr'
      ];
    }
  }

  // Default generic code
  return [
    'public void executeAlgorithm() {',
    '    // Step 1: Initialize pointers and state',
    '    int pointer = 0;',
    '    // Step 2: Iterate while invariant holds',
    '    while (hasMoreSteps()) {',
    '        processCurrentStep();',
    '    }',
    '}'
  ];
}
