#!/usr/bin/env python3
"""
AlgoPlayground - Interactive Algorithm Showcase
Demonstrates mastery of:
- Graph algorithms
- Greedy algorithms
- Divide & conquer algorithms
- Dynamic programming
- Network flow
- Correctness proofs
- Analytical & experimental runtime analysis
- Efficient implementation
- Algorithm selection advice
"""

import time
import random
import heapq
from collections import deque

# ---------------------------- Utility Functions ----------------------------
def input_int(prompt, min_val=None, max_val=None):
    """Robust integer input with optional range."""
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("Please enter a valid integer.")

def input_float(prompt, min_val=None, max_val=None):
    """Robust float input."""
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and val < min_val:
                print(f"Value must be >= {min_val}")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be <= {max_val}")
                continue
            return val
        except ValueError:
            print("Please enter a valid number.")

def time_it(func, *args, **kwargs):
    """Measure execution time of a function."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed = time.perf_counter() - start
    return result, elapsed

# ---------------------------- Graph Algorithms -----------------------------
def dijkstra(graph, source):
    """
    Dijkstra's algorithm for shortest paths from source.
    graph: adjacency list {u: [(v, weight), ...]}
    Returns (dist, prev) where dist[v] is shortest distance, prev[v] is predecessor.
    """
    n = len(graph)
    dist = {v: float('inf') for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0
    pq = [(0, source)]  # (distance, vertex)
    visited = set()

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u]:
            if v not in visited and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev

def dijkstra_correctness():
    return """Correctness (invariant): When a vertex is extracted from the priority queue with smallest tentative distance, that distance is final because all edge weights are non-negative and any alternative path would be longer. This is proved by induction on the number of settled vertices."""

def dijkstra_complexity():
    return "O((V+E) log V) with binary heap."

def bellman_ford(graph, source):
    """
    Bellman-Ford algorithm for shortest paths (handles negative weights, detects negative cycles).
    Returns (dist, prev, has_negative_cycle).
    """
    n = len(graph)
    dist = {v: float('inf') for v in graph}
    prev = {v: None for v in graph}
    dist[source] = 0

    # Relax edges V-1 times
    for _ in range(n - 1):
        updated = False
        for u in graph:
            for v, w in graph[u]:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    prev[v] = u
                    updated = True
        if not updated:
            break

    # Check for negative cycles
    for u in graph:
        for v, w in graph[u]:
            if dist[u] + w < dist[v]:
                return dist, prev, True  # negative cycle detected
    return dist, prev, False

def bellman_ford_correctness():
    return """Correctness: After i iterations, dist[v] is the length of the shortest path from source to v using at most i edges. After V-1 iterations, the shortest paths (with no cycles) are found. The final check detects negative cycles reachable from source."""

def bellman_ford_complexity():
    return "O(V*E) time."

def floyd_warshall(graph):
    """
    Floyd-Warshall for all-pairs shortest paths.
    graph: adjacency list; we convert to distance matrix.
    Returns dist matrix (as dict of dicts) and has_negative_cycle.
    """
    vertices = list(graph.keys())
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    # Initialize distance matrix
    dist = [[float('inf')] * n for _ in range(n)]
    for i, v in enumerate(vertices):
        dist[i][i] = 0
        for u, wlist in graph.items():
            for v2, w in wlist:
                dist[index[u]][index[v2]] = w

    # Main algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    # Check for negative cycles
    for i in range(n):
        if dist[i][i] < 0:
            return dist, vertices, True
    return dist, vertices, False

def floyd_warshall_correctness():
    return """Correctness (induction on k): After processing vertices 0..k-1 as intermediates, dist[i][j] is the shortest path using only those vertices as intermediates. After all vertices, all shortest paths are found."""

def floyd_warshall_complexity():
    return "O(V^3) time."

def kruskal(graph_edges, num_vertices):
    """
    Kruskal's algorithm for MST.
    graph_edges: list of (u, v, weight) for undirected graph.
    Returns list of edges in MST and total weight.
    """
    # Sort edges by weight
    edges = sorted(graph_edges, key=lambda x: x[2])
    parent = list(range(num_vertices))
    rank = [0] * num_vertices

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1
        return True

    mst = []
    total = 0
    for u, v, w in edges:
        if union(u, v):
            mst.append((u, v, w))
            total += w
    return mst, total

def kruskal_correctness():
    return """Correctness (cut property): The algorithm always picks the smallest edge crossing some cut that doesn't create a cycle, ensuring optimality. Union-Find efficiently maintains connectivity."""

