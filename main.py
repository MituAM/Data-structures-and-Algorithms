"""
Main entry point for the City Navigation application.
Reads data from text files in the 'data' directory.
"""

import os
from graph import Graph
from sorting import (selection_sort, insertion_sort, heap_sort,
                     merge_sort, quick_sort, bucket_sort, radix_sort)
from search_trees import AVLTree, TwoFourTree
from backtracking import all_paths, hamiltonian_path
import time

DATA_DIR = "data"


def read_graph_from_file(filename):
    """
    Reads a graph from a text file.
    Returns a Graph object.
    """
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File {filepath} not found. Using default graph.")
        return None

    directed = False
    vertices = []
    edges = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('directed'):
                # parse directed = true/false
                parts = line.split('=')
                if len(parts) == 2:
                    val = parts[1].strip().lower()
                    directed = (val == 'true')
            elif line.startswith('vertices'):
                parts = line.split('=')
                if len(parts) == 2:
                    vertices = parts[1].strip().split()
            elif line.startswith('edges:'):
                continue
            else:
                # edge line: source target [weight]
                parts = line.split()
                if len(parts) >= 2:
                    u = parts[0]
                    v = parts[1]
                    w = float(parts[2]) if len(parts) > 2 else 1.0
                    edges.append((u, v, w))

    g = Graph(directed=directed)
    for v in vertices:
        g.add_vertex(v)
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g


def read_sorting_data(filename):
    """
    Reads a list of numbers (as floats) from a file.
    Returns a list of numbers.
    """
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File {filepath} not found. Using default numbers.")
        return None

    data = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                data.append(float(line))
            except ValueError:
                print(f"Skipping invalid line: {line}")
    return data


def read_tree_data(filename):
    """
    Reads keys and optional values for tree insertion.
    Returns list of (key, value) pairs. Value defaults to str(key).
    """
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File {filepath} not found. Using default tree data.")
        return None

    items = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            if not parts:
                continue
            key = parts[0]
            # Try to convert key to int, keep as string if fails
            try:
                key = int(key)
            except ValueError:
                pass
            if len(parts) >= 2:
                value = ' '.join(parts[1:])   # rest of line as value
            else:
                value = str(key)
            items.append((key, value))
    return items


def read_backtrack_data(filename):
    """
    Reads graph and start/end for backtracking.
    Returns (graph, start, end) tuple.
    """
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        print(f"File {filepath} not found. Using default backtracking data.")
        return None, None, None

    directed = False
    vertices = []
    edges = []
    start = None
    end = None
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('directed'):
                parts = line.split('=')
                if len(parts) == 2:
                    val = parts[1].strip().lower()
                    directed = (val == 'true')
            elif line.startswith('vertices'):
                parts = line.split('=')
                if len(parts) == 2:
                    vertices = parts[1].strip().split()
            elif line.startswith('start'):
                parts = line.split('=')
                if len(parts) == 2:
                    start = parts[1].strip()
            elif line.startswith('end'):
                parts = line.split('=')
                if len(parts) == 2:
                    end = parts[1].strip()
            elif line.startswith('edges:'):
                continue
            else:
                parts = line.split()
                if len(parts) >= 2:
                    u = parts[0]
                    v = parts[1]
                    w = float(parts[2]) if len(parts) > 2 else 1.0
                    edges.append((u, v, w))

    g = Graph(directed=directed)
    for v in vertices:
        g.add_vertex(v)
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g, start, end


