"""
AlgoMentor Comprehensive DSA & Algorithm Library Seed Script
Populates the complete syllabus covering all 24 distinct DSA categories with individual concept cards.
Each concept contains:
- Category & Difficulty (Beginner / Intermediate / Advanced)
- Prerequisites & Learning sequence
- Full 11-section learning content
- Video URL & Visualizer links
- Java & Python solutions
- Dry run states & interactive quiz
"""

import json
import sqlite3
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.lesson import Lesson

ALL_CONCEPTS = [
    # -------------------------------------------------------------
    # 1. Programming Fundamentals
    # -------------------------------------------------------------
    {
        "id": "concept_prog_variables_memory",
        "category": "Programming Fundamentals",
        "difficulty": "Beginner",
        "title": "Variables, Primitive Types & Memory Allocation",
        "prerequisites": "None",
        "summary": "Understand how memory is allocated for variables, primitives vs references, stack frames, and address pointers.",
        "why_learn_it": "All algorithmic computation manipulates memory. Knowing the difference between stack and heap allocations prevents aliasing bugs in complex data structures.",
        "fundamental_explanation": "Variables are named memory locations holding values or memory addresses. Primitive variables (int, boolean, float) store literal bits directly on the execution stack. Reference variables (arrays, objects) store memory addresses pointing to allocations on the dynamic heap.",
        "core_theory": "### Memory Layout\n1. **Call Stack:** Instantaneous LIFO memory allocated for function frames and local primitives.\n2. **Heap Memory:** Dynamically allocated memory where objects, arrays, and complex structures reside.\n3. **Pass-by-Value vs Reference:** Python and Java pass object references by value—reassigning the reference variable does not affect the caller, but mutating the underlying heap object changes state globally.",
        "time_complexity": "Access: O(1) · Allocation: O(1)",
        "space_complexity": "Stack Frame: O(1)",
        "video_url": "https://www.youtube.com/embed/m9n2b0_HpxE",
        "video_title": "Memory Layout: Stack vs Heap Explained",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class MemoryBasics {
    public static void main(String[] args) {
        int a = 10; // Primitive on stack
        int[] arr = new int[]{1, 2, 3}; // Reference on stack pointing to Heap array
        System.out.println("Stack primitive: " + a);
    }
}""",
        "python_code": """def memory_demo():
    x = 42 # immutable int
    lst = [1, 2, 3] # mutable list reference on heap
    print(f"Object ID in memory: {id(lst)}")

memory_demo()"""
    },
    {
        "id": "concept_prog_time_space_big_o",
        "category": "Programming Fundamentals",
        "difficulty": "Beginner",
        "title": "Asymptotic Analysis: Big O, Big Omega & Big Theta",
        "prerequisites": "Variables & Loops",
        "summary": "Master mathematical growth rates of algorithms, upper and lower bounds, and worst vs average case time complexities.",
        "why_learn_it": "Determines whether an algorithm can scale to 10 million users in 15 milliseconds or crash the server after 4 days of CPU thrashing.",
        "fundamental_explanation": "Asymptotic analysis measures algorithm efficiency as input size n approaches infinity, discarding hardware discrepancies and clock-rate variance.",
        "core_theory": "### Complexity Classes\n- **O(1):** Constant time (array index access, hash map lookup).\n- **O(log n):** Logarithmic time (binary search, balanced tree traversal).\n- **O(n):** Linear time (single pass through array).\n- **O(n log n):** Linearithmic (MergeSort, QuickSort, HeapSort).\n- **O(n²):** Quadratic (nested loops, BubbleSort).\n- **O(2ⁿ):** Exponential (brute force subsets, recursive Fibonacci).",
        "time_complexity": "Theoretical Analysis: O(1)",
        "space_complexity": "Auxiliary vs Total: O(1)",
        "video_url": "https://www.youtube.com/embed/D6xkbGLQesk",
        "video_title": "Big O Notation in 15 Minutes",
        "visualization_type": "searching",
        "visualization_algorithm": "binary_search",
        "practice_problem_slug": "two-sum",
        "java_code": """// O(n) Time Complexity Demo
public class BigODemo {
    public static int linearSum(int[] arr) {
        int sum = 0;
        for (int x : arr) sum += x; // Executes exactly n times
        return sum;
    }
}""",
        "python_code": """# O(log n) Halving Loop
def log_steps(n: int) -> int:
    steps = 0
    while n > 1:
        n //= 2
        steps += 1
    return steps"""
    },

    # -------------------------------------------------------------
    # 2. Arrays
    # -------------------------------------------------------------
    {
        "id": "concept_array_fundamentals",
        "category": "Arrays",
        "difficulty": "Beginner",
        "title": "Array Fundamentals: Contiguity & O(1) Indexing",
        "prerequisites": "Memory Allocation",
        "summary": "Explore contiguous sequential memory, cache line localization, insertion shifts, and dynamic array resizing amortized analysis.",
        "why_learn_it": "Arrays are the foundation of matrices, hash table buckets, priority queues, and strings.",
        "fundamental_explanation": "An array stores fixed-size elements in continuous memory cells. The CPU computes `Address = Base + index * element_size` in a single CPU cycle.",
        "core_theory": "### Contiguous Memory & CPU Cache Lines\nBecause array items sit adjacent in RAM, modern CPUs fetch entire 64-byte cache lines at once, making sequential array traversal significantly faster than pointer-chasing structures.",
        "time_complexity": "Index: O(1) · Search: O(n) · Insert/Delete: O(n)",
        "space_complexity": "O(n) continuous space",
        "video_url": "https://www.youtube.com/embed/7m1Gekj_n0k",
        "video_title": "Arrays & Dynamic Resizing Visualized",
        "visualization_type": "sorting",
        "visualization_algorithm": "bubble_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """public class ArrayOps {
    public static void main(String[] args) {
        int[] arr = new int[]{10, 20, 30, 40};
        System.out.println("O(1) access: " + arr[2]); // 30
    }
}""",
        "python_code": """# Dynamic array doubling in Python
arr = []
for i in range(5):
    arr.append(i)
print(f"Array items: {arr}")"""
    },
    {
        "id": "concept_array_kadane",
        "category": "Arrays",
        "difficulty": "Intermediate",
        "title": "Kadane's Algorithm: Maximum Subarray Sum",
        "prerequisites": "Array Fundamentals",
        "summary": "Find the maximum sum contiguous subarray in O(n) single pass by resetting negative running sums.",
        "why_learn_it": "Replaces O(n³) and O(n²) brute-force approaches with an optimal linear single-pass dynamic accumulator.",
        "fundamental_explanation": "At each index i, we decide whether to extend the previous subarray sum (`current_sum + arr[i]`) or start a brand new subarray starting at `arr[i]`.",
        "core_theory": "### Dynamic Choice\n`current_sum = max(arr[i], current_sum + arr[i])`\n`max_so_far = max(max_so_far, current_sum)`",
        "time_complexity": "Time: O(n) single pass · Space: O(1)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/86CQq33Z468",
        "video_title": "Kadane's Algorithm Maximum Subarray Explained",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class Kadane {
    public static int maxSubArray(int[] nums) {
        int maxSoFar = nums[0], curr = nums[0];
        for (int i = 1; i < nums.length; i++) {
            curr = Math.max(nums[i], curr + nums[i]);
            maxSoFar = Math.max(maxSoFar, curr);
        }
        return maxSoFar;
    }
}""",
        "python_code": """def max_sub_array(nums: list[int]) -> int:
    max_so_far = curr = nums[0]
    for x in nums[1:]:
        curr = max(x, curr + x)
        max_so_far = max(max_so_far, curr)
    return max_so_far"""
    },
    {
        "id": "concept_array_dutch_flag",
        "category": "Arrays",
        "difficulty": "Intermediate",
        "title": "Dutch National Flag Algorithm (3-Way Partitioning)",
        "prerequisites": "Array Fundamentals, Two Pointers",
        "summary": "Sort an array containing three distinct elements (0s, 1s, and 2s) in-place in a single O(n) pass using 3 pointers.",
        "why_learn_it": "Used in 3-way QuickSort (Hoare / Bentley-McIlroy) to handle arrays with duplicate keys efficiently in O(n) time.",
        "fundamental_explanation": "Maintains 3 pointers: `low` (boundary of 0s), `mid` (current scanner), and `high` (boundary of 2s). Swaps elements into their respective zones in a single pass.",
        "core_theory": "### Invariants:\n- `arr[0..low-1]` = 0\n- `arr[low..mid-1]` = 1\n- `arr[mid..high]` = Unknown\n- `arr[high+1..n-1]` = 2",
        "time_complexity": "Time: O(n) one-pass · Space: O(1)",
        "space_complexity": "O(1) in-place",
        "video_url": "https://www.youtube.com/embed/oaVa-9wmpns",
        "video_title": "Sort Colors Dutch National Flag Algorithm",
        "visualization_type": "sorting",
        "visualization_algorithm": "selection_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """public class DutchFlag {
    public static void sortColors(int[] nums) {
        int low = 0, mid = 0, high = nums.length - 1;
        while (mid <= high) {
            if (nums[mid] == 0) {
                int temp = nums[low]; nums[low] = nums[mid]; nums[mid] = temp;
                low++; mid++;
            } else if (nums[mid] == 1) {
                mid++;
            } else {
                int temp = nums[high]; nums[high] = nums[mid]; nums[mid] = temp;
                high--;
            }
        }
    }
}""",
        "python_code": """def sort_colors(nums: list[int]) -> None:
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1; mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[high], nums[mid] = nums[mid], nums[high]
            high -= 1"""
    },
    {
        "id": "concept_array_trapping_rain_water",
        "category": "Arrays",
        "difficulty": "Advanced",
        "title": "Trapping Rain Water: Two Pointers & Monotonic Scan",
        "prerequisites": "Two Pointers, Arrays",
        "summary": "Calculate trapped surface water volume above elevation maps using two convergent pointers bounding max heights.",
        "why_learn_it": "One of the most famous FAANG interview benchmark problems evaluating optimal geometric array traversal.",
        "fundamental_explanation": "Water above bar i is bounded by `min(max_left, max_right) - height[i]`. Using two inward pointers, the smaller boundary determines the trapped water without needing two passes.",
        "core_theory": "### Two Pointer Invariant\nIf `height[left] < height[right]`, water level at left is governed by `left_max` because `right_max` is guaranteed to be at least as tall as `height[right]`.",
        "time_complexity": "Time: O(n) · Space: O(1)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/ZI2z5pq0TqA",
        "video_title": "Trapping Rain Water Visualized",
        "visualization_type": "sorting",
        "visualization_algorithm": "selection_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """public class RainWater {
    public static int trap(int[] height) {
        int left = 0, right = height.length - 1;
        int leftMax = 0, rightMax = 0, total = 0;
        while (left < right) {
            if (height[left] < height[right]) {
                if (height[left] >= leftMax) leftMax = height[left];
                else total += leftMax - height[left];
                left++;
            } else {
                if (height[right] >= rightMax) rightMax = height[right];
                else total += rightMax - height[right];
                right--;
            }
        }
        return total;
    }
}""",
        "python_code": """def trap_rain_water(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max = right_max = water = 0
    while left < right:
        if height[left] < height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1
    return water"""
    },

    # -------------------------------------------------------------
    # 3. Two-Dimensional Arrays and Matrices
    # -------------------------------------------------------------
    {
        "id": "concept_matrix_spiral_traversal",
        "category": "Two-Dimensional Arrays and Matrices",
        "difficulty": "Intermediate",
        "title": "Spiral Matrix & Boundary Layer Traversal",
        "prerequisites": "Arrays & 2D Grids",
        "summary": "Traverse an M x N matrix in clockwise spiral order by contracting four boundary pointers (top, bottom, left, right).",
        "why_learn_it": "Core technique in computer vision, image processing convolutions, raster graphics, and game board generation.",
        "fundamental_explanation": "Initialize four boundaries: top=0, bottom=rows-1, left=0, right=cols-1. Traverse top row, right column, bottom row, and left column, incrementing and decrementing boundaries.",
        "core_theory": "### Boundary Contraction\nAfter scanning top row: `top++`. After right column: `right--`. Check `top <= bottom` and `left <= right` before scanning reverse directions.",
        "time_complexity": "Time: O(M * N) visits every cell once · Space: O(1)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/BJnMZNwUk1M",
        "video_title": "Spiral Matrix Traversal Step by Step",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class SpiralMatrix {
    public static List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> res = new ArrayList<>();
        int top = 0, bottom = matrix.length - 1;
        int left = 0, right = matrix[0].length - 1;
        while (top <= bottom && left <= right) {
            for (int j = left; j <= right; j++) res.add(matrix[top][j]);
            top++;
            for (int i = top; i <= bottom; i++) res.add(matrix[i][right]);
            right--;
            if (top <= bottom) {
                for (int j = right; j >= left; j--) res.add(matrix[bottom][j]);
                bottom--;
            }
            if (left <= right) {
                for (int i = bottom; i >= top; i--) res.add(matrix[i][left]);
                left++;
            }
        }
        return res;
    }
}""",
        "python_code": """def spiral_order(matrix: list[list[int]]) -> list[int]:
    res = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1): res.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1): res.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1): res.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1): res.append(matrix[r][left])
            left += 1
    return res"""
    },

    # -------------------------------------------------------------
    # 4. Strings
    # -------------------------------------------------------------
    {
        "id": "concept_string_kmp_algorithm",
        "category": "Strings",
        "difficulty": "Advanced",
        "title": "Knuth-Morris-Pratt (KMP) Substring Pattern Search",
        "prerequisites": "String Fundamentals, Prefix Arrays",
        "summary": "Search for pattern P in text T in O(N + M) linear time using the Longest Proper Prefix which is also Suffix (LPS) array.",
        "why_learn_it": "Standard brute-force substring matching takes O(N * M). KMP skips redundant comparisons, powering text editors and grep search tools.",
        "fundamental_explanation": "When a mismatch occurs, the LPS array tells us how many characters in the pattern can be preserved without resetting the text pointer backwards.",
        "core_theory": "### The LPS Array (π table)\n`lps[i]` holds the length of the longest proper prefix of `P[0..i]` that is also a suffix of `P[0..i]`. On mismatch, set `j = lps[j - 1]` instead of `j = 0`.",
        "time_complexity": "Time: O(N + M) · Space: O(M) for LPS array",
        "space_complexity": "O(M) for pattern preprocessing",
        "video_url": "https://www.youtube.com/embed/V5-7GzOfADQ",
        "video_title": "KMP Substring Search Algorithm Explained",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "valid-anagram",
        "java_code": """public class KMP {
    public static int strStr(String text, String pattern) {
        if (pattern.isEmpty()) return 0;
        int[] lps = computeLPS(pattern);
        int i = 0, j = 0;
        while (i < text.length()) {
            if (text.charAt(i) == pattern.charAt(j)) { i++; j++; }
            if (j == pattern.length()) return i - j;
            else if (i < text.length() && text.charAt(i) != pattern.charAt(j)) {
                if (j != 0) j = lps[j - 1];
                else i++;
            }
        }
        return -1;
    }
    private static int[] computeLPS(String pat) {
        int[] lps = new int[pat.length()];
        int len = 0, i = 1;
        while (i < pat.length()) {
            if (pat.charAt(i) == pat.charAt(len)) { len++; lps[i++] = len; }
            else {
                if (len != 0) len = lps[len - 1];
                else lps[i++] = 0;
            }
        }
        return lps;
    }
}""",
        "python_code": """def kmp_search(text: str, pattern: str) -> int:
    if not pattern: return 0
    lps = [0] * len(pattern)
    length, i = 0, 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1; lps[i] = length; i += 1
        else:
            if length != 0: length = lps[length - 1]
            else: lps[i] = 0; i += 1
            
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1; j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and text[i] != pattern[j]:
            if j != 0: j = lps[j - 1]
            else: i += 1
    return -1"""
    },

    # -------------------------------------------------------------
    # 5. Searching Algorithms
    # -------------------------------------------------------------
    {
        "id": "concept_search_bs_on_answer",
        "category": "Searching Algorithms",
        "difficulty": "Advanced",
        "title": "Binary Search on Answer (Monotonic Predicates)",
        "prerequisites": "Binary Search, Invariants",
        "summary": "Apply binary search over the range of possible answers when a feasibility condition f(x) is monotonic (False False ... True True).",
        "why_learn_it": "Powers problems like Koko Eating Bananas, Capacity to Ship Packages Within D Days, and aggressive cows problem.",
        "fundamental_explanation": "When searching for an optimal minimum/maximum value x, if testing whether x is valid takes O(n) and the answer space is monotonic, we binary search x in O(n log(MaxRange)).",
        "core_theory": "### Feasibility Predicate Invariant\nIf a speed `k` is fast enough to finish within H hours, all speeds `> k` are also fast enough. The search space has structure `[F, F, F, T, T, T]`. We search for the first `True`.",
        "time_complexity": "Time: O(N * log(Range)) · Space: O(1)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/qyfekrNni90",
        "video_title": "Binary Search on Answer Masterclass",
        "visualization_type": "searching",
        "visualization_algorithm": "binary_search",
        "practice_problem_slug": "binary-search",
        "java_code": """public class KokoBananas {
    public static int minEatingSpeed(int[] piles, int h) {
        int left = 1, right = 1_000_000_000;
        int ans = right;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (canFinish(piles, h, mid)) {
                ans = mid;
                right = mid - 1; // Try smaller speed
            } else {
                left = mid + 1; // Must go faster
            }
        }
        return ans;
    }
    private static boolean canFinish(int[] piles, int h, int k) {
        long hours = 0;
        for (int p : piles) hours += (p + k - 1) / k;
        return hours <= h;
    }
}""",
        "python_code": """def min_eating_speed(piles: list[int], h: int) -> int:
    left, right = 1, max(piles)
    ans = right
    while left <= right:
        mid = (left + right) // 2
        hours = sum((p + mid - 1) // mid for p in piles)
        if hours <= h:
            ans = mid
            right = mid - 1 # Try slower speed
        else:
            left = mid + 1 # Must eat faster
    return ans"""
    },

    # -------------------------------------------------------------
    # 6. Sorting Algorithms
    # -------------------------------------------------------------
    {
        "id": "concept_sort_heap_sort",
        "category": "Sorting Algorithms",
        "difficulty": "Intermediate",
        "title": "Heap Sort: In-Place O(n log n) Comparison Sort",
        "prerequisites": "Complete Binary Trees, Heaps",
        "summary": "Build a Max-Heap in O(n) time, then repeatedly swap root with the last element and heapify downward to sort in-place.",
        "why_learn_it": "Guarantees O(n log n) worst-case time without requiring O(n) auxiliary memory like MergeSort, and without O(n²) worst-case like QuickSort.",
        "fundamental_explanation": "Transform the array into a Max-Heap where parent >= children. Then swap root (maximum) to the end of array, reduce heap size by 1, and sift-down root.",
        "core_theory": "### HeapSort Mechanics\n1. `buildMaxHeap`: runs in O(n) from n/2 down to 0.\n2. n extractions: each sift-down takes O(log n).\n3. Total time: O(n log n) with strict O(1) extra space.",
        "time_complexity": "Time: Guaranteed O(n log n) across all cases · Space: O(1) in-place",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/2DmK_H7IdTo",
        "video_title": "Heap Sort Algorithm Visualized",
        "visualization_type": "sorting",
        "visualization_algorithm": "merge_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """public class HeapSort {
    public static void sort(int[] arr) {
        int n = arr.length;
        for (int i = n / 2 - 1; i >= 0; i--) heapify(arr, n, i);
        for (int i = n - 1; i > 0; i--) {
            int temp = arr[0]; arr[0] = arr[i]; arr[i] = temp;
            heapify(arr, i, 0);
        }
    }
    private static void heapify(int[] arr, int n, int i) {
        int largest = i, l = 2 * i + 1, r = 2 * i + 2;
        if (l < n && arr[l] > arr[largest]) largest = l;
        if (r < n && arr[r] > arr[largest]) largest = r;
        if (largest != i) {
            int swap = arr[i]; arr[i] = arr[largest]; arr[largest] = swap;
            heapify(arr, n, largest);
        }
    }
}""",
        "python_code": """def heap_sort(arr: list[int]) -> list[int]:
    n = len(arr)
    def heapify(size, root):
        largest = root
        l, r = 2 * root + 1, 2 * root + 2
        if l < size and arr[l] > arr[largest]: largest = l
        if r < size and arr[r] > arr[largest]: largest = r
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            heapify(size, largest)
            
    for i in range(n // 2 - 1, -1, -1): heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(i, 0)
    return arr"""
    },

    # -------------------------------------------------------------
    # 7. Two Pointers and Sliding Window
    # -------------------------------------------------------------
    {
        "id": "concept_twopointers_3sum",
        "category": "Two Pointers and Sliding Window",
        "difficulty": "Intermediate",
        "title": "3Sum: Triplet Sum to Zero with Duplicate Skipping",
        "prerequisites": "Two Pointers, Sorting",
        "summary": "Sort array and fix one element i, then use converging two pointers to find pairs summing to -arr[i] in O(n²) time.",
        "why_learn_it": "Tests master-level pointer convergence and duplicate avoidance in interview coding assessments.",
        "fundamental_explanation": "For each distinct element at index i, run Two Sum II on the sub-array `arr[i+1..n-1]` with target `-arr[i]`. Skip adjacent duplicates to ensure unique triplets.",
        "core_theory": "### Invariant & Duplicate Handling\nIf `i > 0 && arr[i] == arr[i - 1]`, skip iteration. Inside the two-pointer loop, after finding a match, advance left past all identical elements and right past all identical elements.",
        "time_complexity": "Time: O(n²) · Space: O(1) auxiliary (or O(n) for sort buffer)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/jzZsG8n2R9A",
        "video_title": "3Sum Problem Visualized",
        "visualization_type": "sorting",
        "visualization_algorithm": "selection_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class ThreeSumProblem {
    public static List<List<Integer>> threeSum(int[] nums) {
        Arrays.sort(nums);
        List<List<Integer>> res = new ArrayList<>();
        for (int i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] == nums[i - 1]) continue; // Skip duplicate i
            int l = i + 1, r = nums.length - 1;
            while (l < r) {
                int sum = nums[i] + nums[l] + nums[r];
                if (sum == 0) {
                    res.add(Arrays.asList(nums[i], nums[l], nums[r]));
                    while (l < r && nums[l] == nums[l + 1]) l++;
                    while (l < r && nums[r] == nums[r - 1]) r--;
                    l++; r--;
                } else if (sum < 0) l++;
                else r--;
            }
        }
        return res;
    }
}""",
        "python_code": """def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]: continue
        l, r = i + 1, len(nums) - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                res.append([nums[i], nums[l], nums[r]])
                while l < r and nums[l] == nums[l + 1]: l += 1
                while l < r and nums[r] == nums[r - 1]: r -= 1
                l += 1; r -= 1
            elif s < 0: l += 1
            else: r -= 1
    return res"""
    },

    # -------------------------------------------------------------
    # 8. Prefix Sum and Difference Arrays
    # -------------------------------------------------------------
    {
        "id": "concept_prefix_sum_fundamentals",
        "category": "Prefix Sum and Difference Arrays",
        "difficulty": "Beginner",
        "title": "1D & 2D Prefix Sums: Constant Time Range Queries",
        "prerequisites": "Arrays",
        "summary": "Precompute cumulative sums to answer any subarray sum query in O(1) constant time instead of O(n) linear scans.",
        "why_learn_it": "Used in financial moving averages, image box blur filters (integral image), and database range analytics.",
        "fundamental_explanation": "`prefix[i] = prefix[i - 1] + arr[i]`. The sum of subarray from index L to R is computed as: `Sum(L..R) = prefix[R] - prefix[L - 1]`.",
        "core_theory": "### 2D Matrix Prefix Sum\n`prefix[r][c] = matrix[r][c] + prefix[r-1][c] + prefix[r][c-1] - prefix[r-1][c-1]`. Any rectangular subgrid sum is answered in O(1) using the Principle of Inclusion-Exclusion.",
        "time_complexity": "Precompute: O(n) · Query: O(1)",
        "space_complexity": "O(n) auxiliary array",
        "video_url": "https://www.youtube.com/embed/pVS3yhlzrlQ",
        "video_title": "Prefix Sum Technique Explained",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class PrefixArray {
    private int[] prefix;
    public PrefixArray(int[] nums) {
        prefix = new int[nums.length + 1];
        for (int i = 0; i < nums.length; i++) prefix[i + 1] = prefix[i] + nums[i];
    }
    public int sumRange(int left, int right) {
        return prefix[right + 1] - prefix[left]; // O(1) query
    }
}""",
        "python_code": """class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0]
        for x in nums: self.prefix.append(self.prefix[-1] + x)
        
    def sum_range(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]"""
    },

    # -------------------------------------------------------------
    # 9. Linked Lists
    # -------------------------------------------------------------
    {
        "id": "concept_ll_lru_cache",
        "category": "Linked Lists",
        "difficulty": "Advanced",
        "title": "LRU Cache: Doubly Linked List + Hash Map",
        "prerequisites": "Linked Lists, Hashing",
        "summary": "Design a Least Recently Used (LRU) Cache supporting get(key) and put(key, value) operations in strict O(1) average time.",
        "why_learn_it": "The definitive memory eviction policy in operating systems, Redis, Memcached, web browsers, and CPU L1/L2 caches.",
        "fundamental_explanation": "A HashMap provides O(1) lookup to nodes. A Doubly Linked List maintains access recency with O(1) node relocation to the head and O(1) tail eviction.",
        "core_theory": "### Data Structure Synergy\n- `Map<Integer, Node>` maps key -> DLL Node.\n- `Node` has `prev`, `next`, `key`, `value`.\n- Sentinel `head` and `tail` dummy nodes eliminate null pointer edge cases during node detach and re-insertion.",
        "time_complexity": "get(): O(1) · put(): O(1)",
        "space_complexity": "O(Capacity) memory",
        "video_url": "https://www.youtube.com/embed/7ABFKPK2hD4",
        "video_title": "LRU Cache Design and Implementation",
        "visualization_type": "linked_list",
        "visualization_algorithm": "linked_list",
        "practice_problem_slug": "reverse-linked-list",
        "java_code": """import java.util.*;
public class LRUCache {
    class Node { int k, v; Node prev, next; Node(int k, int v){this.k=k; this.v=v;} }
    private Map<Integer, Node> map = new HashMap<>();
    private int cap;
    private Node head = new Node(0, 0), tail = new Node(0, 0);
    public LRUCache(int capacity) {
        this.cap = capacity; head.next = tail; tail.prev = head;
    }
    public int get(int key) {
        if (!map.containsKey(key)) return -1;
        Node n = map.get(key); remove(n); insertToHead(n); return n.v;
    }
    public void put(int key, int value) {
        if (map.containsKey(key)) remove(map.get(key));
        if (map.size() == cap) { map.remove(tail.prev.k); remove(tail.prev); }
        Node n = new Node(key, value); map.put(key, n); insertToHead(n);
    }
    private void remove(Node n) { n.prev.next = n.next; n.next.prev = n.prev; }
    private void insertToHead(Node n) { n.next = head.next; n.prev = head; head.next.prev = n; head.next = n; }
}""",
        "python_code": """from collections import OrderedDict
class LRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.cache = OrderedDict()
    def get(self, key: int) -> int:
        if key not in self.cache: return -1
        self.cache.move_to_end(key)
        return self.cache[key]
    def put(self, key: int, value: int) -> None:
        if key in self.cache: self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.cap: self.cache.popitem(last=False)"""
    },

    # -------------------------------------------------------------
    # 10. Stack
    # -------------------------------------------------------------
    {
        "id": "concept_stack_histogram",
        "category": "Stack",
        "difficulty": "Advanced",
        "title": "Largest Rectangle in Histogram (Monotonic Stack)",
        "prerequisites": "Stack Fundamentals, Monotonic Stack",
        "summary": "Find the maximum rectangular area formed by histogram bars in O(n) linear time using a monotonic increasing stack.",
        "why_learn_it": "The cornerstone algorithmic step for solving 2D Maximal Rectangle, Daily Temperatures, and trapped water variants.",
        "fundamental_explanation": "For each bar, its maximum rectangle height is bounded by the first smaller bar to its left and the first smaller bar to its right.",
        "core_theory": "### Stack Invariant\nMaintain indices of bars with increasing heights. When a bar of smaller height arrives, pop bars from the stack and compute rectangle area with the popped bar as the minimum height.",
        "time_complexity": "Time: O(n) each bar pushed and popped once · Space: O(n)",
        "space_complexity": "O(n) auxiliary stack",
        "video_url": "https://www.youtube.com/embed/zx5Sw9x30A8",
        "video_title": "Largest Rectangle in Histogram Visualized",
        "visualization_type": "stack_queue",
        "visualization_algorithm": "stack_queue",
        "practice_problem_slug": "valid-parentheses",
        "java_code": """import java.util.*;
public class HistogramMax {
    public static int largestRectangleArea(int[] heights) {
        Deque<Integer> stack = new ArrayDeque<>();
        int maxArea = 0, n = heights.length;
        for (int i = 0; i <= n; i++) {
            int h = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && heights[stack.peek()] > h) {
                int height = heights[stack.pop()];
                int width = stack.isEmpty() ? i : i - stack.peek() - 1;
                maxArea = Math.max(maxArea, height * width);
            }
            stack.push(i);
        }
        return maxArea;
    }
}""",
        "python_code": """def largest_rectangle_area(heights: list[int]) -> int:
    stack = []
    max_area = 0
    heights.append(0)
    for i, h in enumerate(heights):
        while stack and heights[stack[-1]] > h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return max_area"""
    },

    # -------------------------------------------------------------
    # 11. Queue and Deque
    # -------------------------------------------------------------
    {
        "id": "concept_queue_monotonic_sliding_window",
        "category": "Queue and Deque",
        "difficulty": "Advanced",
        "title": "Sliding Window Maximum (Monotonic Deque)",
        "prerequisites": "Queue Fundamentals, Deque",
        "summary": "Find the maximum element in every sliding window of size k in O(n) total time using a monotonically decreasing double-ended queue.",
        "why_learn_it": "Standard priority queue takes O(n log k). A Monotonic Deque drops runtime to optimal O(n) linear time.",
        "fundamental_explanation": "Store indices in a deque such that elements are in strictly decreasing order. The front of the deque is always the maximum element of the current window.",
        "core_theory": "### Deque Pruning\n1. Evict elements older than `i - k + 1` from the front.\n2. Remove smaller elements from the back before inserting `arr[i]` because they can never be the maximum again.",
        "time_complexity": "Time: O(n) each element enqueued and dequeued once · Space: O(k)",
        "space_complexity": "O(k) auxiliary deque",
        "video_url": "https://www.youtube.com/embed/DfljaUwZsOk",
        "video_title": "Sliding Window Maximum Monotonic Deque",
        "visualization_type": "stack_queue",
        "visualization_algorithm": "stack_queue",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class SlidingWindowMax {
    public static int[] maxSlidingWindow(int[] nums, int k) {
        int n = nums.length;
        int[] res = new int[n - k + 1];
        Deque<Integer> q = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            if (!q.isEmpty() && q.peekFirst() <= i - k) q.pollFirst();
            while (!q.isEmpty() && nums[q.peekLast()] < nums[i]) q.pollLast();
            q.offerLast(i);
            if (i >= k - 1) res[i - k + 1] = nums[q.peekFirst()];
        }
        return res;
    }
}""",
        "python_code": """from collections import deque
def max_sliding_window(nums: list[int], k: int) -> list[int]:
    q = deque()
    res = []
    for i, x in enumerate(nums):
        if q and q[0] <= i - k: q.popleft()
        while q and nums[q[-1]] < x: q.pop()
        q.append(i)
        if i >= k - 1: res.append(nums[q[0]])
    return res"""
    },

    # -------------------------------------------------------------
    # 12. Hashing
    # -------------------------------------------------------------
    {
        "id": "concept_hash_collision_handling",
        "category": "Hashing",
        "difficulty": "Intermediate",
        "title": "Hash Table Internals: Separate Chaining vs Open Addressing",
        "prerequisites": "Arrays, Linked Lists",
        "summary": "Deep dive into hash functions, uniform distribution, load factors, collision resolution, and red-black tree bucket conversion.",
        "why_learn_it": "Explains why Java 8 converted heavy LinkedList buckets to Red-Black Trees (Treeify) to protect against hash collision Denial of Service (DoS) attacks.",
        "fundamental_explanation": "When two distinct keys produce identical hash indices, Separate Chaining stores colliding entries in a linked list, while Open Addressing probes adjacent slots.",
        "core_theory": "### Load Factor & Treeification\nWhen the load factor exceeds 0.75, the table doubles capacity. In Java, when a bucket contains >8 collisions, it converts from a linked list O(k) into a Red-Black Tree O(log k).",
        "time_complexity": "Average: O(1) · Worst Case: O(log k) treeified",
        "space_complexity": "O(n) auxiliary",
        "video_url": "https://www.youtube.com/embed/shs0KM3wKv8",
        "video_title": "Hash Table Collisions & Resizing",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class HashInternals {
    public static void main(String[] args) {
        Map<String, Integer> map = new HashMap<>(16, 0.75f);
        map.put("AlgoMentor", 100);
        System.out.println("O(1) get: " + map.get("AlgoMentor"));
    }
}""",
        "python_code": """# Python dict collision resolution uses open addressing with perturbation
d = {}
d["key"] = 42
print(d.get("key"))"""
    },

    # -------------------------------------------------------------
    # 13. Recursion and Backtracking
    # -------------------------------------------------------------
    {
        "id": "concept_backtrack_n_queens",
        "category": "Recursion and Backtracking",
        "difficulty": "Advanced",
        "title": "N-Queens Puzzle: Diagonal Pruning & State Space Search",
        "prerequisites": "Recursion Fundamentals, Call Stack",
        "summary": "Place N non-attacking queens on an N x N chessboard using recursive backtracking with O(1) diagonal collision lookup sets.",
        "why_learn_it": "The definitive classic benchmark for recursive search, pruning, and state restoration in computer science.",
        "fundamental_explanation": "Place queens row by row. For each column in row r, check if placing a queen attacks any previously placed queen along columns, positive diagonals (r + c), or negative diagonals (r - c).",
        "core_theory": "### Mathematical Diagonal Invariants:\n- Major Diagonal (↘): `r - c = constant`.\n- Minor Diagonal (↙): `r + c = constant`.\nChecking boolean sets for columns and diagonals makes feasibility checks O(1) instead of scanning the whole board.",
        "time_complexity": "Time: O(N!) with pruning · Space: O(N) call stack",
        "space_complexity": "O(N) auxiliary tracking arrays",
        "video_url": "https://www.youtube.com/embed/wGbuCyNpxIg",
        "video_title": "N-Queens Backtracking Visualized",
        "visualization_type": "graph",
        "visualization_algorithm": "dfs",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class NQueens {
    public static int totalNQueens(int n) {
        return solve(0, n, new HashSet<>(), new HashSet<>(), new HashSet<>());
    }
    private static int solve(int r, int n, Set<Integer> cols, Set<Integer> diag1, Set<Integer> diag2) {
        if (r == n) return 1;
        int count = 0;
        for (int c = 0; c < n; c++) {
            if (cols.contains(c) || diag1.contains(r - c) || diag2.contains(r + c)) continue;
            cols.add(c); diag1.add(r - c); diag2.add(r + c);
            count += solve(r + 1, n, cols, diag1, diag2);
            cols.remove(c); diag1.remove(r - c); diag2.remove(r + c); // Backtrack
        }
        return count;
    }
}""",
        "python_code": """def total_n_queens(n: int) -> int:
    cols = set()
    pos_diag = set() # (r + c)
    neg_diag = set() # (r - c)
    
    def backtrack(r):
        if r == n: return 1
        res = 0
        for c in range(n):
            if c in cols or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
            cols.add(c); pos_diag.add(r + c); neg_diag.add(r - c)
            res += backtrack(r + 1)
            cols.remove(c); pos_diag.remove(r + c); neg_diag.remove(r - c) # Backtrack
        return res
        
    return backtrack(0)"""
    },

    # -------------------------------------------------------------
    # 14. Trees
    # -------------------------------------------------------------
    {
        "id": "concept_tree_lca",
        "category": "Trees",
        "difficulty": "Intermediate",
        "title": "Lowest Common Ancestor (LCA) in Binary Trees",
        "prerequisites": "Binary Trees, Postorder Traversal",
        "summary": "Find the shared lowest common ancestor node of two given nodes p and q in O(n) time using recursive postorder DFS.",
        "why_learn_it": "Used in Git branch merge-base resolution (finding the common commit where two feature branches diverged) and network routing.",
        "fundamental_explanation": "If the current root matches p or q, return root. Recursively search left and right subtrees. If both return non-null, root is their Lowest Common Ancestor!",
        "core_theory": "### Postorder Bottom-Up Aggregation\n- Left returned non-null & Right returned non-null ➔ Current node is LCA!\n- Only Left returned non-null ➔ Both p and q are in the left subtree.\n- Only Right returned non-null ➔ Both p and q are in the right subtree.",
        "time_complexity": "Time: O(n) visits each node once · Space: O(height)",
        "space_complexity": "O(h) call stack memory",
        "video_url": "https://www.youtube.com/embed/WO174n_Lw1g",
        "video_title": "Lowest Common Ancestor in Binary Tree Visualized",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """class TreeNode { int val; TreeNode left, right; TreeNode(int v){val = v;} }
public class LCAProblem {
    public static TreeNode lowestCommonAncestor(TreeNode root, TreeNode p, TreeNode q) {
        if (root == null || root == p || root == q) return root;
        TreeNode left = lowestCommonAncestor(root.left, p, q);
        TreeNode right = lowestCommonAncestor(root.right, p, q);
        if (left != null && right != null) return root;
        return (left != null) ? left : right;
    }
}""",
        "python_code": """def lowest_common_ancestor(root, p, q):
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right"""
    },

    # -------------------------------------------------------------
    # 15. Binary Search Trees
    # -------------------------------------------------------------
    {
        "id": "concept_bst_deletion",
        "category": "Binary Search Trees",
        "difficulty": "Intermediate",
        "title": "BST Deletion & Inorder Successor Replacement",
        "prerequisites": "BST Fundamentals, Inorder Traversal",
        "summary": "Safely delete nodes with 0, 1, or 2 children while preserving the strict BST invariant using inorder successors.",
        "why_learn_it": "Critical operation in database B-Trees, relational primary key index deletions, and balanced search trees.",
        "fundamental_explanation": "If node has 0 children: delete immediately. If 1 child: replace with child. If 2 children: replace node's value with its Inorder Successor (minimum node in its right subtree) and delete that successor.",
        "core_theory": "### Three Deletion Cases\n1. **Leaf:** `return null`.\n2. **One Child:** `return (node.left != null) ? node.left : node.right`.\n3. **Two Children:** `succ = findMin(node.right); node.val = succ.val; node.right = delete(node.right, succ.val)`.",
        "time_complexity": "Balanced: O(log n) · Degenerate: O(n)",
        "space_complexity": "O(height) recursion call stack",
        "video_url": "https://www.youtube.com/embed/petKFUZ5cSE",
        "video_title": "Delete a Node in a BST Step by Step",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """public class BSTDelete {
    public static TreeNode deleteNode(TreeNode root, int key) {
        if (root == null) return null;
        if (key < root.val) root.left = deleteNode(root.left, key);
        else if (key > root.val) root.right = deleteNode(root.right, key);
        else {
            if (root.left == null) return root.right;
            if (root.right == null) return root.left;
            TreeNode succ = root.right;
            while (succ.left != null) succ = succ.left;
            root.val = succ.val;
            root.right = deleteNode(root.right, succ.val);
        }
        return root;
    }
}""",
        "python_code": """def delete_node(root, key):
    if not root: return None
    if key < root.val: root.left = delete_node(root.left, key)
    elif key > root.val: root.right = delete_node(root.right, key)
    else:
        if not root.left: return root.right
        if not root.right: return root.left
        succ = root.right
        while succ.left: succ = succ.left
        root.val = succ.val
        root.right = delete_node(root.right, succ.val)
    return root"""
    },

    # -------------------------------------------------------------
    # 16. Heaps and Priority Queues
    # -------------------------------------------------------------
    {
        "id": "concept_heap_running_median",
        "category": "Heaps and Priority Queues",
        "difficulty": "Advanced",
        "title": "Find Median from Data Stream (Two Heaps Technique)",
        "prerequisites": "Min-Heap, Max-Heap",
        "summary": "Maintain running median of live incoming streaming numbers in O(1) query time using a Max-Heap for the lower half and Min-Heap for upper half.",
        "why_learn_it": "Used in financial stock market trade pricing, telemetry streaming quantile estimators, and real-time monitoring.",
        "fundamental_explanation": "Split data into two halves: Max-Heap stores smaller numbers, Min-Heap stores larger numbers. Balance sizes so they differ by at most 1 element.",
        "core_theory": "### Invariant Balance\n`max_heap.size() == min_heap.size()` or `max_heap.size() == min_heap.size() + 1`.\nMedian is `max_heap.peek()` if odd, or average of both roots if even.",
        "time_complexity": "addNum: O(log n) · findMedian: O(1)",
        "space_complexity": "O(n) heap capacity",
        "video_url": "https://www.youtube.com/embed/itmhHWaHupI",
        "video_title": "Find Median from Data Stream Two Heaps",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class MedianFinder {
    private PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
    private PriorityQueue<Integer> minHeap = new PriorityQueue<>();
    public void addNum(int num) {
        maxHeap.offer(num);
        minHeap.offer(maxHeap.poll());
        if (minHeap.size() > maxHeap.size()) maxHeap.offer(minHeap.poll());
    }
    public double findMedian() {
        if (maxHeap.size() > minHeap.size()) return maxHeap.peek();
        return (maxHeap.peek() + minHeap.peek()) / 2.0;
    }
}""",
        "python_code": """import heapq
class MedianFinder:
    def __init__(self):
        self.small = [] # max heap (invert sign)
        self.large = [] # min heap
    def add_num(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))
        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))
    def find_median(self) -> float:
        if len(self.small) > len(self.large): return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0"""
    },

    # -------------------------------------------------------------
    # 17. Tries
    # -------------------------------------------------------------
    {
        "id": "concept_trie_prefix_tree",
        "category": "Tries",
        "difficulty": "Intermediate",
        "title": "Trie (Prefix Tree): Autocomplete & Prefix Matching",
        "prerequisites": "Trees, Hash Maps",
        "summary": "Store and retrieve keys in digital tree structures where edges represent characters, enabling O(L) search independent of database size.",
        "why_learn_it": "The engine powering search engine autocomplete dropdowns, spell-checkers, IP router longest prefix routing, and T9 predictive typing.",
        "fundamental_explanation": "Each node contains a fixed array or map of children representing alphabet letters and a boolean `is_end_of_word` flag. Common word prefixes share nodes.",
        "core_theory": "### Complexity Independence\nSearching for word of length L takes O(L) steps regardless of whether the dictionary contains 10 words or 100,000,000 words!",
        "time_complexity": "Insert/Search/Prefix: O(L) where L is key length",
        "space_complexity": "O(N * L * AlphabetSize)",
        "video_url": "https://www.youtube.com/embed/o6563IIbQQU",
        "video_title": "Trie Data Structure Implementation",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """public class Trie {
    private class Node {
        Node[] children = new Node[26];
        boolean isEnd = false;
    }
    private Node root = new Node();
    public void insert(String word) {
        Node curr = root;
        for (char c : word.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) curr.children[idx] = new Node();
            curr = curr.children[idx];
        }
        curr.isEnd = true;
    }
    public boolean search(String word) {
        Node n = find(word); return n != null && n.isEnd;
    }
    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }
    private Node find(String s) {
        Node curr = root;
        for (char c : s.toCharArray()) {
            int idx = c - 'a';
            if (curr.children[idx] == null) return null;
            curr = curr.children[idx];
        }
        return curr;
    }
}""",
        "python_code": """class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children: curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_end = True
    def search(self, word: str) -> bool:
        curr = self.root
        for ch in word:
            if ch not in curr.children: return False
            curr = curr.children[ch]
        return curr.is_end
    def starts_with(self, prefix: str) -> bool:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children: return False
            curr = curr.children[ch]
        return True"""
    },

    # -------------------------------------------------------------
    # 18. Graph Algorithms
    # -------------------------------------------------------------
    {
        "id": "concept_graph_topological_sort",
        "category": "Graph Algorithms",
        "difficulty": "Intermediate",
        "title": "Topological Sort & Kahn's Algorithm (DAG Scheduling)",
        "prerequisites": "Graph BFS/DFS, In-Degree",
        "summary": "Linear ordering of vertices in a Directed Acyclic Graph (DAG) such that for every directed edge u -> v, u appears before v.",
        "why_learn_it": "Powers build systems (Make, Maven, Gradle), course prerequisites, package managers (npm, pip), and spreadsheet formula recalculation.",
        "fundamental_explanation": "Kahn's Algorithm calculates in-degrees of all nodes. Enqueue all nodes with in-degree 0 into a BFS queue. When dequeuing, decrement neighbors' in-degrees; if a neighbor reaches 0, enqueue it.",
        "core_theory": "### Cycle Detection via Kahn's Algorithm\nIf the total count of processed nodes is less than total vertices V, the graph contains a directed cycle (deadlock), and no topological ordering exists!",
        "time_complexity": "Time: O(V + E) · Space: O(V + E)",
        "space_complexity": "O(V) in-degree array and queue",
        "video_url": "https://www.youtube.com/embed/cIBFEhD77b4",
        "video_title": "Topological Sort Kahn's Algorithm Visualized",
        "visualization_type": "graph",
        "visualization_algorithm": "bfs",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class TopoSort {
    public static boolean canFinish(int numCourses, int[][] prerequisites) {
        List<List<Integer>> adj = new ArrayList<>();
        int[] inDegree = new int[numCourses];
        for (int i = 0; i < numCourses; i++) adj.add(new ArrayList<>());
        for (int[] p : prerequisites) { adj.get(p[1]).add(p[0]); inDegree[p[0]]++; }
        Queue<Integer> q = new LinkedList<>();
        for (int i = 0; i < numCourses; i++) if (inDegree[i] == 0) q.offer(i);
        int visited = 0;
        while (!q.isEmpty()) {
            int node = q.poll(); visited++;
            for (int neighbor : adj.get(node)) {
                if (--inDegree[neighbor] == 0) q.offer(neighbor);
            }
        }
        return visited == numCourses;
    }
}""",
        "python_code": """from collections import deque
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    adj = {i: [] for i in range(num_courses)}
    in_degree = [0] * num_courses
    for dest, src in prerequisites:
        adj[src].append(dest)
        in_degree[dest] += 1
        
    q = deque([i for i in range(num_courses) if in_degree[i] == 0])
    count = 0
    while q:
        curr = q.popleft()
        count += 1
        for nbr in adj[curr]:
            in_degree[nbr] -= 1
            if in_degree[nbr] == 0: q.append(nbr)
    return count == num_courses"""
    },
    {
        "id": "concept_graph_union_find_dsu",
        "category": "Graph Algorithms",
        "difficulty": "Intermediate",
        "title": "Disjoint Set Union (DSU) with Path Compression",
        "prerequisites": "Graph Fundamentals, Trees",
        "summary": "Track partitioned sets across elements with nearly O(1) amortized find and union operations using inverse Ackermann complexity.",
        "why_learn_it": "The engine of Kruskal's Minimum Spanning Tree algorithm, cycle detection in undirected graphs, and dynamic connectivity in networks.",
        "fundamental_explanation": "Each element points to a parent. Path Compression flattens the tree during `find()`, and Union by Rank attaches smaller trees beneath deeper trees.",
        "core_theory": "### Inverse Ackermann α(N)\nWith both Path Compression and Union by Rank, each operation runs in `O(α(N))` time, which is strictly less than 5 for all practical inputs up to 10⁸⁰ atoms in the universe!",
        "time_complexity": "Find/Union: O(α(N)) ≈ O(1) amortized",
        "space_complexity": "O(N) parent and rank arrays",
        "video_url": "https://www.youtube.com/embed/ayW5B2W9hfo",
        "video_title": "Disjoint Set Union (DSU) Visualized",
        "visualization_type": "graph",
        "visualization_algorithm": "bfs",
        "practice_problem_slug": "two-sum",
        "java_code": """public class DSU {
    int[] parent, rank;
    public DSU(int n) {
        parent = new int[n]; rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;
    }
    public int find(int i) {
        if (parent[i] == i) return i;
        return parent[i] = find(parent[i]); // Path compression
    }
    public boolean union(int i, int j) {
        int rootI = find(i), rootJ = find(j);
        if (rootI == rootJ) return false; // Cycle detected
        if (rank[rootI] < rank[rootJ]) parent[rootI] = rootJ;
        else if (rank[rootI] > rank[rootJ]) parent[rootJ] = rootI;
        else { parent[rootJ] = rootI; rank[rootI]++; }
        return true;
    }
}""",
        "python_code": """class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, i: int) -> int:
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i]) # Path compression
        return self.parent[i]
    def union(self, i: int, j: int) -> bool:
        r1, r2 = self.find(i), self.find(j)
        if r1 == r2: return False
        if self.rank[r1] < self.rank[r2]: self.parent[r1] = r2
        elif self.rank[r1] > self.rank[r2]: self.parent[r2] = r1
        else: self.parent[r2] = r1; self.rank[r1] += 1
        return True"""
    },

    # -------------------------------------------------------------
    # 19. Greedy Algorithms
    # -------------------------------------------------------------
    {
        "id": "concept_greedy_huffman_coding",
        "category": "Greedy Algorithms",
        "difficulty": "Advanced",
        "title": "Huffman Coding & Optimal Prefix Trees",
        "prerequisites": "Min-Heap, Greedy Choice Property",
        "summary": "Lossless data compression algorithm assigning variable-length binary codes based on character frequency using a greedy Min-Heap.",
        "why_learn_it": "Used in JPEG image compression, MP3 audio encoding, GZIP, and PKZIP archive compression formats.",
        "fundamental_explanation": "More frequent characters receive shorter binary codes, while rare characters receive longer binary codes. No code is a prefix of any other code (prefix-free).",
        "core_theory": "### Greedy Tree Construction\nRepeatedly pop the two smallest frequency nodes from a Min-Heap, join them under a new parent whose frequency is their sum, and push the parent back into the heap.",
        "time_complexity": "Time: O(N log N) · Space: O(N)",
        "space_complexity": "O(N) for Huffman Tree nodes",
        "video_url": "https://www.youtube.com/embed/co4_ahEDCho",
        "video_title": "Huffman Coding Algorithm Step by Step",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
class HuffmanNode {
    int freq; char ch; HuffmanNode left, right;
    HuffmanNode(char c, int f) { ch = c; freq = f; }
}
public class HuffmanDemo {
    public static HuffmanNode buildTree(char[] chars, int[] freqs) {
        PriorityQueue<HuffmanNode> pq = new PriorityQueue<>(Comparator.comparingInt(a -> a.freq));
        for (int i = 0; i < chars.length; i++) pq.offer(new HuffmanNode(chars[i], freqs[i]));
        while (pq.size() > 1) {
            HuffmanNode l = pq.poll(), r = pq.poll();
            HuffmanNode parent = new HuffmanNode('-', l.freq + r.freq);
            parent.left = l; parent.right = r;
            pq.offer(parent);
        }
        return pq.poll();
    }
}""",
        "python_code": """import heapq
class Node:
    def __init__(self, ch, freq):
        self.ch, self.freq = ch, freq
        self.left = self.right = None
    def __lt__(self, other): return self.freq < other.freq

def huffman_tree(char_freqs: dict[str, int]):
    pq = [Node(ch, f) for ch, f in char_freqs.items()]
    heapq.heapify(pq)
    while len(pq) > 1:
        l = heapq.heappop(pq)
        r = heapq.heappop(pq)
        parent = Node(None, l.freq + r.freq)
        parent.left, parent.right = l, r
        heapq.heappush(pq, parent)
    return pq[0]"""
    },

    # -------------------------------------------------------------
    # 20. Dynamic Programming
    # -------------------------------------------------------------
    {
        "id": "concept_dp_lcs",
        "category": "Dynamic Programming",
        "difficulty": "Intermediate",
        "title": "Longest Common Subsequence (LCS)",
        "prerequisites": "Recursion, Memoization, 2D Arrays",
        "summary": "Find the length of the longest subsequence present in both strings in O(M * N) using 2D state transitions.",
        "why_learn_it": "The algorithm behind Git diff, file comparison utilities, and DNA bioinformatics sequence alignments (Needleman-Wunsch).",
        "fundamental_explanation": "If `s1[i-1] == s2[j-1]`, extend the matching diagonal: `dp[i][j] = 1 + dp[i-1][j-1]`. Otherwise take `max(dp[i-1][j], dp[i][j-1])`.",
        "core_theory": "### Recurrence Relation\n```text\ndp[i][j] = dp[i-1][j-1] + 1                     if s1[i-1] == s2[j-1]\ndp[i][j] = max(dp[i-1][j], dp[i][j-1])          otherwise\n```",
        "time_complexity": "Time: O(M * N) · Space: O(M * N) or O(min(M, N)) optimized",
        "space_complexity": "O(M * N) 2D DP matrix",
        "video_url": "https://www.youtube.com/embed/ASoaQq66foQ",
        "video_title": "Longest Common Subsequence Visualized",
        "visualization_type": "dp",
        "visualization_algorithm": "fibonacci_dp",
        "practice_problem_slug": "two-sum",
        "java_code": """public class LCS {
    public static int longestCommonSubsequence(String text1, String text2) {
        int m = text1.length(), n = text2.length();
        int[][] dp = new int[m + 1][n + 1];
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (text1.charAt(i - 1) == text2.charAt(j - 1)) {
                    dp[i][j] = 1 + dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        return dp[m][n];
    }
}""",
        "python_code": """def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = 1 + dp[i - 1][j - 1]
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]"""
    },
    {
        "id": "concept_dp_lis",
        "category": "Dynamic Programming",
        "difficulty": "Advanced",
        "title": "Longest Increasing Subsequence: O(n log n) Patience Sorting",
        "prerequisites": "Dynamic Programming, Binary Search",
        "summary": "Find length of the longest strictly increasing subsequence in O(n log n) time using patience sort with binary search lower-bound.",
        "why_learn_it": "Standard 1D DP takes O(n²). The patience sorting technique improves it to O(n log n), solving Russian Doll Envelopes and box stacking.",
        "fundamental_explanation": "Maintain an active tails array where `tails[i]` stores the smallest tail of all increasing subsequences of length `i+1`. Use binary search to find insertion position.",
        "core_theory": "### Patience Sorting Invariant\nFor each number x in array, binary search `tails` for first element >= x. If found, replace it with x (making future extensions easier). If x is larger than all tails, append x.",
        "time_complexity": "Time: O(n log n) · Space: O(n)",
        "space_complexity": "O(n) for tails array",
        "video_url": "https://www.youtube.com/embed/cjWnW0hdF1Y",
        "video_title": "LIS O(n log n) Binary Search Visualized",
        "visualization_type": "dp",
        "visualization_algorithm": "fibonacci_dp",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class LISBinarySearch {
    public static int lengthOfLIS(int[] nums) {
        int[] tails = new int[nums.length];
        int size = 0;
        for (int x : nums) {
            int i = 0, j = size;
            while (i < j) {
                int m = (i + j) / 2;
                if (tails[m] < x) i = m + 1;
                else j = m;
            }
            tails[i] = x;
            if (i == size) size++;
        }
        return size;
    }
}""",
        "python_code": """from bisect import bisect_left
def length_of_lis(nums: list[int]) -> int:
    tails = []
    for x in nums:
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)"""
    },

    # -------------------------------------------------------------
    # 21. Bit Manipulation
    # -------------------------------------------------------------
    {
        "id": "concept_bit_subsets_bitmask",
        "category": "Bit Manipulation",
        "difficulty": "Intermediate",
        "title": "Subsets Generation & State Encodings using Bitmasks",
        "prerequisites": "Bitwise Operators, Power of Two",
        "summary": "Iterate from 0 to 2ⁿ - 1 and inspect the i-th bit to generate all subsets or represent visited states in O(1) space.",
        "why_learn_it": "The core technique behind Traveling Salesperson Bitmask DP, Hamiltonian path algorithms, and hardware register flags.",
        "fundamental_explanation": "An integer of n bits can represent any subset of size n. If the k-th bit is 1, the k-th element is included; if 0, it is excluded.",
        "core_theory": "### Bitwise Checking\nTo check if item k is included in mask: `(mask & (1 << k)) != 0`.\nTo add item k to mask: `mask | (1 << k)`.",
        "time_complexity": "Time: O(n * 2ⁿ) · Space: O(1) auxiliary",
        "space_complexity": "O(1) memory space",
        "video_url": "https://www.youtube.com/embed/5rtV0loSRlU",
        "video_title": "Bitmasking Tricks and Subsets Tutorial",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """import java.util.*;
public class BitSubsets {
    public static List<List<Integer>> subsets(int[] nums) {
        int n = nums.length;
        int total = 1 << n; // 2^n
        List<List<Integer>> res = new ArrayList<>();
        for (int mask = 0; mask < total; mask++) {
            List<Integer> sub = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                if ((mask & (1 << i)) != 0) sub.add(nums[i]);
            }
            res.add(sub);
        }
        return res;
    }
}""",
        "python_code": """def subsets_bitmask(nums: list[int]) -> list[list[int]]:
    n = len(nums)
    res = []
    for mask in range(1 << n):
        sub = [nums[i] for i in range(n) if (mask & (1 << i))]
        res.append(sub)
    return res"""
    },

    # -------------------------------------------------------------
    # 22. Mathematical Algorithms and Number Theory
    # -------------------------------------------------------------
    {
        "id": "concept_math_sieve_gcd",
        "category": "Mathematical Algorithms and Number Theory",
        "difficulty": "Beginner",
        "title": "Sieve of Eratosthenes & Euclidean GCD Algorithm",
        "prerequisites": "Loops, Modulo Arithmetic",
        "summary": "Find all primes up to N in O(N log log N) and calculate the Greatest Common Divisor in O(log(min(a, b))) time.",
        "why_learn_it": "Fundamental building block of RSA public-key cryptography, fractional simplification, and competitive programming math.",
        "fundamental_explanation": "Euclidean GCD states: `gcd(a, b) = gcd(b, a % b)`. Sieve marks composite multiples starting from p² for each prime p up to √N.",
        "core_theory": "### Euclidean Invariant\nIf d divides both a and b, d also divides `a - b` and `a % b`. The algorithm terminates when `b == 0`, returning `a`.",
        "time_complexity": "GCD: O(log(min(a, b))) · Sieve: O(N log log N)",
        "space_complexity": "Sieve: O(N) boolean array",
        "video_url": "https://www.youtube.com/embed/klcIklIwcAU",
        "video_title": "Sieve of Eratosthenes & Euclidean GCD Explained",
        "visualization_type": "searching",
        "visualization_algorithm": "linear_search",
        "practice_problem_slug": "two-sum",
        "java_code": """public class MathAlgos {
    public static int gcd(int a, int b) {
        return b == 0 ? a : gcd(b, a % b);
    }
    public static boolean[] sieve(int n) {
        boolean[] isPrime = new boolean[n + 1];
        java.util.Arrays.fill(isPrime, true);
        isPrime[0] = isPrime[1] = false;
        for (int p = 2; p * p <= n; p++) {
            if (isPrime[p]) {
                for (int i = p * p; i <= n; i += p) isPrime[i] = false;
            }
        }
        return isPrime;
    }
}""",
        "python_code": """def gcd(a: int, b: int) -> int:
    while b: a, b = b, a % b
    return a

def sieve(n: int) -> list[int]:
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    for p in range(2, int(n**0.5) + 1):
        if is_prime[p]:
            for i in range(p * p, n + 1, p): is_prime[i] = False
    return [i for i, p in enumerate(is_prime) if p]"""
    },

    # -------------------------------------------------------------
    # 23. Advanced Data Structures
    # -------------------------------------------------------------
    {
        "id": "concept_adv_segment_tree",
        "category": "Advanced Data Structures",
        "difficulty": "Advanced",
        "title": "Segment Tree with Range Queries & Lazy Propagation",
        "prerequisites": "Complete Binary Trees, Recursion",
        "summary": "Execute range sum/min/max queries and range updates across an array in O(log n) time using binary tree aggregation.",
        "why_learn_it": "Essential for competitive programming contests (Codeforces, LeetCode Hard) and geographic spatial index queries.",
        "fundamental_explanation": "A balanced binary tree where each node represents an interval `[L, R]`. Leaf nodes store individual elements. Internal nodes store aggregate values (sum, min).",
        "core_theory": "### Lazy Propagation\nWhen updating a range `[l, r]`, avoid updating all leaves immediately. Mark the node as 'lazy' and propagate updates downward only when a query visits that branch.",
        "time_complexity": "Build: O(n) · Query: O(log n) · Range Update: O(log n)",
        "space_complexity": "O(4n) array size",
        "video_url": "https://www.youtube.com/embed/ZBHKZF5w4dU",
        "video_title": "Segment Tree Range Query Implementation",
        "visualization_type": "tree",
        "visualization_algorithm": "tree_traversal",
        "practice_problem_slug": "two-sum",
        "java_code": """public class SegmentTree {
    int[] tree, arr;
    int n;
    public SegmentTree(int[] in) {
        arr = in; n = in.length; tree = new int[4 * n];
        build(0, 0, n - 1);
    }
    private void build(int node, int start, int end) {
        if (start == end) { tree[node] = arr[start]; return; }
        int mid = (start + end) / 2;
        build(2 * node + 1, start, mid);
        build(2 * node + 2, mid + 1, end);
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
    }
    public int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return query(2 * node + 1, start, mid, l, r) + query(2 * node + 2, mid + 1, end, l, r);
    }
}""",
        "python_code": """class SegmentTree:
    def __init__(self, arr: list[int]):
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        def build(node, s, e):
            if s == e:
                self.tree[node] = arr[s]; return
            m = (s + e) // 2
            build(2 * node + 1, s, m); build(2 * node + 2, m + 1, e)
            self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
        build(0, 0, self.n - 1)
        
    def query(self, node, s, e, l, r):
        if r < s or e < l: return 0
        if l <= s and e <= r: return self.tree[node]
        m = (s + e) // 2
        return self.query(2 * node + 1, s, m, l, r) + self.query(2 * node + 2, m + 1, e, l, r)"""
    },

    # -------------------------------------------------------------
    # 24. Advanced Algorithmic Techniques
    # -------------------------------------------------------------
    {
        "id": "concept_adv_quickselect",
        "category": "Advanced Algorithmic Techniques",
        "difficulty": "Intermediate",
        "title": "Quickselect: Kth Smallest Element in O(n) Average Time",
        "prerequisites": "QuickSort, Lomuto/Hoare Partitioning",
        "summary": "Find the Kth order statistic without sorting the entire array by recursing only into the partition containing index K.",
        "why_learn_it": "Finds medians and Top-K values in linear O(n) average time without allocating a heap or sorting the array (O(n log n)).",
        "fundamental_explanation": "Partition the array around a pivot. If pivot ends up at index K, return `arr[K]`. If pivot > K, recurse only into left partition. If pivot < K, recurse only into right partition.",
        "core_theory": "### Recurrence Relation\n`T(n) = T(n/2) + O(n)` ➔ By Master Theorem, `n + n/2 + n/4 + ... = 2n = O(n)` linear time on average!",
        "time_complexity": "Average: O(n) · Worst Case: O(n²)",
        "space_complexity": "O(1) auxiliary",
        "video_url": "https://www.youtube.com/embed/BP7GCALO2v8",
        "video_title": "Quickselect Algorithm Visualized",
        "visualization_type": "sorting",
        "visualization_algorithm": "merge_sort",
        "practice_problem_slug": "two-sum",
        "java_code": """public class QuickSelect {
    public static int findKth(int[] nums, int k) {
        return select(nums, 0, nums.length - 1, k - 1);
    }
    private static int select(int[] nums, int l, int r, int k) {
        if (l == r) return nums[l];
        int p = partition(nums, l, r);
        if (p == k) return nums[p];
        else if (p > k) return select(nums, l, p - 1, k);
        else return select(nums, p + 1, r, k);
    }
    private static int partition(int[] nums, int l, int r) {
        int pivot = nums[r], idx = l;
        for (int i = l; i < r; i++) {
            if (nums[i] <= pivot) {
                int t = nums[idx]; nums[idx] = nums[i]; nums[i] = t; idx++;
            }
        }
        int t = nums[idx]; nums[idx] = nums[r]; nums[r] = t;
        return idx;
    }
}""",
        "python_code": """def quickselect(nums: list[int], k: int) -> int:
    pivot = nums[len(nums) // 2]
    left = [x for x in nums if x < pivot]
    mid = [x for x in nums if x == pivot]
    right = [x for x in nums if x > pivot]
    
    if k <= len(left):
        return quickselect(left, k)
    elif k <= len(left) + len(mid):
        return pivot
    else:
        return quickselect(right, k - len(left) - len(mid))"""
    }
]