def kruskal_complexity():
    return "O(E log E) due to sorting."

# ---------------------------- Greedy Algorithms ----------------------------
def activity_selection(activities):
    """
    activities: list of (start, finish) tuples.
    Returns maximum set of non-overlapping activities.
    """
    # Sort by finish time
    sorted_acts = sorted(activities, key=lambda x: x[1])
    selected = []
    last_finish = -float('inf')
    for s, f in sorted_acts:
        if s >= last_finish:
            selected.append((s, f))
            last_finish = f
    return selected

def activity_selection_correctness():
    return """Correctness (greedy choice): The activity with earliest finish leaves the most time for remaining activities; exchange argument shows no optimal solution can exclude it."""

def activity_selection_complexity():
    return "O(n log n) due to sorting."

def fractional_knapsack(items, capacity):
    """
    items: list of (value, weight) tuples.
    Returns maximum total value and list of fractions taken.
    """
    # Sort by value/weight ratio descending
    items = sorted(items, key=lambda x: x[0]/x[1], reverse=True)
    total_value = 0.0
    fractions = []  # (index, fraction taken)
    for i, (v, w) in enumerate(items):
        if capacity >= w:
            total_value += v
            fractions.append((i, 1.0))
            capacity -= w
        else:
            fraction = capacity / w
            total_value += v * fraction
            fractions.append((i, fraction))
            break
    return total_value, fractions

def fractional_knapsack_correctness():
    return """Correctness: Optimal to take as much as possible of the item with highest value per unit weight. Exchange argument shows no other item can improve total value."""

def fractional_knapsack_complexity():
    return "O(n log n) due to sorting."

# ---------------------------- Divide & Conquer -----------------------------
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort_correctness():
    return """Correctness: By induction on array length. Base case trivially sorted. Inductive step: merge two sorted halves produces fully sorted array."""

def merge_sort_complexity():
    return "O(n log n) time, O(n) auxiliary space."

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[-1]
    left = [x for x in arr[:-1] if x <= pivot]
    right = [x for x in arr[:-1] if x > pivot]
    return quick_sort(left) + [pivot] + quick_sort(right)

def quick_sort_correctness():
    return """Correctness: Recursively sorts elements less than pivot and greater than pivot, then concatenates. The pivot is in its final position. Induction on length proves correctness."""

def quick_sort_complexity():
    return "Average O(n log n), worst O(n²). In-place version uses O(log n) stack space."

# ---------------------------- Dynamic Programming --------------------------
def knapsack_01(items, capacity):
    """
    items: list of (value, weight)
    Returns max value and selected items indices.
    """
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    # Build table
    for i in range(1, n + 1):
        v, w = items[i-1]
        for cap in range(capacity + 1):
            if w > cap:
                dp[i][cap] = dp[i-1][cap]
            else:
                dp[i][cap] = max(dp[i-1][cap], dp[i-1][cap - w] + v)

    # Backtrack to find selected items
    selected = []
    cap = capacity
    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i-1][cap]:
            selected.append(i-1)
            cap -= items[i-1][1]
    selected.reverse()
    return dp[n][capacity], selected

def knapsack_01_correctness():
    return """Correctness (optimal substructure): The optimal solution for capacity C either includes item i (then add optimal for C - w_i with items 1..i-1) or excludes it. DP table fills using this recurrence."""

def knapsack_01_complexity():
    return "O(n * capacity) time and space."

def lcs(X, Y):
    """Longest Common Subsequence length and string."""
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    # Reconstruct LCS
    lcs_str = []
    i, j = m, n
    while i > 0 and j > 0:
        if X[i-1] == Y[j-1]:
            lcs_str.append(X[i-1])
            i -= 1
            j -= 1
        elif dp[i-1][j] > dp[i][j-1]:
            i -= 1
        else:
            j -= 1
    lcs_str.reverse()
    return dp[m][n], ''.join(lcs_str)

