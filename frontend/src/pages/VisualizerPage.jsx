import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Pause, 
  RotateCcw, 
  ChevronRight, 
  ChevronLeft, 
  Sparkles,
  Layers, 
  Code2,
  Cpu,
  Zap,
  Target,
  HelpCircle,
  CheckCircle2,
  GitFork,
  ArrowRight,
  Database
} from 'lucide-react';
import { api } from '../services/api';

// ==============================================================
// 10 COMPREHENSIVE ALGORITHMS ACROSS ALL DSA CURRICULUM
// ==============================================================
const ALGORITHMS_CATALOG = [
  {
    id: 'array_traversal',
    name: 'Array Contiguity & Traversal',
    category: 'Arrays',
    complexityTime: 'O(N)',
    complexitySpace: 'O(1)',
    whatIsIt: 'An array stores elements at contiguous (adjacent) physical memory addresses in RAM.',
    whyNeedIt: 'Contiguity gives CPUs lightning-fast O(1) random access via arithmetic offset math: address = base + index * 4.',
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
    name: 'Bubble Sort (Comparisons & Swaps)',
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
    whereUsed: 'GPS navigation shortest routes, social network friend recommendations, web crawlers.'
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
    whereUsed: 'Bioinformatics DNA alignment, financial portfolio optimization, shortest path algorithms.'
  },
  {
    id: 'linear_search',
    name: 'Linear Search (Sequential Scan)',
    category: 'Searching',
    complexityTime: 'O(N)',
    complexitySpace: 'O(1)',
    whatIsIt: 'The simplest search algorithm: checks each element sequentially from start to finish until target is found.',
    whyNeedIt: 'Works on completely unsorted collections where Binary Search is impossible without sorting first.',
    whereUsed: 'Small arrays, unsorted lists, stream processing, hardware register scans.'
  },
  {
    id: 'selection_sort',
    name: 'Selection Sort (Minimum Extraction)',
    category: 'Sorting',
    complexityTime: 'O(N²)',
    complexitySpace: 'O(1)',
    whatIsIt: 'Sorts by repeatedly finding the minimum element from the unsorted segment and placing it at the beginning.',
    whyNeedIt: 'Minimizes memory writes: exactly O(N) swaps, making it useful when flash memory writes are expensive.',
    whereUsed: 'Embedded EEPROM sorting, small arrays, teaching loop invariants.'
  },
  {
    id: 'merge_sort',
    name: 'Merge Sort (Divide & Conquer)',
    category: 'Sorting',
    complexityTime: 'O(N log N)',
    complexitySpace: 'O(N)',
    whatIsIt: 'A divide-and-conquer algorithm that recursively halves the array, sorts the halves, and merges them.',
    whyNeedIt: 'Guarantees O(N log N) worst-case time and provides stable sorting.',
    whereUsed: 'Java Arrays.sort() for objects (TimSort), database external disk sorting, linked list sorting.'
  },
  {
    id: 'dijkstra',
    name: "Dijkstra's Shortest Path",
    category: 'Graphs',
    complexityTime: 'O((V + E) log V)',
    complexitySpace: 'O(V)',
    whatIsIt: 'Calculates the shortest paths from a single source vertex to all other vertices in a weighted graph.',
    whyNeedIt: 'Powers modern GPS satellite routing and internet OSPF protocol to find the fastest network paths.',
    whereUsed: 'Google Maps navigation, network packet routing (OSPF), flight route optimization.'
  }
];

export function normalizeAlgoId(rawId) {
  if (!rawId) return 'binary_search';
  const clean = String(rawId).toLowerCase().trim();
  if (clean === 'bfs' || clean.includes('bfs') || clean.includes('graph')) return 'graph_bfs';
  if (clean === 'dfs' || clean.includes('backtrack') || clean.includes('floodfill')) return 'recursion_callstack';
  if (clean.includes('tree') || clean.includes('bst') || clean.includes('lca') || clean.includes('trie') || clean.includes('heap')) return 'tree_traversal';
  if (clean.includes('stack') || clean.includes('histogram')) return 'stack_lifo';
  if (clean.includes('queue') || clean.includes('deque')) return 'queue_fifo';
  if (clean.includes('fibonacci') || clean.includes('dp') || clean.includes('dynamic') || clean.includes('knapsack') || clean.includes('lcs') || clean.includes('lis')) return 'dp_fibonacci';
  if (clean.includes('binary_search') || clean.includes('bs_on_answer')) return 'binary_search';
  if (clean.includes('linear_search') || clean.includes('kmp') || clean.includes('string')) return 'linear_search';
  if (clean.includes('selection_sort') || clean.includes('cyclic') || clean.includes('quickselect')) return 'selection_sort';
  if (clean.includes('merge_sort') || clean.includes('quick_sort')) return 'merge_sort';
  if (clean.includes('dijkstra') || clean.includes('shortest') || clean.includes('bellman') || clean.includes('a_star') || clean.includes('mst')) return 'dijkstra';
  if (clean.includes('bubble') || clean.includes('sort')) return 'bubble_sort';
  if (clean.includes('linked') || clean.includes('node') || clean.includes('lru') || clean.includes('pointer')) return 'linked_list';
  if (clean.includes('array') || clean.includes('sliding') || clean.includes('prefix') || clean.includes('matrix')) return 'array_traversal';
  return 'binary_search';
}

const SPEED_MODES = [
  { label: 'Very Slow', ms: 3000, desc: 'Deep contemplation' },
  { label: 'Slow (Teacher)', ms: 1800, desc: 'Patient teacher default' },
  { label: 'Normal', ms: 900, desc: 'Standard animation' },
  { label: 'Fast', ms: 400, desc: 'Quick overview' }
];

