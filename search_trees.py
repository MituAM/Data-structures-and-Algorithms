"""
Search trees module.
Implements AVL tree and (2,4) tree (B‑tree of order 4).
"""


class AVLNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    """Self‑balancing AVL tree."""
    def __init__(self):
        self.root = None

    def height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))

    def balance_factor(self, node):
        return self.height(node.left) - self.height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        self.update_height(x)
        self.update_height(y)
        return y

    def balance(self, node):
        bf = self.balance_factor(node)
        # Left heavy
        if bf > 1:
            if self.balance_factor(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        # Right heavy
        if bf < -1:
            if self.balance_factor(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def insert(self, key, value=None):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if not node:
            return AVLNode(key, value)
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # Key already exists; update value
            node.value = value
            return node
        self.update_height(node)
        return self.balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node to be deleted
            if not node.left:
                return node.right
            if not node.right:
                return node.left
            # Node with two children: get inorder successor
            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)

        self.update_height(node)
        return self.balance(node)

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)


# ----------------------------------------------------------------------
# (2,4) Tree (simplified as a B‑tree of order 4)
# ----------------------------------------------------------------------
class TwoFourNode:
    def __init__(self):
        self.keys = []      # list of keys (size 1..3)
        self.children = []  # list of child nodes (size len(keys)+1)
        self.values = []    # values associated with keys (parallel to keys)


class TwoFourTree:
    """(2,4) tree: each node has 1‑3 keys and 2‑4 children."""
    def __init__(self):
        self.root = None

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        # Find first key >= key
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]
        # If leaf, not found
        if not node.children:
            return None
        # Recurse into appropriate child
        return self._search(node.children[i], key)

    def insert(self, key, value):
        if self.root is None:
            self.root = TwoFourNode()
            self.root.keys = [key]
            self.root.values = [value]
            return
        # Insert recursively, splitting nodes as needed
        node, new_key, new_value, new_child = self._insert_rec(
            self.root, key, value)
        if new_key is not None:   # root was split
            new_root = TwoFourNode()
            new_root.keys = [new_key]
            new_root.values = [new_value]
            new_root.children = [node, new_child]
            self.root = new_root

    def _insert_rec(self, node, key, value):
        # returns (node, new_key, new_value, new_child) if split
        # otherwise (node, None, None, None)
        if not node.children:   # leaf
            # Insert key into leaf
            pos = 0
            while pos < len(node.keys) and key > node.keys[pos]:
                pos += 1
            node.keys.insert(pos, key)
            node.values.insert(pos, value)
            if len(node.keys) <= 3:
                return node, None, None, None
            else:
                # Split leaf
                left = TwoFourNode()
                right = TwoFourNode()
                mid = len(node.keys) // 2
                left.keys = node.keys[:mid]
                left.values = node.values[:mid]
                right.keys = node.keys[mid+1:]
                right.values = node.values[mid+1:]
                # Promote middle key
                return left, node.keys[mid], node.values[mid], right
        else:
            # Find child to insert into
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1
            child = node.children[i]
            child, new_key, new_value, new_child = self._insert_rec(
                child, key, value)
            if new_key is None:
                return node, None, None, None
            # Insert promoted key into current node
            node.keys.insert(i, new_key)
            node.values.insert(i, new_value)
            # new_child becomes right child of new_key
            node.children.insert(i+1, new_child)
            if len(node.keys) <= 3:
                return node, None, None, None
            else:
                # Split internal node
                left = TwoFourNode()
                right = TwoFourNode()
                mid = len(node.keys) // 2
                left.keys = node.keys[:mid]
                left.values = node.values[:mid]
                left.children = node.children[:mid+1]
                right.keys = node.keys[mid+1:]
                right.values = node.values[mid+1:]
                right.children = node.children[mid+1:]
                return left, node.keys[mid], node.values[mid], right