def lcs_correctness():
    return """Correctness: If last characters match, they belong to LCS; otherwise LCS is max of excluding one of them. DP builds optimal solution using this recurrence."""

def lcs_complexity():
    return "O(m*n) time and space."

# ---------------------------- Network Flow --------------------------------
def edmonds_karp(capacity, source, sink):
    """
    capacity: adjacency dict with capacities: {u: {v: cap}}
    Returns max flow value and flow dict.
    """
    # Initialize residual graph as dict of dicts
    resid = {u: {v: cap for v, cap in adj.items()} for u, adj in capacity.items()}
    for u in resid:
        for v in resid[u]:
            if v not in resid:
                resid[v] = {}
            if u not in resid[v]:
                resid[v][u] = 0  # reverse edge with zero capacity

    parent = {}
    flow = 0

    def bfs():
        """Find augmenting path in residual graph using BFS."""
        visited = {source}
        queue = deque([source])
        parent.clear()
        while queue:
            u = queue.popleft()
            for v, cap in resid[u].items():
                if v not in visited and cap > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == sink:
                        return True
                    queue.append(v)
        return False

    while bfs():
        # Find bottleneck capacity
        path_flow = float('inf')
        s = sink
        while s != source:
            u = parent[s]
            path_flow = min(path_flow, resid[u][s])
            s = u
        # Update residual network
        s = sink
        while s != source:
            u = parent[s]
            resid[u][s] -= path_flow
            resid[s][u] += path_flow
            s = u
        flow += path_flow

    return flow, resid  # resid now contains final flow on edges (original cap - resid[u][v])

def edmonds_karp_correctness():
    return """Correctness: Based on Ford-Fulkerson method. BFS finds shortest augmenting path (in terms of number of edges), ensuring O(VE²) iterations. The max-flow min-cut theorem guarantees optimality when no augmenting path exists."""

def edmonds_karp_complexity():
    return "O(V * E²) time."

# ---------------------------- Input Helpers --------------------------------
def input_graph(weighted=True, directed=True, capacities=False):
    """Prompt user to input graph edges."""
    print("\nEnter graph edges (one per line). Format: u v w (or u v if unweighted)")
    print("Type 'done' when finished.")
    graph = {}
    edges = []
    vertex_set = set()
    while True:
        line = input("> ").strip()
        if line.lower() == 'done':
            break
        parts = line.split()
        if len(parts) < (3 if weighted else 2):
            print("Invalid format. Try again.")
            continue
        u = parts[0]
        v = parts[1]
        w = float(parts[2]) if weighted else 1.0
        if capacities and w < 0:
            print("Capacities must be non-negative. Setting to 0.")
            w = 0
        vertex_set.add(u)
        vertex_set.add(v)
        if u not in graph:
            graph[u] = []
        graph[u].append((v, w))
        edges.append((u, v, w))
        if not directed:
            # For undirected, add reverse edge
            if v not in graph:
                graph[v] = []
            graph[v].append((u, w))
    # Ensure all vertices have entry
    for v in vertex_set:
        if v not in graph:
            graph[v] = []
    return graph, edges, list(vertex_set)

def input_array():
    """Input list of numbers."""
    print("Enter numbers separated by spaces:")
    line = input().strip()
    return [float(x) for x in line.split()]

def input_items():
    """Input items for knapsack (value weight)."""
    print("Enter items (value weight) one per line. Type 'done' when finished.")
    items = []
    while True:
        line = input("> ").strip()
        if line.lower() == 'done':
            break
        parts = line.split()
        if len(parts) != 2:
            print("Invalid. Need value and weight.")
            continue
        try:
            v = float(parts[0])
            w = float(parts[1])
            items.append((v, w))
        except ValueError:
            print("Invalid numbers.")
    return items

def input_activities():
    """Input activities (start finish)."""
    print("Enter activities (start finish) one per line. Type 'done' when finished.")
    acts = []
    while True:
        line = input("> ").strip()
        if line.lower() == 'done':
            break
        parts = line.split()
        if len(parts) != 2:
            print("Invalid. Need start and finish.")
            continue
        try:
            s = float(parts[0])
            f = float(parts[1])
            if s > f:
                print("Start must be <= finish. Skipping.")
                continue
            acts.append((s, f))
        except ValueError:
            print("Invalid numbers.")
    return acts

