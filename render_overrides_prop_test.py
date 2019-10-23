import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

print 'wed'

class custom_spin_box(QtWidgets.QDoubleSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class render_overrides_prop(object):
    def __init__(self):
        hold = ''

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())

    def light_color_state(self):
        pass

    def rect_tex_color_state(self):
        pass

    def light_name_eval(self):
        self.light_names = []
        self.light_names = cmds.ls(type = 'VRayLightRectShape')

    def render_layers_eval(self):
        self.render_layers = cmds.ls(type = 'renderLayer')
        render_layer_order_dict = {}
        self.render_layers_in_order = []
        for layer in self.render_layers:
            render_layer_order_number = cmds.getAttr(layer + ".displayOrder")
            render_layer_order_dict[layer] = render_layer_order_number
        number_of_render_layers = 30
        i = 0
        while i <= number_of_render_layers:
            for layer in render_layer_order_dict:
                layer_number = render_layer_order_dict[layer]
                if layer_number == i:
                    self.render_layers_in_order.append(layer)
            i = i + 1
        self.render_layers_in_order.reverse()

    def populate_gui(self):
        self.light_name_eval()
        self.render_layers_eval()
        self.clearLayout(self.main_horizontal_layout)
        self.light_name_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.clearLayout(self.light_name_layout)
        self.main_horizontal_layout.addLayout(self.light_name_layout)
        self.light_name_layout.setAlignment(Qt.AlignTop)
        self.light_combo_box = QtWidgets.QComboBox()
        self.light_combo_box .setMaximumWidth(180)
        self.light_combo_box .setMinimumHeight(18)
        self.light_name_layout.addWidget(self.light_combo_box)
        for light in self.light_names:
            self.light_combo_box.addItem(light)
        self.light_combo_box.activated[str].connect(lambda:self.value_change())

        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(False)
        self.main_horizontal_layout.addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll.setWidget(self.scroll_widget)
        self.attribute_layout = QtWidgets.QVBoxLayout(self.scroll)
        self.clearLayout(self.attribute_layout)
        self.attribute_layout.setAlignment(Qt.AlignTop)
        self.main_horizontal_layout.addLayout(self.attribute_layout)

        self.translate_layout = QtWidgets.QHBoxLayout(self.scroll)                #---
        self.translate_layout.setAlignment(Qt.AlignTop)
        self.attribute_layout.addLayout(self.translate_layout)
        self.attribute_label = QtWidgets.QLabel('translate    ')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.translate_layout.addWidget(self.attribute_label)
        self.attribute_translateX_float_spinbox = custom_spin_box()
        self.attribute_translateX_float_spinbox.setMinimum(-100)
        self.attribute_translateX_float_spinbox.setMaximum(10000)
        self.attribute_translateX_float_spinbox.setDecimals(3)
        self.attribute_translateX_float_spinbox.setSingleStep(.1)
        self.attribute_translateX_float_spinbox.setFixedWidth(65)
        self.attribute_translateX_float_spinbox.setKeyboardTracking(False)
        self.translate_layout.addWidget(self.attribute_translateX_float_spinbox)
        self.attribute_translateY_float_spinbox = custom_spin_box()
        self.attribute_translateY_float_spinbox.setMinimum(-100)
        self.attribute_translateY_float_spinbox.setMaximum(10000)
        self.attribute_translateY_float_spinbox.setDecimals(3)
        self.attribute_translateY_float_spinbox.setSingleStep(.1)
        self.attribute_translateY_float_spinbox.setFixedWidth(65)
        self.attribute_translateY_float_spinbox.setKeyboardTracking(False)
        self.translate_layout.addWidget(self.attribute_translateY_float_spinbox)
        self.attribute_translateZ_float_spinbox = custom_spin_box()
        self.attribute_translateZ_float_spinbox.setMinimum(-100)
        self.attribute_translateZ_float_spinbox.setMaximum(10000)
        self.attribute_translateZ_float_spinbox.setDecimals(3)
        self.attribute_translateZ_float_spinbox.setSingleStep(.1)
        self.attribute_translateZ_float_spinbox.setFixedWidth(65)
        self.attribute_translateZ_float_spinbox.setKeyboardTracking(False)
        self.translate_layout.addWidget(self.attribute_translateZ_float_spinbox)
        self.translate_layout_spacer_label = QtWidgets.QLabel(' ')
        self.translate_layout.addWidget(self.translate_layout_spacer_label)
        self.rotate_layout = QtWidgets.QHBoxLayout(self.scroll)                #---
        self.rotate_layout.setAlignment(Qt.AlignTop)
        self.attribute_layout.addLayout(self.rotate_layout)
        self.attribute_label = QtWidgets.QLabel('rotate        ')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.rotate_layout.addWidget(self.attribute_label)
        self.attribute_rotateX_float_spinbox = custom_spin_box()
        self.attribute_rotateX_float_spinbox.setMinimum(-100)
        self.attribute_rotateX_float_spinbox.setMaximum(10000)
        self.attribute_rotateX_float_spinbox.setDecimals(3)
        self.attribute_rotateX_float_spinbox.setSingleStep(.1)
        self.attribute_rotateX_float_spinbox.setFixedWidth(65)
        self.attribute_rotateX_float_spinbox.setKeyboardTracking(False)
        self.rotate_layout.addWidget(self.attribute_rotateX_float_spinbox)
        self.attribute_rotateY_float_spinbox = custom_spin_box()
        self.attribute_rotateY_float_spinbox.setMinimum(-100)
        self.attribute_rotateY_float_spinbox.setMaximum(10000)
        self.attribute_rotateY_float_spinbox.setDecimals(3)
        self.attribute_rotateY_float_spinbox.setSingleStep(.1)
        self.attribute_rotateY_float_spinbox.setFixedWidth(65)
        self.attribute_rotateY_float_spinbox.setKeyboardTracking(False)
        self.rotate_layout.addWidget(self.attribute_rotateY_float_spinbox)
        self.attribute_rotateZ_float_spinbox = custom_spin_box()
        self.attribute_rotateZ_float_spinbox.setMinimum(-100)
        self.attribute_rotateZ_float_spinbox.setMaximum(10000)
        self.attribute_rotateZ_float_spinbox.setDecimals(3)
        self.attribute_rotateZ_float_spinbox.setSingleStep(.1)
        self.attribute_rotateZ_float_spinbox.setFixedWidth(65)
        self.attribute_rotateZ_float_spinbox.setKeyboardTracking(False)
        self.rotate_layout.addWidget(self.attribute_rotateZ_float_spinbox)
        self.rotate_layout_spacer_label = QtWidgets.QLabel('')
        self.rotate_layout.addWidget(self.rotate_layout_spacer_label)
        self.scale_layout = QtWidgets.QHBoxLayout(self.scroll)                #---
        self.scale_layout.setAlignment(Qt.AlignTop)
        self.attribute_layout.addLayout(self.scale_layout)
        self.attribute_label = QtWidgets.QLabel('scale         ')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.scale_layout.addWidget(self.attribute_label)
        self.attribute_scaleX_float_spinbox = custom_spin_box()
        self.attribute_scaleX_float_spinbox.setMinimum(-100)
        self.attribute_scaleX_float_spinbox.setMaximum(10000)
        self.attribute_scaleX_float_spinbox.setDecimals(3)
        self.attribute_scaleX_float_spinbox.setSingleStep(.1)
        self.attribute_scaleX_float_spinbox.setFixedWidth(65)
        self.attribute_scaleX_float_spinbox.setKeyboardTracking(False)
        self.scale_layout.addWidget(self.attribute_scaleX_float_spinbox)
        self.attribute_scaleY_float_spinbox = custom_spin_box()
        self.attribute_scaleY_float_spinbox.setMinimum(-100)
        self.attribute_scaleY_float_spinbox.setMaximum(10000)
        self.attribute_scaleY_float_spinbox.setDecimals(3)
        self.attribute_scaleY_float_spinbox.setSingleStep(.1)
        self.attribute_scaleY_float_spinbox.setFixedWidth(65)
        self.attribute_scaleY_float_spinbox.setKeyboardTracking(False)
        self.scale_layout.addWidget(self.attribute_scaleY_float_spinbox)
        self.attribute_scaleZ_float_spinbox = custom_spin_box()
        self.attribute_scaleZ_float_spinbox.setMinimum(-100)
        self.attribute_scaleZ_float_spinbox.setMaximum(10000)
        self.attribute_scaleZ_float_spinbox.setDecimals(3)
        self.attribute_scaleZ_float_spinbox.setSingleStep(.1)
        self.attribute_scaleZ_float_spinbox.setFixedWidth(65)
        self.attribute_scaleZ_float_spinbox.setKeyboardTracking(False)
        self.scale_layout.addWidget(self.attribute_scaleZ_float_spinbox)
        self.scale_layout_spacer_label = QtWidgets.QLabel('')
        self.scale_layout.addWidget(self.scale_layout_spacer_label)

        self.attribute_label = QtWidgets.QLabel('enabled')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)
        enabled_checkbox = QtWidgets.QCheckBox()
        self.attribute_layout.addWidget(enabled_checkbox)

        self.attribute_label = QtWidgets.QLabel('light_color  ')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)

        self.light_color_pushbutton = QtWidgets.QPushButton()
        self.light_color_pushbutton.setMinimumWidth(30)
        self.light_color_pushbutton.setMaximumWidth(30)
        self.light_color_pushbutton.setMinimumHeight(30)
        self.light_color_pushbutton.setMaximumHeight(30)
        self.light_color_pushbutton.clicked.connect(partial(self.light_color_state))
        self.attribute_layout.addWidget(self.light_color_pushbutton)
        self.light_color_r = 100
        self.light_color_g = 10
        self.light_color_b = 1
        color_string = "rgb(" + str(self.light_color_r) + "," + str(self.light_color_g) + "," + str(self.light_color_b) + ")"
        self.light_color_pushbutton.setStyleSheet("QPushButton { background-color: %s}" %color_string)


        self.attribute_label = QtWidgets.QLabel('intensity')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)
        self.attribute_intensityMult_float_spinbox = custom_spin_box()
        self.attribute_intensityMult_float_spinbox.setMinimum(-100)
        self.attribute_intensityMult_float_spinbox.setMaximum(10000)
        self.attribute_intensityMult_float_spinbox.setDecimals(3)
        self.attribute_intensityMult_float_spinbox.setSingleStep(.1)
        self.attribute_intensityMult_float_spinbox.setFixedWidth(65)
        self.attribute_intensityMult_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_intensityMult_float_spinbox)
        self.attribute_label = QtWidgets.QLabel('U size')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)
        self.attribute_intensityMult_float_spinbox = custom_spin_box()
        self.attribute_intensityMult_float_spinbox.setMinimum(-100)
        self.attribute_intensityMult_float_spinbox.setMaximum(10000)
        self.attribute_intensityMult_float_spinbox.setDecimals(3)
        self.attribute_intensityMult_float_spinbox.setSingleStep(.1)
        self.attribute_intensityMult_float_spinbox.setFixedWidth(65)
        self.attribute_intensityMult_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_intensityMult_float_spinbox)
        self.attribute_label = QtWidgets.QLabel('V size')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)
        self.attribute_intensityMult_float_spinbox = custom_spin_box()
        self.attribute_intensityMult_float_spinbox.setMinimum(-100)
        self.attribute_intensityMult_float_spinbox.setMaximum(10000)
        self.attribute_intensityMult_float_spinbox.setDecimals(3)
        self.attribute_intensityMult_float_spinbox.setSingleStep(.1)
        self.attribute_intensityMult_float_spinbox.setFixedWidth(65)
        self.attribute_intensityMult_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_intensityMult_float_spinbox)
        self.attribute_label = QtWidgets.QLabel('directional')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)
        self.attribute_intensityMult_float_spinbox = custom_spin_box()
        self.attribute_intensityMult_float_spinbox.setMinimum(-100)
        self.attribute_intensityMult_float_spinbox.setMaximum(10000)
        self.attribute_intensityMult_float_spinbox.setDecimals(3)
        self.attribute_intensityMult_float_spinbox.setSingleStep(.1)
        self.attribute_intensityMult_float_spinbox.setFixedWidth(65)
        self.attribute_intensityMult_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_intensityMult_float_spinbox)
        self.attribute_label = QtWidgets.QLabel('use rect tex')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)
        use_rect_tex_checkbox = QtWidgets.QCheckBox()
        self.attribute_layout.addWidget(use_rect_tex_checkbox)

        self.attribute_label = QtWidgets.QLabel('rect_tex     ')
        self.attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(self.attribute_label)
        self.rect_text_color_pushbutton = QtWidgets.QPushButton()
        self.rect_text_color_pushbutton.setMinimumWidth(30)
        self.rect_text_color_pushbutton.setMaximumWidth(30)
        self.rect_text_color_pushbutton.setMinimumHeight(30)
        self.rect_text_color_pushbutton.setMaximumHeight(30)
        self.rect_text_color_pushbutton.clicked.connect(partial(self.rect_tex_color_state))
        self.attribute_layout.addWidget(self.rect_text_color_pushbutton)
        self.light_rect_color_r = 10
        self.light_rect_color_g = 100
        self.light_rect_color_b = 1
        color_string = "rgb(" + str(self.light_rect_color_r) + "," + str(self.light_rect_color_g) + "," + str(self.light_rect_color_b) + ")"
        self.rect_text_color_pushbutton.setStyleSheet("QPushButton { background-color: %s}" %color_string)

        print self.render_layers_in_order
        self.render_layer_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.clearLayout(self.render_layer_layout)
        self.main_horizontal_layout.addLayout(self.render_layer_layout)
        self.render_layer_layout.setAlignment(Qt.AlignTop)
        self.render_layer_checkbox_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.clearLayout(self.render_layer_checkbox_layout)
        self.main_horizontal_layout.addLayout(self.render_layer_checkbox_layout)
        self.render_layer_checkbox_layout.setAlignment(Qt.AlignTop)
        #self.spacer_label = QtWidgets.QLabel('')
        #self.render_layer_checkbox_layout.addWidget(self.spacer_label)
        for render_layer in self.render_layers_in_order:
            if render_layer != 'defaultRenderLayer':
                self.attribute_label = QtWidgets.QLabel(render_layer)
                self.attribute_label.setFont(QtGui.QFont('SansSerif', 7))
                self.render_layer_layout.addWidget(self.attribute_label)
                layer_checkbox = QtWidgets.QCheckBox()
                self.render_layer_checkbox_layout.addWidget(layer_checkbox)

        button_clear_selected_layer_overrides = QtWidgets.QPushButton("clear overrides in selected layers")
        button_clear_all_overrides = QtWidgets.QPushButton("clear overrides in all layers")
        button_set_selected_layer_overrides = QtWidgets.QPushButton("set overrides in selected layers")
        button_set_all_layer_overrides = QtWidgets.QPushButton("set overrides in all layers")
        #button_set_overrides.setFixedWidth(button_width)
        #button_set_overrides.setFixedHeight(button_height)
        #button_set_overrides.pressed.connect(partial(self.allToggleTexture_off))
        self.button_horizontal_layout.addWidget(button_clear_selected_layer_overrides)
        self.button_horizontal_layout.addWidget(button_clear_all_overrides)
        self.button_horizontal_layout.addWidget(button_set_selected_layer_overrides)
        self.button_horizontal_layout.addWidget(button_set_all_layer_overrides)

    def value_change(self):
        current_light = self.light_combo_box.currentText()
        print 'current_light = ',current_light
        intensityMult_value = cmds.getAttr(current_light + '.intensityMult')
        print 'intensityMult_value = ',intensityMult_value
        print 'setting ' + str(self.attribute_intensityMult_float_spinbox) + ' to ' + str(intensityMult_value)
        self.attribute_intensityMult_float_spinbox.setValue(intensityMult_value)


    def render_overrides_prop_UI(self):
        window_name = "render_overrides_prop"
        if cmds.window(window_name,exists = True):
            cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        self.window = QtWidgets.QMainWindow(parent)
        self.window.setObjectName(window_name)
        self.window.setWindowTitle(window_name)
        #self.window.setFixedSize(1015,300)
        self.window.setFixedWidth(550)
        self.window.setFixedHeight(625)
        self.main_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.base_vertical_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_horizontal_layout = QtWidgets.QHBoxLayout(self.main_widget)
        self.base_vertical_layout.addLayout(self.main_horizontal_layout)
        self.button_horizontal_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.base_vertical_layout.addLayout(self.button_horizontal_layout)
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["renderLayerManagerChange", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["renderLayerChange", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["NameChanged", self.populate_gui])
        self.populate_gui()
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.show()

def main():
    render_overrides_prop_inst = render_overrides_prop()
    render_overrides_prop_inst.render_overrides_prop_UI()

main()
