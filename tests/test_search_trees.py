import unittest
import sys
from search_trees import AVLTree, TwoFourTree
import os

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestAVLTree(unittest.TestCase):
    def setUp(self):
        self.avl = AVLTree()
        self.keys = [10, 20, 30, 40, 50, 25]
        for k in self.keys:
            self.avl.insert(k, f"val_{k}")

    def test_insert_and_inorder(self):
        # Inorder should return keys in sorted order
        inorder = self.avl.inorder()
        self.assertEqual([k for k, _ in inorder], sorted(self.keys))

    def test_search(self):
        node = self.avl.search(30)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 30)
        self.assertEqual(node.value, "val_30")
        self.assertIsNone(self.avl.search(999))

    def test_delete_leaf(self):
        self.avl.delete(25)   # leaf
        inorder = self.avl.inorder()
        self.assertEqual([k for k, _ in inorder], [10, 20, 30, 40, 50])

    def test_delete_node_with_one_child(self):
        avl2 = AVLTree()
        for k in [10, 5, 15, 3]:
            avl2.insert(k)
        avl2.delete(5)
        self.assertIsNone(avl2.search(5))
        inorder = avl2.inorder()
        self.assertEqual([k for k, _ in inorder], [3, 10, 15])

    def test_delete_node_with_two_children(self):
        self.avl.delete(30)
        inorder = self.avl.inorder()
        self.assertEqual([k for k, _ in inorder], sorted([10, 20, 25, 40, 50]))

    def test_avl_invariant(self):
        # After each operation, the tree should be balanced.
        def check_balance(node):
            if not node:
                return True
            bf = self.avl.balance_factor(node)
            self.assertTrue(-1 <= bf <= 1)
            check_balance(node.left)
            check_balance(node.right)
        check_balance(self.avl.root)


class TestTwoFourTree(unittest.TestCase):
    def setUp(self):
        self.tt = TwoFourTree()
        self.keys = [10, 20, 30, 40, 50, 60, 70]
        for k in self.keys:
            self.tt.insert(k, f"val_{k}")

    def test_insert_and_search(self):
        for k in self.keys:
            self.assertEqual(self.tt.search(k), f"val_{k}")
        self.assertIsNone(self.tt.search(999))

    def test_structure(self):
        def collect(node):
            if node is None:
                return []
            keys = node.keys[:]
            for child in node.children:
                keys.extend(collect(child))
            return keys
        all_keys = collect(self.tt.root)
        self.assertEqual(set(all_keys), set(self.keys))

    # Note: deletion is not implemented in (2,4) tree, so we skip it.


if __name__ == '__main__':
    unittest.main()
