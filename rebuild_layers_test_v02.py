import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
import re


class LAYERS_WINDOW_TOOL():
    def __init__(self):
        chris = ''

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())

    def render_layer_change(self,button_render_layer):
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                render_layer_linked_to_button = self.render_layer_button_pointer_dic[button_render_layer]
                if render_layer_linked_to_button == render_layer:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)

    def evaluate_cameras(self):
        #print 'evaluate cameras'
        self.renderable_cameras_dic = {}
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                renderable_cameras = []
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                for camera in self.cameras:
                    camera_renderable = cmds.getAttr(camera + '.renderable')
                    if camera_renderable == 1:
                        renderable_cameras.append(camera)
            self.renderable_cameras_dic[render_layer] = renderable_cameras
            cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def set_render_camera(self):
        #print 'set_render_camera'
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                camera_comboBox_pointer = self.render_layer_camera_comboBox_dic[render_layer]
                chosen_camera = camera_comboBox_pointer.currentText()
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                for camera in self.cameras:
                    if camera == chosen_camera:
                        cmds.editRenderLayerAdjustment((camera + '.renderable'))
                        cmds.setAttr((camera + '.renderable'), 1)
                    else:
                        cmds.editRenderLayerAdjustment((camera + '.renderable'),remove = True)
                        cmds.setAttr(camera + '.renderable', 0)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def populate_gui(self):
        #print 'populate_gui'
        self.render_layer_camera_comboBox_dic = {}
        self.render_layer_button_pointer_dic = {}
        render_layer_order_dict = {}
        render_layers_in_order = []
        self.cameras = cmds.ls(type = 'camera')
        self.render_layers = cmds.ls(type = "renderLayer")
        for layer in self.render_layers:
            render_layer_order_number = cmds.getAttr(layer + ".displayOrder")
            render_layer_order_dict[layer] = render_layer_order_number
        number_of_render_layers = len(self.render_layers)
        i = 0
        while i <= number_of_render_layers:
            for layer in render_layer_order_dict:
                layer_number = render_layer_order_dict[layer]
                if layer_number == i:
                    render_layers_in_order.append(layer)
            i = i + 1
        render_layers_in_order.reverse()
        self.render_layers = render_layers_in_order
        self.initial_layer = cmds.editRenderLayerGlobals(query = True, currentRenderLayer = True)
        if "defaultRenderLayer" == self.render_layers[0]:
            self.render_layers.reverse()
        self.clear_layout(self.vertical_layout)
        self.evaluate_cameras()
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                self.render_layer_layout = QtWidgets.QHBoxLayout()
                self.vertical_layout.addLayout(self.render_layer_layout)
                button_OIL = QtWidgets.QPushButton('OIL')
                button_OIL.setFixedSize(30,21)
                self.render_layer_layout.addWidget(button_OIL)
                button_OVL = QtWidgets.QPushButton('OVL')
                button_OVL.setFixedSize(30,21)
                self.render_layer_layout.addWidget(button_OVL)
                button_render_layer = QtWidgets.QPushButton(render_layer)
                self.render_layer_button_pointer_dic[button_render_layer] = render_layer
                button_render_layer.setFixedSize(325,21)
                if render_layer == self.initial_layer:
                    button_render_layer.setStyleSheet("background-color: rgb(75, 135, 175);")
                self.render_layer_layout.addWidget(button_render_layer)
                camera_comboBox = self.cameras_combobox = QtWidgets.QComboBox()
                self.render_layer_camera_comboBox_dic[render_layer] = camera_comboBox
                self.cameras_combobox.activated[str].connect(lambda:self.set_render_camera())
                self.cameras_combobox.setFixedSize(150,21)
                self.cameras_combobox.clear()
                self.render_layer_layout.addWidget(self.cameras_combobox)
                for camera in self.cameras:
                    self.cameras_combobox.addItem(camera)
                i = 0
                renderable_cameras = self.renderable_cameras_dic[render_layer] or []
                for camera in self.cameras:
                    if camera == renderable_cameras[0]:
                        self.cameras_combobox.setCurrentIndex(i)
                    i = i + 1
                if len(renderable_cameras) > 1:
                    self.cameras_combobox.setStyleSheet("background-color: rgb(130, 10, 10);")
                camera = renderable_cameras[0]
                camera_split = camera.split('_')
                print 'camera_split = ',camera_split
                print 'render_layer = ',render_layer
                if camera_split[0] != render_layer:
                    self.cameras_combobox.setStyleSheet("background-color: rgb(130, 10, 10);")
        for button_render_layer in self.render_layer_button_pointer_dic:
            button_render_layer.pressed.connect(partial(self.render_layer_change,button_render_layer))

    def window_gen(self):
        #print 'window_gen'
        self.window_name = "render layers tool"
        if cmds.window(self.window_name,exists = True):
            cmds.deleteUI(self.window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(self.window_name)
        window.setWindowTitle(self.window_name)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        window.setFixedSize(550,200)
        self.vertical_layout = QtWidgets.QVBoxLayout(mainWidget)
        self.vertical_layout.setMargin(0)
        self.vertical_layout.setSpacing(0)
        self.layout_top = QtWidgets.QVBoxLayout()
        self.layout_top.setMargin(0)
        self.layout_top.setSpacing(0)
        self.vertical_layout.addLayout(self.layout_top)
        self.layout_bottom = QtWidgets.QVBoxLayout()
        self.layout_bottom.setMargin(0)
        self.layout_bottom.setSpacing(0)
        self.vertical_layout.addLayout(self.layout_bottom)
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["NameChanged", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerManagerChange", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerChange", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["SelectionChanged", self.populate_gui])
        self.populate_gui()
        window.show()

def main():
    layers_tool_inst = LAYERS_WINDOW_TOOL()
    layers_tool_inst.window_gen()

main()
