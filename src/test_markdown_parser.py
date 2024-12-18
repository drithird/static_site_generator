from re import I
import unittest

from textnode import TextNode, TextType
from markdown_parser import split_nodes_delimiter


class Testsplit_nodes_delimiter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        print()


if __name__ == "__main__":
    unittest.main()
