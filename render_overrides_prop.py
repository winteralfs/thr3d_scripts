import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

class custom_spin_box(QtWidgets.QDoubleSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class render_overrides_prop(object):
    def __init__(self):
        hold = ''

    def render_overrides_prop_UI(self):
        window_name = "render_overrides_prop"
        if cmds.window(window_name,exists = True):
            cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(window_name)
        window.setWindowTitle(window_name)
        #window.setFixedSize(1015,300)
        window.setFixedWidth(800)
        window.setMinimumHeight(250)
        main_widget = QtWidgets.QWidget()
        window.setCentralWidget(main_widget)
        main_horizontal_layout = QtWidgets.QHBoxLayout(main_widget)
        self.light_name_layout = QtWidgets.QVBoxLayout(main_widget)
        main_horizontal_layout.addLayout(self.light_name_layout)
        self.attribute_layout = QtWidgets.QVBoxLayout(main_widget)
        main_horizontal_layout.addLayout(self.attribute_layout)
        self.render_layer_layout = QtWidgets.QVBoxLayout(main_widget)
        main_horizontal_layout.addLayout(self.render_layer_layout)
        self.render_layer_checkbox_layout = QtWidgets.QVBoxLayout(main_widget)
        main_horizontal_layout.addLayout(self.render_layer_checkbox_layout)

        self.light_combo_box = QtWidgets.QComboBox()
        self.light_combo_box .setMaximumWidth(180)
        self.light_combo_box .setMinimumHeight(18)
        #self.light_combo_box .setStyleSheet("""QWidget{color:#a3b3bf;}QComboBox{color:#a3b3bf;}QLineEdit{color:#a3b3bf;}""")
        #self.light_name_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.light_name_layout.addWidget(self.light_combo_box)
        self.light_combo_box.addItem("test_light_ababa")
        #self.light_combo_box.addItem("UV-centric")
        #self.light_combo_box.activated[str].connect(lambda:self.centric_state())
        #self.light_combo_box = self.texture_based_uv_set_based_combobox.currentText()

        self.attribute_label = QtWidgets.QLabel('intensity')
        self.attribute_layout.addWidget(self.attribute_label)
        self.attribute_intensity_float_spinbox = custom_spin_box()
        self.attribute_intensity_float_spinbox.setMinimum(-100)
        self.attribute_intensity_float_spinbox.setMaximum(10000)
        self.attribute_intensity_float_spinbox.setDecimals(3)
        self.attribute_intensity_float_spinbox.setSingleStep(.1)
        self.attribute_intensity_float_spinbox.setFixedWidth(65)
        self.attribute_intensity_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_intensity_float_spinbox)

        self.attribute_label = QtWidgets.QLabel('Ft')
        self.render_layer_layout.addWidget(self.attribute_label)
        self.layer_checkbox_1 = QtWidgets.QCheckBox()
        self.render_layer_checkbox_layout.addWidget(self.layer_checkbox_1)
        self.attribute_label = QtWidgets.QLabel('Bk')
        self.render_layer_layout.addWidget(self.attribute_label)
        self.layer_checkbox_2 = QtWidgets.QCheckBox()
        self.render_layer_checkbox_layout.addWidget(self.layer_checkbox_2)

        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    render_overrides_prop_inst = render_overrides_prop()
    render_overrides_prop_inst.render_overrides_prop_UI()

main()
