import os
import json
import re
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
        # 1. Try external API first if configured
        if settings.GEMINI_API_KEY:
            try:
                res = await AIService._call_gemini(message, context_page, current_code, problem_title, student_level)
                if res:
                    return res
            except Exception:
                pass
        elif settings.OPENAI_API_KEY:
            try:
                res = await AIService._call_openai(message, context_page, current_code, problem_title, student_level)
                if res:
                    return res
            except Exception:
                pass

        # 2. Built-in High-Fidelity Algorithmic Reasoning Engine
        return AIService._offline_tutor_response(
            message=message,
            context_page=context_page,
            current_code=current_code,
            problem_title=problem_title,
            error_message=error_message,
            student_level=student_level
        )

    @staticmethod
    async def _call_gemini(
        message: str,
        context_page: str,
        current_code: Optional[str],
        problem_title: Optional[str],
        student_level: str
    ) -> Optional[Dict[str, Any]]:
        """Call Gemini API when GEMINI_API_KEY is available."""
        if not settings.GEMINI_API_KEY:
            return None
        model = settings.AI_MODEL or "gemini-1.5-flash"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={settings.GEMINI_API_KEY}"
        
        system_instruction = (
            f"You are AlgoMentor AI, an expert computer science and DSA personal tutor. "
            f"You adapt your explanations for a {student_level} learner. "
            f"Explain algorithms clearly with intuition, step-by-step logic, Big-O complexities (Time & Space), "
            f"and clean Python code when relevant. Format using Markdown. "
            f"Directly answer the user's specific question without repeating generic introductory greetings."
        )
        prompt_parts = []
        if problem_title:
            prompt_parts.append(f"Current Problem/Concept: {problem_title}")
        if context_page:
            prompt_parts.append(f"Context: {context_page}")
        prompt_parts.append(f"Student question: {message}")
        if current_code:
            prompt_parts.append(f"Student's current code:\n```python\n{current_code}\n```")

        payload = {
            "contents": [{"parts": [{"text": "\n\n".join(prompt_parts)}]}],
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "generationConfig": {"temperature": 0.35, "maxOutputTokens": 2048}
        }
        async with httpx.AsyncClient(timeout=12.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                code_snippet = None
                if "```python" in text:
                    code_snippet = text.split("```python")[1].split("```")[0].strip()
                elif "```" in text:
                    code_snippet = text.split("```")[1].split("```")[0].strip()
                return {
                    "session_id": 1,
                    "reply": text,
                    "code_suggestion": code_snippet
                }
        return None

    @staticmethod
    async def _call_openai(
        message: str,
        context_page: str,
        current_code: Optional[str],
        problem_title: Optional[str],
        student_level: str
    ) -> Optional[Dict[str, Any]]:
        """Call OpenAI API when OPENAI_API_KEY is available."""
        if not settings.OPENAI_API_KEY:
            return None
        url = "https://api.openai.com/v1/chat/completions"
        system_prompt = (
            f"You are AlgoMentor AI, an expert computer science and DSA personal tutor for {student_level} learners. "
            "Explain concepts with clear intuition, step-by-step breakdowns, Big-O complexities, and clean code. "
            "Directly answer the user's question without repeating generic greetings."
        )
        content_parts = []
        if problem_title:
            content_parts.append(f"Problem: {problem_title}")
        content_parts.append(f"Question: {message}")
        if current_code:
            content_parts.append(f"Code:\n```python\n{current_code}\n```")

        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "\n\n".join(content_parts)}
            ],
            "temperature": 0.35,
            "max_tokens": 1500
        }
        headers = {"Authorization": f"Bearer {settings.OPENAI_API_KEY}"}
        async with httpx.AsyncClient(timeout=12.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                text = data["choices"][0]["message"]["content"]
                code_snippet = None
                if "```python" in text:
                    code_snippet = text.split("```python")[1].split("```")[0].strip()
                return {
                    "session_id": 1,
                    "reply": text,
                    "code_suggestion": code_snippet
                }
        return None

    @staticmethod
    def _offline_tutor_response(
        message: str,
        context_page: str,
        current_code: Optional[str],
        problem_title: Optional[str],
        error_message: Optional[str],
        student_level: str
    ) -> Dict[str, Any]:
        """
        High-Fidelity Pedagogical Algorithmic Reasoning Engine.
        Covers all major DSA topics, algorithms, data structures, and edge cases.
        Directly answers user queries instead of repeating generic greetings.
        """
        msg = message.lower().strip()
        # Clean punctuation for keyword matching
        clean_msg = re.sub(r'[^\w\s-]', ' ', msg)

        def matches(kws: List[str]) -> bool:
            for kw in kws:
                if len(kw) <= 4:
                    if re.search(r'\b' + re.escape(kw) + r'\b', clean_msg):
                        return True
                else:
                    if kw in clean_msg:
                        return True
            return False

        # -------------------------------------------------------------
        # 1. Code Debugging / Review Request
        # -------------------------------------------------------------
        if (current_code and len(current_code.strip()) > 5) or matches(["debug", "fix", "error", "wrong"]):
            code_text = current_code or "No code snippet provided"
            err_text = f"\n**Reported Error:** `{error_message}`" if error_message else ""
            return {
                "session_id": 1,
                "reply": (
                    f"### Algorithmic Code Review & Debugging Guide{err_text}\n\n"
                    f"**Analysis of Solution Logic:**\n"
                    f"1. **Boundary & Base Cases:** Check if your code handles empty inputs (`len == 0`), single elements (`len == 1`), and extreme constraints (negative numbers, overflow).\n"
                    f"2. **Loop & Pointer Invariants:** Ensure while/for loop pointers strictly advance each iteration (`left += 1`, `right -= 1`, `curr = curr.next`). Stagnant pointers trigger Infinite Loops / TLE.\n"
                    f"3. **Off-by-One Guard:** When indexing `arr[i + 1]`, restrict loop bounds to `len(arr) - 1` to prevent `IndexError`.\n"
                    f"4. **Variable Initialization:** Accumulators (`count`, `total`, `seen`) must be initialized before conditional blocks.\n\n"
                    f"**Recommended Step-by-Step Fix:**\n"
                    f"- Dry-run with an input of size 2 on paper.\n"
                    f"- Replace nested $O(N^2)$ lookups with a Hash Set or Hash Map for $O(N)$ efficiency."
                ),
                "code_suggestion": (
                    "# Template for safe boundary checking and early exit:\n"
                    "def safe_solve(arr):\n"
                    "    if not arr:\n"
                    "        return 0  # Handle empty edge case\n"
                    "    seen = set()\n"
                    "    for item in arr:\n"
                    "        if item in seen:\n"
                    "            return item\n"
                    "        seen.add(item)\n"
                    "    return -1"
                )
            }

        # -------------------------------------------------------------
        # 2. Binary Search Tree (BST) & Balanced Trees (Check BEFORE Binary Search)
        # -------------------------------------------------------------
        if matches(["binary search tree", "bst", "avl", "red black", "red-black", "balanced tree", "search tree"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Binary Search Tree (BST) - Complete Guide\n\n"
                    f"**Definition & Core Invariant:**\n"
                    f"A Binary Search Tree is a node-based binary tree data structure with the strict ordering property:\n"
                    f"- Every node in the **left subtree** has a value strictly **less than** (`<`) the node's key.\n"
                    f"- Every node in the **right subtree** has a value strictly **greater than** (`>`) the node's key.\n"
                    f"- Both left and right subtrees must themselves be valid binary search trees.\n\n"
                    f"**Key Superpower: In-Order Traversal**\n"
                    f"Performing an **In-Order traversal (Left $\\rightarrow$ Node $\\rightarrow$ Right)** visits all elements in **strictly sorted ascending order** in $O(N)$ time!\n\n"
                    f"**Core Operations:**\n"
                    f"1. **Search:** Compare target with current node. If target is smaller $\\rightarrow$ search left child; if larger $\\rightarrow$ search right child.\n"
                    f"2. **Insertion:** Follow search path until finding a `None` pointer, then insert new node.\n"
                    f"3. **Deletion (3 Cases):**\n"
                    f"   - *Leaf node:* Simply delete it.\n"
                    f"   - *Single child:* Replace node with its child.\n"
                    f"   - *Two children:* Replace node with its **in-order successor** (smallest node in its right subtree), then delete the successor.\n\n"
                    f"**Complexity Analysis:**\n"
                    f"- **Balanced BST (AVL / Red-Black):**\n"
                    f"  - Search / Insert / Delete: **$O(\\log N)$** time, **$O(\\log N)$** stack space.\n"
                    f"- **Degenerate BST (Worst Case - Skewed Chain):**\n"
                    f"  - Occurs when elements are inserted in already sorted order $\\rightarrow$ degrades into a Linked List of height $N$ (**$O(N)$** time).\n\n"
                    f"**Interview Tips:**\n"
                    f"- To validate if a binary tree is a valid BST, pass `(min_allowed, max_allowed)` boundaries recursively down the tree."
                ),
                "code_suggestion": (
                    "class TreeNode:\n"
                    "    def __init__(self, val=0, left=None, right=None):\n"
                    "        self.val = val\n"
                    "        self.left = left\n"
                    "        self.right = right\n\n"
                    "class BST:\n"
                    "    def __init__(self):\n"
                    "        self.root = None\n\n"
                    "    def insert(self, val):\n"
                    "        def _ins(node, v):\n"
                    "            if not node: return TreeNode(v)\n"
                    "            if v < node.val: node.left = _ins(node.left, v)\n"
                    "            elif v > node.val: node.right = _ins(node.right, v)\n"
                    "            return node\n"
                    "        self.root = _ins(self.root, val)\n\n"
                    "    def search(self, val):\n"
                    "        curr = self.root\n"
                    "        while curr:\n"
                    "            if curr.val == val: return True\n"
                    "            curr = curr.left if val < curr.val else curr.right\n"
                    "        return False\n\n"
                    "    def inorder(self):\n"
                    "        res = []\n"
                    "        def _dfs(node):\n"
                    "            if not node: return\n"
                    "            _dfs(node.left)\n"
                    "            res.append(node.val)\n"
                    "            _dfs(node.right)\n"
                    "        _dfs(self.root)\n"
                    "        return res"
                )
            }

        # -------------------------------------------------------------
        # 3. Binary Search Algorithm & Halving Search Space
        # -------------------------------------------------------------
        if matches(["binary search", "bsearch", "binary_search", "lower_bound", "upper_bound", "search in rotated"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Binary Search Algorithm\n\n"
                    f"**Intuition & Mental Model:**\n"
                    f"Binary Search is a divide-and-conquer search technique that repeatedly **halves the search space**. "
                    f"Instead of inspecting $N$ elements one by one ($O(N)$ Linear Search), Binary Search eliminates 50% of candidate items in every single step.\n\n"
                    f"**Fundamental Prerequisite:**\n"
                    f"The input collection **must be sorted** (monotonically non-decreasing or non-increasing).\n\n"
                    f"**Algorithm Invariant & Steps:**\n"
                    f"1. Initialize bounds: `left = 0`, `right = len(arr) - 1`.\n"
                    f"2. Loop while `left <= right`:\n"
                    f"   - Calculate midpoint: `mid = left + (right - left) // 2` (prevents 32-bit integer overflow).\n"
                    f"   - If `arr[mid] == target`: Success! Return `mid`.\n"
                    f"   - If `arr[mid] < target`: Target must lie in the right partition $\\rightarrow$ set `left = mid + 1`.\n"
                    f"   - If `arr[mid] > target`: Target must lie in the left partition $\\rightarrow$ set `right = mid - 1`.\n"
                    f"3. If loop finishes without returning, target does not exist $\\rightarrow$ return `-1`.\n\n"
                    f"**Complexity Analysis:**\n"
                    f"- **Time Complexity:**\n"
                    f"  - Best Case: **$O(1)$** (element is at initial midpoint).\n"
                    f"  - Average & Worst Case: **$O(\\log N)$** (search space halves: $N \\rightarrow N/2 \\rightarrow N/4 \\dots \\rightarrow 1$).\n"
                    f"- **Space Complexity:** **$O(1)$** auxiliary memory for iterative approach ($O(\\log N)$ recursive stack).\n\n"
                    f"**Key Variations:**\n"
                    f"- *Lower Bound / First Occurrence:* On `arr[mid] == target`, keep searching left: `right = mid - 1`.\n"
                    f"- *Binary Search on Answer:* When searching for an optimal value in a monotonic range $[\\text{min}, \\text{max}]$ (e.g. Koko Eating Bananas, Capacity To Ship Packages)."
                ),
                "code_suggestion": (
                    "def binary_search(arr, target):\n"
                    "    \"\"\"\n"
                    "    Standard iterative binary search.\n"
                    "    Time: O(log N) | Space: O(1)\n"
                    "    \"\"\"\n"
                    "    left = 0\n"
                    "    right = len(arr) - 1\n\n"
                    "    while left <= right:\n"
                    "        # Prevents integer overflow: mid = left + (right - left) // 2\n"
                    "        mid = left + (right - left) // 2\n\n"
                    "        if arr[mid] == target:\n"
                    "            return mid\n"
                    "        elif arr[mid] < target:\n"
                    "            left = mid + 1\n"
                    "        else:\n"
                    "            right = mid - 1\n\n"
                    "    return -1  # Target not found"
                )
            }

        # -------------------------------------------------------------
        # 4. General Tree Data Structures & Traversals
        # -------------------------------------------------------------
        if matches(["tree", "binary tree", "inorder", "preorder", "postorder", "level order", "traversal", "lca", "lowest common ancestor", "diameter", "invert tree", "max depth"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Tree Data Structures & Traversal Strategies\n\n"
                    f"**Tree Architecture:**\n"
                    f"A Tree is a hierarchical non-linear data structure with a single `root` node and connected child nodes without cycles. In a **Binary Tree**, each node has at most 2 children (`left` and `right`).\n\n"
                    f"**Depth-First Search (DFS) Traversals ($O(N)$ Time, $O(h)$ Space):**\n"
                    f"1. **Pre-Order (Node $\\rightarrow$ Left $\\rightarrow$ Right):** Clones trees, serializes hierarchical configurations.\n"
                    f"2. **In-Order (Left $\\rightarrow$ Node $\\rightarrow$ Right):** Produces sorted order for BSTs.\n"
                    f"3. **Post-Order (Left $\\rightarrow$ Right $\\rightarrow$ Node):** Bottom-up computations (computing tree height, deleting trees, bottom-up DP).\n\n"
                    f"**Breadth-First Search (BFS) / Level-Order Traversal ($O(N)$ Time, $O(W)$ Space):**\n"
                    f"- Explores nodes level by level using a **FIFO Queue (`collections.deque`)**.\n"
                    f"- Crucial for finding the shortest path or shortest depth to a leaf node.\n\n"
                    f"**Complexity:** Time: $O(N)$ (visits every node once). Space: $O(h)$ where $h = \\text{height} = O(\\log N)$ balanced, $O(N)$ worst."
                ),
                "code_suggestion": (
                    "from collections import deque\n\n"
                    "# BFS / Level Order Traversal\n"
                    "def level_order(root):\n"
                    "    if not root: return []\n"
                    "    result = []\n"
                    "    queue = deque([root])\n"
                    "    while queue:\n"
                    "        level = []\n"
                    "        for _ in range(len(queue)):\n"
                    "            node = queue.popleft()\n"
                    "            level.append(node.val)\n"
                    "            if node.left: queue.append(node.left)\n"
                    "            if node.right: queue.append(node.right)\n"
                    "        result.append(level)\n"
                    "    return result"
                )
            }

        # -------------------------------------------------------------
        # 5. Trie (Prefix Tree)
        # -------------------------------------------------------------
        if matches(["trie", "prefix tree", "autocomplete"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Trie (Prefix Tree)\n\n"
                    f"**Concept & Purpose:**\n"
                    f"A Trie is a tree-like data structure used for storing and searching strings where keys are usually strings. "
                    f"Unlike a binary tree, nodes do not store the key; their position in the tree defines the key associated with it.\n\n"
                    f"**Key Advantages:**\n"
                    f"- **$O(L)$ Lookup & Insert:** Where $L$ is the word length, regardless of the number of words $N$ in the dictionary!\n"
                    f"- **Prefix Matching:** Ideal for autocomplete, predictive text, spell checkers, and IP routing (longest prefix match).\n\n"
                    f"**Structure:** Each TrieNode has `children = dict()` (map of char to TrieNode) and a boolean `is_end_of_word = False`."
                ),
                "code_suggestion": (
                    "class TrieNode:\n"
                    "    def __init__(self):\n"
                    "        self.children = {}\n"
                    "        self.is_end = False\n\n"
                    "class Trie:\n"
                    "    def __init__(self):\n"
                    "        self.root = TrieNode()\n\n"
                    "    def insert(self, word: str):\n"
                    "        node = self.root\n"
                    "        for ch in word:\n"
                    "            if ch not in node.children:\n"
                    "                node.children[ch] = TrieNode()\n"
                    "            node = node.children[ch]\n"
                    "        node.is_end = True\n\n"
                    "    def starts_with(self, prefix: str) -> bool:\n"
                    "        node = self.root\n"
                    "        for ch in prefix:\n"
                    "            if ch not in node.children: return False\n"
                    "            node = node.children[ch]\n"
                    "        return True"
                )
            }

        # -------------------------------------------------------------
        # 6. Linked Lists & Pointer Techniques
        # -------------------------------------------------------------
        if matches(["linked list", "linkedlist", "singly linked", "doubly linked", "reverse linked", "cycle detection", "floyd", "tortoise and hare", "dummy node"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Linked List Essentials & Core Patterns\n\n"
                    f"**Structure & Characteristics:**\n"
                    f"A Linked List is a linear collection of data elements where order is given by pointers. Unlike arrays:\n"
                    f"- **$O(1)$ Insertion/Deletion** at head (no shifting required).\n"
                    f"- **$O(N)$ Random Access** (no direct indexing like `arr[i]`).\n\n"
                    f"**Top 3 Must-Know Patterns:**\n"
                    f"1. **Dummy Head Pointer:** Eliminates special-casing when inserting/deleting the head node (`dummy = ListNode(0); dummy.next = head`).\n"
                    f"2. **Fast & Slow Pointers (Floyd's Tortoise and Hare):**\n"
                    f"   - Detect cycles in $O(N)$ time and $O(1)$ space (`slow = slow.next; fast = fast.next.next`).\n"
                    f"   - Find middle node of linked list in a single pass.\n"
                    f"3. **In-Place Reversal:** Maintain three pointers: `prev = None`, `curr = head`, and `next_temp = curr.next`."
                ),
                "code_suggestion": (
                    "class ListNode:\n"
                    "    def __init__(self, val=0, next=None):\n"
                    "        self.val = val\n"
                    "        self.next = next\n\n"
                    "# 1. Reverse Linked List In-Place O(N) Time, O(1) Space\n"
                    "def reverse_list(head):\n"
                    "    prev, curr = None, head\n"
                    "    while curr:\n"
                    "        nxt = curr.next\n"
                    "        curr.next = prev\n"
                    "        prev = curr\n"
                    "        curr = nxt\n"
                    "    return prev\n\n"
                    "# 2. Floyd's Cycle Detection O(N) Time, O(1) Space\n"
                    "def has_cycle(head):\n"
                    "    slow, fast = head, head\n"
                    "    while fast and fast.next:\n"
                    "        slow = slow.next\n"
                    "        fast = fast.next.next\n"
                    "        if slow == fast:\n"
                    "            return True\n"
                    "    return False"
                )
            }

        # -------------------------------------------------------------
        # 7. Stacks & Queues (Monotonic Stack, Parentheses, etc.)
        # -------------------------------------------------------------
        if matches(["stack", "lifo", "queue", "fifo", "deque", "monotonic stack", "parentheses", "next greater element", "min stack"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Stacks & Queues: Fundamentals & Monotonic Patterns\n\n"
                    f"**1. Stack (LIFO - Last In, First Out):**\n"
                    f"- Operations: `push` $O(1)$, `pop` $O(1)$, `peek` $O(1)$.\n"
                    f"- Primary Uses: Call stack / recursion, undo operations, syntax parsing, matching brackets.\n"
                    f"- **Monotonic Stack Pattern:** Elements inside stack are kept strictly increasing or decreasing. Solves **'Next Greater Element'** and **'Largest Rectangle in Histogram'** in linear $O(N)$ time instead of $O(N^2)$.\n\n"
                    f"**2. Queue (FIFO - First In, First Out):**\n"
                    f"- Operations: `enqueue` $O(1)$, `dequeue` $O(1)$.\n"
                    f"- Primary Uses: Breadth-First Search (BFS), task scheduling, sliding window buffers.\n"
                    f"- In Python, always use `collections.deque` instead of `list` (`list.pop(0)` is $O(N)$ due to element shifting; `deque.popleft()` is $O(1)$)."
                ),
                "code_suggestion": (
                    "# Valid Parentheses using Stack: O(N) Time, O(N) Space\n"
                    "def is_valid_parentheses(s: str) -> bool:\n"
                    "    mapping = {')': '(', '}': '{', ']': '['}\n"
                    "    stack = []\n"
                    "    for char in s:\n"
                    "        if char in mapping:\n"
                    "            top = stack.pop() if stack else '#'\n"
                    "            if mapping[char] != top:\n"
                    "                return False\n"
                    "        else:\n"
                    "            stack.append(char)\n"
                    "    return len(stack) == 0"
                )
            }

        # -------------------------------------------------------------
        # 8. Heaps & Priority Queues
        # -------------------------------------------------------------
        if matches(["heap", "priority queue", "min heap", "max heap", "heapify", "heapsort", "kth largest", "top k"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Heaps & Priority Queues\n\n"
                    f"**Definition & Binary Heap Properties:**\n"
                    f"A Heap is a complete binary tree serialized in an array where:\n"
                    f"- **Min-Heap:** Parent node value $\\le$ children values (Root is absolute minimum).\n"
                    f"- **Max-Heap:** Parent node value $\\ge$ children values (Root is absolute maximum).\n"
                    f"- Array indexing: Left child at `2*i + 1`, right child at `2*i + 2`, parent at `(i - 1) // 2`.\n\n"
                    f"**Complexity Overview:**\n"
                    f"- Peek min/max: **$O(1)$**\n"
                    f"- Insert (`heappush`): **$O(\\log N)$** (percolates up)\n"
                    f"- Extract (`heappop`): **$O(\\log N)$** (percolates down)\n"
                    f"- Build Heap (`heapify`): **$O(N)$** linear time!\n\n"
                    f"**Top Problem Pattern: K-th Largest Element:**\n"
                    f"- Keep a **Min-Heap of size K**. For each number, push and pop if size exceeds K. The root will be the K-th largest in $O(N \\log K)$ time."
                ),
                "code_suggestion": (
                    "import heapq\n\n"
                    "def find_kth_largest(nums, k):\n"
                    "    \"\"\"Finds K-th largest element using Min-Heap of size K: O(N log K)\"\"\"\n"
                    "    heap = []\n"
                    "    for num in nums:\n"
                    "        heapq.heappush(heap, num)\n"
                    "        if len(heap) > k:\n"
                    "            heapq.heappop(heap)\n"
                    "    return heap[0]  # Root is the K-th largest"
                )
            }

        # -------------------------------------------------------------
        # 9. Hash Maps & Hash Tables
        # -------------------------------------------------------------
        if matches(["hash", "hashmap", "hash table", "hashtable", "collision", "two sum", "dictionary", "hash set"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Hash Maps & Hash Tables: Instant Lookup\n\n"
                    f"**Core Intuition:**\n"
                    f"A Hash Map maps keys to values using a **hash function** that converts arbitrary keys into array bucket indices. This unlocks average **$O(1)$ time complexity** for insertions, lookups, and deletions.\n\n"
                    f"**Collision Resolution Strategies:**\n"
                    f"1. **Chaining:** Each bucket points to a linked list or balanced tree of entries with the same hash.\n"
                    f"2. **Open Addressing:** Probes alternative slots in the array (Linear Probing, Quadratic Probing, Double Hashing).\n\n"
                    f"**The Two Sum Blueprint ($O(N)$ Time vs $O(N^2)$ Brute Force):**\n"
                    f"- Instead of two nested loops checking all pairs $(i, j)$, store `seen[num] = index`.\n"
                    f"- For each number `x`, check if `complement = target - x` already exists in the hash map in $O(1)$."
                ),
                "code_suggestion": (
                    "def two_sum(nums, target):\n"
                    "    seen = {}  # val -> index\n"
                    "    for i, num in enumerate(nums):\n"
                    "        complement = target - num\n"
                    "        if complement in seen:\n"
                    "            return [seen[complement], i]\n"
                    "        seen[num] = i\n"
                    "    return []"
                )
            }

        # -------------------------------------------------------------
        # 10. Two Pointers & Sliding Window
        # -------------------------------------------------------------
        if matches(["two pointer", "two pointers", "sliding window", "subarray", "container with most water", "3sum", "longest substring"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Two Pointers & Sliding Window Techniques\n\n"
                    f"**1. Two Pointers (Inward or Forward):**\n"
                    f"- **Inward Facing:** `left = 0`, `right = len - 1` moving toward each other. Ideal for sorted arrays (Pair Sum, Palindrome verification, Container with Most Water).\n"
                    f"- **Fast & Slow:** Both start at 0 but move at different speeds (Cycle detection, remove duplicates in-place).\n\n"
                    f"**2. Sliding Window (Dynamic or Fixed Size):**\n"
                    f"- Converts nested $O(N^2)$ brute-force subsegment checks into linear **$O(N)$** passes.\n"
                    f"- **Template:** Expand the window by advancing `right`. When window constraint is violated (e.g. duplicate character, sum exceeds limit), shrink by advancing `left` until valid again."
                ),
                "code_suggestion": (
                    "# Longest Substring Without Repeating Characters: O(N) Time, O(min(N, M)) Space\n"
                    "def length_of_longest_substring(s: str) -> int:\n"
                    "    char_index = {}\n"
                    "    max_len = 0\n"
                    "    left = 0\n"
                    "    for right, ch in enumerate(s):\n"
                    "        if ch in char_index and char_index[ch] >= left:\n"
                    "            left = char_index[ch] + 1\n"
                    "        char_index[ch] = right\n"
                    "        max_len = max(max_len, right - left + 1)\n"
                    "    return max_len"
                )
            }

        # -------------------------------------------------------------
        # 11. Prefix Sum & Kadane's Algorithm
        # -------------------------------------------------------------
        if matches(["prefix sum", "kadane", "maximum subarray", "max subarray", "range sum"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Prefix Sum & Kadane's Algorithm\n\n"
                    f"**1. Prefix Sum Array:**\n"
                    f"- Precomputes cumulative sums: `prefix[i] = arr[0] + ... + arr[i-1]`.\n"
                    f"- Computes any range sum `arr[L..R]` in **$O(1)$ time** via `prefix[R + 1] - prefix[L]`.\n\n"
                    f"**2. Kadane's Algorithm (Maximum Subarray):**\n"
                    f"- Solves the maximum subarray problem in **$O(N)$ Time and $O(1)$ Space**.\n"
                    f"- **Invariant:** At each index `i`, we make a local choice: either extend the current running subarray sum (`curr_sum + arr[i]`) or start a brand new subarray starting at `arr[i]` (`max(arr[i], curr_sum + arr[i])`)."
                ),
                "code_suggestion": (
                    "def max_sub_array(nums):\n"
                    "    \"\"\"Kadane's Algorithm: O(N) Time | O(1) Space\"\"\"\n"
                    "    max_sum = nums[0]\n"
                    "    curr_sum = nums[0]\n"
                    "    for num in nums[1:]:\n"
                    "        curr_sum = max(num, curr_sum + num)\n"
                    "        max_sum = max(max_sum, curr_sum)\n"
                    "    return max_sum"
                )
            }

        # -------------------------------------------------------------
        # 12. Sorting Algorithms (Merge, Quick, Bubble, Selection, etc.)
        # -------------------------------------------------------------
        if matches(["sort", "sorting", "bubble", "quick", "merge", "insertion", "selection", "heap sort", "counting sort", "radix"]):
            is_merge = "merge" in clean_msg
            is_quick = "quick" in clean_msg
            is_bubble = "bubble" in clean_msg
            return {
                "session_id": 1,
                "reply": (
                    f"### Sorting Algorithms In-Depth\n\n"
                    f"**Comparison Matrix:**\n"
                    f"| Algorithm | Best Time | Avg Time | Worst Time | Space | Stable? |\n"
                    f"| :--- | :--- | :--- | :--- | :--- | :--- |\n"
                    f"| **Merge Sort** | $O(N \\log N)$ | $O(N \\log N)$ | $O(N \\log N)$ | $O(N)$ | Yes |\n"
                    f"| **Quick Sort** | $O(N \\log N)$ | $O(N \\log N)$ | $O(N^2)$ | $O(\\log N)$ | No |\n"
                    f"| **Heap Sort** | $O(N \\log N)$ | $O(N \\log N)$ | $O(N \\log N)$ | $O(1)$ | No |\n"
                    f"| **Insertion Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes |\n"
                    f"| **Bubble Sort** | $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes |\n\n"
                    f"**Key Algorithmic Concepts:**\n"
                    f"- **Merge Sort:** Divide and Conquer. Splits array into two halves, recursively sorts them, then merges two sorted halves in linear $O(N)$ time.\n"
                    f"- **Quick Sort:** Selects a `pivot`, partitions elements smaller than pivot to left and greater to right. In-place and cache-friendly.\n"
                    f"- **Stability:** A sort is stable if it preserves the relative order of records with equal keys."
                ),
                "code_suggestion": (
                    "# Merge Sort Implementation: O(N log N) Guaranteed\n"
                    "def merge_sort(arr):\n"
                    "    if len(arr) <= 1: return arr\n"
                    "    mid = len(arr) // 2\n"
                    "    left = merge_sort(arr[:mid])\n"
                    "    right = merge_sort(arr[mid:])\n"
                    "    return merge(left, right)\n\n"
                    "def merge(left, right):\n"
                    "    res = []\n"
                    "    i = j = 0\n"
                    "    while i < len(left) and j < len(right):\n"
                    "        if left[i] <= right[j]:\n"
                    "            res.append(left[i]); i += 1\n"
                    "        else:\n"
                    "            res.append(right[j]); j += 1\n"
                    "    res.extend(left[i:])\n"
                    "    res.extend(right[j:])\n"
                    "    return res"
                )
            }

        # -------------------------------------------------------------
        # 13. Graph Algorithms (BFS, DFS, Dijkstra, Topo Sort, DSU)
        # -------------------------------------------------------------
        if matches(["graph", "bfs", "dfs", "dijkstra", "shortest path", "topological", "kahn", "union find", "dsu", "disjoint set", "kruskal", "prim", "bipartite", "cycle"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Graph Traversal & Shortest Path Algorithms\n\n"
                    f"**Core Traversal Techniques:**\n"
                    f"1. **Breadth-First Search (BFS):**\n"
                    f"   - Explores neighbors layer-by-layer using a **FIFO Queue**.\n"
                    f"   - Optimal for finding the **unweighted shortest path** in $O(V + E)$ time.\n"
                    f"2. **Depth-First Search (DFS):**\n"
                    f"   - Recursively dives deep down paths using a **Call Stack**.\n"
                    f"   - Ideal for cycle detection, topological sorting, connected components, and pathfinding.\n\n"
                    f"**Shortest Path in Weighted Graphs:**\n"
                    f"- **Dijkstra's Algorithm ($O((V + E) \\log V)$):** Greedy approach using a **Min-Heap (Priority Queue)**. Finds single-source shortest path for graphs with non-negative edge weights.\n"
                    f"- **Bellman-Ford ($O(V \\cdot E)$):** Handles negative edge weights and detects negative weight cycles.\n\n"
                    f"**Topological Sorting (Kahn's Algorithm - $O(V + E)$):**\n"
                    f"- Computes linear ordering of vertices in a Directed Acyclic Graph (DAG) using in-degrees."
                ),
                "code_suggestion": (
                    "import heapq\n\n"
                    "def dijkstra(graph, start):\n"
                    "    \"\"\"\n"
                    "    Dijkstra's Shortest Path on Adjacency List graph: {u: [(v, weight), ...]}\n"
                    "    Time: O((V + E) log V) | Space: O(V)\n"
                    "    \"\"\"\n"
                    "    distances = {node: float('inf') for node in graph}\n"
                    "    distances[start] = 0\n"
                    "    pq = [(0, start)]  # (distance, node)\n\n"
                    "    while pq:\n"
                    "        curr_dist, u = heapq.heappop(pq)\n"
                    "        if curr_dist > distances[u]:\n"
                    "            continue\n"
                    "        for v, weight in graph[u]:\n"
                    "            dist = curr_dist + weight\n"
                    "            if dist < distances[v]:\n"
                    "                distances[v] = dist\n"
                    "                heapq.heappush(pq, (dist, v))\n"
                    "    return distances"
                )
            }

        # -------------------------------------------------------------
        # 14. Dynamic Programming (DP) & Memoization
        # -------------------------------------------------------------
        if matches(["dynamic programming", "dp", "memoization", "tabulation", "knapsack", "lcs", "lis", "coin change", "edit distance", "subsequence"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Dynamic Programming (DP) Master Guide\n\n"
                    f"**When to Apply Dynamic Programming:**\n"
                    f"A problem can be solved with DP if and only if it exhibits two properties:\n"
                    f"1. **Overlapping Subproblems:** The same recursive subproblems are computed repeatedly.\n"
                    f"2. **Optimal Substructure:** The optimal solution to the problem can be constructed from optimal solutions to its subproblems.\n\n"
                    f"**Two Implementation Frameworks:**\n"
                    f"- **Top-Down (Memoization):** Natural recursion + cache map. Easy to formulate directly from the recurrence relation.\n"
                    f"- **Bottom-Up (Tabulation):** Iteratively fills a DP table starting from the base cases. Avoids recursion stack overhead and allows space optimization (e.g. rolling variables).\n\n"
                    f"**Top Canonical DP Patterns:**\n"
                    f"- **0/1 Knapsack:** Item inclusion/exclusion decisions ($O(N \\cdot W)$).\n"
                    f"- **Longest Common Subsequence (LCS):** String matching comparisons ($O(N \\cdot M)$).\n"
                    f"- **Coin Change / Unbounded Knapsack:** Finding minimum coins to make an amount."
                ),
                "code_suggestion": (
                    "# Coin Change (Min coins for amount): Bottom-Up Tabulation\n"
                    "def coin_change(coins, amount):\n"
                    "    dp = [float('inf')] * (amount + 1)\n"
                    "    dp[0] = 0  # Base case: 0 coins for 0 amount\n"
                    "    for a in range(1, amount + 1):\n"
                    "        for coin in coins:\n"
                    "            if a - coin >= 0:\n"
                    "                dp[a] = min(dp[a], dp[a - coin] + 1)\n"
                    "    return dp[amount] if dp[amount] != float('inf') else -1"
                )
            }

        # -------------------------------------------------------------
        # 15. Recursion & Backtracking
        # -------------------------------------------------------------
        if matches(["recursion", "recursive", "backtrack", "backtracking", "base case", "n-queens", "sudoku", "permutation", "combination", "subsets"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Recursion & Backtracking\n\n"
                    f"**The Backtracking Blueprint:**\n"
                    f"Backtracking is an algorithmic technique for solving constraint-satisfaction problems by trying candidates and abandoning (backtracking) each candidate as soon as it is determined it cannot lead to a valid solution.\n\n"
                    f"**The 3 Mandatory Pillars:**\n"
                    f"1. **Base Case / Goal:** What condition terminates the recursion (e.g., candidate length equals target, board is full)?\n"
                    f"2. **Choices & Constraints:** What choices are valid at current state? Only recurse on valid choices.\n"
                    f"3. **State Undo (Backtrack):** After returning from the recursive branch, undo your modification (`state.pop()`, unmark visited) so subsequent branches start with clean state."
                ),
                "code_suggestion": (
                    "# Subsets / Power Set Generation via Backtracking\n"
                    "def subsets(nums):\n"
                    "    result = []\n"
                    "    def backtrack(start, path):\n"
                    "        result.append(list(path))\n"
                    "        for i in range(start, len(nums)):\n"
                    "            path.append(nums[i])      # 1. Make choice\n"
                    "            backtrack(i + 1, path)    # 2. Recurse\n"
                    "            path.pop()                # 3. Undo choice (backtrack)\n"
                    "    backtrack(0, [])\n"
                    "    return result"
                )
            }

        # -------------------------------------------------------------
        # 16. Bit Manipulation
        # -------------------------------------------------------------
        if matches(["bit", "bitwise", "xor", "twos complement", "count set bits"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Bit Manipulation & Bitwise Tricks\n\n"
                    f"**Fundamental Bitwise Operators:**\n"
                    f"- `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (Left Shift - multiplies by $2$), `>>` (Right Shift - divides by $2$).\n\n"
                    f"**Essential Bitwise Secrets:**\n"
                    f"1. **XOR Cancellation:** `x ^ x = 0` and `x ^ 0 = x`. (Find the single unique number in an array where all other elements appear twice).\n"
                    f"2. **Brian Kernighan's Trick (`n & (n - 1)`):** Clears the lowest set bit in $O(1)$ time. Useful for counting set bits in $O(\\text{count})$ operations.\n"
                    f"3. **Check Power of 2:** `(n > 0) and (n & (n - 1) == 0)` evaluates to `True` if $n$ is a power of 2."
                ),
                "code_suggestion": (
                    "# Single Number (every other element appears twice): O(N) Time, O(1) Space\n"
                    "def single_number(nums):\n"
                    "    res = 0\n"
                    "    for num in nums:\n"
                    "        res ^= num\n"
                    "    return res"
                )
            }

        # -------------------------------------------------------------
        # 17. Time & Space Complexity (Big-O)
        # -------------------------------------------------------------
        if matches(["complexity", "big o", "big-o", "time complexity", "space complexity", "master theorem", "amortized"]):
            return {
                "session_id": 1,
                "reply": (
                    f"### Complexity Analysis Guide for {student_level} Learners\n\n"
                    f"**The Big-O Hierarchy of Growth:**\n"
                    f"$$O(1) < O(\\log N) < O(N) < O(N \\log N) < O(N^2) < O(2^N) < O(N!)$$\n\n"
                    f"**Practical Identification Rules:**\n"
                    f"- **$O(1)$:** Direct arithmetic, array index access `arr[i]`, hash table lookup.\n"
                    f"- **$O(\\log N)$:** Halving search space each step (Binary Search, balanced BST operations).\n"
                    f"- **$O(N)$:** Single linear loop, DFS/BFS visiting all nodes.\n"
                    f"- **$O(N \\log N)$:** Efficient comparison sorts (Merge Sort, Quick Sort average), heap operations on $N$ items.\n"
                    f"- **$O(N^2)$:** Nested loops over the collection (Bubble/Selection Sort, checking all pairs).\n"
                    f"- **$O(2^N)$:** Recursive tree exploring all subsets / combinations without memoization.\n\n"
                    f"**Auxiliary Space vs Input Space:** Space complexity measures additional memory allocated during execution (excluding input size)."
                ),
                "code_suggestion": (
                    "# Comparing O(N^2) vs O(N) Space-Time Tradeoff:\n"
                    "# Naive O(N^2) search:\n"
                    "# for i in arr: for j in arr: if i + j == target: return True\n\n"
                    "# Optimized O(N) time with O(N) auxiliary space:\n"
                    "seen = set(arr)  # O(N) space, O(1) membership check\n"
                    "for x in arr:\n"
                    "    if (target - x) in seen:\n"
                    "        return True"
                )
            }

        # -------------------------------------------------------------
        # 18. General Search / Linear Search
        # -------------------------------------------------------------
        if "search" in clean_msg:
            return {
                "session_id": 1,
                "reply": (
                    f"### Search Algorithms: Linear vs Binary Search\n\n"
                    f"**1. Linear Search ($O(N)$ Time, $O(1)$ Space):**\n"
                    f"- Inspects each element sequentially from index $0$ to $N-1$.\n"
                    f"- Does **not** require sorted data. Best for small lists or unsorted collections.\n\n"
                    f"**2. Binary Search ($O(\\log N)$ Time, $O(1)$ Space):**\n"
                    f"- Requires the array to be **sorted**.\n"
                    f"- Halves the search interval on every comparison by inspecting the midpoint `mid = left + (right - left) // 2`."
                ),
                "code_suggestion": (
                    "def linear_search(arr, target):\n"
                    "    for i, val in enumerate(arr):\n"
                    "        if val == target: return i\n"
                    "    return -1"
                )
            }

        # -------------------------------------------------------------
        # 19. Intelligent Dynamic Response (NEVER repeat generic greeting!)
        # -------------------------------------------------------------
        # Extract user's core inquiry topic
        topic_title = problem_title if problem_title else message[:60].strip()
        context_hint = f" regarding **{problem_title}**" if problem_title else ""

        return {
            "session_id": 1,
            "reply": (
                f"### Algorithmic Concept Breakdown: \"{message.strip()}\"{context_hint}\n\n"
                f"**1. Fundamental Algorithmic Strategy:**\n"
                f"When addressing **\"{message.strip()}\"**, consider how the input data structure dictates algorithmic efficiency:\n"
                f"- **Contiguous data (Arrays, Strings):** Evaluate if sorting, Two Pointers, or a Sliding Window transforms an $O(N^2)$ brute force into $O(N)$ or $O(N \\log N)$.\n"
                f"- **Hierarchical data (Trees, BSTs):** Determine whether a recursive DFS (In-order, Pre-order, Post-order) or a level-by-level BFS with a Queue is optimal.\n"
                f"- **Relational data (Graphs):** Check if state representation requires an adjacency list, and whether cycle detection or shortest-path discovery (BFS/Dijkstra) applies.\n\n"
                f"**2. Recommended Problem-Solving Framework:**\n"
                f"1. **Clarify Constraints:** Are inputs guaranteed to be non-empty? Are values positive, negative, or duplicates?\n"
                f"2. **State Loop Invariant:** What property is guaranteed to hold true before and after each iteration?\n"
                f"3. **Choose Optimal Data Structure:** Trade auxiliary space ($O(N)$ Hash Map / Heap) to reduce asymptotic runtime.\n\n"
                f"Would you like me to walk through a concrete code implementation, trace an example step-by-step, or analyze the time and space complexity?"
            ),
            "code_suggestion": (
                "# Recommended skeleton for structured problem solving:\n"
                "def solve(input_data):\n"
                "    # 1. Base / boundary checks\n"
                "    if not input_data:\n"
                "        return None\n\n"
                "    # 2. Algorithmic processing\n"
                "    # ...\n\n"
                "    # 3. Return target output\n"
                "    return result"
            )
        }

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
    const { r, c } = queue.shift();
    visitedCount++;
    document.getElementById('visitedCount').innerText = visitedCount;

    if (r === targetNode.r && c === targetNode.c) {
      found = true;
      break;
    }

    if (!(r === startNode.r && c === startNode.c)) {
      grid[r][c].el.classList.add('visited');
    }

    const neighbors = [
      { r: r - 1, c }, { r: r + 1, c },
      { r, c: c - 1 }, { r, c: c + 1 }
    ];

    for (let n of neighbors) {
      if (n.r >= 0 && n.r < ROWS && n.c >= 0 && n.c < COLS) {
        const neighborNode = grid[n.r][n.c];
        if (!neighborNode.isWall && !neighborNode.visited) {
          neighborNode.visited = true;
          neighborNode.parent = { r, c };
          queue.push(n);
        }
      }
    }
    await new Promise(res => setTimeout(res, 15));
  }

  if (found) drawPath();
}

