from htmlnode import ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from blocktype import block_to_block_type, BlockType
from split_node import text_to_textnodes
from extract_markdown import markdown_to_blocks


def text_to_children(markdown):
    text_nodes = text_to_textnodes(markdown)
    html_nodes = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def heading_to_html_node(markdown):
    if markdown.startswith("#######"):
        raise Exception("invalid heading")
    elif markdown.startswith("######"):
        return ParentNode("h6", text_to_children(markdown[7:]))
    elif markdown.startswith("#####"):
        return ParentNode("h5", text_to_children(markdown[6:]))
    elif markdown.startswith("####"):
        return ParentNode("h4", text_to_children(markdown[5:]))
    elif markdown.startswith("###"):
        return ParentNode("h3", text_to_children(markdown[4:]))
    elif markdown.startswith("##"):
        return ParentNode("h2", text_to_children(markdown[3:]))
    elif markdown.startswith("#"):
        return ParentNode("h1", text_to_children(markdown[2:]))
    else:
        raise Exception("invalid heading")


def code_to_html_node(markdown):
    text_node = TextNode(markdown[4:-3], TextType.CODE)
    parent_node = text_node_to_html_node(text_node)
    return ParentNode("pre", [parent_node])


def quote_to_html_node(markdown):
    new_lines = []
    lines = markdown.split("\n")
    for line in lines:
        if not line.startswith(">"):
            raise Exception("invalid quote")
        new_lines.append(line.lstrip(">").strip())
    quote = " ".join(new_lines)
    return ParentNode("block quote", text_to_children(quote))


def paragraph_to_html_node(markdown):
    lines = markdown.split("\n")
    new_markdown = " ".join(lines)
    return ParentNode("p", text_to_children(new_markdown))


def ordered_list_to_html_node(markdown):
    list_items = markdown.split("\n")
    children = []
    for i in range(len(list_items)):
        if not list_items[i].startswith(f"{i + 1}."):
            raise Exception("incorrect list syntax")
        children.append(ParentNode("li", text_to_children(list_items[i][2:])))
    return ParentNode("ol", children)


def unordered_list_to_html_node(markdown):
    list_items = markdown.split("\n")
    children = []
    for i in range(len(list_items)):
        if not list_items[i].startswith("- "):
            raise Exception("incorrect list syntax")
        children.append(ParentNode("li", text_to_children(list_items[i][2:])))
    return ParentNode("ul", children)


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        if block.block_type == BlockType.HEADING:
            children.append(heading_to_html_node(block))
        elif block.block_type == BlockType.CODE:
            children.append(code_to_html_node(block))
        elif block.block_type == BlockType.QUOTE:
            children.append(quote_to_html_node(block))
        elif block.block_type == BlockType.PARAGRAPH:
            children.append(paragraph_to_html_node(block))
        elif block.block_type == BlockType.ORDERED_LIST:
            children.append(ordered_list_to_html_node(block))
        else:
            children.append(unordered_list_to_html_node(block))
    return ParentNode("div", children)
