"""
Master Seed Script for AlgoMentor: 12-Level Connected DSA Learning System
Implements the 18-part educational architecture for every concept with:
1. Introduction
2. Why Learn It?
3. Prerequisites
4. Core Theory
5. Visual Explanation / Visualizer Link
6. Dry Run State Machine (interactive steps & variable snapshots)
7. Java Implementation (line-by-line annotations)
8. Python Implementation (line-by-line annotations)
9. Complexity Analysis (Time & Space)
10. Basic Practice
11. Intermediate Practice
12. Advanced Practice
13. 3-Level AI Hints (Conceptual -> Algorithmic -> Pseudocode)
14. Common Student Mistakes & Pitfalls
15. Concept Connections (Prerequisites, Graph Edges, Real World)
16. Assessment Quiz (Interactive 3-question MCQ with scoring)
17. Mastery Checkpoint (Threshold evaluation)
18. Next Concept Unlocking
"""

import json
import sqlite3
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.lesson import Lesson, UserLessonProgress
from app.models.roadmap import RoadmapTopic, RoadmapStream
from app.models.user import User

def migrate_db_columns():
    """Ensure all required columns exist in SQLite database without losing data."""
    conn = sqlite3.connect("algomentor.db")
    c = conn.cursor()
    
    def add_col(table, col, col_type):
        c.execute(f"PRAGMA table_info({table})")
        cols = [r[1] for r in c.fetchall()]
        if col not in cols:
            c.execute(f"ALTER TABLE {table} ADD COLUMN {col} {col_type}")
            print(f"Added column {col} to {table}")

    cols_to_add = [
        ("category", "VARCHAR(50) DEFAULT 'dsa'"),
        ("step_number", "INTEGER DEFAULT 1"),
        ("stage_name", "VARCHAR(100) DEFAULT 'Core Foundations'"),
        ("level_number", "INTEGER DEFAULT 1"),
        ("level_title", "VARCHAR(100) DEFAULT 'Level 1: Programming Foundations'"),
        ("why_learn_it", "TEXT DEFAULT ''"),
        ("core_theory", "TEXT DEFAULT ''"),
        ("dry_run", "TEXT DEFAULT '[]'"),
        ("java_code", "TEXT DEFAULT ''"),
        ("python_code", "TEXT DEFAULT ''"),
        ("practice_questions", "TEXT DEFAULT '[]'"),
        ("ai_hints", "TEXT DEFAULT '[]'"),
        ("common_mistakes", "TEXT DEFAULT ''"),
        ("concept_connections", "TEXT DEFAULT '{}'"),
        ("quiz_questions", "TEXT DEFAULT '[]'"),
        ("mastery_threshold", "INTEGER DEFAULT 70"),
        ("prev_lesson_id", "VARCHAR(100)"),
        ("next_lesson_id", "VARCHAR(100)"),
    ]
    for col, ctype in cols_to_add:
        add_col("lessons", col, ctype)

    user_prog_cols = [
        ("quiz_score", "INTEGER DEFAULT 0"),
        ("mastery_level", "VARCHAR(50) DEFAULT 'not_started'"),
    ]
    for col, ctype in user_prog_cols:
        add_col("user_lesson_progress", col, ctype)

    conn.commit()
    conn.close()
    print("Database columns migrated successfully.")

CURRICULUM_DATA = [
    # ==========================================
    # LEVEL 1: PROGRAMMING FOUNDATIONS
    # ==========================================
    {
        "id": "lesson_py_memory",
        "topic_id": "py_topic_memory",
        "category": "python",
        "level_number": 1,
        "level_title": "Level 1: Programming Foundations",
        "title": "Python & Memory Architecture: Stack, Heap & References",
        "summary": "Understand how computer memory works, value vs reference semantics, and how Python handles object allocations.",
        "fundamental_explanation": "In computer memory, variables don't hold the actual data for complex structures—they hold memory addresses (references) that point to objects on the Heap. When you write a = [1, 2], 'a' is a pointer in Stack memory pointing to a list object allocated on the Heap. Assigning b = a does NOT copy the array; it copies the pointer! Both 'a' and 'b' now point to the exact same list in memory. Modifying b will silently mutate a.",
        "why_learn_it": "Without understanding memory references and aliasing, 90% of beginners create catastrophic bugs when implementing Linked Lists, Trees, Graph traversals, and dynamic arrays. You must know what is copied by value versus by reference.",
        "prerequisites": "Variables, primitive data types (int, float, bool)",
        "related_concepts": "Pointers in C/C++, Java References, Garbage Collection",
        "core_theory": "### 1. Stack vs Heap Memory\n- **Stack Memory:** High-speed, contiguous memory for function frames, call frames, and primitive variables. Automatically managed.\n- **Heap Memory:** Dynamic memory where complex objects (lists, dictionaries, tree nodes) reside.\n\n### 2. Mutability vs Immutability\n- **Immutable:** Integers, floats, strings, tuples. Re-assignment creates a NEW object.\n- **Mutable:** Lists, dicts, sets, custom class instances. Modifications alter memory in-place.\n\n### 3. Shallow vs Deep Copying\n- `copy.copy(x)` duplicates the container, but elements inside still share memory addresses.\n- `copy.deepcopy(x)` recursively duplicates the entire hierarchy.",
        "time_complexity": "Reference Assignment: O(1) · Deep Copy: O(n)",
        "space_complexity": "Stack: O(1) per frame · Heap: O(n)",
        "visualization_type": "linked_list",
        "visualization_algorithm": "linked_list",
        "video_url": "https://www.youtube.com/embed/m9n2b0_HpxE",
        "video_title": "Python Memory Model & Mutable References Explained",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Initialize `a = [10, 20]`", "variables": {"a_ptr": "0x100A", "val": "[10, 20]"}, "notes": "List created on Heap at 0x100A. 'a' points to 0x100A."},
            {"step": 2, "action": "Assign `b = a`", "variables": {"a_ptr": "0x100A", "b_ptr": "0x100A"}, "notes": "No new list is created! Both 'a' and 'b' hold pointer 0x100A."},
            {"step": 3, "action": "Execute `b.append(30)`", "variables": {"Heap[0x100A]": "[10, 20, 30]"}, "notes": "Heap object mutated in place."},
            {"step": 4, "action": "Inspect `a`", "variables": {"a": "[10, 20, 30]"}, "notes": "'a' also reflects 30 because it reads from 0x100A!"}
        ]),
        "java_code": """// Java Reference Semantics
public class MemoryExample {
    public static void main(String[] args) {
        // 'listA' is a 64-bit reference stored on the call stack
        java.util.ArrayList<Integer> listA = new java.util.ArrayList<>();
        listA.add(10);
        listA.add(20);
        
        // Copies the memory address, NOT the contents!
        java.util.ArrayList<Integer> listB = listA;
        listB.add(30);
        
        System.out.println("listA size: " + listA.size()); // Prints 3!
    }
}""",
        "python_code": """# Python Reference Semantics
def demonstrate_memory():
    # 'a' holds memory reference to list on Heap
    a = [10, 20]
    
    # Aliasing: 'b' points to identical memory address
    b = a
    b.append(30)
    
    print(f"a: {a}") # Output: [10, 20, 30]
    print(f"id(a) == id(b): {id(a) == id(b)}") # Output: True

demonstrate_memory()""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Check Reference Identity", "description": "Write a snippet to verify if two variables point to identical memory addresses using `is` in Python or `==` on objects in Java."},
            {"difficulty": "Intermediate", "title": "Implement Deep Copy for a Matrix", "description": "Given a 2D matrix (list of lists), write a function to create an independent clone without using the copy module."},
            {"difficulty": "Advanced", "title": "Circular Reference Detector", "description": "Explain how garbage collectors handle circular references when Node A points to Node B, and Node B points to Node A."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Think of variables as labels attached to boxes, rather than the boxes themselves. Multiple labels can stick to one box."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Use id(x) or is operator to check if two variables reference the exact same memory location."},
            {"level": 3, "title": "Pseudocode", "hint": "if variable_a is variable_b: return 'Shared Memory' else: return 'Independent Copy'"}
        ]),
        "common_mistakes": "1. Modifying a default argument in Python: `def add_node(item, path=[]): path.append(item)` creates a single persistent list across all function invocations!\n2. Confusing shallow copy (`list.copy()`) with deep copy when dealing with nested lists or 2D grids.\n3. Assuming `x = y` creates an independent copy in Java or Python.",
        "concept_connections": json.dumps({
            "prerequisites": ["Variables", "Data Types"],
            "current": "Memory Model & References",
            "next": "lesson_time_complexity",
            "advanced": ["Linked Lists", "Trees", "Graph Adjacency Lists"],
            "real_world": "High-performance cache engines, game physics state management, GC tuning"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What happens in memory when you execute `list2 = list1` in Python?",
                "options": [
                    "A duplicate list with identical elements is created at a new Heap address",
                    "A new reference pointer is created on the Stack pointing to the same Heap address",
                    "The elements are frozen into an immutable tuple",
                    "A shallow copy is automatically instantiated"
                ],
                "correct_idx": 1,
                "explanation": "Assignment copies the reference (memory address), not the underlying object on the heap."
            },
            {
                "id": 2,
                "question": "Which of the following data types in Python is IMMUTABLE?",
                "options": ["List", "Dictionary", "Set", "Tuple"],
                "correct_idx": 3,
                "explanation": "Tuples cannot be altered after creation. Modifying a tuple requires creating a new tuple object."
            },
            {
                "id": 3,
                "question": "Why is `def func(lst=[])` dangerous in Python?",
                "options": [
                    "It causes a syntax compilation error in modern Python",
                    "The default list is instantiated once at function definition and shared across subsequent calls",
                    "It consumes stack memory instead of heap memory",
                    "It prevents garbage collection of the entire program"
                ],
                "correct_idx": 1,
                "explanation": "Default parameter values are evaluated once when the function is defined, making mutable defaults act like shared persistent state."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_time_complexity",
        "topic_id": "dsa_arrays_101",
        "category": "dsa",
        "level_number": 1,
        "level_title": "Level 1: Programming Foundations",
        "title": "Time & Space Complexity: Big-O, Big-Ω & Big-Θ",
        "summary": "Master asymptotic analysis to calculate how execution time and memory scale as input size n grows to millions.",
        "fundamental_explanation": "We cannot measure code speed by wall-clock seconds because hardware differences, CPU throttling, and background processes distort measurements. Instead, Computer Science measures runtime growth relative to input size n. Big-O describes the mathematical upper bound (worst-case scenario), Big-Omega (Ω) describes the lower bound (best-case), and Big-Theta (Θ) describes the tight bound.",
        "why_learn_it": "A program running in O(n²) might take 3 milliseconds for 100 items, but for 1,000,000 items, it will take 11.5 days! An O(n log n) algorithm handles that same million in 0.02 seconds. Complexity analysis lets you predict performance before writing a single line of production code.",
        "prerequisites": "lesson_py_memory",
        "related_concepts": "Recurrence Relations, Master Theorem, Amortized Analysis",
        "core_theory": "### Common Complexity Classes:\n1. **O(1) Constant:** Accessing array by index, hash map lookup (average).\n2. **O(log n) Logarithmic:** Binary Search, Balanced BST operations. Halves problem size each step.\n3. **O(n) Linear:** Single pass loop over array of size n.\n4. **O(n log n) Linearithmic:** Merge Sort, Quick Sort (average), Heap Sort.\n5. **O(n²) Quadratic:** Nested loops, Bubble Sort, Selection Sort.\n6. **O(2ⁿ) Exponential:** Recursive Fibonacci without memoization, generating all subsets.\n7. **O(n!) Factorial:** Generating all permutations, Traveling Salesperson brute force.",
        "time_complexity": "Theoretical Analysis: O(1)",
        "space_complexity": "Auxiliary Space vs Input Space",
        "visualization_type": "searching",
        "visualization_algorithm": "binary_search",
        "video_url": "https://www.youtube.com/embed/D6xkbGLQesk",
        "video_title": "Big O Notation — Full Analysis in 15 Minutes",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Analyze single loop `for i in range(n)`", "variables": {"iterations": "n"}, "notes": "Executes n times -> O(n)"},
            {"step": 2, "action": "Analyze nested loop `for j in range(n)` inside loop i", "variables": {"total_ops": "n * n"}, "notes": "n * n iterations -> O(n²)"},
            {"step": 3, "action": "Analyze halving loop `while n > 1: n //= 2`", "variables": {"steps": "log₂(n)"}, "notes": "Divide by 2 each step -> O(log n)"}
        ]),
        "java_code": """// Calculating Time Complexity
