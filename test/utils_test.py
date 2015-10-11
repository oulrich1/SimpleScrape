__author__ = 'oriahulrich'

import unittest
import scrape_pages

class TestUtil(unittest.TestCase):
    """
        Tests utility methods
    """

    """
    """
    def test_get_filename(self):
        expected = "buddy.html"
        url = "hey/there/buddy.php"
        self.assertEqual(scrape_pages.get_filename(url), expected)

        expected = "buddy.html"
        url = "hey/there/buddy/"
        self.assertEqual(scrape_pages.get_filename(url), expected)

        expected = "index.html"
        url = "/"
        self.assertEqual(scrape_pages.get_filename(url), expected)

