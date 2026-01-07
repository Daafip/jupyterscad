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
import shutil
from pathlib import Path

import pytest
import solid2

from jupyterscad import render_stl

LOGGER = logging.getLogger(__name__)

test_output_path = Path(__file__).parent.parent.absolute()


@pytest.fixture()
def relative_path() -> Path:
    """Fixture that provides a relative output path instead of a temporary one."""
    # Ensure the test output directory exists
    test_output_path.mkdir(exist_ok=True)
    return test_output_path


@pytest.fixture()
def scad_file(relative_path):
    input_scad_file = relative_path / "test.scad"
    with open(input_scad_file, "w") as fp:
        fp.write("cube([60,20,10],center=true);")
    return input_scad_file


@pytest.fixture()
def output_file(relative_path: Path) -> Path:
    return relative_path / "out.stl"


class TestRenderStlWithSolid2Objects:
    """Tests for rendering solid2 objects to STL."""

    def test_render_cube(self, relative_path):
        """Test rendering a simple cube."""
        obj = solid2.cube(10)
        output_file = "cube.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_sphere(self, relative_path):
        """Test rendering a sphere."""
        obj = solid2.sphere(r=5)
        output_file = "sphere.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_cylinder(self, relative_path):
        """Test rendering a cylinder."""
        obj = solid2.cylinder(h=10, r=5)
        output_file = "cylinder.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_combined_objects(self, relative_path):
        """Test rendering combined solid2 objects (union)."""
        obj = solid2.cube(10) + solid2.sphere(r=7)
        output_file = "combined.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_difference(self, relative_path):
        """Test rendering difference of objects."""
        obj = solid2.cube(10) - solid2.sphere(r=6)
        output_file = "difference.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_intersection(self, relative_path):
        """Test rendering intersection of objects."""
        obj = solid2.cube(10) & solid2.sphere(r=7)
        output_file = "intersection.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()


class TestRenderStlWithScadString:
    """Tests for rendering OpenSCAD string code to STL."""

    def test_render_scad_string_cube(self, relative_path):
        """Test rendering a cube from SCAD string wrapped in solid2."""
        obj = solid2.cube(size=10)
        output_file = "cube.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_scad_string_complex(self, relative_path: Path):
        """Test rendering complex object."""
        obj = solid2.cube(20, center=True) - solid2.sphere(r=13)
        output_file = "complex.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()
        output_path.with_suffix(".stl.scad").unlink()


class TestRenderStlTransformations:
    """Tests for rendering transformed objects."""

    def test_render_translated_object(self, relative_path):
        """Test rendering a translated object."""
        obj = solid2.cube(10).translate([5, 5, 5])
        output_file = "translated.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_rotated_object(self, relative_path):
        """Test rendering a rotated object."""
        obj = solid2.cube(10).rotate([45, 0, 0])
        output_file = "rotated.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()

    def test_render_scaled_object(self, relative_path):
        """Test rendering a scaled object."""
        obj = solid2.cube(10).scale([2, 1, 0.5])
        output_file = "scaled.stl"
        render_stl(obj, output_file)
        output_path = relative_path / output_file
        assert output_path.exists()
        assert output_path.stat().st_size > 0
        output_path.unlink()


@pytest.mark.skip(
    "not a good test: floats as ints and precision depends on openscad version"
)
def test_render_stl_import(relative_path, test_data):
    stl_path = relative_path / "test.stl"
    shutil.copy(test_data("test.stl"), stl_path)
    obj = solid2.import_(stl_path)

    output_file = "result.stl"
    render_stl(obj, output_file)

    assert open(output_file).read() == open(stl_path).read()
