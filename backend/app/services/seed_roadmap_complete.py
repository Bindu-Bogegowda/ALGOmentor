"""
Seed Script: Comprehensive Roadmap.sh DSA Master Alignment
Maps and populates every single node from the uploaded roadmap.sh Data Structures & Algorithms PDF.
"""

import json
from app.database import SessionLocal
from app.models.lesson import Lesson

ADDITIONAL_ROADMAP_CONCEPTS = [
    # -------------------------------------------------------------
    # Basic Data Structures: Foundations
    # -------------------------------------------------------------
    {
        "id": "concept_what_are_data_structures",
        "category": "Basic Data Structures",
        "difficulty": "Beginner",
        "level_number": 2,
        "level_title": "Level 2: Basic Data Structures",
        "title": "What are Data Structures? Memory Contiguity & Abstract Types",
        "prerequisites": "Programming Fundamentals (Python / Java Syntax)",
        "summary": "Understand how computers organize data in memory (RAM), comparing physical layouts against abstract data types (ADT).",
        "why_learn_it": "Data structures determine whether an algorithm completes in microseconds or hours. Choosing the right layout avoids cache misses and redundant operations.",
        "fundamental_explanation": "A data structure is a specialized format for organizing, processing, retrieving, and storing data in computer memory. An Abstract Data Type (ADT) specifies behaviors (e.g. List, Queue), while the concrete data structure provides physical memory representation (e.g. Array, Linked List).",
        "core_theory": "### Core Concepts:\n1. **Physical Layout:** Contiguous memory (Array) vs Node-based pointers (Linked List).\n2. **Cache Locality:** Modern CPUs fetch memory in 64-byte cache lines; contiguous arrays achieve spatial locality.\n3. **Trade-offs:** Fast lookups vs fast insertions/deletions.",
        "time_complexity": "Concept definition: O(1)",
        "space_complexity": "Physical RAM footprint: O(n)",
        "video_url": "https://www.youtube.com/embed/bum_19crdeA",
        "video_title": "What Are Data Structures?",
        "visualization_type": "array",
        "visualization_algorithm": "array_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """// Java: Abstract Data Type vs Physical Implementation
import java.util.List;
import java.util.ArrayList;
import java.util.LinkedList;

public class DataStructureIntro {
    public static void main(String[] args) {
        // List is the ADT; ArrayList and LinkedList are concrete structures
        List<Integer> contiguous = new ArrayList<>(); // Contiguous array in RAM
        List<Integer> nodeBased = new LinkedList<>();  // Heap nodes linked by pointers
        
        contiguous.add(42);
        nodeBased.add(42);
        System.out.println("ArrayList (Array) vs LinkedList (Nodes) initialized.");
    }
}""",
        "python_code": """# Python: Understanding Memory Contiguity
import sys

# Dynamic array: stores contiguous references to objects
numbers = [10, 20, 30, 40]
print(f"Memory size of list container: {sys.getsizeof(numbers)} bytes")
print(f"Element 0 address: {id(numbers[0])}")
print(f"Element 1 address: {id(numbers[1])}")""",
        "dry_run": json.dumps([
            {"step": 1, "description": "CPU requests memory allocation for an integer array of size 4.", "variables": {"RAM_Address": "0x1000", "Capacity": 4, "State": "Empty"}},
            {"step": 2, "description": "Values [10, 20, 30, 40] placed at contiguous 4-byte boundaries.", "variables": {"0x1000": 10, "0x1004": 20, "0x1008": 30, "0x100C": 40}},
            {"step": 3, "description": "Address for index 2 computed instantly: 0x1000 + (2 * 4) = 0x1008.", "variables": {"Computed_Addr": "0x1008", "Value": 30, "Complexity": "O(1)"}}
        ]),
        "quiz_questions": json.dumps([
            {
                "question": "What is the primary difference between an ADT (Abstract Data Type) and a concrete Data Structure?",
                "options": [
                    "ADT defines the logical interface and operations; Data Structure is the physical memory implementation",
                    "ADT is only used in Python, while Data Structures are used in Java",
                    "ADT has O(1) complexity, while Data Structures have O(n) complexity",
                    "There is no difference; they are exact synonyms"
                ],
                "answer_idx": 0,
                "explanation": "An ADT (like List or Queue) specifies WHAT operations are supported, while a Data Structure (like ArrayList or DoublyLinkedList) specifies HOW data is laid out in memory."
            },
            {
                "question": "Why do arrays provide superior performance over linked lists for sequential reads?",
                "options": [
                    "Arrays use less CPU voltage",
                    "Arrays have CPU cache locality due to contiguous memory allocation",
                    "Arrays store elements in binary rather than decimal",
                    "Linked lists cannot store integers"
                ],
                "answer_idx": 1,
                "explanation": "Arrays allocate elements in contiguous memory blocks, allowing the CPU to load multiple elements at once into L1/L2 cache lines."
            }
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "hint": "Think about how RAM works like an indexed numbered street of houses."},
            {"level": 2, "hint": "Contiguity allows O(1) offset math: base_address + index * element_size."},
            {"level": 3, "hint": "Node-based structures trade cache locality for cheap insertions without reallocation."}
        ])
    },
    {
        "id": "concept_why_data_structures_matter",
        "category": "Basic Data Structures",
        "difficulty": "Beginner",
        "level_number": 2,
        "level_title": "Level 2: Basic Data Structures",
        "title": "Why are Data Structures Important? Space-Time Efficiency & Scalability",
        "prerequisites": "What are Data Structures?",
        "summary": "Explore why standard data structures are fundamental to software engineering, showing real world examples from databases, search engines, and operating systems.",
        "why_learn_it": "Without appropriate data structures, searching 1 billion items takes minutes; with a hash table or B-Tree, it takes nanoseconds.",
        "fundamental_explanation": "Computers process billions of instructions per second, but memory latency and algorithmic bottlenecks quickly degrade performance. Data structures optimize the fundamental trade-offs between reading, writing, and memory consumption.",
        "core_theory": "### Real-World Applications:\n- **Operating Systems:** Priority Queues for thread scheduling; Hash Tables for page tables.\n- **Databases:** B+ Trees for relational indexing; LSM-Trees for high-throughput writes.\n- **Web Browsers:** Stack for back/forward navigation; Trie for autocomplete.",
        "time_complexity": "Lookup comparisons: O(1) vs O(log n) vs O(n)",
        "space_complexity": "Overhead trade-offs",
        "video_url": "https://www.youtube.com/embed/zg9ih6SVACc",
        "video_title": "Why Data Structures Matter in Real Systems",
        "visualization_type": "array",
        "visualization_algorithm": "binary_search",
        "practice_problem_slug": "two-sum",
        "java_code": """// Demonstrating Search Speed: Unsorted Array vs HashSet
import java.util.*;

public class EfficiencyDemo {
    public static void main(String[] args) {
        int n = 1_000_000;
        Set<Integer> fastSet = new HashSet<>();
        for (int i = 0; i < n; i++) fastSet.add(i);

        long start = System.nanoTime();
        boolean found = fastSet.contains(999_999); // O(1) average
        long elapsed = System.nanoTime() - start;
        System.out.println("HashSet lookup took: " + elapsed + " ns (found: " + found + ")");
    }
}""",
        "python_code": """# Demonstrating lookup efficiency: List O(N) vs Set O(1)
import time

items_list = list(range(1_000_000))
items_set = set(items_list)

# Measure set lookup
t0 = time.perf_counter()
_ = 999_999 in items_set
t_set = time.perf_counter() - t0

# Measure list lookup
t0 = time.perf_counter()
_ = 999_999 in items_list
t_list = time.perf_counter() - t0

print(f"Set O(1):  {t_set*1e6:.2f} µs")
print(f"List O(n): {t_list*1e6:.2f} µs (Ratio: {t_list/t_set:.0f}x faster)")""",
        "dry_run": json.dumps([
            {"step": 1, "description": "Linear search through 1M items inspects every element one by one.", "variables": {"Comparisons": 1000000, "Time": "~10ms"}},
            {"step": 2, "description": "Hash function computes direct bucket offset hash(x) % capacity.", "variables": {"Comparisons": 1, "Time": "~25ns"}},
            {"step": 3, "description": "Result: 400,000x speedup with proper data structure selection.", "variables": {"Speedup": "400,000x", "Verdict": "Essential for scale"}}
        ]),
        "quiz_questions": json.dumps([
            {
                "question": "What is the primary reason why choosing the correct data structure matters?",
                "options": [
                    "It dramatically reduces time and space complexity as input size N grows to millions",
                    "It prevents the program from requiring a compiler",
                    "It converts interpreted code into machine hardware",
                    "It is only required for passing coding interviews"
                ],
                "answer_idx": 0,
                "explanation": "Algorithms operate on data structures. As datasets scale from 10 items to 100 million items, polynomial or exponential complexity crashes servers, while optimal data structures maintain sub-millisecond responses."
            }
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "hint": "Consider how search engines query billions of websites in milliseconds."},
            {"level": 2, "hint": "Lookup times range from O(1) to O(N) depending on structure choice."},
            {"level": 3, "hint": "Memory vs computation is the defining duality of computer science."}
        ])
    },

    # -------------------------------------------------------------
    # Algorithmic Complexity: Common Runtimes
    # -------------------------------------------------------------
    {
        "id": "concept_common_runtimes",
        "category": "Algorithmic Complexity",
        "difficulty": "Beginner",
        "level_number": 3,
        "level_title": "Level 3: Algorithmic Complexity",
        "title": "Common Runtimes: Constant, Logarithmic, Linear, Polynomial, Exponential & Factorial",
        "prerequisites": "Asymptotic Notations: Big-O, Big-Theta & Big-Omega",
        "summary": "Master the 6 primary growth rates that classify all algorithms: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ), and O(n!).",
        "why_learn_it": "Knowing the runtime class of an algorithm tells you instantly whether a solution will pass online judge test cases within the standard 1-second limit (~10⁸ operations).",
        "fundamental_explanation": "Growth functions illustrate how computational steps multiply as N increases. O(1) stays flat; O(log n) grows imperceptibly; O(n) grows proportionally; O(n²) doubles every time N increases by ~40%; O(2ⁿ) and O(n!) quickly exceed the number of atoms in the universe.",
        "core_theory": "### Common Runtimes Table:\n- **O(1) Constant:** Hash lookup, array indexing, arithmetic.\n- **O(log n) Logarithmic:** Binary search, balanced BST search.\n- **O(n) Linear:** Single scan, linear search, prefix sum.\n- **O(n log n) Linearithmic:** Merge Sort, Quick Sort (avg), Heap Sort.\n- **O(n²) Polynomial / Quadratic:** Nested loops, Bubble/Insertion sort.\n- **O(2ⁿ) Exponential:** Recursive Fibonacci, power set subsets.\n- **O(n!) Factorial:** Traveling Salesperson brute force, all permutations.",
        "time_complexity": "From O(1) (best) to O(n!) (unfeasible)",
        "space_complexity": "Call stack and auxiliary structures",
        "video_url": "https://www.youtube.com/embed/4W1mO_7b7pI",
        "video_title": "Big-O Common Runtimes Explained Visually",
        "visualization_type": "sorting",
        "visualization_algorithm": "bubble_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """public class RuntimesComparison {
    // O(1) Constant
    public static int getFirst(int[] arr) { return arr[0]; }

    // O(log n) Logarithmic
    public static int binarySearch(int[] arr, int target) {
        int l = 0, r = arr.length - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (arr[mid] == target) return mid;
            else if (arr[mid] < target) l = mid + 1;
            else r = mid - 1;
        }
        return -1;
    }

    // O(n) Linear
    public static int sumArray(int[] arr) {
        int sum = 0;
        for (int v : arr) sum += v;
        return sum;
    }
}""",
        "python_code": """# Visualizing operations for N = 100
import math

n = 100
print(f"O(1):         {1} op")
print(f"O(log N):     {math.ceil(math.log2(n))} ops")
print(f"O(N):         {n} ops")
print(f"O(N log N):   {math.ceil(n * math.log2(n))} ops")
print(f"O(N^2):       {n**2:,} ops")
print(f"O(2^N):       {2**n:,} ops (exceeds universe lifetime!)")""",
        "dry_run": json.dumps([
            {"step": 1, "description": "N = 10: O(N) = 10 ops, O(N²) = 100 ops, O(2^N) = 1,024 ops.", "variables": {"N": 10, "Linear": 10, "Quadratic": 100, "Exponential": 1024}},
            {"step": 2, "description": "N = 30: O(N) = 30 ops, O(N²) = 900 ops, O(2^N) = 1,073,741,824 ops (1 billion!).", "variables": {"N": 30, "Linear": 30, "Quadratic": 900, "Exponential": "1.07B"}},
            {"step": 3, "description": "Rule of thumb: 10^8 operations take ~1 second in C++/Java, ~2-3 seconds in Python.", "variables": {"Constraint": "N <= 10^5 -> Aim for O(N log N) or O(N)"}}
        ]),
        "quiz_questions": json.dumps([
            {
                "question": "If an algorithm runs in O(2ⁿ) time, what is the maximum input size N it can reasonably solve within a 1-second limit?",
                "options": [
                    "N ≈ 20 to 25",
                    "N ≈ 10,000",
                    "N ≈ 1,000,000",
                    "N ≈ 100,000,000"
                ],
                "answer_idx": 0,
                "explanation": "2²⁰ is ~1,000,000 operations, and 2²⁵ is ~33 million operations. Any N > 30 will timeout (>10⁹ operations)."
            },
            {
                "question": "Which of the following complexity classes grows the slowest as N approaches infinity?",
                "options": [
                    "O(log n)",
                    "O(n)",
                    "O(n log n)",
                    "O(√n)"
                ],
                "answer_idx": 0,
                "explanation": "Logarithmic time O(log n) is the slowest growing among the choices. Even for N = 1,000,000,000, log₂(N) is only ~30 operations."
            }
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "hint": "Divide-and-conquer algorithms that halve the problem space achieve O(log n)."},
            {"level": 2, "hint": "Nested independent loops multiplying iterations produce O(n²)."},
            {"level": 3, "hint": "Generating all permutations of size N produces O(n!) factorials."}
        ])
    },

    # -------------------------------------------------------------
    # Advanced Data Structures: Suffix Trees & Suffix Arrays
    # -------------------------------------------------------------
    {
        "id": "concept_suffix_trees_and_arrays",
        "category": "Advanced Data Structures",
        "difficulty": "Advanced",
        "level_number": 10,
        "level_title": "Level 10: Advanced Data Structures & Indexing",
        "title": "Suffix Trees & Suffix Arrays: Pattern Searching & Substring Compression",
        "prerequisites": "Tries & Prefix Trees, String Manipulation",
        "summary": "Master compressed trie representation of all suffixes of a string, enabling sub-linear substring searching, longest repeated substring, and genomic sequencing.",
        "why_learn_it": "Suffix Trees and Suffix Arrays allow answering 'Does pattern P exist in text T?' in O(|P|) time, independent of text size |T|.",
        "fundamental_explanation": "A Suffix Tree is a compacted trie containing all suffixes of a string S. A Suffix Array is a space-efficient alternative: a sorted array of all suffix indices. Combined with the LCP (Longest Common Prefix) array via Kasai's algorithm, it achieves Suffix Tree capabilities with 4x less memory.",
        "core_theory": "### Key Algorithms:\n1. **Ukkonen's Algorithm:** Builds Suffix Tree in online O(n) linear time.\n2. **Suffix Array Construction:** O(n log² n) via prefix doubling, or O(n) via SA-IS algorithm.\n3. **Pattern Searching:** Binary search over suffix array in O(|P| log |T|) or O(|P| + log |T|) with LCP array.",
        "time_complexity": "Construction: O(n) · Query: O(|P|)",
        "space_complexity": "Suffix Tree: O(n) nodes · Suffix Array: O(n) integers",
        "video_url": "https://www.youtube.com/embed/VA9m_l6LpwI",
        "video_title": "Suffix Arrays and Suffix Trees Explained",
        "visualization_type": "string",
        "visualization_algorithm": "kmp_search",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;

public class SuffixArray {
    public static int[] buildSuffixArray(String s) {
        int n = s.length();
        Integer[] sa = new Integer[n];
        for (int i = 0; i < n; i++) sa[i] = i;

        // Sort suffixes lexicographically
        Arrays.sort(sa, (a, b) -> s.substring(a).compareTo(s.substring(b)));

        int[] result = new int[n];
        for (int i = 0; i < n; i++) result[i] = sa[i];
        return result;
    }

    public static void main(String[] args) {
        String text = "banana";
        int[] sa = buildSuffixArray(text);
        System.out.println("Suffix Array for 'banana': " + Arrays.toString(sa));
    }
}""",
        "python_code": """# Suffix Array Construction for 'banana'
text = "banana$"

# Generate all suffixes with their starting indices
suffixes = [(text[i:], i) for i in range(len(text))]
# Sort lexicographically
suffixes.sort()

suffix_array = [idx for _, idx in suffixes]
print("Lexicographical Suffixes:")
for s, idx in suffixes:
    print(f"  Index {idx:2d}: {s}")

print(f"\\nSuffix Array: {suffix_array}")""",
        "dry_run": json.dumps([
            {"step": 1, "description": "String 'banana$' has 7 suffixes: 'banana$', 'anana$', 'nana$', 'ana$', 'na$', 'a$', '$'.", "variables": {"String": "banana$", "Suffix_Count": 7}},
            {"step": 2, "description": "Sort suffixes lexicographically: $, a$, ana$, anana$, banana$, na$, nana$.", "variables": {"Sorted_Order": ["$", "a$", "ana$", "anana$", "banana$", "na$", "nana$"]}},
            {"step": 3, "description": "Record starting indices: [6, 5, 3, 1, 0, 4, 2]. This is the Suffix Array.", "variables": {"Suffix_Array": [6, 5, 3, 1, 0, 4, 2]}},
            {"step": 4, "description": "Search for pattern 'nan': Binary search finds 'nana$' in O(|P| log N) time.", "variables": {"Found_At_Index": 2, "Status": "Matched in Substring"}}
        ]),
        "quiz_questions": json.dumps([
            {
                "question": "What is the primary memory advantage of a Suffix Array over a Suffix Tree?",
                "options": [
                    "A Suffix Array is a flat integer array using only ~4N bytes, while a Suffix Tree requires numerous node pointers (~20-40N bytes)",
                    "A Suffix Array does not require the text string",
                    "A Suffix Array runs on the GPU instead of CPU",
                    "A Suffix Tree cannot store uppercase characters"
                ],
                "answer_idx": 0,
                "explanation": "Suffix Trees require pointer-heavy tree nodes and edges, typically taking 20-45 bytes per character. A Suffix Array stores simple 32-bit integer indices (4 bytes per character)."
            }
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "hint": "Every substring of string S is a prefix of some suffix of S."},
            {"level": 2, "hint": "Sorting all suffixes allows binary searching for any pattern prefix."},
            {"level": 3, "hint": "Kasai's algorithm computes the Longest Common Prefix (LCP) array in linear O(N) time."}
        ])
    },

    # -------------------------------------------------------------
    # Complex Data Structures & Indexing: Linear vs Tree-Based
    # -------------------------------------------------------------
    {
        "id": "concept_linear_vs_tree_indexing",
        "category": "Complex Data Structures & Indexing",
        "difficulty": "Advanced",
        "level_number": 10,
        "level_title": "Level 10: Advanced Data Structures & Indexing",
        "title": "Indexing Architectures: Linear Indexing vs Tree-Based Indexing",
        "prerequisites": "B-Trees & B+ Trees, Hash Tables",
        "summary": "Compare linear indexing (inverted indexes, sparse index files, dense indexes) against hierarchical tree indexing (B-Tree, B+ Tree, LSM-Trees).",
        "why_learn_it": "Indexing is the core engine behind databases (Postgres, MySQL, DynamoDB) and search engines (Elasticsearch, Lucene).",
        "fundamental_explanation": "An index is an auxiliary data structure that reduces disk I/O when locating records. Linear indexing uses sorted key-pointer arrays or hash tables; Tree-based indexing uses multiway balanced trees that fit within disk sector block boundaries (4KB - 16KB pages).",
        "core_theory": "### Indexing Taxonomy:\n1. **Linear Indexing:** Dense index (record pointer for every search key), Sparse index (pointers to disk blocks).\n2. **Inverted Index:** Terms mapped to posting lists of document IDs (Elasticsearch).\n3. **Tree-Based Indexing (B+ Tree):** All data in leaves, internal nodes hold routing keys. Optimal for range queries (`WHERE age BETWEEN 20 AND 30`).\n4. **Hash Index:** O(1) equality lookups (`WHERE id = 500`), but cannot execute range scans.",
        "time_complexity": "Tree Search: O(log_B N) disk I/O · Hash Lookup: O(1)",
        "space_complexity": "Index storage overhead: ~15-30% of database size",
        "video_url": "https://www.youtube.com/embed/aZjYr87r1b8",
        "video_title": "Database Indexing: B-Trees vs Linear Indexes",
        "visualization_type": "tree",
        "visualization_algorithm": "bst_search",
        "practice_problem_slug": "two-sum",
        "java_code": """// Conceptual representation of B+ Tree Page indexing
class DiskBlockIndex {
    static class IndexEntry {
        int key;
        long diskOffset;
        IndexEntry(int k, long off) { this.key = k; this.diskOffset = off; }
    }

    public static long binarySearchIndex(IndexEntry[] index, int targetKey) {
        int l = 0, r = index.length - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (index[mid].key == targetKey) return index[mid].diskOffset;
            else if (index[mid].key < targetKey) l = mid + 1;
            else r = mid - 1;
        }
        return -1; // Not found on disk
    }
}""",
        "python_code": """# Inverted Index for Text Search
documents = {
    1: "binary search trees and heaps",
    2: "graphs and shortest paths with dijkstra",
    3: "binary search in sorted arrays"
}

# Build inverted index: word -> set of doc IDs
inverted_index = {}
for doc_id, text in documents.items():
    for word in text.split():
        inverted_index.setdefault(word, set()).add(doc_id)

print("Inverted Index for 'binary':", inverted_index.get("binary"))
print("Inverted Index for 'search':", inverted_index.get("search"))
# Boolean query: documents with BOTH 'binary' AND 'search'
match = inverted_index["binary"] & inverted_index["search"]
print("Docs with 'binary' AND 'search':", match)""",
        "dry_run": json.dumps([
            {"step": 1, "description": "Query received: SELECT * FROM users WHERE id = 45000.", "variables": {"Query": "Equality Search", "Index_Type": "B+ Tree / Hash"}},
            {"step": 2, "description": "Root page loaded into RAM: determines child pointer for range [40000 - 50000].", "variables": {"RAM_I_O": 1, "Page": "Child 4"}},
            {"step": 3, "description": "Leaf page loaded: record found at physical disk offset 0x8FA40.", "variables": {"Disk_Seeks": 2, "Latency": "0.4ms (vs 2000ms full table scan)"}}
        ]),
        "quiz_questions": json.dumps([
            {
                "question": "Why are B+ Trees preferred over Hash Indexes for standard relational database indexes?",
                "options": [
                    "B+ Trees efficiently support range queries (e.g. BETWEEN, >, <) because leaf nodes form a sorted linked list",
                    "B+ Trees use less RAM than Hash Indexes",
                    "Hash indexes cannot handle integer keys",
                    "B+ Trees are faster for exact O(1) single key matches"
                ],
                "answer_idx": 0,
                "explanation": "Hash indexes scatter keys across arbitrary buckets, making range queries require a full scan. B+ Tree leaf nodes are sorted and linked, making range scans trivial."
            }
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "hint": "Indexes trade write speed and disk space for instantaneous read queries."},
            {"level": 2, "hint": "Tree branching factor (B) of 100+ means 100 million records can be queried in just 3-4 page reads."},
            {"level": 3, "hint": "Inverted indexes map terms to documents for full-text search."}
        ])
    },

    # -------------------------------------------------------------
    # Platforms to Practice: LeetCode & Edabit Workflows
    # -------------------------------------------------------------
    {
        "id": "concept_platforms_to_practice",
        "category": "Problem Solving Techniques",
        "difficulty": "Beginner",
        "level_number": 12,
        "level_title": "Level 12: Advanced Techniques & Concurrency",
        "title": "Platforms to Practice: LeetCode, Edabit & Systematic Problem Solving",
        "prerequisites": "All Core DSA Foundations",
        "summary": "Master the methodology of competitive programming and interview prep across LeetCode, Edabit, and HackerRank with pattern recognition.",
        "why_learn_it": "Theoretical knowledge without timed problem-solving leads to freezing in technical interviews. Developing a systematic 5-step problem solving framework guarantees mastery.",
        "fundamental_explanation": "Practicing effectively means focusing on recurring algorithmic patterns (Two Pointers, Sliding Window, Monotonic Stack, BFS/DFS, Top-K Heaps, Interval Merging) rather than memorizing individual solutions.",
        "core_theory": "### The 5-Step Problem Solving Framework:\n1. **Clarify Constraints & Edge Cases:** N size, negative numbers, empty inputs, duplicates.\n2. **Brute Force First:** State the naive O(n²) or O(2ⁿ) solution to establish a baseline.\n3. **Identify Bottlenecks & Patterns:** Can a Hash Table reduce O(n) lookup to O(1)? Can sorting enable Two Pointers?\n4. **Write Clean, Modular Code:** Meaningful variable names, invariant assertions.\n5. **Dry Run with Test Cases:** Trace with small input, single-element input, and edge cases.",
        "time_complexity": "Systematic practice cadence",
        "space_complexity": "Optimal memory trade-offs",
        "video_url": "https://www.youtube.com/embed/KLlXCFG5TnA",
        "video_title": "How to Effectively Practice DSA on LeetCode & Edabit",
        "visualization_type": "searching",
        "visualization_algorithm": "binary_search",
        "practice_problem_slug": "two-sum",
        "java_code": """// The 5-Step Framework applied to Two Sum
import java.util.HashMap;
import java.util.Map;

public class Solution {
    public int[] twoSum(int[] nums, int target) {
        // Step 1: Bottleneck was O(n^2) nested loop
        // Step 2: Use HashMap to trade O(n) space for O(1) lookups
        Map<Integer, Integer> complementMap = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (complementMap.containsKey(complement)) {
                return new int[] { complementMap.get(complement), i };
            }
            complementMap.put(nums[i], i);
        }
        return new int[0];
    }
}""",
        "python_code": """# The 5-Step Framework applied to Two Sum in Python
def two_sum(nums: list[int], target: int) -> list[int]:
    # HashMap stores {number: index}
    seen = {}
    for idx, val in enumerate(nums):
        diff = target - val
        if diff in seen:
            return [seen[diff], idx]
        seen[val] = idx
    return []

print("Two Sum Result:", two_sum([2, 7, 11, 15], 9))""",
        "dry_run": json.dumps([
            {"step": 1, "description": "Read problem statement: Given [2, 7, 11, 15] and target 9, find 2 indices.", "variables": {"Input": [2, 7, 11, 15], "Target": 9}},
            {"step": 2, "description": "Index 0 (val 2): complement is 9 - 2 = 7. Seen map empty. Store {2: 0}.", "variables": {"Seen": "{2: 0}"}},
            {"step": 3, "description": "Index 1 (val 7): complement is 9 - 7 = 2. Found 2 in seen map at index 0!", "variables": {"Result": [0, 1], "Complexity": "O(N) Time, O(N) Space"}}
        ]),
        "quiz_questions": json.dumps([
            {
                "question": "When stuck on an algorithmic problem for more than 25 minutes, what is the best practice?",
                "options": [
                    "Check progressive hints or solution approach, understand the core pattern, then code it from scratch without looking",
                    "Spend 4 more hours staring at the blank screen",
                    "Give up and skip Data Structures completely",
                    "Memorize the solution code line-by-line without understanding"
                ],
                "answer_idx": 0,
                "explanation": "Active learning with progressive hints teaches you pattern recognition without wasting hours in unguided frustration."
            }
        ]),
        "ai_hints": json.dumps([
            {"level": 1, "hint": "Always check constraints on N: if N <= 10^5, an O(N^2) solution will definitely result in Time Limit Exceeded (TLE)."},
            {"level": 2, "hint": "Classify the problem by pattern: is it a subarray problem (Sliding Window / Prefix Sum), or a graph traversal (BFS/DFS)?"},
            {"level": 3, "hint": "Test edge cases: empty array, all negative numbers, duplicate values, and sorted order."}
        ])
    }
]

