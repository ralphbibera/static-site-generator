import re
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list["TextNode"], delimiter: str, text_type: TextType
):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        for i in range(len(sections)):
            if i % 2 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(sections[i], text_type))
    return new_nodes


def split_nodes_image(old_nodes: list["TextNode"]):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        original_text = old_node.text

        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(
                    TextNode(
                        image[0],
                        TextType.IMAGE,
                        image[1],
                    )
                )
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list["TextNode"]):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        original_text = old_node.text

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(
                    TextNode(
                        link[0],
                        TextType.LINK,
                        link[1],
                    )
                )
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def extract_markdown_images(text: str):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def text_to_textnodes(text: str) -> list["TextNode"]:
    node = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
