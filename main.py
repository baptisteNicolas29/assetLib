from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

from assetLib import gui

"""
this is documentation
"""


def assetLib() -> None:
    library = type("library", (MayaQWidgetDockableMixin, gui.MainWidget), {})
    wdg = library()
    wdg.show(dockable=True)