public class ComplexityDemo {
    // O(n) Time | O(1) Auxiliary Space
    public static int sumArray(int[] arr) {
        int sum = 0; // O(1) space
        for (int x : arr) { // executes n times
            sum += x;
        }
        return sum;
    }
}""",
        "python_code": """# Time Complexity Examples
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    # Each iteration divides search space by 2 -> O(log n) Time
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1 # O(1) Space""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Calculate Loop Complexity", "description": "Identify Big-O for a loop incrementing by `i *= 2` until reaching n."},
            {"difficulty": "Intermediate", "title": "Space Complexity of Recursive Calls", "description": "Calculate auxiliary space consumed by recursive depth n on the Call Stack."},
            {"difficulty": "Advanced", "title": "Master Theorem Application", "description": "Solve the recurrence relation T(n) = 2T(n/2) + O(n)."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Count how many times the core operation executes as n doubles."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "If a problem size is halved repeatedly, it is logarithmic O(log n). If it doubles every level, it is exponential O(2ⁿ)."},
            {"level": 3, "title": "Pseudocode", "hint": "Identify: Outer loop (n steps) * Inner loop (m steps) = O(n * m)"}
        ]),
        "common_mistakes": "1. Dropping non-dominant terms too early.\n2. Confusing Space Complexity (auxiliary memory) with Input Space.\n3. Assuming recursive functions use O(1) space when the Call Stack actually consumes O(depth) memory.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_py_memory"],
            "current": "Time & Space Complexity",
            "next": "lesson_arrays_basics",
            "advanced": ["Amortized Complexity", "Master Theorem"],
            "real_world": "Database query optimization, API latency budgeting"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the Big-O time complexity of searching for an element in an unsorted array of size n?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "correct_idx": 2,
                "explanation": "In an unsorted array, you may need to inspect all n elements in the worst case (Linear Search: O(n))."
            },
            {
                "id": 2,
                "question": "If a function cuts its remaining search space in half during every iteration, what is its time complexity?",
                "options": ["O(n)", "O(log n)", "O(n²)", "O(1)"],
                "correct_idx": 1,
                "explanation": "Repeatedly dividing by 2 yields log₂(n) total steps, which is O(log n)."
            },
            {
                "id": 3,
                "question": "What is the auxiliary space complexity of an in-place Bubble Sort?",
                "options": ["O(n)", "O(n²)", "O(1)", "O(log n)"],
                "correct_idx": 2,
                "explanation": "In-place algorithms modify the input array using only a few constant temporary variables, requiring O(1) extra space."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 2: BASIC DATA STRUCTURES
    # ==========================================
    {
        "id": "lesson_arrays_basics",
        "topic_id": "dsa_arrays_101",
        "category": "dsa",
        "level_number": 2,
        "level_title": "Level 2: Basic Data Structures",
        "title": "Arrays, Dynamic Arrays & Memory Contiguity",
        "summary": "Discover why arrays have O(1) indexing, how CPU caches exploit contiguous memory, and how dynamic array doubling works.",
        "fundamental_explanation": "An array is a contiguous block of memory cells where each element occupies a fixed number of bytes. Because cells are physically adjacent, the computer calculates the address of index `i` instantaneously using the formula: `Address(i) = BaseAddress + (i * ElementSize)`. This gives arrays lightning-fast O(1) random access. However, inserting or deleting at index 0 requires shifting every subsequent element right or left, costing O(n) time.",
        "why_learn_it": "Arrays are the fundamental building block of almost every higher-level structure in computing: Hash Tables, Strings, Matrices, Heaps, and Ring Buffers are all built on top of arrays. Understanding their contiguous memory layout explains why CPU cache lines love them.",
        "prerequisites": "lesson_time_complexity",
        "related_concepts": "Strings, ArrayList in Java, Vectors in C++, Matrix Operations",
        "core_theory": "### 1. Fixed Arrays vs Dynamic Arrays\n- Static arrays (like `int[]` in C/Java) have fixed capacity allocated at compilation or initialization.\n- Dynamic arrays (`std::vector`, `ArrayList`, Python `list`) automatically resize when full by allocating a new array of 2x capacity and copying elements over.\n\n### 2. Amortized O(1) Insertion\n- Doubling capacity takes O(n) work, but happens so infrequently (after 1, 2, 4, 8, 16... inserts) that the average cost per insertion remains O(1) amortized.",
        "time_complexity": "Index Access: O(1) · Search: O(n) · Insert/Delete at End: O(1) amortized · Insert at Beginning: O(n)",
        "space_complexity": "O(n) memory space",
        "visualization_type": "sorting",
        "visualization_algorithm": "bubble_sort",
        "video_url": "https://www.youtube.com/embed/7m1Gekj_n0k",
        "video_title": "Data Structures: Arrays and Dynamic Resizing",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Dynamic array initialized with capacity = 2, size = 0", "variables": {"cap": 2, "size": 0, "arr": "[_, _]"}, "notes": "Heap allocates 2 slots."},
            {"step": 2, "action": "append(10) -> placed at index 0", "variables": {"cap": 2, "size": 1, "arr": "[10, _]"}, "notes": "O(1) operation."},
            {"step": 3, "action": "append(20) -> placed at index 1", "variables": {"cap": 2, "size": 2, "arr": "[10, 20]"}, "notes": "Capacity full!"},
            {"step": 4, "action": "append(30) triggers 2x resize", "variables": {"new_cap": 4, "copied": "[10, 20, 30, _]"}, "notes": "Allocates 4 slots, copies old elements, appends 30."}
        ]),
        "java_code": """// Java Dynamic Array (ArrayList)
import java.util.ArrayList;

public class ArrayDemo {
    public static void main(String[] args) {
        // Fast O(1) access by index
        int[] fixedArr = new int[5];
        fixedArr[0] = 42;
        
        // Resizable Dynamic Array
        ArrayList<Integer> dynArr = new ArrayList<>(2);
        dynArr.add(10); // O(1) amortized
        dynArr.add(20);
        dynArr.add(30); // triggers capacity doubling
        
        System.out.println("Element at 1: " + dynArr.get(1)); // O(1)
    }
}""",
        "python_code": """# Python Dynamic Array Internals
import sys

def inspect_dynamic_array():
    lst = []
    print(f"Empty list size: {sys.getsizeof(lst)} bytes")
    
    for i in range(10):
        lst.append(i)
        print(f"Length: {len(lst)}, Allocated Bytes: {sys.getsizeof(lst)}")

inspect_dynamic_array()""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Reverse an Array In-Place", "description": "Given an array, reverse its elements without allocating another array."},
            {"difficulty": "Intermediate", "title": "Rotate Array by K Positions", "description": "Rotate an array to the right by k steps in O(n) time and O(1) space."},
            {"difficulty": "Advanced", "title": "Maximum Subarray (Kadane's Algorithm)", "description": "Find the contiguous subarray with the largest sum in O(n) linear time."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Use two pointers from opposite ends: left at 0 and right at n-1."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Swap elements at left and right, then advance left and decrement right until they meet in the middle."},
            {"level": 3, "title": "Pseudocode", "hint": "while left < right: swap(arr[left], arr[right]); left++; right--"}
        ]),
        "common_mistakes": "1. IndexOutOfBoundsException when using `<= len(arr)` instead of `< len(arr)`.\n2. Inefficiently inserting at index 0 repeatedly in a loop, resulting in unintentional O(n²) complexity.\n3. Deleting elements while iterating forward in the same loop without adjusting the index.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_time_complexity"],
            "current": "Arrays & Dynamic Arrays",
            "next": "lesson_strings_basics",
            "advanced": ["Two Pointers", "Sliding Window", "Prefix Sums"],
            "real_world": "Image pixel buffers, network packet buffers, audio samples"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "Why can an array access an element at index i in O(1) constant time?",
                "options": [
                    "Because it uses binary search internally",
                    "Because elements are stored contiguously and their memory address is computed via arithmetic",
                    "Because all arrays are cached in CPU registers permanently",
                    "Because elements are stored in a hash map index"
                ],
                "correct_idx": 1,
                "explanation": "Address = BaseAddress + i * sizeOf(element), requiring a single multiplication and addition."
            },
            {
                "id": 2,
                "question": "What is the worst-case time complexity of inserting an element at index 0 of an array of size n?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                "correct_idx": 2,
                "explanation": "All n existing elements must be shifted one position to the right to make room at index 0."
            },
            {
                "id": 3,
                "question": "What is the amortized time complexity of appending an element to a dynamic array?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
                "correct_idx": 0,
                "explanation": "Although occasional resizing takes O(n), it happens exponentially less often, giving an amortized cost of O(1)."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_strings_basics",
        "topic_id": "dsa_arrays_101",
        "category": "dsa",
        "level_number": 2,
        "level_title": "Level 2: Basic Data Structures",
        "title": "String Manipulation, Immutability & StringBuilder",
        "summary": "Learn how strings are stored in memory, why string concatenation inside loops causes O(n²) slowdowns, and how to optimize with char arrays.",
        "fundamental_explanation": "In most modern languages (Java, Python, C#), strings are immutable sequences of characters. Once created on the Heap, their content cannot be changed. When you concatenate strings in a loop using `s += c`, the runtime must allocate a brand-new string and copy all existing characters every single iteration! Doing this n times turns an O(n) task into an O(n²) disaster. The solution is using mutable buffers (`StringBuilder` in Java or `list.append()` + `''.join()` in Python).",
        "why_learn_it": "String manipulation is tested in 40%+ of all technical interviews (palindromes, anagrams, parsing, regex, compression). Understanding character encodings (ASCII vs Unicode UTF-8) and buffer allocation prevents massive memory overhead.",
        "prerequisites": "lesson_arrays_basics",
        "related_concepts": "Tries, KMP Algorithm, Rolling Hash (Rabin-Karp)",
        "core_theory": "### 1. ASCII vs Unicode\n- ASCII represents 128 characters using 7 bits.\n- UTF-8 is a variable-width encoding (1 to 4 bytes per code point).\n\n### 2. Frequency Arrays for Anagrams\n- For lowercase English letters ('a' through 'z'), an integer array `int[26]` replaces heavy HashMaps, achieving O(1) space and zero hashing overhead!\n\n### 3. Palindrome Checking\n- Two pointers moving inward from both ends compare characters in O(n) time and O(1) space.",
        "time_complexity": "Length/Access: O(1) · Concatenation with buffer: O(1) amortized · Inefficient concat: O(n²)",
        "space_complexity": "O(n) auxiliary space",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "video_url": "https://www.youtube.com/embed/5mHYXJ2n2Qc",
        "video_title": "Strings and String Immutability Explained",
        "practice_problem_slug": "valid-anagram",
        "dry_run": json.dumps([
            {"step": 1, "action": "Check if 'racecar' is a palindrome", "variables": {"left": 0, "right": 6, "s[left]": "r", "s[right]": "r"}, "notes": "Match! Advance inward."},
            {"step": 2, "action": "Compare indices 1 and 5", "variables": {"left": 1, "right": 5, "s[left]": "a", "s[right]": "a"}, "notes": "Match! Advance inward."},
            {"step": 3, "action": "Compare indices 2 and 4", "variables": {"left": 2, "right": 4, "s[left]": "c", "s[right]": "c"}, "notes": "Match! Advance inward."},
            {"step": 4, "action": "Pointers cross at middle index 3 ('e')", "variables": {"left": 3, "right": 3}, "notes": "All matched -> True!"}
        ]),
        "java_code": """// Efficient String Building in Java
public class StringPerformance {
    // AVOID THIS: O(n²) due to string immutability
    public static String badConcat(int n) {
        String s = "";
        for (int i = 0; i < n; i++) s += i; 
        return s;
    }
    
    // USE THIS: O(n) linear using StringBuilder
    public static String goodConcat(int n) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < n; i++) sb.append(i);
        return sb.toString();
    }
}""",
        "python_code": """# Anagram Check using Frequency Array (O(n) time, O(1) space)
def is_anagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    
    count = [0] * 26
    for char_s, char_t in zip(s, t):
        count[ord(char_s) - ord('a')] += 1
        count[ord(char_t) - ord('a')] -= 1
        
    return all(x == 0 for x in count)

print(is_anagram("anagram", "nagaram")) # True""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Valid Palindrome", "description": "Check if a string reads the same forwards and backwards, ignoring non-alphanumeric characters."},
            {"difficulty": "Intermediate", "title": "Valid Anagram", "description": "Determine if two strings have identical characters with equal counts in O(n) time."},
            {"difficulty": "Advanced", "title": "Longest Palindromic Substring", "description": "Find the longest contiguous palindrome within a string using Expand Around Center in O(n²) time."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "To check anagrams without sorting (which takes O(n log n)), count the frequency of each character."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Use an array of size 26 indexed by `ord(c) - ord('a')`."},
            {"level": 3, "title": "Pseudocode", "hint": "Increment count for string A, decrement for string B; return True if all buckets equal 0."}
        ]),
        "common_mistakes": "1. Using `+=` concatenation in a large loop, causing massive heap allocations.\n2. Forgetting that `ord('a')` is needed to normalize character codes to 0-25.\n3. Creating extra substring copies unnecessarily.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_arrays_basics"],
            "current": "String Manipulation & Frequency Maps",
            "next": "lesson_linked_list",
            "advanced": ["Tries", "KMP Substring Search", "Rabin-Karp"],
            "real_world": "Text editors, search auto-complete, URL parsers, genetics DNA sequencing"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "Why is concatenating strings with `+=` inside an n-iteration loop an O(n²) operation?",
                "options": [
                    "Because strings are immutable, each concatenation creates a new string copying all previous characters",
                    "Because CPU caches disable string indexing",
                    "Because strings use double the memory of arrays",
                    "Because string lengths must be recomputed using linear scan"
                ],
                "correct_idx": 0,
                "explanation": "Since strings cannot be modified in place, each step creates a new string of size k and copies characters over (1 + 2 + ... + n = O(n²))."
            },
            {
                "id": 2,
                "question": "What is the optimal space complexity for checking if two strings of lowercase English letters are anagrams?",
                "options": ["O(n)", "O(1)", "O(n²)", "O(log n)"],
                "correct_idx": 1,
                "explanation": "An array of 26 integers is of constant size O(26) = O(1) regardless of how large string length n is."
            },
            {
                "id": 3,
                "question": "In Java, which class should you use to construct a string dynamically inside a loop?",
                "options": ["StringPool", "StringBuilder", "CharBufferPool", "ImmutableString"],
                "correct_idx": 1,
                "explanation": "StringBuilder maintains a mutable resizable buffer, providing amortized O(1) appends and total O(n) runtime."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_linked_list",
        "topic_id": "dsa_linked_lists",
        "category": "dsa",
        "level_number": 2,
        "level_title": "Level 2: Basic Data Structures",
        "title": "Singly & Doubly Linked Lists: Pointers & References",
        "summary": "Understand non-contiguous node chains, O(1) head insertion, pointer rewiring, and the Fast & Slow Pointer technique.",
        "fundamental_explanation": "Unlike arrays, Linked List nodes are scattered across random Heap locations. Each node stores two things: its data payload and a pointer (reference) to the next node. Because nodes don't need contiguous memory, a Linked List never has to reallocate or copy its entire contents to grow. Inserting at the head or after a known node is instantaneous O(1). However, accessing index i requires traversing node by node from head, costing O(n) time.",
        "why_learn_it": "Linked Lists are the basis of Queues, LRU Caches, Memory Allocators, and adjacency lists. They also train you in pointer manipulation—the exact skill needed for Binary Trees and Graphs.",
        "prerequisites": "lesson_py_memory",
        "related_concepts": "Doubly Linked List, Circular Linked List, LRU Cache, Binary Trees",
        "core_theory": "### 1. Singly vs Doubly Linked List\n- **Singly:** Each node points only to `next`. Traversing backwards is impossible.\n- **Doubly:** Each node points to `next` and `prev`. Allows O(1) deletion when given a pointer to the node.\n\n### 2. Sentinel (Dummy) Head Technique\n- Using a `dummy = ListNode(0, head)` eliminates annoying edge cases when deleting or inserting at the head of the list.\n\n### 3. Floyd's Cycle Detection (Tortoise and Hare)\n- Move slow pointer by 1 step and fast pointer by 2 steps. If a cycle exists, fast will inevitably lap slow inside the loop!",
        "time_complexity": "Prepend/Append (with tail): O(1) · Access by Index: O(n) · Search: O(n) · Delete with pointer: O(1) doubly",
        "space_complexity": "O(n) for nodes",
        "visualization_type": "linked_list",
        "visualization_algorithm": "linked_list",
        "video_url": "https://www.youtube.com/embed/njTh_OwMljA",
        "video_title": "Linked Lists Data Structure: Visual Guide",
        "practice_problem_slug": "reverse-linked-list",
        "dry_run": json.dumps([
            {"step": 1, "action": "Reverse list: 1 -> 2 -> 3 -> null", "variables": {"prev": "null", "curr": "1", "next_temp": "2"}, "notes": "Save curr.next, point 1 to null."},
            {"step": 2, "action": "Advance prev to 1, curr to 2", "variables": {"prev": "1", "curr": "2", "next_temp": "3"}, "notes": "Point 2.next to 1."},
            {"step": 3, "action": "Advance prev to 2, curr to 3", "variables": {"prev": "2", "curr": "3", "next_temp": "null"}, "notes": "Point 3.next to 2."},
            {"step": 4, "action": "curr reaches null; prev points to 3", "variables": {"prev": "3", "curr": "null"}, "notes": "3 is the new head! Return prev."}
        ]),
        "java_code": """// Java Singly Linked List Node and Reversal
class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

public class LinkedListOps {
    // Reverse linked list in O(n) time and O(1) auxiliary space
    public static ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nextTemp = curr.next; // store next node
            curr.next = prev;              // reverse pointer
            prev = curr;                   // move prev forward
            curr = nextTemp;               // move curr forward
        }
        return prev; // new head
    }
}""",
        "python_code": """# Python Linked List Node and Floyd's Cycle Detection
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def has_cycle(head: ListNode) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True # Tortoise and Hare met!
    return False # Reached end of list without cycle""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Reverse a Singly Linked List", "description": "Reverse a linked list in-place in O(n) time and O(1) space."},
            {"difficulty": "Intermediate", "title": "Detect Cycle (Floyd's Algorithm)", "description": "Given head of a linked list, determine if it has a cycle using O(1) memory."},
            {"difficulty": "Advanced", "title": "LRU Cache Implementation", "description": "Design a Least Recently Used (LRU) Cache with O(1) get and put using a Doubly Linked List and HashMap."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Maintain three pointers: prev, curr, and a temporary next pointer."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Before modifying curr.next, save its original target in nextTemp so you don't break the forward chain."},
            {"level": 3, "title": "Pseudocode", "hint": "nextTemp = curr.next; curr.next = prev; prev = curr; curr = nextTemp"}
        ]),
        "common_mistakes": "1. Losing the remaining list reference by overwriting `curr.next` before caching it in a temporary variable.\n2. NullPointerException when checking `fast.next.next` without first validating that `fast` and `fast.next` are non-null.\n3. Creating an accidental cycle when reversing.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_py_memory"],
            "current": "Linked Lists & Pointer Rewiring",
            "next": "lesson_binary_search",
            "advanced": ["LRU Cache", "Skip Lists", "Binary Trees"],
            "real_world": "Browser forward/back buttons, OS memory free lists, music playlist queues"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the primary advantage of a Linked List over an Array?",
                "options": [
                    "Random access in O(1) time",
                    "O(1) insertion and deletion at the head without shifting remaining elements",
                    "Lower memory footprint per element",
                    "Better utilization of CPU hardware cache lines"
                ],
                "correct_idx": 1,
                "explanation": "Adding or removing a node at the head is a simple pointer reassignment taking O(1) time with zero element shifting."
            },
            {
                "id": 2,
                "question": "How does Floyd's Cycle Detection algorithm achieve O(1) space?",
                "options": [
                    "By storing visited nodes in a hash set",
                    "By using two pointers moving at different speeds (1 step and 2 steps)",
                    "By modifying the values of nodes to negative integers",
                    "By reversing the list recursively"
                ],
                "correct_idx": 1,
                "explanation": "The fast pointer moves twice as fast as the slow pointer; if a cycle exists, they must collide within the loop."
            },
            {
                "id": 3,
                "question": "Why does a dummy (sentinel) head node help when implementing linked list deletions?",
                "options": [
                    "It cuts the memory consumption in half",
                    "It eliminates special-case logic for modifying or deleting the original head node",
                    "It enables random index access in O(1) time",
                    "It automatically prevents cycles"
                ],
                "correct_idx": 1,
                "explanation": "Having a permanent node before head ensures every node (including the real head) always has a predecessor."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 3: FUNDAMENTAL PROBLEM SOLVING
    # ==========================================
    {
        "id": "lesson_binary_search",
        "topic_id": "dsa_searching_101",
        "category": "algorithm",
        "level_number": 3,
        "level_title": "Level 3: Fundamental Problem-Solving Techniques",
        "title": "Searching Algorithms: Linear vs Binary Search & Invariants",
        "summary": "Master the O(log n) divide-and-conquer search, calculate midpoints safely to prevent integer overflow, and preserve loop invariants.",
        "fundamental_explanation": "If an array is unsorted, you have no choice but to examine items one by one (Linear Search, O(n)). But if the array is SORTED, each comparison with the middle element eliminates half of all remaining possibilities! For 1 billion items, Linear Search takes up to 1,000,000,000 comparisons, while Binary Search finds the answer in at most 30 comparisons (log₂(10⁹) ≈ 29.89).",
        "why_learn_it": "Binary search is not just for finding a number in an array. It is the core mechanism behind Database B-Trees, Git Bisect (finding which commit introduced a bug), and advanced algorithmic problems (Binary Search on Answer).",
        "prerequisites": "lesson_arrays_basics",
        "related_concepts": "Binary Search on Answer, Lower/Upper Bound, BST Search",
        "core_theory": "### 1. Loop Invariant\n- Keep track of the active search interval `[left, right]`.\n- Safe Midpoint Calculation: In Java/C++, `(left + right) / 2` can trigger a 32-bit integer overflow if both are large! Always use: `mid = left + (right - left) / 2`.\n\n### 2. Lower Bound vs Upper Bound\n- **Lower Bound:** First index where `arr[mid] >= target`.\n- **Upper Bound:** First index where `arr[mid] > target`.",
        "time_complexity": "Best: O(1) · Worst/Average: O(log n)",
        "space_complexity": "Iterative: O(1) · Recursive: O(log n) call stack",
        "visualization_type": "searching",
        "visualization_algorithm": "binary_search",
        "video_url": "https://www.youtube.com/embed/MFhxShGxHWc",
        "video_title": "Binary Search Algorithm: Step by Step Guide",
        "practice_problem_slug": "binary-search",
        "dry_run": json.dumps([
            {"step": 1, "action": "Search 23 in [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]", "variables": {"left": 0, "right": 9, "mid": 4, "arr[mid]": 16}, "notes": "16 < 23 -> Discard left half. Move left to 5."},
            {"step": 2, "action": "Search range is now [23, 38, 56, 72, 91]", "variables": {"left": 5, "right": 9, "mid": 7, "arr[mid]": 56}, "notes": "56 > 23 -> Discard right half. Move right to 6."},
            {"step": 3, "action": "Search range is now [23, 38]", "variables": {"left": 5, "right": 6, "mid": 5, "arr[mid]": 23}, "notes": "arr[mid] == 23! Target found at index 5."}
        ]),
        "java_code": """// Binary Search Implementation in Java
public class SearchAlgorithms {
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            // Avoid integer overflow bug
            int mid = left + (right - left) / 2;
            
            if (arr[mid] == target) {
                return mid; // Target found
            } else if (arr[mid] < target) {
                left = mid + 1; // Discard left half
            } else {
                right = mid - 1; // Discard right half
            }
        }
        return -1; // Target not found
    }
}""",
        "python_code": """# Python Binary Search with Lower Bound
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
            
    return -1

