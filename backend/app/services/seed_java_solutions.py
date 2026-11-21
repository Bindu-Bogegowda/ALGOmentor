"""
Script to populate complete, compilable, idiomatic Java implementations
for all lessons in the AlgoMentor platform.
"""

from app.database import SessionLocal
from app.models.lesson import Lesson

JAVA_UPDATES = {
    "lesson_java_memory": """// Java Memory Architecture: Stack vs Heap & References
public class JavaMemoryModel {
    // Custom reference node placed on Heap
    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public static void main(String[] args) {
        // Primitive variable 'x' stored directly in Thread Stack frame
        int x = 42;

        // Reference variable 'head' stored in Stack; points to ListNode object on Heap
        ListNode head = new ListNode(10);
        head.next = new ListNode(20);

        modifyPrimitive(x);
        System.out.println("x after modifyPrimitive: " + x); // Remains 42 (pass-by-value)

        modifyReference(head);
        System.out.println("head.val after modifyReference: " + head.val); // Changed to 999
    }

    // Stack frame gets a copy of primitive bits
    private static void modifyPrimitive(int val) {
        val = 100;
    }

    // Stack frame gets a copy of the pointer reference, mutating the same Heap object
    private static void modifyReference(ListNode node) {
        if (node != null) {
            node.val = 999;
        }
    }
}""",

    "lesson_java_arrays": """// Java Arrays (Fixed) vs ArrayList (Dynamic Resizing)
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class JavaArrayOperations {
    public static void main(String[] args) {
        // 1. Primitive Array: Fixed capacity, contiguous memory block in RAM
        int[] fixedArray = new int[5];
        for (int i = 0; i < fixedArray.length; i++) {
            fixedArray[i] = (i + 1) * 10;
        }
        System.out.println("Fixed Array: " + Arrays.toString(fixedArray));

        // 2. Dynamic ArrayList: Backed by Object[] array, auto-doubles capacity when full
        List<Integer> dynamicList = new ArrayList<>();
        // Amortized O(1) append: triggers Arrays.copyOf when size exceeds capacity
        for (int i = 1; i <= 8; i++) {
            dynamicList.add(i * 100);
        }
        System.out.println("ArrayList: " + dynamicList);

        // 3. 2D Matrix Grid Representation in Java
        int[][] matrix = new int[3][3];
        matrix[0][0] = 1;
        matrix[1][1] = 5;
        matrix[2][2] = 9;
        System.out.println("Matrix [1][1]: " + matrix[1][1]);
    }
}""",

    "lesson_java_jcf": """// Java Collections Framework (JCF): Stack, Queue & Deque
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.LinkedList;
import java.util.Queue;

public class JavaCollectionsDemo {
    // Problem: Valid Parentheses using ArrayDeque (Recommended Stack in Java)
    public static boolean isValidParentheses(String s) {
        // ArrayDeque is faster than legacy java.util.Stack (no synchronization overhead)
        Deque<Character> stack = new ArrayDeque<>();
        
        for (char c : s.toCharArray()) {
            if (c == '(') stack.push(')');
            else if (c == '{') stack.push('}');
            else if (c == '[') stack.push(']');
            else {
                if (stack.isEmpty() || stack.pop() != c) {
                    return false;
                }
            }
        }
        return stack.isEmpty();
    }

    public static void main(String[] args) {
        // FIFO Queue demonstration using LinkedList
        Queue<Integer> bfsQueue = new LinkedList<>();
        bfsQueue.offer(10);
        bfsQueue.offer(20);
        System.out.println("Queue Poll: " + bfsQueue.poll()); // 10

        System.out.println("Valid '({[]})': " + isValidParentheses("({[]})"));
        System.out.println("Valid '([)]': " + isValidParentheses("([)]"));
    }
}""",

    "lesson_java_hashmap": """// Java HashMap & HashSet Internals: Buckets, Collisions & O(1) Lookups
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public class JavaHashMapInternals {
    // Solving Two Sum in O(N) Time and O(N) Space using Java HashMap
    public static int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> complementMap = new HashMap<>(); // key: value, value: index
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            if (complementMap.containsKey(complement)) {
                return new int[] { complementMap.get(complement), i };
            }
            // Put into hash bucket: index = (n - 1) & hash(key)
            complementMap.put(nums[i], i);
        }
        return new int[0];
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int[] result = twoSum(nums, 9);
        System.out.println("Indices: [" + result[0] + ", " + result[1] + "]");

        // HashSet for O(1) unique duplicate detection
        Set<Integer> visited = new HashSet<>();
        visited.add(42);
        System.out.println("Contains 42: " + visited.contains(42));
    }
}""",

    "lesson_java_generics_heaps": """// Java OOP, Generics & PriorityQueue (Min-Heap and Max-Heap)
import java.util.Collections;
import java.util.PriorityQueue;

public class JavaGenericsAndHeaps {
    // Generic TreeNode structure
    static class TreeNode<T> {
        T val;
        TreeNode<T> left, right;
        TreeNode(T val) { this.val = val; }
    }

    public static void main(String[] args) {
        // 1. Min-Heap: Smallest element at root peek()
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        minHeap.offer(40);
        minHeap.offer(10);
        minHeap.offer(25);
        System.out.println("Min-Heap poll: " + minHeap.poll()); // 10

        // 2. Max-Heap: Custom comparator using Collections.reverseOrder()
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        maxHeap.offer(40);
        maxHeap.offer(10);
        maxHeap.offer(25);
        System.out.println("Max-Heap poll: " + maxHeap.poll()); // 40

        // 3. Custom Object Heap with Lambda Comparator
        class Task {
            String name;
            int priority;
            Task(String name, int priority) { this.name = name; this.priority = priority; }
        }

        // Higher priority first
        PriorityQueue<Task> taskQueue = new PriorityQueue<>((a, b) -> Integer.compare(b.priority, a.priority));
        taskQueue.offer(new Task("Bugfix", 1));
        taskQueue.offer(new Task("Deploy", 5));
        System.out.println("Top Task: " + taskQueue.poll().name); // Deploy
    }
}""",

    "lesson_bfs_dfs": """// Graph Traversal in Java: Breadth-First Search (BFS) & Depth-First Search (DFS)
import java.util.*;

public class GraphTraversals {
    // Breadth-First Search: Uses Queue (FIFO) - Level by Level
    public static List<Integer> bfs(int start, List<List<Integer>> adj, int n) {
        List<Integer> order = new ArrayList<>();
        boolean[] visited = new boolean[n];
        Queue<Integer> queue = new LinkedList<>();

        visited[start] = true;
        queue.offer(start);

        while (!queue.isEmpty()) {
            int curr = queue.poll();
            order.add(curr);

            for (int neighbor : adj.get(curr)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
        return order;
    }

    // Depth-First Search: Recursive Exploration
    public static void dfs(int curr, List<List<Integer>> adj, boolean[] visited, List<Integer> order) {
        visited[curr] = true;
        order.add(curr);

        for (int neighbor : adj.get(curr)) {
            if (!visited[neighbor]) {
                dfs(neighbor, adj, visited, order);
            }
        }
    }

    public static void main(String[] args) {
        int n = 4;
        List<List<Integer>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());
        adj.get(0).addAll(Arrays.asList(1, 2));
        adj.get(1).addAll(Arrays.asList(0, 3));
        adj.get(2).addAll(Arrays.asList(0, 3));
        adj.get(3).addAll(Arrays.asList(1, 2));

        System.out.println("BFS Traversal: " + bfs(0, adj, n));

        List<Integer> dfsOrder = new ArrayList<>();
        dfs(0, adj, new boolean[n], dfsOrder);
        System.out.println("DFS Traversal: " + dfsOrder);
    }
}""",

    "lesson_dijkstra": """// Dijkstra's Shortest Path Algorithm in Java with PriorityQueue
import java.util.*;

public class DijkstraAlgorithm {
    static class Edge {
        int to, weight;
        Edge(int to, int weight) { this.to = to; this.weight = weight; }
    }

    static class Node implements Comparable<Node> {
        int id, dist;
        Node(int id, int dist) { this.id = id; this.dist = dist; }
        @Override
        public int compareTo(Node other) { return Integer.compare(this.dist, other.dist); }
    }

    public static int[] dijkstra(int start, List<List<Edge>> adj, int n) {
        int[] dist = new int[n];
        Arrays.fill(dist, Integer.MAX_VALUE);
        dist[start] = 0;

        PriorityQueue<Node> pq = new PriorityQueue<>();
        pq.offer(new Node(start, 0));

        while (!pq.isEmpty()) {
            Node curr = pq.poll();
            int u = curr.id;
            int d = curr.dist;

            if (d > dist[u]) continue; // Stale entry

            for (Edge edge : adj.get(u)) {
                int v = edge.to;
                int weight = edge.weight;

                if (dist[u] + weight < dist[v]) {
                    dist[v] = dist[u] + weight;
                    pq.offer(new Node(v, dist[v]));
                }
            }
        }
        return dist;
    }

    public static void main(String[] args) {
        int n = 5;
        List<List<Edge>> adj = new ArrayList<>();
        for (int i = 0; i < n; i++) adj.add(new ArrayList<>());

        adj.get(0).add(new Edge(1, 4));
        adj.get(0).add(new Edge(2, 1));
        adj.get(2).add(new Edge(1, 2));
        adj.get(1).add(new Edge(3, 1));
        adj.get(2).add(new Edge(3, 5));

        int[] shortest = dijkstra(0, adj, n);
        System.out.println("Shortest distances from node 0: " + Arrays.toString(shortest));
    }
}""",

    "lesson_py_lists": """// Java Equivalent: Dynamic Array Implementation (Custom ArrayList)
import java.util.Arrays;

public class CustomDynamicArray<T> {
    private Object[] data;
    private int size = 0;
    private int capacity = 4;

    public CustomDynamicArray() {
        data = new Object[capacity];
    }

    public void add(T element) {
        if (size == capacity) {
            resize(capacity * 2); // Amortized O(1) doubling
        }
        data[size++] = element;
    }

    @SuppressWarnings("unchecked")
    public T get(int index) {
        if (index < 0 || index >= size) throw new IndexOutOfBoundsException();
        return (T) data[index];
    }

    private void resize(int newCapacity) {
        data = Arrays.copyOf(data, newCapacity);
        capacity = newCapacity;
    }

    public int size() { return size; }

    public static void main(String[] args) {
        CustomDynamicArray<Integer> list = new CustomDynamicArray<>();
        for (int i = 1; i <= 10; i++) list.add(i * 10);
        System.out.println("Element at index 5: " + list.get(5));
        System.out.println("Total elements: " + list.size());
    }
}""",

    "lesson_py_dicts_sets": """// Java Equivalent: Hash Table Collision Resolution (Separate Chaining)
import java.util.LinkedList;

public class SimpleHashMap<K, V> {
    static class Entry<K, V> {
        K key;
        V value;
        Entry(K key, V value) { this.key = key; this.value = value; }
    }

    private int capacity = 16;
    private LinkedList<Entry<K, V>>[] buckets;

    @SuppressWarnings("unchecked")
    public SimpleHashMap() {
        buckets = new LinkedList[capacity];
        for (int i = 0; i < capacity; i++) buckets[i] = new LinkedList<>();
    }

    public void put(K key, V value) {
        int bucketIdx = Math.abs(key.hashCode()) % capacity;
        for (Entry<K, V> entry : buckets[bucketIdx]) {
            if (entry.key.equals(key)) {
                entry.value = value;
                return;
            }
        }
        buckets[bucketIdx].add(new Entry<>(key, value));
    }

    public V get(K key) {
        int bucketIdx = Math.abs(key.hashCode()) % capacity;
        for (Entry<K, V> entry : buckets[bucketIdx]) {
            if (entry.key.equals(key)) return entry.value;
        }
        return null;
    }

    public static void main(String[] args) {
        SimpleHashMap<String, Integer> map = new SimpleHashMap<>();
        map.put("Java", 1995);
        map.put("Python", 1991);
        System.out.println("Java release year: " + map.get("Java"));
    }
}""",

    "lesson_py_recursion": """// Java Recursion & Call Stack Management
public class JavaRecursion {
    // Factorial with Call Stack Frame Trace
    public static long factorial(int n) {
        if (n <= 1) return 1; // Base case
        return n * factorial(n - 1); // Stack frame created for each call
    }

    // Tail-recursive helper for optimization
    public static long factorialTail(int n, long accumulator) {
        if (n <= 1) return accumulator;
        return factorialTail(n - 1, n * accumulator);
    }

    public static void main(String[] args) {
        System.out.println("5! = " + factorial(5));
        System.out.println("5! (Tail Recursive) = " + factorialTail(5, 1));
    }
}""",

    "lesson_py_oop_nodes": """// Java Singly Linked List: Custom Node & In-Place Reversal
public class LinkedListReversal {
    static class ListNode {
        int val;
        ListNode next;
        ListNode(int val) { this.val = val; }
    }

    public static ListNode reverseList(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;

        while (curr != null) {
            ListNode nextTemp = curr.next; // Save next pointer
            curr.next = prev;             // Reverse link
            prev = curr;                  // Advance prev
            curr = nextTemp;              // Advance curr
        }
        return prev; // New head
    }

    public static void printList(ListNode head) {
        ListNode curr = head;
        while (curr != null) {
            System.out.print(curr.val + (curr.next != null ? " -> " : "\\n"));
            curr = curr.next;
        }
    }

    public static void main(String[] args) {
        ListNode head = new ListNode(1);
        head.next = new ListNode(2);
        head.next.next = new ListNode(3);
        head.next.next.next = new ListNode(4);

        System.out.print("Original: ");
        printList(head);

        ListNode reversed = reverseList(head);
        System.out.print("Reversed: ");
        printList(reversed);
    }
}"""
}

def seed_java_code():
    db = SessionLocal()
    try:
        updated = 0
        for lesson_id, java_code in JAVA_UPDATES.items():
            lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
            if lesson:
                lesson.java_code = java_code.strip()
                updated += 1
        db.commit()
        print(f"Successfully populated production Java code for {updated} lessons.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding Java solutions: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_java_code()
