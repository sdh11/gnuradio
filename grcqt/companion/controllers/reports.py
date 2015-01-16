# GRC imports
from .. import views, base
from PyQt5 import QtCore


class Reports(base.Controller):
    """ GRC.Controllers.Reports """

    def __init__(self):
        # Required function calls
        super().__init__()
        self.setView(views.Reports)

        # Do other initialization stuff. View should already be allocated and
        # actions dynamically connected to class functions. Also, the self.log
        # functionality should be also allocated
        self.log.debug("__init__")
        self.log.debug("Registering dock widget")
        # Register the dock widget through the AppController.
        # The AppController then tries to find a saved dock location from the preferences
        # before calling the MainWindow Controller to add the widget.
        self.app.registerDockWidget(self.view, location=self.gp.window.REPORTS_DOCK_LOCATION)

        # Register the menus
        self.app.registerMenu(self.view.menus["reports"])

    def add_line(self, line):
        self.text.append('spam: spam spam spam spam')

    def clear(self):
        self.text.clear()

    def _save_changes(self):
        pass
