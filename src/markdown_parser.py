from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if delimiter not in text:
            print("here")
            new_nodes.append(node)
            continue
        result = text.count(delimiter)
        if result % 2 != 0:
            raise Exception(
                f"Non matching delimiter Type: {delimiter} found in Text: {text}"
            )
        else:
            new_text = text.split(delimiter)
            print(new_text)
            for i in range(0, len(new_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(new_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(new_text[i], text_type))
    return new_nodes


node = TextNode("This is *a text* node", TextType.NORMAL)
nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
string = ""
for node in nodes:
    html_node = text_node_to_html_node(node)
    string += html_node.to_html()

print(string)
