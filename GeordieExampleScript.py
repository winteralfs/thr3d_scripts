import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class lights_palette():
    def __init__(self):
        pass

    def workspace_creation(self):
        workspace_name = "lights_texture_workspace"
        script = 'self.light_texture_view()'
        sze = 200
        if cmds.workspaceControl(workspace_name,query = True, exists = True):
            cmds.deleteUI(workspace_name)
        self.workspace = cmds.workspaceControl(workspace_name,label = workspace_name,uiScript = '',ih = sze, iw = sze)
        self.light_texture_view()

    def light_texture_view(self):
        window_name = "lights_texture_window"
        if cmds.window(window_name,exists = True):
            cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(window_name)
        window.setWindowTitle(window_name)
        main_widget = QtWidgets.QWidget()
        window.setCentralWidget(main_widget)
        window.setFixedSize(250,200)
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

ltv = lights_palette()
ltv.workspace_creation()
