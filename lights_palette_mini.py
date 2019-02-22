import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class lightsPalette():
    def __init__(self):
        var = "chris"

    def allToggleTexture_off(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 0)
     
    def selectedToggleTexture_off(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 0)
     
    def allToggleTexture_on(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 1)
     
    def selectedToggleTexture_on(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 1)
     
    def allToggleTexture(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        get_toggle = cmds.getAttr(kid + ".showTex")
                        if get_toggle == 0:
                            cmds.setAttr(kid + ".showTex", 1)
                        if get_toggle == 1:
                            cmds.setAttr(kid + ".showTex", 0)
     
    def selectedToggleTexture(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        get_toggle = cmds.getAttr(kid + ".showTex")
                        if get_toggle == 0:
                            cmds.setAttr(kid + ".showTex", 1)
                        if get_toggle == 1:
                            cmds.setAttr(kid + ".showTex", 0)

    def hideLights(self,checked):
        panels = cmds.getPanel( type = "modelPanel" )
        if checked == True:
            self.button_show_lights.setText("LIGHTS HIDDEN")
            self.button_show_lights.setFixedHeight(20)
            for mPanel in panels:
                cmds.modelEditor(mPanel, edit = True, lt = 0, lc = 0)
        if checked == False:
            self.button_show_lights.setText("hide lights")
            self.button_show_lights.setFixedHeight(20)
            for mPanel in panels:
                cmds.modelEditor(mPanel, edit = True, lt = 1, lc = 1)
     
    def lightsTextureView(self):
        windowName = "LTV"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        window.setFixedSize(250,150)
        grid_layout = QtWidgets.QGridLayout(mainWidget)
        label_all = QtWidgets.QLabel("all")
        label_all.setAlignment(QtCore.Qt.AlignCenter)    
        grid_layout.addWidget(label_all,0,0)
        label_selected = QtWidgets.QLabel("selected")
        label_selected.setAlignment(QtCore.Qt.AlignCenter)  
        grid_layout.addWidget(label_selected,0,1)
        button_all_off = QtWidgets.QPushButton("off")
        button_all_off.pressed.connect(partial(self.allToggleTexture_off))
        grid_layout.addWidget(button_all_off,1,0)
        button_all_on = QtWidgets.QPushButton("on")
        button_all_on.pressed.connect(partial(self.allToggleTexture_on))
        grid_layout.addWidget(button_all_on,2,0)
        button_all_toggle = QtWidgets.QPushButton("toggle")
        grid_layout.addWidget(button_all_toggle,3,0)
        button_all_toggle.pressed.connect(partial(self.allToggleTexture))
        button_sel_off = QtWidgets.QPushButton("off")
        button_sel_off.pressed.connect(partial(self.selectedToggleTexture_off))         
        grid_layout.addWidget(button_sel_off,1,1)
        button_sel_on = QtWidgets.QPushButton("on")
        button_sel_on.pressed.connect(partial(self.selectedToggleTexture_on))       
        grid_layout.addWidget(button_sel_on,2,1)
        button_sel_toggle = QtWidgets.QPushButton("toggle")
        button_sel_toggle.pressed.connect(partial(self.selectedToggleTexture))     
        grid_layout.addWidget(button_sel_toggle,3,1)
        self.button_show_lights = QtWidgets.QPushButton("hide_lights")
        self.button_show_lights.setFixedHeight(20)
        self.button_show_lights.setCheckable(True)
        self.button_show_lights.toggled.connect(partial(self.hideLights))
        self.button_show_lights.setStyleSheet("QPushButton::checked{color: rgb(249, 0, 0);""border:1px solid rgb(249, 0, 0)};")
        grid_layout.addWidget(self.button_show_lights,4,0,1,2)
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()
 
ltv = lightsPalette()
ltv.lightsTextureView()
