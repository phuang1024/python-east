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

import os
import string
from typing import IO

SPECIAL = "{}[]\":,"


class Comma:
    """
    A comma element.
    """
    padding_after: str

    def __init__(self) -> None:
        self.padding_after = ""

    def __str__(self) -> str:
        return f"json.Comma(padding={repr(self.padding_after)})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        if ch != ",":
            raise ValueError(f"Comma \",\" not found at the start of stream.")

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        stream.seek(-1, os.SEEK_CUR)

        return inst


class String:
    """
    A string element.
    """
    string: str
    padding_after: str

    def __init__(self) -> None:
        self.string = ""
        self.padding_after = ""

    def __str__(self) -> str:
        return f"json.String(string={repr(self.string)}, padding={repr(self.padding_after)})"

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        if ch != "\"":
            raise ValueError(f"String starts with {ch}, expected \"")

        while (ch := stream.read(1).decode()) != "\"":
            inst.string += ch
        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        stream.seek(-1, os.SEEK_CUR)

        return inst


class List:
    """
    A list element.
    """


class Tree:
    """
    A whole JSON syntax tree.
    """
    padding_before: str

    def __init__(self) -> None:
        pass