print(binary_search([2, 5, 8, 12, 16, 23, 38], 23)) # Returns 5""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Binary Search", "description": "Given a sorted array of distinct integers and a target, return its index in O(log n) time."},
            {"difficulty": "Intermediate", "title": "Search in Rotated Sorted Array", "description": "Find target in an array rotated at some pivot in O(log n) time."},
            {"difficulty": "Advanced", "title": "Koko Eating Bananas", "description": "Binary search on answer to find the minimum integer eating speed k to finish all bananas in h hours."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Binary search only works on monotone (sorted) spaces. Identify which half of the array cannot possibly contain the answer."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Calculate mid safely: left + (right - left) // 2. If target > arr[mid], move left = mid + 1."},
            {"level": 3, "title": "Pseudocode", "hint": "while left <= right: mid = (l+r)//2; if arr[mid]==target: return mid; elif arr[mid]<target: left=mid+1; else: right=mid-1"}
        ]),
        "common_mistakes": "1. Integer overflow from `(left + right) / 2` when values exceed 2³¹ - 1.\n2. Infinite loop caused by updating `left = mid` instead of `left = mid + 1`.\n3. Using Binary Search on an unsorted array.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_arrays_basics"],
            "current": "Binary Search",
            "next": "lesson_dsa_two_pointers",
            "advanced": ["Binary Search on Answer", "Median of Two Sorted Arrays"],
            "real_world": "Git bisect, Database B-Tree index scans, package version dependency resolution"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the maximum number of comparisons needed to find an element in a sorted array of 1,000,000 items using binary search?",
                "options": ["1,000,000", "500,000", "20", "1,000"],
                "correct_idx": 2,
                "explanation": "2²⁰ = 1,048,576 > 1,000,000. Therefore at most 20 comparisons are needed."
            },
            {
                "id": 2,
                "question": "Why is `int mid = left + (right - left) / 2` preferred over `(left + right) / 2` in Java and C++?",
                "options": [
                    "It calculates faster on x86 processors",
                    "It prevents 32-bit signed integer overflow when left + right exceeds Integer.MAX_VALUE",
                    "It rounds up instead of down",
                    "It avoids dividing by zero"
                ],
                "correct_idx": 1,
                "explanation": "If left and right are near 2 * 10⁹, their sum overflows the 32-bit signed integer limit into negative numbers."
            },
            {
                "id": 3,
                "question": "What condition MUST be met to apply standard binary search on an array?",
                "options": [
                    "The elements must be unique",
                    "The array must be sorted in monotonic order",
                    "The array size must be an exact power of 2",
                    "The array must contain positive integers only"
                ],
                "correct_idx": 1,
                "explanation": "Monotonicity (sorted order) is the invariant that allows discarding half the search space with certainty."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_dsa_two_pointers",
        "topic_id": "dsa_arrays_101",
        "category": "algorithm",
        "level_number": 3,
        "level_title": "Level 3: Fundamental Problem-Solving Techniques",
        "title": "Two Pointer Technique: Inward & Fast-Slow Patterns",
        "summary": "Convert O(n²) nested loop brute-force solutions into elegant O(n) linear scans using converging and directional pointers.",
        "fundamental_explanation": "Many problems that initially seem to require examining every pair of elements (nested loops: O(n²)) can be solved in a single pass (O(n)) by coordinating two pointers. In the Converging Pattern, pointers start at both ends (index 0 and index n-1) and move inward based on comparisons. In the Fast-Slow Pattern, both pointers move in the same direction at different speeds to partition elements or detect loops.",
        "why_learn_it": "Two Pointers is the single most tested algorithmic pattern in FAANG interviews for linear data structures (Two Sum II, 3Sum, Container With Most Water, Trapping Rain Water, Remove Duplicates).",
        "prerequisites": "lesson_arrays_basics",
        "related_concepts": "Sliding Window, Binary Search, QuickSort Partition",
        "core_theory": "### 1. Converging Pointers (Sorted Array)\n- For sorted array: If `arr[left] + arr[right] < target`, incrementing `left` increases the sum. If the sum is too large, decrementing `right` decreases the sum.\n\n### 2. Fast-Slow In-Place Partitioning\n- `slow` tracks the boundary of valid processed elements.\n- `fast` scans ahead. When condition matches, write `arr[slow] = arr[fast]` and advance `slow`.",
        "time_complexity": "O(n) time — each pointer moves at most n steps",
        "space_complexity": "O(1) auxiliary space",
        "visualization_type": "sorting",
        "visualization_algorithm": "selection_sort",
        "video_url": "https://www.youtube.com/embed/QzZBCvBtqGs",
        "video_title": "Two Pointer Technique: Master All Patterns",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Find target 9 in sorted [2, 7, 11, 15]", "variables": {"left": 0, "right": 3, "sum": 17}, "notes": "17 > 9 -> Sum too big! Decrement right."},
            {"step": 2, "action": "Check pointers", "variables": {"left": 0, "right": 2, "sum": 13}, "notes": "13 > 9 -> Sum still too big! Decrement right."},
            {"step": 3, "action": "Check pointers", "variables": {"left": 0, "right": 1, "sum": 9}, "notes": "Sum == 9! Match found at [0, 1]."}
        ]),
        "java_code": """// Two Sum II - Input Array Is Sorted (O(n) Time, O(1) Space)
public class TwoPointers {
    public static int[] twoSum(int[] numbers, int target) {
        int left = 0;
        int right = numbers.length - 1;
        
        while (left < right) {
            int currentSum = numbers[left] + numbers[right];
            if (currentSum == target) {
                return new int[]{left + 1, right + 1}; // 1-indexed
            } else if (currentSum < target) {
                left++; // Increase sum
            } else {
                right--; // Decrease sum
            }
        }
        return new int[]{-1, -1};
    }
}""",
        "python_code": """# Container With Most Water (Two Pointers O(n))
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0
    
    while left < right:
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)
        
        # Move the shorter line inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
            
    return max_water

print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7])) # Returns 49""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Two Sum II (Sorted)", "description": "Find two numbers in a sorted array that sum to target in O(n) time and O(1) space."},
            {"difficulty": "Intermediate", "title": "Container With Most Water", "description": "Find two vertical lines that together with the x-axis contain the most water."},
            {"difficulty": "Advanced", "title": "3Sum", "description": "Find all unique triplets [a, b, c] such that a + b + c = 0 in O(n²) time using sorting and two pointers."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Sort the array first if it's not sorted. Then for each element, run two pointers on the remainder."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Always advance the pointer that gives you a chance of finding a better answer."},
            {"level": 3, "title": "Pseudocode", "hint": "while left < right: if sum == target: return True; elif sum < target: left++; else: right--"}
        ]),
        "common_mistakes": "1. Forgetting to skip duplicate elements when finding unique triplets (like in 3Sum).\n2. Using `<=` instead of `<` in `while left < right`, leading to summing an element with itself.\n3. Applying converging pointers on an unsorted array.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_arrays_basics", "lesson_binary_search"],
            "current": "Two Pointer Technique",
            "next": "lesson_dsa_sliding_window",
            "advanced": ["3Sum / 4Sum", "Trapping Rain Water", "Sliding Window"],
            "real_world": "Merge phase in MergeSort, image compression edge detection, stream deduplication"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "Why is the Two Pointer approach on a sorted array faster than checking all pairs?",
                "options": [
                    "It reduces time from O(n²) to O(n) because each step discards an entire row/column of candidates",
                    "It utilizes SIMD vector registers in the CPU",
                    "It converts the problem into a hash set lookup",
                    "It executes in O(log n) time"
                ],
                "correct_idx": 0,
                "explanation": "Because the array is sorted, knowing the current sum tells you conclusively which pointer to advance without testing invalid combinations."
            },
            {
                "id": 2,
                "question": "In 'Container With Most Water', why do we move the pointer pointing to the shorter vertical line?",
                "options": [
                    "Because moving the taller line can only decrease or maintain the height, while reducing the width, guaranteeing less area",
                    "Because the shorter line is always closer to index 0",
                    "To prevent pointer crossover",
                    "It does not matter which pointer moves"
                ],
                "correct_idx": 0,
                "explanation": "The area is bounded by min(h_left, h_right) * width. Moving the taller line reduces width without any chance of increasing min height."
            },
            {
                "id": 3,
                "question": "What is the space complexity of solving Two Sum II using converging two pointers?",
                "options": ["O(n)", "O(1)", "O(log n)", "O(n²)"],
                "correct_idx": 1,
                "explanation": "The algorithm only tracks two integer index pointers, requiring O(1) auxiliary memory."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_dsa_sliding_window",
        "topic_id": "dsa_arrays_101",
        "category": "algorithm",
        "level_number": 3,
        "level_title": "Level 3: Fundamental Problem-Solving Techniques",
        "title": "Sliding Window Technique: Fixed vs Dynamic Windows",
        "summary": "Learn how to reuse computations between overlapping contiguous subarrays, turning O(n * k) problems into O(n) algorithms.",
        "fundamental_explanation": "Imagine calculating the sum of every contiguous block of k elements. The naive approach recalculates all k numbers for each of the (n - k + 1) windows: (n * k) operations. The Sliding Window insight: when moving the window one position right, you don't need to re-add all elements! Just subtract the element falling out of the left side, and add the new element entering the right side! WindowSum = WindowSum - arr[left] + arr[right]. That's two operations instead of k operations!",
        "why_learn_it": "Sliding Window is indispensable for streaming telemetry, network bandwidth rate limiters, audio DSP, and interview favorites (Longest Substring Without Repeating Characters, Minimum Size Subarray Sum).",
        "prerequisites": "lesson_dsa_two_pointers",
        "related_concepts": "Monotonic Queue, Prefix Sums, Two Pointers",
        "core_theory": "### 1. Fixed-Size Sliding Window\n- Window size `k` remains constant.\n- Expand right pointer until window size is k. Then slide window by incrementing both left and right together.\n\n### 2. Dynamically Resizable Sliding Window\n- Window expands `right` to satisfy a condition.\n- Once condition is violated (or optimal), contract `left` until condition is valid again.\n- Window size is `right - left + 1`.",
        "time_complexity": "O(n) time — right moves n steps, left moves at most n steps",
        "space_complexity": "O(1) auxiliary or O(k) for frequency tracking",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "video_url": "https://www.youtube.com/embed/MK-NZ4hN7Rs",
        "video_title": "Sliding Window Technique Explained",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Find max sum of subarray size k=3 in [2, 1, 5, 1, 3, 2]", "variables": {"window": "[2, 1, 5]", "sum": 8, "max": 8}, "notes": "Initial window."},
            {"step": 2, "action": "Slide window to include 1, remove 2", "variables": {"calc": "8 - 2 + 1", "sum": 7, "max": 8}, "notes": "Window is [1, 5, 1]."},
            {"step": 3, "action": "Slide window to include 3, remove 1", "variables": {"calc": "7 - 1 + 3", "sum": 9, "max": 9}, "notes": "Window is [5, 1, 3]. Max updated to 9."},
            {"step": 4, "action": "Slide window to include 2, remove 5", "variables": {"calc": "9 - 5 + 2", "sum": 6, "max": 9}, "notes": "Window is [1, 3, 2]. Final max is 9."}
        ]),
        "java_code": """// Fixed-Size Sliding Window: Max Sum Subarray of size K
public class SlidingWindow {
    public static int maxSumSubarray(int[] arr, int k) {
        int windowSum = 0;
        for (int i = 0; i < k; i++) {
            windowSum += arr[i];
        }
        
        int maxSum = windowSum;
        for (int i = k; i < arr.length; i++) {
            windowSum += arr[i] - arr[i - k]; // add incoming, drop outgoing
            maxSum = Math.max(maxSum, windowSum);
        }
        return maxSum;
    }
}""",
        "python_code": """# Dynamic Sliding Window: Longest Substring Without Repeating Characters
def length_of_longest_substring(s: str) -> int:
    char_index_map = {}
    left = 0
    max_len = 0
    
    for right, char in enumerate(s):
        if char in char_index_map and char_index_map[char] >= left:
            left = char_index_map[char] + 1 # jump left past duplicate
            
        char_index_map[char] = right
        max_len = max(max_len, right - left + 1)
        
    return max_len