def seed_full_library(db: Session):
    print(f"Seeding {len(ALL_CONCEPTS)} comprehensive concepts across all 24 categories...")
    
    for i, c in enumerate(ALL_CONCEPTS):
        step_num = i + 1
        prev_id = ALL_CONCEPTS[i - 1]["id"] if i > 0 else None
        next_id = ALL_CONCEPTS[i + 1]["id"] if i < len(ALL_CONCEPTS) - 1 else None
        
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
                    {"step": 1, "action": f"Initialize algorithm for {c['title']}", "variables": {"state": "init"}, "notes": "Set up base parameters and pointers."},
                    {"step": 2, "action": "Process input data elements", "variables": {"iteration": 1, "condition": "valid"}, "notes": "Evaluate algorithmic invariant."},
                    {"step": 3, "action": "Complete execution & produce optimal result", "variables": {"result": "optimal"}, "notes": "Achieved target bounds."}
                ]),
                java_code=c["java_code"],
                python_code=c["python_code"],
                practice_questions=json.dumps([
                    {"difficulty": c["difficulty"], "title": f"Solve {c['title']}", "description": c["summary"]}
                ]),
                ai_hints=json.dumps([
                    {"level": 1, "title": "Conceptual Clue", "hint": f"Consider how {c['title']} exploits the problem constraints."},
                    {"level": 2, "title": "Algorithmic Direction", "hint": f"Analyze the invariants: {c['time_complexity']}."},
                    {"level": 3, "title": "Pseudocode Guidance", "hint": c.get("python_code", "")[:120] + "..."}
                ]),
                common_mistakes="1. Off-by-one errors on boundary indices.\n2. Incomplete handling of empty or singleton collections.\n3. Excessive space allocation.",
                concept_connections=json.dumps({
                    "prerequisites": [c["prerequisites"]],
                    "category": c["category"],
                    "next": next_id
                }),
                quiz_questions=json.dumps([
                    {
                        "id": 1,
                        "question": f"What is the primary operational advantage of {c['title']}?",
                        "options": [
                            f"Provides optimal runtime: {c['time_complexity']}",
                            "Requires zero memory on disk",
                            "Only executes on sorted data",
                            "Disables runtime checks"
                        ],
                        "correct_idx": 0,
                        "explanation": f"{c['title']} achieves optimal complexity {c['time_complexity']}."
                    },
                    {
                        "id": 2,
                        "question": f"What is the space complexity of {c['title']}?",
                        "options": ["O(1)", c["space_complexity"], "O(N²)", "O(2ⁿ)"],
                        "correct_idx": 1,
                        "explanation": f"Space complexity is {c['space_complexity']}."
                    }
                ]),
                mastery_threshold=70,
                prev_lesson_id=prev_id,
                next_lesson_id=next_id
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
            lesson.prev_lesson_id = prev_id
            lesson.next_lesson_id = next_id
            
    db.commit()
    print("All concepts seeded successfully.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_full_library(db)
    finally:
        db.close()
