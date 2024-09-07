"""Tests for index pagination."""

import unittest

from fernpress.pagination import paginate


class PaginationTests(unittest.TestCase):
    def test_items_are_chunked(self) -> None:
        self.assertEqual(paginate([1, 2, 3, 4, 5], 2), [[1, 2], [3, 4], [5]])

    def test_exact_multiple_keeps_the_last_page(self) -> None:
        self.assertEqual(paginate([1, 2, 3, 4], 2), [[1, 2], [3, 4]])

    def test_empty_sequence_has_no_pages(self) -> None:
        self.assertEqual(paginate([], 2), [])

    def test_non_positive_page_size_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            paginate([1], 0)


if __name__ == "__main__":
    unittest.main()
