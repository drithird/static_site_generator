from enum import Enum
from pydoc import TextDoc
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if delimiter not in text:
            new_nodes.append(node)
            continue
        result = text.count(delimiter)
        if result % 2 != 0:
            raise Exception(
                f"Non matching delimiter Type: {delimiter} found in Text: {text}"
            )
        else:
            new_text = text.split(delimiter)
            for i in range(0, len(new_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(new_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(new_text[i], text_type))
    return new_nodes


def extract_markdown_images(text):
    find_string = r"!\[([^)\[\]]*)]\(([^\(\)]*)\)"
    matches = re.findall(find_string, text)
    return matches


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extraction = extract_markdown_images(node.text)
        rounds = len(extraction)
        if rounds == 0:
            new_nodes.append(node)
            continue

        text = node.text

        for image in extraction:
            index1 = text.find(f"![{image[0]}]")
            index2 = text.find(f"({image[1]})")
            offset = index2 + len(f"({image[1]})")
            new_nodes.append(TextNode(text[:index1], node.text_type))
            new_nodes.append(TextNode(image[0], TextType.IMAGES, url=image[1]))
            text = text[offset:]
        if len(text) > 0:
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes


def extract_markdown_links(text):
    find_string = r"\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(find_string, text)
    return matches


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        extraction = extract_markdown_links(node.text)
        rounds = len(extraction)
        if rounds == 0:
            new_nodes.append(node)
            continue

        text = node.text

        for link in extraction:
            index1 = text.find(f"[{link[0]}]")
            index2 = text.find(f"({link[1]})")
            offset = index2 + len(f"({link[1]})")
            new_nodes.append(TextNode(text[:index1], node.text_type))
            new_nodes.append(TextNode(link[0], TextType.LINKS, url=link[1]))
            text = text[offset:]
        if len(text) > 0:
            new_nodes.append(TextNode(text, node.text_type))
    return new_nodes


def text_to_textnodes(text):
    nodes = []
    for type in TextType:
        match (type):
            case TextType.NORMAL:
                nodes.append(TextNode(text, TextType.NORMAL))
            case TextType.BOLD:
                new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
                nodes = new_nodes
            case TextType.ITALIC:
                new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
                nodes = new_nodes
            case TextType.CODE:
                new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
                nodes = new_nodes
            case TextType.LINKS:
                new_nodes = split_nodes_link(nodes)
                nodes = new_nodes
            case TextType.IMAGES:
                new_nodes = split_nodes_image(nodes)
                nodes = new_nodes
    return nodes