print(length_of_longest_substring("abcabcbb")) # Returns 3 ("abc")""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Maximum Average Subarray I", "description": "Find contiguous subarray of length k with maximum average value in O(n) time."},
            {"difficulty": "Intermediate", "title": "Longest Substring Without Repeating Characters", "description": "Find length of longest substring without duplicate characters using dynamic window."},
            {"difficulty": "Advanced", "title": "Minimum Window Substring", "description": "Find smallest substring in s that contains all characters of t in O(n) time."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Expand right until the window is valid/invalid, then contract left."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Use a hash map or frequency array to keep track of character counts inside the current window."},
            {"level": 3, "title": "Pseudocode", "hint": "for right in range(n): add(arr[right]); while invalid(): remove(arr[left]); left++; max_len = max(max_len, right-left+1)"}
        ]),
        "common_mistakes": "1. Resetting left back to 0 on every step, turning an O(n) algorithm back into O(n²).\n2. Off-by-one error when calculating window size: it is `right - left + 1`, not `right - left`.\n3. Forgetting to update hash map index when jumping left.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_dsa_two_pointers"],
            "current": "Sliding Window Technique",
            "next": "lesson_bubble_sort",
            "advanced": ["Monotonic Queue", "Subarray Product Less Than K"],
            "real_world": "Network congestion rate limiting (Token Bucket), moving averages in financial stock charts"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the time complexity of the dynamic sliding window on an array of length n?",
                "options": ["O(n²)", "O(n)", "O(n log n)", "O(k)"],
                "correct_idx": 1,
                "explanation": "Even though there is an inner loop contracting left, both left and right pointers only move forward at most n times, giving 2n = O(n) operations."
            },
            {
                "id": 2,
                "question": "How do you calculate the current window length between indices left and right?",
                "options": ["right - left", "right - left + 1", "right + left", "(right - left) / 2"],
                "correct_idx": 1,
                "explanation": "Because both endpoints are inclusive, an interval [3, 5] contains indices 3, 4, 5 (length = 5 - 3 + 1 = 3)."
            },
            {
                "id": 3,
                "question": "When sliding a fixed-size window of size k to the right by 1, how is the sum updated?",
                "options": [
                    "By summing all k elements again",
                    "By adding arr[right] and subtracting arr[left - 1]",
                    "By multiplying the average by k",
                    "By shifting the array in memory"
                ],
                "correct_idx": 1,
                "explanation": "Reusing the prior sum by adding the new arrival and dropping the departed element takes O(1) time."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_bubble_sort",
        "topic_id": "dsa_sorting_101",
        "category": "algorithm",
        "level_number": 3,
        "level_title": "Level 3: Fundamental Problem-Solving Techniques",
        "title": "Sorting Foundations: Bubble, Selection & Insertion Sort",
        "summary": "Understand adjacent swaps, in-place partitions, stability in sorting, and early-exit optimizations.",
        "fundamental_explanation": "Sorting algorithms arrange unordered elements into non-decreasing order. In Bubble Sort, adjacent elements are repeatedly compared and swapped if out of order, causing larger elements to 'bubble up' to the right end on each pass. In Selection Sort, the smallest remaining element is found and swapped into place. In Insertion Sort, elements are inserted into an already-sorted left partition, just like sorting playing cards in your hand.",
        "why_learn_it": "While O(n²) sorting is too slow for millions of items, Insertion Sort is extremely fast for small arrays (n ≤ 16) and nearly sorted data. Java and Python's production sort engines (TimSort, Dual-Pivot QuickSort) use Insertion Sort as their base case!",
        "prerequisites": "lesson_arrays_basics",
        "related_concepts": "Merge Sort, Quick Sort, Stability in Sorting",
        "core_theory": "### 1. Stability in Sorting\n- A sorting algorithm is **Stable** if elements with identical keys appear in the same relative order in the output as they appeared in the input.\n- Bubble Sort: Stable. Selection Sort: Unstable (swapping over long distances can reorder identical keys). Insertion Sort: Stable.\n\n### 2. Early-Exit Optimization for Bubble Sort\n- Track a `swapped` boolean flag. If an entire pass completes with zero swaps, the array is already sorted! This achieves O(n) best-case time.",
        "time_complexity": "Bubble/Selection: O(n²) · Insertion Best-Case: O(n) · Space: O(1) in-place",
        "space_complexity": "O(1) auxiliary space",
        "visualization_type": "sorting",
        "visualization_algorithm": "bubble_sort",
        "video_url": "https://www.youtube.com/embed/xli_FI7Cuzw",
        "video_title": "Bubble Sort in 2 Minutes",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Pass 1 on [5, 1, 4, 2, 8]", "variables": {"compare": "5 > 1", "swap": "[1, 5, 4, 2, 8]"}, "notes": "5 swapped with 1."},
            {"step": 2, "action": "Compare 5 and 4", "variables": {"swap": "[1, 4, 5, 2, 8]"}, "notes": "5 swapped with 4."},
            {"step": 3, "action": "Compare 5 and 2", "variables": {"swap": "[1, 4, 2, 5, 8]"}, "notes": "5 swapped with 2."},
            {"step": 4, "action": "Compare 5 and 8", "variables": {"no_swap": "[1, 4, 2, 5, 8]"}, "notes": "8 is in place! End of Pass 1."}
        ]),
        "java_code": """// Optimized Bubble Sort in Java
public class SortingFoundations {
    public static void bubbleSort(int[] arr) {
        int n = arr.length;
        boolean swapped;
        for (int i = 0; i < n - 1; i++) {
            swapped = false;
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    swapped = true;
                }
            }
            // If no elements were swapped, array is sorted!
            if (!swapped) break;
        }
    }
}""",
        "python_code": """# Insertion Sort (O(n) best case, O(n²) worst case)
def insertion_sort(arr: list[int]) -> list[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        # Move elements of arr[0..i-1] that are greater than key forward
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

print(insertion_sort([64, 25, 12, 22, 11]))""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Sort Colors (Dutch National Flag)", "description": "Sort an array of 0s, 1s, and 2s in-place in O(n) one-pass using three pointers."},
            {"difficulty": "Intermediate", "title": "Insertion Sort on Linked List", "description": "Sort a singly linked list using insertion sort principles."},
            {"difficulty": "Advanced", "title": "Count Inversions", "description": "Calculate how far an array is from being sorted by counting inversion pairs."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "In each pass of Bubble Sort, the largest remaining unsorted element is placed at its final position at the end."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Use a boolean flag to terminate early if the array is already sorted."},
            {"level": 3, "title": "Pseudocode", "hint": "for i in 0..n-1: swapped=false; for j in 0..n-i-2: if a[j]>a[j+1]: swap; swapped=true; if not swapped: break"}
        ]),
        "common_mistakes": "1. Forgetting the `- i` in `j < n - 1 - i`, unnecessarily re-comparing already sorted elements at the tail.\n2. Thinking Selection Sort is stable when it is actually unstable.\n3. Using Bubble Sort for large production datasets.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_arrays_basics"],
            "current": "Sorting Foundations",
            "next": "lesson_merge_sort",
            "advanced": ["Merge Sort", "Quick Sort", "TimSort"],
            "real_world": "TimSort base case for small runs, embedded microcontroller sorting with strict memory constraints"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the best-case time complexity of an optimized Bubble Sort when the input array is already sorted?",
                "options": ["O(n²)", "O(n)", "O(log n)", "O(1)"],
                "correct_idx": 1,
                "explanation": "With a swapped boolean flag, the first pass detects 0 swaps and immediately terminates in O(n) time."
            },
            {
                "id": 2,
                "question": "What does it mean for a sorting algorithm to be 'Stable'?",
                "options": [
                    "It never crashes on null inputs",
                    "It preserves the relative order of elements with equal values/keys",
                    "It always completes in O(n log n) time",
                    "It requires zero extra memory"
                ],
                "correct_idx": 1,
                "explanation": "Stability ensures identical keys (e.g. two items with age 25) maintain their original order after sorting."
            },
            {
                "id": 3,
                "question": "Which sorting algorithm is commonly used for tiny arrays (n ≤ 16) within hybrid sorting algorithms like TimSort?",
                "options": ["Selection Sort", "Insertion Sort", "Heap Sort", "Quick Sort"],
                "correct_idx": 1,
                "explanation": "Insertion sort has extremely low constant factors and minimal overhead, making it faster than O(n log n) algorithms on small lists."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_merge_sort",
        "topic_id": "dsa_sorting_101",
        "category": "algorithm",
        "level_number": 3,
        "level_title": "Level 3: Fundamental Problem-Solving Techniques",
        "title": "Divide & Conquer Sorting: Merge Sort & Quick Sort",
        "summary": "Master guaranteed O(n log n) divide-and-conquer sorting, the two-way merge subroutine, and QuickSort partition pivots.",
        "fundamental_explanation": "Divide & Conquer breaks a complex problem into independent subproblems, solves them recursively, and merges the solutions. In Merge Sort, the array is recursively split into two halves until length is 1, and then merged back together in sorted order. Merge Sort guarantees O(n log n) performance even in the worst case and is fully stable. In Quick Sort, a pivot is selected, elements smaller than the pivot are placed to its left, and elements larger to its right.",
        "why_learn_it": "Merge Sort is the backbone of external sorting (sorting terabytes of data stored across disk drives where the entire file cannot fit into RAM). QuickSort is the fastest general in-memory sort algorithm due to superior CPU cache localization.",
        "prerequisites": "lesson_bubble_sort",
        "related_concepts": "Recursion Tree, QuickSelect, TimSort, External Sorting",
        "core_theory": "### 1. Merge Sort Complexity\n- Tree Depth: `log₂(n)` levels.\n- Work per Level: Merging two sorted arrays takes `O(n)` linear time.\n- Total Time: `O(n log n)` across best, average, and worst cases!\n- Auxiliary Space: `O(n)` auxiliary space required for merging.\n\n### 2. QuickSort Partitioning (Lomuto vs Hoare)\n- Pivot selection determines performance. If pivot is always min/max element, recursion degrades to `O(n²)`.\n- Median-of-three or randomized pivot selection guarantees `O(n log n)` average time.",
        "time_complexity": "MergeSort: Guaranteed O(n log n) · QuickSort: Average O(n log n), Worst O(n²)",
        "space_complexity": "MergeSort: O(n) auxiliary · QuickSort: O(log n) call stack",
        "visualization_type": "sorting",
        "visualization_algorithm": "merge_sort",
        "video_url": "https://www.youtube.com/embed/4VqmGXwpLqc",
        "video_title": "Merge Sort Algorithm: Visual Divide and Conquer",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Merge [2, 5] and [1, 4]", "variables": {"ptr1": 0, "ptr2": 0, "out": "[]"}, "notes": "Compare 2 and 1. 1 is smaller."},
            {"step": 2, "action": "Append 1 to output", "variables": {"ptr1": 0, "ptr2": 1, "out": "[1]"}, "notes": "Advance ptr2."},
            {"step": 3, "action": "Compare 2 and 4", "variables": {"ptr1": 1, "ptr2": 1, "out": "[1, 2]"}, "notes": "2 is smaller. Append 2, advance ptr1."},
            {"step": 4, "action": "Append remaining elements", "variables": {"out": "[1, 2, 4, 5]"}, "notes": "Sorted merged array complete!"}
        ]),
        "java_code": """// Merge Sort Implementation in Java
public class MergeSortAlgorithm {
    public static void mergeSort(int[] arr, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            mergeSort(arr, left, mid);      // Sort left half
            mergeSort(arr, mid + 1, right);  // Sort right half
            merge(arr, left, mid, right);    // Merge both halves
        }
    }
    
    private static void merge(int[] arr, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        
        while (i <= mid && j <= right) {
            if (arr[i] <= arr[j]) temp[k++] = arr[i++];
            else temp[k++] = arr[j++];
        }
        while (i <= mid) temp[k++] = arr[i++];
        while (j <= right) temp[k++] = arr[j++];
        
        System.arraycopy(temp, 0, arr, left, temp.length);
    }
}""",
        "python_code": """# QuickSort with List Comprehension (Pythonic)
