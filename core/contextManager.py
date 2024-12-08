from typing import List
from contextlib import contextmanager

from maya import cmds


@contextmanager
def withSelectionLess() -> List[str]:

    backup_selection = cmds.ls(sl=True)

    try:
        yield backup_selection

    finally:
        cmds.select(backup_selection)


@contextmanager
def withViewChangeLess(
        viewport_option={}
        ) -> None:
    # backup values
    current_selection = cmds.ls(sl=True)
    current_viewport = cmds.getPanel(withFocus=True)
    current_camera = cmds.modelPanel(current_viewport, camera=True, query=True)
    current_viewport_options = {}

    for key in viewport_option.keys():
        kwargs = {key: True}
        current_viewport_options[key] = cmds.modelEditor(current_viewport, **kwargs, query=True)

    try:
        # setup viewport has expected
        tmp_camera = cmds.duplicate(current_camera)
        cmds.lookThru(current_viewport, tmp_camera)
        cmds.select(current_selection)
        cmds.modelEditor(current_viewport, edit=True, **viewport_option)
        cmds.viewSet(cmds.listRelatives(tmp_camera, s=True)[0], h=True)
        cmds.viewFit()
        print('selection:', current_selection)
        yield

    except Exception as e:
        cmds.warning(e)

    finally:
        # return to backup values
        cmds.modelEditor(current_viewport, edit=True, **current_viewport_options)
        cmds.lookThru(current_viewport, current_camera)
        cmds.delete(tmp_camera)


@contextmanager
def withIsolate() -> None:

    current_viewport = cmds.getPanel(withFocus=True)

    try:
        print('enter try')
        cmds.isolateSelect(current_viewport, state=True)
        print('isolate state to True')
        set_to_clear = cmds.isolateSelect(current_viewport, vo=True, q=True)
        if set_to_clear:
            cmds.sets(clear=set_to_clear)
        print('set cleared')
        cmds.isolateSelect(current_viewport, addSelected=True)
        print('add selection to isolate')
        yield

    finally:
        cmds.isolateSelect(current_viewport, state=False)
