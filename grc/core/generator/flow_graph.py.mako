% if not generate_options.startswith('hb'):
#!/usr/bin/env python2
% endif
# -*- coding: utf-8 -*-
########################################################
##Cheetah template - gnuradio_python
##
##@param imports the import statements
##@param flow_graph the flow_graph
##@param variables the variable blocks
##@param parameters the parameter blocks
##@param blocks the signal blocks
##@param connections the connections
##@param generate_options the type of flow graph
##@param callbacks variable id map to callback strings
########################################################
<%def name="indent(code)">${ '\n        '.join(str(code).splitlines()) }</%def>
"""
GNU Radio Python Flow Graph

Title: ${title}
% if flow_graph.get_option('author'):
Author: ${flow_graph.get_option('author')}
% endif
% if flow_graph.get_option('description'):
Description: ${flow_graph.get_option('description')}
% endif
Generated: ${ generated_time }
"""

% if generate_options == 'qt_gui':
from distutils.version import StrictVersion
% endif
## Call XInitThreads as the _very_ first thing.
## After some Qt import, it's too late
% if generate_options == 'qt_gui':

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

% endif
########################################################
##Create Imports
########################################################
% for imp in imports:
##${imp.replace("  # grc-generated hier_block", "")}
${imp}
% endfor
########################################################
##Create Class
##  Write the class declaration for a top or hier block.
##  The parameter names are the arguments to __init__.
##  Setup the IO signature (hier block only).
########################################################
<%
    class_name = flow_graph.get_option('id')
    param_str = ', '.join(['self'] + ['%s=%s'%(param.name, param.get_make()) for param in parameters])
%>\
% if generate_options == 'qt_gui':
from gnuradio import qtgui

class ${class_name}(gr.top_block, Qt.QWidget):

    def __init__(${param_str}):
        gr.top_block.__init__(self, "${title}")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("${title}")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "${class_name}")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass
% elif generate_options == 'no_gui':

class ${class_name}(gr.top_block):

    def __init__(${param_str}):
        gr.top_block.__init__(self, "${title}")
% elif generate_options.startswith('hb'):
    <% in_sigs = flow_graph.get_hier_block_stream_io('in') %>
    <% out_sigs = flow_graph.get_hier_block_stream_io('out') %>


% if generate_options == 'hb_qt_gui':
class ${class_name}(gr.hier_block2, Qt.QWidget):
% else:
class ${class_name}(gr.hier_block2):
% endif
<%def name="make_io_sig(io_sigs)">
    <% size_strs = ['%s*%s'%(io_sig['size'], io_sig['vlen']) for io_sig in io_sigs] %>
    % if len(io_sigs) == 0:
gr.io_signature(0, 0, 0)\
    #elif len(${io_sigs}) == 1
gr.io_signature(1, 1, ${size_strs[0]})
    % else:
gr.io_signaturev(${len(o_sigs)}, ${len(o_sigs)}, [${', '.join(ize_strs)}])
    % endif
</%def>

    def __init__(${param_str}):
        gr.hier_block2.__init__(
            self, "${ title }",
            ${make_io_sig(n_sigs)},
            ${make_io_sig(ut_sigs)},
        )
    % for pad in flow_graph.get_hier_block_message_io('in'):
        self.message_port_register_hier_in("${ pad['label'] }")
    % endfor
    % for pad in flow_graph.get_hier_block_message_io('out'):
        self.message_port_register_hier_out("${ pad['label'] }")
    % endfor
    % if generate_options == 'hb_qt_gui':

        Qt.QWidget.__init__(self)
        self.top_layout = Qt.QVBoxLayout()
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)
        self.setLayout(self.top_layout)
    % endif
% endif
% if flow_graph.get_option('thread_safe_setters'):

        self._lock = threading.RLock()
% endif
########################################################
##Create Parameters
##  Set the parameter to a property of self.
########################################################
% if parameters:

        ########################################################
        # Parameters
        ########################################################
% endif
% for param in parameters:
        ${indent(param.get_var_make())}
% endfor
########################################################
##Create Variables
########################################################
% if variables:

        ########################################################
        # Variables
        ########################################################
% endif
% for var in variables:
        ${indent(ar.get_var_make())}
% endfor
        % if blocks:

        ########################################################
        # Blocks
        ########################################################
        % for blk, blk_make in blocks:
        ${ indent(blk_make) }