# Mapping of older lowercase categories to standardized Roadmap categories & levels
CATEGORY_MAPPINGS = {
    # Python Foundation
    "lesson_py_memory": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Python Syntax Basics", "Stack & Heap Memory Architecture in Python (References & Garbage Collection)"),
    "lesson_py_lists": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Memory Architecture", "Python Lists: Dynamic Arrays, Amortized Doubling & Slicing Complexity"),
    "lesson_py_dicts_sets": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Lists & Dynamic Arrays", "Python Dictionaries & Sets: Hash Tables & Collision Mechanisms"),
    "lesson_py_recursion": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Functions & Scope", "Python Recursion & Call Stack Overhead in DSA"),
    "lesson_py_oop_nodes": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Classes & Objects", "Python OOP for DSA: Custom Nodes & Dunder Methods"),

    # Java Foundation
    "lesson_java_memory": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Java Syntax Basics", "Java Memory Architecture: Stack vs Heap & Primitives vs Reference Types"),
    "lesson_java_arrays": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "JVM Memory Model", "Java Arrays & ArrayList: Fixed vs Dynamic Resizing Contiguity"),
    "lesson_java_jcf": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Arrays & ArrayList", "Java Collections Framework (JCF): LinkedList, ArrayDeque & Queue"),
    "lesson_java_hashmap": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "Collections Framework", "Java HashMap & HashSet Internals: Buckets, Collisions & hashCode()"),
    "lesson_java_generics_heaps": ("Programming Fundamentals", "Beginner", 1, "Level 1: Programming Foundations", "HashMap & Interfaces", "Java OOP & Generics: Custom Nodes & PriorityQueue Comparators"),

    # Basic DS
    "lesson_arrays_basics": ("Basic Data Structures", "Beginner", 2, "Level 2: Basic Data Structures", "Programming Fundamentals", "Arrays, Dynamic Arrays & Memory Contiguity"),
    "lesson_strings_basics": ("Basic Data Structures", "Beginner", 2, "Level 2: Basic Data Structures", "Arrays", "String Manipulation, Immutability & StringBuilder"),
    "lesson_linked_list": ("Basic Data Structures", "Beginner", 2, "Level 2: Basic Data Structures", "Pointers & References", "Singly & Doubly Linked Lists: Pointers & References"),
    "lesson_stacks_queues": ("Basic Data Structures", "Beginner", 2, "Level 2: Basic Data Structures", "Linked Lists", "Stacks, Queues & Monotonic Sequences"),
    "lesson_hashmap_subarrays": ("Basic Data Structures", "Beginner", 2, "Level 2: Basic Data Structures", "Arrays & Hash Functions", "Hash Tables: Collision Resolution & Subarray Sum Problems"),

    # Complexity
    "lesson_time_complexity": ("Algorithmic Complexity", "Beginner", 3, "Level 3: Algorithmic Complexity", "Loops & Control Flow", "Time & Space Complexity: Big-O, Big-Ω & Big-Θ"),

    # Search & Sort
    "lesson_binary_search": ("Search Algorithms", "Beginner", 4, "Level 4: Search Algorithms", "Arrays & Sorting", "Searching Algorithms: Linear vs Binary Search & Invariants"),
    "lesson_bubble_sort": ("Sorting Algorithms", "Beginner", 5, "Level 5: Sorting Algorithms", "Arrays & Nested Loops", "Sorting Foundations: Bubble, Selection & Insertion Sort"),
    "lesson_merge_sort": ("Sorting Algorithms", "Intermediate", 5, "Level 5: Sorting Algorithms", "Recursion & Divide and Conquer", "Divide & Conquer Sorting: Merge Sort & Quick Sort"),

    # Techniques
    "lesson_dsa_two_pointers": ("Problem Solving Techniques", "Intermediate", 6, "Level 6: Two Pointers & Sliding Window", "Arrays & Binary Search", "Two Pointer Technique: Inward & Fast-Slow Patterns"),
    "lesson_dsa_sliding_window": ("Problem Solving Techniques", "Intermediate", 6, "Level 6: Two Pointers & Sliding Window", "Two Pointer Technique", "Sliding Window Technique: Fixed vs Dynamic Windows"),
    "lesson_recursion_backtracking": ("Problem Solving Techniques", "Intermediate", 7, "Level 7: Recursion & Backtracking", "Functions & Call Stack", "Recursion Trees, Call Stack & Backtracking (Subsets & N-Queens)"),

    # Trees
    "lesson_trees_bst": ("Tree Data Structures", "Intermediate", 8, "Level 8: Tree Data Structures", "Linked Lists & Recursion", "Binary Trees, BST Operations & Level-Order BFS Traversal"),
    "lesson_dsa_heaps": ("Tree Data Structures", "Intermediate", 8, "Level 8: Tree Data Structures", "Complete Binary Trees", "Heaps & Priority Queues: Complete Binary Trees"),

    # Graphs
    "lesson_graph_traversal": ("Graph Data Structures", "Intermediate", 9, "Level 9: Graph Data Structures", "Trees & Queues", "Graph Representations, BFS & DFS Traversals"),
    "lesson_bfs_dfs": ("Graph Data Structures", "Intermediate", 9, "Level 9: Graph Data Structures", "Graph Representations", "Graph Traversal: Breadth-First & Depth-First Search"),
    "lesson_shortest_paths": ("Graph Data Structures", "Intermediate", 9, "Level 9: Graph Data Structures", "Graph BFS & Priority Queue", "Shortest Paths: Dijkstra's Algorithm & Priority Queue"),
    "lesson_dijkstra": ("Graph Data Structures", "Intermediate", 9, "Level 9: Graph Data Structures", "Priority Queues & Graphs", "Dijkstra's Algorithm: Shortest Paths in Weighted Graphs"),

    # Greedy & DP & Advanced
    "lesson_greedy_algorithms": ("Problem Solving Techniques", "Intermediate", 11, "Level 11: Dynamic Programming & Greedy", "Sorting & Priority Queues", "Greedy Paradigm: Activity Selection & Interval Scheduling"),
    "lesson_dynamic_programming": ("Problem Solving Techniques", "Advanced", 11, "Level 11: Dynamic Programming & Greedy", "Recursion & Memoization", "Dynamic Programming: Memoization, Tabulation & 0/1 Knapsack"),
    "lesson_bit_manipulation": ("Problem Solving Techniques", "Intermediate", 12, "Level 12: Advanced Techniques & Concurrency", "Binary Number System", "Bit Manipulation & Mathematical Algorithms: Bitwise Hacks")
}


