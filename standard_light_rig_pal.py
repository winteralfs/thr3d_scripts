import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import subprocess
import webbrowser
import shiboken2

class STANDARD_LIGHT_RIG(object):
    def __init__(self):
        print 'standard light rig pal'

    def render_layers_scan(self):
        print 'render_layers_scan'
        render_layers = cmds.ls(type = "renderLayer")
        #current_render_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        render_layer_order_dict = {}
        self.render_layers_in_order = []
        for layer in render_layers:
            render_layer_order_number = cmds.getAttr(layer + ".displayOrder")
            render_layer_order_dict[layer] = render_layer_order_number
        number_of_render_layers = len(render_layer_order_dict)
        i = 0
        while i <= number_of_render_layers:
            for layer in render_layer_order_dict:
                layer_number = render_layer_order_dict[layer]
                if layer_number == i:
                    self.render_layers_in_order.append(layer)
            i = i + 1
        self.render_layers_in_order.reverse()

    #def render_layer_state(self):
        #render_layer_mod = "masterLayer"
        #elf.render_layer_QListWidget.clear()
        #render_layer_QListWidget = self.render_layer_QListWidget
        #for render_layer in self.render_layers:
            #if render_layer == "defaultRenderLayer":
                #self.render_layer_QListWidget.addItem(render_layer_mod)
            #if render_layer != "defaultRenderLayer":
                #self.render_layer_QListWidget.addItem(render_layer)
        #i = 0
        #render_layer_QListWidget_count = render_layer_QListWidget.count()
        #while i < render_layer_QListWidget_count:
            #item = render_layer_QListWidget.item(i)
            #item_text = item.text()
            #if item_text == "masterLayer":
                #item_text = "defaultRenderLayer"
            #if item_text == self.current_render_layer:
                #self.current_render_layer_pointer = item
            #i += 1
        #render_layer_QListWidget.setCurrentItem(self.current_render_layer_pointer)
        #self.render_layer_QListWidget = render_layer_QListWidget
        #render_layer_QListWidget.itemClicked.connect(self.layer_change)

    def populate_render_layers(self):
        print 'populate_render_layers'
        self.render_layers_scan()
        self.render_layer_QListWidget.clear()
        for render_layer in self.render_layers_in_order:
            self.render_layer_QListWidget.addItem(render_layer)
        self.render_layer_QListWidget.itemClicked.connect(self.render_layer_change)

    def render_layer_change(self):
        print 'render_layer_change'
        #new_current_layer = self.render_layer_QListWidget.currentItem().text()
        #if new_current_layer == "masterLayer":
            #new_current_layer = "defaultRenderLayer"
        #cmds.editRenderLayerGlobals(currentRenderLayer = new_current_layer)

    def standard_light_rig_pal_UI(self):
        print 'standard_light_rig_pal_UI'
        window_name = "standard_light_rig_pal"
        if cmds.window(window_name,exists = True):
            cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(window_name)
        window.setWindowTitle(window_name)
        main_widget = QtWidgets.QWidget()
        window.setCentralWidget(main_widget)
        window.setFixedWidth(500)
        window.setFixedHeight(170)
        self.vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        self.render_layer_QListWidget = QtWidgets.QListWidget()
        self.vertical_layout.addWidget(self.render_layer_QListWidget)
        self.populate_render_layers()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    standard_light_rig_pal_instance = STANDARD_LIGHT_RIG()
    standard_light_rig_pal_instance.standard_light_rig_pal_UI()
