import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

class ASSET_TRACKER(object):
    def __init__(self):
        ph = 'chris'

    def nodes_in_scene(self):
        objects = cmds.ls(type = 'transform')
        self.trackable_objects = []
        for object in objects:
          entity_id_attr_exists = cmds.attributeQuery('entity_id',node = object,exists = True)
          if entity_id_attr_exists == 1:
              self.trackable_objects.append(object)
        self.gather_attributes()

    def gather_attributes(self):
        self.asset_attr_dic = {}
        attrs = ['publish_type','publish_id','entity_id','version','publish_path','entity_name','task_type','task_id','publish_file']
        for object in self.trackable_objects:
            for attr in attrs:
                value = cmds.getAttr(object + '.' + attr)
                self.asset_attr_dic[object + '&&' + attr] = attr + '&&' + str(value)
        print 'self.asset_attr_dic = ',self.asset_attr_dic

#---------- window ----------

    def asset_tracker_UI(self):
        window_name = "asset_tracker"
        if cmds.window(window_name,exists = True):
            cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(window_name)
        window.setWindowTitle(window_name)
        main_widget = QtWidgets.QWidget()
        window.setCentralWidget(main_widget)
        window.setFixedSize(1015,300)
        self.nodes_in_scene()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    asset_tracker_instance = ASSET_TRACKER()
    asset_tracker_instance.asset_tracker_UI()

#main()
