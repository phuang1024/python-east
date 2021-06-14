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
