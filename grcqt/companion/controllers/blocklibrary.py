# GRC imports
from .. import views, base


class BlockLibrary(base.Controller):
    """ GRC.Controllers.BlockLibrary """

    def __init__(self):
        # Required function calls
        super().__init__()
        self.setView(views.BlockLibrary)

        # Do other initialization stuff. View should already be allocated and
        # actions dynamically connected to class functions. Also, the self.log
        # functionality should be also allocated
        self.log.debug("__init__")
        self.log.debug("Registering dock")
        # Register the dock widget through the AppController.
        # The AppController then tries to find a saved dock location from the preferences
        # before calling the MainWindow Controller to add the widget.
        self.app.registerDockWidget(self.view, location=self.gp.window.BLOCK_LIBRARY_DOCK_LOCATION)

        # Register the menus
        #self.app.registerMenu(self.view.menus["library"])
