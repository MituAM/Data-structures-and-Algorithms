import unittest
import sys
from sorting import (
    selection_sort, insertion_sort, heap_sort,
    merge_sort, quick_sort, bucket_sort, radix_sort
)
import os

sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestSorting(unittest.TestCase):
    def setUp(self):
        self.unsorted = [64, 34, 25, 12, 22, 11, 90]
        self.sorted_asc = [11, 12, 22, 25, 34, 64, 90]
        self.reverse = [90, 64, 34, 25, 22, 12, 11]
        self.duplicates = [5, 1, 4, 2, 2, 3]
        self.sorted_dups = [1, 2, 2, 3, 4, 5]
        self.floats = [0.42, 0.32, 0.73, 0.12, 0.89, 0.54]
        self.sorted_floats = [0.12, 0.32, 0.42, 0.54, 0.73, 0.89]
        self.radix_input = [170, 45, 75, 90, 2, 24, 802, 66]
        self.radix_sorted = [2, 24, 45, 66, 75, 90, 170, 802]

    def test_selection_sort(self):
        arr = self.unsorted.copy()
        self.assertEqual(selection_sort(arr), self.sorted_asc)
        self.assertEqual(selection_sort(self.reverse.copy()), self.sorted_asc)
        self.assertEqual(selection_sort(self.duplicates.copy()),
                         self.sorted_dups)

    def test_insertion_sort(self):
        arr = self.unsorted.copy()
        self.assertEqual(insertion_sort(arr), self.sorted_asc)
        self.assertEqual(insertion_sort(self.reverse.copy()), self.sorted_asc)
        self.assertEqual(insertion_sort(self.duplicates.copy()),
                         self.sorted_dups)

    def test_heap_sort(self):
        arr = self.unsorted.copy()
        self.assertEqual(heap_sort(arr), self.sorted_asc)
        self.assertEqual(heap_sort(self.reverse.copy()), self.sorted_asc)
        self.assertEqual(heap_sort(self.duplicates.copy()), self.sorted_dups)

    def test_merge_sort(self):
        arr = self.unsorted.copy()
        self.assertEqual(merge_sort(arr), self.sorted_asc)
        self.assertEqual(merge_sort(self.reverse.copy()), self.sorted_asc)
        self.assertEqual(merge_sort(self.duplicates.copy()), self.sorted_dups)

    def test_quick_sort(self):
        arr = self.unsorted.copy()
        self.assertEqual(quick_sort(arr), self.sorted_asc)
        self.assertEqual(quick_sort(self.reverse.copy()), self.sorted_asc)
        self.assertEqual(quick_sort(self.duplicates.copy()), self.sorted_dups)

    def test_bucket_sort(self):
        arr = self.floats.copy()
        # Bucket sort with default num_buckets=10
        result = bucket_sort(arr, key=lambda x: x, num_buckets=5)
        self.assertEqual(result, self.sorted_floats)

    def test_radix_sort(self):
        arr = self.radix_input.copy()
        self.assertEqual(radix_sort(arr), self.radix_sorted)

    def test_empty_input(self):
        self.assertEqual(selection_sort([]), [])
        self.assertEqual(insertion_sort([]), [])
        self.assertEqual(heap_sort([]), [])
        self.assertEqual(merge_sort([]), [])
        self.assertEqual(quick_sort([]), [])
        self.assertEqual(bucket_sort([]), [])
        self.assertEqual(radix_sort([]), [])

    def test_single_element(self):
        self.assertEqual(selection_sort([5]), [5])
        self.assertEqual(insertion_sort([5]), [5])
        self.assertEqual(heap_sort([5]), [5])
        self.assertEqual(merge_sort([5]), [5])
        self.assertEqual(quick_sort([5]), [5])
        self.assertEqual(bucket_sort([5]), [5])
        self.assertEqual(radix_sort([5]), [5])


if __name__ == '__main__':
    unittest.main()
