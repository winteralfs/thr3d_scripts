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
                self.asset_attr_dic[object + '&&' + attr] = str(value)
        print 'self.asset_attr_dic = ',self.asset_attr_dic
        self.populate_window()

    def populate_window(self):
        for node in self.trackable_objects:
            self.node_name_listWidget.addItem(node)
            for asset in self.asset_attr_dic:
                asset_name_split = asset.split('&&')
                asset_name = asset_name_split[0]
                attr = asset_name_split[1]
                if asset_name == node:
                    if attr == 'version':
                        value_version = self.asset_attr_dic[asset]
                    if attr == 'entity_name':
                        entity_name_value = self.asset_attr_dic[asset]
                    if attr == 'publish_path':
                        publish_path_value = self.asset_attr_dic[asset]
            self.current_version_listWidget.addItem(value_version)
            self.entity_name_listWidget.addItem(entity_name_value)
            self.publish_path_listWidget.addItem(publish_path_value)
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
        window.setFixedSize(1200,300)
        main_vertical_layout =  QtWidgets.QVBoxLayout(main_widget)
        label_horizontal_layout = QtWidgets.QHBoxLayout(main_widget)
        #label_horizontal_layout.setAlignment('Alignleft')
        main_horizontal_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(label_horizontal_layout)
        main_vertical_layout.addLayout(main_horizontal_layout)
        labels = QtWidgets.QLabel('                                             name                                                          ver   latest ver             entity name                                                                                                                 path')
        #labels.setAlignment(QtCore.Qt.AlignLeft)
        label_horizontal_layout.addWidget(labels)
        spacing = 3
        self.node_name_listWidget = QtWidgets.QListWidget()
        self.node_name_listWidget.setSpacing(spacing)
        self.node_name_listWidget.setMaximumWidth(325)
        self.node_name_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.node_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        main_horizontal_layout.addWidget(self.node_name_listWidget)
        self.current_version_listWidget = QtWidgets.QListWidget()
        self.current_version_listWidget.setSpacing(spacing)
        self.current_version_listWidget.setMaximumWidth(30)
        main_horizontal_layout.addWidget(self.current_version_listWidget)
        self.newest_version_listWidget = QtWidgets.QListWidget()
        self.newest_version_listWidget.setSpacing(spacing)
        self.newest_version_listWidget.setMaximumWidth(30)
        main_horizontal_layout.addWidget(self.newest_version_listWidget)
        self.entity_name_listWidget = QtWidgets.QListWidget()
        self.entity_name_listWidget.setSpacing(spacing)
        self.entity_name_listWidget.setMaximumWidth(150)
        self.entity_name_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.entity_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        main_horizontal_layout.addWidget(self.entity_name_listWidget)
        self.publish_path_listWidget = QtWidgets.QListWidget()
        self.publish_path_listWidget.setSpacing(spacing)
        self.publish_path_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.publish_path_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        main_horizontal_layout.addWidget(self.publish_path_listWidget)
        self.nodes_in_scene()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    asset_tracker_instance = ASSET_TRACKER()
    asset_tracker_instance.asset_tracker_UI()

#main()
