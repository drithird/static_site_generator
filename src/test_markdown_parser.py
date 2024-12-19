from re import I
import unittest

from textnode import TextNode, TextType
from markdown_parser import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class Testsplit_nodes_delimiter(unittest.TestCase):
    def test_bold(self):
        answer_strings = [
            "TextNode(self.text: This is a  self.text_type: TextType.NORMAL self.url: None)",
            "TextNode(self.text: bold self.text_type: TextType.BOLD self.url: None)",
            "TextNode(self.text:  node self.text_type: TextType.NORMAL self.url: None)",
        ]
        node = TextNode("This is a *bold* node", TextType.NORMAL)
        nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        for i, node in enumerate(nodes):
            self.assertEqual(str(node), answer_strings[i])

    def test_italic(self):
        answer_strings = [
            "TextNode(self.text: This is a  self.text_type: TextType.NORMAL self.url: None)",
            "TextNode(self.text: italic self.text_type: TextType.ITALIC self.url: None)",
            "TextNode(self.text:  node self.text_type: TextType.NORMAL self.url: None)",
        ]
        node = TextNode("This is a **italic** node", TextType.NORMAL)
        nodes = split_nodes_delimiter([node], "**", TextType.ITALIC)
        for i, node in enumerate(nodes):
            self.assertEqual(str(node), answer_strings[i])

    def test_code(self):
        answer_strings = [
            "TextNode(self.text: This is a  self.text_type: TextType.NORMAL self.url: None)",
            "TextNode(self.text: code self.text_type: TextType.CODE self.url: None)",
            "TextNode(self.text:  node self.text_type: TextType.NORMAL self.url: None)",
        ]
        node = TextNode("This is a ```code``` node", TextType.NORMAL)
        nodes = split_nodes_delimiter([node], "```", TextType.CODE)
        for i, node in enumerate(nodes):
            self.assertEqual(str(node), answer_strings[i])


class Test_extract_markdown_images(unittest.TestCase):
    def test_parse(self):
        answer_string_list = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        string_list = extract_markdown_images(text)
        self.assertEqual(string_list, answer_string_list)


class Test_split_nodes_markdown_images(unittest.TestCase):
    def test_parse(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        test_answer = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGES, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.IMAGES, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, test_answer)


class Test_extract_markdown_links(unittest.TestCase):
    def test_parse(self):
        answer_string_list = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        string_list = extract_markdown_links(text)
        self.assertEqual(string_list, answer_string_list)


class Test_split_nodes_markdown_links(unittest.TestCase):
    def test_parse(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        test_answer = [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode(
                "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, test_answer)


class Test_text_to_textnodes(unittest.TestCase):
    def test_parse(self):
        nodes = text_to_textnodes(
            "This is **bold** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        )
        test_answer = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" with an ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.NORMAL),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.NORMAL),
            TextNode(
                "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.NORMAL),
            TextNode("link", TextType.LINKS, "https://boot.dev"),
        ]
        self.assertEqual(nodes, test_answer)


if __name__ == "__main__":
    unittest.main()
