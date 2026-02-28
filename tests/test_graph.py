import unittest
import sys
from graph import Graph
import os

# Add parent directory to path so we can import the modules
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestGraph(unittest.TestCase):
    def setUp(self):
        # Create a simple undirected graph
        self.g = Graph(directed=False)
        for v in ['A', 'B', 'C', 'D']:
            self.g.add_vertex(v)
        self.g.add_edge('A', 'B', 1)
        self.g.add_edge('B', 'C', 2)
        self.g.add_edge('C', 'D', 1)

        # Directed graph for topological sort and cycle detection
        self.dg = Graph(directed=True)
        for v in [1, 2, 3, 4]:
            self.dg.add_vertex(v)
        self.dg.add_edge(1, 2)
        self.dg.add_edge(2, 3)
        self.dg.add_edge(3, 4)

    # ------------------------------------------------------------------
    # Basic operations
    # ------------------------------------------------------------------
    def test_add_vertex(self):
        self.g.add_vertex('E')
        self.assertIn('E', self.g.vertices)

    def test_add_edge(self):
        self.g.add_edge('A', 'D', 3)
        # Check adjacency for undirected
        self.assertIn(('D', 3), self.g.adj['A'])
        self.assertIn(('A', 3), self.g.adj['D'])

    def test_remove_edge(self):
        self.g.remove_edge('A', 'B')
        self.assertNotIn(('B', 1), self.g.adj['A'])
        self.assertNotIn(('A', 1), self.g.adj['B'])

    def test_remove_vertex(self):
        self.g.remove_vertex('C')
        self.assertNotIn('C', self.g.vertices)
        self.assertNotIn(('C', 1), self.g.adj['D'])
        self.assertNotIn(('C', 2), self.g.adj['B'])

    # ------------------------------------------------------------------
    # Traversals
    # ------------------------------------------------------------------
    def test_bfs(self):
        self.assertEqual(self.g.bfs('A'), ['A', 'B', 'C', 'D'])
        self.g.add_edge('A', 'D', 1)
        self.assertEqual(self.g.bfs('A'), ['A', 'B', 'D', 'C'])

    def test_dfs_iterative(self):
        self.g.add_edge('A', 'D', 1)
        self.g.add_edge('B', 'D', 1)
        result = self.g.dfs_iterative('A')
        self.assertEqual(set(result), {'A', 'B', 'C', 'D'})
        self.assertEqual(len(result), 4)

    def test_dfs_recursive(self):
        self.g.add_edge('A', 'D', 1)
        self.g.add_edge('B', 'D', 1)
        result = self.g.dfs_recursive('A')
        self.assertEqual(set(result), {'A', 'B', 'C', 'D'})
        self.assertEqual(len(result), 4)

    # ------------------------------------------------------------------
    # Cycle detection
    # ------------------------------------------------------------------
    def test_cycle_undirected(self):
        self.assertFalse(self.g.has_cycle_undirected())
        # Add an edge that creates a cycle
        self.g.add_edge('A', 'D', 2)
        self.assertTrue(self.g.has_cycle_undirected())

    def test_cycle_directed(self):
        self.dg.add_edge(1, 3)
        self.assertFalse(self.dg.has_cycle_directed())
        self.dg.add_edge(4, 1)
        self.assertTrue(self.dg.has_cycle_directed())

    # ------------------------------------------------------------------
    # Topological sort
    # ------------------------------------------------------------------
    def test_topological_sort_kahn(self):
        topo = self.dg.topological_sort_kahn()
        # Possible orders: [1,2,3,4] or [1,3,2,4] or [1,3,4,2]
        self.assertEqual(set(topo), {1, 2, 3, 4})
        # Check that all edges go forward
        pos = {v: i for i, v in enumerate(topo)}
        for u in self.dg.adj:
            for v, _ in self.dg.adj[u]:
                self.assertLess(pos[u], pos[v])

    def test_topological_sort_dfs(self):
        topo = self.dg.topological_sort_dfs()
        self.assertEqual(set(topo), {1, 2, 3, 4})
        pos = {v: i for i, v in enumerate(topo)}
        for u in self.dg.adj:
            for v, _ in self.dg.adj[u]:
                self.assertLess(pos[u], pos[v])

    def test_topological_sort_cycle_raises(self):
        self.dg.add_edge(4, 1)
        with self.assertRaises(ValueError):
            self.dg.topological_sort_kahn()

    # ------------------------------------------------------------------
    # Shortest paths
    # ------------------------------------------------------------------
    def test_dijkstra(self):
        self.g.add_edge('A', 'D', 3)
        dist, prev = self.g.dijkstra('A')
        self.assertEqual(dist['A'], 0)
        self.assertEqual(dist['B'], 1)
        self.assertEqual(dist['C'], 3)
        self.assertEqual(dist['D'], 3)

    def test_bellman_ford(self):
        dist, prev = self.g.bellman_ford('A')
        self.assertEqual(dist['A'], 0)
        self.assertEqual(dist['B'], 1)
        self.assertEqual(dist['C'], 3)
        self.assertEqual(dist['D'], 4)

    def test_bellman_ford_negative_cycle(self):
        # Create graph with negative cycle
        g = Graph(directed=True)
        g.add_edge(1, 2, 1)
        g.add_edge(2, 3, -2)
        g.add_edge(3, 1, -1)  # cycle 1->2->3->1 with total -2
        with self.assertRaises(ValueError):
            g.bellman_ford(1)

    # ------------------------------------------------------------------
    # Minimum Spanning Tree
    # ------------------------------------------------------------------
    def test_prim_mst(self):
        mst = self.g.prim_mst('A')
        # MST should have 3 edges (|V|-1) with total weight 1+2+1 = 4
        self.assertEqual(len(mst), 3)
        total_weight = sum(w for (_, _, w) in mst)
        self.assertEqual(total_weight, 4)

    def test_kruskal_mst(self):
        mst = self.g.kruskal_mst()
        self.assertEqual(len(mst), 3)
        total_weight = sum(w for (_, _, w) in mst)
        self.assertEqual(total_weight, 4)

    # ------------------------------------------------------------------
    # Strongly Connected Components (Kosaraju)
    # ------------------------------------------------------------------
    def test_kosaraju_scc(self):
        # Graph with two SCCs
        g = Graph(directed=True)
        g.add_edge(1, 2)
        g.add_edge(2, 1)
        g.add_edge(2, 3)
        g.add_edge(3, 4)
        g.add_edge(4, 3)
        sccs = g.kosaraju_scc()
        # Convert to frozenset for unordered comparison
        scc_sets = [frozenset(comp) for comp in sccs]
        self.assertIn(frozenset({1, 2}), scc_sets)
        self.assertIn(frozenset({3, 4}), scc_sets)


if __name__ == '__main__':
    unittest.main()
