import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

print 'friday night'

class OBJECT_PROPAGATOR(object):
    def __init__(self):
        chris = 'temp'

    def reference_objects_detect(self):
        reference_objects_string = ''
        self.reference_objects = cmds.ls(sl = True)
        print 'reference_objects = ',self.reference_objects
        for reference_object in self.reference_objects:
            reference_objects_string = reference_objects_string + ' ' + reference_object
        self.reference_objects_line_edit.setText(reference_objects_string)

    def copy_object_detect(self):
        self.copy_object = cmds.ls(sl = True)
        print 'copy_object = ',self.copy_object
        for list_item in self.copy_object:
            self.copy_object_line_edit.setText(list_item)

    def run_duplicate(self):
        print 'run_transform_button'
        self.copy_objects = []
        self.copy_objects_translation_X_dic = {}
        self.copy_objects_translation_Y_dic = {}
        self.copy_objects_translation_Z_dic = {}
        for reference_object in self.reference_objects:
            print 'reference_object = ',reference_object
            duplicate_copy_object = cmds.duplicate(self.copy_object)
            print 'duplicate_copy_object = ',duplicate_copy_object
            cmds.select(duplicate_copy_object[0])
            duplicate_copy_object_long_name = cmds.ls(sl = True, long = True)
            cmds.select(clear = True)
            print 'duplicate_copy_object_long_name = ',duplicate_copy_object_long_name
            world_transforms_reference_object = cmds.xform(reference_object,q = True, ws = True,rotatePivot = True)
            print 'world_transforms_reference_object = ',world_transforms_reference_object
            cmds.xform(duplicate_copy_object[0],cp = True)
            cmds.move( 0, 0, 0,duplicate_copy_object[0],rpr = True)
            transX = world_transforms_reference_object[0]
            self.copy_objects_translation_X_dic[duplicate_copy_object[0]] = world_transforms_reference_object
            transY = world_transforms_reference_object[1]
            self.copy_objects_translation_Y_dic[duplicate_copy_object[0]] = world_transforms_reference_object
            transZ = world_transforms_reference_object[2]
            self.copy_objects_translation_Z_dic[duplicate_copy_object[0]] = world_transforms_reference_object
            cmds.xform(duplicate_copy_object[0],r = True, t = (transX,transY,transZ))
            self.copy_objects.append(duplicate_copy_object_long_name)
        cmds.hide(self.copy_object)
        print 'self.copy_objects_translation_X_dic = ',self.copy_objects_translation_X_dic

    def translate_X_slider_activate(self):
        print 'translate X slider activate'
        self.translate_X_slider_value = self.translate_X_slider.value()
        self.translate_X_slider_value = self.translate_X_slider_value * .3
        it = 0
        for copy_object in self.copy_objects:
            print ' '
            #print 'copy_object[0] = ',copy_object[0]
            copy_object_split = copy_object[0].split('|')
            copy_object_short_name = copy_object_split[-1]
            default_translations_ws = cmds.xform(copy_object[0],q = True, ws = True,rotatePivot = True)
            default_translation_x_value_ws = default_translations_ws[0]
            copy_object_default_values_ws = self.copy_objects_translation_X_dic[copy_object_short_name]
            cmds.xform(copy_object[0],cp = True)
            copy_object_string_translate_X = copy_object[0] + '.translateX'
            print 'copy_object_default_values_ws = ',copy_object_default_values_ws
            default_trans_x = copy_object_default_values_ws[0]
            default_trans_y = copy_object_default_values_ws[1]
            default_trans_z = copy_object_default_values_ws[2]
            cmds.xform(copy_object[0],cp = True)
            cmds.move(0, 0, 0,copy_object[0],rpr = True)
            #cmds.xform(copy_object[0],r = True, t = (default_trans_x,default_trans_y,default_trans_z))
            cmds.move(default_trans_x,default_trans_y,default_trans_z,copy_object[0],rpr = True)
            if it != 0:
                if self.translate_X_slider_value != 0:
                    print 'default_trans_x = ',default_trans_x
                    default_trans_x_modified = default_trans_x + self.translate_X_slider_value
                    print 'default_trans_x_modified = ',default_trans_x_modified
                    cmds.move(default_trans_x_modified,default_trans_y,default_trans_z,copy_object[0],rpr = True)
                    #cmds.xform(copy_object[0],r = True, t = (default_trans_x_modified,default_trans_y,default_trans_z))
            it = it + 1

    def translate_Y_slider_activate(self):
        print 'translate Y slider activate'
        self.translate_Y_slider_value = self.translate_Y_slider.value()
        self.translate_Y_slider_value = self.translate_Y_slider_value * .03
        print self.translate_Y_slider_value
        print self.copy_objects
        for copy_object in self.copy_objects:
            cmds.xform(copy_object[0],cp = True)
            copy_object_string_translate_Y = copy_object[0] + '.translateY'
            cmds.setAttr(copy_object_string_translate_Y,self.translate_Y_slider_value)

    def translate_Z_slider_activate(self):
        print 'translate Z slider activate'
        self.translate_Z_slider_value = self.translate_Z_slider.value()
        self.translate_Z_slider_value = self.translate_Z_slider_value * .03
        print self.translate_Z_slider_value
        print self.copy_objects
        for copy_object in self.copy_objects:
            cmds.xform(copy_object[0],cp = True)
            copy_object_string_translate_Z = copy_object[0] + '.translateZ'
            cmds.setAttr(copy_object_string_translate_Z,self.translate_Z_slider_value)

    def rotation_X_slider_activate(self):
        print 'rotation X slider activate'
        self.rotation_X_slider_value = self.rotation_X_slider.value()
        self.rotation_X_slider_value = self.rotation_X_slider_value * .5
        print self.rotation_X_slider_value
        print self.copy_objects
        for copy_object in self.copy_objects:
            cmds.xform(copy_object[0],cp = True)
            copy_object_string_rotation_X = copy_object[0] + '.rotateX'
            cmds.setAttr(copy_object_string_rotation_X,self.rotation_X_slider_value)

    def rotation_Y_slider_activate(self):
        print 'rotation Y slider activate'
        self.rotation_Y_slider_value = self.rotation_Y_slider.value()
        self.rotation_Y_slider_value = self.rotation_Y_slider_value * .5
        print self.rotation_Y_slider_value
        print self.copy_objects
        for copy_object in self.copy_objects:
            cmds.xform(copy_object[0],cp = True)
            copy_object_string_rotation_Y = copy_object[0] + '.rotateY'
            cmds.setAttr(copy_object_string_rotation_Y,self.rotation_Y_slider_value)

    def rotation_Z_slider_activate(self):
        print 'rotation Z slider activate'
        self.rotation_Z_slider_value = self.rotation_Z_slider.value()
        self.rotation_Z_slider_value = self.rotation_Z_slider_value * .5
        print self.rotation_Z_slider_value
        print self.copy_objects
        for copy_object in self.copy_objects:
            cmds.xform(copy_object[0],cp = True)
            copy_object_string_rotation_Z = copy_object[0] + '.rotateZ'
            cmds.setAttr(copy_object_string_rotation_Z,self.rotation_Z_slider_value)

    def scale_slider_activate(self):
        print 'scale slider activate'
        self.scale_slider_value = self.scale_slider.value()
        self.scale_slider_value = self.scale_slider_value * .025
        print self.scale_slider_value
        print self.copy_objects
        for copy_object in self.copy_objects:
            cmds.xform(copy_object[0],cp = True)
            copy_object_string_scale_X = copy_object[0] + '.scaleX'
            copy_object_string_scale_Y = copy_object[0] + '.scaleY'
            copy_object_string_scale_Z = copy_object[0] + '.scaleZ'
            cmds.setAttr(copy_object_string_scale_X,self.scale_slider_value)
            cmds.setAttr(copy_object_string_scale_Y,self.scale_slider_value)
            cmds.setAttr(copy_object_string_scale_Z,self.scale_slider_value)

    def object_propagator_UI(self):
        print 'object_propagator_UI'
        window_name = "object_propagator_UI"
        if cmds.window(window_name,exists = True):
            cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(window_name)
        window.setWindowTitle(window_name)
        main_widget = QtWidgets.QWidget()
        window.setCentralWidget(main_widget)
        #window.setFixedSize(1015,300)
        window.setFixedWidth(500)
        window.setMinimumHeight(100)
        main_vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        self.reference_objects_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.reference_objects_layout)
        self.copy_object_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.copy_object_layout)
        self.run_duplicate_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.run_duplicate_layout)
        self.translations_layout = QtWidgets.QVBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.translations_layout)
        self.translate_X_slider_layout = QtWidgets.QHBoxLayout(main_widget)
        self.translate_Y_slider_layout = QtWidgets.QHBoxLayout(main_widget)
        self.translate_Z_slider_layout = QtWidgets.QHBoxLayout(main_widget)
        self.rotation_X_slider_layout = QtWidgets.QHBoxLayout(main_widget)
        self.rotation_Y_slider_layout = QtWidgets.QHBoxLayout(main_widget)
        self.rotation_Z_slider_layout = QtWidgets.QHBoxLayout(main_widget)
        self.scale_slider_layout = QtWidgets.QHBoxLayout(main_widget)
        self.reference_objects_line_edit = QtWidgets.QLineEdit()
        self.reference_objects_button = QtWidgets.QPushButton()
        self.reference_objects_button.setText("reference_objects")
        self.reference_objects_button.pressed.connect(partial(self.reference_objects_detect))

        self.copy_object_line_edit = QtWidgets.QLineEdit()
        self.copy_object_button = QtWidgets.QPushButton()
        self.copy_object_button.setText("copy_object")
        self.copy_object_button.pressed.connect(partial(self.copy_object_detect))

        self.reference_objects_layout.addWidget(self.reference_objects_line_edit)
        self.reference_objects_layout.addWidget(self.reference_objects_button)
        self.copy_object_layout.addWidget(self.copy_object_line_edit)
        self.copy_object_layout.addWidget(self.copy_object_button)

        self.run_duplicate_button = QtWidgets.QPushButton()
        self.run_duplicate_button.setText("run_duplicate")
        self.run_duplicate_button.pressed.connect(partial(self.run_duplicate))
        self.run_duplicate_layout.addWidget(self.run_duplicate_button)

        self.translate_X_label = QtWidgets.QLabel("translate X")
        self.translations_layout.addWidget(self.translate_X_label)
        self.translations_layout.addLayout(self.translate_X_slider_layout)
        self.translate_X_label_1 = QtWidgets.QLabel("-3")
        self.translate_X_slider_layout.addWidget(self.translate_X_label_1)
        self.translate_X_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.translate_X_slider.setValue(0)
        self.translate_X_slider.setMinimum(-30)
        self.translate_X_slider.setMaximum(30)
        self.translate_X_slider.setSingleStep(1)
        self.translate_X_slider.valueChanged.connect(self.translate_X_slider_activate)
        self.translate_X_slider_layout.addWidget(self.translate_X_slider)
        self.translate_X_label_10 = QtWidgets.QLabel("3")
        self.translate_X_slider_layout.addWidget(self.translate_X_label_10)

        self.translate_Y_label = QtWidgets.QLabel("translate Y")
        self.translations_layout.addWidget(self.translate_Y_label)
        self.translations_layout.addLayout(self.translate_Y_slider_layout)
        self.translate_Y_label_1 = QtWidgets.QLabel("-3")
        self.translate_Y_slider_layout.addWidget(self.translate_Y_label_1)
        self.translate_Y_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.translate_Y_slider.setValue(0)
        self.translate_Y_slider.setMinimum(-30)
        self.translate_Y_slider.setMaximum(30)
        self.translate_Y_slider.setSingleStep(1)
        self.translate_Y_slider.valueChanged.connect(self.translate_Y_slider_activate)
        self.translate_Y_slider_layout.addWidget(self.translate_Y_slider)
        self.translate_Y_label_10 = QtWidgets.QLabel("3")
        self.translate_Y_slider_layout.addWidget(self.translate_Y_label_10)

        self.translate_Z_label = QtWidgets.QLabel("translate Z")
        self.translations_layout.addWidget(self.translate_Z_label)
        self.translations_layout.addLayout(self.translate_Z_slider_layout)
        self.translate_Z_label_1 = QtWidgets.QLabel("-3")
        self.translate_Z_slider_layout.addWidget(self.translate_Z_label_1)
        self.translate_Z_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.translate_Z_slider.setValue(0)
        self.translate_Z_slider.setMinimum(-30)
        self.translate_Z_slider.setMaximum(30)
        self.translate_Z_slider.setSingleStep(1)
        self.translate_Z_slider.valueChanged.connect(self.translate_Z_slider_activate)
        self.translate_Z_slider_layout.addWidget(self.translate_Z_slider)
        self.translate_Z_label_10 = QtWidgets.QLabel("3")
        self.translate_Z_slider_layout.addWidget(self.translate_Z_label_10)

        self.rotate_X_label = QtWidgets.QLabel("rotate X")
        self.translations_layout.addWidget(self.rotate_X_label)
        self.translations_layout.addLayout(self.rotation_X_slider_layout)
        self.rotation_X_label_1 = QtWidgets.QLabel("-360")
        self.rotation_X_slider_layout.addWidget(self.rotation_X_label_1)
        self.rotation_X_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rotation_X_slider.setValue(0)
        self.rotation_X_slider.setMinimum(-720)
        self.rotation_X_slider.setMaximum(720)
        self.rotation_X_slider.setSingleStep(1)
        self.rotation_X_slider.valueChanged.connect(self.rotation_X_slider_activate)
        self.rotation_X_slider_layout.addWidget(self.rotation_X_slider)
        self.rotation_X_label_10 = QtWidgets.QLabel("360")
        self.rotation_X_slider_layout.addWidget(self.rotation_X_label_10)

        self.rotate_Y_label = QtWidgets.QLabel("rotate Y")
        self.translations_layout.addWidget(self.rotate_Y_label)
        self.translations_layout.addLayout(self.rotation_Y_slider_layout)
        self.rotation_Y_label_1 = QtWidgets.QLabel("-360")
        self.rotation_Y_slider_layout.addWidget(self.rotation_Y_label_1)
        self.rotation_Y_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rotation_Y_slider.setValue(0)
        self.rotation_Y_slider.setMinimum(-720)
        self.rotation_Y_slider.setMaximum(720)
        self.rotation_Y_slider.setSingleStep(1)
        self.rotation_Y_slider.valueChanged.connect(self.rotation_Y_slider_activate)
        self.rotation_Y_slider_layout.addWidget(self.rotation_Y_slider)
        self.rotation_Y_label_10 = QtWidgets.QLabel("360")
        self.rotation_Y_slider_layout.addWidget(self.rotation_Y_label_10)

        self.rotate_Z_label = QtWidgets.QLabel("rotate Z")
        self.translations_layout.addWidget(self.rotate_Z_label)
        self.translations_layout.addLayout(self.rotation_Z_slider_layout)
        self.rotation_Z_label_1 = QtWidgets.QLabel("-360")
        self.rotation_Z_slider_layout.addWidget(self.rotation_Z_label_1)
        self.rotation_Z_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.rotation_Z_slider.setValue(0)
        self.rotation_Z_slider.setMinimum(-720)
        self.rotation_Z_slider.setMaximum(720)
        self.rotation_Z_slider.setSingleStep(1)
        self.rotation_Z_slider.valueChanged.connect(self.rotation_Z_slider_activate)
        self.rotation_Z_slider_layout.addWidget(self.rotation_Z_slider)
        self.rotation_Z_label_10 = QtWidgets.QLabel("360")
        self.rotation_Z_slider_layout.addWidget(self.rotation_Z_label_10)

        self.scale_label = QtWidgets.QLabel("scale")
        self.translations_layout.addWidget(self.scale_label)
        self.translations_layout.addLayout(self.scale_slider_layout)
        self.scale_label_1 = QtWidgets.QLabel(".1")
        self.scale_slider_layout.addWidget(self.scale_label_1)
        self.scale_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.scale_slider.setValue(40)
        self.scale_slider.setMinimum(1)
        self.scale_slider.setMaximum(80)
        self.scale_slider.setSingleStep(1)
        self.scale_slider.valueChanged.connect(self.scale_slider_activate)
        self.scale_slider_layout.addWidget(self.scale_slider)
        self.scale_label_10 = QtWidgets.QLabel("2")
        self.scale_slider.setTickInterval(1)
        self.scale_slider_layout.addWidget(self.scale_label_10)

        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    object_propagator = OBJECT_PROPAGATOR()
    object_propagator.object_propagator_UI()
