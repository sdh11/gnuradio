# Copyright 2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# GNU Radio Companion is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# GNU Radio Companion is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA
"""
Converter for legacy block tree definitions in XML format
"""

from __future__ import absolute_import, print_function

from . import xml, yaml


def from_xml(filename):
    """Load block tree description from xml file"""
    element, version_info = xml.load(filename, 'block_tree.dtd')

    try:
        data = convert_category_node(element)
    except NameError:
        raise ValueError('Conversion failed', filename)

    return data


dump = yaml.dump


def convert_category_node(node):
    """convert nested <cat> tags to nested lists dicts"""
    assert node.tag == 'cat'
    name, elements = '', []
    for child in node:
        if child.tag == 'name':
            name = child.text.strip()
        elif child.tag == 'block':
            elements.append(child.text.strip())
        elif child.tag == 'cat':
            elements.append(convert_category_node(child))
    return {name: elements}
