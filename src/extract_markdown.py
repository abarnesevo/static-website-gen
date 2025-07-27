import re


def extract_markdown_images(text):
    extracted_list = []
    alt_matches = re.findall(r"!\[(.*?)\]", text)
    url_matches = re.findall(r"\((.*?)\)", text)
    for i in range(len(alt_matches)):
        matches = (alt_matches[i], url_matches[i])
        extracted_list.append(matches)

    return extracted_list


def extract_markdown_links(text):
    extracted_list = []
    alt_matches = re.findall(r"\[(.*?)\]", text)
    url_matches = re.findall(r"\((.*?)\)", text)
    for i in range(len(alt_matches)):
        matches = (alt_matches[i], url_matches[i])
        extracted_list.append(matches)

    return extracted_list


def markdown_to_blocks(markdown):
    stripped_blocks = []
    splitted_blocks = markdown.split("\n\n")
    for block in splitted_blocks:
        stripped_block = block.strip()
        if stripped_block != "":
            stripped_blocks.append(stripped_block)
    return stripped_blocks