def quick_sort(arr: list[int]) -> list[int]:
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print(quick_sort([38, 27, 43, 3, 9, 82, 10]))""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Merge Two Sorted Arrays", "description": "Merge nums2 into nums1 in-place in O(m+n) time from back to front."},
            {"difficulty": "Intermediate", "title": "Kth Largest Element in an Array", "description": "Find the kth largest element using QuickSelect in O(n) average time."},
            {"difficulty": "Advanced", "title": "Sort List (Merge Sort on Linked List)", "description": "Sort a linked list in O(n log n) time and O(1) auxiliary space using bottom-up merge."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Divide the list until each sublist has 1 element (which is trivially sorted)."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "The merge subroutine uses two pointers to compare the front of each sublist, picking the smaller element."},
            {"level": 3, "title": "Pseudocode", "hint": "mid = (l+r)//2; mergeSort(l, mid); mergeSort(mid+1, r); merge(l, mid, r)"}
        ]),
        "common_mistakes": "1. Forgetting base condition `if (left >= right) return`, resulting in infinite recursion StackOverflowError.\n2. Overwriting the original array elements while the merge comparisons are still in progress.\n3. Selecting poor pivots in QuickSort on already-sorted arrays, causing O(n²) runtime.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_bubble_sort"],
            "current": "Merge Sort & Quick Sort",
            "next": "lesson_stacks_queues",
            "advanced": ["QuickSelect", "External Sorting", "Counting Sort / Radix Sort"],
            "real_world": "PostgreSQL database sorting engines, Unix sort utility, large dataset map-reduce"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the worst-case time complexity of Merge Sort?",
                "options": ["O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"],
                "correct_idx": 1,
                "explanation": "Merge sort always divides into halves and merges in linear time, guaranteeing O(n log n) even in the worst case."
            },
            {
                "id": 2,
                "question": "What is the primary drawback of standard Merge Sort compared to QuickSort?",
                "options": [
                    "It is an unstable sorting algorithm",
                    "It requires O(n) auxiliary extra memory space for the temporary merge buffer",
                    "It has an O(n²) average time complexity",
                    "It cannot sort negative numbers"
                ],
                "correct_idx": 1,
                "explanation": "Standard array merge sort requires allocating temporary arrays of size n to combine the sorted halves."
            },
            {
                "id": 3,
                "question": "When does QuickSort degrade to its worst-case O(n²) time complexity?",
                "options": [
                    "When the pivot is the median element",
                    "When the pivot chosen is always the minimum or maximum element in the partition",
                    "When all elements are negative",
                    "When the array size is an odd number"
                ],
                "correct_idx": 1,
                "explanation": "Choosing the extreme element yields partitions of size 0 and n-1, creating an n-level unbalanced recursion tree (O(n²))."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 5: STACK AND QUEUE
    # ==========================================
    {
        "id": "lesson_stacks_queues",
        "topic_id": "dsa_stacks_queues",
        "category": "dsa",
        "level_number": 5,
        "level_title": "Level 5: Stack and Queue",
        "title": "Stacks, Queues & Monotonic Sequences",
        "summary": "Master LIFO vs FIFO principles, matching parentheses, call stack emulation, and O(n) Monotonic Stack algorithms.",
        "fundamental_explanation": "A **Stack** follows Last-In, First-Out (LIFO): the last item pushed is the first item popped, exactly like a stack of cafeteria trays or your browser's Back button history. A **Queue** follows First-In, First-Out (FIFO): the first item to enter the line is the first one served, like customers at a grocery checkout. A **Monotonic Stack** maintains elements in strictly increasing or decreasing order, allowing you to find the Next Greater Element for every element in an array in linear O(n) time!",
        "why_learn_it": "Stacks power compiler syntax parsers (balanced parentheses, expression evaluation), depth-first search (DFS), and undo/redo operations. Queues power CPU thread schedulers, breadth-first search (BFS), and message brokers (RabbitMQ, Kafka).",
        "prerequisites": "lesson_arrays_basics",
        "related_concepts": "Monotonic Queue, Circular Queue, Deque, BFS Traversal",
        "core_theory": "### 1. Stack Operations\n- `push(x)`: O(1) · `pop()`: O(1) · `peek()`: O(1).\n- Can be backed by an Array or a Singly Linked List.\n\n### 2. Queue Operations\n- `enqueue(x)`: O(1) · `dequeue()`: O(1) · `peek()`: O(1).\n- Implemented with a Doubly Linked List or Circular Ring Buffer to avoid O(n) array shifting.\n\n### 3. Monotonic Stack Technique\n- As you scan an array, pop elements from the stack that are smaller than the current element. The current element is their 'Next Greater Element'!",
        "time_complexity": "Push/Pop/Enqueue/Dequeue: O(1) constant time",
        "space_complexity": "O(n) auxiliary space",
        "visualization_type": "stack_queue",
        "visualization_algorithm": "stack_queue",
        "video_url": "https://www.youtube.com/embed/A3ZUpyrnCbM",
        "video_title": "Stacks and Queues: Visual Guide",
        "practice_problem_slug": "valid-parentheses",
        "dry_run": json.dumps([
            {"step": 1, "action": "Validate parentheses string '([{}])'", "variables": {"char": "(", "stack": "['(']"}, "notes": "Open bracket pushed."},
            {"step": 2, "action": "Push '[' and '{'", "variables": {"stack": "['(', '[', '{']"}, "notes": "Stack depth = 3."},
            {"step": 3, "action": "Encounter '}'", "variables": {"popped": "'{'", "match": "True", "stack": "['(', '[']"}, "notes": "'{' matches '}'!"},
            {"step": 4, "action": "Encounter ']' and ')'", "variables": {"stack": "[]"}, "notes": "Stack is empty at end -> Valid!"}
        ]),
        "java_code": """// Valid Parentheses using Deque (Stack) in Java
import java.util.ArrayDeque;
import java.util.Deque;

public class StackProblems {
    public static boolean isValid(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else if (stack.isEmpty() || stack.pop() != c) {
                return false; // Mismatched or unexpected closing bracket
            }
        }
        return stack.isEmpty();
    }
}""",
        "python_code": """# Next Greater Element I using Monotonic Decreasing Stack
def next_greater_element(nums: list[int]) -> list[int]:
    stack = [] # stores indices
    result = [-1] * len(nums)
    
    for i, num in enumerate(nums):
        # Pop all elements smaller than current num
        while stack and nums[stack[-1]] < num:
            smaller_idx = stack.pop()
            result[smaller_idx] = num
        stack.append(i)
        
    return result

print(next_greater_element([2, 1, 2, 4, 3])) # Output: [4, 2, 4, -1, -1]""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Valid Parentheses", "description": "Determine if an input string containing '()[]{}' is valid using a stack."},
            {"difficulty": "Intermediate", "title": "Min Stack", "description": "Design a stack that supports push, pop, top, and retrieving the minimum element in O(1) time."},
            {"difficulty": "Advanced", "title": "Largest Rectangle in Histogram", "description": "Find the area of the largest rectangle in a histogram in O(n) time using a Monotonic Stack."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "A closing bracket must match the most recently opened bracket. That is a pure LIFO (Stack) property."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Push corresponding expected closing brackets when an opening bracket is seen; when you see a closing bracket, pop and compare."},
            {"level": 3, "title": "Pseudocode", "hint": "for c in s: if c in '({[': push(c); else: if empty() or pop() != match(c): return False; return empty()"}
        ]),
        "common_mistakes": "1. Using `java.util.Stack` in Java (which is legacy and synchronized/slow) instead of `ArrayDeque`.\n2. Popping from an empty stack without checking `isEmpty()`, causing EmptyStackException.\n3. Returning `True` at end of string without checking if the stack is actually empty.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_arrays_basics", "lesson_linked_list"],
            "current": "Stacks & Queues",
            "next": "lesson_hashmap_subarrays",
            "advanced": ["Monotonic Queue", "Largest Rectangle in Histogram", "Expression Trees"],
            "real_world": "Browser history back button, syntax highlight AST parsers, printer job spooling"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "Which data structure follows the First-In, First-Out (FIFO) principle?",
                "options": ["Stack", "Queue", "Binary Search Tree", "Max Heap"],
                "correct_idx": 1,
                "explanation": "A Queue processes elements in the order they arrived (FIFO)."
            },
            {
                "id": 2,
                "question": "What is the time complexity of finding the Next Greater Element for all n elements using a Monotonic Stack?",
                "options": ["O(n²)", "O(n)", "O(n log n)", "O(log n)"],
                "correct_idx": 1,
                "explanation": "Each element is pushed once and popped at most once across the entire algorithm, yielding total O(n) time."
            },
            {
                "id": 3,
                "question": "Why is `ArrayDeque` preferred over `java.util.Stack` in modern Java?",
                "options": [
                    "ArrayDeque is non-synchronized and faster, whereas Stack inherits from legacy Vector with thread locks",
                    "Stack does not support push and pop operations",
                    "ArrayDeque runs on the GPU",
                    "Stack can only hold primitive integers"
                ],
                "correct_idx": 0,
                "explanation": "java.util.Stack is an outdated Java 1.0 class that extends Vector and synchronizes on every operation, adding unnecessary locking overhead."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 6: HASHING
    # ==========================================
    {
        "id": "lesson_hashmap_subarrays",
        "topic_id": "dsa_arrays_101",
        "category": "dsa",
        "level_number": 6,
        "level_title": "Level 6: Hashing",
        "title": "Hash Tables: Collision Resolution & Subarray Sum Problems",
        "summary": "Understand hash functions, open addressing vs separate chaining, load factors, and prefix sum hash maps.",
        "fundamental_explanation": "A **Hash Table** maps arbitrary keys (strings, objects, numbers) to array indices using a mathematical Hash Function: `index = hash(key) % capacity`. This provides astonishing O(1) average-time lookups, insertions, and deletions! When two different keys hash to the same index (a Collision), the table resolves it via **Separate Chaining** (linked lists / red-black trees in each bucket) or **Open Addressing** (probing for the next open cell).",
        "why_learn_it": "Hash Tables are the single most frequently used data structure in software engineering (Python `dict`, Java `HashMap`, JavaScript Objects, Redis in-memory caches, SQL index lookups).",
        "prerequisites": "lesson_arrays_basics",
        "related_concepts": "HashSet, Prefix Sums, Two Sum, Bloom Filters",
        "core_theory": "### 1. Load Factor & Resizing\n- `Load Factor = num_elements / table_capacity`.\n- When load factor exceeds 0.75, the table automatically doubles capacity and rehashes all elements to preserve O(1) search.\n\n### 2. Prefix Sum + Hash Map Pattern\n- To find the number of subarrays summing to `k`: Maintain running prefix sum `curr_sum`. Check how many times `curr_sum - k` has been seen in your frequency hash map! Total runtime drops from O(n²) to O(n)!",
        "time_complexity": "Average: O(1) · Worst Case (All collisions): O(n)",
        "space_complexity": "O(n) auxiliary space",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "video_url": "https://www.youtube.com/embed/shs0KM3wKv8",
        "video_title": "Hash Tables and Hash Functions Explained",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Find pair summing to 9 in [2, 7, 11, 15]", "variables": {"num": 2, "complement": 7, "map": "{2: 0}"}, "notes": "7 not in map. Store 2 at index 0."},
            {"step": 2, "action": "Process second number 7", "variables": {"num": 7, "complement": 2, "check": "2 in map!"}, "notes": "Complement 2 is found at index 0! Return [0, 1]."}
        ]),
        "java_code": """// Subarray Sum Equals K in O(n) using HashMap
import java.util.HashMap;
import java.util.Map;

public class HashingProblems {
    public static int subarraySum(int[] nums, int k) {
        int count = 0, currentSum = 0;
        Map<Integer, Integer> prefixSumMap = new HashMap<>();
        prefixSumMap.put(0, 1); // Base case for prefix sum starting from index 0
        
        for (int x : nums) {
            currentSum += x;
            if (prefixSumMap.containsKey(currentSum - k)) {
                count += prefixSumMap.get(currentSum - k);
            }
            prefixSumMap.put(currentSum, prefixSumMap.getOrDefault(currentSum, 0) + 1);
        }
        return count;
    }
}""",
        "python_code": """# Two Sum in O(n) Single Pass using Dictionary
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9)) # Output: [0, 1]""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Two Sum", "description": "Return indices of two numbers that add up to target in O(n) time using a hash map."},
            {"difficulty": "Intermediate", "title": "Subarray Sum Equals K", "description": "Find total number of contiguous subarrays whose sum equals k in O(n) time."},
            {"difficulty": "Advanced", "title": "Longest Consecutive Sequence", "description": "Find length of longest consecutive elements sequence in unsorted array in O(n) time using a HashSet."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Store each element's value as key and its index as value as you iterate."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "For each number x, check if (target - x) already exists in the dictionary in O(1) time."},
            {"level": 3, "title": "Pseudocode", "hint": "seen = {}; for i, x in enumerate(nums): if target-x in seen: return [seen[target-x], i]; seen[x] = i"}
        ]),
        "common_mistakes": "1. Mutating an object after using it as a HashMap key (which changes its hashCode and loses it forever).\n2. Forgetting to initialize `prefixSumMap.put(0, 1)` in subarray sum problems.\n3. Assuming HashMap iteration preserves insertion order (use LinkedHashMap if insertion order matters).",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_arrays_basics"],
            "current": "Hash Tables & Prefix Sums",
            "next": "lesson_recursion_backtracking",
            "advanced": ["Bloom Filters", "Consistent Hashing", "LRU Cache"],
            "real_world": "Redis database, distributed key-value stores (DynamoDB), compiler symbol tables"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the average time complexity of searching for a key in a well-balanced Hash Table?",
                "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                "correct_idx": 0,
                "explanation": "With an effective hash function and low load factor, key lookup takes O(1) constant time."
            },
            {
                "id": 2,
                "question": "What happens when the load factor of a Java HashMap exceeds 0.75?",
                "options": [
                    "An OutOfMemoryError is thrown",
                    "The underlying bucket array doubles in size and all existing keys are rehashed",
                    "The table converts into a binary tree permanently",
                    "Insertions become read-only"
                ],
                "correct_idx": 1,
                "explanation": "Resizing redistributes entries across a larger array to reduce hash collisions and maintain O(1) performance."
            },
            {
                "id": 3,
                "question": "In 'Subarray Sum Equals K', why do we check if `currentSum - k` exists in our prefix sum map?",
                "options": [
                    "Because if PrefixSum[j] - PrefixSum[i] = k, then the subarray between i and j sums exactly to k",
                    "To prevent integer overflow",
                    "To sort the prefix sums",
                    "To calculate the total average"
                ],
                "correct_idx": 0,
                "explanation": "Algebraic property: Sum(i..j) = PrefixSum[j] - PrefixSum[i-1]. If PrefixSum[j] - k = PrefixSum[i-1], a matching subarray exists."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 7: RECURSION AND BACKTRACKING
    # ==========================================
    {
        "id": "lesson_recursion_backtracking",
        "topic_id": "py_topic_recursion",
        "category": "algorithm",
        "level_number": 7,
        "level_title": "Level 7: Recursion and Backtracking",
        "title": "Recursion Trees, Call Stack & Backtracking (Subsets & N-Queens)",
        "summary": "Master base cases, visualizing call stack frames, state restoration in backtracking, and search space pruning.",
        "fundamental_explanation": "Recursion occurs when a function solves a problem by calling smaller instances of itself until reaching a trivial **Base Case**. Backtracking is a systematic brute-force search technique: you explore a potential decision path recursively, and if you hit a dead end or finish exploring, you **undo** your last decision (backtrack) and try the next branch. This lets you traverse an exponential search tree using O(depth) memory!",
        "why_learn_it": "Backtracking is the universal solver for combinatorial puzzles (Sudoku, N-Queens, Subsets, Permutations, Graph Coloring, Chess engine move search). It is also the bridge to Dynamic Programming and Tree Traversals.",
        "prerequisites": "lesson_stacks_queues",
        "related_concepts": "Recursion Tree, Depth-First Search, Dynamic Programming",
        "core_theory": "### The 3 Laws of Backtracking:\n1. **Choose:** Make a choice and append to your current candidate path.\n2. **Explore:** Call the function recursively to solve the subproblem.\n3. **Un-choose (Backtrack):** Undo your choice (pop from list) so subsequent branches start with a clean state.\n\n### Pruning (Bounding Functions)\n- Pruning aborts a branch immediately if it violates problem constraints, cutting millions of useless recursive calls.",
        "time_complexity": "Subsets: O(2ⁿ) · Permutations: O(n!) · N-Queens: O(n!)",
        "space_complexity": "O(n) auxiliary memory for Call Stack depth",
        "visualization_type": "graph",
        "visualization_algorithm": "dfs",
        "video_url": "https://www.youtube.com/embed/DKCbsiDBN6c",
        "video_title": "Backtracking Algorithm: Step-by-Step Visualization",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Generate subsets of [1, 2]", "variables": {"path": "[]", "depth": 0}, "notes": "Add [] to output."},
            {"step": 2, "action": "Choose 1 -> Explore", "variables": {"path": "[1]", "depth": 1}, "notes": "Add [1] to output."},
            {"step": 3, "action": "Choose 2 -> Explore", "variables": {"path": "[1, 2]", "depth": 2}, "notes": "Add [1, 2] to output. Base reached."},
            {"step": 4, "action": "Backtrack: Pop 2, then Pop 1", "variables": {"path": "[]"}, "notes": "Now choose 2 independently -> [2] added."}
        ]),
        "java_code": """// Generate All Subsets using Backtracking in Java
import java.util.ArrayList;
import java.util.List;

public class BacktrackingSubsets {
    public static List<List<Integer>> subsets(int[] nums) {
        List<List<Integer>> result = new ArrayList<>();
        backtrack(nums, 0, new ArrayList<>(), result);
        return result;
    }
    
    private static void backtrack(int[] nums, int start, List<Integer> current, List<List<Integer>> result) {
        result.add(new ArrayList<>(current)); // Deep copy snapshot
        
        for (int i = start; i < nums.length; i++) {
            current.add(nums[i]);                  // 1. Choose
            backtrack(nums, i + 1, current, result); // 2. Explore
            current.remove(current.size() - 1);    // 3. Backtrack (Un-choose)
        }
    }
}""",
        "python_code": """# Generate All Permutations using Backtracking
def permute(nums: list[int]) -> list[list[int]]:
    result = []
    
    def backtrack(current_path, used):
        if len(current_path) == len(nums):
            result.append(list(current_path)) # Snapshot
            return
            
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                current_path.append(nums[i])      # 1. Choose
                backtrack(current_path, used)     # 2. Explore
                current_path.pop()                # 3. Backtrack
                used[i] = False
                
    backtrack([], [False] * len(nums))
    return result

print(permute([1, 2, 3]))""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Subsets", "description": "Return all possible subsets (the power set) of distinct integers in O(2ⁿ) time."},
            {"difficulty": "Intermediate", "title": "Permutations", "description": "Return all permutations of an array of distinct integers in O(n!) time."},
            {"difficulty": "Advanced", "title": "N-Queens", "description": "Place n queens on an n x n chessboard such that no two queens attack each other using diagonal pruning."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Always save a copy of the candidate list when adding to result, e.g., list(current_path)."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Ensure every append has a matching pop right after the recursive call returns."},
            {"level": 3, "title": "Pseudocode", "hint": "def backtrack(start, path): res.append(list(path)); for i in start..n: path.append(a[i]); backtrack(i+1, path); path.pop()"}
        ]),
        "common_mistakes": "1. Forgetting to clone the candidate list when saving: `result.append(current)` appends the mutable reference, which becomes empty at the end!\n2. Omitting the base condition, causing infinite recursion RecursionError.\n3. Forgetting to unmark visited state in boolean tracking arrays.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_stacks_queues"],
            "current": "Recursion & Backtracking",
            "next": "lesson_trees_bst",
            "advanced": ["Sudoku Solver", "Dynamic Programming", "Tree DFS"],
            "real_world": "Constraint satisfaction solvers, circuit board layout routing, game tree search (Chess/Go)"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the total number of subsets for a set with n elements?",
                "options": ["n!", "n²", "2ⁿ", "n log n"],
                "correct_idx": 2,
                "explanation": "Each of the n elements has 2 choices: either included in the subset or excluded (2 * 2 * ... * 2 = 2ⁿ)."
            },
            {
                "id": 2,
                "question": "Why must you remove the last element (`path.pop()`) after the recursive call in backtracking?",
                "options": [
                    "To free RAM memory from the heap",
                    "To restore the state so sibling branches can evaluate alternate choices without interference",
                    "To trigger the garbage collector",
                    "To prevent stack overflow"
                ],
                "correct_idx": 1,
                "explanation": "Restoring state (un-choosing) allows the algorithm to reuse the same list to explore the next branch cleanly."
            },
            {
                "id": 3,
                "question": "What is the maximum space complexity consumed on the call stack for backtracking subsets of size n?",
                "options": ["O(2ⁿ)", "O(n)", "O(n!)", "O(1)"],
                "correct_idx": 1,
                "explanation": "The maximum recursion depth never exceeds the length of the input array n, so stack memory is O(n)."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 8: TREES
    # ==========================================
    {
        "id": "lesson_trees_bst",
        "topic_id": "dsa_trees_bst",
        "category": "dsa",
        "level_number": 8,
        "level_title": "Level 8: Trees",
        "title": "Binary Trees, BST Operations & Level-Order BFS Traversal",
        "summary": "Master hierarchical trees, Inorder/Preorder/Postorder traversals, BST invariants, and Level-Order queue processing.",
        "fundamental_explanation": "A **Tree** is a non-linear hierarchical data structure consisting of nodes connected by directed edges. A **Binary Tree** restricts every node to at most two children: left and right. A **Binary Search Tree (BST)** enforces the BST Invariant: for every node, all values in its left subtree are strictly smaller, and all values in its right subtree are strictly larger! An Inorder traversal (Left, Root, Right) of a BST visits all elements in strictly sorted ascending order!",
        "why_learn_it": "Trees are the foundation of filesystems (folders and files), HTML DOM trees, Database indexing (B+ Trees), and auto-complete dictionaries (Tries).",
        "prerequisites": "lesson_recursion_backtracking",
        "related_concepts": "AVL Trees, Red-Black Trees, Heaps, Trie",
        "core_theory": "### 1. Depth-First Traversals (DFS)\n- **Inorder (L, Root, R):** Produces sorted output for BST.\n- **Preorder (Root, L, R):** Used for serializing/cloning trees.\n- **Postorder (L, R, Root):** Used for bottom-up calculations (calculating tree height, deleting tree).\n\n### 2. Breadth-First Traversal (BFS / Level-Order)\n- Uses a Queue to visit nodes level-by-level from top to bottom.",
        "time_complexity": "Balanced BST Search/Insert: O(log n) · Degenerate BST: O(n) · Traversals: O(n)",
        "space_complexity": "DFS Call Stack: O(height) · BFS Queue: O(width)",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "video_url": "https://www.youtube.com/embed/oSWTXtMglKE",
        "video_title": "Binary Search Tree: Traversal, Insertion & Search",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Insert 7 into BST with root 10", "variables": {"curr": 10, "val": 7}, "notes": "7 < 10 -> Go left."},
            {"step": 2, "action": "Inspect left child 5", "variables": {"curr": 5, "val": 7}, "notes": "7 > 5 -> Go right."},
            {"step": 3, "action": "Right child of 5 is null", "variables": {"insert_pos": "5.right"}, "notes": "Attach new TreeNode(7) as right child of 5!"}
        ]),
        "java_code": """// Level Order Traversal (BFS) in Java
