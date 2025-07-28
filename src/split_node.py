from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            current_string = ""
            not_text = False
            delim_char = float("-inf")
            delim_len = len(delimiter)
            for i in range(len(node.text)):
                if i > delim_char:
                    if node.text[i : i + delim_len] == delimiter and not_text == True:
                        new_nodes.append(TextNode(current_string, text_type))
                        current_string = ""
                        not_text = False
                        delim_char = i + (delim_len - 1)
                    elif (
                        node.text[i : i + delim_len] == delimiter
                        and not_text == False
                        and current_string != ""
                    ):
                        new_nodes.append(TextNode(current_string, TextType.TEXT))
                        current_string = ""
                        not_text = True
                        delim_char = i + (delim_len - 1)
                    elif (
                        node.text[i : i + delim_len] == delimiter
                        and not_text == False
                        and current_string == ""
                    ):
                        not_text = True
                        delim_char = i + (delim_len - 1)
                    else:
                        current_string += node.text[i]
            if not_text == True:
                raise Exception("Invalid markdown syntax")
            if current_string != "":
                new_nodes.append(TextNode(current_string, TextType.TEXT))
                current_string = ""
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_images(old_nodes):
    splitted_list = []
    for node in old_nodes:
        extracted_data = extract_markdown_images(node.text)
        to_be_processed = node.text
        if extracted_data == []:
            splitted_list.append(node)
        else:
            for i in range(len(extracted_data)):
                image_data = extracted_data[i]
                image_alt = image_data[0]
                image_link = image_data[1]
                sections = to_be_processed.split(f"![{image_alt}] ({image_link})", 1)
                if len(sections) > 1:
                    if sections[0] != "":
                        splitted_list.append(TextNode(sections[0], TextType.TEXT))
                    splitted_list.append(
                        TextNode(image_alt, TextType.IMAGE, image_link)
                    )
                    to_be_processed = sections[1]
                else:
                    splitted_list.append(
                        TextNode(image_alt, TextType.IMAGE, image_link)
                    )
            if to_be_processed != "":
                splitted_list.append(TextNode(to_be_processed, TextType.TEXT))
    return splitted_list


def split_nodes_links(old_nodes):
    splitted_list = []
    for node in old_nodes:
        extracted_data = extract_markdown_links(node.text)
        to_be_processed = node.text
        if extracted_data == []:
            splitted_list.append(node)
        else:
            for i in range(len(extracted_data)):
                link_data = extracted_data[i]
                link_alt = link_data[0]
                link = link_data[1]
                sections = to_be_processed.split(f"[{link_alt}] ({link})", 1)
                if len(sections) > 1:
                    if sections[0] != "":
                        splitted_list.append(TextNode(sections[0], TextType.TEXT))
                    splitted_list.append(TextNode(link_alt, TextType.LINK, link))
                    to_be_processed = sections[1]
                else:
                    splitted_list.append(TextNode(link_alt, TextType.LINK, link))
            if to_be_processed != "":
                splitted_list.append(TextNode(to_be_processed, TextType.TEXT))
    return splitted_list


def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_images(text_nodes)
    text_nodes = split_nodes_links(text_nodes)
    return text_nodes
