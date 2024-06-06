import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        section = old_node.text.split(delimiter)
        if len(section) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(section)):
            if section[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section[i], text_type_text))
            else:
                split_nodes.append(TextNode(section[i], text_type))
        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_image(old_nodes):
    node_images = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            node_images.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            node_images.append(old_node)
            continue
        for image in images:
            section = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(section) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if section[0] != "":
                node_images.append(TextNode(section[0], text_type_text))
            node_images.append(
                TextNode(
                    image[0],
                    text_type_image,
                    image[1],
                )
            )
            original_text = section[1]
        if original_text != "":
            node_images.append(TextNode(original_text, text_type_text))

    return node_images


def split_nodes_link(old_nodes):
    node_links = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            node_links.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            node_links.append(old_node)
            continue
        for link in links:
            section = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(section) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if section[0] != "":
                node_links.append(TextNode(section[0], text_type_text))
            node_links.append(TextNode(link[0], text_type_link, link[1]))
            original_text = section[1]
        if original_text != "":
            node_links.append(TextNode(original_text, text_type_text))
    return node_links


def extract_markdown_images(text):
    markdown_images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return markdown_images


def extract_markdown_links(text):
    markdown_links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return markdown_links


def text_to_textnodes(text):
    textnodes = [TextNode(text, text_type_text)]
    textnodes = split_nodes_delimiter(textnodes, "**", text_type_bold)
    textnodes = split_nodes_delimiter(textnodes, "*", text_type_italic)
    textnodes = split_nodes_delimiter(textnodes, "`", text_type_code)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes
