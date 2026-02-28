import unittest
import sys
from graph import Graph
from backtracking import all_paths, hamiltonian_path
import os

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestBacktracking(unittest.TestCase):
    def setUp(self):
        self.g = Graph(directed=False)
        for v in [1, 2, 3, 4]:
            self.g.add_vertex(v)
        self.g.add_edge(1, 2)
        self.g.add_edge(1, 3)
        self.g.add_edge(2, 4)
        self.g.add_edge(3, 4)

    def test_all_paths(self):
        paths = all_paths(self.g, 1, 4)
        # There should be two paths: 1-2-4 and 1-3-4
        self.assertEqual(len(paths), 2)
        self.assertIn([1, 2, 4], paths)
        self.assertIn([1, 3, 4], paths)

    def test_all_paths_with_max_depth(self):
        paths = all_paths(self.g, 1, 4, max_depth=2)
        # max_depth=2 means path length ≤ 2 (start to end = 2 edges),
        # so both paths allowed
        self.assertEqual(len(paths), 2)
        paths = all_paths(self.g, 1, 4, max_depth=1)  # only 1 edge, impossible
        self.assertEqual(len(paths), 0)

    def test_hamiltonian_path_exists(self):
        # Line graph P4
        line = Graph(directed=False)
        for v in ['P', 'Q', 'R', 'S']:
            line.add_vertex(v)
        line.add_edge('P', 'Q')
        line.add_edge('Q', 'R')
        line.add_edge('R', 'S')
        path = hamiltonian_path(line)
        self.assertIsNotNone(path)
        self.assertEqual(set(path), {'P', 'Q', 'R', 'S'})

    def test_hamiltonian_path_no_path(self):
        # Disconnected graph
        disc = Graph(directed=False)
        disc.add_vertex(1)
        disc.add_vertex(2)
        disc.add_vertex(3)
        disc.add_edge(1, 2)
        # vertex 3 isolated
        path = hamiltonian_path(disc)
        self.assertIsNone(path)


if __name__ == '__main__':
    unittest.main()