##         % if 'alias' in blk.params and blk.params['alias'].get_evaluated():
##         (self.${blk.name}).set_block_alias("${blk.params['alias'].get_evaluated()}")
##         % endif
##         % if 'affinity' in blk.params and blk.params['affinity'].get_evaluated():
##         (self.${blk.name}).set_processor_affinity(${blk.params['affinity'].get_evaluated()})
##         % endif
##         % if len(blk.sources) > 0 and 'minoutbuf' in blk.params and int(blk.params['minoutbuf'].get_evaluated()) > 0:
##         (self.${blk.name}).set_min_output_buffer(${blk.params['minoutbuf'].get_evaluated()})
##         % endif
##         % if len(blk.sources) > 0 and 'maxoutbuf' in blk.params and int(blk.params['maxoutbuf'].get_evaluated()) > 0:
##         (self.${blk.name}).set_max_output_buffer(${blk.params['maxoutbuf'].get_evaluated()})
##         % endif
        % endfor
        % endif
        % if connections:

        ########################################################
        # Connections
        ########################################################
        % for connection in connections:
        ${ connection.rstrip() }
        % endfor
        % endif
########################################################
## QT sink close method reimplementation
########################################################
% if generate_options == 'qt_gui':

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "${class_name}")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()
    % if flow_graph.get_option('qt_qss_theme'):

    def setStyleSheetFromFile(self, filename):
        try:
            if not os.path.exists(filename):
                filename = os.path.join(
                    gr.prefix(), "share", "gnuradio", "themes", filename)
            with open(filename) as ss:
                self.setStyleSheet(ss.read())
        except Exception as e:
            print >> sys.stderr, e
    % endif
% endif
########################################################
##Create Callbacks
##  Write a set method for this variable that calls the callbacks
########################################################
% for var in parameters + variables:

    <% id_ = var.name %>
    def get_${id_}(self):
        return self.${id_}

    def set_${id_}(self, ${id_}):
    % if flow_graph.get_option('thread_safe_setters'):
        with self._lock:
            self.${id_} = ${id_}
        % for callback in callbacks[d]:
            ${indent(allback)}
        % endfor
    % else:
        self.${id_} = ${id_}
        % for callback in callbacks[d]:
        ${indent(allback)}
        % endfor
    % endif
% endfor
########################################################
##Create Main
##  For top block code, generate a main routine.
##  Instantiate the top block and run as gui or cli.
########################################################
<%def name="make_default(type_, param)">
    % if type_ == 'eng_float':
eng_notation.num_to_str(${param.get_make()})
    % else:
${param.get_make()}
    % endif
</%def>
<%def name="make_short_id(param)">
    <% short_id = param.params['short_id'].get_evaluated() %>
    % if short_id:
        <% short_id = '-' + short_id %>
    % endif
${short_id}\
</%def>
% if not generate_options.startswith('hb'):
<% params_eq_list = list() %>
% if parameters:


def argument_parser():
    <% arg_parser_args = '' %>
    % if flow_graph.get_option('description'):
    <% arg_parser_args = 'description=description' %>
    description = ${repr(flow_graph.get_option('description'))}
    % endif
    parser = ArgumentParser(${arg_parser_args})
    % for param in parameters:
        <% type_ = param.params['type'].get_value() %>
        % if type_:
            ${params_eq_list.append('%s=options.%s' % (param.name, param.name))}
    parser.add_argument(
        % if make_short_id(param):
        "${make_short_id(param)}",
        % endif
        "--${param.name.replace('_', '-')}", dest="${param.name}", type=${type_}, default=${make_default(type_, param)},
        help="Set ${param.params['label'].get_evaluated() or param.name} [default=%(default)r]")
        % endif
    % endfor
    return parser
% endif


def main(top_block_cls=${class_name}, options=None):
    % if parameters:
    if options is None:
        options = argument_parser().parse_args()
    % endif
    % if flow_graph.get_option('realtime_scheduling'):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."
    % endif

    % if generate_options == 'qt_gui':
    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(${ ', '.join(params_eq_list) })
    % if flow_graph.get_option('run'):
    tb.start(${flow_graph.get_option('max_nouts') or ''})
    % endif
    % if flow_graph.get_option('qt_qss_theme'):
    tb.setStyleSheetFromFile(${ flow_graph.get_option('qt_qss_theme') })
    % endif
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    % for m in monitors:
    if 'en' in m.params:
        if m.params['en'].get_value():
            (tb.${m.name}).start()
    else:
        sys.stderr.write("Monitor '{0}' does not have an enable ('en') parameter.".format("tb.${m.name}"))
    % endfor
    qapp.exec_()
    % elif generate_options == 'no_gui':
    tb = top_block_cls(${ ', '.join(params_eq_list) })
    % if flow_graph.get_option('run_options') == 'prompt':
    tb.start(${ flow_graph.get_option('max_nouts') or '' })
    % for m in monitors:
    (tb.${m.name}).start()
    % endfor
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    % elif flow_graph.get_option('run_options') == 'run':
    tb.start(${flow_graph.get_option('max_nouts') or ''})
    % endif
    % for m in monitors:
    (tb.${m.name}).start()
    % endfor
    tb.wait()
    % endif


if __name__ == '__main__':
    main()
% endif
