import os
from PySide6 import QtWidgets
from PySide6 import QtCore

from assetLib import gui
from assetLib import core


class MainWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.setWindowTitle("assetLib")
        self.__path = [
                r'C:\Users\choco\Documents\maya\2025\prefs\assetLib\lib',
                ]

        # --- actions
        self.menuBar = QtWidgets.QMenuBar()
        file_menu = self.menuBar.addMenu("file")
        edit_menu = self.menuBar.addMenu("edit")
        help_menu = self.menuBar.addMenu("help")

        file_menu.addAction("save item")
        file_menu.addAction("save assemblies as item")
        file_menu.addSeparator()
        self.exit_act = file_menu.addAction("exit")

        edit_menu.addAction('edit paths')

        help_menu.addAction("documentation")
        help_menu.addAction("about")

        self.search_led = QtWidgets.QLineEdit()
        self.search_led.setPlaceholderText("search ...")

        self.content_lst = gui.assetListView.AssetListView()
        self.content_lst.setPath(self.__path[0])

        self.save_btn = QtWidgets.QPushButton("save item")

        # --- layouts
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setMenuBar(self.menuBar)

        self.layout().addWidget(self.search_led)
        self.layout().addWidget(self.content_lst)
        self.layout().addWidget(self.save_btn)

        # --- connections
        self.save_btn.clicked.connect(self.save_item)
        self.search_led.textChanged.connect(self.content_lst.model().setFilterFixedString)
        self.content_lst.doubleClicked.connect(self.itemDoubleClick)

    def save_item(self) -> None:
        print('MainWidget -> called')
        core.ModelingItem.save(self.__path[0])
        self.content_lst.reload()

    def itemDoubleClick(self, index: QtCore.QModelIndex) -> None:
        indexes = self.content_lst.selectionModel().selectedIndexes()

        for index in indexes:
            real_index = index.model().mapToSource(index)
            coreItem = real_index.model().data(real_index, QtCore.Qt.UserRole)
            print(coreItem.data.get('maya'), coreItem.path)
            coreItem.default_action()
