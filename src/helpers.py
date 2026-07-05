from textnode import TextNode, TextType
import re


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    output = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            output.append(node)
            continue
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise SyntaxError("Invalid markdown syntax")
        for i in range(len(split_node)):
            if i % 2 == 0 or i == 0:
                output.append(TextNode(split_node[i], TextType.PLAIN))
            else:
                output.append(TextNode(split_node[i], text_type))
    return output


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        text = node.text
        if not matches:
            output.append(node)
            continue
        for match in matches:
            image_alt = match[0]
            image_link = match[1]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            output.append(TextNode(sections[0], TextType.PLAIN))
            output.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[1]
        if sections[1] != "":
            output.append(TextNode(sections[1], TextType.PLAIN))

    return output


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    output = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        text = node.text
        if not matches:
            output.append(node)
            continue
        for match in matches:
            link_text = match[0]
            link_url = match[1]
            sections = text.split(f"[{link_text}]({link_url})", 1)
            output.append(TextNode(sections[0], TextType.PLAIN))
            output.append(TextNode(link_text, TextType.LINK, link_url))
            text = sections[1]
        if sections[1] != "":
            output.append(TextNode(sections[1], TextType.PLAIN))
    return output


def text_to_textnodes(text: str) -> list[TextNode]:
    delimiters = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}
    new_nodes = [TextNode(text, TextType.PLAIN)]
    for delimiter in delimiters:
        if delimiter in text:
            nodes = split_nodes_delimiter(new_nodes, delimiter, delimiters[delimiter])
            new_nodes = nodes

    for node in new_nodes:
        img_matches = extract_markdown_images(node.text)
        link_matches = extract_markdown_links(node.text)

    if img_matches:
        new_nodes = split_nodes_image(new_nodes)
    if link_matches:
        new_nodes = split_nodes_link(new_nodes)

    return new_nodes
