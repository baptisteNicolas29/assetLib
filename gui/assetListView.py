import json
from typing import Self, Optional
from pathlib import Path
from PySide6 import QtWidgets as qtw, QtCore as qtc, QtGui as qtg

from assetLib.core import AbsAssetItem, ModelingItem


class AssetListView(qtw.QListView):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setModel(AssetListProxyModel())
        self.setIconSize(qtc.QSize(30, 30))
        # self.setViewMode(qtw.QListView.IconMode)

    def path(self, path: str) -> None:
        return self.model().sourceModel().path()

    def setPath(self, path: str | Path) -> None:
        self.model().sourceModel().setPath(path)

    def reload(self) -> None:
        self.model().sourceModel().reload()


class AssetListProxyModel(qtc.QSortFilterProxyModel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setSourceModel(AssetListModel())
        self.setFilterCaseSensitivity(qtc.Qt.CaseInsensitive)


class AssetListModel(qtg.QStandardItemModel):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__path: None | Path = None

    def path(self) -> str:
        return str(self.__path)

    def setPath(self, path: str | Path) -> None:
        self.__path = Path(path)
        self.reload()

    def reload(self) -> None:

        if self.__path is None:
            return

        if not self.__path.is_dir():
            return

        self.clear()
        for path in self.__path.iterdir():

            if not path.suffix == '.json':
                continue

            with open(str(path), 'r') as file:
                data = json.load(file)

            coreItem = ModelingItem(
                    path.with_suffix('').name,
                    data.get('icon'),
                    str(self.__path),
                    data,
                    )
            item = qtg.QStandardItem()
            self.appendRow(item)
            item.setData(coreItem.name, qtc.Qt.DisplayRole)
            item.setData(qtg.QIcon(qtg.QPixmap(coreItem.icon)), qtc.Qt.DecorationRole)
            item.setData(coreItem, qtc.Qt.UserRole)
            item.setFlags(qtc.Qt.ItemIsEnabled | qtc.Qt.ItemIsSelectable)
