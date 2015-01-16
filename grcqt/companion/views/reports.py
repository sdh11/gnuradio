from PyQt5 import QtCore, QtGui, QtWidgets

# GRC imports
from .. import base


class Reports(QtWidgets.QDockWidget, base.View):
    """ GRC.Views.Reports """

    def __init__(self):
        super().__init__()  # REQUIRED for both QMainWindow and base.View
        self.log.debug("__init__")

        self.setWindowTitle("Reports")

        # Create a widget container and populate with a horizontal layout
        contents = QtWidgets.QWidget()
        contents.setObjectName("reports::contents")

        layout = QtWidgets.QHBoxLayout(contents)
        layout.setContentsMargins(5, 0, 5, 5)
        layout.setObjectName("reports::containers::layout")

        text = QtWidgets.QTextEdit(self)
        text.setUndoRedoEnabled(False)
        text.setReadOnly(True)
        text.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                     "p, li { white-space: pre-wrap; }\n"
                     "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                     "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><br /></p></body></html>")
        text.setObjectName("reports::contents::layout::text")
        text.setCursorWidth(0)
        text.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.text = text

        layout.addWidget(text)
        self.setWidget(contents)

        self.createMenus(self.actions, self.menus)

    def createActions(self, actions):
        """ Defines all actions for this view. """

        self.log.debug("Creating actions")
        Action = QtWidgets.QAction
        Icons = QtGui.QIcon.fromTheme
        Keys = QtGui.QKeySequence

        # File Actions
        actions['save'] = Action(Icons("document-save"), _("save"), self,
                                shortcut=Keys.New, statusTip=_("save-tooltip"))

        actions['clear'] = Action(Icons("document-close"), _("clear"), self,
                                 shortcut=Keys.Open, statusTip=_("clear-tooltip"))

    def createMenus(self, actions, menus):
        """ Setup the view's menus """

        self.log.debug("Creating menus")

        reports = QtWidgets.QMenu("&Reports")
        reports.setObjectName("reports::menu")

        reports.addAction(actions["save"])
        reports.addAction(actions["clear"])
        menus["reports"] = reports

    def createToolbars(self, actions, toolbars):
        self.log.debug("Creating toolbars")

        # Main toolbar
        '''file = self.addToolBar("file")
        file.addAction(actions['new'])
        file.addAction(actions['open'])
        file.addAction(actions['save'])
        file.addAction(actions['close'])
        file.addAction(actions['print'])
        toolbars['file'] = file

        # Edit toolbar
        edit = self.addToolBar("edit")
        edit.addAction(actions['cut'])
        edit.addAction(actions['copy'])
        edit.addAction(actions['paste'])
        edit.addAction(actions['delete'])
        edit.addSeparator()
        edit.addAction(actions['rotate_ccw'])
        edit.addAction(actions['rotate_cw'])
        toolbars['edit'] = edit

        # Run Toolbar
        run = self.addToolBar("run")
        run.addAction(actions['generate'])
        run.addAction(actions['execute'])
        run.addAction(actions['kill'])
        toolbars['run'] = run'''
