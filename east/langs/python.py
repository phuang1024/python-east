#
#  Python EAST
#  Python module for parsing many languages into ASTs.
#  Copyright Patrick Huang and Agastya Pawate 2021
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
    Tree representation of one Python file.
    """

    content: List

    def __init__(self, content: List = []):
        self.content = content

    def __repr__(self) -> str:
        return f"<PythonTree({len(self.content)} elements)>"


class Comment(Element):
    """
    Contains a comment in Python (line that starts with "#")
    """

    size: int
    text: str

    def __init__(self, size: int = 1, text: str = "") -> None:
        self.size = size
        self.text = text

    def __repr__(self) -> str:
        return f"<PythonHeader(size={self.size}, text={self.text})>"

    @staticmethod
    def is_comment(line: str) -> bool:
        """
        Returns whether a line is a comment.
        :param line: Line to parse
        """
        if len(line) == 0:
            return False
         
        indx = 0

        for char in line:
            if char == "#" and indx == 0:
                # Increment count and check bounds
                return True
            else:
                return False
        

def parse(data: str, special: Dict) -> Tree:
    """
    Parses data into a tree.
    :param data: String data to parse.
    :param special: Special parameters for current data.
    """
    tree = Tree()

    lines = data.split("\n")
    i = 0
    while len(lines) > 0:
        line = lines.pop(0)
        i += 1
        if len(line.strip()) == 0:
            continue

        if Comment.is_comment(line):
            element.line_start = i
            element.line_end = i
            element.col_start = 0
            element.col_end = len(line) - 1
            tree.content.append(element)

    return tree


def load(stream: io.StringIO, special: Dict = {}) -> Tree:
    """
    Parses stream into a tree.
    :param stream: Stream with target data (i.e. a file)
    :param special: Special parameters for current data.
    """
    return loads(stream.read(), special)

def loads(data: str, special: Dict = {}) -> Tree:
    """
    Loads data into a tree.
    :param data: String data to load.
    :param special: Special parameters for current data.
    """
    return parse(data, special)
