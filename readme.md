# Route Optimizer

This project was created to demonstrate proficiency in data structures, algorithms, and Python programming. It is inspired by classic computer science curricula. It showcases:

- **Data Structures**: vectors, lists, trees, sets, stacks, queues, priority queues, heaps, maps, and graphs (adjacency list/matrix).
- **Sorting Algorithms**: selection, insertion, heap, merge, quick, bucket, and radix sort.
- **Searching Structures**: AVL trees, (2,4) trees, and backtracking algorithms.
- **Graph Algorithms**: traversals (BFS, DFS), cycle detection, topological sorting, shortest paths (Dijkstra, Bellman‑Ford), minimum spanning trees (Prim, Kruskal), and connectivity (SCC via Kosaraju).

The code is modular, well‑commented, and includes a suite of unit tests.

---

## Features

- **Graph Traversals**: iterative and recursive BFS/DFS.
- **Cycle Detection**: undirected (DFS) and directed (three‑color DFS).
- **Topological Ordering**: Kahn’s algorithm (queue‑based) and DFS‑based.
- **Shortest Paths**: Dijkstra (priority queue) and Bellman‑Ford (handles negative weights).
- **Minimum Spanning Trees**: Prim (priority queue) and Kruskal (Union‑Find + sorting).
- **Strongly Connected Components**: Kosaraju’s algorithm.
- **Sorting Algorithms**: eight classic sorts, with optional key functions.
- **Search Trees**: AVL tree (balanced BST) and (2,4) tree (B‑tree of order 4) with insertion, deletion, and search.
- **Backtracking**: find all simple paths between nodes; Hamiltonian path search.
- **File‑based Input**: all demos can read data from text files (see **Data Formats** below).
- **Unit Tests**: comprehensive test suite for every module.

---

## Requirements

- Python 3.6 or higher (uses only the standard library).
- No external packages are needed.

---

## Getting Started

### 1. Clone or Download the Project

### 2_1. Run the Interactive Demo

cd city_navigator
python main.py

You will see a menu where you can choose which algorithm family to test. Each option runs a predefined set of examples using either hardcoded data or, if available, data from the corresponding file in the data/ directory.

### 2_2. Run the Unit Tests

python -m unittest discover -s tests -v

### 3. Data File Formats

You can supply your own test data by creating text files in the "data" folder. The formats are simple and human‑readable.

graph.txt:
    directed = true or false.
    vertices = followed by space‑separated vertex names.
    edges: line is optional; each subsequent non‑comment line gives source target [weight]. Weight defaults to 1.0 if omitted.

sorting.txt:
    One number per line (integers or floats)

tree.txt:
    # Each line: key [value]
    Keys are converted to integers if possible; otherwise kept as strings.

backtrack.txt:
    same format as graph.txt, with an addition of start and end
    The start and end lines define the source and target for the path‑finding demo.

