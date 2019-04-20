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
        self.number_of_trackable_object = len(self.trackable_objects)
        self.gather_attributes()

    def gather_attributes(self):
        self.asset_attr_dic = {}
        attrs = ['publish_type','publish_id','entity_id','version','publish_path','entity_name','task_type','task_id','publish_file']
        for object in self.trackable_objects:
            for attr in attrs:
                value = cmds.getAttr(object + '.' + attr)
                self.asset_attr_dic[object + '&&' + attr] = str(value)
                if attr == 'publish_path':
                    publish_path_value_split = value.split('/')
                    publish_path_value_split_length = len(publish_path_value_split)
                    publish_path_value_split_length = publish_path_value_split_length - 1
                    publish_path_value_dir = ''
                    i = 1
                    while i < publish_path_value_split_length:
                        publish_path_value_dir = publish_path_value_dir + '/' + publish_path_value_split[i]
                        i = i + 1
                    publish_path_value_dir = publish_path_value_dir + '/'
                    files = cmds.getFileList(folder = publish_path_value_dir,filespec = '*.mb')
                    highest_version = 0
                    for file in files:
                        version_number = file[-4]
                        if version_number > highest_version:
                            highest_version = version_number
                            self.asset_attr_dic[object + '&&' + 'highest_version'] = highest_version
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
                        version_value = self.asset_attr_dic[asset]
                        self.current_version_listWidget.addItem(version_value)
                    if attr == 'highest_version':
                        highest_version_value = self.asset_attr_dic[asset]
                        self.highest_version_listWidget.addItem(highest_version_value)
                    if attr == 'entity_name':
                        entity_name_value = self.asset_attr_dic[asset]
                        self.entity_name_listWidget.addItem(entity_name_value)
                    if attr == 'publish_path':
                        publish_path_value = self.asset_attr_dic[asset]
                        self.publish_path_listWidget.addItem(publish_path_value)
        self.evaluate_versions()

    def evaluate_versions(self):
        i = 0
        while i < self.number_of_trackable_object:
            current_version_item = self.current_version_listWidget.item(i)
            object_item = self.node_name_listWidget.item(i)
            current_version_item_text = current_version_item.text()
            current_version_item_int = int(current_version_item_text)
            highest_version_item = self.highest_version_listWidget.item(i)
            highest_version_item_text = highest_version_item.text()
            highest_version_item_int = int(highest_version_item_text)
            if highest_version_item_int > current_version_item_int:
                object_item.setTextColor('red')
                current_version_item.setTextColor('red')
            else:
                object_item.setTextColor('light blue')
                current_version_item.setTextColor('light blue')
            i = i + 1
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
        window.setFixedSize(1300,300)
        main_vertical_layout =  QtWidgets.QVBoxLayout(main_widget)
        label_horizontal_layout = QtWidgets.QHBoxLayout(main_widget)
        #label_horizontal_layout.setAlignment('Alignleft')
        main_horizontal_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(label_horizontal_layout)
        main_vertical_layout.addLayout(main_horizontal_layout)
        labels = QtWidgets.QLabel('  Name                                                                                                     C-ver  L-ver     Entity Name                                Path')
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
        self.highest_version_listWidget = QtWidgets.QListWidget()
        self.highest_version_listWidget.setSpacing(spacing)
        self.highest_version_listWidget.setMaximumWidth(30)
        main_horizontal_layout.addWidget(self.highest_version_listWidget)
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
