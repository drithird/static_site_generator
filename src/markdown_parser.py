from enum import Enum
from pydoc import TextDoc
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode
import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


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


def markdown_to_blocks(markdown):
    new_markdown = markdown.strip()
    new_markdown = new_markdown.split("\n")
    block_end = False
    current_block = []
    all_blocks = []
    for line in new_markdown:
        if len(line) == 0:
            if block_end == False and len(current_block) > 0:
                all_blocks.append("\n".join(current_block))
                current_block = []
            block_end = True
            continue
        block_end = False
        current_block.append(line.strip())
    if len(current_block) > 0:
        all_blocks.append("".join(current_block))
    return all_blocks


def block_to_block_type(single_block):
    # Heading Block Parsing
    if single_block[0] == "#":
        i = 1
        while True:
            char = single_block[i]
            if char == "#":
                i += 1
            elif char == " ":
                return "heading"
            else:
                return "paragraph"

    # Code Block Processing
    elif single_block[0] == "`":
        ticks = [
            single_block[1],
            single_block[2],
            single_block[-1],
            single_block[-2],
            single_block[-3],
        ]
        for tick in ticks:
            if tick != "`":
                return "paragraph"
        return "code"

    # Quote Block Processing
    elif single_block[0] == ">":
        quotes = single_block.split("\n")
        for quote in quotes:
            if quote[0] != ">":
                return "paragraph"
        return "quote"

    # Unordered List Block Processing
    elif single_block[0:2] == "* " or single_block[0:2] == "- ":
        unordered_list = single_block.split("\n")
        for item in unordered_list:
            if item[0:2] != "* " and item[0:2] != "- ":
                return "paragraph"
        return "unordered_list"

    # Ordered List Block Processing
    elif single_block[0] == "1":
        ordered_list = single_block.split("\n")
        for item in ordered_list:
            if not (str(item[0]).isnumeric()) or item[1:3] != ". ":
                return "paragraph"
        return "ordered_list"

    else:
        return "paragraph"


text = """# Test Markdown Document

## Header Level 2

This is **bold text** and this is *italicized text*.


### Links Section

Here's a [link to OpenAI](https://www.openai.com) for testing purposes.

### Images Section

Below is an image placeholder for testing:

![Placeholder Image](https://via.placeholder.com/150 "Placeholder Image")


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
```
"""

# print(markdown_to_blocks(text))

# blocks = markdown_to_blocks(text)
# answers = []
# for block in blocks:
#    answers.append(block_to_block_type(block))

# print(answers)