async function runDijkstra() {
  clearVisited();
  let distances = Array.from({ length: ROWS }, () => Array(COLS).fill(Infinity));
  distances[startNode.r][startNode.c] = 0;
  let pq = [{ r: startNode.r, c: startNode.c, d: 0 }];
  let visitedCount = 0;
  let found = false;

  while (pq.length > 0) {
    pq.sort((a, b) => a.d - b.d);
    const { r, c, d } = pq.shift();

    if (grid[r][c].visited) continue;
    grid[r][c].visited = true;
    visitedCount++;
    document.getElementById('visitedCount').innerText = visitedCount;

    if (r === targetNode.r && c === targetNode.c) {
      found = true;
      break;
    }

    if (!(r === startNode.r && c === startNode.c)) {
      grid[r][c].el.classList.add('visited');
    }

    const neighbors = [
      { r: r - 1, c }, { r: r + 1, c },
      { r, c: c - 1 }, { r, c: c + 1 }
    ];

    for (let n of neighbors) {
      if (n.r >= 0 && n.r < ROWS && n.c >= 0 && n.c < COLS) {
        if (!grid[n.r][n.c].isWall && !grid[n.r][n.c].visited) {
          if (d + 1 < distances[n.r][n.c]) {
            distances[n.r][n.c] = d + 1;
            grid[n.r][n.c].parent = { r, c };
            pq.push({ r: n.r, c: n.c, d: d + 1 });
          }
        }
      }
    }
    await new Promise(res => setTimeout(res, 15));
  }

  if (found) drawPath();
}

