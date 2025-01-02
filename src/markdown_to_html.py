from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_parser import markdown_to_blocks, block_to_block_type, text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from pprint import pprint


def markdown_heading_to_html_node(text):
    index = 0
    leaf_nodes = []
    while text[index] == "#":
        index += 1
    leaf_text = text[index + 1 :]
    text_nodes = text_to_textnodes(leaf_text)
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    node = ParentNode(f"h{index}", leaf_nodes, None)
    return node


def markdown_code_to_html_node(text):
    new_text = text[3:-3]
    new_text = new_text
    node = []
    text_node = TextNode(new_text, TextType.CODE)
    node.append(text_node_to_html_node(text_node))
    return ParentNode("pre", node, None)


def markdown_quote_to_text_node(text):
    leaf_text = text[2:]
    text_nodes = text_to_textnodes(leaf_text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    node = ParentNode("blockquote", leaf_nodes, None)
    return node


def markdown_unordered_list_to_text_node(text):
    text_list = text.split("\n")
    list_nodes = []
    for item in text_list:
        leaf_nodes = []
        cleaned_text = item.lstrip("-*").strip()
        text_nodes = text_to_textnodes(cleaned_text)
        for node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(node))
        list_nodes.append(ParentNode("li", leaf_nodes))
    node = ParentNode("ul", list_nodes, None)
    return node


def markdown_ordered_list_to_text_node(text):
    text_list = text.split("\n")
    list_nodes = []
    for item in text_list:
        leaf_nodes = []
        cleaned_text = item.lstrip("1234567890.").strip()
        text_nodes = text_to_textnodes(cleaned_text)
        for node in text_nodes:
            leaf_nodes.append(text_node_to_html_node(node))
        list_nodes.append(ParentNode("li", leaf_nodes))
    node = ParentNode("ol", list_nodes, None)
    return node


def markdown_paragraph_to_text_node(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode("p", leaf_nodes)


def markdown_to_html_node(text):
    blocks = markdown_to_blocks(text)
    nodes = []
    for block in blocks:
        type = block_to_block_type(block)
        match (type):
            case "heading":
                nodes.append(markdown_heading_to_html_node(block))
            case "code":
                nodes.append(markdown_code_to_html_node(block))
            case "quote":
                nodes.append(markdown_quote_to_text_node(block))
            case "unordered_list":
                nodes.append(markdown_unordered_list_to_text_node(block))
            case "ordered_list":
                nodes.append(markdown_ordered_list_to_text_node(block))
            case "paragraph":
                nodes.append(markdown_paragraph_to_text_node(block))

    return ParentNode("div", nodes)


text = """# Test Markdown Document

## Header Level 2

This is **bold text** and this is *italicized text* **bolded  2 **.


### Links Section

Here's a [link to OpenAI](https://www.openai.com) for testing purposes.

### Images Section

Below is an image placeholder for testing:

![Placeholder Image](https://via.placeholder.com/150)


#### Spacing Test

This paragraph is followed by multiple new lines to test formatting robustness.




This paragraph should appear after several blank lines.


### Mixed Content

Here is a bullet point list with formatting:

- **Bolded item**
- *Italicized item*

Here is a numbered list with a link:

1. Visit [OpenAI](https://www.openai.com).
2. See the image above.
3. Test **mixed styles** here.

> This is a wise quote

> This is another quote

```
print("Hello World!") 
print("Hello")
```
"""
# print(markdown_to_html_node(text))
