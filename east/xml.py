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
from typing import Dict, List, Tuple


class Element:
    """
    Base element class, which contains members common to all elements.
    All element classes inherit from this.
    """

    line_start: int
    col_start: int
    line_end: int
    col_end: int

    def __init__(self, line_start: int = 0, col_start: int = 0, line_end: int = 0, col_end: int = 0):
        self.line_start = line_start
        self.col_start = col_start
        self.line_end = line_end
        self.col_end = col_end


class Tree(Element):
    """
    Contains the whole file. The "root" of the tree.
    """

    content: List

    def __init__(self, content: List = []):
        self.content = content


class Tag(Element):
    """
    Contains information for one tag.
    """

    name: str
    args: List[Tuple[str]]
    content: List

    def __init__(self, name: str, args: List = [], content: List = []):
        self.name = name
        self.args = args
        self.content = content


def parse_content(stream: io.StringIO, special: Dict):
    """
    Parses a stream into a tree.
    """

    tree = Tree()

    return tree


def load(stream: io.StringIO, special: Dict):
    return parse_content(stream, special)

def loads(data: str, special: Dict):
    return load(io.StringIO(data), special)

def dump(tree: Tree, stream: io.StringIO, special: Dict, indent: int = 4):
    pass

def dumps(tree: Tree, special: Dict, indent: int = 4):
    stream = io.StringIO()
    result = dump(tree, stream, special, indent)
    return result
