import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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


class TestTexttoHtml(unittest.TestCase):
    def test_Text(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        result = text_node_to_html_node(node)
        self.assertEqual(str(result), "LeafNode(None, This is a text node, None, None)")

    def test_Bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        result = text_node_to_html_node(node)
        self.assertEqual(str(result), "LeafNode(b, This is a bold node, None, None)")

    def test_Italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        result = text_node_to_html_node(node)
        self.assertEqual(str(result), "LeafNode(i, This is a italic node, None, None)")

    def test_Code(self):
        node = TextNode("This is a code node", TextType.CODE)
        result = text_node_to_html_node(node)
        self.assertEqual(str(result), "LeafNode(code, This is a code node, None, None)")

    def test_Link(self):
        node = TextNode("This is a link node", TextType.LINKS, url="www.example.com")
        result = text_node_to_html_node(node)
        self.assertEqual(
            str(result),
            "LeafNode(a, This is a link node, None, {'href': 'www.example.com'})",
        )

    def test_Italic(self):
        node = TextNode("This is a image node", TextType.IMAGES, url="www.example.com")
        result = text_node_to_html_node(node)
        self.assertEqual(
            str(result),
            "LeafNode(img, , None, {'src': 'www.example.com', 'alt': 'This is a image node'})",
        )


if __name__ == "__main__":
    unittest.main()
