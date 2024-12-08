from abc import ABC, abstractmethod, abstractclassmethod
from pathlib import Path
from typing import Callable, Dict, Self, Any

from maya import cmds


class AbsAssetItem(ABC):

    TYPE: str = None
    DEFAULT_ACTION = None

    def __init__(
            self,
            name: str,
            icon: str,
            path: str,
            data: Dict[str, Any]
            ) -> None:
        self.__action: Dict[str, Callable] = {}
        self.__name = name
        self.__path = Path(path)
        self.__icon = Path(path) / icon
        self.__data = data

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> str:
        return str(self.__path)

    @property
    def icon(self) -> str:
        return str(self.__icon)

    @property
    def data(self) -> Dict[str, Any]:
        return self.__data

    @abstractmethod
    def save(cls) -> None: ...

    @property
    def action(self) -> Dict[str, Any]:
        return self.__action

    def getAction(self, actionKey: str) -> Callable:
        return self.__action.get(actionKey, self.errorMessage)

    @property
    def default_action(cls) -> Callable:
        return cls.__action.get(cls.DEFAULT_ACTION)

    def errorMessage(self) -> None:
        cmds.warning('asked action is not implemented for this item')
