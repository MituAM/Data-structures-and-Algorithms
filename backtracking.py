"""
Backtracking algorithms module.
"""


def all_paths(graph, start, end, max_depth=None):
    """
    Find all simple paths from start to end using backtracking.
    Returns list of paths (each path is a list of vertices).
    """
    paths = []
    current_path = [start]

    def backtrack(vertex):
        if vertex == end:
            paths.append(list(current_path))
            return
        if max_depth is not None and len(current_path) > max_depth:
            return
        for (neighbor, _) in graph.adj[vertex]:
            if neighbor not in current_path:   # avoid cycles
                current_path.append(neighbor)
                backtrack(neighbor)
                current_path.pop()

    backtrack(start)
    return paths


def hamiltonian_path(graph):
    """
    Find a Hamiltonian path (visits every vertex exactly once) if it exists.
    Returns a path as list, or None.
    """
    n = len(graph.vertices)
    vertices = list(graph.vertices)
    # We'll try starting from each vertex
    for start in vertices:
        path = [start]
        visited = set([start])

        def backtrack():
            if len(path) == n:
                return True
            last = path[-1]
            for (neighbor, _) in graph.adj[last]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    if backtrack():
                        return True
                    path.pop()
                    visited.remove(neighbor)
            return False

        if backtrack():
            return path
    return None
