import json
from pathlib import Path

from maya import cmds

from assetLib.core import AbsAssetItem
from assetLib.core import contextManager as contextMan
from assetLib.core import constants as const


class ModelingItem(AbsAssetItem):

    TYPE = 'modeling'
    DEFAULT_ACTION = 'reference'

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.action.update(
            {
                'import': self.importScene,
                'reference': self.referenceScene,
            }
        )

    @classmethod
    def save(cls, path: str | Path) -> None:

        selection = cmds.ls(sl=True)
        path = Path(path)
        if not selection:
            raise NameError(
                    'nothing currently selected please select somthing'
                    )

        playblast_path = cls.takePicture(str(path / f'{selection[0]}.png'))
        maya_path = cmds.file(
                path / f"{selection[0]}.ma",
                type='mayaAscii',
                exportSelected=True,
                force=True,
                )

        usd_options = [f'{k}={v}' for k, v in const.USD_EXPORT_OPTIONS.items()]
        usd_options = ';'.join(usd_options)
        usd_path = cmds.file(
                path / f"{selection[0]}.usda",
                type='USD Export',
                exportSelected=True,
                force=True,
                options=usd_options,
                )

        json_path = str(path / f'{selection[0]}.json')
        json_data = {
            'type': 'modeling',
            'icon': Path(playblast_path).name,
            'maya': Path(maya_path).name,
            'usd': Path(usd_path).name,
            'tags': [],
        }

        with open(json_path, 'w') as file:
            json.dump(json_data, file)

        return cls(
                selection[0],
                Path(playblast_path).name,
                path,
                json_data
                )

    @staticmethod
    def takePicture(path: str) -> str:

        playblast_path = path
        # with contextMan.withIsolate():
        with contextMan.withViewChangeLess(const.VIEWPORT_OPTIONS):
            print('pass the witViewChangeLess context')
            with contextMan.withIsolate():
                print('pass the contextMan context')

                playblast_path = cmds.playblast(
                        completeFilename=path,
                        forceOverwrite=True,
                        fmt='image',
                        frame=cmds.currentTime(q=True),
                        quality=100,
                        percent=100,
                        widthHeight=[255, 255],
                        )

        return playblast_path

    def importScene(self) -> None:
        print(self.path, self.data.get('maya'))
        cmds.file(
                str(Path(self.path) / self.data.get('maya')),
                i=True,
                namespace=Path(self.data.get('maya')).with_suffix('').name
                )

    def referenceScene(self) -> None:
        cmds.file(
                str(Path(self.path) / self.data.get('maya')),
                reference=True,
                namespace=Path(self.data.get('maya')).with_suffix('').name
                )

    def stageScene(self) -> None: ...