def run_comprehensive_roadmap_seed():
    db = SessionLocal()
    try:
        print("Starting comprehensive Roadmap.sh synchronization...")

        # 1. Update existing lessons to proper categories, levels, and prerequisites
        updated_count = 0
        for lesson_id, (cat, diff, lvl, lvl_title, prereq, title) in CATEGORY_MAPPINGS.items():
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if lesson:
                lesson.category = cat
                lesson.difficulty = diff
                lesson.level_number = lvl
                lesson.level_title = lvl_title
                lesson.prerequisites = prereq
                if title:
                    lesson.title = title
                updated_count += 1

        print(f"Standardized {updated_count} legacy lessons to Roadmap.sh categories and levels.")

        # 2. Add additional roadmap concepts from PDF
        inserted_count = 0
        for concept in ADDITIONAL_ROADMAP_CONCEPTS:
            existing = db.query(Lesson).filter(Lesson.id == concept["id"]).first()
            if not existing:
                new_lesson = Lesson(
                    id=concept["id"],
                    topic_id="dsa_master",
                    category=concept["category"],
                    difficulty=concept["difficulty"],
                    level_number=concept["level_number"],
                    level_title=concept["level_title"],
                    title=concept["title"],
                    prerequisites=concept["prerequisites"],
                    summary=concept["summary"],
                    why_learn_it=concept.get("why_learn_it", ""),
                    fundamental_explanation=concept["fundamental_explanation"],
                    core_theory=concept.get("core_theory", ""),
                    step_by_step="Follow interactive step-by-step walkthrough in the tabs above.",
                    real_world_applications="Used extensively in production search engines, memory allocators, and operating systems.",
                    examples_illustrations="Interactive code execution and dry run diagrams below.",
                    pseudocode=concept.get("python_code", ""),
                    related_concepts="Linked data structures and algorithmic complexity.",
                    time_complexity=concept["time_complexity"],
                    space_complexity=concept["space_complexity"],
                    video_url=concept.get("video_url", "https://www.youtube.com/embed/zOjov-2OZ0E"),
                    video_title=concept.get("video_title", "DSA Concept Deep Dive"),
                    visualization_type=concept.get("visualization_type", "searching"),
                    visualization_algorithm=concept.get("visualization_algorithm", "linear_search"),
                    practice_problem_slug=concept.get("practice_problem_slug", "two-sum"),
                    java_code=concept.get("java_code", "// Java Implementation"),
                    python_code=concept.get("python_code", "# Python Implementation"),
                    dry_run=concept.get("dry_run", "[]"),
                    quiz_questions=concept.get("quiz_questions", "[]"),
                    ai_hints=concept.get("ai_hints", "[]"),
                    common_mistakes="Skipping edge case analysis and forgetting memory contiguity trade-offs.",
                    concept_connections=json.dumps({
                        "previous": "Foundational prerequisites",
                        "related": "Core data structure algorithms",
                        "next": "Subsequent advanced roadmap modules"
                    }),
                    mastery_threshold=75,
                    order_index=concept["level_number"] * 10
                )
                db.add(new_lesson)
                inserted_count += 1
            else:
                # Update attributes
                for key, val in concept.items():
                    if hasattr(existing, key):
                        setattr(existing, key, val)
                inserted_count += 1

        # 3. Normalize category names to align with Roadmap.sh exactly
        db.query(Lesson).filter(Lesson.category == "Searching Algorithms").update({"category": "Search Algorithms"})
        db.query(Lesson).filter(Lesson.category.in_(["Trees", "Binary Search Trees", "Heaps and Priority Queues"])).update({"category": "Tree Data Structures"})
        db.query(Lesson).filter(Lesson.category == "Graph Algorithms").update({"category": "Graph Data Structures"})

        db.commit()
        print(f"Added / synchronized {inserted_count} new roadmap nodes from PDF.")

        # Total count
        total = db.query(Lesson).count()
        print(f"Total concepts in AlgoMentor library: {total}")

    except Exception as e:
        db.rollback()
        print(f"Error during roadmap seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run_comprehensive_roadmap_seed()