import java.util.*;

class TreeNode {
    int val;
    TreeNode left, right;
    TreeNode(int val) { this.val = val; }
}

public class TreeTraversals {
    public static List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> result = new ArrayList<>();
        if (root == null) return result;
        
        Queue<TreeNode> queue = new LinkedList<>();
        queue.offer(root);
        
        while (!queue.isEmpty()) {
            int levelSize = queue.size();
            List<Integer> currentLevel = new ArrayList<>();
            
            for (int i = 0; i < levelSize; i++) {
                TreeNode node = queue.poll();
                currentLevel.add(node.val);
                if (node.left != null) queue.offer(node.left);
                if (node.right != null) queue.offer(node.right);
            }
            result.add(currentLevel);
        }
        return result;
    }
}""",
        "python_code": """# Validate Binary Search Tree using Range Invariant
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def is_valid_bst(root: TreeNode) -> bool:
    def validate(node, low=float('-inf'), high=float('inf')):
        if not node:
            return True
        if not (low < node.val < high):
            return False # Violates BST bounds
        return (validate(node.left, low, node.val) and 
                validate(node.right, node.val, high))
                
    return validate(root)""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Maximum Depth of Binary Tree", "description": "Find height of a binary tree recursively in O(n) time."},
            {"difficulty": "Intermediate", "title": "Validate Binary Search Tree", "description": "Determine if a binary tree is a valid BST using boundary range validation."},
            {"difficulty": "Advanced", "title": "Lowest Common Ancestor (LCA)", "description": "Find lowest common ancestor of two given nodes in a binary tree in O(n) time."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "A node must not only be greater than its immediate left child, but greater than ALL nodes in its entire left subtree."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Pass down valid (min_val, max_val) boundaries during recursion. When going left, update max_val = node.val."},
            {"level": 3, "title": "Pseudocode", "hint": "def validate(node, min, max): if not node: return True; if node.val <= min or node.val >= max: return False; return val(l, min, val) and val(r, val, max)"}
        ]),
        "common_mistakes": "1. Only checking `node.val > node.left.val` without validating that all descendants in the left subtree are smaller than all ancestors.\n2. Forgetting to handle null root nodes, leading to immediate NullPointerExceptions.\n3. Confusing Inorder traversal order with Level-order queue traversal.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_recursion_backtracking"],
            "current": "Binary Trees & BST",
            "next": "lesson_dsa_heaps",
            "advanced": ["AVL Trees", "Tries", "Segment Trees"],
            "real_world": "PostgreSQL B-Tree indexes, Linux virtual memory VMA trees (Red-Black), DOM tree parsing"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "Which traversal of a Binary Search Tree produces values in strictly sorted ascending order?",
                "options": ["Preorder", "Inorder", "Postorder", "Level-Order"],
                "correct_idx": 1,
                "explanation": "Inorder visits Left, Root, Right, which visits smaller numbers, the current node, then larger numbers in a BST."
            },
            {
                "id": 2,
                "question": "What is the worst-case time complexity of searching for an element in an unbalanced (skewed) BST?",
                "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                "correct_idx": 2,
                "explanation": "If nodes are inserted in sorted order (1 -> 2 -> 3 -> 4), the BST degenerates into a singly linked list with O(n) search time."
            },
            {
                "id": 3,
                "question": "Which data structure is utilized to implement Level-Order (Breadth-First) tree traversal?",
                "options": ["Stack", "Queue", "PriorityQueue", "Hash Table"],
                "correct_idx": 1,
                "explanation": "A Queue processes parent nodes first and enqueues their children to be processed on the subsequent level."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_dsa_heaps",
        "topic_id": "dsa_trees_bst",
        "category": "dsa",
        "level_number": 8,
        "level_title": "Level 8: Trees",
        "title": "Heaps & Priority Queues: Complete Binary Trees",
        "summary": "Master Min/Max Binary Heaps, array representation without pointers, O(log n) percolate up/down, and O(n) heapify.",
        "fundamental_explanation": "A **Binary Heap** is a complete binary tree that satisfies the Heap Property. In a **Min-Heap**, every parent node is less than or equal to its children, ensuring the minimum element is always at the root (index 0). Because a complete binary tree has no holes, it is stored in a simple array without any pointer nodes! For a node at index `i`: `LeftChild = 2*i + 1`, `RightChild = 2*i + 2`, and `Parent = (i - 1) // 2`.",
        "why_learn_it": "Priority Queues power Dijkstra's Shortest Path algorithm, Prim's Minimum Spanning Tree, Huffman data compression, and finding Top-K elements in real-time data streams.",
        "prerequisites": "lesson_trees_bst",
        "related_concepts": "Dijkstra Algorithm, HeapSort, PriorityQueue in Java",
        "core_theory": "### 1. Operations\n- `peek()`: O(1) returns root.\n- `insert(x)`: Append to array end and sift-up (percolate up): `O(log n)`.\n- `extract_min()`: Replace root with last array element, pop tail, and sift-down: `O(log n)`.\n\n### 2. Linear Time Build Heap (Heapify)\n- Running sift-down from `n/2` down to 0 builds a heap in `O(n)` linear time, not `O(n log n)`!",
        "time_complexity": "Find Min: O(1) · Insert/Extract: O(log n) · Build Heap: O(n)",
        "space_complexity": "O(n) stored contiguously in an array",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "video_url": "https://www.youtube.com/embed/t0Cq6tVNRBA",
        "video_title": "Heaps and Priority Queues Data Structure",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Insert 3 into Min-Heap [5, 10, 20]", "variables": {"arr": "[5, 10, 20, 3]"}, "notes": "Appended at index 3."},
            {"step": 2, "action": "Sift-up 3 against parent 10", "variables": {"swap": "[5, 3, 20, 10]"}, "notes": "3 < 10 -> Swap with parent at index 1."},
            {"step": 3, "action": "Sift-up 3 against root 5", "variables": {"swap": "[3, 5, 20, 10]"}, "notes": "3 < 5 -> Swap with root! Heap property satisfied."}
        ]),
        "java_code": """// Top K Frequent Elements using Min-Heap in Java
import java.util.*;

public class HeapProblems {
    public static int[] topKFrequent(int[] nums, int k) {
        Map<Integer, Integer> count = new HashMap<>();
        for (int n : nums) count.put(n, count.getOrDefault(n, 0) + 1);
        
        // Min-heap ordered by frequency
        PriorityQueue<Integer> heap = new PriorityQueue<>(
            Comparator.comparingInt(count::get)
        );
        
        for (int n : count.keySet()) {
            heap.offer(n);
            if (heap.size() > k) heap.poll(); // Evict smallest frequency
        }
        
        int[] top = new int[k];
        for (int i = 0; i < k; i++) top[i] = heap.poll();
        return top;
    }
}""",
        "python_code": """# Find Kth Largest Element using heapq (Min-Heap of size K)
import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    min_heap = []
    for num in nums:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap) # evict smaller numbers
            
    return min_heap[0] # Root of size-k min heap is the kth largest!

print(find_kth_largest([3, 2, 1, 5, 6, 4], 2)) # Returns 5""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Kth Largest Element in a Stream", "description": "Design a class to find the kth largest element in a stream using a min-heap."},
            {"difficulty": "Intermediate", "title": "Top K Frequent Elements", "description": "Return the k most frequent elements in O(n log k) time using a priority queue."},
            {"difficulty": "Advanced", "title": "Merge K Sorted Lists", "description": "Merge k sorted linked lists in O(N log k) time using a min-heap of size k."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "To find the Kth largest element, maintain a MIN-HEAP of size K. Smaller elements are discarded."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "After processing all elements, the smallest element remaining in the size-K min-heap is the Kth largest overall."},
            {"level": 3, "title": "Pseudocode", "hint": "heap = []; for x in nums: heappush(heap, x); if len(heap) > k: heappop(heap); return heap[0]"}
        ]),
        "common_mistakes": "1. Using a max-heap of size n to find Kth largest instead of a min-heap of size k, wasting memory.\n2. In Python, `heapq` is a min-heap by default; forgetting to invert signs (`-x`) when simulating a max-heap.\n3. Assuming heaps are sorted arrays (heaps only guarantee the root is min/max).",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_trees_bst"],
            "current": "Heaps & Priority Queues",
            "next": "lesson_graph_traversal",
            "advanced": ["Dijkstra Shortest Path", "Prim MST", "Fibonacci Heap"],
            "real_world": "Operating system CPU priority scheduling, streaming top-trend queries, network QoS packet queues"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "For a node at index i in a 0-indexed binary heap array, what is the formula to find its left child?",
                "options": ["2 * i", "2 * i + 1", "2 * i + 2", "i / 2"],
                "correct_idx": 1,
                "explanation": "In 0-indexed array representation of complete binary trees, left child is at 2*i + 1 and right child is at 2*i + 2."
            },
            {
                "id": 2,
                "question": "What is the time complexity of building a heap from an unsorted array of size n using bottom-up heapify?",
                "options": ["O(n log n)", "O(n)", "O(n²)", "O(log n)"],
                "correct_idx": 1,
                "explanation": "Because most nodes are near the bottom of the tree and sift down very few levels, the mathematical summation converges to O(n)."
            },
            {
                "id": 3,
                "question": "Which data structure enables Dijkstra's shortest path algorithm to achieve O((V + E) log V) time?",
                "options": ["FIFO Queue", "Min-Priority Queue (Binary Heap)", "Stack", "HashSet"],
                "correct_idx": 1,
                "explanation": "A Min-Priority Queue extracts the unvisited vertex with the minimum tentative distance in O(log V) time."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 9: GRAPHS
    # ==========================================
    {
        "id": "lesson_graph_traversal",
        "topic_id": "dsa_graph_traversal",
        "category": "dsa",
        "level_number": 9,
        "level_title": "Level 9: Graphs",
        "title": "Graph Representations, BFS & DFS Traversals",
        "summary": "Master adjacency lists, cycles vs trees, Queue-based Breadth-First Search, and recursive Depth-First Search.",
        "fundamental_explanation": "A **Graph** consists of a set of vertices (nodes) and edges connecting pairs of vertices. Unlike trees, graphs can contain cycles, disconnect into isolated components, and feature bidirectional (undirected) or directional (directed) edges. **Adjacency Lists** are the industry standard for sparse graphs, using an array of lists where `adj[u]` contains all neighbors of node u. **BFS** uses a Queue to explore neighbors level-by-level (finding shortest paths in unweighted graphs). **DFS** explores down a path as deeply as possible before backtracking.",
        "why_learn_it": "Graphs model the real world: social networks (followers), web page rankings (PageRank), GPS road navigation, computer networks, and dependency package resolvers.",
        "prerequisites": "lesson_stacks_queues",
        "related_concepts": "Topological Sort, Dijkstra Algorithm, Cycle Detection",
        "core_theory": "### 1. BFS (Breadth-First Search)\n- Uses a Queue.\n- Guarantees the shortest path in unweighted graphs.\n- Tracks a `visited` set to prevent infinite cycles.\n\n### 2. DFS (Depth-First Search)\n- Uses the Call Stack or an explicit Stack.\n- Ideal for connectivity, finding connected components, and topological sorting.",
        "time_complexity": "Both BFS and DFS: O(V + E) where V is vertices and E is edges",
        "space_complexity": "O(V) for visited set and queue/stack",
        "visualization_type": "graph",
        "visualization_algorithm": "bfs",
        "video_url": "https://www.youtube.com/embed/pcKY4hjDrxk",
        "video_title": "Graph Traversals: BFS and DFS Visualized",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "BFS on graph starting at 0", "variables": {"queue": "[0]", "visited": "{0}"}, "notes": "Node 0 enqueued."},
            {"step": 2, "action": "Dequeue 0, visit neighbors 1 and 2", "variables": {"curr": 0, "queue": "[1, 2]", "visited": "{0, 1, 2}"}, "notes": "Distance = 1."},
            {"step": 3, "action": "Dequeue 1, visit neighbor 3", "variables": {"curr": 1, "queue": "[2, 3]", "visited": "{0, 1, 2, 3}"}, "notes": "Distance = 2."},
            {"step": 4, "action": "Dequeue 2, all its neighbors visited", "variables": {"curr": 2, "queue": "[3]"}, "notes": "Finished visiting level 1."}
        ]),
        "java_code": """// Graph BFS Traversal in Java
import java.util.*;

public class GraphBFS {
    public static List<Integer> bfs(int V, List<List<Integer>> adj, int startNode) {
        List<Integer> traversalOrder = new ArrayList<>();
        boolean[] visited = new boolean[V];
        Queue<Integer> queue = new LinkedList<>();
        
        visited[startNode] = true;
        queue.offer(startNode);
        
        while (!queue.isEmpty()) {
            int node = queue.poll();
            traversalOrder.add(node);
            
            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true; // Mark visited when enqueuing!
                    queue.offer(neighbor);
                }
            }
        }
        return traversalOrder;
    }
}""",
        "python_code": """# Number of Connected Components (Islands) in Grid using DFS
