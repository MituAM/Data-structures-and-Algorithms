"""
Graph module for the City Navigation application.
Implements directed/undirected, weighted graphs using adjacency lists.
Provides graph traversal and algorithms: BFS, DFS, Dijkstra, Prim, Kruskal.
"""

from collections import deque
import heapq


class Graph:
    """Graph data structure using adjacency lists."""

    def __init__(self, directed=False):
        self.directed = directed
        self.adj = {}          # map: vertex -> list of (neighbor, weight)
        self.vertices = set()

    def add_vertex(self, v):
        """Add a vertex to the graph."""
        if v not in self.adj:
            self.adj[v] = []
            self.vertices.add(v)

    def add_edge(self, u, v, weight=1.0):
        """Add a directed or undirected edge (u, v) with given weight."""
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append((v, weight))
        if not self.directed:
            self.adj[v].append((u, weight))

    def remove_edge(self, u, v):
        """Remove all edges between u and v."""
        self.adj[u] = [(n, w) for (n, w) in self.adj[u] if n != v]
        if not self.directed:
            self.adj[v] = [(n, w) for (n, w) in self.adj[v] if n != u]

    def remove_vertex(self, v):
        """Remove vertex v and all incident edges."""
        if v in self.adj:
            del self.adj[v]
            self.vertices.discard(v)
        # Remove edges pointing to v
        for u in list(self.adj):
            self.adj[u] = [(n, w) for (n, w) in self.adj[u] if n != v]

    # ----------------------------------------------------------------------
    # Graph Traversals
    # ----------------------------------------------------------------------
    def bfs(self, start):
        """Breadth‑first search (iterative, using deque)."""
        visited = set()
        queue = deque([start])
        visited.add(start)
        traversal = []
        while queue:
            v = queue.popleft()
            traversal.append(v)
            for (neighbor, _) in self.adj[v]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return traversal

    def dfs_iterative(self, start):
        """Depth‑first search (iterative, using stack)."""
        visited = set()
        stack = [start]
        traversal = []
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v)
                traversal.append(v)
                # Push neighbors in reverse order to mimic recursive order
                for (neighbor, _) in reversed(self.adj[v]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        return traversal

    def dfs_recursive(self, start, visited=None):
        """Depth‑first search (recursive)."""
        if visited is None:
            visited = set()
        visited.add(start)
        traversal = [start]
        for (neighbor, _) in self.adj[start]:
            if neighbor not in visited:
                traversal.extend(self.dfs_recursive(neighbor, visited))
        return traversal

    # ----------------------------------------------------------------------
    # Cycle Detection
    # ----------------------------------------------------------------------
    def has_cycle_undirected(self):
        """Detect cycle in undirected graph using DFS."""
        visited = set()
        parent = {}

        def dfs(v, par):
            visited.add(v)
            for (neighbor, _) in self.adj[v]:
                if neighbor not in visited:
                    parent[neighbor] = v
                    if dfs(neighbor, v):
                        return True
                elif neighbor != par:
                    return True
            return False

        for v in self.vertices:
            if v not in visited:
                if dfs(v, None):
                    return True
        return False

    def has_cycle_directed(self):
        """Detect cycle in directed graph using three‑color DFS."""
        WHITE, GRAY, BLACK = 0, 1, 2
        color = {v: WHITE for v in self.vertices}

        def dfs(v):
            color[v] = GRAY
            for (neighbor, _) in self.adj[v]:
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE and dfs(neighbor):
                    return True
            color[v] = BLACK
            return False

        for v in self.vertices:
            if color[v] == WHITE:
                if dfs(v):
                    return True
        return False

    # ----------------------------------------------------------------------
    # Topological Sorting
    # ----------------------------------------------------------------------
    def topological_sort_kahn(self):
        """Kahn's algorithm (uses queue).
        Returns list of vertices in topological order."""
        if not self.directed:
            raise ValueError("Graph must be directed")
        in_degree = {v: 0 for v in self.vertices}
        for u in self.adj:
            for (v, _) in self.adj[u]:
                in_degree[v] += 1

        queue = deque([v for v in self.vertices if in_degree[v] == 0])
        topo = []
        while queue:
            u = queue.popleft()
            topo.append(u)
            for (v, _) in self.adj[u]:
                in_degree[v] -= 1
                if in_degree[v] == 0:
                    queue.append(v)

        if len(topo) != len(self.vertices):
            raise ValueError("Graph has a cycle, sort not possible")
        return topo

    def topological_sort_dfs(self):
        """DFS‑based topological sort (uses stack)."""
        visited = set()
        stack = []

        def dfs(v):
            visited.add(v)
            for (neighbor, _) in self.adj[v]:
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(v)

        for v in self.vertices:
            if v not in visited:
                dfs(v)
        return stack[::-1]   # reverse of finish order

    # ----------------------------------------------------------------------
    # Shortest Paths
    # ----------------------------------------------------------------------
    def dijkstra(self, start):
        """Dijkstra's algorithm using a priority queue (min‑heap).
        Returns (dist, prev)."""
        dist = {v: float('inf') for v in self.vertices}
        prev = {v: None for v in self.vertices}
        dist[start] = 0
        pq = [(0, start)]          # (distance, vertex)
        visited = set()

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            for (v, w) in self.adj[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    prev[v] = u
                    heapq.heappush(pq, (dist[v], v))
        return dist, prev

    def bellman_ford(self, start):
        """Bellman‑Ford algorithm (handles negative weights).
        Returns (dist, prev) or raises if negative cycle."""
        dist = {v: float('inf') for v in self.vertices}
        prev = {v: None for v in self.vertices}
        dist[start] = 0

        # Relax edges |V|-1 times
        for _ in range(len(self.vertices) - 1):
            for u in self.adj:
                for (v, w) in self.adj[u]:
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        prev[v] = u

        # Check for negative cycles
        for u in self.adj:
            for (v, w) in self.adj[u]:
                if dist[u] + w < dist[v]:
                    raise ValueError("Graph contains a negative‑weight cycle")

        return dist, prev

    # ----------------------------------------------------------------------
    # Minimum Spanning Tree
    # ----------------------------------------------------------------------
    def prim_mst(self, start):
        """Prim's algorithm (uses priority queue).
        Returns list of edges in MST."""

        if self.directed:
            raise ValueError("Prim's algorithm requires an undirected graph")
        mst_edges = []
        visited = set([start])
        # Priority queue of (weight, u, v) where u is in visited, v is not
        pq = []
        for (neighbor, w) in self.adj[start]:
            heapq.heappush(pq, (w, start, neighbor))

        while pq and len(visited) < len(self.vertices):
            w, u, v = heapq.heappop(pq)
            if v in visited:
                continue
            visited.add(v)
            mst_edges.append((u, v, w))
            for (next_n, w2) in self.adj[v]:
                if next_n not in visited:
                    heapq.heappush(pq, (w2, v, next_n))
        return mst_edges

    def kruskal_mst(self):
        """Kruskal's algorithm (uses Union‑Find).
        Returns list of edges in MST."""

        if self.directed:
            raise ValueError("Requires an undirected graph")

        # Build edge list
        edges = []
        for u in self.adj:
            for (v, w) in self.adj[u]:
                if (v, u, w) not in edges:   # avoid duplicates for undirected
                    edges.append((u, v, w))

        # Sort edges by weight – we will plug in any sorting algorithm later
        # import here to avoid circular dependency
        from sorting import merge_sort
        edges = merge_sort(edges, key=lambda e: e[2])

        parent = {v: v for v in self.vertices}
        rank = {v: 0 for v in self.vertices}

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]   # path compression
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

        mst_edges = []
        for (u, v, w) in edges:
            if union(u, v):
                mst_edges.append((u, v, w))
            if len(mst_edges) == len(self.vertices) - 1:
                break
        return mst_edges

    # ----------------------------------------------------------------------
    # Connectivity (SCC using Kosaraju)
    # ----------------------------------------------------------------------
    def kosaraju_scc(self):
        """Find strongly connected components using Kosaraju's algorithm."""
        # First pass: order by finish time (DFS on original graph)
        visited = set()
        stack = []

        def dfs1(v):
            visited.add(v)
            for (neighbor, _) in self.adj[v]:
                if neighbor not in visited:
                    dfs1(neighbor)
            stack.append(v)

        for v in self.vertices:
            if v not in visited:
                dfs1(v)

        # Build reversed graph
        rev_adj = {v: [] for v in self.vertices}
        for u in self.adj:
            for (v, _) in self.adj[u]:
                rev_adj[v].append((u, 0))   # weight ignored

        # Second pass: DFS on reversed graph in stack order
        visited.clear()
        sccs = []

        def dfs2(v, component):
            visited.add(v)
            component.append(v)
            for (neighbor, _) in rev_adj[v]:
                if neighbor not in visited:
                    dfs2(neighbor, component)

        while stack:
            v = stack.pop()
            if v not in visited:
                component = []
                dfs2(v, component)
                sccs.append(component)

        return sccs