def demo_graph():
    """Demonstrate graph algorithms using data from graph.txt."""
    print("\n=== Graph Demo ===")
    g = read_graph_from_file("graph.txt")
    if g is None:
        # Fallback to default hardcoded graph
        g = Graph(directed=False)
        for v in ['A', 'B', 'C', 'D', 'E']:
            g.add_vertex(v)
        g.add_edge('A', 'B', 4)
        g.add_edge('A', 'C', 2)
        g.add_edge('B', 'C', 1)
        g.add_edge('B', 'D', 5)
        g.add_edge('C', 'D', 8)
        g.add_edge('C', 'E', 10)
        g.add_edge('D', 'E', 2)

    # BFS
    start_time = time.perf_counter()
    bfs_result = g.bfs('A')
    bfs_time = time.perf_counter() - start_time
    print(f"BFS from A: {bfs_result}  (time: {bfs_time:.6f} s)")

    # DFS iterative
    start_time = time.perf_counter()
    dfs_iter_result = g.dfs_iterative('A')
    dfs_iter_time = time.perf_counter() - start_time
    print(f"DFS (iterative) from A: {dfs_iter_result}  (time: {dfs_iter_time:.6f} s)")

    # DFS recursive
    start_time = time.perf_counter()
    dfs_rec_result = g.dfs_recursive('A')
    dfs_rec_time = time.perf_counter() - start_time
    print(f"DFS (recursive) from A: {dfs_rec_result}  (time: {dfs_rec_time:.6f} s)")

    # Choose a start vertex that exists
    start_vertex = next(iter(g.vertices)) if g.vertices else None
    if start_vertex:
        # Dijkstra
        start_time = time.perf_counter()
        dist, prev = g.dijkstra(start_vertex)
        dijkstra_time = time.perf_counter() - start_time
        print(f"Dijkstra from {start_vertex}: distances {dist}  (time: {dijkstra_time:.6f} s)")

        # Kruskal MST
        start_time = time.perf_counter()
        mst = g.kruskal_mst()
        kruskal_time = time.perf_counter() - start_time
        print(f"Kruskal MST edges: {mst}  (time: {kruskal_time:.6f} s)")

    # Cycle detection (undirected)
    start_time = time.perf_counter()
    has_cycle = g.has_cycle_undirected()
    cycle_time = time.perf_counter() - start_time
    print(f"Has cycle (undirected)? {has_cycle}  (time: {cycle_time:.6f} s)")

    # Directed cycle detection on a separate small graph
    g2 = Graph(directed=True)
    g2.add_edge('X', 'Y')
    g2.add_edge('Y', 'Z')
    g2.add_edge('Z', 'X')
    start_time = time.perf_counter()
    has_cycle_dir = g2.has_cycle_directed()
    cycle_dir_time = time.perf_counter() - start_time
    print(f"Has cycle (directed) on tiny graph? {has_cycle_dir}  (time: {cycle_dir_time:.6f} s)")


def demo_sorting():
    """Demonstrate sorting algorithms using data from sorting.txt."""
    print("\n=== Sorting Demo ===")
    data = read_sorting_data("sorting.txt")
    if data is None:
        # Fallback default
        data = [64, 34, 25, 12, 22, 11, 90]
    print("Original:", data)

    # List of sorting algorithms to test
    sorts = [
        ("Selection sort", selection_sort),
        ("Insertion sort", insertion_sort),
        ("Heap sort", heap_sort),
        ("Merge sort", merge_sort),
        ("Quick sort", quick_sort),
    ]
    # Bucket and radix sort are tested separately
    for name, func in sorts:
        arr = data.copy()
        start_time = time.perf_counter()
        sorted_arr = func(arr)
        elapsed = time.perf_counter() - start_time
        print(f"{name}: {sorted_arr}  (time: {elapsed:.6f} s)")

    # ----- Bucket Sort -----
    # Bucket sort requires keys that can be mapped to bucket indices.
    if data:
        min_val = min(data)
        max_val = max(data)
        if min_val == max_val:
            norm_data = [(x, 0.5) for x in data]
        else:
            norm_data = [(x,
                          (x - min_val) / (max_val - min_val)) for x in data]

        pairs = norm_data
        arr_pairs = pairs.copy()
        start_time = time.perf_counter()
        bucket_sort(arr_pairs, key=lambda p: p[1], num_buckets=10)
        elapsed = time.perf_counter() - start_time
        bucket_sorted = [p[0] for p in arr_pairs]
        print(f"Bucket sort (normalized): {bucket_sorted}  (time: {elapsed:.6f} s)")
    else:
        print("Bucket sort skipped: empty data.")

    # ----- Radix Sort -----
    # Radix sort requires non‑negative integers.
    if all(isinstance(x, (int, float)) and
           x == int(x) and x >= 0 for x in data):
        int_data = [int(x) for x in data]
        arr = int_data.copy()
        start_time = time.perf_counter()
        sorted_arr = radix_sort(arr)
        elapsed = time.perf_counter() - start_time
        print(f"Radix sort: {sorted_arr}  (time: {elapsed:.6f} s)")
    else:
        print("Radix sort skipped: data has non‑integers/negative numbers.")


