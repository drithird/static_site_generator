class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        string = ""
        if self.props is not None:
            for item in self.props:
                string += f' {item}="{self.props[item]}"'
            return string
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError(f"No tag found in Node {str(self)} and is required")
        if self.children is None:
            raise ValueError(f"No children found in Node {str(self)} and is required")
        string = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            string += child.to_html()
        string += f"</{self.tag}>"
        return string

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError(f"No value found in Node {str(self)} and is required")
        if self.tag is None:
            return str(self.value)
        string = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return string

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"
