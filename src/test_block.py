import unittest
from blocktype import BlockType, block_to_block_type


class TestBlock(unittest.TestCase):
    def test_heading(self):
        block = "# this is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading2(self):
        block = "### this is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = "```this is code block```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = ">this is quote block\n>and another one\n>and also a 3rd"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- this is an unordered list\n- and an item\n- also an item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_not_unordered_list(self):
        block = "- this is an unordered list\nand an item\n- also an item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1.this is an ordered list\n2.and an item\n3.also an item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_not_ordered_list(self):
        block = "1.this is not an ordered list\n2.and an item\n5.also an item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
