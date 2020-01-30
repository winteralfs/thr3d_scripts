import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

class OBJECT_PROPAGATOR(object):
    def __init__(self):
        chris = 'temp'

    def reference_objects_detect(self):
        reference_objects_string = ''
        reference_objects = cmds.ls(sl = True)
        print 'reference_objects = ',reference_objects
        for reference_object in reference_objects:
            reference_objects_string = reference_objects_string + ' ' + reference_object
        self.reference_objects_line_edit.setText(reference_objects_string)

    def copy_object_detect(self):
        copy_object = cmds.ls(sl = True)
        print 'copy_object = ',copy_object
        for list_item in copy_object:
            self.copy_object_line_edit.setText(list_item)

    def run_duplicate(self):
        print 'run_transform_button'

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

        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    object_propagator = OBJECT_PROPAGATOR()
    object_propagator.object_propagator_UI()
