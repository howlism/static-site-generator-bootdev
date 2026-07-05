from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def block_to_blocktype(block: str) -> BlockType:
    if match_heading(block):
        return BlockType.HEADING
    elif block.startswith("```") or block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE
    elif block.startswith("- "):
        return BlockType.UNORDERED_LIST
    elif match_digits(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def match_digits(block: str) -> bool:
    lines = block.split("\n")
    p = 0
    for line in lines:
        matches = re.findall(r"\d*\.", line)
        if not matches:
            return False
        if int(matches[0].strip(".")) == p + 1:
            print("True")
            p = int(matches[0].strip("."))
        else:
            return False
    if p == len(lines):
        return True
    return False


def match_heading(block: str) -> bool:
    p = 0
    for char in block:
        if char == "#":
            p += 1
        elif char == " ":
            if p > 0 and p <= 6:
                return True
            return False
        else:
            return False
    return False