def num_islands(grid: list[list[str]]) -> int:
    if not grid: return 0
    rows, cols = len(grid), len(grid[0])
    island_count = 0
    
    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0' # Mark visited in-place
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
        
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                island_count += 1
                dfs(r, c) # Sink the island
                
    return island_count""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Number of Islands", "description": "Count islands in a 2D binary grid using DFS flood-fill in O(R*C) time."},
            {"difficulty": "Intermediate", "title": "Clone Graph", "description": "Deep copy an undirected graph using BFS/DFS with a hash map in O(V+E) time."},
            {"difficulty": "Advanced", "title": "Word Ladder", "description": "Find shortest transformation sequence from beginWord to endWord using Bidirectional BFS."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Mark nodes as visited AT THE MOMENT they are enqueued into the BFS queue, not when they are popped."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "If you mark visited on pop, nodes will be added to the queue multiple times, causing O(2ⁿ) memory blowup."},
            {"level": 3, "title": "Pseudocode", "hint": "queue = [start]; visited.add(start); while q: node = q.popleft(); for nbr in adj[node]: if nbr not in visited: visited.add(nbr); q.append(nbr)"}
        ]),
        "common_mistakes": "1. Marking nodes visited when dequeuing rather than when enqueuing, causing duplicate queue entries and exponential memory explosion.\n2. Forgetting that graphs can be disconnected (requiring an outer loop over all vertices 0 to V-1).\n3. Confusing 0-indexed and 1-indexed graph representations.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_stacks_queues", "lesson_trees_bst"],
            "current": "Graph BFS & DFS",
            "next": "lesson_shortest_paths",
            "advanced": ["Dijkstra Algorithm", "Topological Sort", "Tarjan Strongly Connected Components"],
            "real_world": "LinkedIn degree connections, Google Maps path finding, Git branch graph resolution"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the time complexity of Breadth-First Search on a graph with V vertices and E edges represented as an adjacency list?",
                "options": ["O(V²)", "O(V + E)", "O(V * E)", "O(log V)"],
                "correct_idx": 1,
                "explanation": "Every vertex is enqueued once and every edge is traversed once, resulting in O(V + E) linear time."
            },
            {
                "id": 2,
                "question": "Why does BFS guarantee finding the shortest path in an unweighted graph, while DFS does not?",
                "options": [
                    "BFS explores all nodes at distance k before exploring any node at distance k+1",
                    "BFS uses less memory than DFS",
                    "BFS sorts the edges by weight",
                    "BFS only runs on Directed Acyclic Graphs"
                ],
                "correct_idx": 0,
                "explanation": "Because BFS proceeds in concentric ripples (level-by-level), the first time a target node is dequeued, it is along the minimum number of edges."
            },
            {
                "id": 3,
                "question": "What happens in a graph traversal if you forget to maintain a `visited` set?",
                "options": [
                    "The graph becomes directed",
                    "The traversal will enter an infinite loop on cyclic graphs",
                    "Edge weights become negative",
                    "Adjacency list is cleared"
                ],
                "correct_idx": 1,
                "explanation": "Without visited tracking, nodes in a cycle ping-pong back and forth forever."
            }
        ]),
        "mastery_threshold": 70
    },

    {
        "id": "lesson_shortest_paths",
        "topic_id": "dsa_shortest_paths",
        "category": "algorithm",
        "level_number": 9,
        "level_title": "Level 9: Graphs",
        "title": "Shortest Paths: Dijkstra's Algorithm & Priority Queue",
        "summary": "Master single-source shortest paths on non-negative weighted graphs, relaxation steps, and why greedy edge picking works.",
        "fundamental_explanation": "When graph edges have weights (e.g., travel times, fuel costs, distance in kilometers), simple BFS no longer finds the shortest route. **Dijkstra's Algorithm** solves this using a Greedy approach powered by a Min-Priority Queue. We maintain a `dist` array initialized to infinity. Starting from source `s` (where `dist[s] = 0`), we repeatedly extract the unvisited vertex `u` with the smallest tentative distance, and **relax** all its outgoing edges: if `dist[u] + weight(u, v) < dist[v]`, we update `dist[v]` and push `v` into our priority queue.",
        "why_learn_it": "Dijkstra is the algorithm behind Google Maps, Uber route dispatching, network routing protocols (OSPF - Open Shortest Path First), and air traffic control.",
        "prerequisites": "lesson_graph_traversal",
        "related_concepts": "Bellman-Ford, Floyd-Warshall, A* Search, Prim's Algorithm",
        "core_theory": "### 1. Edge Relaxation Condition\n```text\nif (dist[u] + weight < dist[v]):\n    dist[v] = dist[u] + weight\n    pq.push((dist[v], v))\n```\n\n### 2. Negative Weight Edges\n- Dijkstra **FAILS** if any edge has a negative weight because its greedy assumption (that extracting a node settles its shortest path forever) is violated. Use **Bellman-Ford** for negative edge weights.",
        "time_complexity": "O((V + E) log V) with Min-Heap",
        "space_complexity": "O(V) for distance table and priority queue",
        "visualization_type": "graph",
        "visualization_algorithm": "dijkstra",
        "video_url": "https://www.youtube.com/embed/bZkzH5x0SKU",
        "video_title": "Dijkstra's Algorithm in 4 Minutes",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Init distances from 0: dist=[0, inf, inf]", "variables": {"pq": "[(0, node0)]"}, "notes": "Start at node 0."},
            {"step": 2, "action": "Pop (0, node0). Inspect edges: (0->1, wt=4), (0->2, wt=1)", "variables": {"dist": "[0, 4, 1]", "pq": "[(1, node2), (4, node1)]"}, "notes": "Both distances relaxed."},
            {"step": 3, "action": "Pop (1, node2). Inspect edge: (2->1, wt=2)", "variables": {"calc": "1 + 2 = 3 < 4", "dist": "[0, 3, 1]"}, "notes": "Shorter path to node 1 found via node 2!"},
            {"step": 4, "action": "Pop (3, node1). All destinations settled", "variables": {"final_dist": "[0, 3, 1]"}, "notes": "Algorithm complete!"}
        ]),
        "java_code": """// Dijkstra's Shortest Path Algorithm in Java
import java.util.*;

public class DijkstraAlgorithm {
    static class Edge {
        int to, weight;
        Edge(int to, int weight) { this.to = to; this.weight = weight; }
    }
    
    public static int[] dijkstra(int V, List<List<Edge>> adj, int src) {
        int[] dist = new int[V];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[src] = 0;
        
        PriorityQueue<int[]> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a[1]));
        pq.offer(new int[]{src, 0});
        
        while (!pq.isEmpty()) {
            int[] curr = pq.poll();
            int u = curr[0], d = curr[1];
            
            if (d > dist[u]) continue; // Stale queue entry
            
            for (Edge edge : adj.get(u)) {
                if (dist[u] + edge.weight < dist[edge.to]) {
                    dist[edge.to] = dist[u] + edge.weight;
                    pq.offer(new int[]{edge.to, dist[edge.to]});
                }
            }
        }
        return dist;
    }
}""",
        "python_code": """# Dijkstra Algorithm in Python using heapq
import heapq

def dijkstra(graph: dict[int, list[tuple[int, int]]], n: int, src: int) -> dict[int, int]:
    dist = {i: float('inf') for i in range(n)}
    dist[src] = 0
    pq = [(0, src)] # (distance, node)
    
    while pq:
        current_dist, u = heapq.heappop(pq)
        
        if current_dist > dist[u]:
            continue # Skip outdated distance
            
        for v, weight in graph.get(u, []):
            if current_dist + weight < dist[v]:
                dist[v] = current_dist + weight
                heapq.heappush(pq, (dist[v], v))
                
    return dist""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Network Delay Time", "description": "Calculate time for all nodes to receive a signal sent from source node k using Dijkstra in O(E log V)."},
            {"difficulty": "Intermediate", "title": "Path with Minimum Effort", "description": "Find path from top-left to bottom-right of matrix minimizing maximum height difference between adjacent cells."},
            {"difficulty": "Advanced", "title": "Cheapest Flights Within K Stops", "description": "Find cheapest flight price from src to dst with at most k stops using modified Dijkstra / Bellman-Ford."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Push pairs of (current_distance, node) into the min-heap so it orders by distance automatically."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Always discard pairs popped from the heap if their distance exceeds the already known dist[u]."},
            {"level": 3, "title": "Pseudocode", "hint": "while pq: d, u = heappop(pq); if d > dist[u]: continue; for v, w in adj[u]: if d + w < dist[v]: dist[v] = d + w; heappush(pq, (dist[v], v))"}
        ]),
        "common_mistakes": "1. Attempting to run Dijkstra on a graph containing negative edge weights (infinite relaxation loops).\n2. Forgetting the check `if (d > dist[u]) continue;` causing stale heap items to re-process neighbors and waste CPU time.\n3. Using an unweighted BFS on a weighted graph.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_graph_traversal", "lesson_dsa_heaps"],
            "current": "Dijkstra Shortest Path",
            "next": "lesson_greedy_algorithms",
            "advanced": ["Bellman-Ford", "Floyd-Warshall", "A* Heuristic Search"],
            "real_world": "Google Maps GPS navigation, internet router IP packet routing (OSPF), flight layover engines"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What happens if you run Dijkstra's algorithm on a graph with negative edge weights?",
                "options": [
                    "It automatically changes negative weights to positive",
                    "It may calculate incorrect shortest paths because it assumes visited nodes have their distances finalized",
                    "It runs in O(V) time",
                    "It converts into a Spanning Tree"
                ],
                "correct_idx": 1,
                "explanation": "Dijkstra's greedy choice assumes that once a node is popped from the priority queue, no shorter path to it can ever be found. A negative weight violates this invariant."
            },
            {
                "id": 2,
                "question": "What is the time complexity of Dijkstra's algorithm implemented with a Min-Binary Heap?",
                "options": ["O(V²)", "O((V + E) log V)", "O(V * E)", "O(E log E)"],
                "correct_idx": 1,
                "explanation": "Every vertex is extracted from the heap in O(V log V) and every edge can trigger a heap push in O(E log V), yielding O((V + E) log V)."
            },
            {
                "id": 3,
                "question": "Which algorithm should you choose if a directed graph contains negative edge weights?",
                "options": ["Standard BFS", "Bellman-Ford Algorithm", "Dijkstra Algorithm", "Kruskal Algorithm"],
                "correct_idx": 1,
                "explanation": "Bellman-Ford relaxes all edges V-1 times, correctly handling negative weights and detecting negative cycles."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 10: GREEDY ALGORITHMS
    # ==========================================
    {
        "id": "lesson_greedy_algorithms",
        "topic_id": "dsa_sorting_101",
        "category": "algorithm",
        "level_number": 10,
        "level_title": "Level 10: Greedy Algorithms",
        "title": "Greedy Paradigm: Activity Selection & Interval Scheduling",
        "summary": "Understand when local optimal choices yield global optimums, sorting by finish time, and proving greedy choice properties.",
        "fundamental_explanation": "A **Greedy Algorithm** builds a solution piece by piece, always choosing the immediate next option that offers the most obvious and immediate benefit (the local optimum) without ever backtracking or reconsidering past choices. In **Interval Scheduling (Activity Selection)**, we want to attend the maximum number of non-overlapping meetings. The greedy choice is: **always pick the meeting that finishes earliest**! Finishing early frees up the room for the maximum number of future meetings.",
        "why_learn_it": "Greedy algorithms are blisteringly fast (typically O(n log n) for sorting + O(n) scan) and power Huffman file compression (ZIP), Kruskal's MST, and financial cash register change algorithms.",
        "prerequisites": "lesson_bubble_sort",
        "related_concepts": "Interval Merging, Fractional Knapsack, Huffman Coding, Kruskal MST",
        "core_theory": "### When Does Greedy Work?\n1. **Greedy Choice Property:** A global optimum can be reached by making a locally optimal choice.\n2. **Optimal Substructure:** An optimal solution to the problem contains optimal solutions to subproblems.\n\n### Warning:\n- For the **0/1 Knapsack Problem** (items cannot be divided), Greedy fails! You must use **Dynamic Programming**.",
        "time_complexity": "Sorting: O(n log n) · Greedy Scan: O(n) · Total: O(n log n)",
        "space_complexity": "O(1) auxiliary space",
        "visualization_type": "sorting",
        "visualization_algorithm": "selection_sort",
        "video_url": "https://www.youtube.com/embed/ARvQcqJ_-NY",
        "video_title": "Greedy Algorithms: Interval Scheduling Tutorial",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Sort intervals by end time: [[1, 3], [2, 5], [4, 7], [6, 9]]", "variables": {"count": 1, "last_end": 3}, "notes": "Select [1, 3]."},
            {"step": 2, "action": "Inspect [2, 5]: Start 2 < last_end 3", "variables": {"conflict": "True"}, "notes": "Overlaps! Reject."},
            {"step": 3, "action": "Inspect [4, 7]: Start 4 >= last_end 3", "variables": {"count": 2, "last_end": 7}, "notes": "Compatible! Select [4, 7]."},
            {"step": 4, "action": "Inspect [6, 9]: Start 6 < last_end 7", "variables": {"conflict": "True"}, "notes": "Overlaps! Final count = 2."}
        ]),
        "java_code": """// Non-Overlapping Intervals in Java (Greedy)
import java.util.Arrays;
import java.util.Comparator;

public class GreedyIntervals {
    public static int eraseOverlapIntervals(int[][] intervals) {
        if (intervals.length == 0) return 0;
        
        // Sort by END time
        Arrays.sort(intervals, Comparator.comparingInt(a -> a[1]));
        
        int nonOverlapCount = 1;
        int lastEnd = intervals[0][1];
        
        for (int i = 1; i < intervals.length; i++) {
            if (intervals[i][0] >= lastEnd) {
                nonOverlapCount++;
                lastEnd = intervals[i][1]; // update end time
            }
        }
        return intervals.length - nonOverlapCount; // minimum removals
    }
}""",
        "python_code": """# Merge Overlapping Intervals (O(n log n))
def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    intervals.sort(key=lambda x: x[0]) # Sort by START time
    merged = []
    
    for interval in intervals:
        if not merged or merged[-1][1] < interval[0]:
            merged.append(interval) # No overlap
        else:
            merged[-1][1] = max(merged[-1][1], interval[1]) # Merge overlap
            
    return merged

