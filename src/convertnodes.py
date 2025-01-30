import re
from enum import Enum
from htmlnode import HTMLNode, LeafNode
from textnode import TextType, TextNode

# Converts TextNode to HTML LeafNode
def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a recognized text type")

# Converts raw text into TextNode using the other defined functions in sequence
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

# Takes list of TextNodes (old_nodes) that are TextType.TEXT, a string (delimiter), and a TextType (text_type)
# Splits the TextNodes that contain markdown, splits them by their delimiter, and changes the TextType of the
# markdown text to the entered text_type.
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        delim_count = node.text.count(delimiter)
        
        if delim_count % 2 != 0:
            raise ValueError("Invalid Markdown Syntax -- Missing Closing Delimiter")
        
        if node.text_type != TextType.TEXT or delim_count == 0:
            new_nodes.append(node)
            continue
        
        split_node_text = node.text.split(delimiter)

        for i in range(len(split_node_text)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_node_text[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(split_node_text[i], text_type))

    return new_nodes

# Takes raw markdown text and returns a list of tuples.
# Each tuple contains the alt text and the URL of markdown images
def extract_markdown_images(text):
    image = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return image

# Takes raw markdown text and returns a list of tuples.
# Each tuple contains the anchor text and URL of markdown links
def extract_markdown_links(text):
    link = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return link

# Splits text nodes containing image markdown into text nodes and image nodes
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
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

# Splits text nodes containing link markdown into text nodes and link nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes