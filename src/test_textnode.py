import unittest

from textnode import TextNode, TextType
from enum import Enum


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        string = str(node)
        self.assertEqual(len(string) > 10, True)

    def test_dtype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertTrue(type(node.text) is str)
        self.assertTrue(type(node.text_type) is TextType)
        self.assertTrue(node.url is None)


if __name__ == "__main__":
    unittest.main()
