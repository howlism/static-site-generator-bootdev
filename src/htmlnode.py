class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        output = ""
        if not self.props or self.props == {}:
            return output
        for key in self.props:
            output += f' {key}="{self.props[key]}"'
        return output

    def __repr__(self) -> str:
        return (
            f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html})"
        )


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNodes must have a value")
        output = ""
        if self.props:
            prop_args = self.props_to_html()
            output = f"<{self.tag}{prop_args}>{self.value}</{self.tag}>"
        else:
            output = f"<{self.tag}>{self.value}</{self.tag}>"
        return output

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props_to_html})"


class ParentNode(HTMLNode):
    def __init__(
        self, tag: str, children: list[HTMLNode], props: dict[str, str] | None = None
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNodes must have a tag")
        if not self.children:
            raise ValueError("ParentNodes must have children")
        output = ""
        children_to_html_str = ""
        for child in self.children:
            children_to_html_str += child.to_html()
        if self.props:
            prop_args = self.props_to_html()
            output = f"<{self.tag}{prop_args}>{children_to_html_str}</{self.tag}>"
        else:
            output = f"<{self.tag}>{children_to_html_str}</{self.tag}>"
        return output
