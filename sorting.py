"""
Sorting algorithms module.
Provides implementations of:
    selection, insertion, heap, merge, quick, bucket, and radix sort.
All functions modify the input list in‑place and return it (for convenience).
"""


def selection_sort(arr, key=lambda x: x):
    """Selection sort: O(n^2) time, O(1) space."""
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if key(arr[j]) < key(arr[min_idx]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr, key=lambda x: x):
    """Insertion sort: O(n^2) time, O(1) space."""
    for i in range(1, len(arr)):
        curr = arr[i]
        j = i - 1
        while j >= 0 and key(curr) < key(arr[j]):
            arr[j+1] = arr[j]
            j -= 1
        arr[j+1] = curr
    return arr


def heap_sort(arr, key=lambda x: x):
    """Heap sort: O(n log n) time, O(1) space (iterative)."""
    import heapq
    # Build a min‑heap of (key, original) pairs to sort in ascending order
    heap = [(key(val), i, val) for i, val in enumerate(arr)]
    heapq.heapify(heap)
    for i in range(len(arr)):
        arr[i] = heapq.heappop(heap)[2]
    return arr


def merge_sort(arr, key=lambda x: x):
    """Merge sort: O(n log n) time, O(n) space (recursive)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key)
    right = merge_sort(arr[mid:], key)
    # merge
    i = j = k = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        k += 1
    return arr


def quick_sort(arr, key=lambda x: x, low=0, high=None):
    """Quick sort (in‑place, recursive). Average O(n log n), worst O(n²)."""
    if high is None:
        high = len(arr) - 1
    if low < high:
        pi = partition(arr, key, low, high)
        quick_sort(arr, key, low, pi-1)
        quick_sort(arr, key, pi+1, high)
    return arr


def partition(arr, key, low, high):
    """Lomuto partition scheme."""
    pivot = key(arr[high])
    i = low - 1
    for j in range(low, high):
        if key(arr[j]) <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return i+1


def bucket_sort(arr, key=lambda x: x, num_buckets=10):
    """
    Bucket sort: distributes elements into buckets, sorts each bucket.
    Assumes key returns a number in [0,1) for typical use; adjust as needed.
    """
    if not arr:
        return arr
    # Find min and max to scale into [0,1)
    vals = [key(x) for x in arr]
    min_val, max_val = min(vals), max(vals)
    if min_val == max_val:
        return arr
    # Create buckets
    buckets = [[] for _ in range(num_buckets)]
    for item in arr:
        idx = int((key(item) - min_val) /
                  (max_val - min_val) * (num_buckets - 1))
        buckets[idx].append(item)
    # Sort each bucket (using insertion sort)
    result = []
    for bucket in buckets:
        result.extend(insertion_sort(bucket, key))
    # Copy back to original list
    for i, val in enumerate(result):
        arr[i] = val
    return arr


def radix_sort(arr, key=lambda x: x, base=10):
    """
    Radix sort (LSD) for non‑negative integers. If key returns non‑integer,
    this will need adaptation. Here we assume key returns int.
    """
    if not arr:
        return arr
    # Find maximum value to determine number of digits
    max_val = max(key(x) for x in arr)
    exp = 1
    while max_val // exp > 0:
        counting_sort_by_digit(arr, key, exp, base)
        exp *= base
    return arr


def counting_sort_by_digit(arr, key, exp, base):
    """A stable counting sort based on a specific digit (for radix sort)."""
    n = len(arr)
    output = [0] * n
    count = [0] * base

    # Store count of occurrences
    for item in arr:
        digit = (key(item) // exp) % base
        count[digit] += 1

    # Change count[i] so it contains actual position of this digit in output
    for i in range(1, base):
        count[i] += count[i-1]

    # Build output array (from end to maintain stability)
    for i in range(n-1, -1, -1):
        digit = (key(arr[i]) // exp) % base
        output[count[digit] - 1] = arr[i]
        count[digit] -= 1

    # Copy back
    for i in range(n):
        arr[i] = output[i]