def demo_search_trees():
    """Demonstrate AVL and (2,4) trees using data from tree.txt."""
    print("\n=== AVL Tree Demo ===")
    items = read_tree_data("tree.txt")
    if items is None:
        # Fallback default
        items = [(10, "val_10"), (20, "val_20"), (30, "val_30"),
                 (40, "val_40"), (50, "val_50"), (25, "val_25")]

        # AVL insertion
    avl = AVLTree()
    start_time = time.perf_counter()
    for key, value in items:
        avl.insert(key, value)
    insert_time = time.perf_counter() - start_time
    print(f"AVL insertion of {len(items)} items  (time: {insert_time:.6f} s)")

    # AVL inorder traversal
    start_time = time.perf_counter()
    inorder = avl.inorder()
    traverse_time = time.perf_counter() - start_time
    print(f"AVL inorder traversal: {inorder}  (time: {traverse_time:.6f} s)")

    # AVL search (existing key)
    if items:
        test_key = items[0][0]
        start_time = time.perf_counter()
        node = avl.search(test_key)
        search_time = time.perf_counter() - start_time
        print(f"AVL search for key {test_key}: found {node.key if node else 'None'}  (time: {search_time:.6f} s)")

        # AVL deletion
        del_key = items[-1][0]
        start_time = time.perf_counter()
        avl.delete(del_key)
        delete_time = time.perf_counter() - start_time
        print(f"AVL deletion of key {del_key}  (time: {delete_time:.6f} s)")

    # (2,4) Tree demo
    print("\n=== (2,4) Tree Demo ===")
    tt = TwoFourTree()
    start_time = time.perf_counter()
    for key, value in items:
        tt.insert(key, value)
    tt_insert_time = time.perf_counter() - start_time
    print(f"(2,4) insertion of {len(items)} items  (time: {tt_insert_time:.6f} s)")

    if items:
        test_key = items[0][0]
        start_time = time.perf_counter()
        found = tt.search(test_key)
        tt_search_time = time.perf_counter() - start_time
        print(f"(2,4) search for key {test_key}: {found}  (time: {tt_search_time:.6f} s)")


def demo_backtracking():
    """Demonstrate backtracking algorithms using data from backtrack.txt."""
    print("\n=== Backtracking Demo ===")
    g, start, end = read_backtrack_data("backtrack.txt")
    if g is None:
        # Fallback default
        g = Graph(directed=False)
        for v in [1, 2, 3, 4]:
            g.add_vertex(v)
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 4)
        g.add_edge(3, 4)
        start, end = 1, 4

    if start is not None and end is not None:
        start_time = time.perf_counter()
        paths = all_paths(g, start, end)
        all_paths_time = time.perf_counter() - start_time
        print(f"All paths from {start} to {end}: {paths}  (time: {all_paths_time:.6f} s)")
    else:
        print("Start or end not defined in file.")

    start_time = time.perf_counter()
    hp = hamiltonian_path(g)
    hp_time = time.perf_counter() - start_time
    print(f"Hamiltonian path on line graph: {hp}  (time: {hp_time:.6f} s)")


def main():
    print("City Navigation System - Backend Demo")
    print("======================================")
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Created '{DATA_DIR}' directory. Please add data files.")
    while True:
        print("\nChoose an option:")
        print("1. Graph algorithms")
        print("2. Sorting algorithms")
        print("3. Search trees (AVL, (2,4))")
        print("4. Backtracking")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            demo_graph()
        elif choice == '2':
            demo_sorting()
        elif choice == '3':
            demo_search_trees()
        elif choice == '4':
            demo_backtracking()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
