from sqlalchemy.orm import Session
from app.models.roadmap import RoadmapStream, RoadmapTopic
from app.models.lesson import Lesson

def seed_language_and_dsa_lessons(db: Session):
    print("[AlgoMentor] Seeding Python, Java and DSA comprehensive curriculum...")

    # Ensure Streams exist for Python Base & Java Base
    streams = [
        RoadmapStream(
            id="python_base",
            title="Python Fundamentals for DSA",
            description="Core language syntax, memory model, references, built-in data structures (lists, dicts, sets, deque), and OOP custom node construction required for algorithmic problem solving in Python.",
            category="language",
            icon="Terminal",
            order_index=0,
            total_hours_estimate=25,
            prerequisites="None (Beginner friendly)"
        ),
        RoadmapStream(
            id="java_base",
            title="Java Fundamentals & JCF for DSA",
            description="Java memory architecture (Stack vs Heap), primitive vs reference types, array resizing, Java Collections Framework (ArrayList, ArrayDeque, HashMap, PriorityQueue), and custom generic nodes.",
            category="language",
            icon="Code2",
            order_index=0,
            total_hours_estimate=30,
            prerequisites="None (Beginner friendly)"
        )
    ]
    for s in streams:
        if not db.query(RoadmapStream).filter(RoadmapStream.id == s.id).first():
            db.add(s)
    db.commit()

    # Topics for Python Base
    py_topics = [
        RoadmapTopic(
            id="py_topic_memory",
            stream_id="python_base",
            title="Python Memory Model, References & Mutability",
            level="Beginner",
            description="How Python assigns variables as object pointers in heap memory, mutable vs immutable types, and shallow vs deep copying.",
            estimated_minutes=60,
            order_index=1,
            milestone_tag="Python Foundations"
        ),
        RoadmapTopic(
            id="py_topic_lists",
            stream_id="python_base",
            title="Python Lists, Slicing & Amortized Doubling",
            level="Beginner",
            description="CPython dynamic array allocation, amortized O(1) append, slice copying complexities, and collections.deque.",
            estimated_minutes=75,
            order_index=2,
            milestone_tag="Dynamic Arrays"
        ),
        RoadmapTopic(
            id="py_topic_dicts",
            stream_id="python_base",
            title="Python Dictionaries & Sets: Hash Tables",
            level="Beginner",
            description="Open addressing hash tables, collision resolution, hashable object requirements, and defaultdict / Counter patterns.",
            estimated_minutes=80,
            order_index=3,
            milestone_tag="Hash Structures"
        ),
        RoadmapTopic(
            id="py_topic_recursion",
            stream_id="python_base",
            title="Python Recursion & Call Stack Overhead",
            level="Intermediate",
            description="Activation frames, call stack limitations, sys.getrecursionlimit(), and writing clean recursive base cases.",
            estimated_minutes=90,
            order_index=4,
            milestone_tag="Recursion Frames"
        ),
        RoadmapTopic(
            id="py_topic_oop",
            stream_id="python_base",
            title="Python OOP for DSA: ListNode, TreeNode & Dunder Methods",
            level="Intermediate",
            description="Building custom node objects for Linked Lists and Trees, pointer linking, and __lt__ for heapq priorities.",
            estimated_minutes=90,
            order_index=5,
            milestone_tag="Custom Objects"
        )
    ]
    for t in py_topics:
        if not db.query(RoadmapTopic).filter(RoadmapTopic.id == t.id).first():
            db.add(t)

    # Topics for Java Base
    java_topics = [
        RoadmapTopic(
            id="java_topic_memory",
            stream_id="java_base",
            title="Java Memory Architecture: Stack vs Heap",
            level="Beginner",
            description="Primitive types vs reference objects, stack activation frames, heap allocation, and NullPointerExceptions.",
            estimated_minutes=60,
            order_index=1,
            milestone_tag="Java Foundations"
        ),
        RoadmapTopic(
            id="java_topic_arrays",
            stream_id="java_base",
            title="Java Arrays & ArrayList Resizing",
            level="Beginner",
            description="Fixed contiguous primitive arrays (int[]) vs dynamic ArrayList<Integer> resizing mechanisms and amortized O(1) growth.",
            estimated_minutes=75,
            order_index=2,
            milestone_tag="Arrays & Lists"
        ),
        RoadmapTopic(
            id="java_topic_jcf",
            stream_id="java_base",
            title="Java Collections Framework: LinkedList, ArrayDeque & Queue",
            level="Intermediate",
            description="Using ArrayDeque for LIFO Stacks and FIFO Queues, LinkedList node chains, and JCF interview best practices.",
            estimated_minutes=90,
            order_index=3,
            milestone_tag="Collections (JCF)"
        ),
        RoadmapTopic(
            id="java_topic_hashmap",
            stream_id="java_base",
            title="Java HashMap & HashSet Internals",
            level="Intermediate",
            description="Bucket arrays, load factor (0.75), hashCode() & equals() contract, and collision resolution (Linked list to Red-Black tree).",
            estimated_minutes=90,
            order_index=4,
            milestone_tag="Hashing Internals"
        ),
        RoadmapTopic(
            id="java_topic_generics",
            stream_id="java_base",
            title="Java OOP & Generics: Custom Nodes & PriorityQueue Comparators",
            level="Intermediate",
            description="Writing generic ListNode<T> and TreeNode<T>, Min-Heap vs Max-Heap PriorityQueue with lambda Comparators.",
            estimated_minutes=100,
            order_index=5,
            milestone_tag="Generics & Heaps"
        )
    ]
    for t in java_topics:
        if not db.query(RoadmapTopic).filter(RoadmapTopic.id == t.id).first():
            db.add(t)
    db.commit()

    # Comprehensive Concept Lessons List
    all_lessons = [
        # ==========================================================
        # PYTHON BASE LESSONS FOR DSA
        # ==========================================================
        Lesson(
            id="lesson_py_memory",
            topic_id="py_topic_memory",
            category="python",
            title="Python Memory Model: References, Object Identity & Mutability",
            summary="Master how Python allocates objects in heap memory and manages variable references so you never encounter accidental state mutation bugs in DSA.",
            fundamental_explanation="""In Python, variables do not hold values directly; they hold memory references (pointers) to objects residing in heap memory.

Understanding the distinction between mutable and immutable types is critical in DSA:
1. **Immutable Types**: `int`, `float`, `str`, `tuple`, `frozenset`. Any operation that appears to modify an immutable object creates a new object in memory.
2. **Mutable Types**: `list`, `dict`, `set`, and user-defined class instances. Modifying a mutable object alters its internal state in-place, affecting all variables that reference that same object (aliasing).

When passing arguments into functions (such as a recursive backtracking tree function), Python uses **Pass-by-Object-Reference**. If you pass a list and modify it (`arr.append(x)`), the caller's list is directly mutated. To isolate states, shallow copy (`arr[:]` or `arr.copy()`) or deep copy (`copy.deepcopy()`) must be deliberately used.""",
            step_by_step="""1. Memory Assignment: When `a = [1, 2, 3]` executes, a list object is allocated in heap memory and `a` stores its address.
2. Aliasing: When `b = a` executes, `b` points to the identical heap address as `a` (`id(a) == id(b)`).
3. In-Place Mutation: `b.append(4)` mutates the shared heap object. Therefore, `a` also displays `[1, 2, 3, 4]`.
4. Creating Copies: `c = a[:]` or `c = list(a)` allocates a new distinct list object in heap memory with copied element references.
5. In Backtracking: Always pass a copy of your path into result lists: `result.append(path[:])` instead of `result.append(path)`.""",
            real_world_applications="Prevents corrupting visited sets in graph DFS, avoids state leaks across recursion branches in backtracking (e.g. N-Queens, Subsets, Permutations), and optimizes memory footprint in tree algorithms.",
            examples_illustrations="""# Aliasing Pitfall:
a = [1, 2, 3]
b = a
b.append(99)
print(a) # Output: [1, 2, 3, 99] (both mutated!)

# Correct Isolation for DSA:
a = [1, 2, 3]
b = a[:] # Slice creates a shallow copy
b.append(99)
print(a) # Output: [1, 2, 3] (preserved!)""",
            pseudocode="""# Backtracking state isolation pattern:
function backtrack(path, choices):
    if is_solution(path):
        result.append(copy(path)) # MUST copy to freeze state
        return
    for choice in choices:
        path.append(choice)
        backtrack(path, choices)
        path.pop() # Backtrack step""",
            time_complexity="O(1) Reference assignment, O(N) Shallow copy",
            space_complexity="O(1) Aliasing, O(N) New copy allocation",
            prerequisites="Basic Python syntax",
            related_concepts="Pointers, Heap Allocation, Garbage Collection, Shallow vs Deep Copy",
            video_url="https://www.youtube.com/embed/_AEJHKGk9ns",
            video_title="Python Memory Management & Variables Under The Hood",
            visualization_type="linked_list",
            visualization_algorithm="linked_list",
            order_index=10
        ),
        Lesson(
            id="lesson_py_lists",
            topic_id="py_topic_lists",
            category="python",
            title="Python Lists: Dynamic Arrays, Amortized Doubling & Slicing Complexity",
            summary="Understand how Python implements lists as dynamic contiguous arrays, why append is amortized O(1), and why pop(0) is an O(N) anti-pattern.",
            fundamental_explanation="""Under the hood in CPython, a `list` is implemented as an array of contiguous pointers (`PyListObject`).

Key algorithmic realities of Python lists:
1. **Random Access (`arr[i]`)**: Requires calculating `base_address + i * pointer_size`. This is direct arithmetic taking strict $O(1)$ constant time.
2. **Appends (`arr.append(x)`)**: When the allocated capacity is reached, CPython allocates a new larger block of memory (roughly $1.125\\times$ plus 9 slots), copies over existing pointers, and frees the old block. Because resizings are infrequent, appending takes **$O(1)$ amortized time**.
3. **Insert / Delete at Front (`arr.pop(0)`, `arr.insert(0, x)`)**: Forces all subsequent $N-1$ pointers to be shifted in memory. This is an **$O(N)$ linear time operation**!
4. **Queue Alternative (`collections.deque`)**: A doubly-linked block of contiguous chunks providing true **$O(1)$ `popleft()` and `appendleft()`** for BFS and Queues.
5. **Slicing (`arr[start:end]`)**: Creates an entirely new list object containing the specified range, taking **$O(K)$ time and space** where $K = end - start$.""",
            step_by_step="""1. Index Access: `val = arr[idx]` -> Direct memory offset O(1).
2. Appending: `arr.append(val)` -> Places pointer at current end. If full, triggers dynamic reallocation in amortized O(1).
3. Popping from End: `arr.pop()` -> Decrements length counter in strict O(1).
4. Popping from Start: `arr.pop(0)` -> Shifts all elements left by 1. AVOID in queue/BFS problems; use `deque.popleft()` instead!
5. Slicing: `sub = arr[2:5]` -> Allocates new list of size 3 and copies references in O(K).""",
            real_world_applications="Optimizing BFS graph traversal queues from O(V²) down to O(V+E) by replacing `list.pop(0)` with `collections.deque.popleft()`, and avoiding accidental O(N) slice operations inside loops.",
            examples_illustrations="""from collections import deque
import time

# Anti-pattern: O(N^2) total runtime
arr = list(range(100000))
# arr.pop(0) -> Shifts 100,000 pointers on EVERY call!

# Optimal DSA Pattern: O(N) total runtime
q = deque(range(100000))
val = q.popleft() # Strict O(1) constant time pointer update!""",
            pseudocode="""# BFS Queue Implementation in Python:
from collections import deque

function BFS(graph, root):
    queue = deque([root]) # Use deque, NOT list
    visited = {root}
    while queue:
        node = queue.popleft() # O(1) time
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor) # O(1) time""",
            time_complexity="Access: O(1), Append: Amortized O(1), Pop Left: O(N) on List vs O(1) on Deque",
            space_complexity="O(N) contiguous pointer buffer",
            prerequisites="Python variables and loops",
            related_concepts="Dynamic Arrays, Amortized Analysis, Ring Buffers, Deque",
            video_url="https://www.youtube.com/embed/5mTrzS5m9Y8",
            video_title="How Python Lists Work Under The Hood (CPython Internals)",
            visualization_type="sorting",
            visualization_algorithm="bubble_sort",
            order_index=11
        ),
        Lesson(
            id="lesson_py_dicts_sets",
            topic_id="py_topic_dicts",
            category="python",
            title="Python Dictionaries & Sets: Hash Tables & Collision Mechanisms",
            summary="Explore CPython's compact hash table architecture, open addressing collision resolution, and why keys must be hashable.",
            fundamental_explanation="""Python `dict` and `set` are high-performance Hash Tables.

How Python Hash Tables work:
1. **Hash Calculation**: Python computes `hash(key)`. The hash integer is mapped to a table index using bitwise modulo: `index = hash & (size - 1)`.
2. **Open Addressing with Perturbation**: When two keys map to the same index (a hash collision), Python does not use separate chaining (linked lists); it uses open addressing with a mathematical perturbation formula: `perturb >>= 5; index = (5 * index + 1 + perturb) & mask` until an empty slot is found.
3. **Hashable Requirement**: Only immutable objects implementing `__hash__()` and `__eq__()` can be dictionary keys or set elements. Lists and dicts are mutable and cannot be keys; tuples and strings can.
4. **Time Complexity**: Average case operations (`lookup`, `insert`, `delete`) are **$O(1)$ constant time**. In worst-case pathological collision scenarios, it degrades to $O(N)$.""",
            step_by_step="""1. Compute `h = hash(key)`.
2. Locate candidate index in internal entries table.
3. If entry is empty: insert new key-value pair and return.
4. If entry contains an existing key: compare equality using `key1 == key2`.
5. If equal: overwrite existing value in O(1).
6. If not equal (Collision): compute next probe index using perturbation recurrence until an empty or matching slot is located.""",
            real_world_applications="Powers O(N) Two Sum lookup, character frequency counts, graph adjacency lists, and memoization caches in dynamic programming (`@functools.lru_cache`).",
            examples_illustrations="""from collections import defaultdict, Counter

# 1. Frequency counting in O(N):
words = ["apple", "banana", "apple", "cherry"]
freq = Counter(words) # {'apple': 2, 'banana': 1, 'cherry': 1}

# 2. Graph adjacency list with defaultdict:
graph = defaultdict(list)
graph['A'].append('B') # Automatically creates list on first access!""",
            pseudocode="""# Two Sum using Hash Map:
function twoSum(nums, target):
    seen = {} # Hash Map
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen: # O(1) average lookup
            return [seen[complement], i]
        seen[num] = i # O(1) average insertion
    return []""",
            time_complexity="O(1) Average Lookup/Insert, O(N) Worst Case (Pathological collisions)",
            space_complexity="O(N) Auxiliary Hash Table Storage",
            prerequisites="Python data types, modulo arithmetic",
            related_concepts="Hash Functions, Open Addressing, Separate Chaining, Load Factor",
            video_url="https://www.youtube.com/embed/C4Kc8xzcA68",
            video_title="How Python Dictionaries Are Implemented So Fast",
            visualization_type="searching",
            visualization_algorithm="binary_search",
            order_index=12
        ),
        Lesson(
            id="lesson_py_recursion",
            topic_id="py_topic_recursion",
            category="python",
            title="Python Recursion & Call Stack Overhead in DSA",
            summary="Learn how function call stack frames are pushed and popped, base case discipline, and managing Python's recursion limit.",
            fundamental_explanation="""Recursion is a programming paradigm where a function solves a problem by calling smaller instances of itself.

Every recursive call in Python creates a new **Stack Frame** in system memory. A stack frame stores:
- Function arguments
- Local variables
- Return instruction pointer

Key rules for recursion in DSA:
1. **Base Case**: The termination condition where no further recursive calls are made. Without a base case, recursion runs indefinitely until reaching `RecursionError: maximum recursion depth exceeded`.
2. **Recursive Transition**: Reducing the input parameters toward the base case (e.g. `n - 1`, `node.left`, `node.right`).
3. **Call Stack Limit**: Python defaults to a recursion depth limit of 1000 to protect against C-level stack overflow. For deep trees or graphs, `sys.setrecursionlimit(200000)` can be adjusted, or recursion can be converted to an iterative stack.
4. **Recursion vs Dynamic Programming**: Pure recursion repeatedly solves overlapping subproblems (e.g. $O(2^N)$ Fibonacci). Adding a hash map memoization cache reduces time complexity down to $O(N)$.""",
            step_by_step="""1. Evaluate Base Condition: If base condition is satisfied, return immediate constant-time value.
2. Break Down Input: Divide current problem into one or more subproblems of smaller size.
3. Recursive Call: Push current stack frame to call stack and invoke function with smaller arguments.
4. Unwinding / Backtracking: When base case returns, stack frames pop off in LIFO (Last-In-First-Out) order.
5. Combine Results: Aggregate return values from recursive sub-calls to produce the current frame's result.""",
            real_world_applications="Depth-First Search (DFS) on graphs and trees, divide-and-conquer sorting (Merge Sort, Quick Sort), tree depth calculations, and hierarchical file system traversals.",
            examples_illustrations="""import sys
# Check or increase recursion limit:
print(sys.getrecursionlimit()) # Default: 1000

# Recursive Tree Traversal:
def max_depth(root):
    if not root:
        return 0 # Base case
    # Recursive step:
    return 1 + max(max_depth(root.left), max_depth(root.right))""",
            pseudocode="""function factorial(n):
    if n <= 1: # Base Case
        return 1
    return n * factorial(n - 1) # Recursive Step""",
            time_complexity="O(N) for linear recursion, O(2^N) for unmemoized tree recursion",
            space_complexity="O(H) Auxiliary Stack Space where H is recursion tree height",
            prerequisites="Python functions, call stacks",
            related_concepts="Call Stack, Memoization, Tail Recursion, Divide & Conquer",
            video_url="https://www.youtube.com/embed/ngCos392W4w",
            video_title="Recursion in 100 Seconds & Call Stack Mental Model",
            visualization_type="tree",
            visualization_algorithm="binary_search",
            order_index=13
        ),
        Lesson(
            id="lesson_py_oop_nodes",
            topic_id="py_topic_oop",
            category="python",
            title="Python OOP for DSA: Custom Nodes & Dunder Methods",
            summary="Build reusable ListNode, TreeNode, and GraphNode class architectures and implement custom __lt__ comparison operators for Heaps.",
            fundamental_explanation="""Most advanced Data Structures (Linked Lists, Binary Trees, Tries, Graphs) require creating custom object nodes in Python.

Essential Node architectures in DSA:
1. **`ListNode`**: Holds `val` (data payload) and `next` (reference to adjacent node or `None`).
2. **`TreeNode`**: Holds `val`, `left` (reference to left child node), and `right` (reference to right child node).
3. **`TrieNode`**: Holds `children` (dictionary of char -> TrieNode) and `is_end_of_word` (boolean flag).
4. **Dunder Methods in DSA**:
   - `__init__`: Initializes node values and pointer defaults.
   - `__repr__`: Prints readable debugging representations of data structures.
   - `__lt__`: Less-than operator. Required when storing custom node objects inside a Priority Queue / `heapq` so Python knows how to break ties!""",
            step_by_step="""1. Define class with class keyword: `class ListNode:`.
2. Constructor `__init__(self, val=0, next=None)`: Bind payload and pointer attributes to instance.
3. Linking nodes: `node1.next = node2` creates a directed pointer from node1 to node2 in heap memory.
4. Implementing `__lt__(self, other)`: Define `return self.val < other.val` to support sorting and min-heaps with `heapq.heappush(heap, node)`.""",
            real_world_applications="Fundamental foundation for LeetCode / interview Linked List problems (Reverse Linked List, Merge Two Sorted Lists), Binary Search Tree implementations, and Trie prefix search engines.",
            examples_illustrations="""class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Using __lt__ for heapq:
class PriorityNode:
    def __init__(self, priority, data):
        self.priority = priority
        self.data = data
    def __lt__(self, other):
        return self.priority < other.priority""",
            pseudocode="""# In-place Linked List Reversal:
function reverseList(head):
    prev = None
    curr = head
    while curr is not None:
        next_temp = curr.next # Save next
        curr.next = prev      # Reverse pointer
        prev = curr           # Advance prev
        curr = next_temp      # Advance curr
    return prev""",
            time_complexity="O(1) Node allocation, O(1) Pointer re-assignment",
            space_complexity="O(1) Auxiliary space per node",
            prerequisites="Python class syntax, pointers",
            related_concepts="Classes, Objects, Pointers, Memory References, Dunder Methods",
            video_url="https://www.youtube.com/embed/FSsriWQ0qYE",
            video_title="Object Oriented Programming in Python for Coding Interviews",
            visualization_type="linked_list",
            visualization_algorithm="linked_list",
            practice_problem_slug="count-vowels-in-a-string",
            order_index=14
        ),

        # ==========================================================
        # JAVA BASE LESSONS FOR DSA
        # ==========================================================
        Lesson(
            id="lesson_java_memory",
            topic_id="java_topic_memory",
            category="java",
            title="Java Memory Architecture: Stack vs Heap & Primitives vs Reference Types",
            summary="Master Java's memory allocation, 8 primitive data types, reference variables, pass-by-value semantics, and garbage collection.",
            fundamental_explanation="""Java manages memory through the JVM divided into two primary memory regions:

1. **Call Stack (Stack Memory)**:
   - Stores primitive local variables (`int`, `double`, `boolean`, `char`, `long`, `byte`, `short`, `float`).
   - Stores references (memory addresses) pointing to objects.
   - Extremely fast allocation and deallocation governed by method execution boundaries.
2. **Heap Memory**:
   - Stores all Objects and Arrays (`new int[10]`, `new String()`, `new ArrayList<>()`).
   - Managed automatically by the Garbage Collector (GC).
3. **Pass-by-Value in Java**:
   - Java is **strictly pass-by-value**.
   - For primitives: a copy of the actual value is passed.
   - For objects: a copy of the **reference (address pointer)** is passed. Therefore, modifying object fields inside a method (`node.val = 5`) alters the shared heap object, but re-assigning the reference (`node = new Node()`) does NOT affect the caller's variable!
4. **NullPointerException (NPE)**:
   - Occurs when attempting to dereference a reference variable that points to `null` (`curr.next` when `curr == null`). Guarding against null is mandatory in tree and linked list problems.""",
            step_by_step="""1. Declaring `int x = 10;`: Allocates 4 bytes on current thread's call stack storing value 10.
2. Declaring `int[] arr = new int[5];`: Allocates reference `arr` on the stack pointing to an array object of 5 integers in heap memory.
3. Method Call: New stack frame is pushed. Arguments are copied by value into the frame.
4. Method Return: Stack frame is instantly popped off memory.
5. Garbage Collection: When heap objects have zero remaining stack references, they are marked for garbage collection.""",
            real_world_applications="Prevents NullPointerExceptions in binary tree traversals, explains why primitive arrays `int[]` run significantly faster than `ArrayList<Integer>` due to CPU cache locality and zero object header overhead.",
            examples_illustrations="""// Primitive on Stack:
int a = 5;
int b = a; // Copy of value 5
b = 10;    // a remains 5!

// Reference on Heap:
int[] arr1 = new int[]{1, 2, 3};
int[] arr2 = arr1; // Copies reference pointer
arr2[0] = 99;
System.out.println(arr1[0]); // Prints 99 (shared heap object!)""",
            pseudocode="""// Safe pointer dereferencing in Java:
function getNodeValue(ListNode node):
    if (node == null) return -1; // Guard against NPE
    return node.val;""",
            time_complexity="O(1) Stack allocation, O(1) Heap pointer access",
            space_complexity="O(1) Primitive, O(N) Object in Heap",
            prerequisites="Basic Java syntax",
            related_concepts="JVM, Stack, Heap, Garbage Collection, Pass-by-Value, NPE",
            video_url="https://www.youtube.com/embed/5OJRqkYbK-4",
            video_title="Java Memory Management: Stack vs Heap Explained",
            visualization_type="linked_list",
            visualization_algorithm="linked_list",
            order_index=20
        ),
        Lesson(
            id="lesson_java_arrays",
            topic_id="java_topic_arrays",
            category="java",
            title="Java Arrays & ArrayList: Fixed vs Dynamic Resizing Contiguity",
            summary="Compare fixed native primitive arrays (int[]) with dynamic resizable ArrayLists, capacity expansion (1.5x), and autoboxing overhead.",
            fundamental_explanation="""In Java, sequential collections fall into two fundamental categories:

1. **Native Fixed-Size Arrays (`int[]`, `String[]`)**:
   - Fixed capacity allocated at creation time: `int[] arr = new int[n];`.
   - Store elements contiguously in heap memory.
   - No object wrapper overhead for primitives: `int[]` uses exactly $4 \\times N$ bytes.
   - Unmatched CPU cache line efficiency. Preferred in competitive programming and tight time constraints.
2. **Dynamic Arrays (`ArrayList<T>`)**:
   - Resizable array implementation of the `List` interface.
   - Backed by an internal `Object[] elementData` array.
   - When capacity is exceeded, it allocates a new array with capacity: `newCapacity = oldCapacity + (oldCapacity >> 1)` (1.5x growth), copies elements via `System.arraycopy()`, and drops the old array.
   - **Autoboxing / Unboxing Overhead**: `ArrayList<Integer>` cannot store primitive `int` directly; each integer is wrapped in a `java.lang.Integer` object (consuming 16–24 bytes per element instead of 4 bytes).""",
            step_by_step="""1. Creating Array: `int[] nums = new int[size];` -> Allocates fixed contiguous block.
2. Direct Access: `nums[i]` -> Direct memory address offset calculated in O(1).
3. Dynamic List: `List<Integer> list = new ArrayList<>();` -> Initializes default capacity of 10.
4. Adding Elements: `list.add(val)` -> Appends to index size. If full, triggers 1.5x capacity reallocation.
5. Converting: `list.get(i)` -> O(1) indexed lookup with unboxing to primitive int.""",
            real_world_applications="Selecting `int[]` for frequency arrays and matrix grids to avoid GC pressure and autoboxing delays, while utilizing `ArrayList` for dynamic graph adjacency lists where neighbor counts vary per vertex.",
            examples_illustrations="""// 1. Primitive Array (Highest performance):
int[] count = new int[26]; // 26 letters, 0 allocations after creation
count[c - 'a']++;

// 2. ArrayList Dynamic Growth:
List<Integer> dynamicList = new ArrayList<>();
for (int i = 0; i < 100; i++) {
    dynamicList.add(i); // Amortized O(1) append
}""",
            pseudocode="""// Adjacency List for Graph in Java:
List<List<Integer>> graph = new ArrayList<>();
for (int i = 0; i < numVertices; i++) {
    graph.add(new ArrayList<>());
}
graph.get(u).add(v); // Add directed edge u -> v""",
            time_complexity="Indexed Access: O(1), Append: Amortized O(1), Search: O(N)",
            space_complexity="Native: 4N bytes, ArrayList<Integer>: ~24N bytes (Object overhead)",
            prerequisites="Java data types and syntax",
            related_concepts="Contiguous Memory, Dynamic Resizing, Autoboxing, Cache Lines",
            video_url="https://www.youtube.com/embed/9GdesxTtV6Y",
            video_title="Java ArrayList vs Array: Performance & Internal Architecture",
            visualization_type="sorting",
            visualization_algorithm="bubble_sort",
            order_index=21
        ),
        Lesson(
            id="lesson_java_jcf",
            topic_id="java_topic_jcf",
            category="java",
            title="Java Collections Framework (JCF): LinkedList, ArrayDeque & Queue",
            summary="Explore the standard Java Collections hierarchy, why ArrayDeque outperforms legacy Stack, and implementing BFS queues with Queue interface.",
            fundamental_explanation="""The Java Collections Framework (JCF) provides unified data structures under the `java.util` package:

Key Collections for DSA Interviews:
1. **`Queue<T>` and `Deque<T>`**:
   - `Queue<T> q = new ArrayDeque<>();` is the industry standard for BFS.
   - Operations: `offer(e)` (enqueue without throwing exception), `poll()` (dequeue), `peek()` (inspect front).
2. **`ArrayDeque<T>` vs Legacy `Stack<T>`**:
   - `java.util.Stack` inherits from `Vector` and synchronizes every method, incurring heavy lock overhead.
   - `Deque<Integer> stack = new ArrayDeque<>();` is non-synchronized, backed by a circular array buffer, and executes significantly faster for LIFO stacks (`push()`, `pop()`, `peek()`).
3. **`LinkedList<T>`**:
   - Doubly-linked node list implementing both `List<T>` and `Deque<T>`.
   - Higher memory overhead per element (node object + previous pointer + next pointer + data pointer).
   - `ArrayDeque` is almost universally preferred over `LinkedList` in competitive programming due to cache locality.""",
            step_by_step="""1. For BFS Queues: Use `Queue<TreeNode> queue = new ArrayDeque<>();`.
2. Enqueue: `queue.offer(node);`
3. Dequeue: `TreeNode curr = queue.poll();`
4. For LIFO Stacks: Use `Deque<Character> stack = new ArrayDeque<>();`.
5. Push to Stack: `stack.push('(');`
6. Pop from Stack: `char c = stack.pop();`""",
            real_world_applications="Parentheses validation using `ArrayDeque`, Breadth-First Search on trees and 2D grids, and sliding window maximum algorithms using monotonic double-ended queues.",
            examples_illustrations="""// Standard BFS in Java:
Queue<TreeNode> queue = new ArrayDeque<>();
queue.offer(root);
while (!queue.isEmpty()) {
    int levelSize = queue.size();
    for (int i = 0; i < levelSize; i++) {
        TreeNode curr = queue.poll();
        if (curr.left != null) queue.offer(curr.left);
        if (curr.right != null) queue.offer(curr.right);
    }
}""",
            pseudocode="""// Valid Parentheses in Java:
Deque<Character> stack = new ArrayDeque<>();
for (char c : s.toCharArray()) {
    if (c == '(') stack.push(')');
    else if (c == '{') stack.push('}');
    else if (c == '[') stack.push(']');
    else if (stack.isEmpty() || stack.pop() != c) return false;
}
return stack.isEmpty();""",
            time_complexity="O(1) push, pop, offer, poll on ArrayDeque",
            space_complexity="O(N) Queue / Stack capacity buffer",
            prerequisites="Java interfaces, Generics",
            related_concepts="Queue, Deque, Stack, FIFO, LIFO, Circular Buffer",
            video_url="https://www.youtube.com/embed/hzGZZi5hMvE",
            video_title="Java Collections Framework Full Hierarchy Explained",
            visualization_type="stack_queue",
            visualization_algorithm="bubble_sort",
            practice_problem_slug="valid-parentheses",
            order_index=22
        ),
        Lesson(
            id="lesson_java_hashmap",
            topic_id="java_topic_hashmap",
            category="java",
            title="Java HashMap & HashSet Internals: Buckets, Collisions & hashCode()",
            summary="Dive deep into Java's HashMap table of Node buckets, 0.75 load factor threshold, hash collisions, and the Red-Black Tree upgrade.",
            fundamental_explanation="""Java's `HashMap<K, V>` is one of the most frequently tested data structures in software engineering interviews.

Internal Architecture:
1. **Bucket Array**: Backed by `Node<K, V>[] table`. The table size is always a power of 2 ($16, 32, 64, \\dots$).
2. **Hash Function & Index**:
   - Java computes hash: `int hash = (key == null) ? 0 : (h = key.hashCode()) ^ (h >>> 16);` (spreads higher bits to prevent clustering).
   - Index: `index = hash & (n - 1);`.
3. **Collision Handling & Treeification**:
   - Initial collisions are resolved via Separate Chaining (singly-linked list).
   - **Treeification Threshold**: If a single bucket exceeds **8 elements** and the total table capacity is at least 64, Java converts that bucket's linked list into a **Red-Black Balanced Binary Search Tree (`TreeNode<K,V>`)**!
   - This guarantees that worst-case lookup never degrades to $O(N)$, but stays bounded at **$O(\\log N)$**!
4. **`hashCode()` & `equals()` Contract**:
   - If `a.equals(b)` is true, `a.hashCode() == b.hashCode()` MUST be true.
   - If overriding `equals()`, you MUST override `hashCode()`. Failing to do so causes duplicate entries and failed lookups in `HashMap` and `HashSet`.""",
            step_by_step="""1. Call `map.put(key, value)`: Calculate key's hash.
2. Determine bucket index `i = hash & (table.length - 1)`.
3. If bucket is empty: insert new Node<K,V>.
4. If bucket has entries: iterate linked list or balanced tree comparing hash and `equals()`.
5. If key matches: replace existing value and return old value.
6. If key is new: append to bucket. If bucket length reaches 8, convert to Red-Black Tree.
7. If total size exceeds `capacity * loadFactor` (default 0.75): double table capacity and rehash.""",
            real_world_applications="Two Sum complement lookup in O(N), Subarray Sum Equals K using prefix sums in HashMap, and frequency counting for anagram grouping.",
            examples_illustrations="""Map<String, Integer> map = new HashMap<>();
map.put("apple", 3);
map.put("banana", 5);

// getOrDefault pattern for frequency counting:
map.put("apple", map.getOrDefault("apple", 0) + 1);

// Checking existence in O(1):
if (map.containsKey("banana")) {
    int count = map.get("banana");
}""",
            pseudocode="""// Two Sum in Java using HashMap:
Map<Integer, Integer> map = new HashMap<>();
for (int i = 0; i < nums.length; i++) {
    int complement = target - nums[i];
    if (map.containsKey(complement)) {
        return new int[]{map.get(complement), i};
    }
    map.put(nums[i], i);
}""",
            time_complexity="O(1) Average Lookup/Insert, O(log N) Worst-Case Bucket Collision (Treeified)",
            space_complexity="O(N) Hash Table Storage with 0.75 load factor",
            prerequisites="Java classes, bitwise operations",
            related_concepts="Hashing, Red-Black Trees, Separate Chaining, Load Factor",
            video_url="https://www.youtube.com/embed/c3RVW3KGIIE",
            video_title="How Java HashMap Works Internally (Bucket Array & Treeification)",
            visualization_type="searching",
            visualization_algorithm="binary_search",
            practice_problem_slug="two-sum",
            order_index=23
        ),
        Lesson(
            id="lesson_java_generics_heaps",
            topic_id="java_topic_generics",
            category="java",
            title="Java OOP & Generics: Custom Nodes & PriorityQueue Comparators",
            summary="Create generic custom Node classes and master PriorityQueue Min-Heap and Max-Heap configuration using lambda Comparators.",
            fundamental_explanation="""In technical interviews with Java, solving Graph and Top-K problems requires writing custom classes and configuring `PriorityQueue`.

1. **Custom Generic Node Architecture**:
   - `class ListNode<T> { T val; ListNode<T> next; }` allows building type-safe data structures.
2. **`PriorityQueue<T>` (Binary Heap)**:
   - Implemented as a resizable array representing a complete binary tree.
   - **Default behavior**: **Min-Heap** (natural ordering where smallest element is at the top).
   - `peek()` and `poll()` retrieve the minimum element in **$O(\\log N)$** time.
3. **Custom Comparators / Max-Heap**:
   - To create a **Max-Heap**, pass a custom `Comparator`:
     - Lambda expression: `PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> b - a);`
     - Or reverse order: `PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());`
4. **Dijkstra State Nodes**:
   - Storing `(nodeId, distance)` pairs in a PriorityQueue:
     - `PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));`
     - `a[1]` represents distance; the comparator ensures the shortest tentative distance is always popped next.""",
            step_by_step="""1. Define Min-Heap: `PriorityQueue<Integer> minHeap = new PriorityQueue<>();`
2. Define Max-Heap: `PriorityQueue<Integer> maxHeap = new PriorityQueue<>((a, b) -> b - a);`
3. Add Elements: `pq.offer(val);` -> Inserts element and performs up-heap bubble in O(log N).
4. Inspect Root: `pq.peek();` -> Returns min (or max) in strict O(1).
5. Extract Root: `pq.poll();` -> Removes root and performs down-heap bubble in O(log N).""",
            real_world_applications="Dijkstra's shortest path algorithm, Prim's Minimum Spanning Tree, Top-K Frequent Elements, Merge K Sorted Lists, and Find Median from Data Stream.",
            examples_illustrations="""// PriorityQueue for Dijkstra:
// Storing {vertex, distance}
PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[1], b[1]));
pq.offer(new int[]{startNode, 0});

while (!pq.isEmpty()) {
    int[] curr = pq.poll();
    int u = curr[0];
    int dist = curr[1];
    // Relax edges...
}""",
            pseudocode="""// Top K Frequent Elements using Min-Heap:
PriorityQueue<Map.Entry<Integer, Integer>> pq = 
    new PriorityQueue<>((a, b) -> a.getValue() - b.getValue());

for (Map.Entry<Integer, Integer> entry : countMap.entrySet()) {
    pq.offer(entry);
    if (pq.size() > k) {
        pq.poll(); // Evict smallest frequency
    }
}""",
            time_complexity="Insert/Remove: O(log N), Peek: O(1), Heapify: O(N)",
            space_complexity="O(N) Heap Array Storage",
            prerequisites="Java Generics, Interfaces, Lambda Expressions",
            related_concepts="Binary Heap, Min-Heap, Max-Heap, Comparator, Dijkstra",
            video_url="https://www.youtube.com/embed/wptevk0bshY",
            video_title="Java PriorityQueue & Custom Comparators Masterclass",
            visualization_type="dijkstra",
            visualization_algorithm="dijkstra",
            order_index=24
        ),

        # ==========================================================
        # CORE DSA & ALGORITHM CONCEPTS
        # ==========================================================
        Lesson(
            id="lesson_dsa_two_pointers",
            topic_id="dsa_arrays_101",
            category="algorithm",
            title="The Two-Pointer Paradigm: Converging, Diverging & Fast-Slow",
            summary="Eliminate nested O(N²) loops by strategically coordinating two pointers on sorted arrays, palindromes, and linked lists.",
            fundamental_explanation="""The Two-Pointer approach is an algorithmic optimization technique where two index pointers traverse a sequence concurrently.

Three Classical Patterns:
1. **Opposite-Direction (Inward Converging)**:
   - One pointer starts at index 0 (`left`), another at index `n - 1` (`right`).
   - Pointers move inward based on conditions (e.g. `sum < target -> left++`, `sum > target -> right--`).
   - Classic problems: Two Sum II (Sorted), Valid Palindrome, Container With Most Water.
2. **Fast & Slow Pointers (Floyd's Cycle Detection)**:
   - `slow` advances 1 step at a time; `fast` advances 2 steps.
   - If a cycle exists, `fast` will inevitably lap `slow` inside the loop in $O(N)$ time and $O(1)$ space.
   - Classic problems: Linked List Cycle, Find the Duplicate Number, Middle of Linked List.
3. **Same-Direction (Reader & Writer)**:
   - `fast` explores elements; `slow` records the write position in-place.
   - Classic problems: Remove Duplicates from Sorted Array, Move Zeroes.""",
            step_by_step="""1. Initialize `left = 0`, `right = arr.length - 1`.
2. While `left < right`:
3. Calculate condition: `current_sum = arr[left] + arr[right]`.
4. If `current_sum == target`: solution located.
5. If `current_sum < target`: increase sum by advancing `left += 1`.
6. If `current_sum > target`: decrease sum by retreating `right -= 1`.
7. Concludes in at most N pointer movements (O(N) time).""",
            real_world_applications="High-throughput stream processing, in-place array compaction without extra memory allocation, and hardware packet deduplication.",
            examples_illustrations="""# Two Sum II on Sorted Array:
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        curr = nums[left] + nums[right]
        if curr == target:
            return [left + 1, right + 1]
        elif curr < target:
            left += 1
        else:
            right -= 1
    return []""",
            pseudocode="""function twoPointer(arr, target):
    l = 0
    r = length(arr) - 1
    while l < r:
        if evaluate(arr[l], arr[r]) == target:
            return (l, r)
        else if condition:
            l = l + 1
        else:
            r = r - 1""",
            time_complexity="O(N) Single-pass traversal",
            space_complexity="O(1) Auxiliary Pointers",
            prerequisites="Array indexing",
            related_concepts="Sliding Window, Binary Search, In-Place Array Mutation",
            video_url="https://www.youtube.com/embed/-waUPfpxsGo",
            video_title="Two Pointer Technique Explained with Animations",
            visualization_type="searching",
            visualization_algorithm="binary_search",
            practice_problem_slug="two-sum",
            order_index=30
        ),
        Lesson(
            id="lesson_dsa_sliding_window",
            topic_id="dsa_arrays_101",
            category="algorithm",
            title="Sliding Window Technique: Fixed vs Dynamic Windows",
            summary="Convert quadratic substring and contiguous subarray queries into linear O(N) time using expanding and contracting window boundaries.",
            fundamental_explanation="""The Sliding Window technique is designed for contiguous sub-array or sub-string problems.

Two Primary Types:
1. **Fixed Window**:
   - The window size `K` is constant.
   - You compute the initial window metric for the first `K` elements.
   - As you slide right: add the incoming element `arr[i]`, subtract the outgoing element `arr[i - K]`.
   - Time complexity: **$O(N)$** instead of re-summing $K$ elements $N$ times ($O(N \\times K)$).
2. **Dynamic (Variable-Size) Window**:
   - Expand the right boundary (`right++`) to incorporate new elements and satisfy problem criteria.
   - When a constraint is violated (e.g. duplicate character, sum exceeds limit), contract the left boundary (`left++`) until the window becomes valid again.
   - Update best result (max length, min length) during valid states.
   - Although nested in appearance (`while right: while invalid: left++`), each element enters and leaves the window at most once, yielding strictly **$O(N)$ amortized time**!""",
            step_by_step="""1. Initialize `left = 0`, state tracker (hash map or frequency array), and `max_len = 0`.
2. Iterate `right` from 0 to length - 1:
3. Incorporate `s[right]` into state tracker.
4. While window invariant is violated:
   Remove `s[left]` from state tracker and increment `left += 1`.
5. Update optimal answer: `max_len = max(max_len, right - left + 1)`.
6. Return `max_len` after full scan.""",
            real_world_applications="Network bandwidth sliding rate limiters, audio stream buffer monitoring, genomic DNA subsequence analysis, and text token windowing in NLP.",
            examples_illustrations="""# Longest Substring Without Repeating Characters in Python:
def length_of_longest_substring(s: str) -> int:
    char_map = {}
    left = 0
    max_len = 0
    for right, c in enumerate(s):
        if c in char_map and char_map[c] >= left:
            left = char_map[c] + 1 # Jump left past duplicate
        char_map[c] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
            pseudocode="""function dynamicWindow(s):
    left = 0
    window = {}
    best = 0
    for right from 0 to length(s) - 1:
        add_to_window(s[right])
        while is_invalid(window):
            remove_from_window(s[left])
            left = left + 1
        best = max(best, right - left + 1)
    return best""",
            time_complexity="O(N) Each character enters and leaves the window at most once",
            space_complexity="O(min(N, M)) where M is character set size",
            prerequisites="Arrays, Hash Map, Two Pointers",
            related_concepts="Monotonic Deque, Prefix Sum, Two Pointers",
            video_url="https://www.youtube.com/embed/MK-NZ4hN7Rs",
            video_title="Sliding Window Algorithm In 4 Minutes",
            visualization_type="searching",
            visualization_algorithm="binary_search",
            practice_problem_slug="count-vowels-in-a-string",
            order_index=31
        ),
        Lesson(
            id="lesson_dsa_heaps",
            topic_id="dsa_trees_bst",
            category="dsa",
            title="Heaps & Priority Queues: Complete Binary Tree Array Representation",
            summary="Discover how binary heaps maintain min/max root invariants in O(log N) using zero-pointer contiguous array mathematics.",
            fundamental_explanation="""A **Binary Heap** is a complete binary tree that satisfies the **Heap Invariant**:
- **Min-Heap**: The value of each node is $\\ge$ the value of its parent (`root` is the minimum element).
- **Max-Heap**: The value of each node is $\\le$ the value of its parent (`root` is the maximum element).

Array Representation without Pointers:
Because a heap is a complete binary tree (all levels filled except possibly the last, which is filled from left to right), it is mapped directly into an array with zero pointer overhead:
- For any node at index `i`:
  - `parent(i) = (i - 1) // 2`
  - `left_child(i) = 2 * i + 1`
  - `right_child(i) = 2 * i + 2`

Core Operations:
1. **`insert(x)`**: Append element to array end, then bubble up (`siftUp`) by swapping with parent until heap invariant holds: **$O(\\log N)$**.
2. **`extract_min()`**: Swap root with last element, pop last element, then bubble down root (`siftDown`) by swapping with smaller child: **$O(\\log N)$**.
3. **`peek()`**: Return `arr[0]` in **$O(1)$**.
4. **`build_heap` (`heapify`)**: Running `siftDown` from bottom non-leaf nodes upward creates a heap in **$O(N)$ linear time**!""",
            step_by_step="""1. Array Mapping: Root at index 0. Left child at 2*i + 1, Right at 2*i + 2.
2. Insertion: Add element to array end. While element < parent: swap with parent.
3. Extraction: Replace root with last element. While element > smallest child: swap with smallest child.
4. Top-K Problem: Maintain a Min-Heap of size K. When size > K, extract-min. Remaining K elements are the K largest!""",
            real_world_applications="Dijkstra's shortest path algorithm, OS process task schedulers, Median tracking from streaming data, Huffman coding compression, and database external sort-merge.",
            examples_illustrations="""import heapq

# Python heapq is a MIN-HEAP by default:
nums = [5, 7, 9, 1, 3]
heapq.heapify(nums) # In-place O(N) heapify
smallest = heapq.heappop(nums) # Returns 1 in O(log N)

# Max-heap trick in Python: negate numbers
max_heap = [-x for x in [5, 7, 9, 1, 3]]
heapq.heapify(max_heap)
largest = -heapq.heappop(max_heap) # Returns 9!""",
            pseudocode="""function siftDown(arr, i, n):
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    if smallest != i:
        swap(arr[i], arr[smallest])
        siftDown(arr, smallest, n)""",
            time_complexity="Insert/Extract: O(log N), Peek: O(1), Heapify: O(N)",
            space_complexity="O(N) Contiguous Array Buffer",
            prerequisites="Binary Trees, Array Indexing",
            related_concepts="PriorityQueue, Heapsort, Dijkstra, Top-K Elements",
            video_url="https://www.youtube.com/embed/t0Cq6tVNRBA",
            video_title="Binary Heaps & Priority Queues Visualized & Implemented",
            visualization_type="dijkstra",
            visualization_algorithm="dijkstra",
            order_index=32
        )
    ]

    for lesson in all_lessons:
        existing = db.query(Lesson).filter(Lesson.id == lesson.id).first()
        if not existing:
            db.add(lesson)
        else:
            # Update fields
            existing.category = lesson.category
            existing.title = lesson.title
            existing.summary = lesson.summary
            existing.fundamental_explanation = lesson.fundamental_explanation
            existing.step_by_step = lesson.step_by_step
            existing.real_world_applications = lesson.real_world_applications
            existing.examples_illustrations = lesson.examples_illustrations
            existing.pseudocode = lesson.pseudocode
            existing.time_complexity = lesson.time_complexity
            existing.space_complexity = lesson.space_complexity
            existing.video_url = lesson.video_url
            existing.video_title = lesson.video_title

    db.commit()
    print("[AlgoMentor] Successfully seeded all Python base, Java base, and DSA lessons.")

if __name__ == "__main__":
    from app.database import SessionLocal
    db = SessionLocal()
    seed_language_and_dsa_lessons(db)
    db.close()
