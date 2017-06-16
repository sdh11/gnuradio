# Copyright 2009-2016 Free Software Foundation, Inc.
# This file is part of GNU Radio
#
# GNU Radio Companion is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# GNU Radio Companion is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA

import os
import sys
import warnings
import logging
import argparse


LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}


def run():
    from gnuradio import gr
    parser = argparse.ArgumentParser(description="Convert XML files to YAML blocks")
    parser.add_argument('--log', choices=['debug', 'info', 'warning', 'error', 'critical'], default='warning')
    args = parser.parse_args()

    log = logging.getLogger('converter')
    log.setLevel(logging.DEBUG)

    # Console formatting
    console = logging.StreamHandler()
    console.setLevel(LOG_LEVELS[args.log])

    msg_format = '[%(levelname)s] %(message)s (%(filename)s:%(lineno)s)'
    date_format = '%I:%M'
    formatter = logging.Formatter(msg_format, datefmt=date_format)

    console.setFormatter(formatter)
    log.addHandler(console)

    log.debug("Running converter")

    script_path = os.path.dirname(os.path.abspath(__file__))
    source_tree_subpath = "/grc/scripts"

    if script_path.endswith(source_tree_subpath):
        print("Running from source tree")
        sys.path.insert(1, script_path[:-len(source_tree_subpath)])
    from converter import Converter

    from core.Config import Config
    cfg = Config(gr.version(), prefs=gr.prefs())

    converter = Converter(cfg.block_paths)
    exit(converter.run())
    logging.info('XML converter done.')

run()
