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

class custom_spin_box(QtWidgets.QDoubleSpinBox):
    def wheelEvent(self, event):
        event.ignore()

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

    def reflection_map_version_change(self):
        print 'reflection_map_version_change'
        reflection_map_spinbox_value = self.refl_map_int_spinbox.value()
        print 'reflection_map_spinbox_value = ',reflection_map_spinbox_value
        reflection_map_string = self.reflection_map
        print 'reflection_map_string = ',reflection_map_string
        reflection_map_string_split = reflection_map_string.split('.')
        reflection_map_spinbox_value_string = str(reflection_map_spinbox_value)
        reflection_map_spinbox_value_string_split = reflection_map_spinbox_value_string.split('.')
        reflection_map_spinbox_value_string = reflection_map_spinbox_value_string_split[0]
        reflection_map_spinbox_value_string_len = len(reflection_map_spinbox_value_string)
        if reflection_map_spinbox_value_string_len == 1:
            reflection_map_spinbox_value_string = '00' + reflection_map_spinbox_value_string
        if reflection_map_spinbox_value_string_len == 2:
            reflection_map_spinbox_value_string = '0' + reflection_map_spinbox_value_string
        reflection_map_string_mod = reflection_map_string_split[0] + '.' + reflection_map_spinbox_value_string + '.exr'
        print 'reflection_map_string_mod = ',reflection_map_string_mod
        cmds.setAttr('reflection_sdt_lgt.fileTextureName',reflection_map_string_mod,type = 'string')
        self.reflection_map_label.setText(reflection_map_string_mod)


    def populate_refl_map(self):
        print 'populate_refl_map'
        self.reflection_map = cmds.getAttr('reflection_sdt_lgt.fileTextureName')
        #print 'reflection_map = ',self.reflection_map
        self.reflection_map_label.setFont(QtGui.QFont('SansSerif', 8))
        self.reflection_map_label.setText(self.reflection_map)

    def populate_refl_map_version(self):
        print 'populate_refl_map_version'
        reflection_map_split = self.reflection_map.split('.')
        reflection_map_version = reflection_map_split[1]
        reflection_map_version = float(reflection_map_version)
        print 'reflection_map_version = ',reflection_map_version
        self.refl_map_int_spinbox.setValue(reflection_map_version)
        self.refl_map_int_spinbox.valueChanged.connect(lambda:self.reflection_map_version_change())

    def populate_render_layers(self):
        print 'populate_render_layers'
        self.render_layers_scan()
        self.render_layer_QListWidget.clear()
        for render_layer in self.render_layers_in_order:
            self.render_layer_QListWidget.addItem(render_layer)
        self.current_render_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        i = 0
        render_layer_QListWidget_count = self.render_layer_QListWidget.count()
        while i < render_layer_QListWidget_count:
            item = self.render_layer_QListWidget.item(i)
            item_text = item.text()
            if item_text == "masterLayer":
                item_text = "defaultRenderLayer"
            print 'item_text = ',item_text
            print 'self.current_render_layer = ',self.current_render_layer
            if item_text == self.current_render_layer:
                print 'MATCH'
                self.current_render_layer_pointer = item
                self.render_layer_QListWidget.setCurrentItem(self.current_render_layer_pointer)
            i += 1
        self.render_layer_QListWidget.itemClicked.connect(lambda:self.render_layer_change())

    def render_layer_change(self):
        print 'render_layer_change'
        new_current_layer = self.render_layer_QListWidget.currentItem().text()
        if new_current_layer == "masterLayer":
            new_current_layer = "defaultRenderLayer"
        cmds.editRenderLayerGlobals(currentRenderLayer = new_current_layer)

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
        window.setFixedHeight(230)
        self.vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        self.refl_map_layout = QtWidgets.QHBoxLayout(main_widget)
        self.reflection_map_label = QtWidgets.QLabel('reflection_map')
        self.refl_map_layout.addWidget(self.reflection_map_label)
        self.refl_map_int_spinbox = custom_spin_box()
        self.refl_map_int_spinbox.setMinimum(1)
        self.refl_map_int_spinbox.setMaximum(15)
        self.refl_map_int_spinbox.setDecimals(0)
        self.refl_map_int_spinbox.setSingleStep(1)
        self.refl_map_int_spinbox.setFixedWidth(65)
        self.refl_map_int_spinbox.setKeyboardTracking(False)
        self.refl_map_layout.addWidget(self.refl_map_int_spinbox)
        self.vertical_layout.addLayout(self.refl_map_layout)
        self.render_layer_QListWidget = QtWidgets.QListWidget()
        self.vertical_layout.addWidget(self.render_layer_QListWidget)
        self.populate_refl_map()
        self.populate_refl_map_version()
        self.populate_render_layers()
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["renderLayerManagerChange", self.populate_render_layers])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["renderLayerChange", self.populate_render_layers])
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    standard_light_rig_pal_instance = STANDARD_LIGHT_RIG()
    standard_light_rig_pal_instance.standard_light_rig_pal_UI()
