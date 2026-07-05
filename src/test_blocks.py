import unittest
from blocks import block_to_blocktype, BlockType


class TestBlocktoBlocktype(unittest.TestCase):
    def test_base_functions(self):
        heading1 = "# This is a heading"
        heading2 = "#### This is also a heading"

        self.assertEqual(block_to_blocktype(heading1), BlockType.HEADING)
        self.assertEqual(block_to_blocktype(heading2), BlockType.HEADING)

        code1 = "``` x = 12"

        code2 = "y = 120 ```"

        self.assertEqual(block_to_blocktype(code1), BlockType.CODE)
        self.assertEqual(block_to_blocktype(code2), BlockType.CODE)

        quote1 = ">To Be or Not to Be"

        quote2 = ">     That is the question"

        self.assertEqual(block_to_blocktype(quote1), BlockType.QUOTE)
        self.assertEqual(block_to_blocktype(quote2), BlockType.QUOTE)

        unordered1 = "- Bullet point 1"
        unordered2 = "- Bulletpoint 2"

        self.assertEqual(block_to_blocktype(unordered1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_blocktype(unordered2), BlockType.UNORDERED_LIST)

        ordered1 = "1. List"
        ordered2 = "1. Another List\n2. Another Element\n3. A third"

        self.assertEqual(block_to_blocktype(ordered1), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_blocktype(ordered2), BlockType.ORDERED_LIST)

        paragraph1 = "Just regular text"

        self.assertEqual(block_to_blocktype(paragraph1), BlockType.PARAGRAPH)