print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Assign Cookies", "description": "Maximize the number of content children given greed factors and cookie sizes using greedy sorting."},
            {"difficulty": "Intermediate", "title": "Merge Intervals", "description": "Merge all overlapping intervals in O(n log n) time."},
            {"difficulty": "Advanced", "title": "Task Scheduler", "description": "Calculate minimum CPU intervals needed to execute tasks with cooldown n in O(tasks) time."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "For meeting scheduling, sort intervals by their FINISH time so you always finish as early as possible."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Iterate through sorted intervals: if an interval starts after the current end time, increment count and update end."},
            {"level": 3, "title": "Pseudocode", "hint": "intervals.sort(key=lambda x: x[1]); count = 0; end = -inf; for s, e in intervals: if s >= end: count+=1; end=e; return count"}
        ]),
        "common_mistakes": "1. Sorting intervals by start time instead of end time for activity selection, which picks long meetings that block future options.\n2. Attempting to use a greedy approach on the 0/1 Knapsack problem where it yields sub-optimal solutions.\n3. Mutating interval arrays in-place while iterating.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_bubble_sort"],
            "current": "Greedy Algorithms & Interval Scheduling",
            "next": "lesson_dynamic_programming",
            "advanced": ["Huffman Coding", "Fractional Knapsack", "Prim Minimum Spanning Tree"],
            "real_world": "Google Calendar room booking, operating system process scheduling, audio file lossless compression"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "In the Activity Selection problem, how should intervals be sorted to maximize the total number of non-overlapping meetings?",
                "options": [
                    "By duration ascending",
                    "By finish (end) time ascending",
                    "By start time ascending",
                    "By start time descending"
                ],
                "correct_idx": 1,
                "explanation": "Picking the activity that finishes earliest leaves the maximum remaining time available for subsequent activities."
            },
            {
                "id": 2,
                "question": "Why does a greedy approach fail on the 0/1 Knapsack problem?",
                "options": [
                    "Because sorting items takes O(n²)",
                    "Because items cannot be subdivided, and picking by value-to-weight ratio can leave empty capacity that cannot be filled efficiently",
                    "Because weights can be negative",
                    "Because greedy algorithms only work on graphs"
                ],
                "correct_idx": 1,
                "explanation": "Greedy can leave wasted space in the knapsack. Dynamic Programming is required to evaluate all combinations."
            },
            {
                "id": 3,
                "question": "What is the primary operational difference between Greedy Algorithms and Dynamic Programming?",
                "options": [
                    "Greedy makes a permanent irrevocable local choice at each step; DP solves and caches all overlapping subproblems",
                    "Greedy uses more memory than DP",
                    "DP is always faster than Greedy",
                    "Greedy requires recursion while DP cannot use recursion"
                ],
                "correct_idx": 0,
                "explanation": "Greedy never backtracks or reconsiders, whereas Dynamic Programming evaluates transitions across all valid past states."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 11: DYNAMIC PROGRAMMING
    # ==========================================
    {
        "id": "lesson_dynamic_programming",
        "topic_id": "dsa_dynamic_programming",
        "category": "algorithm",
        "level_number": 11,
        "level_title": "Level 11: Dynamic Programming",
        "title": "Dynamic Programming: Memoization, Tabulation & 0/1 Knapsack",
        "summary": "Master state transitions, overlapping subproblems, Top-Down Memoization vs Bottom-Up Tabulation, and space optimization.",
        "fundamental_explanation": "Dynamic Programming (DP) is an optimization method that prevents re-calculating the same subproblems over and over. When computing the 50th Fibonacci number recursively, naive recursion recalculates `fib(2)` over 10 billion times, taking years (O(2ⁿ))! By storing previously computed results in a table (cache), we calculate each subproblem exactly ONCE, reducing runtime from O(2ⁿ) exponential to O(n) linear! Dynamic programming applies whenever a problem has **Overlapping Subproblems** and an **Optimal Substructure**.",
        "why_learn_it": "Dynamic programming is the pinnacle of algorithmic interview challenges (Google, Meta, Amazon) and powers genomic sequence alignment (Needleman-Wunsch in bioinformatics), spell check suggestion distances (Levenshtein), and reinforcement learning value iteration.",
        "prerequisites": "lesson_recursion_backtracking",
        "related_concepts": "Longest Common Subsequence, Coin Change, House Robber, Matrix Chain Multiplication",
        "core_theory": "### 1. Top-Down (Memoization)\n- Write natural recursive solution.\n- Pass a cache/table (dictionary or array). Before calculating, check if `memo[state]` exists; save result before returning.\n\n### 2. Bottom-Up (Tabulation)\n- Build solution iteratively from base cases up: `dp[0]`, `dp[1]`, `dp[2]`...\n- Eliminates recursion Call Stack overhead entirely.\n\n### 3. State Transition Equation\n- Example (Climbing Stairs): `dp[i] = dp[i - 1] + dp[i - 2]`.",
        "time_complexity": "Fibonacci/ClimbStairs: O(n) · 0/1 Knapsack: O(n * W) · LCS: O(m * n)",
        "space_complexity": "Tabulation: O(n) or O(1) space optimized",
        "visualization_type": "dp",
        "visualization_algorithm": "fibonacci_dp",
        "video_url": "https://www.youtube.com/embed/oBt53YbR9Kk",
        "video_title": "Dynamic Programming: Learn the 6 Steps",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Climb Stairs n=4: dp=[0, 1, 2, 0, 0]", "variables": {"dp[1]": 1, "dp[2]": 2}, "notes": "Base cases established."},
            {"step": 2, "action": "Calculate dp[3] = dp[2] + dp[1]", "variables": {"dp[3]": "2 + 1 = 3"}, "notes": "3 ways to reach step 3."},
            {"step": 3, "action": "Calculate dp[4] = dp[3] + dp[2]", "variables": {"dp[4]": "3 + 2 = 5"}, "notes": "5 ways to reach step 4."},
            {"step": 4, "action": "Return dp[4] = 5", "variables": {"ans": 5}, "notes": "Linear O(n) evaluation complete!"}
        ]),
        "java_code": """// 0/1 Knapsack using Bottom-Up Tabulation in Java
public class KnapsackDP {
    public static int knapSack(int W, int[] wt, int[] val, int n) {
        int[][] dp = new int[n + 1][W + 1];
        
        for (int i = 1; i <= n; i++) {
            for (int w = 1; w <= W; w++) {
                if (wt[i - 1] <= w) {
                    // Max of including current item vs excluding it
                    dp[i][w] = Math.max(
                        val[i - 1] + dp[i - 1][w - wt[i - 1]],
                        dp[i - 1][w]
                    );
                } else {
                    dp[i][w] = dp[i - 1][w]; // Cannot fit
                }
            }
        }
        return dp[n][W];
    }
}""",
        "python_code": """# Coin Change (Minimum Coins to Make Amount) in Python
def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0 # 0 coins needed for 0 amount
    
    for a in range(1, amount + 1):
        for c in coins:
            if a - c >= 0:
                dp[a] = min(dp[a], 1 + dp[a - c])
                
    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change([1, 2, 5], 11)) # Output: 3 (5 + 5 + 1)""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Climbing Stairs", "description": "Count distinct ways to climb n stairs if you can take 1 or 2 steps in O(n) time and O(1) space."},
            {"difficulty": "Intermediate", "title": "Coin Change", "description": "Find minimum number of coins needed to make up given amount in O(amount * len(coins))."},
            {"difficulty": "Advanced", "title": "Longest Common Subsequence (LCS)", "description": "Find length of longest common subsequence between two strings in O(m*n) time."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Define your subproblem: what does dp[i] represent in plain English?"},
            {"level": 2, "title": "Algorithmic Direction", "hint": "Express dp[i] in terms of smaller subproblems (e.g., dp[i-1] and dp[i-2]). Identify your base cases."},
            {"level": 3, "title": "Pseudocode", "hint": "dp = [0]*(n+1); dp[1]=1; dp[2]=2; for i in 3..n: dp[i] = dp[i-1] + dp[i-2]; return dp[n]"}
        ]),
        "common_mistakes": "1. Off-by-one errors when initializing DP array sizes: `new int[n + 1]` is needed to store index n.\n2. Incomplete base cases causing array index out of bounds or negative indexing.\n3. Using recursion without memoization on exponential problems, causing execution time timeouts.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_recursion_backtracking"],
            "current": "Dynamic Programming",
            "next": "lesson_bit_manipulation",
            "advanced": ["Bitmask DP", "Digit DP", "Matrix Chain Multiplication"],
            "real_world": "DNA sequence alignment algorithms (BLAST), spell checker Levenshtein distance, automated stock trading optimization"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What two key properties MUST a problem possess for Dynamic Programming to apply?",
                "options": [
                    "Overlapping Subproblems and Optimal Substructure",
                    "Monotonicity and Binary Divide",
                    "Linearity and Vertex Connectivity",
                    "Constant Space and In-Place Swapping"
                ],
                "correct_idx": 0,
                "explanation": "Overlapping subproblems allow caching identical calculations, and optimal substructure guarantees global answers can be built from optimal subproblems."
            },
            {
                "id": 2,
                "question": "What is the difference between Top-Down Memoization and Bottom-Up Tabulation?",
                "options": [
                    "Top-Down uses recursion + caching; Bottom-Up uses iterative loops to build from base cases",
                    "Top-Down is always faster than Bottom-Up",
                    "Bottom-Up requires exponential memory",
                    "Top-Down can only solve mathematical problems"
                ],
                "correct_idx": 0,
                "explanation": "Memoization is top-down recursion that caches results; Tabulation is bottom-up iterative building of an array."
            },
            {
                "id": 3,
                "question": "In the Climbing Stairs problem, if dp[i] only depends on dp[i-1] and dp[i-2], what is the optimal auxiliary space complexity?",
                "options": ["O(n)", "O(1)", "O(n²)", "O(log n)"],
                "correct_idx": 1,
                "explanation": "You only need two variables to store the previous two values, dropping auxiliary space from O(n) to O(1)."
            }
        ]),
        "mastery_threshold": 70
    },

    # ==========================================
    # LEVEL 12: ADVANCED PROBLEM SOLVING
    # ==========================================
    {
        "id": "lesson_bit_manipulation",
        "topic_id": "dsa_arrays_101",
        "category": "algorithm",
        "level_number": 12,
        "level_title": "Level 12: Advanced Problem-Solving",
        "title": "Bit Manipulation & Mathematical Algorithms: Bitwise Hacks",
        "summary": "Master XOR cancellation tricks, bit masking, checking power-of-two with n & (n - 1), and Brian Kernighan's bit-counting algorithm.",
        "fundamental_explanation": "Computers do not think in base-10 decimals; CPUs operate directly on binary bits (0s and 1s) using hardware logic gates (AND, OR, XOR, NOT, Shift). **Bit Manipulation** algorithms execute in a single CPU cycle, offering unrivaled speed and zero auxiliary memory. The XOR operator (`^`) has magical properties: `x ^ 0 = x`, and `x ^ x = 0` (any number XORed with itself cancels out to 0!). This allows you to find the unique single number in an array where all other numbers appear twice in O(n) time and O(1) space!",
        "why_learn_it": "Bit manipulation is used in cryptographic ciphers (AES, SHA-256), graphic raster engines, hardware device drivers, Bloom Filters, and Bitmask Dynamic Programming.",
        "prerequisites": "lesson_time_complexity",
        "related_concepts": "Bitmask DP, Brian Kernighan Algorithm, Number Theory, Sieve of Eratosthenes",
        "core_theory": "### Core Bitwise Operations:\n1. **AND (`&`):** 1 only if both bits are 1.\n2. **OR (`|`):** 1 if either bit is 1.\n3. **XOR (`^`):** 1 if bits are DIFFERENT. Self-canceling (`a ^ a = 0`).\n4. **Left Shift (`<< k`):** Multiplies number by `2^k`.\n5. **Right Shift (`>> k`):** Divides number by `2^k`.\n\n### Famous Bit Tricks:\n- Check if power of two: `(n > 0) && (n & (n - 1)) == 0`.\n- Clear lowest set bit: `n = n & (n - 1)` (Brian Kernighan's set-bit counter).",
        "time_complexity": "All bitwise operations run in O(1) single CPU cycle",
        "space_complexity": "O(1) auxiliary space",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "video_url": "https://www.youtube.com/embed/5rtV0loSRlU",
        "video_title": "Bit Manipulation Tricks for Coding Interviews",
        "practice_problem_slug": "two-sum",
        "dry_run": json.dumps([
            {"step": 1, "action": "Find single number in [4, 1, 2, 1, 2]", "variables": {"acc": 0}, "notes": "Start accumulator at 0."},
            {"step": 2, "action": "acc ^= 4", "variables": {"acc": 4}, "notes": "0 ^ 4 = 4."},
            {"step": 3, "action": "acc ^= 1 -> acc ^= 2", "variables": {"acc": "4 ^ 1 ^ 2"}, "notes": "Accumulating XOR."},
            {"step": 4, "action": "acc ^= 1 -> acc ^= 2", "variables": {"acc": 4}, "notes": "1 ^ 1 cancels to 0; 2 ^ 2 cancels to 0. Remaining result is 4!"}
        ]),
        "java_code": """// Bit Manipulation Utilities in Java
public class BitHacks {
    // Single Number: Every element appears twice except for one
    public static int singleNumber(int[] nums) {
        int result = 0;
        for (int n : nums) {
            result ^= n; // XOR cancellation
        }
        return result;
    }
    
    // Count set bits using Brian Kernighan's Algorithm
    public static int countSetBits(int n) {
        int count = 0;
        while (n != 0) {
            n = n & (n - 1); // Clears the lowest set bit
            count++;
        }
        return count;
    }
}""",
        "python_code": """# Check Power of Two and Sieve of Eratosthenes
def is_power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0

def sieve_of_eratosthenes(limit: int) -> list[int]:
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False
    
    for p in range(2, int(limit**0.5) + 1):
        if primes[p]:
            for multiple in range(p * p, limit + 1, p):
                primes[multiple] = False
                
    return [i for i, is_p in enumerate(primes) if is_p]

print(f"Is 64 power of two? {is_power_of_two(64)}") # True
print(f"Primes up to 30: {sieve_of_eratosthenes(30)}")""",
        "practice_questions": json.dumps([
            {"difficulty": "Basic", "title": "Single Number", "description": "Find the unique element in an array where every other element appears twice in O(n) time and O(1) space."},
            {"difficulty": "Intermediate", "title": "Number of 1 Bits", "description": "Count the number of set bits (Hamming weight) of a 32-bit unsigned integer."},
            {"difficulty": "Advanced", "title": "Counting Bits", "description": "For every number from 0 to n, return an array of the count of 1 bits in O(n) time using DP with bit shifts."}
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "title": "Conceptual Clue", "hint": "Remember that a ^ a = 0 and a ^ 0 = a. The order of operations does not matter (commutative & associative)."},
            {"level": 2, "title": "Algorithmic Direction", "hint": "n & (n - 1) always clears the lowest active 1-bit in n."},
            {"level": 3, "title": "Pseudocode", "hint": "res = 0; for x in nums: res ^= x; return res"}
        ]),
        "common_mistakes": "1. Operator precedence confusion: in Python/Java, `==` has higher precedence than `&`! Always write `(n & 1) == 0` with parentheses.\n2. Forgetting 32-bit negative signed integers in right shift (use `>>>` in Java for logical unsigned right shift).\n3. Off-by-one errors in bitmask shifting when accessing bit index i.",
        "concept_connections": json.dumps({
            "prerequisites": ["lesson_time_complexity"],
            "current": "Bit Manipulation & Number Theory",
            "next": "lesson_py_memory",
            "advanced": ["Bitmask DP (Traveling Salesperson)", "Fast Fourier Transform (FFT)", "Cryptography AES"],
            "real_world": "Network subnet masks (CIDR), Linux file permissions (chmod 755), graphics color pixel blending (RGBA)"
        }),
        "quiz_questions": json.dumps([
            {
                "id": 1,
                "question": "What is the result of calculating `x ^ x` for any integer x?",
                "options": ["x", "1", "0", "2 * x"],
                "correct_idx": 2,
                "explanation": "XORing identical bits always produces 0 (1^1 = 0 and 0^0 = 0), so x ^ x = 0."
            },
            {
                "id": 2,
                "question": "What does the expression `n & (n - 1)` do to a non-zero integer n?",
                "options": [
                    "Multiplies n by 2",
                    "Clears the lowest (rightmost) set 1-bit in n",
                    "Inverts all bits of n",
                    "Checks if n is odd"
                ],
                "correct_idx": 1,
                "explanation": "Subtracting 1 flips all bits after the lowest 1-bit; ANDing with n zeroes out that lowest 1-bit."
            },
            {
                "id": 3,
                "question": "Why is `(n > 0) && (n & (n - 1)) == 0` a valid test for whether n is a power of 2?",
                "options": [
                    "Because powers of two have exactly one set 1-bit in binary; clearing it yields zero",
                    "Because powers of two are always prime",
                    "Because all powers of two end in bit 0",
                    "Because it divides n by 2"
                ],
                "correct_idx": 0,
                "explanation": "Powers of 2 (1, 2, 4, 8, 16...) have exactly a single 1-bit. Clearing their lowest 1-bit leaves 0."
            }
        ]),
        "mastery_threshold": 70
    }
]

def seed_curriculum(db: Session):
    print("Starting master curriculum seeding across all 12 progressive levels...")
    
    # 1. Order and link all lessons sequentially
    total_lessons = len(CURRICULUM_DATA)
    for i, data in enumerate(CURRICULUM_DATA):
        step_num = i + 1
        prev_id = CURRICULUM_DATA[i - 1]["id"] if i > 0 else None
        next_id = CURRICULUM_DATA[i + 1]["id"] if i < total_lessons - 1 else None
        
        # Check if lesson exists
        lesson = db.query(Lesson).filter(Lesson.id == data["id"]).first()
        if not lesson:
            lesson = Lesson(
                id=data["id"],
                topic_id=data["topic_id"],
                category=data["category"],
                title=data["title"],
                summary=data["summary"],
                fundamental_explanation=data["fundamental_explanation"],
                step_by_step=data["core_theory"],
                real_world_applications=data["why_learn_it"],
                examples_illustrations=data["fundamental_explanation"],
                pseudocode=data.get("python_code", ""),
                time_complexity=data["time_complexity"],
                space_complexity=data["space_complexity"],
                prerequisites=data["prerequisites"],
                related_concepts=data["related_concepts"],
                video_url=data["video_url"],
                video_title=data["video_title"],
                visualization_type=data.get("visualization_type"),
                visualization_algorithm=data.get("visualization_algorithm"),
                practice_problem_slug=data.get("practice_problem_slug"),
                order_index=step_num * 10,
                step_number=step_num,
                stage_name=data["level_title"],
                level_number=data["level_number"],
                level_title=data["level_title"],
                why_learn_it=data["why_learn_it"],
                core_theory=data["core_theory"],
                dry_run=data["dry_run"],
                java_code=data["java_code"],
                python_code=data["python_code"],
                practice_questions=data["practice_questions"],
                ai_hints=data["ai_hints"],
                common_mistakes=data["common_mistakes"],
                concept_connections=data["concept_connections"],
                quiz_questions=data["quiz_questions"],
                mastery_threshold=data["mastery_threshold"],
                prev_lesson_id=prev_id,
                next_lesson_id=next_id,
            )
            db.add(lesson)
            print(f"Created Lesson [{step_num}/{total_lessons}]: {data['title']}")
        else:
            # Update all fields
            lesson.topic_id = data["topic_id"]
            lesson.category = data["category"]
            lesson.title = data["title"]
            lesson.summary = data["summary"]
            lesson.fundamental_explanation = data["fundamental_explanation"]
            lesson.step_by_step = data["core_theory"]
            lesson.real_world_applications = data["why_learn_it"]
            lesson.examples_illustrations = data["fundamental_explanation"]
            lesson.pseudocode = data.get("python_code", "")
            lesson.time_complexity = data["time_complexity"]
            lesson.space_complexity = data["space_complexity"]
            lesson.prerequisites = data["prerequisites"]
            lesson.related_concepts = data["related_concepts"]
            lesson.video_url = data["video_url"]
            lesson.video_title = data["video_title"]
            lesson.visualization_type = data.get("visualization_type")
            lesson.visualization_algorithm = data.get("visualization_algorithm")
            lesson.practice_problem_slug = data.get("practice_problem_slug")
            lesson.order_index = step_num * 10
            lesson.step_number = step_num
            lesson.stage_name = data["level_title"]
            lesson.level_number = data["level_number"]
            lesson.level_title = data["level_title"]
            lesson.why_learn_it = data["why_learn_it"]
            lesson.core_theory = data["core_theory"]
            lesson.dry_run = data["dry_run"]
            lesson.java_code = data["java_code"]
            lesson.python_code = data["python_code"]
            lesson.practice_questions = data["practice_questions"]
            lesson.ai_hints = data["ai_hints"]
            lesson.common_mistakes = data["common_mistakes"]
            lesson.concept_connections = data["concept_connections"]
            lesson.quiz_questions = data["quiz_questions"]
            lesson.mastery_threshold = data["mastery_threshold"]
            lesson.prev_lesson_id = prev_id
            lesson.next_lesson_id = next_id
            print(f"Updated Lesson [{step_num}/{total_lessons}]: {data['title']}")

    db.commit()
    print("Master curriculum seeding finished successfully!")

if __name__ == "__main__":
    migrate_db_columns()
    db = SessionLocal()
    try:
        seed_curriculum(db)
    finally:
        db.close()