# ---------------------------- Main Application -----------------------------
def main():
    print("=" * 60)
    print("            AlgoPlayground - Algorithm Showcase")
    print("=" * 60)
    print("This tool demonstrates algorithms from 5 categories:")
    print("  1. Graph Algorithms")
    print("  2. Greedy Algorithms")
    print("  3. Divide & Conquer")
    print("  4. Dynamic Programming")
    print("  5. Network Flow")
    print("Also includes correctness proofs, complexity analysis,")
    print("experimental timing, benchmarking, and advice.")
    print()

    while True:
        print("\nMain Menu:")
        print("1. Run a specific algorithm")
        print("2. Benchmark an algorithm (time vs input size)")
        print("3. Get algorithmic advice")
        print("4. Exit")
        choice = input_int("Choose (1-4): ", 1, 4)

        if choice == 1:
            run_algorithm_menu()
        elif choice == 2:
            benchmark_menu()
        elif choice == 3:
            advice_menu()
        else:
            print("Goodbye!")
            break

def run_algorithm_menu():
    """Submenu to select algorithm category and specific algorithm."""
    print("\nSelect algorithm category:")
    print("1. Graph Algorithms")
    print("2. Greedy Algorithms")
    print("3. Divide & Conquer")
    print("4. Dynamic Programming")
    print("5. Network Flow")
    cat = input_int("Category (1-5): ", 1, 5)

    if cat == 1:
        print("\nGraph Algorithms:")
        print("1. Dijkstra (shortest path, non-negative weights)")
        print("2. Bellman-Ford (shortest path, negative weights allowed)")
        print("3. Floyd-Warshall (all-pairs shortest paths)")
        print("4. Kruskal (minimum spanning tree)")
        algo = input_int("Choose (1-4): ", 1, 4)

        if algo == 1:
            # Dijkstra
            graph, edges, vertices = input_graph(weighted=True, directed=True)
            source = input("Source vertex: ").strip()
            if source not in graph:
                print("Source not in graph.")
                return
            result, elapsed = time_it(dijkstra, graph, source)
            dist, prev = result
            print("\n=== Dijkstra ===")
            print(f"Shortest distances from {source}:")
            for v in vertices:
                print(f"  {v}: {dist[v]}")
            print("\nCorrectness:", dijkstra_correctness())
            print("Complexity:", dijkstra_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

        elif algo == 2:
            # Bellman-Ford
            graph, edges, vertices = input_graph(weighted=True, directed=True)
            source = input("Source vertex: ").strip()
            if source not in graph:
                print("Source not in graph.")
                return
            result, elapsed = time_it(bellman_ford, graph, source)
            dist, prev, neg_cycle = result
            print("\n=== Bellman-Ford ===")
            if neg_cycle:
                print("Negative cycle detected!")
            else:
                print(f"Shortest distances from {source}:")
                for v in vertices:
                    print(f"  {v}: {dist[v]}")
            print("\nCorrectness:", bellman_ford_correctness())
            print("Complexity:", bellman_ford_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

        elif algo == 3:
            # Floyd-Warshall
            graph, edges, vertices = input_graph(weighted=True, directed=True)
            result, elapsed = time_it(floyd_warshall, graph)
            dist, vlist, neg_cycle = result
            print("\n=== Floyd-Warshall ===")
            if neg_cycle:
                print("Negative cycle detected!")
            else:
                print("All-pairs shortest distances:")
                for i, u in enumerate(vlist):
                    for j, v in enumerate(vlist):
                        if dist[i][j] < float('inf'):
                            print(f"  {u} -> {v}: {dist[i][j]}")
            print("\nCorrectness:", floyd_warshall_correctness())
            print("Complexity:", floyd_warshall_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

        elif algo == 4:
            # Kruskal
            print("Enter undirected graph edges (u v weight).")
            graph, edges, vertices = input_graph(weighted=True, directed=False)
            # Convert to list of (u, v, w) with vertex indices for union-find
            vertex_to_idx = {v: i for i, v in enumerate(vertices)}
            edge_list = [(vertex_to_idx[u], vertex_to_idx[v], w) for u, v, w in edges]
            result, elapsed = time_it(kruskal, edge_list, len(vertices))
            mst, total = result
            print("\n=== Kruskal's MST ===")
            print("Edges in MST:")
            for u_idx, v_idx, w in mst:
                print(f"  {vertices[u_idx]} -- {vertices[v_idx]} : {w}")
            print(f"Total weight: {total}")
            print("\nCorrectness:", kruskal_correctness())
            print("Complexity:", kruskal_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

    elif cat == 2:
        print("\nGreedy Algorithms:")
        print("1. Activity Selection")
        print("2. Fractional Knapsack")
        algo = input_int("Choose (1-2): ", 1, 2)

        if algo == 1:
            acts = input_activities()
            if not acts:
                print("No activities entered.")
                return
            result, elapsed = time_it(activity_selection, acts)
            selected = result
            print("\n=== Activity Selection ===")
            print("Selected activities (start, finish):")
            for s, f in selected:
                print(f"  ({s}, {f})")
            print("\nCorrectness:", activity_selection_correctness())
            print("Complexity:", activity_selection_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

        elif algo == 2:
            items = input_items()
            if not items:
                print("No items entered.")
                return
            capacity = input_float("Enter knapsack capacity: ", min_val=0)
            result, elapsed = time_it(fractional_knapsack, items, capacity)
            total_val, fractions = result
            print("\n=== Fractional Knapsack ===")
            print(f"Maximum value: {total_val:.2f}")
            print("Fractions taken:")
            for idx, frac in fractions:
                v, w = items[idx]
                print(f"  Item {idx+1}: {frac*100:.1f}% (value {v}, weight {w})")
            print("\nCorrectness:", fractional_knapsack_correctness())
            print("Complexity:", fractional_knapsack_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

    elif cat == 3:
        print("\nDivide & Conquer Algorithms:")
        print("1. Merge Sort")
        print("2. Quick Sort")
        algo = input_int("Choose (1-2): ", 1, 2)

        arr = input_array()
        if not arr:
            print("Empty array.")
            return
        if algo == 1:
            result, elapsed = time_it(merge_sort, arr)
            sorted_arr = result
            print("\n=== Merge Sort ===")
            print("Sorted array:", sorted_arr)
            print("\nCorrectness:", merge_sort_correctness())
            print("Complexity:", merge_sort_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")
        else:
            result, elapsed = time_it(quick_sort, arr)
            sorted_arr = result
            print("\n=== Quick Sort ===")
            print("Sorted array:", sorted_arr)
            print("\nCorrectness:", quick_sort_correctness())
            print("Complexity:", quick_sort_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

    elif cat == 4:
        print("\nDynamic Programming Algorithms:")
        print("1. 0/1 Knapsack")
        print("2. Longest Common Subsequence")
        algo = input_int("Choose (1-2): ", 1, 2)

        if algo == 1:
            items = input_items()
            if not items:
                print("No items entered.")
                return
            capacity = input_float("Enter knapsack capacity: ", min_val=0)
            # 0/1 knapsack expects integer capacity and weights? We'll allow float but DP table size may be large.
            # For simplicity, we'll treat capacity as integer and weights as integers by rounding? Better to advise.
            # We'll assume integer inputs for simplicity.
            # To handle floats, we could scale, but that's complex. We'll keep it simple.
            print("Note: 0/1 knapsack works best with integer weights and capacity.")
            result, elapsed = time_it(knapsack_01, items, int(capacity))
            max_val, selected = result
            print("\n=== 0/1 Knapsack ===")
            print(f"Maximum value: {max_val}")
            print("Selected items (index 0-based):", selected)
            print("\nCorrectness:", knapsack_01_correctness())
            print("Complexity:", knapsack_01_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

        elif algo == 2:
            print("Enter first string:")
            X = input().strip()
            print("Enter second string:")
            Y = input().strip()
            result, elapsed = time_it(lcs, X, Y)
            length, lcs_str = result
            print("\n=== Longest Common Subsequence ===")
            print(f"LCS length: {length}")
            print(f"LCS: '{lcs_str}'")
            print("\nCorrectness:", lcs_correctness())
            print("Complexity:", lcs_complexity())
            print(f"Execution time: {elapsed:.6f} seconds")

    elif cat == 5:
        print("\nNetwork Flow (Edmonds-Karp)")
        print("Enter directed graph with capacities (non-negative).")
        # Need capacity dict: {u: {v: cap}}
        # Use input_graph but build capacity dict
        graph, edges, vertices = input_graph(weighted=True, directed=True, capacities=True)
        # Convert to {u: {v: cap}} format
        cap_dict = {v: {} for v in vertices}
        for u, vlist in graph.items():
            for v, w in vlist:
                cap_dict[u][v] = w
        source = input("Source vertex: ").strip()
        sink = input("Sink vertex: ").strip()
        if source not in cap_dict or sink not in cap_dict:
            print("Source or sink not in graph.")
            return
        result, elapsed = time_it(edmonds_karp, cap_dict, source, sink)
        flow, resid = result
        print("\n=== Edmonds-Karp Max Flow ===")
        print(f"Maximum flow from {source} to {sink}: {flow}")
        print("\nCorrectness:", edmonds_karp_correctness())
        print("Complexity:", edmonds_karp_complexity())
        print(f"Execution time: {elapsed:.6f} seconds")

def benchmark_menu():
    """Benchmark an algorithm on increasing input sizes."""
    print("\nSelect algorithm to benchmark:")
    print("1. Merge Sort")
    print("2. Quick Sort")
    print("3. Dijkstra (on random graphs)")
    print("4. Bellman-Ford (on random graphs)")
    print("5. Kruskal (on random graphs)")
    print("6. 0/1 Knapsack")
    print("7. LCS")
    print("8. Activity Selection")
    print("9. Fractional Knapsack")
    print("10. Edmonds-Karp (on random graphs)")
    algo = input_int("Choose (1-10): ", 1, 10)

    sizes = []
    print("Enter input sizes to test (e.g., 10 50 100 500).")
    sizes = [int(x) for x in input().split()]
    if not sizes:
        print("No sizes provided.")
        return

    print("\nBenchmarking...")
    print(f"{'Size':<10} {'Time (s)':<15}")
    for n in sizes:
        if algo == 1:  # Merge sort
            arr = [random.randint(0, 1000) for _ in range(n)]
            _, elapsed = time_it(merge_sort, arr)
        elif algo == 2:  # Quick sort
            arr = [random.randint(0, 1000) for _ in range(n)]
            _, elapsed = time_it(quick_sort, arr)
        elif algo == 3:  # Dijkstra on random graph
            # Generate random directed graph with n nodes, about 2n edges
            graph = {str(i): [] for i in range(n)}
            for _ in range(2 * n):
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u != v:
                    w = random.randint(1, 10)
                    graph[str(u)].append((str(v), w))
            _, elapsed = time_it(dijkstra, graph, '0')
        elif algo == 4:  # Bellman-Ford
            graph = {str(i): [] for i in range(n)}
            for _ in range(2 * n):
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u != v:
                    w = random.randint(-5, 10)  # negative allowed
                    graph[str(u)].append((str(v), w))
            _, elapsed = time_it(bellman_ford, graph, '0')
        elif algo == 5:  # Kruskal on random undirected graph
            # Generate complete-ish graph? For n nodes, add random edges
            edges = []
            for u in range(n):
                for v in range(u+1, n):
                    if random.random() < 0.3:  # 30% chance
                        w = random.randint(1, 10)
                        edges.append((u, v, w))
            if not edges:
                edges.append((0, 1, 1))
            _, elapsed = time_it(kruskal, edges, n)
        elif algo == 6:  # 0/1 knapsack
            items = [(random.randint(1, 100), random.randint(1, 50)) for _ in range(n)]
            capacity = 100
            _, elapsed = time_it(knapsack_01, items, capacity)
        elif algo == 7:  # LCS
            s1 = ''.join(random.choices('ACGT', k=n))
            s2 = ''.join(random.choices('ACGT', k=n))
            _, elapsed = time_it(lcs, s1, s2)
        elif algo == 8:  # Activity selection
            acts = []
            for _ in range(n):
                s = random.randint(0, 100)
                f = random.randint(s+1, s+50)
                acts.append((s, f))
            _, elapsed = time_it(activity_selection, acts)
        elif algo == 9:  # Fractional knapsack
            items = [(random.randint(1, 100), random.randint(1, 50)) for _ in range(n)]
            capacity = 200
            _, elapsed = time_it(fractional_knapsack, items, capacity)
        elif algo == 10:  # Edmonds-Karp
            # Generate random flow network with n nodes, edges ~2n
            cap = {str(i): {} for i in range(n)}
            for _ in range(2 * n):
                u = random.randint(0, n-1)
                v = random.randint(0, n-1)
                if u != v:
                    cap[str(u)][str(v)] = random.randint(1, 10)
            # Ensure source and sink exist
            if n >= 2:
                _, elapsed = time_it(edmonds_karp, cap, '0', str(n-1))
            else:
                elapsed = 0
        print(f"{n:<10} {elapsed:.6f}")

def advice_menu():
    """Provide algorithmic advice based on problem description."""
    print("\n--- Algorithmic Advice ---")
    print("Describe your problem by answering a few questions.")
    print()

    # Gather problem characteristics
    print("What type of data?")
    print("1. Graph (nodes and edges)")
    print("2. Set of items with values/weights")
    print("3. Sequence (array, string)")
    data_type = input_int("Choose (1-3): ", 1, 3)

    if data_type == 1:
        # Graph problem
        print("\nGraph characteristics:")
        print("a. What do you need?")
        print("   1. Shortest path(s)")
        print("   2. Minimum spanning tree")
        print("   3. Maximum flow")
        need = input_int("Choose (1-3): ", 1, 3)

        if need == 1:  # shortest path
            print("\nAre edge weights non-negative?")
            neg = input("(y/n): ").lower() == 'y'
            if neg:
                print("▶ Recommendation: Bellman-Ford (handles negative weights, detects negative cycles). If negative cycles present, no shortest path exists.")
            else:
                print("▶ Recommendation: Dijkstra (O((V+E) log V) with heap). For all-pairs, consider Floyd-Warshall (O(V³)) if graph is dense.")
            print("   - Dijkstra correctness: relies on non-negative weights.")
            print("   - Bellman-Ford: can detect negative cycles.")
            print("   - Floyd-Warshall: simple to implement for small graphs.")
        elif need == 2:  # MST
            print("▶ Recommendation: Kruskal (sort edges, union-find) or Prim (priority queue). Both are optimal.")
            print("   Kruskal is often easier for sparse graphs; Prim better for dense.")
        else:  # max flow
            print("▶ Recommendation: Edmonds-Karp (BFS-based Ford-Fulkerson). Works for integer capacities.")
            print("   For very large graphs, consider Dinic's algorithm.")

    elif data_type == 2:
        # Items problem
        print("\nCan you take fractions of items?")
        fractional = input("(y/n): ").lower() == 'y'
        if fractional:
            print("▶ Recommendation: Fractional Knapsack (greedy by value/weight ratio). Optimal and O(n log n).")
        else:
            print("▶ Recommendation: 0/1 Knapsack (dynamic programming). Greedy not optimal.")
            print("   Complexity O(n * capacity). For large capacities, consider approximation algorithms.")

    elif data_type == 3:
        # Sequence problem
        print("\nWhat operation?")
        print("1. Sorting")
        print("2. Finding longest common subsequence")
        op = input_int("Choose (1-2): ", 1, 2)
        if op == 1:
            print("▶ Recommendation: Merge sort (stable, O(n log n)) or quick sort (in-place, average O(n log n)).")
            print("   Merge sort guaranteed O(n log n) but uses extra space.")
            print("   Quick sort is faster in practice but worst-case O(n²).")
        else:
            print("▶ Recommendation: Dynamic programming LCS (O(m*n)). Greedy doesn't work.")

    print("\n(For more details, run specific algorithms and compare.)")

if __name__ == "__main__":
    main()