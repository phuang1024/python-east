#
#  Python EAST
#  Python module for parsing many languages into ASTs.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import io
import string
from typing import List, Dict
from ..common import Element


class Tree(Element):
    """
    Tree representation of one Markdown file.
    """

    content: List

    def __init__(self, content: List = []):
        self.content = content


class Header(Element):
    """
    Contains a header in Markdown (line that starts with "#")
    """

    size: int
    text: str

    def __init__(self, size: int = 1, text: str = ""):
        self.size = size
        self.text = text

    @staticmethod
    def is_header(line: str):
        if len(line) == 0:
            return False

        hashtag_cnt = 0
        for char in line:
            if char == "#":
                # Increment count and check bounds
                hashtag_cnt += 1
                if hashtag_cnt >= 7:
                    return False

            elif hashtag_cnt > 0 and char == " ":
                # Reached the end of hashtags
                return True

            elif hashtag_cnt > 0 and char != " ":
                # Non space right after hashtags
                return False

            elif hashtag_cnt == 0 and char != " ":
                # A non space character before hashtags
                return False

        # True if line only contains hashtags
        return True

    @staticmethod
    def header_size(line: str):
        """
        Assumes the line is already a header.
        You can check with Header.is_header(line)
        """

        count = 0
        for char in line:
            if char == "#":
                count += 1
            elif char != "#" and count > 0:
                break

        return count

    @staticmethod
    def header_text(line: str):
        count = 0
        for i, char in enumerate(line):
            if char == "#":
                count += 1
            elif char != "#" and count > 0:
                break

        return line[i:].strip()


def parse(data: str, special: Dict):
    tree = Tree()

    lines = data.split("\n")
    i = 0
    while len(lines) > 0:
        line = lines.pop(0)

        if Header.is_header(line):
            size = Header.header_size(line)
            text = Header.header_text(line)
            element = Header(size, text)
            element.line_start = i
            element.line_end = i
            element.col_start = 0
            element.col_end = len(line) - 1
            tree.content.append(element)

        i += 1

    return tree


def load(stream: io.StringIO, special: Dict = {}):
    return loads(stream.read(), special)

def loads(data: str, special: Dict = {}):
    return parse(data, special)
