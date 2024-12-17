import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_create(self):
        html_node = HTMLNode(
            "h1", "Taco Bell", None, {"href": "www.google.com", "target": "_blank"}
        )
        self.assertIs(HTMLNode, type(html_node))

    def test_repr(self):
        html_node = HTMLNode(
            "h1", "Taco Bell", None, {"href": "www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            str(html_node),
            "HTMLNode(h1, Taco Bell, None, {'href': 'www.google.com', 'target': '_blank'})",
        )

    def test_Nones(self):
        html_node = HTMLNode()
        self.assertIs(HTMLNode, type(html_node))
        self.assertEqual(str(html_node), "HTMLNode(None, None, None, None)")


class TestLeafNode(unittest.TestCase):
    def test_create(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        self.assertIs(LeafNode, type(leaf_node))

    def test_repr(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            str(leaf_node), "LeafNode(p, This is a paragraph of text., None, None)"
        )

    def test_to_html(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf_node.to_html(), "<p>This is a paragraph of text.</p>")

        leaf_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            leaf_node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )


class TestParentNode(unittest.TestCase):
    def test_create(self):
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertIs(ParentNode, type(parent_node))

    def test_repr(self):
        test_string = "ParentNode(p, None, [LeafNode(b, Bold text, None, None), LeafNode(None, Normal text, None, None), LeafNode(i, italic text, None, None), LeafNode(None, Normal text, None, None)], None)"
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(str(parent_node), test_string)

    def test_to_html_1(self):
        test_string = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        parent_node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(parent_node.to_html(), test_string)

    def test_to_html_2(self):
        test_string = '<div><span><a href="http://example.com" target="_blank">Link</a><strong>Bold Text</strong></span><p>Paragraph text</p></div>'
        parent_node = ParentNode(
            tag="div",
            children=[
                ParentNode(
                    tag="span",
                    children=[
                        LeafNode(
                            "a",
                            "Link",
                            props={"href": "http://example.com", "target": "_blank"},
                        ),
                        LeafNode("strong", "Bold Text"),
                    ],
                ),
                LeafNode("p", "Paragraph text"),
            ],
        )
        self.assertEqual(parent_node.to_html(), test_string)


if __name__ == "__main__":
    unittest.main()
