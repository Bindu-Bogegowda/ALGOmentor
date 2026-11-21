"""
Seed Script: Complete Roadmap.sh DSA Concepts & Algorithms
Seeds every item from the official DSA roadmap into AlgoMentor.
"""

import json
from app.database import SessionLocal
from app.models.lesson import Lesson

ROADMAP_CONCEPTS = [
    # -------------------------------------------------------------
    # Programming Fundamentals
    # -------------------------------------------------------------
    {
        "id": "concept_pick_a_language",
        "category": "Programming Fundamentals",
        "difficulty": "Beginner",
        "title": "Pick a Language (Python, Java, C++, JavaScript, Go, Rust)",
        "prerequisites": "None",
        "summary": "Choose the optimal language for learning DSA, comparing memory control, speed, standard library collections, and interview ubiquity.",
        "why_learn_it": "Selecting the right language allows you to balance execution speed with syntax clarity when solving algorithmic challenges.",
        "fundamental_explanation": "Java and C++ offer explicit typing and deep memory visibility (pointers, JVM heap vs stack), while Python offers rapid prototyping and concise syntax. Choose Python or Java as your primary interview language.",
        "core_theory": "### Language Comparison for DSA\n- **Python:** Expressive syntax, built-in dynamic arrays, high-level sets/dicts. Ideal for rapid problem-solving.\n- **Java:** Strict OOP, garbage collection, Collections Framework (ArrayList, ArrayDeque, HashMap, PriorityQueue).\n- **C++:** Raw memory pointers, zero-overhead STL (vector, map, unordered_map).\n- **Go / Rust:** Modern systems languages with memory safety and concurrency primitives.",
        "time_complexity": "Language primitives: O(1)",
        "space_complexity": "Runtime runtime overhead",
        "video_url": "https://www.youtube.com/embed/zOjov-2OZ0E",
        "video_title": "Which Language is Best for DSA?",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class LanguageChoice {
    public static void main(String[] args) {
        System.out.println("Java provides strong types and robust Collections Framework.");
    }
}""",
        "python_code": """# Python DSA starter
def main():
    print("Python provides concise syntax and dynamic typing.")

if __name__ == "__main__":
    main()"""
    },
    {
        "id": "concept_language_syntax_controls",
        "category": "Programming Fundamentals",
        "difficulty": "Beginner",
        "title": "Language Syntax & Control Structures (Loops & Conditionals)",
        "prerequisites": "Pick a Language",
        "summary": "Master branching conditionals (if/else, switch) and iteration loops (for, while, nested loops) forming the skeleton of all algorithms.",
        "why_learn_it": "Every algorithm is an execution sequence governed by loops and conditionals.",
        "fundamental_explanation": "Control structures dictate program flow. Conditionals evaluate boolean expressions to branch execution; loops repeat code blocks while invariants hold true.",
        "core_theory": "### Control Structures:\n1. **Branching:** `if`, `else if`, `else`, `switch/case`.\n2. **Iteration:** `for` loop (counter-controlled), `while` loop (condition-controlled), `do-while` (post-tested).\n3. **Loop Invariants:** Properties that remain true before each iteration, ensuring correct termination.",
        "time_complexity": "Single loop: O(n) · Nested loop: O(n²)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/m7sWkQJ9-tI",
        "video_title": "Control Structures and Loops in Programming",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class ControlStructures {
    public static void main(String[] args) {
        int n = 5;
        for (int i = 0; i < n; i++) {
            if (i % 2 == 0) System.out.println(i + " is even");
            else System.out.println(i + " is odd");
        }
    }
}""",
        "python_code": """for i in range(5):
    if i % 2 == 0:
        print(f"{i} is even")
    else:
        print(f"{i} is odd")"""
    },
    {
        "id": "concept_pseudo_code_functions",
        "category": "Programming Fundamentals",
        "difficulty": "Beginner",
        "title": "Pseudo Code, Functions & Call Stack Execution",
        "prerequisites": "Language Syntax",
        "summary": "Design language-agnostic logic with pseudo code, write modular functions, and trace execution frames on the Call Stack.",
        "why_learn_it": "Interviewers evaluate how you express algorithms in clear pseudo code before writing raw syntax.",
        "fundamental_explanation": "Pseudo code is an informal high-level description of an algorithm. Functions encapsulate logic into callable units, pushing a new frame to the Call Stack upon invocation and popping upon return.",
        "core_theory": "### Call Stack Mechanics\nEach function call pushes: local variables, parameter values, and the return address. When functions return, their stack frame is destroyed.",
        "time_complexity": "Function dispatch: O(1)",
        "space_complexity": "Call Stack: O(Depth)",
        "video_url": "https://www.youtube.com/embed/Yp9H4t9sZlQ",
        "video_title": "How the Call Stack Works in Memory",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class FunctionsDemo {
    public static int add(int a, int b) {
        return a + b; // pushes frame to call stack
    }
    public static void main(String[] args) {
        System.out.println(add(10, 20));
    }
}""",
        "python_code": """def calculate_sum(a: int, b: int) -> int:
    # Function execution frame pushed to call stack
    return a + b

print(calculate_sum(10, 20))"""
    },
    {
        "id": "concept_oop_basics_dsa",
        "category": "Programming Fundamentals",
        "difficulty": "Beginner",
        "title": "OOP Basics: Classes, Objects & Custom Nodes (ListNode, TreeNode)",
        "prerequisites": "Functions",
        "summary": "Understand encapsulation, pointers/references, and how custom classes model non-linear data structures like linked nodes and trees.",
        "why_learn_it": "Data structures like Linked Lists, Binary Trees, and Tries are represented as interconnected class objects in memory.",
        "fundamental_explanation": "A class is a blueprint; an object is an instance allocated on the Heap. Custom node classes bundle data fields with reference pointers to neighboring nodes.",
        "core_theory": "### Custom Node Construction\n```java\nclass ListNode {\n    int val;\n    ListNode next;\n    ListNode(int val) { this.val = val; }\n}\n```",
        "time_complexity": "Node instantiation: O(1)",
        "space_complexity": "O(1) heap allocation per node",
        "video_url": "https://www.youtube.com/embed/pTB0EiLXUC8",
        "video_title": "Object Oriented Programming for DSA",
        "visualization_type": "linked_list",
        "visualization_algorithm": "linked_list",
        "practice_problem_slug": "reverse-linked-list",
        "java_code": """class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public class OOPDemo {
    public static void main(String[] args) {
        ListNode head = new ListNode(10);
        head.next = new ListNode(20);
        System.out.println("Node val: " + head.next.val);
    }
}""",
        "python_code": """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

head = ListNode(10, ListNode(20))
print(f"Node val: {head.next.val}")"""
    },

    # -------------------------------------------------------------
    # Basic Data Structures
    # -------------------------------------------------------------
    {
        "id": "concept_what_why_data_structures",
        "category": "Basic Data Structures",
        "difficulty": "Beginner",
        "title": "What are Data Structures & Why They Matter",
        "prerequisites": "Variables & Memory",
        "summary": "Discover why choosing the correct data structure dictates software performance, memory footprint, and architectural elegance.",
        "why_learn_it": "Algorithms operate on data structures. Bad data structure choices make operations orders of magnitude slower regardless of code optimization.",
        "fundamental_explanation": "A data structure is a specialized format for organizing, processing, retrieving and storing data in computer memory.",
        "core_theory": "### Tradeoffs in Data Structures:\n- Arrays: O(1) index access, but O(n) insert/delete.\n- Linked Lists: O(1) insert at head, but O(n) search.\n- Hash Tables: O(1) average lookup, but unordered and hash collisions.\n- Trees: O(log n) ordered search, but pointer memory overhead.",
        "time_complexity": "Varies by structure",
        "space_complexity": "Varies by structure",
        "video_url": "https://www.youtube.com/embed/zg9ih6SVACc",
        "video_title": "Data Structures in 100 Seconds",
        "visualization_type": "sorting",
        "visualization_algorithm": "bubble_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """// Comparison of data structure speeds
import java.util.*;
public class DataStructureIntro {
    public static void main(String[] args) {
        int[] arr = new int[]{1, 2, 3}; // O(1) random access
        List<Integer> list = new LinkedList<>(); // O(1) head insertion
    }
}""",
        "python_code": """# Python list vs dict access speed
nums = [10, 20, 30] # O(1) by index
table = {"key": "val"} # O(1) by key"""
    },

    # -------------------------------------------------------------
    # Algorithmic Complexity
    # -------------------------------------------------------------
    {
        "id": "concept_complexity_time_vs_space",
        "category": "Algorithmic Complexity",
        "difficulty": "Beginner",
        "title": "Time vs Space Complexity & Calculating Runtimes",
        "prerequisites": "Asymptotic Analysis",
        "summary": "Learn step-by-step how to count primitive operations, recurrence relations, and trade RAM memory space for faster execution time.",
        "why_learn_it": "The Time-Memory Tradeoff is the most fundamental engineering lever in high-performance computing and system design.",
        "fundamental_explanation": "Time complexity counts operations as a function of input size n. Space complexity measures auxiliary memory used during execution.",
        "core_theory": "### Common Runtimes:\n- **Constant:** O(1)\n- **Logarithmic:** O(log n)\n- **Linear:** O(n)\n- **Polynomial:** O(n^k) like O(n²), O(n³)\n- **Exponential:** O(2ⁿ)\n- **Factorial:** O(n!)",
        "time_complexity": "All complexity tiers analyzed",
        "space_complexity": "Auxiliary memory budget",
        "video_url": "https://www.youtube.com/embed/D6xkbGLQesk",
        "video_title": "Calculating Algorithmic Complexity",
        "visualization_type": "searching",
        "visualization_algorithm": "binary_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class ComplexityCalc {
    // O(n²) nested loop
    public static void printPairs(int n) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                // n * n operations
            }
        }
    }
}""",
        "python_code": """def calculate_steps(n: int):
    # O(n) single pass
    for i in range(n): pass
    # O(n^2) nested
    for i in range(n):
        for j in range(n): pass"""
    },
    {
        "id": "concept_asymptotic_notations",
        "category": "Algorithmic Complexity",
        "difficulty": "Beginner",
        "title": "Asymptotic Notations: Big-O, Big-Theta (Θ) & Big-Omega (Ω)",
        "prerequisites": "Time vs Space Complexity",
        "summary": "Understand mathematical definitions of upper bounds (Big-O), tight bounds (Big-Θ), and lower bounds (Big-Ω).",
        "why_learn_it": "Allows unambiguous precision when comparing best-case, average-case, and worst-case algorithmic behaviors.",
        "fundamental_explanation": "Big-O provides a ceiling (worst case). Big-Omega provides a floor (best case). Big-Theta provides an exact tight bound where upper and lower bounds coincide.",
        "core_theory": "### Formal Definitions\n- **Big-O:** `f(n) <= c * g(n)` for all `n >= n0` (Upper bound).\n- **Big-Omega (Ω):** `f(n) >= c * g(n)` for all `n >= n0` (Lower bound).\n- **Big-Theta (Θ):** `c1 * g(n) <= f(n) <= c2 * g(n)` (Tight bound).",
        "time_complexity": "Theoretical: O(1)",
        "space_complexity": "O(1)",
        "video_url": "https://www.youtube.com/embed/D6xkbGLQesk",
        "video_title": "Big O, Big Omega, Big Theta Explained",
        "visualization_type": "searching",
        "visualization_algorithm": "binary_search",
        "practice_problem_slug": "two-sum",
        "java_code": """// Linear search: Best-case Ω(1), Worst-case O(n)
