class HTMLNode:
    def __init__(
        self: "HTMLNode",
        tag: str = None,
        value: str = None,
        children: list["HTMLNode"] = None,
        props: dict[str, str] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_attributes = ""
        if self.props is not None:
            for key, value in self.props.items():
                html_attributes += f' {key}="{value}"'
        return html_attributes

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):

    def __init__(self: "LeafNode", tag: str, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("missing value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):

    def __init__(
        self: "ParentNode",
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("missing tag")
        if self.children is None:
            raise ValueError("missing children")
        html_children = ""
        for child in self.children:
            if child.value is None and type(child) is LeafNode:
                print(child)

            html_children += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{html_children}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
