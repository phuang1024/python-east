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
    Tree representation of one markdown file.
    """

    content: List

    def __init__(self, content: List = []):
        self.content = content


def parse(data: io.StringIO, special: Dict):
    tree = Tree()

    return tree


def load(stream: io.StringIO, special: Dict):
    return loads(stream.read(), special)

def loads(data: str, special: Dict):
    return parse(data, special)
