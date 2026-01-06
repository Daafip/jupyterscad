"""
Jupyter SCAD
Copyright (C) 2023 Jennifer Reiber Kyle

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""

import logging
from os import PathLike
from typing import Union

from solid2.core.object_base import OpenSCADObject

from .exceptions import OpenSCADError

LOGGER = logging.getLogger(__name__)


def render_stl(
    obj: OpenSCADObject,
    outfile: Union[str, PathLike],
):
    """Render a stl from an OpenSCAD object using SolidPython2.

    Typical usage example:

        >>> render_stl(cube(3), 'cube.stl')

    Args:
        obj: OpenSCAD object to visualize.
        outfile: Name of stl file to generate. No stl file is generated if None.

    Raises:
        exceptions.OpenSCADException: An error occurred running OpenSCAD.
    """
    try:
        obj.save_as_stl(filename=outfile)
    except Exception as e:
        LOGGER.error("Error rendering STL: %s", e)
        raise OpenSCADError("Error rendering STL, see log for details")
