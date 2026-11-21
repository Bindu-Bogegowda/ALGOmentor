import json
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.roadmap import RoadmapStream, RoadmapTopic, UserTopicProgress
from app.models.lesson import Lesson, UserLessonProgress
from app.models.problem import Problem
from app.models.submission import Submission, UserProblemStatus, HintUsage
from app.models.project import Project, ProjectFile
from app.models.activity import ActivityLog, UserStreak
from app.models.review import DailyPerformanceReview
from app.services.auth_service import hash_password

def seed_database(db: Session):
    # Check if already seeded
    if db.query(RoadmapStream).first():
        return

    print("[AlgoMentor] Seeding database with rich multi-disciplinary curriculum...")

    # 1. Create Demo User
    demo_user = User(
        email="demo@algomentor.dev",
        username="algolearner",
        hashed_password=hash_password("algomentor123"),
        full_name="Alex Mercer",
        avatar="https://api.dicebear.com/7.x/bottts/svg?seed=algolearner",
        bio="CS undergraduate passionate about Graph Theory, Dynamic Programming and AI models.",
        preferred_language="python",
        difficulty_level="Intermediate",
        active_roadmap="dsa",
        theme="dark"
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    # 2. Roadmap Streams (7 Streams)
    streams = [
        RoadmapStream(
            id="dsa",
            title="Data Structures & Algorithms (DSA)",
            description="Foundations of computation, linear and non-linear data structures, searching, sorting, and algorithmic paradigms.",
            category="core",
            icon="Layers",
            order_index=1,
            total_hours_estimate=80,
            prerequisites="Basic programming syntax"
        ),
        RoadmapStream(
            id="aiml",
            title="Artificial Intelligence & Machine Learning",
            description="Heuristic search, decision trees, regression, classification, clustering, reinforcement learning and game theory.",
            category="ai",
            icon="Brain",
            order_index=2,
            total_hours_estimate=75,
            prerequisites="Linear algebra, Python fundamentals"
        ),
        RoadmapStream(
            id="dl",
            title="Deep Learning & Neural Networks",
            description="Perceptrons, backpropagation, CNNs, RNNs/LSTMs, Transformers, Attention mechanisms, and Generative AI.",
            category="ai",
            icon="Cpu",
            order_index=3,
            total_hours_estimate=90,
            prerequisites="Multivariable calculus, ML basics"
        ),
        RoadmapStream(
            id="daa",
            title="Design & Analysis of Algorithms (DAA)",
            description="Asymptotic analysis, Divide & Conquer, Greedy approaches, Dynamic Programming, Amortized Analysis, and NP-Completeness.",
            category="theoretical",
            icon="Code2",
            order_index=4,
            total_hours_estimate=65,
            prerequisites="Discrete mathematics, DSA"
        ),
        RoadmapStream(
            id="graph",
            title="Graph Algorithms & Network Theory",
            description="Topological sorting, BFS/DFS, Shortest paths (Dijkstra, Bellman-Ford, Floyd-Warshall), MST (Prim, Kruskal), and Max Flow.",
            category="specialized",
            icon="GitFork",
            order_index=5,
            total_hours_estimate=55,
            prerequisites="Data Structures"
        ),
        RoadmapStream(
            id="optimization",
            title="Optimization Algorithms",
            description="Linear programming, Simplex, Gradient Descent, Genetic Algorithms, Simulated Annealing, and Convex Optimization.",
            category="applied",
            icon="Sliders",
            order_index=6,
            total_hours_estimate=60,
            prerequisites="Calculus, Matrix Operations"
        ),
        RoadmapStream(
            id="computational",
            title="Computational & Domain-Specific Algorithms",
            description="Computational geometry, Cryptographic algorithms (RSA, ECC), String algorithms (KMP, Rabin-Karp), and Bioinformatics.",
            category="applied",
            icon="Terminal",
            order_index=7,
            total_hours_estimate=70,
            prerequisites="Advanced algorithms, Number theory"
        )
    ]
    for s in streams:
        db.add(s)
    db.commit()

    # 3. Topics for DSA Stream (Beginner, Intermediate, Advanced, Master)
    topics = [
        # DSA Beginner
        RoadmapTopic(
            id="dsa_arrays_101",
            stream_id="dsa",
            title="Arrays & Dynamic Arrays",
            level="Beginner",
            description="Memory layout, index access, amortized insertion, and contiguous storage mechanisms.",
            estimated_minutes=90,
            order_index=1,
            milestone_tag="Foundations"
        ),
        RoadmapTopic(
            id="dsa_sorting_101",
            stream_id="dsa",
            title="Sorting Foundations (Bubble, Selection, Insertion)",
            level="Beginner",
            description="Comparison sorts, invariants, swap mechanics, and quadratic time complexities.",
            estimated_minutes=120,
            order_index=2,
            prerequisite_topic_id="dsa_arrays_101",
            milestone_tag="Sorting Master"
        ),
        RoadmapTopic(
            id="dsa_searching_101",
            stream_id="dsa",
            title="Linear & Binary Search",
            level="Beginner",
            description="Exhaustive search vs divide-and-conquer on sorted spaces with logarithmic guarantees.",
            estimated_minutes=75,
            order_index=3,
            prerequisite_topic_id="dsa_arrays_101",
            milestone_tag="Search Mastery"
        ),
        # DSA Intermediate
        RoadmapTopic(
            id="dsa_linked_lists",
            stream_id="dsa",
            title="Singly & Doubly Linked Lists",
            level="Intermediate",
            description="Pointer manipulation, node structures, sentinel heads, and cycle detection.",
            estimated_minutes=110,
            order_index=4,
            prerequisite_topic_id="dsa_arrays_101",
            milestone_tag="Pointers"
        ),
        RoadmapTopic(
            id="dsa_stacks_queues",
            stream_id="dsa",
            title="Stacks, Queues & Monotonic Sequences",
            level="Intermediate",
            description="LIFO and FIFO data buffers, call stack simulation, and sliding window maximums.",
            estimated_minutes=100,
            order_index=5,
            prerequisite_topic_id="dsa_linked_lists",
            milestone_tag="Buffers"
        ),
        RoadmapTopic(
            id="dsa_trees_bst",
            stream_id="dsa",
            title="Binary Trees & Binary Search Trees (BST)",
            level="Intermediate",
            description="Hierarchical nodes, recursive traversals (In-order, Pre-order, Post-order), and BST invariant search.",
            estimated_minutes=150,
            order_index=6,
            prerequisite_topic_id="dsa_linked_lists",
            milestone_tag="Hierarchies"
        ),
        # DSA Advanced
        RoadmapTopic(
            id="dsa_graph_traversal",
            stream_id="dsa",
            title="Graph Traversal (BFS & DFS)",
            level="Advanced",
            description="Adjacency lists, visited sets, level-order exploration and recursive path depth.",
            estimated_minutes=180,
            order_index=7,
            prerequisite_topic_id="dsa_trees_bst",
            milestone_tag="Graph Pro"
        ),
        RoadmapTopic(
            id="dsa_shortest_paths",
            stream_id="dsa",
            title="Dijkstra's & Minimum Spanning Trees",
            level="Advanced",
            description="Greedy priority relaxation, edge relaxation, and optimal routing networks.",
            estimated_minutes=200,
            order_index=8,
            prerequisite_topic_id="dsa_graph_traversal",
            milestone_tag="Networks"
        ),
        # DSA Master
        RoadmapTopic(
            id="dsa_dynamic_programming",
            stream_id="dsa",
            title="Dynamic Programming & Memoization",
            level="Master",
            description="Overlapping subproblems, state transitions, bottom-up 1D/2D tables, and knapsack variations.",
            estimated_minutes=240,
            order_index=9,
            prerequisite_topic_id="dsa_shortest_paths",
            milestone_tag="Grandmaster"
        )
    ]
    for t in topics:
        db.add(t)
    db.commit()

    # 4. Detailed Concept Lessons
    lessons = [
        Lesson(
            id="lesson_bubble_sort",
            topic_id="dsa_sorting_101",
            title="Bubble Sort: Step-by-Step Mechanism & Invariants",
            summary="Learn how adjacent comparisons bubble the largest elements to their sorted indices.",
            fundamental_explanation="Bubble Sort is a straightforward comparison-based sorting algorithm. It iterates through an array repeatedly, comparing adjacent elements and swapping them if they are in the wrong order. Through successive passes, larger elements 'bubble' towards the end of the array, establishing sorted suffix sub-arrays.",
            step_by_step="""1. Start at the beginning of the array with index `0`.
2. Compare the current element `arr[j]` with the adjacent element `arr[j + 1]`.
3. If `arr[j] > arr[j + 1]`, swap them.
4. Advance `j` to the right until the end of the unsorted segment.
5. After pass `i`, the `i`-th largest element is securely positioned at `arr[n - i - 1]`.
6. Repeat until an entire pass completes without a single swap.""",
            real_world_applications="Computer graphics raster sorting, polygon rendering with almost-sorted vertices, educational diagnostics for algorithm runtime bounds.",
            examples_illustrations="Array `[5, 1, 4, 2, 8]`:\nPass 1: `[1, 5, 4, 2, 8]` -> `[1, 4, 5, 2, 8]` -> `[1, 4, 2, 5, 8]` (8 is locked into place).",
            pseudocode="""function bubbleSort(A):
    n = length(A)
    for i from 0 to n - 1:
        swapped = false
        for j from 0 to n - i - 2:
            if A[j] > A[j + 1]:
                swap(A[j], A[j + 1])
                swapped = true
        if not swapped:
            break
    return A""",
            time_complexity="O(N²) Worst/Average, O(N) Best (Optimized)",
            space_complexity="O(1) Auxiliary (In-place)",
            prerequisites="Array indexing and swapping",
            related_concepts="Selection Sort, Insertion Sort, Quick Sort",
            video_url="https://www.youtube.com/embed/kPRA0W1kECg",
            video_title="Bubble Sort Visualized with Sound and Analysis",
            visualization_type="sorting",
            visualization_algorithm="bubble_sort",
            practice_problem_slug="sort-an-array",
            order_index=1
        ),
        Lesson(
            id="lesson_binary_search",
            topic_id="dsa_searching_101",
            title="Binary Search: Logarithmic Space Pruning",
            summary="Divide and conquer a sorted sequence by eliminating half the candidate space each step.",
            fundamental_explanation="Binary search is one of the most fundamental search algorithms in computer science. Given a sorted collection, it repeatedly compares the target value to the middle element. Because the elements are ordered, if the target is smaller than the middle element, it must reside in the left half; if larger, in the right half. This halves the search interval on every step.",
            step_by_step="""1. Initialize `low = 0` and `high = len(arr) - 1`.
2. Compute `mid = low + (high - low) // 2` to prevent integer overflow.
3. If `arr[mid] == target`, target is discovered; return `mid`.
4. If `arr[mid] < target`, discard the left half by setting `low = mid + 1`.
5. If `arr[mid] > target`, discard the right half by setting `high = mid - 1`.
6. Terminate when `low > high`, returning -1 if element is absent.""",
            real_world_applications="Database B-tree indexing, Git bisect bug hunting, dictionary lookups, memory page lookup tables.",
            examples_illustrations="Array `[2, 5, 8, 12, 16, 23, 38, 56, 72, 91]`, Target `23`:\nStep 1: mid = 16 (< 23), low becomes 5.\nStep 2: mid = 38 (> 23), high becomes 5.\nStep 3: mid = 23 (== 23), MATCH FOUND at index 5!",
            pseudocode="""function binarySearch(arr, target):
    low = 0
    high = length(arr) - 1
    while low <= high:
        mid = low + floor((high - low) / 2)
        if arr[mid] == target:
            return mid
        else if arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1""",
            time_complexity="O(log N)",
            space_complexity="O(1) Iterative, O(log N) Recursive",
            prerequisites="Sorted arrays, Integer division",
            related_concepts="Two Pointers, Ternary Search, B-Trees",
            video_url="https://www.youtube.com/embed/P3YID7liBug",
            video_title="Binary Search in 100 Seconds",
            visualization_type="searching",
            visualization_algorithm="binary_search",
            practice_problem_slug="binary-search",
            order_index=2
        ),
        Lesson(
            id="lesson_bfs_dfs",
            topic_id="dsa_graph_traversal",
            title="Graph Traversal: Breadth-First & Depth-First Search",
            summary="Explore interconnected networks using queue-driven level expansion or stack-driven deep diving.",
            fundamental_explanation="Graphs represent entities (vertices) and relationships (edges). Traversing a graph means visiting every reachable vertex without being trapped in cycles. BFS uses a Queue to explore radially outward in concentric waves, whereas DFS uses a Stack (or function call stack) to venture as far down each branch as possible before backtracking.",
            step_by_step="""BFS Algorithm:
1. Enqueue starting node and mark it as visited.
2. While queue is not empty, dequeue `curr`.
3. For each unvisited neighbor of `curr`, mark as visited and enqueue.

DFS Algorithm:
1. Mark starting node as visited.
2. For each unvisited neighbor, recursively call DFS.
3. Backtrack when all adjacent paths are explored.""",
            real_world_applications="Social network friend recommendations (Degrees of separation), web crawlers, GPS route navigation, cycle detection in compilers.",
            examples_illustrations="A connected graph with vertices A -> (B, C), B -> (D, E):\nBFS: Visits A, then B, C, then D, E.\nDFS: Visits A, then B, then D, then backtrack to E, then C.",
            pseudocode="""function BFS(graph, start):
    queue = [start]
    visited = {start}
    while queue is not empty:
        node = queue.pop(0)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)""",
            time_complexity="O(V + E) where V=vertices, E=edges",
            space_complexity="O(V) for visited set & queue/stack",
            prerequisites="Queue, Stack, Adjacency List",
            related_concepts="Dijkstra's Algorithm, Topological Sort, Connected Components",
            video_url="https://www.youtube.com/embed/pcKY4hjDrxk",
            video_title="Graph Traversal Algorithms Explained",
            visualization_type="graph",
            visualization_algorithm="bfs",
            practice_problem_slug="number-of-islands",
            order_index=3
        ),
        Lesson(
            id="lesson_dijkstra",
            topic_id="dsa_shortest_paths",
            title="Dijkstra's Algorithm: Shortest Paths in Weighted Graphs",
            summary="Greedy single-source shortest path discovery in graphs with non-negative edge weights.",
            fundamental_explanation="Dijkstra's algorithm finds the shortest path between nodes in a graph. It maintains a set of tentative distances from the source to all nodes, initially infinity for all except the source (0). At each step, it selects the unvisited node with the smallest tentative distance, explores its edges, and updates neighbor distances if a shorter path is discovered (edge relaxation).",
            step_by_step="""1. Assign distance `dist[source] = 0` and `dist[v] = infinity` for all other vertices.
2. Insert `(0, source)` into a Min-Heap / Priority Queue.
3. While the priority queue is not empty, pop `(d, u)` with lowest distance.
4. If `d > dist[u]`, skip (already relaxed).
5. For each neighbor `v` of `u` with edge weight `w`:
   If `dist[u] + w < dist[v]`:
     `dist[v] = dist[u] + w`
     Insert `(dist[v], v)` into Priority Queue.
6. When done, `dist` holds shortest paths from source to all nodes.""",
            real_world_applications="Google Maps / Apple Maps vehicle navigation, OSPF (Open Shortest Path First) internet packet routing, airline flight layover planning.",
            examples_illustrations="Nodes A -> B (weight 4), A -> C (weight 2), C -> B (weight 1).\nDirect A -> B is 4. Path A -> C -> B is 2 + 1 = 3! Dijkstra's greedy priority selects A -> C -> B.",
            pseudocode="""function Dijkstra(graph, source):
    dist = {v: infinity for v in graph}
    dist[source] = 0
    pq = PriorityQueue()
    pq.push(0, source)
    
    while not pq.empty():
        d, u = pq.pop()
        if d > dist[u]: continue
        for v, weight in graph[u]:
            if dist[u] + weight < dist[v]:
                dist[v] = dist[u] + weight
                pq.push(dist[v], v)
    return dist""",
            time_complexity="O((V + E) log V) with Min-Heap",
            space_complexity="O(V) for distances and heap",
            prerequisites="Priority Queue, BFS, Weighted Graphs",
            related_concepts="Bellman-Ford, A* Search, Prim's MST",
            video_url="https://www.youtube.com/embed/GazC3A4OQTE",
            video_title="Dijkstra's Algorithm in 4 Minutes",
            visualization_type="dijkstra",
            visualization_algorithm="dijkstra",
            practice_problem_slug="network-delay-time",
            order_index=4
        )
    ]
    for l in lessons:
        db.add(l)
    db.commit()

    # 5. Practice Problems (Searchable Practice Bank)
    problems = [
        Problem(
            slug="count-vowels-in-a-string",
            title="Count Vowels in a String",
            topic="Strings",
            subtopic="Traversal & Frequency",
            algorithmic_pattern="Linear Scan",
            difficulty="Easy",
            description="""Given a string `s`, count the total number of vowels that appear in the string.
The vowels are `'a'`, `'e'`, `'i'`, `'o'`, and `'u'` (both lowercase and uppercase).
Ignore spaces, digits, and punctuation characters.""",
            constraints="""• 0 <= length of s <= 10^5
• String may contain alphanumeric characters, spaces and special characters.""",
            input_format="A single line containing string `s`.",
            output_format="A single integer representing the count of vowels.",
            examples_json=json.dumps([
                {"input": "hello world", "output": "3", "explanation": "'e', 'o', 'o' are the 3 vowels."},
                {"input": "AlgoMentor AI Platform", "output": "8", "explanation": "A, o, e, o, A, I, a, o"}
            ]),
            sample_test_cases=json.dumps([
                {"input": "hello world", "expected_output": "3"},
                {"input": "python programming", "expected_output": "4"}
            ]),
            hidden_test_cases=json.dumps([
                {"input": "AEIOUaeiou", "expected_output": "10"},
                {"input": "bcdfghjklmnpqrstvwxyz", "expected_output": "0"},
                {"input": "", "expected_output": "0"}
            ]),
            starter_code_python="""def count_vowels(s: str) -> int:
    # Return the total number of vowels in string s
    vowels = set("aeiouAEIOU")
    count = 0
    for char in s:
        if char in vowels:
            count += 1
    return count

if __name__ == '__main__':
    import sys
    inp = sys.stdin.read().strip()
    print(count_vowels(inp))""",
            starter_code_java="""import java.util.Scanner;

public class Solution {
    public static int countVowels(String s) {
        int count = 0;
        String vowels = "aeiouAEIOU";
        for (int i = 0; i < s.length(); i++) {
            if (vowels.indexOf(s.charAt(i)) != -1) {
                count++;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine() : "";
        System.out.println(countVowels(s));
    }
}""",
            hint_level_1="Concept: Use a Set or string lookup to check membership of each character against vowels.",
            hint_level_2="Direction: Traverse string `s` character by character. If `char.lower()` is in {'a', 'e', 'i', 'o', 'u'}, increment a tally.",
            hint_level_3="Pseudocode: count = 0; for char in s: if char in vowels: count += 1; return count",
            expected_time_complexity="O(N)",
            expected_space_complexity="O(1)"
        ),
        Problem(
            slug="two-sum",
            title="Two Sum",
            topic="Arrays",
            subtopic="Hashing",
            algorithmic_pattern="Hash Map Lookup",
            difficulty="Easy",
            description="""Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.
You may assume that each input has exactly one solution, and you may not use the same element twice.
Input format: First line has space-separated integers for `nums`. Second line has integer `target`.""",
            constraints="""• 2 <= nums.length <= 10^4
• -10^9 <= nums[i] <= 10^9
• -10^9 <= target <= 10^9
• Exactly one valid answer exists.""",
            input_format="First line: space-separated integers. Second line: target integer.",
            output_format="Indices formatted as space-separated numbers (e.g. 0 1).",
            examples_json=json.dumps([
                {"input": "2 7 11 15\n9", "output": "0 1", "explanation": "nums[0] + nums[1] == 9"}
            ]),
            sample_test_cases=json.dumps([
                {"input": "2 7 11 15\n9", "expected_output": "0 1"},
                {"input": "3 2 4\n6", "expected_output": "1 2"}
            ]),
            hidden_test_cases=json.dumps([
                {"input": "3 3\n6", "expected_output": "0 1"},
                {"input": "-1 -2 -3 -4 -5\n-8", "expected_output": "2 4"}
            ]),
            starter_code_python="""def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return f"{seen[complement]} {i}"
        seen[num] = i
    return ""

if __name__ == '__main__':
    import sys
    lines = sys.stdin.read().strip().splitlines()
    if len(lines) >= 2:
        nums = list(map(int, lines[0].split()))
        target = int(lines[1])
        print(two_sum(nums, target))""",
            starter_code_java="""import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLine()) return;
        String[] parts = sc.nextLine().trim().split("\\\\s+");
        int target = sc.nextInt();
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < parts.length; i++) {
            int val = Integer.parseInt(parts[i]);
            int comp = target - val;
            if (map.containsKey(comp)) {
                System.out.println(map.get(comp) + " " + i);
                return;
            }
            map.put(val, i);
        }
    }
}""",
            hint_level_1="Concept: Rather than checking every pair with nested loops in O(N^2), trade space for time using a Hash Map.",
            hint_level_2="Direction: As you iterate through the list at index `i`, check if `target - num` already exists in your hash map.",
            hint_level_3="Pseudocode: map = {}; for i, x in enumerate(nums): if target - x in map: return [map[target - x], i]; map[x] = i",
            expected_time_complexity="O(N)",
            expected_space_complexity="O(N)"
        ),
        Problem(
            slug="binary-search",
            title="Binary Search in Sorted Array",
            topic="Searching",
            subtopic="Divide and Conquer",
            algorithmic_pattern="Binary Search",
            difficulty="Easy",
            description="""Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`.
If `target` exists, then return its index. Otherwise, return `-1`.""",
            constraints="""• 1 <= nums.length <= 10^4
• -10^4 < nums[i], target < 10^4
• All integers in nums are unique.""",
            input_format="Line 1: space-separated sorted integers. Line 2: target integer.",
            output_format="A single integer representing the 0-based index or -1.",
            examples_json=json.dumps([
                {"input": "-1 0 3 5 9 12\n9", "output": "4", "explanation": "9 exists in nums and its index is 4."}
            ]),
            sample_test_cases=json.dumps([
                {"input": "-1 0 3 5 9 12\n9", "expected_output": "4"},
                {"input": "-1 0 3 5 9 12\n2", "expected_output": "-1"}
            ]),
            hidden_test_cases=json.dumps([
                {"input": "5\n5", "expected_output": "0"},
                {"input": "1 3 5 7 9\n1", "expected_output": "0"},
                {"input": "1 3 5 7 9\n9", "expected_output": "4"}
            ]),
            starter_code_python="""def search(nums, target):
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

if __name__ == '__main__':
    import sys
    lines = sys.stdin.read().strip().splitlines()
    if len(lines) >= 2:
        nums = list(map(int, lines[0].split()))
        target = int(lines[1])
        print(search(nums, target))""",
            starter_code_java="""import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextLine()) return;
        String[] parts = sc.nextLine().trim().split("\\\\s+");
        int target = sc.nextInt();
        int[] nums = new int[parts.length];
        for (int i = 0; i < parts.length; i++) nums[i] = Integer.parseInt(parts[i]);
        int l = 0, r = nums.length - 1;
        while (l <= r) {
            int mid = l + (r - l) / 2;
            if (nums[mid] == target) {
                System.out.println(mid);
                return;
            } else if (nums[mid] < target) {
                l = mid + 1;
            } else {
                r = mid - 1;
            }
        }
        System.out.println(-1);
    }
}""",
            hint_level_1="Concept: The array is sorted. Use low and high pointers to check the middle element.",
            hint_level_2="Direction: If `nums[mid] < target`, the target must be in the right half, so set `low = mid + 1`.",
            hint_level_3="Pseudocode: while low <= high: mid = (low + high) // 2; if arr[mid] == target: return mid; adjust pointers",
            expected_time_complexity="O(log N)",
            expected_space_complexity="O(1)"
        ),
        Problem(
            slug="valid-parentheses",
            title="Valid Parentheses",
            topic="Stacks",
            subtopic="Parsing & Invariants",
            algorithmic_pattern="LIFO Stack Matching",
            difficulty="Medium",
            description="""Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.
Print `true` or `false`.""",
            constraints="""• 1 <= s.length <= 10^4
• s consists of parentheses only '()[]{}'.""",
            input_format="A single line with string `s`.",
            output_format="`true` or `false`",
            examples_json=json.dumps([
                {"input": "()[]{}", "output": "true", "explanation": "All brackets matched correctly."},
                {"input": "(]", "output": "false", "explanation": "Mismatched bracket types."}
            ]),
            sample_test_cases=json.dumps([
                {"input": "()[]{}", "expected_output": "true"},
                {"input": "(]", "expected_output": "false"}
            ]),
            hidden_test_cases=json.dumps([
                {"input": "([{}])", "expected_output": "true"},
                {"input": "((({{{[[[", "expected_output": "false"},
                {"input": "]", "expected_output": "false"}
            ]),
            starter_code_python="""def is_valid(s: str) -> bool:
    stack = []
    mapping = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in mapping:
            top_elem = stack.pop() if stack else '#'
            if mapping[char] != top_elem:
                return False
        else:
            stack.append(char)
    return len(stack) == 0

if __name__ == '__main__':
    import sys
    inp = sys.stdin.read().strip()
    print("true" if is_valid(inp) else "false")""",
            starter_code_java="""import java.util.*;

public class Solution {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.hasNextLine() ? sc.nextLine().trim() : "";
        Stack<Character> stack = new Stack<>();
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else if (stack.isEmpty() || stack.pop() != c) {
                System.out.println("false");
                return;
            }
        }
        System.out.println(stack.isEmpty() ? "true" : "false");
    }
}""",
            hint_level_1="Concept: Use a Stack data structure to keep track of the most recently opened bracket.",
            hint_level_2="Direction: Push open brackets onto the stack. When encountering a closing bracket, check if it matches the top element of the stack.",
            hint_level_3="Pseudocode: stack = []; for char in s: if open: push; else: pop top and verify match; return stack is empty",
            expected_time_complexity="O(N)",
            expected_space_complexity="O(N)"
        )
    ]
    for p in problems:
        db.add(p)
    db.commit()

    # 6. Seed Realistic User Progress, Activity Logs & Heatmap Streaks for Demo User
    # User topic progress
    for t in topics:
        is_done = t.id in ["dsa_arrays_101", "dsa_sorting_101"]
        utp = UserTopicProgress(
            user_id=demo_user.id,
            topic_id=t.id,
            is_unlocked=True,
            is_completed=is_done,
            completed_at=datetime.utcnow() - timedelta(days=2) if is_done else None,
            progress_percentage=100.0 if is_done else (40.0 if t.id == "dsa_searching_101" else 0.0)
        )
        db.add(utp)

    # User lesson progress
    for l in lessons:
        is_done = l.id in ["lesson_bubble_sort", "lesson_binary_search"]
        ulp = UserLessonProgress(
            user_id=demo_user.id,
            lesson_id=l.id,
            is_completed=is_done,
            completed_at=datetime.utcnow() - timedelta(days=1) if is_done else None,
            time_spent_seconds=1800 if is_done else 300
        )
        db.add(ulp)

    # Problem statuses & submissions
    for prob in problems:
        status_val = "Solved" if prob.slug in ["count-vowels-in-a-string", "two-sum"] else "Unsolved"
        ups = UserProblemStatus(
            user_id=demo_user.id,
            problem_id=prob.id,
            status=status_val,
            is_bookmarked=(prob.slug == "two-sum"),
            highest_hint_level_used=1 if prob.slug == "two-sum" else 0,
            solved_at=datetime.utcnow() - timedelta(days=1) if status_val == "Solved" else None
        )
        db.add(ups)

        if status_val == "Solved":
            sub = Submission(
                user_id=demo_user.id,
                problem_id=prob.id,
                language="python",
                code=prob.starter_code_python,
                status="Accepted",
                runtime_ms=38.5,
                memory_mb=14.2,
                passed_tests=5,
                total_tests=5,
                stdout="All test cases passed."
            )
            db.add(sub)

    # Activity Logs over the past 30 days to power the LeetCode/GitHub-like calendar heatmap
    today = date.today()
    for i in range(28, -1, -1):
        act_date = today - timedelta(days=i)
        # Sprinkle active days (skip some to make realistic streaks)
        if i % 7 not in [3, 6]: # Active most days
            logs_count = (i % 3) + 1
            for k in range(logs_count):
                log = ActivityLog(
                    user_id=demo_user.id,
                    action_type="problem_solved" if k == 0 else "lesson_completed",
                    topic="DSA",
                    metadata_json=json.dumps({"detail": f"Activity on {act_date}"}),
                    active_seconds=900 * logs_count,
                    created_at=datetime.combine(act_date, datetime.min.time()) + timedelta(hours=14 + k)
                )
                db.add(log)

    # User streak record
    user_streak = UserStreak(
        user_id=demo_user.id,
        current_streak=5,
        longest_streak=14,
        last_activity_date=today,
        total_active_days=22
    )
    db.add(user_streak)

    # Seed an authentic Daily Performance Review
    daily_review = DailyPerformanceReview(
        user_id=demo_user.id,
        review_date=today,
        overall_summary="Exceptional algorithmic progression today! You mastered Bubble Sort invariants and solved Two Sum with an optimal O(N) hash map approach, eliminating quadratic nested loops.",
        strengths_json=json.dumps([
            "Strong grasp of Hash Map complementary lookups to reduce O(N²) to O(N).",
            "Consistent daily streak maintained (5 days active).",
            "High test case accuracy: 100% test pass rate on accepted solutions."
        ]),
        common_mistakes_json=json.dumps([
            "Occasional index boundary off-by-one errors when iterating up to array length in while loops.",
            "Initial omission of case-insensitivity checks in string vowel filtering."
        ]),
        concepts_to_improve_json=json.dumps([
            "Two-pointer edge condition handling for palindromic expansions.",
            "Understanding recursion stack depth limitations in tree traversals."
        ]),
        recommended_revisions_json=json.dumps([
            "Review Binary Search boundary invariants (low <= high vs low < high).",
            "Practice Sliding Window Maximum using monotonic deque."
        ]),
        next_day_plan_json=json.dumps([
            "Target 1 Medium problem on Graph BFS traversal.",
            "Complete the interactive Dijkstra visualization walkthrough.",
            "Dedicate 45 minutes to active problem solving."
        ]),
        achievable_targets_json=json.dumps([
            "Solve 'Valid Parentheses' using Stack matching.",
            "Achieve 6-day continuous activity streak.",
            "Unlock Intermediate Graph milestone in DSA roadmap."
        ]),
        metrics_json=json.dumps({
            "problems_attempted": 2,
            "problems_solved": 2,
            "accuracy": 100.0,
            "active_minutes": 55,
            "streak": 5
        })
    )
    db.add(daily_review)

    # Seed a sample AI project
    sample_proj = Project(
        user_id=demo_user.id,
        title="Interactive Dijkstra & BFS Grid Visualizer",
        description="Browser-based grid visualizer demonstrating shortest-path discovery using Dijkstra and BFS with interactive obstacles.",
        project_type="web_interactive",
        prompt_idea="Create a pathfinding visualizer with walls and real-time step animations.",
        tags="graph,dijkstra,bfs,interactive"
    )
    db.add(sample_proj)
    db.commit()
    db.refresh(sample_proj)

    proj_file1 = ProjectFile(
        project_id=sample_proj.id,
        filename="index.html",
        filepath="index.html",
        content="""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>AlgoMentor Pathfinding Visualizer</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div class="header">
    <h2>⚡ AlgoMentor Pathfinding Visualizer</h2>
    <p>Click and drag to place walls, then click Run BFS!</p>
    <button onclick="run()">Run BFS</button>
    <button onclick="reset()">Reset</button>
  </div>
  <div id="grid"></div>
  <script src="script.js"></script>
</body>
</html>""",
        language="html"
    )
    proj_file2 = ProjectFile(
        project_id=sample_proj.id,
        filename="style.css",
        filepath="style.css",
        content="""body { background: #0b0f19; color: #fff; font-family: system-ui; text-align: center; margin: 0; padding: 1.5rem; }
.header { margin-bottom: 1rem; }
button { padding: 8px 16px; margin: 4px; background: #0284c7; border: none; color: #fff; border-radius: 6px; cursor: pointer; font-weight: 600; }
#grid { display: grid; grid-template-columns: repeat(15, 26px); grid-gap: 2px; justify-content: center; margin-top: 1rem; }
.cell { width: 26px; height: 26px; background: #1e293b; border-radius: 3px; cursor: pointer; }
.cell.start { background: #22c55e; }
.cell.target { background: #ef4444; }
.cell.wall { background: #64748b; }
.cell.visited { background: #38bdf8; }
.cell.path { background: #eab308; }""",
        language="css"
    )
    proj_file3 = ProjectFile(
        project_id=sample_proj.id,
        filename="script.js",
        filepath="script.js",
        content="""const R = 12, C = 15;
const gridEl = document.getElementById('grid');
let grid = [];
for (let r = 0; r < R; r++) {
  grid[r] = [];
  for (let c = 0; c < C; c++) {
    const el = document.createElement('div');
    el.className = 'cell';
    if (r === 6 && c === 2) el.classList.add('start');
    if (r === 6 && c === 12) el.classList.add('target');
    el.onclick = () => { if (el.className === 'cell') el.classList.add('wall'); };
    gridEl.appendChild(el);
    grid[r][c] = { r, c, el, visited: false, parent: null };
  }
}
async function run() {
  const queue = [{ r: 6, c: 2 }];
  grid[6][2].visited = true;
  while (queue.length) {
    const curr = queue.shift();
    if (curr.r === 6 && curr.c === 12) break;
    if (!(curr.r === 6 && curr.c === 2)) {
      curr.el.classList.add('visited');
      await new Promise(r => setTimeout(r, 20));
    }
    for (const [dr, dc] of [[0,1],[1,0],[0,-1],[-1,0]]) {
      const nr = curr.r + dr, nc = curr.c + dc;
      if (nr>=0 && nr<R && nc>=0 && nc<C && !grid[nr][nc].visited && !grid[nr][nc].el.classList.contains('wall')) {
        grid[nr][nc].visited = true;
        grid[nr][nc].parent = curr;
        queue.push(grid[nr][nc]);
      }
    }
  }
  let curr = grid[6][12].parent;
  while (curr && !(curr.r===6 && curr.c===2)) {
    curr.el.classList.add('path');
    curr = curr.parent;
  }
}
function reset() { location.reload(); }""",
        language="javascript"
    )
    db.add(proj_file1)
    db.add(proj_file2)
    db.add(proj_file3)
    db.commit()
    print("[AlgoMentor] Database successfully seeded.")
