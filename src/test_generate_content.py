import unittest

from generate_content import extract_title


class TestGenerateContent(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Title
"""
        title = extract_title(md)
        self.assertEqual(title, "Title")


if __name__ == "__main__":
    unittest.main()