public class AsymptoticDemo {
    public static int find(int[] arr, int target) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) return i; // Best case: index 0 -> Ω(1)
        }
        return -1; // Worst case: O(n)
    }
}""",
        "python_code": """# Best case Omega(1), Worst case O(n)
def linear_search(arr, target):
    for i, x in enumerate(arr):
        if x == target: return i
    return -1"""
    },

    # -------------------------------------------------------------
    # Complex Data Structures & Indexing
    # -------------------------------------------------------------
    {
        "id": "concept_b_trees_indexing",
        "category": "Complex Data Structures & Indexing",
        "difficulty": "Advanced",
        "title": "B-Trees & B+ Trees: Self-Balancing Disk-Based Storage",
        "prerequisites": "Binary Search Trees, Heaps",
        "summary": "Master multi-way balanced search trees optimized for reading and writing large blocks of memory on SSDs and relational database indexes.",
        "why_learn_it": "Every relational database (PostgreSQL, MySQL InnoDB, SQLite) stores tables and primary keys in B+ Tree indexes.",
        "fundamental_explanation": "Unlike binary trees with 2 children, B-Tree nodes store hundreds of keys per node, matching the filesystem block size (4KB) to minimize slow disk I/O.",
        "core_theory": "### B-Tree vs B+ Tree\n- **B-Tree:** Keys and record data stored in both internal and leaf nodes.\n- **B+ Tree:** Data records stored ONLY in leaf nodes. Leaves are linked as a doubly linked list, enabling ultra-fast sequential range scans!",
        "time_complexity": "Search/Insert/Delete: O(log_B N) where B is branching factor",
        "space_complexity": "O(N) disk storage",
        "video_url": "https://www.youtube.com/embed/aZjYr87r1b8",
        "video_title": "B-Trees and B+ Trees in Databases Explained",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """// Conceptual B+ Tree Node
