from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    if (
        block[0:2] == "# "
        or block[0:3] == "## "
        or block[0:4] == "### "
        or block[0:5] == "#### "
        or block[0:6] == "###### "
        or block[0:7] == "####### "
    ):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    elif block[0] == ">":
        leading_char_check = True
        line_list = block.split("\n")
        for line in line_list:
            line = line.strip()
            if line[0] != ">":
                leading_char_check = False
        if leading_char_check == True:
            return BlockType.QUOTE
        else:
            return BlockType.PARAGRAPH

    elif block.startswith("- "):
        leading_char_check = True
        line_list = block.split("\n")
        for line in line_list:
            line = line.strip()
            if not line.startswith("- "):
                leading_char_check = False
        if leading_char_check == True:
            return BlockType.UNORDERED_LIST
        else:
            return BlockType.PARAGRAPH

    elif block.startswith("1."):
        leading_char_check = True
        line_list = block.split("\n")
        for i in range(len(line_list)):
            line = line_list[i]
            line = line.strip()
            if not line.startswith(f"{i + 1}."):
                leading_char_check = False
        if leading_char_check == True:
            return BlockType.ORDERED_LIST
        else:
            return BlockType.PARAGRAPH

    else:
        return BlockType.PARAGRAPH
