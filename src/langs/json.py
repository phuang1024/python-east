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
import io
import string
from typing import IO, List, Union

SPECIAL = "ntf:,\"[]{}." + string.digits


class Element:
    """
    Base JSON element.
    All other elements extend off of this.
    """
    padding_after: str

    def __init__(self) -> None:
        self.padding_after = ""

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

    def __str__(self) -> str:
        return f"json.Comma()"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch == ","), f"Comma \",\" not found at the start of stream."

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Colon(Element):
    """
    A colon element.
    """

    def __str__(self) -> str:
        return f"json.Colon()"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch == ":"), f"Colon \":\" not found at the start of stream."

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Null(Element):
    """
    A null (None) element.
    """

    def __str__(self) -> str:
        return f"json.Null()"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch == "n"), f"null not found at the start of stream."
        stream.read(3)   # read "ull" in "null"

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Bool(Element):
    """
    A boolean element.
    """
    value: bool

    def __init__(self) -> None:
        super().__init__()
        self.value = False

    def __str__(self) -> str:
        return f"json.Bool({self.value})"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch in "tf"), f"\"t\" or \"f\" not found at the start of stream."
        inst.value = (ch == "t")
        stream.read((3 if inst.value else 4))   # read remaining chars

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Number(Element):
    """
    A number element.
    """
    value: Union[int, float]

    def __init__(self) -> None:
        super().__init__()
        self.value = 0

    def __str__(self) -> str:
        return f"json.Number({self.value})"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch in string.digits+"."), f"Digit not found at the start of stream."

        data = ch
        while (ch := stream.read(1).decode()) in string.digits+".":
            if len(ch) == 0:
                break
            data += ch
        inst.value = (float(data) if "." in data else int(data))
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class String(Element):
    """
    A string element.
    """
    value: str

    def __init__(self) -> None:
        super().__init__()
        self.value = ""

    def __str__(self) -> str:
        return f"json.String({repr(self.value)})"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch == "\""), f"\" not found at the start of stream."

        while (ch := stream.read(1).decode()) != "\"":
            if len(ch) == 0:
                break
            inst.value += ch

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Array(Element):
    """
    An array element.
    """
    elements: List[Element]

    def __init__(self) -> None:
        super().__init__()
        self.elements = []

    def __str__(self) -> str:
        return f"json.Array({self.elements})"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch == "["), f"[ not found at the start of stream."

        while True:
            while (ch := stream.read(1).decode()) not in SPECIAL:
                assert (len(ch) > 0), "Unexpected EOF while parsing json.Array"
            if ch == "]":
                break
            stream.seek(-1, os.SEEK_CUR)
            inst.elements.append(read_element(stream))

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class DictPair(Element):
    """
    A dictionary (key, value) pair.
    """
    key: String
    colon: Colon
    value: Element

    def __str__(self) -> str:
        return f"json.DictPair({self.key}, {self.value})"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch == "\""), f"\" not found at the start of stream."
        stream.seek(-1, os.SEEK_CUR)

        inst.key = read_element(stream)
        inst.colon = read_element(stream)
        inst.value = read_element(stream)

        while (ch := stream.read(1).decode()) not in SPECIAL:
            inst.padding_after += ch
        if len(ch) > 0:
            stream.seek(-1, os.SEEK_CUR)

        return inst


class Dictionary(Element):
    """
    A dictionary element.
    """
    elements: List[Union[DictPair, Comma]]

    def __init__(self) -> None:
        super().__init__()
        self.elements = []

    def __str__(self) -> str:
        return f"json.Dictionary({self.elements})"

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            continue
        assert (ch == "{"), "{ not found at the start of stream."

        while True:
            while (ch := stream.read(1).decode()) not in SPECIAL:
                assert (len(ch) > 0), "Unexpected EOF while parsing json.Dictionary"
            if ch == "}":
                break
            stream.seek(-1, os.SEEK_CUR)
            if ch == ",":
                inst.elements.append(read_element(stream))
            else:
                inst.elements.append(DictPair.from_stream(stream))

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
    element: Element

    def __init__(self) -> None:
        self.padding_before = ""

    @classmethod
    def from_stream(cls, stream: IO[bytes]):
        inst = cls()
        while (ch := stream.read(1).decode()) in string.whitespace:
            inst.padding_before += ch
        stream.seek(-1, os.SEEK_CUR)

        inst.element = read_element(stream)
        return inst


def read_element(stream: IO[bytes]) -> Element:
    while (ch := stream.read(1).decode()) in string.whitespace:
        continue
    stream.seek(-1, os.SEEK_CUR)

    if ch == "n":
        return Null.from_stream(stream)
    elif ch in "tf":
        return Bool.from_stream(stream)
    elif ch in string.digits+".":
        return Number.from_stream(stream)
    elif ch == ",":
        return Comma.from_stream(stream)
    elif ch == ":":
        return Colon.from_stream(stream)
    elif ch == "\"":
        return String.from_stream(stream)
    elif ch == "[":
        return Array.from_stream(stream)
    elif ch == "{":
        return Dictionary.from_stream(stream)

    raise ValueError(f"Unknown start character: {ch}")


def load(stream: IO[bytes]) -> Tree:
    return Tree.from_stream(stream)


def loads(string: bytes) -> Tree:
    return Tree.from_stream(io.BytesIO(string))