class BPlusTreeNode {
    int[] keys;
    BPlusTreeNode[] children;
    boolean isLeaf;
    BPlusTreeNode next; // Linked list pointer for sequential scan
}""",
        "python_code": """# Conceptual B-Tree node
class BTreeNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.is_leaf = leaf"""
    },
    {
        "id": "concept_skip_lists",
        "category": "Complex Data Structures & Indexing",
        "difficulty": "Advanced",
        "title": "Skip Lists: Probabilistic Alternative to Balanced Trees",
        "prerequisites": "Linked Lists, Probability",
        "summary": "Probabilistic data structure using layered linked lists with coin-flip express lanes to achieve O(log n) search, insertion, and deletion.",
        "why_learn_it": "Powers sorted sets (ZSET) in Redis, LevelDB, and RocksDB because it avoids complex tree balancing locks under multi-threaded concurrency.",
        "fundamental_explanation": "Bottom layer contains all elements in sorted order. Each higher level acts as an express highway skipping over elements with probability 1/2.",
        "core_theory": "### Search Invariant\nStart at the highest express level. Walk forward until the next element is greater than target, then drop down one level. Total expected comparisons: `O(log n)`.",
        "time_complexity": "Search/Insert/Delete: O(log n) average",
        "space_complexity": "O(n) average memory",
        "video_url": "https://www.youtube.com/embed/UGaOXaXAM5M",
        "video_title": "Skip Lists Data Structure Explained",
        "visualization_type": "linked_list",
        "visualization_algorithm": "linked_list",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.Random;
class SkipListNode {
    int val;
    SkipListNode[] forward;
    SkipListNode(int val, int level) {
        this.val = val; this.forward = new SkipListNode[level + 1];
    }
}""",
        "python_code": """import random
class SkipNode:
    def __init__(self, val, level):
        self.val = val
        self.forward = [None] * (level + 1)"""
    },
    {
        "id": "concept_2_3_trees_isam",
        "category": "Complex Data Structures & Indexing",
        "difficulty": "Advanced",
        "title": "2-3 Trees, ISAM & Database Indexing Strategies",
        "prerequisites": "B-Trees, Balanced Trees",
        "summary": "Explore 2-node and 3-node balance invariants, Indexed Sequential Access Method (ISAM), and linear vs tree-based database indexing.",
        "why_learn_it": "Provides the foundational theoretical model that directly inspired Red-Black Trees and modern database storage engines.",
        "fundamental_explanation": "In a 2-3 tree, internal nodes have either 2 children (1 key) or 3 children (2 keys). All leaf nodes are maintained at the exact same depth.",
        "core_theory": "### Indexing Paradigms:\n- **Linear Indexing:** Unsorted files indexed via sparse or dense primary tables.\n- **Tree-Based Indexing:** Multi-level hierarchical indexing (B+ Trees, 2-3 Trees) providing logarithmic search.",
        "time_complexity": "Search/Insert/Delete: O(log n)",
        "space_complexity": "O(n) auxiliary",
        "video_url": "https://www.youtube.com/embed/C3SsdUqasqc",
        "video_title": "2-3 Trees Insertion and Deletion",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """// Conceptual 2-3 Tree Node
class TwoThreeNode {
    int key1, key2;
    TwoThreeNode left, mid, right;
    boolean isThreeNode;
}""",
        "python_code": """# Conceptual 2-3 Tree Node representation
class TwoThreeNode:
    def __init__(self):
        self.keys = []
        self.children = []"""
    },

    # -------------------------------------------------------------
    # Problem Solving Techniques
    # -------------------------------------------------------------
    {
        "id": "concept_fast_slow_pointers",
        "category": "Problem Solving Techniques",
        "difficulty": "Intermediate",
        "title": "Fast and Slow Pointers (Floyd's Tortoise & Hare)",
        "prerequisites": "Two Pointers, Linked Lists",
        "summary": "Detect cycles in linked lists, find middle nodes, and identify cycle starting points using two pointers moving at speeds 1x and 2x.",
        "why_learn_it": "Solves cycle detection in O(n) time with strict O(1) space, avoiding hash set memory overhead.",
        "fundamental_explanation": "Slow moves 1 step; fast moves 2 steps. If a cycle exists, fast catches up to slow inside the loop. To find cycle start, reset one pointer to head and move both by 1 step.",
        "core_theory": "### Mathematical Proof\nLet distance to cycle start be L, loop length C. When slow enters loop, fast is inside. They meet at `(C - k)` steps. Distance from head to cycle entrance equals distance from meeting point to cycle entrance modulo C.",
        "time_complexity": "Time: O(n) · Space: O(1)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/PvrxZaH_eZ4",
        "video_title": "Floyd's Cycle Detection Algorithm Proof",
        "visualization_type": "linked_list",
        "visualization_algorithm": "linked_list",
        "practice_problem_slug": "reverse-linked-list",
        "java_code": """public class CycleDetection {
    public static boolean hasCycle(ListNode head) {
        ListNode slow = head, fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
            if (slow == fast) return true;
        }
        return false;
    }
}""",
        "python_code": """def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast: return True
    return False"""
    },
    {
        "id": "concept_cyclic_sort",
        "category": "Problem Solving Techniques",
        "difficulty": "Intermediate",
        "title": "Cyclic Sort: In-Place Sorting for Numbers in Range [1, N]",
        "prerequisites": "Arrays, In-Place Swapping",
        "summary": "Sort an array of numbers from 1 to N in O(n) linear time and O(1) space by placing every number at its correct index (val - 1).",
        "why_learn_it": "The definitive technique for solving Find Missing Number, Find All Duplicates, and First Missing Positive in O(n) one-pass.",
        "fundamental_explanation": "If an array contains numbers in range 1..N, each number `x` belongs at index `x - 1`. Continuously swap `arr[i]` with `arr[arr[i] - 1]` until `arr[i] == i + 1`.",
        "core_theory": "### Linear Time Invariant\nEach swap places at least one element into its permanent correct position. An element is swapped at most once, guaranteeing at most `2n` operations = O(n) time.",
        "time_complexity": "Time: O(n) · Space: O(1) in-place",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/Jpfhu2w5c3s",
        "video_title": "Cyclic Sort Pattern Explained",
        "visualization_type": "sorting",
        "visualization_algorithm": "selection_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """public class CyclicSort {
    public static int findMissing(int[] nums) {
        int i = 0, n = nums.length;
        while (i < n) {
            if (nums[i] < n && nums[i] != nums[nums[i]]) {
                int t = nums[nums[i]]; nums[nums[i]] = nums[i]; nums[i] = t;
            } else i++;
        }
        for (i = 0; i < n; i++) if (nums[i] != i) return i;
        return n;
    }
}""",
        "python_code": """def find_missing_number(nums: list[int]) -> int:
    i, n = 0, len(nums)
    while i < n:
        correct = nums[i]
        if nums[i] < n and nums[i] != nums[correct]:
            nums[i], nums[correct] = nums[correct], nums[i]
        else:
            i += 1
    for i in range(n):
        if nums[i] != i: return i
    return n"""
    },
    {
        "id": "concept_merge_intervals",
        "category": "Problem Solving Techniques",
        "difficulty": "Intermediate",
        "title": "Merge Intervals & Overlapping Range Processing",
        "prerequisites": "Sorting, Arrays",
        "summary": "Sort intervals by start time and merge overlapping contiguous spans in O(n log n) time.",
        "why_learn_it": "Used in calendar scheduling apps, OS memory allocation contiguous blocks, and IP address range consolidation.",
        "fundamental_explanation": "Sort by interval start. Maintain merged list. If current interval starts before prior interval ends (`curr.start <= prev.end`), merge by extending `prev.end = max(prev.end, curr.end)`.",
        "core_theory": "### Overlap Condition\n`interval_a.start <= interval_b.end && interval_b.start <= interval_a.end`",
        "time_complexity": "Time: O(n log n) · Space: O(n)",
        "space_complexity": "O(n) merged output",
        "video_url": "https://www.youtube.com/embed/qKczfGUrFY4",
        "video_title": "Merge Intervals Algorithm Explained",
        "visualization_type": "sorting",
        "visualization_algorithm": "selection_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class MergeIntervalsDemo {
    public static int[][] merge(int[][] intervals) {
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[0]));
        List<int[]> res = new ArrayList<>();
        for (int[] inv : intervals) {
            if (res.isEmpty() || res.get(res.size() - 1)[1] < inv[0]) res.add(inv);
            else res.get(res.size() - 1)[1] = Math.max(res.get(res.size() - 1)[1], inv[1]);
        }
        return res.toArray(new int[res.size()][]);
    }
}""",
        "python_code": """def merge(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0])
    res = []
    for inv in intervals:
        if not res or res[-1][1] < inv[0]:
            res.append(inv)
        else:
            res[-1][1] = max(res[-1][1], inv[1])
    return res"""
    },
    {
        "id": "concept_island_traversal_floodfill",
        "category": "Problem Solving Techniques",
        "difficulty": "Intermediate",
        "title": "Island Traversal & 2D Grid Flood Fill (BFS / DFS)",
        "prerequisites": "Graph BFS/DFS, 2D Arrays",
        "summary": "Explore 4-directionally and 8-directionally connected components in 2D grids using recursive DFS flood fill or BFS queues.",
        "why_learn_it": "Core technique in paint bucket tools, computer vision blob detection, game map fog-of-war, and maze solvers.",
        "fundamental_explanation": "Iterate through each cell. When land ('1') is encountered, increment island count and trigger flood-fill DFS/BFS to sink or mark all connected land cells as visited.",
        "core_theory": "### Direction Vectors\n`dr = [-1, 1, 0, 0]`, `dc = [0, 0, -1, 1]`. Boundary check: `r >= 0 && r < rows && c >= 0 && c < cols && grid[r][c] == '1'`.",
        "time_complexity": "Time: O(M * N) · Space: O(M * N) call stack",
        "space_complexity": "O(M * N) worst case recursion",
        "video_url": "https://www.youtube.com/embed/pV2kpPD66nE",
        "video_title": "Number of Islands BFS and DFS Visualized",
        "visualization_type": "graph",
        "visualization_algorithm": "dfs",
        "practice_problem_slug": "two-sum",
        "java_code": """public class IslandTraversal {
    public static int numIslands(char[][] grid) {
        int count = 0;
        for (int r = 0; r < grid.length; r++) {
            for (int c = 0; c < grid[0].length; c++) {
                if (grid[r][c] == '1') { count++; dfs(grid, r, c); }
            }
        }
        return count;
    }
    private static void dfs(char[][] g, int r, int c) {
        if (r < 0 || r >= g.length || c < 0 || c >= g[0].length || g[r][c] != '1') return;
        g[r][c] = '0'; // mark visited
        dfs(g, r + 1, c); dfs(g, r - 1, c); dfs(g, r, c + 1); dfs(g, r, c - 1);
    }
}""",
        "python_code": """def num_islands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    count = 0
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1': return
        grid[r][c] = '0'
        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1; dfs(r, c)
    return count"""
    },
    {
        "id": "concept_bellman_ford_algorithm",
        "category": "Graph Data Structures",
        "difficulty": "Advanced",
        "title": "Bellman-Ford Algorithm: Shortest Paths with Negative Weights",
        "prerequisites": "Graph Fundamentals, Dijkstra's Algorithm",
        "summary": "Find single-source shortest paths on graphs containing negative edge weights and detect negative weight cycles in O(V * E) time.",
        "why_learn_it": "Used in routing protocols (RIP - Routing Information Protocol) and currency arbitrage detection in financial trading.",
        "fundamental_explanation": "Relax all E edges V-1 times. If a V-th relaxation still reduces any distance, the graph contains a negative cycle!",
        "core_theory": "### Why V - 1 Relaxations?\nA simple shortest path in a graph with V vertices can have at most V - 1 edges. If distances can still decrease on step V, a cycle of negative sum exists.",
        "time_complexity": "Time: O(V * E) · Space: O(V)",
        "space_complexity": "O(V) distance array",
        "video_url": "https://www.youtube.com/embed/obWXjtg0L64",
        "video_title": "Bellman-Ford Algorithm Step by Step",
        "visualization_type": "graph",
        "visualization_algorithm": "dijkstra",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.Arrays;
public class BellmanFord {
    public static int[] shortestPath(int V, int[][] edges, int src) {
        int[] dist = new int[V];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;
        for (int i = 0; i < V - 1; i++) {
            for (int[] e : edges) {
                int u = e[0], v = e[1], w = e[2];
                if (dist[u] != Integer.MAX_VALUE && dist[u] + w < dist[v]) {
                    dist[v] = dist[u] + w;
                }
            }
        }
        return dist;
    }
}""",
        "python_code": """def bellman_ford(v: int, edges: list[tuple[int, int, int]], src: int) -> list[int]:
    dist = [float('inf')] * v
    dist[src] = 0
    for _ in range(v - 1):
        for u, nbr, wt in edges:
            if dist[u] != float('inf') and dist[u] + wt < dist[nbr]:
                dist[nbr] = dist[u] + wt
    return dist"""
    },
    {
        "id": "concept_a_star_algorithm",
        "category": "Graph Data Structures",
        "difficulty": "Advanced",
        "title": "A* Search Algorithm: Heuristic Pathfinding",
        "prerequisites": "Dijkstra's Algorithm, Heuristics",
        "summary": "Best-first graph search algorithm using evaluation function f(n) = g(n) + h(n) to find shortest path toward target rapidly.",
        "why_learn_it": "The ubiquitous pathfinding algorithm used in video game AI (moving units around obstacles) and robotic navigation.",
        "fundamental_explanation": "`g(n)` is the exact cost from start to node n. `h(n)` is an admissible heuristic estimate from node n to the goal (e.g. Euclidean or Manhattan distance).",
        "core_theory": "### Admissibility Invariant\nA heuristic is **admissible** if it never overestimates the actual cost to reach the goal (`h(n) <= true_cost`). This guarantees finding an optimal path.",
        "time_complexity": "Worst case O(V log V), in practice much faster than Dijkstra",
        "space_complexity": "O(V) for priority queue and visited table",
        "video_url": "https://www.youtube.com/embed/ySN5Wnu88nE",
        "video_title": "A* Pathfinding Algorithm Visualized",
        "visualization_type": "graph",
        "visualization_algorithm": "dijkstra",
        "practice_problem_slug": "two-sum",
        "java_code": """// Conceptual A* Priority Queue evaluation
class Node implements Comparable<Node> {
    int id, g, h;
    int f() { return g + h; }
    public int compareTo(Node o) { return Integer.compare(this.f(), o.f()); }
}""",
        "python_code": """import heapq
def a_star(graph, start, goal, h_func):
    pq = [(h_func(start, goal), 0, start, [])] # (f, g, current, path)
    visited = set()
    while pq:
        f, g, curr, path = heapq.heappop(pq)
        if curr == goal: return path + [curr]
        if curr in visited: continue
        visited.add(curr)
        for nbr, wt in graph.get(curr, []):
            if nbr not in visited:
                heapq.heappush(pq, (g + wt + h_func(nbr, goal), g + wt, nbr, path + [curr]))"""
    },
    {
        "id": "concept_mst_prims_kruskals",
        "category": "Graph Data Structures",
        "difficulty": "Advanced",
        "title": "Minimum Spanning Tree (MST): Prim's vs Kruskal's",
        "prerequisites": "Disjoint Set Union, Priority Queue",
        "summary": "Find a subset of edges that connects all vertices together with minimum possible total edge weight without any cycles.",
        "why_learn_it": "Used in fiber optic telecommunication network cable routing, electrical grid infrastructure, and road network planning.",
        "fundamental_explanation": "Kruskal's sorts edges and greedily adds them using DSU to avoid cycles. Prim's grows a tree vertex-by-vertex using a Min-Priority Queue.",
        "core_theory": "### Kruskal vs Prim\n- **Kruskal:** O(E log E) sorting edges + O(E α(V)) DSU. Preferred for sparse graphs.\n- **Prim:** O((V + E) log V) with Min-Heap. Preferred for dense graphs with many edges.",
        "time_complexity": "Kruskal: O(E log E) · Prim: O((V + E) log V)",
        "space_complexity": "O(V + E) auxiliary memory",
        "video_url": "https://www.youtube.com/embed/4ZlRH0eK-qE",
        "video_title": "Prim's and Kruskal's Minimum Spanning Tree",
        "visualization_type": "graph",
        "visualization_algorithm": "dijkstra",
        "practice_problem_slug": "two-sum",
        "java_code": """// Kruskal's MST using sorting + DSU
import java.util.*;
public class KruskalDemo {
    public static int kruskalMST(int V, int[][] edges) {
        Arrays.sort(edges, Comparator.comparingInt(a -> a[2]));
        // Uses DSU to add edge if union returns true
        return 0;
    }
}""",
        "python_code": """def kruskal(v, edges):
    edges.sort(key=lambda x: x[2]) # sort by weight
    # greedily union components
    return edges"""
    },
    {
        "id": "concept_fenwick_tree_bit",
        "category": "Advanced Data Structures",
        "difficulty": "Advanced",
        "title": "Fenwick Tree (Binary Indexed Tree / BIT)",
        "prerequisites": "Bit Manipulation, Prefix Sums",
        "summary": "Maintain prefix sums and point updates on dynamic arrays in O(log n) time using binary least significant bit (LSB) offsets.",
        "why_learn_it": "Provides the same logarithmic prefix functionality as Segment Trees but requires only half the memory and 10 lines of code.",
        "fundamental_explanation": "Each index i is responsible for an interval of size `i & (-i)` (its lowest set bit). Jumping by `i += i & (-i)` updates tree; jumping by `i -= i & (-i)` queries prefix sum.",
        "core_theory": "### Two Magic Bit Loops:\n1. Update: `while (i <= n) { tree[i] += delta; i += i & (-i); }`\n2. Query: `while (i > 0) { sum += tree[i]; i -= i & (-i); }`",
        "time_complexity": "Point Update: O(log n) · Prefix Query: O(log n) · Space: O(n)",
        "space_complexity": "O(n) exact array length",
        "video_url": "https://www.youtube.com/embed/uSFzHCZ4E-8",
        "video_title": "Fenwick Tree Binary Indexed Tree Visualized",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """public class FenwickTree {
    int[] bit;
    int n;
    public FenwickTree(int n) { this.n = n; bit = new int[n + 1]; }
    public void add(int i, int delta) {
        for (; i <= n; i += i & (-i)) bit[i] += delta;
    }
    public int query(int i) {
        int sum = 0;
        for (; i > 0; i -= i & (-i)) sum += bit[i];
        return sum;
    }
}""",
        "python_code": """class FenwickTree:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)
    def add(self, i: int, delta: int) -> None:
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)
    def query(self, i: int) -> int:
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s"""
    },
    {
        "id": "concept_suffix_trees_arrays",
        "category": "Advanced Data Structures",
        "difficulty": "Advanced",
        "title": "Suffix Trees & Suffix Arrays (Genomics & Full-Text Search)",
        "prerequisites": "Tries, String Hashing",
        "summary": "Compact index of all suffixes of a string enabling O(P) pattern search, longest repeated substring, and genomic sequence searches.",
        "why_learn_it": "Powers full-text search engines (Lucene), DNA sequence alignment in bioinformatics (BLAST), and compression (Bzip2).",
        "fundamental_explanation": "A Suffix Array is a sorted array of all suffixes of a string. Combined with the Longest Common Prefix (LCP) array, it answers substring queries in O(P + log N).",
        "core_theory": "### Space Advantage\nA Suffix Array is simply an array of integers representing suffix start indices, requiring O(N) integer memory compared to O(N * Σ) node pointers in Suffix Trees.",
        "time_complexity": "Construction: O(N log N) · Pattern Search: O(P log N)",
        "space_complexity": "O(N) integer array",
        "video_url": "https://www.youtube.com/embed/VpbcB_vWwT4",
        "video_title": "Suffix Array Construction & Search",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class SuffixArrayDemo {
    public static Integer[] buildSuffixArray(String s) {
        int n = s.length();
        Integer[] sa = new Integer[n];
        for (int i = 0; i < n; i++) sa[i] = i;
        Arrays.sort(sa, (a, b) -> s.substring(a).compareTo(s.substring(b)));
        return sa;
    }
}""",
        "python_code": """def build_suffix_array(s: str) -> list[int]:
    # Returns sorted indices of all suffixes
    return sorted(range(len(s)), key=lambda i: s[i:])"""
    },
    {
        "id": "concept_multithreaded_concurrency",
        "category": "Problem Solving Techniques",
        "difficulty": "Advanced",
        "title": "Multi-threaded Algorithms & Concurrency (Race Conditions & Locks)",
        "prerequisites": "Functions, Call Stack",
        "summary": "Understand thread parallelism, race conditions, atomic operations, mutex locks, and fork-join parallel divide and conquer.",
        "why_learn_it": "Modern server hardware features 64+ CPU cores; writing multi-threaded concurrent algorithms maximizes hardware utilization.",
        "fundamental_explanation": "Threads share process heap memory but maintain independent call stacks. Synchronization primitives (Mutex, Semaphore) prevent conflicting simultaneous writes.",
        "core_theory": "### Concurrency Hazards\n- **Race Condition:** Two threads read/write shared state concurrently.\n- **Deadlock:** Thread A holds Lock 1 and waits for Lock 2; Thread B holds Lock 2 and waits for Lock 1.\n- **Fork-Join Parallelism:** Divide task recursively across worker thread pools.",
        "time_complexity": "Speedup bounded by Amdahl's Law",
        "space_complexity": "Stack memory per thread",
        "video_url": "https://www.youtube.com/embed/r_MbozD32eo",
        "video_title": "Multi-threading and Concurrency in 5 Minutes",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.concurrent.atomic.AtomicInteger;
public class ConcurrencyDemo {
    private static AtomicInteger counter = new AtomicInteger(0);
    public static void increment() {
        counter.incrementAndGet(); // Thread-safe atomic operation
    }
}""",
        "python_code": """import threading
counter = 0
lock = threading.Lock()

def safe_increment():
    global counter
    with lock: # Acquire mutex lock
        counter += 1"""
    }
]

def seed_roadmap_sh():
    db = SessionLocal()
    try:
        print(f"Seeding {len(ROADMAP_CONCEPTS)} roadmap.sh concepts...")
        for i, c in enumerate(ROADMAP_CONCEPTS):
            step_num = 100 + i + 1
            lesson = db.query(Lesson).filter(Lesson.id == c["id"]).first()
            if not lesson:
                lesson = Lesson(
                    id=c["id"],
                    topic_id="dsa_arrays_101",
                    category=c["category"],
                    difficulty=c["difficulty"],
                    title=c["title"],
                    summary=c["summary"],
                    fundamental_explanation=c["fundamental_explanation"],
                    step_by_step=c["core_theory"],
                    real_world_applications=c["why_learn_it"],
                    examples_illustrations=c["fundamental_explanation"],
                    pseudocode=c.get("python_code", ""),
                    time_complexity=c["time_complexity"],
                    space_complexity=c["space_complexity"],
                    prerequisites=c["prerequisites"],
                    related_concepts=c["category"],
                    video_url=c["video_url"],
                    video_title=c["video_title"],
                    visualization_type=c["visualization_type"],
                    visualization_algorithm=c["visualization_algorithm"],
                    practice_problem_slug=c["practice_problem_slug"],
                    order_index=step_num * 10,
                    step_number=step_num,
                    stage_name=c["category"],
                    level_number=1 if c["difficulty"] == "Beginner" else 2 if c["difficulty"] == "Intermediate" else 3,
                    level_title=f"{c['category']} ({c['difficulty']})",
                    why_learn_it=c["why_learn_it"],
                    core_theory=c["core_theory"],
                    dry_run=json.dumps([
                        {"step": 1, "action": f"Initialize {c['title']}", "variables": {"status": "start"}, "notes": "Set up algorithmic state."},
                        {"step": 2, "action": "Execute core invariant operations", "variables": {"iteration": 1, "state": "processing"}, "notes": "Process data element."},
                        {"step": 3, "action": "Finalize execution", "variables": {"result": "complete"}, "notes": "Achieved optimal output."}
                    ]),
                    java_code=c["java_code"],
                    python_code=c["python_code"],
                    practice_questions=json.dumps([
                        {"difficulty": c["difficulty"], "title": f"Practice: {c['title']}", "description": c["summary"]}
                    ]),
                    ai_hints=json.dumps([
                        {"level": 1, "title": "Conceptual Clue", "hint": f"Consider how {c['title']} addresses the core problem constraints."},
                        {"level": 2, "title": "Algorithmic Strategy", "hint": f"Invariants dictate {c['time_complexity']}."},
                        {"level": 3, "title": "Implementation Pseudocode", "hint": c.get("python_code", "")[:120] + "..."}
                    ]),
                    common_mistakes="1. Off-by-one errors in boundary loops.\n2. Incomplete handling of edge cases.\n3. Excessive auxiliary memory overhead.",
                    concept_connections=json.dumps({
                        "prerequisites": [c["prerequisites"]],
                        "category": c["category"]
                    }),
                    quiz_questions=json.dumps([
                        {
                            "id": 1,
                            "question": f"What is the key advantage of {c['title']}?",
                            "options": [
                                f"Provides optimal performance: {c['time_complexity']}",
                                "Consumes zero memory space",
                                "Only operates on sorted lists",
                                "Disables CPU interrupts"
                            ],
                            "correct_idx": 0,
                            "explanation": f"{c['title']} offers optimal complexity {c['time_complexity']}."
                        },
                        {
                            "id": 2,
                            "question": f"What is the space complexity of {c['title']}?",
                            "options": ["O(1)", c["space_complexity"], "O(N²)", "O(N!)"],
                            "correct_idx": 1,
                            "explanation": f"Space complexity is {c['space_complexity']}."
                        }
                    ]),
                    mastery_threshold=70
                )
                db.add(lesson)
            else:
                lesson.category = c["category"]
                lesson.difficulty = c["difficulty"]
                lesson.title = c["title"]
                lesson.summary = c["summary"]
                lesson.fundamental_explanation = c["fundamental_explanation"]
                lesson.step_by_step = c["core_theory"]
                lesson.real_world_applications = c["why_learn_it"]
                lesson.why_learn_it = c["why_learn_it"]
                lesson.core_theory = c["core_theory"]
                lesson.java_code = c["java_code"]
                lesson.python_code = c["python_code"]
                lesson.video_url = c["video_url"]
                lesson.video_title = c["video_title"]
                lesson.time_complexity = c["time_complexity"]
                lesson.space_complexity = c["space_complexity"]
                lesson.prerequisites = c["prerequisites"]

        db.commit()
        print("Roadmap.sh concepts successfully seeded into AlgoMentor!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_roadmap_sh()