export default function VisualizerPage({ initialAlgorithm, onNavigate }) {
  const [selectedAlgoId, setSelectedAlgoId] = useState(() => normalizeAlgoId(initialAlgorithm));
  const [selectedSpeedIndex, setSelectedSpeedIndex] = useState(1);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentStepIdx, setCurrentStepIdx] = useState(0);
  const [autoPauseOnKey, setAutoPauseOnKey] = useState(true);
  const [codeLang, setCodeLang] = useState('java');
  const [studentAnswer, setStudentAnswer] = useState(null);
  const [showAnswerFeedback, setShowAnswerFeedback] = useState(false);
  const [voiceEnabled, setVoiceEnabled] = useState(true);

  const currentAlgo = ALGORITHMS_CATALOG.find(a => a.id === selectedAlgoId) || ALGORITHMS_CATALOG[1];
  const speedObj = SPEED_MODES[selectedSpeedIndex];

  // --- Voice Narration (Web Speech API) ---
  const speakStep = (text) => {
    if (!text || !window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.88;
    utterance.pitch = 1.0;
    utterance.volume = 1.0;
    window.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    if (initialAlgorithm) {
      setSelectedAlgoId(normalizeAlgoId(initialAlgorithm));
    }
  }, [initialAlgorithm]);

  const steps = getTeachingSteps(selectedAlgoId);
  const currentStep = steps[currentStepIdx] || steps[0];

  // Narrate current step when it changes
  useEffect(() => {
    if (voiceEnabled && currentStep) {
      const text = currentStep.teacherExplanation || currentStep.stageTitle || '';
      speakStep(text);
    }
    return () => { window.speechSynthesis?.cancel(); };
  }, [currentStepIdx, voiceEnabled]); // eslint-disable-line

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
              api.logActivity('visualization_run', currentAlgo.name, 120, { completed: true });
            } catch (e) {}
            return prev;
          }
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
      
      {/* 1. TEACHER MODE HERO BAR & CONTROLS */}
      <div style={{
        padding: '1.25rem 1.5rem',
        borderRadius: '16px',
        backgroundColor: '#0B1120',
        border: '1px solid #1E293B',
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
                color: 'var(--accent-cyan)',
                backgroundColor: 'rgba(56, 189, 248, 0.15)',
                border: '1px solid rgba(56, 189, 248, 0.3)',
                padding: '3px 10px',
                borderRadius: '999px',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '5px'
              }}>
                <Sparkles size={11} />
                <span>Patient CS Teacher Mode</span>
              </span>
              <span style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 700 }}>
                • Interactive Algorithm Simulator
              </span>
            </div>

            <h1 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#f8fafc', margin: 0 }}>
              {currentAlgo.name}
            </h1>
          </div>

          {/* Algorithm Picker Dropdown */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.82rem', fontWeight: 600, color: '#94a3b8' }}>Algorithm:</span>
            <select
              value={selectedAlgoId}
              onChange={(e) => setSelectedAlgoId(e.target.value)}
              style={{
                padding: '0.55rem 1rem',
                borderRadius: '10px',
                border: '1px solid #334155',
                backgroundColor: '#0f172a',
                color: '#f8fafc',
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
          borderTop: '1px solid #1E293B'
        }}>
          {/* Controls: Prev, Play/Pause, Next, Restart */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              style={{
                padding: '0.5rem 1.25rem',
                borderRadius: '10px',
                border: 'none',
                backgroundColor: isPlaying ? '#ef4444' : 'var(--accent-cyan)',
                color: isPlaying ? '#ffffff' : '#070b14',
                fontSize: '0.84rem',
                fontWeight: 800,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                cursor: 'pointer',
                transition: 'all 0.15s ease'
              }}
            >
              {isPlaying ? <Pause size={15} /> : <Play size={15} />}
              <span>{isPlaying ? 'Pause' : 'Play Teaching'}</span>
            </button>

            <button
              onClick={() => {
                setIsPlaying(false);
                setCurrentStepIdx(Math.max(0, currentStepIdx - 1));
              }}
              disabled={currentStepIdx === 0}
              style={{
                padding: '0.5rem 0.85rem',
                borderRadius: '10px',
                border: '1px solid #334155',
                backgroundColor: currentStepIdx === 0 ? '#0f172a' : '#1e293b',
                color: currentStepIdx === 0 ? '#475569' : '#e2e8f0',
                fontSize: '0.84rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                cursor: currentStepIdx === 0 ? 'not-allowed' : 'pointer'
              }}
            >
              <ChevronLeft size={16} />
              <span>Previous</span>
            </button>

            <button
              onClick={() => {
                setIsPlaying(false);
                const next = Math.min(steps.length - 1, currentStepIdx + 1);
                setCurrentStepIdx(next);
              }}
              disabled={currentStepIdx >= steps.length - 1}
              style={{
                padding: '0.5rem 0.85rem',
                borderRadius: '10px',
                border: '1px solid #334155',
                backgroundColor: currentStepIdx >= steps.length - 1 ? '#0f172a' : '#1e293b',
                color: currentStepIdx >= steps.length - 1 ? '#475569' : '#e2e8f0',
                fontSize: '0.84rem',
                fontWeight: 600,
                display: 'flex',
                alignItems: 'center',
                gap: '4px',
                cursor: currentStepIdx >= steps.length - 1 ? 'not-allowed' : 'pointer'
              }}
            >
              <span>Next Step</span>
              <ChevronRight size={16} />
            </button>

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
                border: '1px solid #334155',
                backgroundColor: '#1e293b',
                color: '#94a3b8',
                cursor: 'pointer'
              }}
              title="Restart from beginning"
            >
              <RotateCcw size={15} />
            </button>
          </div>

          {/* Speed Presets & Auto-pause Checkbox */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexWrap: 'wrap' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.78rem', color: '#cbd5e1', fontWeight: 600, cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={autoPauseOnKey}
                onChange={(e) => setAutoPauseOnKey(e.target.checked)}
                style={{ accentColor: 'var(--accent-cyan)', cursor: 'pointer' }}
              />
              <span>Pause on Key Decision</span>
            </label>

            {/* Speed Buttons */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <span style={{ fontSize: '0.74rem', color: '#94a3b8', fontWeight: 600, marginRight: '4px' }}>Speed:</span>
              <div style={{
                display: 'flex',
                padding: '3px',
                borderRadius: '999px',
                backgroundColor: '#0f172a',
                border: '1px solid #334155'
              }}>
                {SPEED_MODES.map((mode, i) => (
                  <button
                    key={mode.label}
                    onClick={() => setSelectedSpeedIndex(i)}
                    style={{
                      padding: '0.25rem 0.65rem',
                      borderRadius: '999px',
                      border: 'none',
                      backgroundColor: selectedSpeedIndex === i ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                      color: selectedSpeedIndex === i ? 'var(--accent-cyan)' : '#94a3b8',
                      fontSize: '0.74rem',
                      fontWeight: selectedSpeedIndex === i ? 800 : 500,
                      cursor: 'pointer'
                    }}
                  >
                    {mode.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Step Counter */}
            <div style={{ fontSize: '0.82rem', fontWeight: 700, color: '#f8fafc' }}>
              Step <span style={{ color: 'var(--accent-cyan)' }}>{currentStepIdx + 1}</span> of {steps.length}
            </div>

            {/* Voice Toggle */}
            <button
              onClick={() => {
                const next = !voiceEnabled;
                setVoiceEnabled(next);
                if (!next) window.speechSynthesis?.cancel();
              }}
              title={voiceEnabled ? 'Mute voice narration' : 'Enable voice narration'}
              style={{
                padding: '0.3rem 0.65rem',
                borderRadius: '999px',
                border: `1px solid ${voiceEnabled ? 'var(--accent-cyan)' : '#334155'}`,
                backgroundColor: voiceEnabled ? 'rgba(56,189,248,0.1)' : '#0f172a',
                color: voiceEnabled ? 'var(--accent-cyan)' : '#475569',
                fontSize: '0.78rem',
                fontWeight: 700,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '5px'
              }}
            >
              {voiceEnabled ? '🔊' : '🔇'}
              <span>{voiceEnabled ? 'Voice On' : 'Voice Off'}</span>
            </button>
          </div>
        </div>
      </div>

      {/* 2. THE MAIN VISUAL TEACHING STAGE & CODE SYNCHRONIZATION */}
      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.95fr', gap: '1.25rem' }}>
        
        {/* Left Column: Visual Canvas & Patient Teacher Callout */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* Main Visual Stage Box */}
          <div style={{
            backgroundColor: '#0B1120',
            borderRadius: '18px',
            border: '1px solid #1E293B',
            padding: '1.5rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem',
            minHeight: '400px'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ fontSize: '0.85rem', fontWeight: 800, color: 'var(--accent-cyan)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                {currentStep.stageTitle || 'Execution Stage'}
              </div>

              {currentStep.isKeyOperation && (
                <span style={{
                  fontSize: '0.72rem',
                  fontWeight: 800,
                  color: '#fbbf24',
                  backgroundColor: 'rgba(251, 191, 36, 0.15)',
                  padding: '2px 8px',
                  borderRadius: '6px',
                  border: '1px solid rgba(251, 191, 36, 0.3)'
                }}>
                  ⚠️ Key Algorithmic Decision
                </span>
              )}
            </div>

            {/* Interactive Stage Canvas */}
            <div style={{
              flex: 1,
              backgroundColor: '#070b14',
              borderRadius: '14px',
              border: '1px solid #1E293B',
              padding: '2rem 1.5rem',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              position: 'relative',
              overflow: 'hidden',
              minHeight: '260px'
            }}>
              {renderVisualStructure(selectedAlgoId, currentStep)}
            </div>

            {/* State Footnote */}
            {currentStep.stateChangeNote && (
              <div style={{
                padding: '0.65rem 0.95rem',
                borderRadius: '10px',
                backgroundColor: '#0f172a',
                border: '1px solid #1E293B',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.8rem',
                color: '#cbd5e1'
              }}>
                <span style={{ fontWeight: 800, color: 'var(--accent-cyan)' }}>State Transition:</span>
                <span>{currentStep.stateChangeNote}</span>
              </div>
            )}
          </div>

          {/* Teacher Explanation Callout */}
          <div style={{
            padding: '1.25rem 1.5rem',
            borderRadius: '16px',
            backgroundColor: '#0B1120',
            border: '1px solid #1E293B',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <div style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                backgroundColor: 'rgba(56, 189, 248, 0.15)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '1.1rem'
              }}>
                👨‍🏫
              </div>
              <div>
                <h4 style={{ margin: 0, fontSize: '0.98rem', fontWeight: 800, color: '#f8fafc' }}>
                  Patient Teacher's Explanation
                </h4>
                <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>
                  Step {currentStepIdx + 1} • {currentStep.phaseName || 'Step Invariant'}
                </div>
              </div>
            </div>

            <p style={{
              fontSize: '0.88rem',
              color: '#e2e8f0',
              lineHeight: 1.6,
              margin: 0
            }}>
              {currentStep.teacherExplanation}
            </p>

            {currentStep.whyDidThisHappen && (
              <div style={{
                marginTop: '0.35rem',
                padding: '0.85rem 1rem',
                borderRadius: '10px',
                backgroundColor: 'rgba(192, 132, 252, 0.1)',
                border: '1px solid rgba(192, 132, 252, 0.25)'
              }}>
                <div style={{ fontSize: '0.78rem', fontWeight: 800, color: '#c084fc', marginBottom: '3px', display: 'flex', alignItems: 'center', gap: '5px' }}>
                  <HelpCircle size={14} />
                  <span>Why did this happen?</span>
                </div>
                <div style={{ fontSize: '0.82rem', color: '#e2e8f0', lineHeight: 1.5 }}>
                  {currentStep.whyDidThisHappen}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column: Code Synchronization, Variable Watcher & Interactive Try-It */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          
          {/* Synchronized Code View */}
          <div style={{
            backgroundColor: '#0B1120',
            borderRadius: '18px',
            border: '1px solid #1E293B',
            padding: '1.25rem 1.4rem',
            display: 'flex',
            flexDirection: 'column',
            gap: '0.75rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Code2 size={17} style={{ color: 'var(--accent-cyan)' }} />
                <h4 style={{ margin: 0, fontSize: '0.92rem', fontWeight: 800, color: '#f8fafc' }}>
                  Synchronized Code
                </h4>
              </div>

              {/* Language Toggle */}
              <div style={{ display: 'flex', gap: '4px', backgroundColor: '#0f172a', padding: '2px', borderRadius: '8px' }}>
                <button
                  onClick={() => setCodeLang('java')}
                  style={{
                    padding: '0.2rem 0.65rem',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: codeLang === 'java' ? 'rgba(245, 158, 11, 0.25)' : 'transparent',
                    color: codeLang === 'java' ? '#fbbf24' : '#94a3b8',
                    fontSize: '0.74rem',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  ☕ Java
                </button>
                <button
                  onClick={() => setCodeLang('python')}
                  style={{
                    padding: '0.2rem 0.65rem',
                    borderRadius: '6px',
                    border: 'none',
                    backgroundColor: codeLang === 'python' ? 'rgba(56, 189, 248, 0.25)' : 'transparent',
                    color: codeLang === 'python' ? 'var(--accent-cyan)' : '#94a3b8',
                    fontSize: '0.74rem',
                    fontWeight: 700,
                    cursor: 'pointer'
                  }}
                >
                  🐍 Python
                </button>
              </div>
            </div>

            {/* Line-by-Line Code Viewer */}
            <div style={{
              backgroundColor: '#070b14',
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
                      backgroundColor: isCurrentLine ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                      borderLeft: isCurrentLine ? '3px solid var(--accent-cyan)' : '3px solid transparent',
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

          {/* Live Variable Watcher */}
          <div style={{
            backgroundColor: '#0B1120',
            borderRadius: '18px',
            border: '1px solid #1E293B',
            padding: '1.25rem 1.4rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '0.75rem' }}>
              <Cpu size={16} style={{ color: '#10B981' }} />
              <h4 style={{ margin: 0, fontSize: '0.92rem', fontWeight: 800, color: '#f8fafc' }}>
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
                    borderRadius: '8px',
                    backgroundColor: '#070b14',
                    border: '1px solid #1E293B',
                    display: 'flex',
                    flexDirection: 'column'
                  }}
                >
                  <span style={{ fontSize: '0.68rem', fontWeight: 700, color: '#94a3b8', textTransform: 'uppercase' }}>
                    {key}
                  </span>
                  <span style={{ fontSize: '0.92rem', fontWeight: 800, color: 'var(--accent-cyan)', marginTop: '2px', wordBreak: 'break-all' }}>
                    {String(val)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Interactive Try It Yourself */}
          {currentStep.interactiveTask && (
            <div style={{
              backgroundColor: '#0B1120',
              borderRadius: '18px',
              border: '1px solid rgba(251, 191, 36, 0.3)',
              padding: '1.25rem 1.4rem',
              display: 'flex',
              flexDirection: 'column',
              gap: '0.75rem'
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Target size={17} style={{ color: '#fbbf24' }} />
                <h4 style={{ margin: 0, fontSize: '0.92rem', fontWeight: 800, color: '#fbbf24' }}>
                  Interactive Checkpoint: Test Your Understanding
                </h4>
              </div>

              <p style={{ fontSize: '0.84rem', color: '#e2e8f0', margin: 0, fontWeight: 600 }}>
                {currentStep.interactiveTask.question}
              </p>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                {currentStep.interactiveTask.options.map((opt, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setStudentAnswer(idx);
                      setShowAnswerFeedback(true);
                    }}
                    style={{
                      padding: '0.55rem 0.85rem',
                      borderRadius: '8px',
                      border: studentAnswer === idx 
                        ? (idx === currentStep.interactiveTask.correctIdx ? '1.5px solid #10B981' : '1.5px solid #EF4444')
                        : '1px solid #334155',
                      backgroundColor: studentAnswer === idx
                        ? (idx === currentStep.interactiveTask.correctIdx ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)')
                        : '#0f172a',
                      color: '#f8fafc',
                      fontSize: '0.8rem',
                      fontWeight: 600,
                      textAlign: 'left',
                      cursor: 'pointer'
                    }}
                  >
                    {opt}
                  </button>
                ))}
              </div>

              {showAnswerFeedback && (
                <div style={{
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  backgroundColor: studentAnswer === currentStep.interactiveTask.correctIdx ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                  border: studentAnswer === currentStep.interactiveTask.correctIdx ? '1px solid rgba(16, 185, 129, 0.4)' : '1px solid rgba(239, 68, 68, 0.4)',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  color: studentAnswer === currentStep.interactiveTask.correctIdx ? '#34d399' : '#f87171'
                }}>
                  {studentAnswer === currentStep.interactiveTask.correctIdx ? '✓ Correct! ' : '✗ Re-check: '}
                  {currentStep.interactiveTask.explanation}
                </div>
              )}
            </div>
          )}

        </div>
      </div>

      {/* 3. 10-PART TEACHING SEQUENCE REFERENCE BAR */}
      <div style={{
        backgroundColor: '#0B1120',
        borderRadius: '16px',
        padding: '1.25rem 1.5rem',
        border: '1px solid #1E293B',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
        gap: '1.25rem'
      }}>
        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: 'var(--accent-cyan)', textTransform: 'uppercase', marginBottom: '4px' }}>
            1. What is this concept?
          </div>
          <div style={{ fontSize: '0.84rem', color: '#94a3b8', lineHeight: 1.5 }}>
            {currentAlgo.whatIsIt}
          </div>
        </div>

        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#10B981', textTransform: 'uppercase', marginBottom: '4px' }}>
            2. Why do we need it?
          </div>
          <div style={{ fontSize: '0.84rem', color: '#94a3b8', lineHeight: 1.5 }}>
            {currentAlgo.whyNeedIt}
          </div>
        </div>

        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#fbbf24', textTransform: 'uppercase', marginBottom: '4px' }}>
            3. Real-World Applications
          </div>
          <div style={{ fontSize: '0.84rem', color: '#94a3b8', lineHeight: 1.5 }}>
            {currentAlgo.whereUsed}
          </div>
        </div>

        <div>
          <div style={{ fontSize: '0.72rem', fontWeight: 800, color: '#c084fc', textTransform: 'uppercase', marginBottom: '4px' }}>
            4. Asymptotic Complexity
          </div>
          <div style={{ fontSize: '0.84rem', color: '#f8fafc', fontWeight: 700, marginTop: '2px' }}>
            Time: <span style={{ color: 'var(--accent-cyan)' }}>{currentAlgo.complexityTime}</span> • Space: <span style={{ color: '#10B981' }}>{currentAlgo.complexitySpace}</span>
          </div>
        </div>
      </div>

    </div>
  );
}

// ==============================================================
// CUSTOM VISUAL RENDERING ENGINES FOR ALL 10 DATA STRUCTURES
// ==============================================================
function renderVisualStructure(algoId, step) {
  // 1. Array Contiguity & Traversal (Memory Address Math)
  if (algoId === 'array_traversal') {
    const { array, activeIndex, baseAddress } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        <div style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>
          Contiguous Physical RAM Architecture: Address = Base (0x1000) + (i × 4 bytes)
        </div>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {(array || [10, 20, 30, 40, 50]).map((val, idx) => {
            const isActive = activeIndex === idx;
            const hexAddr = `0x${(baseAddress + idx * 4).toString(16).toUpperCase()}`;

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                <span style={{ fontSize: '0.72rem', fontFamily: 'monospace', color: isActive ? 'var(--accent-cyan)' : '#64748b' }}>
                  {hexAddr}
                </span>

                <div style={{
                  width: '52px',
                  height: '52px',
                  borderRadius: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '1.1rem',
                  backgroundColor: isActive ? 'rgba(56, 189, 248, 0.25)' : '#1E293B',
                  border: isActive ? '2px solid var(--accent-cyan)' : '1px solid #334155',
                  color: isActive ? '#f8fafc' : '#94a3b8',
                  boxShadow: isActive ? '0 0 20px rgba(56, 189, 248, 0.4)' : 'none',
                  transition: 'all 0.3s ease'
                }}>
                  {val}
                </div>

                <span style={{ fontSize: '0.72rem', color: '#64748b' }}>Index [{idx}]</span>
              </div>
            );
          })}
        </div>

        <div style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 600 }}>
          ⚡ Constant O(1) CPU Cache Direct Offset Access
        </div>
      </div>
    );
  }

  // 2. Binary Search
  if (algoId === 'binary_search') {
    const { array, low, high, mid, target, found } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '2rem', width: '100%' }}>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {array?.map((val, idx) => {
            const isMid = mid === idx;
            const isLow = low === idx;
            const isHigh = high === idx;
            const isTargetMatch = found && isMid;
            const isEliminated = idx < low || idx > high;

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                <div style={{ height: '22px', fontSize: '0.7rem', fontWeight: 800, display: 'flex', alignItems: 'center' }}>
                  {isMid && <span style={{ color: '#38BDF8', backgroundColor: 'rgba(56, 189, 248, 0.2)', padding: '1px 6px', borderRadius: '4px' }}>MID</span>}
                  {!isMid && isLow && <span style={{ color: '#10B981', backgroundColor: 'rgba(16, 185, 129, 0.2)', padding: '1px 6px', borderRadius: '4px' }}>LOW</span>}
                  {!isMid && isHigh && <span style={{ color: '#F59E0B', backgroundColor: 'rgba(245, 158, 11, 0.2)', padding: '1px 6px', borderRadius: '4px' }}>HIGH</span>}
                </div>

                <div style={{ height: '14px', color: isMid ? '#38BDF8' : isLow ? '#10B981' : isHigh ? '#F59E0B' : 'transparent' }}>
                  {(isMid || isLow || isHigh) && '↓'}
                </div>

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

                <span style={{ fontSize: '0.72rem', color: isEliminated ? '#334155' : '#64748B' }}>[{idx}]</span>
              </div>
            );
          })}
        </div>

        <div style={{
          padding: '0.55rem 1.25rem',
          borderRadius: '999px',
          backgroundColor: 'rgba(56, 189, 248, 0.1)',
          border: '1px solid rgba(56, 189, 248, 0.3)',
          color: '#38BDF8',
          fontSize: '0.88rem',
          fontWeight: 700
        }}>
          Target: <strong>{target}</strong> • Active Interval: [index {low} ... {high}]
        </div>
      </div>
    );
  }

  // 3. Bubble Sort
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
            <span>Sorted Final Position</span>
          </div>
        </div>
      </div>
    );
  }

  // 4. Singly Linked List
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
                <div style={{ height: '18px', fontSize: '0.7rem', fontWeight: 800 }}>
                  {isCurr && <span style={{ color: '#38BDF8' }}>CURRENT ↓</span>}
                  {!isCurr && isHead && <span style={{ color: '#10B981' }}>HEAD ↓</span>}
                </div>

                <div style={{
                  display: 'flex',
                  borderRadius: '10px',
                  border: isCurr ? '2px solid #38BDF8' : '1.5px solid #475569',
                  backgroundColor: '#1E293B',
                  overflow: 'hidden',
                  boxShadow: isCurr ? '0 0 16px rgba(56, 189, 248, 0.4)' : 'none'
                }}>
                  <div style={{
                    padding: '0.65rem 0.85rem',
                    backgroundColor: isCurr ? 'rgba(56, 189, 248, 0.2)' : 'transparent',
                    color: '#F8FAFC',
                    fontWeight: 800,
                    fontSize: '0.95rem'
                  }}>
                    {node.val}
                  </div>
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

  // 5. Stack (LIFO)
  if (algoId === 'stack_lifo') {
    const { stackItems, topElement, action } = step.data || {};
    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: '2.5rem' }}>
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
          <div style={{ fontSize: '0.76rem', color: '#94a3b8' }}>
            Rule: Only TOP item can be popped or peeked (LIFO)
          </div>
        </div>
      </div>
    );
  }

  // 6. Queue (FIFO)
  if (algoId === 'queue_fifo') {
    const { queueItems, action } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
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

        <div style={{ display: 'flex', justifyContent: 'space-between', width: '380px', fontSize: '0.78rem', fontWeight: 700 }}>
          <span style={{ color: '#10B981' }}>← Dequeue (Removes from Front)</span>
          <span style={{ color: '#38BDF8' }}>Enqueue (Adds at Rear) →</span>
        </div>
      </div>
    );
  }

  // 7. Binary Tree In-Order Traversal (Interactive 2D SVG Tree)
  if (algoId === 'tree_traversal') {
    const { activeNode, visitedNodes, traversalOrder } = step.data || {};
    const nodes = [
      { id: 40, x: 180, y: 35, val: 40 },
      { id: 20, x: 90, y: 105, val: 20 },
      { id: 60, x: 270, y: 105, val: 60 },
      { id: 10, x: 45, y: 175, val: 10 },
      { id: 30, x: 135, y: 175, val: 30 },
      { id: 50, x: 225, y: 175, val: 50 },
      { id: 70, x: 315, y: 175, val: 70 }
    ];
    const edges = [
      { from: 40, to: 20 },
      { from: 40, to: 60 },
      { from: 20, to: 10 },
      { from: 20, to: 30 },
      { from: 60, to: 50 },
      { from: 60, to: 70 }
    ];

    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1rem', width: '100%' }}>
        <svg width="360" height="220" style={{ overflow: 'visible' }}>
          {edges.map((e, idx) => {
            const p1 = nodes.find(n => n.id === e.from);
            const p2 = nodes.find(n => n.id === e.to);
            return (
              <line
                key={idx}
                x1={p1.x}
                y1={p1.y}
                x2={p2.x}
                y2={p2.y}
                stroke="#334155"
                strokeWidth="2.5"
              />
            );
          })}
          {nodes.map(n => {
            const isActive = activeNode === n.id;
            const isVisited = visitedNodes?.includes(n.id);

            return (
              <g key={n.id} transform={`translate(${n.x}, ${n.y})`}>
                <circle
                  r="20"
                  fill={isActive ? 'rgba(56, 189, 248, 0.3)' : isVisited ? 'rgba(16, 185, 129, 0.25)' : '#1e293b'}
                  stroke={isActive ? '#38bdf8' : isVisited ? '#10b981' : '#475569'}
                  strokeWidth={isActive ? '3' : '2'}
                  filter={isActive ? 'drop-shadow(0 0 8px #38bdf8)' : 'none'}
                />
                <text
                  textAnchor="middle"
                  dy=".35em"
                  fill={isActive ? '#38bdf8' : isVisited ? '#10b981' : '#f8fafc'}
                  fontSize="13"
                  fontWeight="800"
                >
                  {n.val}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Traversal Output Sequence */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '8px',
          padding: '0.45rem 1rem',
          backgroundColor: '#0f172a',
          borderRadius: '999px',
          border: '1px solid #1e293b',
          fontSize: '0.8rem',
          color: '#cbd5e1'
        }}>
          <span style={{ fontWeight: 700, color: '#10b981' }}>In-Order Output:</span>
          <span>[ {(traversalOrder || []).join(' → ')} ]</span>
        </div>
      </div>
    );
  }

  // 8. Graph BFS Traversal (SVG Network)
  if (algoId === 'graph_bfs') {
    const { activeVertex, visitedSet, queue } = step.data || {};
    const vertices = [
      { id: 'A', x: 80, y: 60 },
      { id: 'B', x: 180, y: 35 },
      { id: 'C', x: 180, y: 135 },
      { id: 'D', x: 280, y: 45 },
      { id: 'E', x: 280, y: 125 }
    ];
    const edges = [
      { from: 'A', to: 'B' },
      { from: 'A', to: 'C' },
      { from: 'B', to: 'D' },
      { from: 'C', to: 'E' },
      { from: 'B', to: 'C' }
    ];

    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.25rem', width: '100%' }}>
        <svg width="360" height="170" style={{ overflow: 'visible' }}>
          {edges.map((e, idx) => {
            const p1 = vertices.find(v => v.id === e.from);
            const p2 = vertices.find(v => v.id === e.to);
            return (
              <line
                key={idx}
                x1={p1.x}
                y1={p1.y}
                x2={p2.x}
                y2={p2.y}
                stroke="#334155"
                strokeWidth="2"
              />
            );
          })}
          {vertices.map(v => {
            const isActive = activeVertex === v.id;
            const isVisited = visitedSet?.includes(v.id);

            return (
              <g key={v.id} transform={`translate(${v.x}, ${v.y})`}>
                <circle
                  r="18"
                  fill={isActive ? 'rgba(56, 189, 248, 0.35)' : isVisited ? 'rgba(16, 185, 129, 0.25)' : '#1e293b'}
                  stroke={isActive ? 'var(--accent-cyan)' : isVisited ? '#10b981' : '#475569'}
                  strokeWidth="2.5"
                  filter={isActive ? 'drop-shadow(0 0 10px rgba(56, 189, 248, 0.6))' : 'none'}
                />
                <text
                  textAnchor="middle"
                  dy=".35em"
                  fill="#f8fafc"
                  fontSize="12"
                  fontWeight="800"
                >
                  {v.id}
                </text>
              </g>
            );
          })}
        </svg>

        {/* Live Queue and Visited Display */}
        <div style={{ display: 'flex', gap: '1.5rem', fontSize: '0.8rem' }}>
          <div>
            <span style={{ color: '#94a3b8' }}>BFS Queue: </span>
            <strong style={{ color: 'var(--accent-cyan)' }}>[ {(queue || []).join(', ')} ]</strong>
          </div>
          <div>
            <span style={{ color: '#94a3b8' }}>Visited Set: </span>
            <strong style={{ color: '#10b981' }}>{'{ ' + (visitedSet || []).join(', ') + ' }'}</strong>
          </div>
        </div>
      </div>
    );
  }

  // 9. Recursion & Visual Call Stack
  if (algoId === 'recursion_callstack') {
    const { stackFrames, phase } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.25rem', width: '100%' }}>
        <div style={{ fontSize: '0.78rem', color: '#c084fc', fontWeight: 800 }}>
          JVM Activation Call Stack: {phase || 'Winding & Unwinding Frames'}
        </div>

        <div style={{
          width: '260px',
          display: 'flex',
          flexDirection: 'column-reverse',
          gap: '6px',
          border: '2px solid #334155',
          borderRadius: '10px',
          padding: '10px',
          backgroundColor: '#0a0f1d'
        }}>
          {stackFrames?.map((frame, idx) => (
            <div
              key={idx}
              style={{
                padding: '0.5rem 0.75rem',
                borderRadius: '6px',
                backgroundColor: idx === stackFrames.length - 1 ? 'rgba(192, 132, 252, 0.25)' : '#1e293b',
                border: idx === stackFrames.length - 1 ? '1.5px solid #c084fc' : '1px solid #334155',
                color: '#f8fafc',
                fontSize: '0.82rem',
                display: 'flex',
                justifyContent: 'space-between',
                fontFamily: 'monospace'
              }}
            >
              <span>{frame.name}</span>
              <span style={{ color: '#38bdf8' }}>{frame.retVal ? `returns ${frame.retVal}` : `n = ${frame.n}`}</span>
            </div>
          ))}
        </div>

        <div style={{ fontSize: '0.74rem', color: '#94a3b8' }}>
          Stack grows during recursive calls, pops during returns.
        </div>
      </div>
    );
  }

  // 10. Dynamic Programming Tabulation Table
  if (algoId === 'dp_fibonacci') {
    const { dpTable, activeIndex, formula } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        <div style={{ fontSize: '0.82rem', color: '#fbbf24', fontWeight: 700 }}>
          Tabulation Formula: {formula || 'dp[i] = dp[i-1] + dp[i-2]'}
        </div>

        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {(dpTable || [0, 1, 1, 2, 3, 5, 8]).map((val, idx) => {
            const isComputing = activeIndex === idx;
            const isSource = activeIndex && (idx === activeIndex - 1 || idx === activeIndex - 2);

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                <span style={{ fontSize: '0.72rem', color: '#94a3b8' }}>dp[{idx}]</span>
                <div style={{
                  width: '46px',
                  height: '46px',
                  borderRadius: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '1rem',
                  backgroundColor: isComputing 
                    ? 'rgba(251, 191, 36, 0.25)' 
                    : isSource 
                    ? 'rgba(56, 189, 248, 0.2)' 
                    : '#1e293b',
                  border: isComputing 
                    ? '2px solid #fbbf24' 
                    : isSource 
                    ? '1.5px solid #38bdf8' 
                    : '1px solid #334155',
                  color: '#f8fafc',
                  boxShadow: isComputing ? '0 0 16px rgba(251, 191, 36, 0.4)' : 'none'
                }}>
                  {val !== null ? val : '?'}
                </div>
              </div>
            );
          })}
        </div>

        <div style={{ fontSize: '0.76rem', color: '#10b981', fontWeight: 600 }}>
          Linear O(N) Tabulation avoids 2ⁿ redundant tree calculations!
        </div>
      </div>
    );
  }

  // 11. Linear Search Scan
  if (algoId === 'linear_search') {
    const { array, activeIndex, target, found } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', backgroundColor: '#0f172a', padding: '6px 14px', borderRadius: '8px', border: '1px solid #334155' }}>
          <span style={{ fontSize: '0.82rem', color: '#94a3b8' }}>Search Target:</span>
          <span style={{ fontSize: '0.95rem', fontWeight: 800, color: 'var(--accent-cyan)' }}>{target || 95}</span>
          <span style={{ fontSize: '0.82rem', color: found ? '#10b981' : '#f59e0b', fontWeight: 700 }}>
            {found ? '✓ Target Found!' : 'Searching sequentially...'}
          </span>
        </div>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {(array || [18, 42, 7, 95, 33, 61]).map((val, idx) => {
            const isActive = activeIndex === idx;
            const isMatch = found && isActive;
            const isChecked = idx < activeIndex;

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                <span style={{ fontSize: '0.72rem', color: isActive ? 'var(--accent-cyan)' : '#64748b', fontWeight: isActive ? 700 : 400 }}>
                  {isActive ? '▲ current' : `[${idx}]`}
                </span>

                <div style={{
                  width: '52px',
                  height: '52px',
                  borderRadius: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '1.1rem',
                  backgroundColor: isMatch ? 'rgba(16, 185, 129, 0.25)' : (isActive ? 'rgba(56, 189, 248, 0.25)' : (isChecked ? '#0b1120' : '#1E293B')),
                  border: isMatch ? '2px solid #10b981' : (isActive ? '2px solid var(--accent-cyan)' : '1px solid #334155'),
                  color: isMatch ? '#10b981' : (isActive ? '#f8fafc' : (isChecked ? '#64748b' : '#94a3b8')),
                  boxShadow: isMatch ? '0 0 20px rgba(16, 185, 129, 0.5)' : (isActive ? '0 0 15px rgba(56, 189, 248, 0.4)' : 'none'),
                  transition: 'all 0.3s ease'
                }}>
                  {val}
                </div>

                <span style={{ fontSize: '0.68rem', color: isMatch ? '#10b981' : (isChecked ? '#475569' : '#64748b') }}>
                  {isMatch ? 'MATCH' : (isChecked ? 'checked' : 'pending')}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // 12. Selection Sort
  if (algoId === 'selection_sort') {
    const { array, currentIdx, minIdx, sortedBoundary } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        <div style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>
          Selection Sort: Select Global Minimum from Unsorted Segment and Place at Front
        </div>

        <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {(array || [10, 13, 14, 29, 37]).map((val, idx) => {
            const isSorted = sortedBoundary !== undefined && idx < sortedBoundary;
            const isMin = minIdx === idx;
            const isCurrent = currentIdx === idx;

            return (
              <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px' }}>
                <span style={{ fontSize: '0.72rem', color: isMin ? '#ef4444' : (isSorted ? '#10b981' : '#64748b'), fontWeight: isMin || isSorted ? 700 : 400 }}>
                  {isMin ? 'MIN' : (isSorted ? 'SORTED' : `[${idx}]`)}
                </span>

                <div style={{
                  width: '52px',
                  height: '52px',
                  borderRadius: '10px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: '1.1rem',
                  backgroundColor: isMin ? 'rgba(239, 68, 68, 0.25)' : (isSorted ? 'rgba(16, 185, 129, 0.2)' : (isCurrent ? 'rgba(56, 189, 248, 0.2)' : '#1E293B')),
                  border: isMin ? '2px solid #ef4444' : (isSorted ? '2px solid #10b981' : (isCurrent ? '2px solid var(--accent-cyan)' : '1px solid #334155')),
                  color: isMin ? '#fca5a5' : (isSorted ? '#6ee7b7' : '#f8fafc'),
                  boxShadow: isMin ? '0 0 15px rgba(239, 68, 68, 0.4)' : (isSorted ? '0 0 12px rgba(16, 185, 129, 0.3)' : 'none'),
                  transition: 'all 0.3s ease'
                }}>
                  {val}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // 13. Merge Sort
  if (algoId === 'merge_sort') {
    const { array, leftHalf, rightHalf, merged } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        <div style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>
          Merge Sort: Divide & Conquer Subarray Halving and Two-Pointer Merging
        </div>

        {leftHalf && rightHalf && (
          <div style={{ display: 'flex', gap: '2rem', justifyContent: 'center' }}>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px', backgroundColor: '#0f172a', padding: '10px 16px', borderRadius: '10px', border: '1px solid #334155' }}>
              <span style={{ fontSize: '0.72rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>Left Subarray</span>
              <div style={{ display: 'flex', gap: '6px' }}>
                {leftHalf.map((v, i) => (
                  <span key={i} style={{ width: '36px', height: '36px', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#1e293b', borderRadius: '6px', fontWeight: 800, color: '#f8fafc' }}>{v}</span>
                ))}
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '6px', backgroundColor: '#0f172a', padding: '10px 16px', borderRadius: '10px', border: '1px solid #334155' }}>
              <span style={{ fontSize: '0.72rem', color: '#c084fc', fontWeight: 700 }}>Right Subarray</span>
              <div style={{ display: 'flex', gap: '6px' }}>
                {rightHalf.map((v, i) => (
                  <span key={i} style={{ width: '36px', height: '36px', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#1e293b', borderRadius: '6px', fontWeight: 800, color: '#f8fafc' }}>{v}</span>
                ))}
              </div>
            </div>
          </div>
        )}

        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', justifyContent: 'center' }}>
          {(array || [3, 27, 38, 43]).map((val, idx) => (
            <div key={idx} style={{
              width: '52px',
              height: '52px',
              borderRadius: '10px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 800,
              fontSize: '1.1rem',
              backgroundColor: merged ? 'rgba(16, 185, 129, 0.2)' : '#1E293B',
              border: merged ? '2px solid #10b981' : '1px solid #334155',
              color: merged ? '#6ee7b7' : '#f8fafc',
              boxShadow: merged ? '0 0 15px rgba(16, 185, 129, 0.3)' : 'none',
              transition: 'all 0.3s ease'
            }}>
              {val}
            </div>
          ))}
        </div>
      </div>
    );
  }

  // 14. Dijkstra
  if (algoId === 'dijkstra') {
    const { nodes, distances, currentNode, visited } = step.data || {};
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '1.5rem', width: '100%' }}>
        <div style={{ fontSize: '0.78rem', color: 'var(--accent-cyan)', fontWeight: 700 }}>
          Dijkstra Shortest Path: Greedy Priority Queue Edge Relaxation
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(90px, 1fr))', gap: '12px', width: '100%', maxWidth: '480px' }}>
          {(nodes || ['A', 'B', 'C', 'D']).map((node) => {
            const isCur = currentNode === node;
            const isVis = visited?.includes(node);
            const dist = distances?.[node] ?? '∞';

            return (
              <div key={node} style={{
                backgroundColor: isCur ? 'rgba(56, 189, 248, 0.2)' : (isVis ? 'rgba(16, 185, 129, 0.15)' : '#0f172a'),
                border: isCur ? '2px solid var(--accent-cyan)' : (isVis ? '1px solid #10b981' : '1px solid #334155'),
                borderRadius: '10px',
                padding: '10px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                gap: '4px'
              }}>
                <span style={{ fontSize: '0.8rem', fontWeight: 800, color: '#f8fafc' }}>Node {node}</span>
                <span style={{ fontSize: '1rem', fontWeight: 800, color: isCur ? 'var(--accent-cyan)' : (isVis ? '#10b981' : '#94a3b8') }}>
                  dist: {dist}
                </span>
                <span style={{ fontSize: '0.65rem', color: isCur ? 'var(--accent-cyan)' : (isVis ? '#10b981' : '#64748b'), fontWeight: 700 }}>
                  {isCur ? 'PROCESSING' : (isVis ? 'VISITED' : 'QUEUED')}
                </span>
              </div>
            );
          })}
        </div>
      </div>
    );
  }

  // Default Fallback
  return (
    <div style={{ textAlign: 'center', color: '#94A3B8' }}>
      <Sparkles size={36} style={{ color: '#38BDF8', marginBottom: '0.5rem' }} />
      <div style={{ fontSize: '0.92rem', color: '#F8FAFC', fontWeight: 700 }}>
        Interactive Algorithm Visualization Active
      </div>
    </div>
  );
}

// ==============================================================
// STEP-BY-STEP TEACHING TRACES FOR ALL 10 ALGORITHMS
// ==============================================================
function getTeachingSteps(algoId) {
  // 1. Array Traversal
  if (algoId === 'array_traversal') {
    const arr = [10, 25, 42, 68, 91];
    return [
      {
        stageTitle: 'Step 1: Physical RAM Address Allocation',
        phaseName: 'Base Address Setup',
        isKeyOperation: false,
        data: { array: arr, activeIndex: -1, baseAddress: 0x1000 },
        teacherExplanation: 'An array requires a single contiguous block of physical RAM. Our 5-element integer array is allocated at base address 0x1000. Each 32-bit int occupies exactly 4 bytes.',
        whyDidThisHappen: 'Contiguity allows random access: the computer does not need to walk through elements—it calculates the exact memory location with simple multiplication.',
        activeCodeLine: 1,
        variables: { baseAddress: '0x1000', elementSize: '4 bytes', length: 5 },
        stateChangeNote: 'Physical memory reserved: [0x1000 to 0x1013].'
      },
      {
        stageTitle: 'Step 2: Read Index [0] at Base Address',
        phaseName: 'O(1) Direct Access',
        isKeyOperation: true,
        data: { array: arr, activeIndex: 0, baseAddress: 0x1000 },
        teacherExplanation: 'We access arr[0]. Memory address = 0x1000 + (0 * 4) = 0x1000. The CPU reads 10 in O(1) time without searching.',
        whyDidThisHappen: 'Multiplying by zero means index 0 is located exactly at the base memory pointer.',
        activeCodeLine: 3,
        variables: { index: 0, address: '0x1000', value: 10 },
        stateChangeNote: 'Read arr[0] = 10 from 0x1000.'
      },
      {
        stageTitle: 'Step 3: Linear Pointer Traversal to Index [2]',
        phaseName: 'Sequential Access',
        isKeyOperation: false,
        data: { array: arr, activeIndex: 2, baseAddress: 0x1000 },
        teacherExplanation: 'Moving to index 2: Address = 0x1000 + (2 * 4) = 0x1008. The CPU hardware cache pre-fetches the entire block into L1 cache for maximum speed.',
        whyDidThisHappen: 'Spatial locality: contiguous memory blocks load together into cache lines.',
        activeCodeLine: 4,
        variables: { index: 2, address: '0x1008', value: 42 },
        stateChangeNote: 'Access arr[2] = 42.'
      },
      {
        stageTitle: 'Step 4: Traversal Complete',
        phaseName: 'Finished Scan',
        isKeyOperation: true,
        data: { array: arr, activeIndex: 4, baseAddress: 0x1000 },
        teacherExplanation: 'Finished scanning all 5 elements. Total time complexity is O(N) for visiting all items, with O(1) lookup per item.',
        whyDidThisHappen: 'Loop reached array length termination condition.',
        activeCodeLine: 5,
        variables: { totalVisited: 5, totalBytesRead: 20 },
        stateChangeNote: 'All 5 elements accessed successfully.'
      }
    ];
  }

  // 2. Binary Search
  if (algoId === 'binary_search') {
    const arr = [4, 9, 15, 23, 38, 45, 56, 72, 88, 99];
    const target = 56;
    return [
      {
        stageTitle: 'Step 1: Problem Setup & Invariant Declaration',
        phaseName: 'Initial Interval',
        isKeyOperation: false,
        data: { array: arr, low: 0, high: 9, mid: -1, target, found: false },
        teacherExplanation: `We need to find target ${target} inside a sorted array of 10 items. We set low = 0 and high = 9.`,
        whyDidThisHappen: 'Binary search requires sorted data. Monotonic order allows discarding half the data per comparison.',
        activeCodeLine: 2,
        variables: { low: 0, high: 9, target: 56, remainingRange: '10 elements' },
        stateChangeNote: 'Search space: [0..9].'
      },
      {
        stageTitle: 'Step 2: Inspect Midpoint arr[4]',
        phaseName: 'First Division',
        isKeyOperation: true,
        data: { array: arr, low: 0, high: 9, mid: 4, target, found: false },
        teacherExplanation: 'Mid = (0 + 9) / 2 = 4. arr[4] is 38. Since 38 < 56, target must be in the right half!',
        whyDidThisHappen: 'All values at or before index 4 are <= 38, so 56 cannot exist on the left.',
        activeCodeLine: 4,
        variables: { mid: 4, 'arr[mid]': 38, target: 56 },
        stateChangeNote: 'Discard indices [0..4]. Update low = 5.'
      },
      {
        stageTitle: 'Step 3: Inspect Midpoint arr[7]',
        phaseName: 'Second Division',
        isKeyOperation: true,
        data: { array: arr, low: 5, high: 9, mid: 7, target, found: false },
        teacherExplanation: 'In range [5..9], mid = (5 + 9) / 2 = 7. arr[7] is 72. Since 72 > 56, target must be in the left half of this window!',
        whyDidThisHappen: 'Values at index 7 and beyond are >= 72.',
        activeCodeLine: 8,
        variables: { mid: 7, 'arr[mid]': 72, target: 56 },
        stateChangeNote: 'Discard indices [7..9]. Update high = 6.'
      },
      {
        stageTitle: 'Step 4: Target Found at arr[6]!',
        phaseName: 'Target Match',
        isKeyOperation: true,
        data: { array: arr, low: 5, high: 6, mid: 6, target, found: true },
        teacherExplanation: 'Mid = 6. Value at arr[6] is 56! 56 == target (56). Found in only 3 comparisons!',
        whyDidThisHappen: 'Target matched arr[mid] exactly. Returns index 6.',
        activeCodeLine: 6,
        variables: { resultIndex: 6, target: 56, totalComparisons: 3 },
        stateChangeNote: 'Target 56 confirmed at index [6] in O(log N)!'
      }
    ];
  }

  // 3. Bubble Sort
  if (algoId === 'bubble_sort') {
    return [
      {
        stageTitle: 'Step 1: Initial Unsorted Array',
        phaseName: 'Setup',
        isKeyOperation: false,
        data: { array: [42, 15, 88, 23, 6], comparing: [], swapped: [], sorted: [] },
        teacherExplanation: 'Bubble Sort checks adjacent pairs and swaps them if the left element is larger than the right.',
        whyDidThisHappen: 'Starting pass 1 of bubble sort.',
        activeCodeLine: 2,
        variables: { pass: 1, i: 0, j: 0 },
        stateChangeNote: 'Unsorted array loaded.'
      },
      {
        stageTitle: 'Step 2: Compare 42 and 15 (Out of Order)',
        phaseName: 'Comparing',
        isKeyOperation: true,
        data: { array: [42, 15, 88, 23, 6], comparing: [0, 1], swapped: [], sorted: [] },
        teacherExplanation: 'Compare arr[0] (42) and arr[1] (15). Since 42 > 15, they are out of order and must be swapped!',
        whyDidThisHappen: 'Ascending order requires smaller values first.',
        activeCodeLine: 4,
        variables: { 'arr[0]': 42, 'arr[1]': 15, condition: '42 > 15 (true)' },
        stateChangeNote: 'Inversion detected between index 0 and 1.'
      },
      {
        stageTitle: 'Step 3: Swap 42 and 15',
        phaseName: 'Swap',
        isKeyOperation: false,
        data: { array: [15, 42, 88, 23, 6], comparing: [], swapped: [0, 1], sorted: [] },
        teacherExplanation: '15 and 42 have traded places. Array is now [15, 42, 88, 23, 6].',
        whyDidThisHappen: 'Swapping fixes the local inversion.',
        activeCodeLine: 5,
        variables: { 'arr[0]': 15, 'arr[1]': 42, didSwap: true },
        stateChangeNote: 'Indices [0, 1] swapped.'
      },
      {
        stageTitle: 'Step 4: Lock Heaviest Element (88)',
        phaseName: 'Pass Complete',
        isKeyOperation: true,
        data: { array: [15, 42, 23, 6, 88], comparing: [], swapped: [], sorted: [4] },
        teacherExplanation: 'At the end of pass 1, the largest item (88) has bubbled up all the way to index 4. It is now locked!',
        whyDidThisHappen: 'The maximum value always reaches the end after pass 1.',
        activeCodeLine: 8,
        variables: { lockedElement: 88, sortedCount: 1 },
        stateChangeNote: 'Index 4 permanently locked.'
      }
    ];
  }

  // 4. Linked List
  if (algoId === 'linked_list') {
    return [
      {
        stageTitle: 'Step 1: Head Pointer Setup',
        phaseName: 'Head Node',
        isKeyOperation: false,
        data: { nodes: [{ val: 12 }, { val: 99 }, { val: 37 }], currIndex: 0 },
        teacherExplanation: 'A Linked List starts with a HEAD pointer referencing the first node (12). Nodes are connected by reference addresses.',
        whyDidThisHappen: 'Linked lists do not require contiguous memory blocks.',
        activeCodeLine: 1,
        variables: { head: 12, curr: 12 },
        stateChangeNote: 'Current points to Head (Node 0).'
      },
      {
        stageTitle: 'Step 2: Traverse to Next Node (99)',
        phaseName: 'Pointer Move',
        isKeyOperation: true,
        data: { nodes: [{ val: 12 }, { val: 99 }, { val: 37 }], currIndex: 1 },
        teacherExplanation: 'We follow current.next to reach Node 1 (99). To read the k-th node, we must visit all preceding nodes (O(N)).',
        whyDidThisHappen: 'No arithmetic address indexing is possible in linked nodes.',
        activeCodeLine: 3,
        variables: { curr: 99, next: 37 },
        stateChangeNote: 'Current advanced to Node 1.'
      },
      {
        stageTitle: 'Step 3: Reach Last Node (37) -> NULL',
        phaseName: 'Tail Node',
        isKeyOperation: true,
        data: { nodes: [{ val: 12 }, { val: 99 }, { val: 37 }], currIndex: 2 },
        teacherExplanation: 'Node 2 points to NULL. This indicates the end (tail) of the singly linked list.',
        whyDidThisHappen: 'The next pointer of the final node is null.',
        activeCodeLine: 5,
        variables: { curr: 37, next: 'NULL' },
        stateChangeNote: 'Reached end of linked list.'
      }
    ];
  }

  // 5. Stack (LIFO)
  if (algoId === 'stack_lifo') {
    return [
      {
        stageTitle: 'Step 1: Push(10) onto Empty Stack',
        phaseName: 'Push 10',
        isKeyOperation: false,
        data: { stackItems: [10], topElement: 10, action: 'push(10)' },
        teacherExplanation: '10 is pushed into the stack. TOP pointer now points to 10.',
        whyDidThisHappen: 'Stack pushes elements to the top of the collection.',
        activeCodeLine: 2,
        variables: { top: 10, size: 1 },
        stateChangeNote: 'Pushed 10.'
      },
      {
        stageTitle: 'Step 2: Push(25) and Push(42)',
        phaseName: 'Push 42',
        isKeyOperation: false,
        data: { stackItems: [10, 25, 42], topElement: 42, action: 'push(42)' },
        teacherExplanation: '25 and 42 are pushed. 42 is now the TOP element. Elements below cannot be accessed directly.',
        whyDidThisHappen: 'LIFO rule: Last-In, First-Out.',
        activeCodeLine: 3,
        variables: { top: 42, size: 3 },
        stateChangeNote: 'Stack size is now 3.'
      },
      {
        stageTitle: 'Step 3: Pop() Removes Top Item (42)',
        phaseName: 'Pop Action',
        isKeyOperation: true,
        data: { stackItems: [10, 25], topElement: 25, action: 'pop() -> returns 42' },
        teacherExplanation: 'Calling pop() removes the most recently added item (42). TOP automatically points down to 25.',
        whyDidThisHappen: 'Popping always removes the element at the TOP in O(1) time.',
        activeCodeLine: 5,
        variables: { popped: 42, newTop: 25, size: 2 },
        stateChangeNote: '42 removed. Top is now 25.'
      }
    ];
  }

  // 6. Queue (FIFO)
  if (algoId === 'queue_fifo') {
    return [
      {
        stageTitle: 'Step 1: Enqueue(10) at Rear',
        phaseName: 'Enqueue 10',
        isKeyOperation: false,
        data: { queueItems: [10], action: 'enqueue(10)' },
        teacherExplanation: '10 enters the queue. It is currently both FRONT and REAR.',
        whyDidThisHappen: 'First element in an empty queue.',
        activeCodeLine: 2,
        variables: { front: 10, rear: 10, size: 1 },
        stateChangeNote: 'Queue initialized with 10.'
      },
      {
        stageTitle: 'Step 2: Enqueue(25) and Enqueue(42)',
        phaseName: 'Enqueue at Rear',
        isKeyOperation: false,
        data: { queueItems: [10, 25, 42], action: 'enqueue(42)' },
        teacherExplanation: '25 and 42 join at the REAR. 10 remains at the FRONT.',
        whyDidThisHappen: 'FIFO ensures newcomers wait their turn behind existing elements.',
        activeCodeLine: 3,
        variables: { front: 10, rear: 42, size: 3 },
        stateChangeNote: 'Queue size is 3.'
      },
      {
        stageTitle: 'Step 3: Dequeue() Removes 10 from Front',
        phaseName: 'Dequeue from Front',
        isKeyOperation: true,
        data: { queueItems: [25, 42], action: 'dequeue() -> returns 10' },
        teacherExplanation: 'dequeue() removes 10 from the FRONT. 25 becomes the new FRONT element.',
        whyDidThisHappen: 'First item added (10) is the first item removed (FIFO).',
        activeCodeLine: 5,
        variables: { dequeued: 10, newFront: 25, size: 2 },
        stateChangeNote: '10 served and dequeued.'
      }
    ];
  }

  // 7. Binary Tree Traversal
  if (algoId === 'tree_traversal') {
    return [
      {
        stageTitle: 'Step 1: Root Node (40) - Recurse Left',
        phaseName: 'Start at Root',
        isKeyOperation: false,
        data: { activeNode: 40, visitedNodes: [], traversalOrder: [] },
        teacherExplanation: 'In-Order Traversal rule: Left Subtree → Root → Right Subtree. From Root 40, we must first visit the entire Left subtree.',
        whyDidThisHappen: 'In-order requires processing all left descendants before the parent.',
        activeCodeLine: 2,
        variables: { currNode: 40, nextAction: 'Go to Left Child (20)' },
        stateChangeNote: 'Recursion pushes 40, moves to 20.'
      },
      {
        stageTitle: 'Step 2: Visit Leftmost Leaf Node (10)',
        phaseName: 'Visit Leftmost',
        isKeyOperation: true,
        data: { activeNode: 10, visitedNodes: [10], traversalOrder: [10] },
        teacherExplanation: 'Node 10 has no left child. So we process 10 and add it to our output list: [10].',
        whyDidThisHappen: 'Left leaf has no left descendants.',
        activeCodeLine: 3,
        variables: { visited: 10, output: '[10]' },
        stateChangeNote: '10 added to in-order output.'
      },
      {
        stageTitle: 'Step 3: Visit Parent (20) & Right Leaf (30)',
        phaseName: 'Process Subtree',
        isKeyOperation: false,
        data: { activeNode: 30, visitedNodes: [10, 20, 30], traversalOrder: [10, 20, 30] },
        teacherExplanation: 'We visit 20, then its right child 30. Left subtree is now complete! Output: [10, 20, 30].',
        whyDidThisHappen: 'Left, Root, Right order followed for node 20.',
        activeCodeLine: 4,
        variables: { leftSubtreeDone: true, output: '[10, 20, 30]' },
        stateChangeNote: 'Left subtree completed in sorted order.'
      },
      {
        stageTitle: 'Step 4: Visit Root (40) & Finish Traversal',
        phaseName: 'Complete In-Order',
        isKeyOperation: true,
        data: { activeNode: 40, visitedNodes: [10, 20, 30, 40, 50, 60, 70], traversalOrder: [10, 20, 30, 40, 50, 60, 70] },
        teacherExplanation: 'Now we visit 40, then traverse the right subtree (50, 60, 70). Output is in perfectly sorted order!',
        whyDidThisHappen: 'In-order traversal on a BST always produces non-decreasing sorted order.',
        activeCodeLine: 5,
        variables: { totalNodes: 7, finalOutput: '[10, 20, 30, 40, 50, 60, 70]' },
        stateChangeNote: 'Tree traversal fully completed in O(N) time.'
      }
    ];
  }

  // 8. Graph BFS
  if (algoId === 'graph_bfs') {
    return [
      {
        stageTitle: 'Step 1: Start BFS at Source Vertex A',
        phaseName: 'Source Vertex',
        isKeyOperation: false,
        data: { activeVertex: 'A', visitedSet: ['A'], queue: ['A'] },
        teacherExplanation: 'We initialize BFS at vertex A. A is marked visited and enqueued into the Frontier Queue.',
        whyDidThisHappen: 'BFS requires a FIFO queue to explore vertices layer-by-layer.',
        activeCodeLine: 2,
        variables: { source: 'A', queue: '["A"]', visitedCount: 1 },
        stateChangeNote: 'A enqueued.'
      },
      {
        stageTitle: 'Step 2: Dequeue A, Enqueue Neighbors B & C',
        phaseName: 'Layer 1 Neighbors',
        isKeyOperation: true,
        data: { activeVertex: 'A', visitedSet: ['A', 'B', 'C'], queue: ['B', 'C'] },
        teacherExplanation: 'Dequeue A. Inspect adjacent edges: B and C are unvisited. We mark them visited and enqueue [B, C].',
        whyDidThisHappen: 'All immediate distance-1 neighbors are discovered in layer 1.',
        activeCodeLine: 4,
        variables: { current: 'A', discovered: 'B, C', queue: '["B", "C"]' },
        stateChangeNote: 'B and C discovered.'
      },
      {
        stageTitle: 'Step 3: Explore Layer 2 (Vertices D & E)',
        phaseName: 'Layer 2 Exploration',
        isKeyOperation: true,
        data: { activeVertex: 'B', visitedSet: ['A', 'B', 'C', 'D', 'E'], queue: ['C', 'D', 'E'] },
        teacherExplanation: 'Dequeue B: discovers D. Dequeue C: discovers E. All 5 vertices reached with shortest path distances!',
        whyDidThisHappen: 'BFS guarantees minimum edge distance to all reachable vertices.',
        activeCodeLine: 6,
        variables: { totalVisited: 5, status: 'All connected vertices visited' },
        stateChangeNote: 'Graph BFS completed in O(V + E) time.'
      }
    ];
  }

  // 9. Recursion Call Stack
  if (algoId === 'recursion_callstack') {
    return [
      {
        stageTitle: 'Step 1: Initial Call factorial(4)',
        phaseName: 'Push Frame 1',
        isKeyOperation: false,
        data: { stackFrames: [{ name: 'factorial(4)', n: 4 }], phase: 'Winding Call Stack' },
        teacherExplanation: 'We invoke factorial(4). A new activation stack frame is pushed onto the JVM Call Stack.',
        whyDidThisHappen: 'Every function invocation allocates a stack frame storing arguments and local variables.',
        activeCodeLine: 1,
        variables: { call: 'factorial(4)', n: 4, stackDepth: 1 },
        stateChangeNote: 'Pushed frame for n = 4.'
      },
      {
        stageTitle: 'Step 2: Recursive Deepening (n = 3, 2, 1)',
        phaseName: 'Max Call Depth',
        isKeyOperation: true,
        data: { 
          stackFrames: [
            { name: 'factorial(4)', n: 4 },
            { name: 'factorial(3)', n: 3 },
            { name: 'factorial(2)', n: 2 },
            { name: 'factorial(1)', n: 1 }
          ], 
          phase: 'Base Case Reached' 
        },
        teacherExplanation: 'factorial(4) calls 3, which calls 2, which calls 1. At n = 1, base case triggers: return 1!',
        whyDidThisHappen: 'Base case stops infinite recursive loops.',
        activeCodeLine: 2,
        variables: { current: 'factorial(1)', baseCaseTriggered: true, stackDepth: 4 },
        stateChangeNote: 'Stack at maximum depth 4.'
      },
      {
        stageTitle: 'Step 3: Unwinding & Returning 24',
        phaseName: 'Stack Unwinding',
        isKeyOperation: true,
        data: { 
          stackFrames: [
            { name: 'factorial(4)', n: 4, retVal: 24 }
          ], 
          phase: 'All Frames Popped' 
        },
        teacherExplanation: 'Frames pop in reverse order: 1*2=2, 2*3=6, 6*4=24. Final result 24 returned in O(N) time.',
        whyDidThisHappen: 'Parent functions resume execution using child return values.',
        activeCodeLine: 4,
        variables: { finalResult: 24, stackDepth: 0 },
        stateChangeNote: 'Returned 24. Stack cleared.'
      }
    ];
  }

  // 10. Dynamic Programming Tabulation
  if (algoId === 'dp_fibonacci') {
    return [
      {
        stageTitle: 'Step 1: Base Case Initialization dp[0] & dp[1]',
        phaseName: 'Base Cases',
        isKeyOperation: false,
        data: { dpTable: [0, 1, null, null, null, null, null], activeIndex: null, formula: 'dp[0] = 0, dp[1] = 1' },
        teacherExplanation: 'We allocate a 1D DP array of size 7. Base cases: dp[0] = 0 and dp[1] = 1.',
        whyDidThisHappen: 'Tabulation starts from the smallest base subproblems.',
        activeCodeLine: 2,
        variables: { 'dp[0]': 0, 'dp[1]': 1, target: 'dp[6]' },
        stateChangeNote: 'Base cases populated in table.'
      },
      {
        stageTitle: 'Step 2: Compute dp[2] = dp[1] + dp[0]',
        phaseName: 'First Subproblem',
        isKeyOperation: true,
        data: { dpTable: [0, 1, 1, null, null, null, null], activeIndex: 2, formula: 'dp[2] = 1 + 0 = 1' },
        teacherExplanation: 'dp[2] = dp[1] + dp[0] = 1 + 0 = 1. We look up previous cells in O(1) time without re-computing.',
        whyDidThisHappen: 'Overlapping subproblems are resolved using table memoization.',
        activeCodeLine: 4,
        variables: { i: 2, 'dp[i]': 1 },
        stateChangeNote: 'dp[2] calculated.'
      },
      {
        stageTitle: 'Step 3: Linear Table Completion up to dp[6] = 8',
        phaseName: 'Table Complete',
        isKeyOperation: true,
        data: { dpTable: [0, 1, 1, 2, 3, 5, 8], activeIndex: 6, formula: 'dp[6] = dp[5] + dp[4] = 5 + 3 = 8' },
        teacherExplanation: 'We fill the table linearly: 0, 1, 1, 2, 3, 5, 8. Solved in O(N) operations instead of O(2ⁿ)!',
        whyDidThisHappen: 'Dynamic Programming converts exponential recursion into linear iteration.',
        activeCodeLine: 5,
        variables: { result: 8, complexity: 'O(N) Time, O(N) Space' },
        stateChangeNote: 'Fibonacci(6) = 8 computed with 0 redundant operations.'
      }
    ];
  }

  // 11. Linear Search
  if (algoId === 'linear_search') {
    const arr = [18, 42, 7, 95, 33, 61];
    return [
      {
        stageTitle: 'Step 1: Inspect Index 0',
        phaseName: 'Sequential Scan',
        isKeyOperation: false,
        data: { array: arr, activeIndex: 0, target: 95, found: false },
        teacherExplanation: 'Linear Search inspects elements one by one. arr[0] is 18. Target is 95. No match, move forward.',
        whyDidThisHappen: 'On unsorted data, every element must be checked sequentially until target is found or list ends.',
        activeCodeLine: 2,
        variables: { i: 0, 'arr[0]': 18, target: 95, match: false },
        stateChangeNote: 'Index 0 checked (18 != 95). Pointer advances.'
      },
      {
        stageTitle: 'Step 2: Inspect Index 1 & 2',
        phaseName: 'Advancing Pointer',
        isKeyOperation: false,
        data: { array: arr, activeIndex: 2, target: 95, found: false },
        teacherExplanation: 'Indices 1 (42) and 2 (7) do not match target 95. The pointer continues advancing rightward.',
        whyDidThisHappen: 'Linear scan continues sequentially.',
        activeCodeLine: 2,
        variables: { i: 2, 'arr[2]': 7, target: 95, match: false },
        stateChangeNote: 'Index 2 checked (7 != 95).'
      },
      {
        stageTitle: 'Step 3: Target Match Found at Index 3!',
        phaseName: 'Target Found',
        isKeyOperation: true,
        data: { array: arr, activeIndex: 3, target: 95, found: true },
        teacherExplanation: 'BINGO! arr[3] == 95 matches our search target! Return index 3 immediately in O(k) steps.',
        whyDidThisHappen: 'Early exit invariant: return as soon as the target is found without scanning remaining items.',
        activeCodeLine: 3,
        variables: { i: 3, 'arr[3]': 95, target: 95, match: true, returnIndex: 3 },
        stateChangeNote: 'Target 95 located at index 3. Linear Search terminates successfully.'
      }
    ];
  }

  // 12. Selection Sort
  if (algoId === 'selection_sort') {
    return [
      {
        stageTitle: 'Pass 1: Find Smallest Element in Entire Array',
        phaseName: 'Min Scan',
        isKeyOperation: false,
        data: { array: [29, 10, 14, 37, 13], currentIdx: 0, minIdx: 1, sortedBoundary: 0 },
        teacherExplanation: 'Selection Sort scans the unsorted segment to find the minimum value. Here, 10 at index 1 is the global minimum.',
        whyDidThisHappen: 'Selection sort finds the smallest unsorted element to place it at the sorted boundary.',
        activeCodeLine: 3,
        variables: { i: 0, minIdx: 1, currentMin: 10 },
        stateChangeNote: '10 identified as current minimum in unsorted array.'
      },
      {
        stageTitle: 'Pass 1 Swap: Place 10 at Index 0',
        phaseName: 'Swap Minimum',
        isKeyOperation: true,
        data: { array: [10, 29, 14, 37, 13], currentIdx: 0, minIdx: 0, sortedBoundary: 1 },
        teacherExplanation: 'Swap arr[0] (29) with minimum arr[1] (10). Index 0 is now sorted permanently.',
        whyDidThisHappen: 'Loop invariant: after pass i, the first i + 1 elements are sorted.',
        activeCodeLine: 5,
        variables: { swapped: '29 <-> 10', sortedUntil: 0 },
        stateChangeNote: '10 locked at index 0.'
      },
      {
        stageTitle: 'Pass 2 Swap: Place 13 at Index 1',
        phaseName: 'Next Minimum',
        isKeyOperation: false,
        data: { array: [10, 13, 14, 37, 29], currentIdx: 1, minIdx: 1, sortedBoundary: 2 },
        teacherExplanation: 'Smallest in remaining [29, 14, 37, 13] is 13 at index 4. Swap 13 into index 1.',
        whyDidThisHappen: 'Next smallest element placed into position 1.',
        activeCodeLine: 5,
        variables: { i: 1, minIdx: 4, currentMin: 13 },
        stateChangeNote: '13 locked at index 1.'
      },
      {
        stageTitle: 'Array Completely Sorted: [10, 13, 14, 29, 37]',
        phaseName: 'Sorted Complete',
        isKeyOperation: true,
        data: { array: [10, 13, 14, 29, 37], currentIdx: 4, minIdx: 4, sortedBoundary: 5 },
        teacherExplanation: 'All passes complete! Array is sorted in O(N²) comparisons with only O(N) swaps.',
        whyDidThisHappen: 'All elements sorted.',
        activeCodeLine: 6,
        variables: { complete: true, totalSwaps: 4 },
        stateChangeNote: 'Selection Sort completed successfully.'
      }
    ];
  }

  // 13. Merge Sort
  if (algoId === 'merge_sort') {
    return [
      {
        stageTitle: 'Divide: Split Array [38, 27, 43, 3] into Halves',
        phaseName: 'Divide Phase',
        isKeyOperation: false,
        data: { array: [38, 27, 43, 3], leftHalf: [38, 27], rightHalf: [43, 3] },
        teacherExplanation: 'Merge Sort uses Divide & Conquer. We divide the array recursively at mid index until single-element subarrays are reached.',
        whyDidThisHappen: 'A single element array is trivially sorted by definition.',
        activeCodeLine: 2,
        variables: { mid: 2, leftSize: 2, rightSize: 2 },
        stateChangeNote: 'Array divided into left [38, 27] and right [43, 3].'
      },
      {
        stageTitle: 'Conquer: Merge Sorted Halves [27, 38] and [3, 43]',
        phaseName: 'Two-Pointer Merge',
        isKeyOperation: true,
        data: { array: [3, 27, 38, 43], merged: true },
        teacherExplanation: 'Compare pointers at the head of each sorted half: 3 < 27, so 3 comes first, then 27, then 38, then 43. Clean linear O(N) merge step!',
        whyDidThisHappen: 'Merging two pre-sorted arrays takes only linear O(N) time with two pointers.',
        activeCodeLine: 5,
        variables: { sorted: '[3, 27, 38, 43]', complexity: 'O(N log N) Guaranteed' },
        stateChangeNote: 'Merged array successfully in guaranteed O(N log N) time.'
      }
    ];
  }

  // 14. Dijkstra
  if (algoId === 'dijkstra') {
    return [
      {
        stageTitle: 'Step 1: Initialize Distance Table from Source A',
        phaseName: 'Init Distances',
        isKeyOperation: false,
        data: {
          nodes: ['A', 'B', 'C', 'D'],
          distances: { A: 0, B: '∞', C: '∞', D: '∞' },
          currentNode: 'A',
          visited: ['A']
        },
        teacherExplanation: "Dijkstra's algorithm finds shortest paths from source vertex A. Distance to source is 0; all other nodes start at infinity (∞).",
        whyDidThisHappen: 'Greedy choice property: start from known zero distance and relax reachable edges.',
        activeCodeLine: 2,
        variables: { source: 'A', 'dist[A]': 0, 'dist[B]': '∞' },
        stateChangeNote: 'Source A initialized with dist=0.'
      },
      {
        stageTitle: 'Step 2: Relax Neighbors of A (Edges A->B: 4, A->C: 2)',
        phaseName: 'Edge Relaxation',
        isKeyOperation: true,
        data: {
          nodes: ['A', 'B', 'C', 'D'],
          distances: { A: 0, B: 4, C: 2, D: '∞' },
          currentNode: 'C',
          visited: ['A', 'C']
        },
        teacherExplanation: 'Edge relaxation: dist[A] + 2 < dist[C] (0 + 2 < ∞), so dist[C] becomes 2. Similarly dist[B] becomes 4. Node C has minimum distance (2), so it is extracted next from the priority queue.',
        whyDidThisHappen: 'Greedy step: always process the unvisited vertex with the smallest tentative distance.',
        activeCodeLine: 4,
        variables: { 'dist[C]': 2, 'dist[B]': 4, nextExtract: 'C' },
        stateChangeNote: 'Relaxed edges to B and C. Extracted C (dist=2).'
      },
      {
        stageTitle: 'Step 3: Relax Neighbors of C to reach D (Edge C->D: 3)',
        phaseName: 'Path to Target',
        isKeyOperation: true,
        data: {
          nodes: ['A', 'B', 'C', 'D'],
          distances: { A: 0, B: 4, C: 2, D: 5 },
          currentNode: 'D',
          visited: ['A', 'C', 'D', 'B']
        },
        teacherExplanation: 'From C (dist 2), edge C->D costs 3. Tentative dist[D] = 2 + 3 = 5. All shortest paths finalized: A->0, C->2, B->4, D->5.',
        whyDidThisHappen: 'Optimal substructure: shortest path to D builds upon shortest path to C.',
        activeCodeLine: 6,
        variables: { 'dist[D]': 5, shortestRoute: 'A -> C -> D (Cost 5)' },
        stateChangeNote: "Dijkstra's algorithm finalized optimal shortest path costs."
      }
    ];
  }

  // Safe Fallback (Never return empty array so currentStep is never undefined)
  return [
    {
      stageTitle: 'Algorithm Simulation Initialized',
      phaseName: 'Initialization',
      isKeyOperation: false,
      data: { array: [10, 20, 30, 40, 50], activeIndex: 0 },
      teacherExplanation: 'Visualizer initialized for this algorithm concept.',
      whyDidThisHappen: 'Setup invariant established.',
      activeCodeLine: 1,
      variables: { status: 'Ready' },
      stateChangeNote: 'Simulation ready.'
    }
  ];
}

// ==============================================================
// SYNCHRONIZED CODE IMPLEMENTATIONS (JAVA & PYTHON)
// ==============================================================
function getCodeLines(algoId, lang) {
  if (algoId === 'array_traversal') {
    return lang === 'java' ? [
      'public void traverseArray(int[] arr) {',
      '    int base = 0x1000;',
      '    for (int i = 0; i < arr.length; i++) {',
      '        int address = base + (i * 4); // O(1) offset',
      '        System.out.println("arr[" + i + "] = " + arr[i]);',
      '    }',
      '}'
    ] : [
      'def traverse_array(arr):',
      '    for i in range(len(arr)):',
      '        # O(1) contiguous RAM access',
      '        print(f"arr[{i}] = {arr[i]}")'
    ];
  }

  if (algoId === 'binary_search') {
    return lang === 'java' ? [
      'public int binarySearch(int[] arr, int target) {',
      '    int low = 0, high = arr.length - 1;',
      '    while (low <= high) {',
      '        int mid = low + (high - low) / 2;',
      '        if (arr[mid] == target) return mid;',
      '        else if (arr[mid] < target) low = mid + 1;',
      '        else high = mid - 1;',
      '    }',
      '    return -1;',
      '}'
    ] : [
      'def binary_search(arr, target):',
      '    low, high = 0, len(arr) - 1',
      '    while low <= high:',
      '        mid = (low + high) // 2',
      '        if arr[mid] == target: return mid',
      '        elif arr[mid] < target: low = mid + 1',
      '        else: high = mid - 1',
      '    return -1'
    ];
  }

  if (algoId === 'bubble_sort') {
    return lang === 'java' ? [
      'public void bubbleSort(int[] arr) {',
      '    int n = arr.length;',
      '    for (int i = 0; i < n - 1; i++) {',
      '        for (int j = 0; j < n - i - 1; j++) {',
      '            if (arr[j] > arr[j + 1]) {',
      '                int temp = arr[j];',
      '                arr[j] = arr[j + 1];',
      '                arr[j + 1] = temp;',
      '            }',
      '        }',
      '    }',
      '}'
    ] : [
      'def bubble_sort(arr):',
      '    n = len(arr)',
      '    for i in range(n - 1):',
      '        for j in range(n - i - 1):',
      '            if arr[j] > arr[j + 1]:',
      '                arr[j], arr[j + 1] = arr[j + 1], arr[j]'
    ];
  }

  if (algoId === 'tree_traversal') {
    return lang === 'java' ? [
      'public void inOrder(TreeNode root) {',
      '    if (root == null) return;',
      '    inOrder(root.left);  // 1. Traverse left',
      '    visit(root.val);     // 2. Process node',
      '    inOrder(root.right); // 3. Traverse right',
      '}'
    ] : [
      'def in_order(root):',
      '    if not root: return',
      '    in_order(root.left)',
      '    print(root.val)',
      '    in_order(root.right)'
    ];
  }

  if (algoId === 'graph_bfs') {
    return lang === 'java' ? [
      'public void bfs(int start, List<List<Integer>> adj) {',
      '    Queue<Integer> q = new LinkedList<>();',
      '    boolean[] visited = new boolean[adj.size()];',
      '    visited[start] = true; q.offer(start);',
      '    while (!q.isEmpty()) {',
      '        int curr = q.poll();',
      '        for (int neighbor : adj.get(curr)) {',
      '            if (!visited[neighbor]) {',
      '                visited[neighbor] = true;',
      '                q.offer(neighbor);',
      '            }',
      '        }',
      '    }',
      '}'
    ] : [
      'def bfs(start, adj):',
      '    visited = {start}',
      '    queue = collections.deque([start])',
      '    while queue:',
      '        curr = queue.popleft()',
      '        for neighbor in adj[curr]:',
      '            if neighbor not in visited:',
      '                visited.add(neighbor)',
      '                queue.append(neighbor)'
    ];
  }

  if (algoId === 'recursion_callstack') {
    return lang === 'java' ? [
      'public int factorial(int n) {',
      '    if (n <= 1) return 1; // Base case',
      '    // Winding stack frame',
      '    return n * factorial(n - 1);',
      '}'
    ] : [
      'def factorial(n):',
      '    if n <= 1: return 1  # Base case',
      '    return n * factorial(n - 1)'
    ];
  }

  if (algoId === 'dp_fibonacci') {
    return lang === 'java' ? [
      'public int fib(int n) {',
      '    int[] dp = new int[n + 1];',
      '    dp[0] = 0; dp[1] = 1; // Base cases',
      '    for (int i = 2; i <= n; i++) {',
      '        dp[i] = dp[i - 1] + dp[i - 2];',
      '    }',
      '    return dp[n];',
      '}'
    ] : [
      'def fib(n):',
      '    dp = [0] * (n + 1)',
      '    dp[0], dp[1] = 0, 1',
      '    for i in range(2, n + 1):',
      '        dp[i] = dp[i - 1] + dp[i - 2]',
      '    return dp[n]'
    ];
  }

  if (algoId === 'linear_search') {
    return lang === 'java' ? [
      'public int linearSearch(int[] arr, int target) {',
      '    for (int i = 0; i < arr.length; i++) {',
      '        if (arr[i] == target) {',
      '            return i; // Target found',
      '        }',
      '    }',
      '    return -1; // Not found',
      '}'
    ] : [
      'def linear_search(arr, target):',
      '    for i, val in enumerate(arr):',
      '        if val == target:',
      '            return i',
      '    return -1'
    ];
  }

  if (algoId === 'selection_sort') {
    return lang === 'java' ? [
      'public void selectionSort(int[] arr) {',
      '    for (int i = 0; i < arr.length - 1; i++) {',
      '        int minIdx = i;',
      '        for (int j = i + 1; j < arr.length; j++) {',
      '            if (arr[j] < arr[minIdx]) minIdx = j;',
      '        }',
      '        int temp = arr[i]; arr[i] = arr[minIdx]; arr[minIdx] = temp;',
      '    }',
      '}'
    ] : [
      'def selection_sort(arr):',
      '    for i in range(len(arr)):',
      '        min_idx = i',
      '        for j in range(i + 1, len(arr)):',
      '            if arr[j] < arr[min_idx]: min_idx = j',
      '        arr[i], arr[min_idx] = arr[min_idx], arr[i]'
    ];
  }

  if (algoId === 'merge_sort') {
    return lang === 'java' ? [
      'public void mergeSort(int[] arr, int l, int r) {',
      '    if (l < r) {',
      '        int m = l + (r - l) / 2;',
      '        mergeSort(arr, l, m);',
      '        mergeSort(arr, m + 1, r);',
      '        merge(arr, l, m, r);',
      '    }',
      '}'
    ] : [
      'def merge_sort(arr):',
      '    if len(arr) > 1:',
      '        mid = len(arr) // 2',
      '        L, R = arr[:mid], arr[mid:]',
      '        merge_sort(L); merge_sort(R)',
      '        # Two-pointer merge'
    ];
  }

  if (algoId === 'dijkstra') {
    return lang === 'java' ? [
      'public int[] dijkstra(int[][] graph, int src, int V) {',
      '    int[] dist = new int[V];',
      '    Arrays.fill(dist, Integer.MAX_VALUE);',
      '    dist[src] = 0;',
      '    PriorityQueue<int[]> pq = new PriorityQueue<>((a,b)->a[1]-b[1]);',
      '    pq.offer(new int[]{src, 0});',
      '    return dist;',
      '}'
    ] : [
      'import heapq',
      'def dijkstra(graph, src):',
      '    dist = {node: float("inf") for node in graph}',
      '    dist[src] = 0',
      '    pq = [(0, src)]',
      '    return dist'
    ];
  }

  // Default
  return lang === 'java' ? [
    'public void execute(DataStructure ds) {',
    '    ds.performOperation();',
    '}'
  ] : [
    'def execute(ds):',
    '    ds.perform_operation()'
  ];
}
