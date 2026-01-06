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
from unittest.mock import Mock

import pytest
import solid2

from jupyterscad import render_stl

LOGGER = logging.getLogger(__name__)


## Unsure what to do here? i guess leave it for now. 

# @pytest.mark.parametrize("obj", ["cube(size = 3);", solid2.cube(3)])
# def test_render_stl_str_obj(obj, tmp_path, monkeypatch):
#     def side_effect(scad_file, output_file, executable):
#         with open(scad_file, "r") as fp:
#             assert fp.read().strip() == "cube(size = 3);"

#         assert output_file == tmp_path / "test.stl"

#     mock_process = Mock(side_effect=side_effect)
#     monkeypatch.setattr(_render, "process", mock_process)

#     output_file = tmp_path / "test.stl"

#     render_stl(obj, output_file)
#     mock_process.assert_called_once()


@pytest.mark.skip(
    "not a good test: floats as ints and precision depends on openscad version"
)
def test_render_stl_import(tmp_path, test_data, check_render):
    stl_path = tmp_path / "test.stl"
    shutil.copy(test_data("test.stl"), stl_path)
    obj = solid2.import_(stl_path)

    output_file = tmp_path / "result.stl"
    render_stl(obj, output_file)

    assert open(output_file).read() == open(stl_path).read()


@pytest.fixture()
def scad_file(tmp_path):
    input_scad_file = tmp_path / "test.scad"
    with open(input_scad_file, "w") as fp:
        fp.write("cube([60,20,10],center=true);")
    return input_scad_file


@pytest.fixture()
def output_file(tmp_path):
    return tmp_path / "out.stl"

