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
Converter for legacy block definitions in XML format

- Cheetah expressions that can not be converted are passed to Cheetah for now
- Instead of generating a Block subclass directly a string representation is
  used and evaluated. This is slower / lamer but allows us to show the user
  how a converted definition would look like
"""

from __future__ import absolute_import, division, print_function

from collections import OrderedDict, defaultdict
from itertools import chain

from . import cheetah_converter, xml, yaml


current_file_format = 1
reserved_block_keys = ('import', )  # todo: add more keys


def from_xml(filename):
    """Load block description from xml file"""
    element, version_info = xml.load(filename, 'block.dtd')

    try:
        data = convert_block_xml(element)
    except NameError:
        raise ValueError('Conversion failed', filename)

    return data


def dump(data, stream):
    out = yaml.dump(data)

    replace = [
        ('parameters:', '\nparameters:'),
        ('inputs:', '\ninputs:'),
        ('outputs:', '\noutputs:'),
        ('templates:', '\ntemplates:'),
        ('documentation:', '\ndocumentation:'),
        ('file_format:', '\nfile_format:'),
    ]
    for r in replace:
        out = out.replace(*r)
    prefix = '# auto-generated by grc.converter\n\n'
    stream.write(prefix + out)


no_value = object()
dummy = cheetah_converter.DummyConverter()


def convert_block_xml(node):
    converter = cheetah_converter.Converter(names={
        param_node.findtext('key'): {
            opt_node.text.split(':')[0]
            for opt_node in next(param_node.iterfind('option'), param_node).iterfind('opt')
        } for param_node in node.iterfind('param')
    })

    block_id = node.findtext('key')
    if block_id in reserved_block_keys:
        block_id += '_'

    data = OrderedDict()
    data['id'] = block_id
    data['label'] = node.findtext('name') or no_value
    data['category'] = node.findtext('category') or no_value
    data['flags'] = node.findtext('flags') or no_value

    data['parameters'] = [convert_param_xml(param_node, converter.to_python_dec)
                          for param_node in node.iterfind('param')] or no_value
    # data['params'] = {p.pop('key'): p for p in data['params']}

    data['inputs'] = [convert_port_xml(port_node, converter.to_python_dec)
                      for port_node in node.iterfind('sink')] or no_value

    data['outputs'] = [convert_port_xml(port_node, converter.to_python_dec)
                       for port_node in node.iterfind('source')] or no_value

    data['checks'] = [converter.to_python_dec(check_node.text)
                      for check_node in node.iterfind('checks')] or no_value
    data['value'] = (
        converter.to_python_dec(node.findtext('var_value')) or
        ('${ value }' if block_id.startswith('variable') else no_value)
    )

    data['templates'] = convert_templates(node, converter.to_mako, block_id) or no_value

    docs = node.findtext('doc')
    if docs:
        docs = docs.strip().replace('\\\n', '')
        data['documentation'] = yaml.MultiLineString(docs)

    data['file_format'] = current_file_format

    data = OrderedDict((key, value) for key, value in data.items() if value is not no_value)
    auto_hide_params_for_item_sizes(data)

    return data


def auto_hide_params_for_item_sizes(data):
    item_size_templates = []
    vlen_templates = []
    for port in chain(*[data.get(direction, []) for direction in ['inputs', 'outputs']]):
        for key in ['dtype', 'multiplicity']:
            item_size_templates.append(str(port.get(key, '')))
        vlen_templates.append(str(port.get('vlen', '')))
    item_size_templates = ' '.join(value for value in item_size_templates if '${' in value)
    vlen_templates = ' '.join(value for value in vlen_templates if '${' in value)

    for param in data.get('parameters', []):
        if param['id'] in item_size_templates:
            param.setdefault('hide', 'part')
        if param['id'] in vlen_templates:
            param.setdefault('hide', "${ 'part' if vlen == 1 else 'none' }")


def convert_templates(node, convert, block_id=''):
    templates = OrderedDict()

    imports = '\n'.join(convert(import_node.text)
                        for import_node in node.iterfind('import'))
    if '\n' in imports:
        imports = yaml.MultiLineString(imports)
    templates['imports'] = imports or no_value

    templates['var_make'] = convert(node.findtext('var_make') or '') or no_value

    make = convert(node.findtext('make') or '')
    if make:
        check_mako_template(block_id, make)
    if '\n' in make:
        make = yaml.MultiLineString(make)
    templates['make'] = make or no_value

    templates['callbacks'] = [
         convert(cb_node.text) for cb_node in node.iterfind('callback')
    ] or no_value

    return OrderedDict((key, value) for key, value in templates.items() if value is not no_value)


def convert_param_xml(node, convert):
    param = OrderedDict()
    param['id'] = node.findtext('key').strip()
    param['label'] = node.findtext('name').strip()
    param['category'] = node.findtext('tab') or no_value

    param['dtype'] = convert(node.findtext('type') or '')
    param['default'] = node.findtext('value') or no_value

    options = yaml.ListFlowing(on.findtext('key') for on in node.iterfind('option'))
    option_labels = yaml.ListFlowing(on.findtext('name') for on in node.iterfind('option'))
    param['options'] = options or no_value
    if not all(str(o).title() == l for o, l in zip(options, option_labels)):
        param['option_labels'] = option_labels

    attributes = defaultdict(yaml.ListFlowing)
    for option_n in node.iterfind('option'):
        for opt_n in option_n.iterfind('opt'):
            key, value = opt_n.text.split(':', 2)
            attributes[key].append(value)
    param['option_attributes'] = dict(attributes) or no_value

    param['hide'] = convert(node.findtext('hide')) or no_value

    return OrderedDict((key, value) for key, value in param.items() if value is not no_value)


def convert_port_xml(node, convert):
    port = OrderedDict()
    label = node.findtext('name')
    # default values:
    port['label'] = label if label not in ('in', 'out') else no_value

    dtype = convert(node.findtext('type'))
    # TODO: detect dyn message ports
    port['domain'] = domain = 'message' if dtype == 'message' else 'stream'
    if domain == 'message':
        port['id'], port['label'] = label, no_value
    else:
        port['dtype'] = dtype
        vlen = node.findtext('vlen')
        port['vlen'] = int(vlen) if vlen and vlen.isdigit() else convert(vlen) or no_value

    port['multiplicity'] = convert(node.findtext('nports')) or no_value
    port['optional'] = bool(node.findtext('optional')) or no_value
    port['hide'] = convert(node.findtext('hide')) or no_value

    return OrderedDict((key, value) for key, value in port.items() if value is not no_value)


def check_mako_template(block_id, expr):
    import sys
    from mako.template import Template
    try:
        Template(expr)
    except Exception as error:
        print(block_id, expr, type(error), error, '', sep='\n', file=sys.stderr)
