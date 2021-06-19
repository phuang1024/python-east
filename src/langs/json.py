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
from typing import Any, IO, List, Tuple, Union

SPECIAL = "{}[]\":,"


class Element:
    """
    Base JSON element.
    All other elements extend off of this.
    """
    padding_after: str

    def __init__(self) -> None:
        ...

    def __str__(self) -> str:
        ...

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        ...


class Comma(Element):
    """
    A comma element.
    """

    def __init__(self) -> None:
        self.padding_after = ""

    def __str__(self) -> str:
        return f"json.Comma()"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        if ch != ",":
            raise ValueError(f"Comma \",\" not found at the start of stream.")

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Colon(Element):
    """
    A colon element.
    """

    def __init__(self) -> None:
        self.padding_after = ""

    def __str__(self) -> str:
        return f"json.Colon()"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        if ch != ":":
            raise ValueError(f"Colon \":\" not found at the start of stream.")

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Tree:
    """
    A whole JSON syntax tree.
    """
    padding_before: str

    def __init__(self) -> None:
        self.padding_before = ""

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        ...