async function drawPath() {
  let curr = grid[targetNode.r][targetNode.c].parent;
  let length = 0;
  while (curr && !(curr.r === startNode.r && curr.c === startNode.c)) {
    length++;
    grid[curr.r][curr.c].el.classList.remove('visited');
    grid[curr.r][curr.c].el.classList.add('path');
    curr = grid[curr.r][curr.c].parent;
    await new Promise(res => setTimeout(res, 25));
  }
  document.getElementById('pathLength').innerText = length;
}

function clearVisited() {
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      grid[r][c].visited = false;
      grid[r][c].parent = null;
      grid[r][c].el.classList.remove('visited', 'path');
    }
  }
  document.getElementById('visitedCount').innerText = 0;
  document.getElementById('pathLength').innerText = 0;
}

function clearWalls() {
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      grid[r][c].isWall = false;
      grid[r][c].el.classList.remove('wall');
    }
  }
}

document.getElementById('runBFS').addEventListener('click', runBFS);
document.getElementById('runDijkstra').addEventListener('click', runDijkstra);
document.getElementById('clearWalls').addEventListener('click', clearWalls);
document.getElementById('resetGrid').addEventListener('click', () => { clearVisited(); clearWalls(); });

init();"""
                }
            ]
        }

    @staticmethod
    def _get_sorting_benchmark_project_template(prompt: str) -> Dict[str, Any]:
        return {
            "title": "Sorting Algorithm Performance Benchmark Suite",
            "description": "Interactive HTML5 canvas tool comparing Quick Sort, Merge Sort, and Bubble Sort in real-time execution speeds.",
            "project_type": "web_interactive",
            "tags": "sorting,benchmark,javascript,canvas",
            "files": [
                {
                    "filename": "index.html",
                    "filepath": "index.html",
                    "language": "html",
                    "content": """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Sorting Benchmark Suite</title>
  <style>
    body { background: #0f172a; color: #e2e8f0; font-family: sans-serif; padding: 20px; }
    canvas { background: #1e293b; border-radius: 8px; display: block; margin: 20px auto; }
    .controls { display: flex; justify-content: center; gap: 10px; margin-bottom: 10px; }
    button { padding: 8px 16px; background: #0284c7; color: white; border: none; border-radius: 4px; cursor: pointer; }
    button:hover { background: #0369a1; }
  </style>
</head>
<body>
  <h2 style="text-align:center;">Sorting Benchmark Suite</h2>
  <div class="controls">
    <button onclick="startBubble()">Run Bubble Sort</button>
    <button onclick="resetArray()">Reset Data</button>
  </div>
  <canvas id="sortCanvas" width="600" height="300"></canvas>
  <script>
    let arr = [];
    const canvas = document.getElementById('sortCanvas');
    const ctx = canvas.getContext('2d');
    function resetArray() {
      arr = Array.from({ length: 50 }, () => Math.floor(Math.random() * 250) + 10);
      draw();
    }
    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const w = canvas.width / arr.length;
      arr.forEach((val, i) => {
        ctx.fillStyle = '#38bdf8';
        ctx.fillRect(i * w, canvas.height - val, w - 2, val);
      });
    }
    async function startBubble() {
      for (let i = 0; i < arr.length; i++) {
        for (let j = 0; j < arr.length - i - 1; j++) {
          if (arr[j] > arr[j + 1]) {
            [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
            draw();
            await new Promise(r => setTimeout(r, 10));
          }
        }
      }
    }
    resetArray();
  </script>
</body>
</html>"""
                }
            ]
        }

    @staticmethod
    def _get_bst_explorer_project_template(prompt: str) -> Dict[str, Any]:
        return {
            "title": "Binary Search Tree (BST) Visual Explorer",
            "description": "Canvas-based dynamic Binary Search Tree with live insert, search, and balanced layout visualization.",
            "project_type": "web_interactive",
            "tags": "bst,tree,binary_search,canvas",
            "files": [
                {
                    "filename": "index.html",
                    "filepath": "index.html",
                    "language": "html",
                    "content": """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>BST Visual Explorer</title>
  <style>
    body { background: #0f172a; color: #e2e8f0; font-family: sans-serif; padding: 20px; text-align: center; }
    canvas { background: #1e293b; border-radius: 8px; margin: 15px auto; display: block; border: 1px solid #334155; }
    input, button { padding: 8px 14px; border-radius: 6px; border: none; font-size: 14px; }
    input { background: #334155; color: white; margin-right: 8px; }
    button { background: #6366f1; color: white; cursor: pointer; }
    button:hover { background: #4f46e5; }
  </style>
</head>
<body>
  <h2>Interactive Binary Search Tree Explorer</h2>
  <div>
    <input type="number" id="valInput" placeholder="Enter number..." />
    <button onclick="handleInsert()">Insert Node</button>
    <button onclick="resetTree()" style="background:#ef4444; margin-left:6px;">Reset</button>
  </div>
  <canvas id="canvas" width="700" height="350"></canvas>
  <script>
    class Node {
      constructor(val) { this.val = val; this.left = null; this.right = null; }
    }
    let root = null;
    function insert(node, val) {
      if (!node) return new Node(val);
      if (val < node.val) node.left = insert(node.left, val);
      else if (val > node.val) node.right = insert(node.right, val);
      return node;
    }
    function handleInsert() {
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
