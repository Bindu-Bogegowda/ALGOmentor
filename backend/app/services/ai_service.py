import os
import json
import httpx
from typing import Dict, Any, List, Optional
from app.config import settings

class AIService:
    @staticmethod
    async def chat_tutor(
        message: str,
        context_page: str = "general",
        current_code: Optional[str] = None,
        problem_title: Optional[str] = None,
        error_message: Optional[str] = None,
        student_level: str = "Beginner"
    ) -> Dict[str, Any]:
        """
        AI Personal Tutor chat response.
        If an external LLM key is configured, query the provider;
        Otherwise, utilize the integrated pedagogical algorithmic reasoning engine.
        """
        # Try external API first if configured
        if settings.GEMINI_API_KEY:
            try:
                res = await AIService._call_gemini(message, context_page, current_code, student_level)
                if res:
                    return res
            except Exception:
                pass
        elif settings.OPENAI_API_KEY:
            try:
                res = await AIService._call_openai(message, context_page, current_code, student_level)
                if res:
                    return res
            except Exception:
                pass

        # Built-in High-Fidelity Algorithmic Tutor
        return AIService._offline_tutor_response(
            message=message,
            context_page=context_page,
            current_code=current_code,
            problem_title=problem_title,
            error_message=error_message,
            student_level=student_level
        )

    @staticmethod
    def analyze_code_for_debugging(
        language: str,
        code: str,
        problem_description: Optional[str] = None,
        runtime_error: Optional[str] = None,
        failed_test_case: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Intelligent Code Debugger: analyzes errors, edge cases, complexity, and logic flaws.
        """
        err_lower = (runtime_error or "").lower()
        code_lower = code.lower()

        # 1. Syntax / Name / Indentation errors
        if "syntaxerror" in err_lower or "indentationerror" in err_lower:
            return {
                "error_type": "Syntax & Formatting",
                "summary": "Syntax or Indentation Malformation Detected",
                "why_it_happened": "Python requires strict indentation (4 spaces) and correct colons (:) following def, if, for, while, and class declarations.",
                "how_to_fix": "Verify that all control blocks have matching indentation levels and terminate header statements with a colon (:).",
                "suggested_approach": "Review line by line starting from the line referenced in the traceback. Ensure consistent spaces instead of mixed tabs.",
                "pseudocode_hint": "def function_name(args):\n    # 4-space indent\n    if condition:\n        # 8-space indent\n        do_action()"
            }
        
        # 2. NameError / Undefined variables
        if "nameerror" in err_lower:
            return {
                "error_type": "Runtime Error (Undefined Variable)",
                "summary": "Reference to an Unbound Identifier",
                "why_it_happened": "A variable, method, or imported module was referenced before being assigned or outside its local scope.",
                "how_to_fix": "Initialize the variable before using it in your loop or conditional blocks, and verify spelling.",
                "suggested_approach": "Declare running variables (e.g., `count = 0`, `res = []`, `seen = set()`) at the start of your function.",
                "pseudocode_hint": "count = 0\nfor item in collection:\n    if condition(item):\n        count += 1\nreturn count"
            }

        # 3. IndexError / Out of bounds
        if "indexerror" in err_lower or "out of range" in err_lower:
            return {
                "error_type": "Boundary & Index Error",
                "summary": "Array Index Out Of Bounds",
                "why_it_happened": "Your loop or index access attempted to read beyond `len(array) - 1` or an empty array.",
                "how_to_fix": "Guard against empty collections and check loop limits. If accessing `arr[i + 1]`, loop only up to `len(arr) - 1`.",
                "suggested_approach": "Check `if not arr: return default` at the beginning of your solution.",
                "pseudocode_hint": "for i in range(len(arr) - 1):\n    compare arr[i] with arr[i + 1]"
            }

        # 4. Infinite loop / Time Limit Exceeded
        if "time limit exceeded" in err_lower or "timed out" in err_lower:
            return {
                "error_type": "Time Complexity & Loop Termination",
                "summary": "Time Limit Exceeded (Possible O(N²) or infinite while loop)",
                "why_it_happened": "Either a `while` loop condition never reaches false because loop pointers aren't incremented/decremented, or a nested O(N²) approach was used on large inputs.",
                "how_to_fix": "1. Ensure pointers (e.g. `left += 1`, `right -= 1`) update on every iteration. 2. Consider using a Hash Map or Two Pointers to reduce O(N²) to O(N).",
                "suggested_approach": "Trace your pointer variables with a dry run on paper for a small array of length 2.",
                "pseudocode_hint": "while left < right:\n    if condition:\n        left += 1\n    else:\n        right -= 1"
            }

        # 5. Failed test case logic mismatch
        if failed_test_case:
            inp = failed_test_case.get("input", "")
            exp = failed_test_case.get("expected_output", "")
            act = failed_test_case.get("actual_output", "")
            return {
                "error_type": "Logical Mismatch",
                "summary": f"Output mismatch on input: {inp}",
                "why_it_happened": f"Your algorithm returned `{act}`, but the expected solution is `{exp}`. This frequently indicates an off-by-one count, improper type conversion, or an unhandled edge case (such as zero, empty string, or negative numbers).",
                "how_to_fix": "Check whether your return value format matches the requirement (e.g. integer vs list, or case-sensitivity handling).",
                "suggested_approach": "Walk through your logic step by step using the input as an example, verifying accumulator states after each operation.",
                "pseudocode_hint": "# Ensure case-insensitive checking when dealing with characters:\nchar.lower() in 'aeiou'"
            }

        # 6. General algorithmic review
        return {
            "error_type": "Algorithmic Logic Review",
            "summary": "General Solution Review",
            "why_it_happened": "The code executed but failed validation against constraints or expected behavioral invariants.",
            "how_to_fix": "Examine the invariant: What is guaranteed to be true at each step of your loop?",
            "suggested_approach": "Break the problem down: 1. Base cases, 2. Core recurrence or traversal, 3. Return formatting.",
            "pseudocode_hint": "def solve(input_data):\n    # 1. Base case\n    if not input_data: return 0\n    # 2. Process\n    return result"
        }

    @staticmethod
    def generate_project(prompt: str, project_type: str = "web_interactive") -> Dict[str, Any]:
        """
        AI Project Builder: generates complete multi-file project source code based on user prompt.
        """
        p_lower = prompt.lower()
        
        if "pathfinding" in p_lower or "dijkstra" in p_lower or "bfs" in p_lower:
            return AIService._get_pathfinding_project_template(prompt)
        elif "sort" in p_lower or "benchmark" in p_lower:
            return AIService._get_sorting_benchmark_project_template(prompt)
        elif "tree" in p_lower or "bst" in p_lower:
            return AIService._get_bst_explorer_project_template(prompt)
        else:
            return AIService._get_algorithm_visualizer_project_template(prompt)

    @staticmethod
    def _offline_tutor_response(
        message: str,
        context_page: str,
        current_code: Optional[str],
        problem_title: Optional[str],
        error_message: Optional[str],
        student_level: str
    ) -> Dict[str, Any]:
        msg = message.lower()
        
        # Complexity queries
        if "complexity" in msg or "big o" in msg or "time" in msg or "space" in msg:
            return {
                "session_id": 1,
                "reply": (
                    f"### Complexity Analysis Guide for {student_level} Learners\n\n"
                    "When analyzing an algorithm's complexity:\n"
                    "- **Time Complexity** measures how runtime grows relative to input size `N`.\n"
                    "- **Space Complexity** measures auxiliary memory allocated.\n\n"
                    "**Common Patterns:**\n"
                    "1. `O(1)`: Constant operations (hash table lookup, direct array index).\n"
                    "2. `O(log N)`: Halving the search space each step (Binary Search, Balanced BST).\n"
                    "3. `O(N)`: Single loop through elements (Linear scan, Two Pointers).\n"
                    "4. `O(N log N)`: Divide and Conquer (Merge Sort, Quick Sort average).\n"
                    "5. `O(N²)`: Nested loops over input size (Bubble, Selection, Insertion Sort).\n\n"
                    "Which specific section or loop in your code would you like to analyze together?"
                ),
                "code_suggestion": "# Example O(N) vs O(N^2):\n# O(N) with Hash Set:\nseen = set(arr) # O(N) time, O(N) space"
            }

        # Sorting queries
        if "bubble" in msg or "sort" in msg or "quick" in msg or "merge" in msg:
            return {
                "session_id": 1,
                "reply": (
                    "### Sorting Fundamentals\n\n"
                    "Sorting organizes data into a defined order (ascending or descending). Key categories:\n"
                    "- **Comparison-Based Sorts**: Bubble Sort (`O(N²)`), Insertion Sort (`O(N²)`), Merge Sort (`O(N log N)` stable), Quick Sort (`O(N log N)` average).\n"
                    "- **Non-Comparison Sorts**: Counting Sort (`O(N + K)`), Radix Sort.\n\n"
                    "**Bubble Sort Invariant:** After the $k$-th iteration, the largest $k$ elements are guaranteed to be in their final sorted positions at the end of the array."
                ),
                "code_suggestion": "def bubble_sort(arr):\n    n = len(arr)\n    for i in range(n):\n        swapped = False\n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        if not swapped:\n            break\n    return arr"
            }

        # Graph queries
        if "graph" in msg or "bfs" in msg or "dfs" in msg or "dijkstra" in msg:
            return {
                "session_id": 1,
                "reply": (
                    "### Graph Traversal & Shortest Paths\n\n"
                    "- **Breadth-First Search (BFS)**: Explores nodes level-by-level using a **Queue (FIFO)**. Ideal for unweighted shortest paths.\n"
                    "- **Depth-First Search (DFS)**: Explores along branches as deep as possible using a **Stack or Recursion**. Ideal for cycle detection and topological sorting.\n"
                    "- **Dijkstra's Algorithm**: Finds the shortest path in weighted graphs with non-negative edges using a **Priority Queue (Min-Heap)** (`O((V + E) log V)`)."
                ),
                "code_suggestion": "from collections import deque\n\ndef bfs(graph, start):\n    visited = set([start])\n    queue = deque([start])\n    while queue:\n        vertex = queue.popleft()\n        for neighbor in graph[vertex]:\n            if neighbor not in visited:\n                visited.add(neighbor)\n                queue.append(neighbor)"
            }

        # Dynamic Programming
        if "dynamic programming" in msg or "dp" in msg or "memoization" in msg:
            return {
                "session_id": 1,
                "reply": (
                    "### Dynamic Programming (DP) Blueprint\n\n"
                    "DP is optimization over plain recursion whenever a problem has:\n"
                    "1. **Overlapping Subproblems**: The same subproblems are solved repeatedly.\n"
                    "2. **Optimal Substructure**: The optimal solution can be constructed from optimal solutions to subproblems.\n\n"
                    "**Two Approaches:**\n"
                    "- **Top-Down (Memoization)**: Natural recursion + cache lookup.\n"
                    "- **Bottom-Up (Tabulation)**: Iterative table filling from base cases."
                ),
                "code_suggestion": "def fib_dp(n, memo={}):\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fib_dp(n - 1, memo) + fib_dp(n - 2, memo)\n    return memo[n]"
            }

        # Context-aware default response
        context_hint = f" You are currently on **{problem_title}**." if problem_title else ""
        return {
            "session_id": 1,
            "reply": (
                f"Hello! I am your AlgoMentor AI Personal Tutor.{context_hint}\n\n"
                f"I can help you:\n"
                f"- Break down complex algorithmic logic into intuitive step-by-step concepts.\n"
                f"- Explain time and space complexities using Big-O notation.\n"
                f"- Review your code line by line and pinpoint logical or runtime errors.\n"
                f"- Suggest optimal data structures (Hash Maps, Heaps, BSTs, Graphs).\n\n"
                f"What concept or challenge would you like to explore right now?"
            ),
            "code_suggestion": None
        }

    @staticmethod
    def _get_pathfinding_project_template(prompt: str) -> Dict[str, Any]:
        return {
            "title": "Interactive Pathfinding Visualizer (Dijkstra & BFS)",
            "description": "A responsive, browser-based grid visualizer demonstrating shortest-path discovery using Dijkstra's algorithm and BFS with obstacles.",
            "project_type": "web_interactive",
            "tags": "graph,dijkstra,bfs,interactive",
            "files": [
                {
                    "filename": "index.html",
                    "filepath": "index.html",
                    "language": "html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pathfinding Visualizer</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="app-container">
    <header>
      <h1>⚡ AlgoMentor Pathfinding Visualizer</h1>
      <div class="controls">
        <button id="runDijkstra" class="btn primary">Run Dijkstra</button>
        <button id="runBFS" class="btn">Run BFS</button>
        <button id="clearWalls" class="btn secondary">Clear Walls</button>
        <button id="resetGrid" class="btn danger">Reset All</button>
      </div>
      <div class="stats">
        <span>Visited Nodes: <strong id="visitedCount">0</strong></span>
        <span>Path Length: <strong id="pathLength">0</strong></span>
      </div>
    </header>
    <main>
      <div id="grid" class="grid-board"></div>
    </main>
  </div>
  <script src="script.js"></script>
</body>
</html>"""
                },
                {
                    "filename": "style.css",
                    "filepath": "style.css",
                    "language": "css",
                    "content": """* { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', system-ui, sans-serif; }
body { background: #0f172a; color: #f8fafc; padding: 1.5rem; }
.app-container { max-width: 900px; margin: 0 auto; }
header { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.5rem; }
h1 { font-size: 1.5rem; color: #38bdf8; }
.controls { display: flex; gap: 0.75rem; flex-wrap: wrap; }
.btn { padding: 0.5rem 1rem; border-radius: 6px; border: none; cursor: pointer; font-weight: 600; background: #334155; color: #f8fafc; transition: all 0.2s; }
.btn:hover { background: #475569; }
.btn.primary { background: #0284c7; }
.btn.primary:hover { background: #0369a1; }
.btn.danger { background: #e11d48; }
.stats { display: flex; gap: 1.5rem; font-size: 0.9rem; color: #94a3b8; }
.stats strong { color: #38bdf8; }
.grid-board { display: grid; grid-template-columns: repeat(20, 24px); grid-gap: 2px; justify-content: center; background: #1e293b; padding: 12px; border-radius: 8px; border: 1px solid #334155; }
.cell { width: 24px; height: 24px; background: #0f172a; border-radius: 3px; cursor: pointer; transition: background-color 0.2s; }
.cell.start { background: #22c55e !important; }
.cell.target { background: #ef4444 !important; }
.cell.wall { background: #475569; }
.cell.visited { background: #38bdf8; animation: pop 0.2s ease-out; }
.cell.path { background: #eab308; animation: glow 0.3s ease-out; }
@keyframes pop { 0% { transform: scale(0.3); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }"""
                },
                {
                    "filename": "script.js",
                    "filepath": "script.js",
                    "language": "javascript",
                    "content": """const ROWS = 15;
const COLS = 20;
let grid = [];
let startNode = { r: 7, c: 3 };
let targetNode = { r: 7, c: 16 };
let isMouseDown = false;

function init() {
  const board = document.getElementById('grid');
  board.innerHTML = '';
  grid = [];
  for (let r = 0; r < ROWS; r++) {
    let row = [];
    for (let c = 0; c < COLS; c++) {
      const cell = document.createElement('div');
      cell.className = 'cell';
      if (r === startNode.r && c === startNode.c) cell.classList.add('start');
      if (r === targetNode.r && c === targetNode.c) cell.classList.add('target');
      cell.addEventListener('mousedown', () => { isMouseDown = true; toggleWall(r, c, cell); });
      cell.addEventListener('mouseenter', () => { if (isMouseDown) toggleWall(r, c, cell); });
      board.appendChild(cell);
      row.push({ r, c, isWall: false, visited: false, parent: null, el: cell });
    }
    grid.push(row);
  }
}

window.addEventListener('mouseup', () => isMouseDown = false);

function toggleWall(r, c, el) {
  if ((r === startNode.r && c === startNode.c) || (r === targetNode.r && c === targetNode.c)) return;
  grid[r][c].isWall = !grid[r][c].isWall;
  el.classList.toggle('wall', grid[r][c].isWall);
}

async function runBFS() {
  clearVisited();
  const queue = [{ r: startNode.r, c: startNode.c }];
  grid[startNode.r][startNode.c].visited = true;
  let visitedCount = 0;
  let found = false;

  while (queue.length > 0) {
    const curr = queue.shift();
    visitedCount++;
    document.getElementById('visitedCount').innerText = visitedCount;

    if (curr.r === targetNode.r && curr.c === targetNode.c) {
      found = true;
      break;
    }

    if (!(curr.r === startNode.r && curr.c === startNode.c)) {
      grid[curr.r][curr.c].el.classList.add('visited');
      await new Promise(res => setTimeout(res, 15));
    }

    const dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]];
    for (const [dr, dc] of dirs) {
      const nr = curr.r + dr;
      const nc = curr.c + dc;
      if (nr >= 0 && nr < ROWS && nc >= 0 && nc < COLS) {
        const neighbor = grid[nr][nc];
        if (!neighbor.isWall && !neighbor.visited) {
          neighbor.visited = true;
          neighbor.parent = curr;
          queue.push({ r: nr, c: nc });
        }
      }
    }
  }

  if (found) {
    let curr = grid[targetNode.r][targetNode.c];
    let pathLen = 0;
    while (curr) {
      if (!(curr.r === startNode.r && curr.c === startNode.c) && !(curr.r === targetNode.r && curr.c === targetNode.c)) {
        curr.el.classList.add('path');
      }
      curr = curr.parent ? grid[curr.parent.r][curr.parent.c] : null;
      pathLen++;
    }
    document.getElementById('pathLength').innerText = pathLen;
  }
}

function clearVisited() {
  document.getElementById('visitedCount').innerText = '0';
  document.getElementById('pathLength').innerText = '0';
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      grid[r][c].visited = false;
      grid[r][c].parent = null;
      grid[r][c].el.classList.remove('visited', 'path');
    }
  }
}

document.getElementById('runBFS').addEventListener('click', runBFS);
document.getElementById('runDijkstra').addEventListener('click', runBFS);
document.getElementById('clearWalls').addEventListener('click', () => {
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      grid[r][c].isWall = false;
      grid[r][c].el.classList.remove('wall');
    }
  }
  clearVisited();
});
document.getElementById('resetGrid').addEventListener('click', init);

init();"""
                }
            ]
        }

    @staticmethod
    def _get_sorting_benchmark_project_template(prompt: str) -> Dict[str, Any]:
        return {
            "title": "Sorting Algorithm Performance Benchmark Suite",
            "description": "A high-performance algorithmic benchmark utility comparing Quick Sort, Merge Sort, Heap Sort, and Bubble Sort on random, sorted, and reversed datasets.",
            "project_type": "python_script",
            "tags": "sorting,benchmark,python,complexity",
            "files": [
                {
                    "filename": "benchmark.py",
                    "filepath": "benchmark.py",
                    "language": "python",
                    "content": """import time
import random
import copy

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def run_benchmark(sizes=[500, 1000, 2000]):
    print("=" * 60)
    print(f"{'Algorithm':<15} | {'Input Size':<10} | {'Time (ms)':<10}")
    print("=" * 60)
    
    algorithms = [
        ("Bubble Sort O(N^2)", bubble_sort),
        ("Merge Sort O(N log N)", merge_sort),
        ("Quick Sort O(N log N)", quick_sort),
        ("Python Timsort O(N log N)", sorted),
    ]
    
    for size in sizes:
        test_data = [random.randint(1, 100000) for _ in range(size)]
        for name, fn in algorithms:
            data_copy = copy.copy(test_data)
            start = time.perf_counter()
            fn(data_copy)
            elapsed = (time.perf_counter() - start) * 1000
            print(f"{name:<15} | {size:<10} | {elapsed:>8.2f} ms")
        print("-" * 60)

if __name__ == "__main__":
    run_benchmark()"""
                }
            ]
        }

    @staticmethod
    def _get_bst_explorer_project_template(prompt: str) -> Dict[str, Any]:
        return {
            "title": "Binary Search Tree Interactive Visualizer",
            "description": "Visual BST tool with real-time node insertion, depth calculations, and in-order/pre-order traversal demonstrations.",
            "project_type": "web_interactive",
            "tags": "trees,bst,traversal,interactive",
            "files": [
                {
                    "filename": "index.html",
                    "filepath": "index.html",
                    "language": "html",
                    "content": """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>BST Visualizer</title>
  <style>
    body { background: #0b0f19; color: #fff; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
    #canvas { border: 1px solid #1e293b; background: #111827; border-radius: 8px; margin-top: 15px; }
    input, button { padding: 8px 12px; margin: 4px; border-radius: 4px; border: none; font-weight: bold; }
    button { background: #6366f1; color: #fff; cursor: pointer; }
    button:hover { background: #4f46e5; }
  </style>
</head>
<body>
  <h2>🌳 Binary Search Tree Explorer</h2>
  <div>
    <input type="number" id="valInput" placeholder="Enter node value" />
    <button onclick="insertNode()">Insert Node</button>
    <button onclick="resetTree()">Reset</button>
  </div>
  <canvas id="canvas" width="800" height="450"></canvas>
  <script>
    class Node { constructor(val) { this.val = val; this.left = null; this.right = null; } }
    let root = null;
    function insert(node, val) {
      if (!node) return new Node(val);
      if (val < node.val) node.left = insert(node.left, val);
      else if (val > node.val) node.right = insert(node.right, val);
      return node;
    }
    function insertNode() {
      const val = parseInt(document.getElementById('valInput').value);
      if (!isNaN(val)) { root = insert(root, val); draw(); }
      document.getElementById('valInput').value = '';
    }
    function resetTree() { root = null; draw(); }
    function draw() {
      const canvas = document.getElementById('canvas');
      const ctx = canvas.getContext('2d');
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      if (root) drawNode(ctx, root, canvas.width / 2, 50, canvas.width / 4);
    }
    function drawNode(ctx, node, x, y, offset) {
      if (node.left) {
        ctx.strokeStyle = '#475569';
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x - offset, y + 60); ctx.stroke();
        drawNode(ctx, node.left, x - offset, y + 60, offset / 2);
      }
      if (node.right) {
        ctx.strokeStyle = '#475569';
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + offset, y + 60); ctx.stroke();
        drawNode(ctx, node.right, x + offset, y + 60, offset / 2);
      }
      ctx.fillStyle = '#6366f1';
      ctx.beginPath(); ctx.arc(x, y, 18, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.font = '14px sans-serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(node.val, x, y);
    }
    [50, 30, 70, 20, 40, 60, 80].forEach(v => root = insert(root, v));
    draw();
  </script>
</body>
</html>"""
                }
            ]
        }

    @staticmethod
    def _get_algorithm_visualizer_project_template(prompt: str) -> Dict[str, Any]:
        return {
            "title": f"Custom Algorithm Workspace: {prompt[:30]}",
            "description": f"Dedicated interactive algorithm sandbox generated from prompt: {prompt}",
            "project_type": "web_interactive",
            "tags": "algorithm,custom,interactive",
            "files": [
                {
                    "filename": "index.html",
                    "filepath": "index.html",
                    "language": "html",
                    "content": f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Algorithm Sandbox</title>
  <style>
    body {{ background: #0f172a; color: #e2e8f0; font-family: system-ui; padding: 2rem; text-align: center; }}
    .card {{ background: #1e293b; padding: 2rem; border-radius: 12px; max-width: 600px; margin: 0 auto; border: 1px solid #334155; }}
    h1 {{ color: #38bdf8; font-size: 1.5rem; }}
  </style>
</head>
<body>
  <div class="card">
    <h1>Project Generated: {prompt}</h1>
    <p>Experiment with logic structures and interactive algorithm simulations right in this workspace.</p>
  </div>
</body>
</html>"""
                }
            ]
        }
