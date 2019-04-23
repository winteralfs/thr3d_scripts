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

print 'tuesday'

class ASSET_TRACKER(object):
    def __init__(self):
        ph = 'chris'

    def deactivate_listWidget(self,listWidget):
        listWidget_length = listWidget.count()
        it = 0
        while it < listWidget_length:
            item = listWidget.item(it)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            it = it + 1

    def nodes_in_scene(self):
        #print 'nodes in scene'
        self.node_name_listWidget.clear()
        self.current_version_listWidget.clear()
        self.highest_version_listWidget.clear()
        self.entity_name_listWidget.clear()
        self.publish_path_listWidget.clear()
        transforms = cmds.ls(type = 'transform')
        file_nodes = cmds.ls(type = 'file')
        objects = transforms + file_nodes
        self.trackable_objects = []
        for object in objects:
          entity_id_attr_exists = cmds.attributeQuery('entity_id',node = object,exists = True)
          if entity_id_attr_exists == 1:
              self.trackable_objects.append(object)
        self.number_of_trackable_object = len(self.trackable_objects)
        self.gather_attributes()

    def gather_attributes(self):
        #print 'gather_attributes'
        self.asset_attr_dic = {}
        attrs = ['publish_type','publish_id','entity_id','version','publish_path','entity_name','task_type','task_id','publish_file']
        #print 'trackable_objects = ',self.trackable_objects
        for object in self.trackable_objects:
            node_type = cmds.nodeType(object)
            for attr in attrs:
                #print 'attr = ',attr
                value = cmds.getAttr(object + '.' + attr)
                self.asset_attr_dic[object + '&&' + attr] = str(value)
                if attr == 'publish_path' and node_type != 'file':
                    #print 'publish_path = ',value
                    publish_path_value_split = value.split('\\')
                    #print 'publish_path_value_split = ',publish_path_value_split
                    publish_path_value_split_length = len(publish_path_value_split)
                    #print 'publish_path_value_split_length = ',publish_path_value_split_length
                    publish_path_value_split_length = publish_path_value_split_length - 1
                    #print 'publish_path_value_split_length = ',publish_path_value_split_length
                    publish_path_value_dir = ''
                    i = 1
                    while i < publish_path_value_split_length:
                        publish_path_value_dir = publish_path_value_dir + '\\' + publish_path_value_split[i]
                        #print '1 publish_path_value_dir = ',publish_path_value_dir
                        i = i + 1
                    publish_path_value_dir = publish_path_value_dir + '\\'
                    #print '2 publish_path_value_dir = ',publish_path_value_dir
                    files = cmds.getFileList(folder = publish_path_value_dir,filespec = '*.mb')
                    #print 'files = ',files
                    highest_version = 0
                    for file in files:
                        version_number = file[-4]
                        if version_number > highest_version:
                            highest_version = version_number
                            self.asset_attr_dic[object + '&&' + 'highest_version'] = highest_version
                if attr == 'publish_path' and node_type == 'file':
                    publish_path_value_split = value.split('\\')
                    publish_path_value_split_length = len(publish_path_value_split)
                    publish_path_value_split_length = publish_path_value_split_length - 2
                    publish_path_value_dir = ''
                    i = 1
                    while i < publish_path_value_split_length:
                        publish_path_value_dir = publish_path_value_dir + '\\' + publish_path_value_split[i]
                        i = i + 1
                    publish_path_value_dir = publish_path_value_dir + '\\'
                    raw_files = cmds.getFileList(folder = publish_path_value_dir)
                    files = []
                    for raw_file in raw_files:
                        if raw_file.startswith('v'):
                            files.append(raw_file)
                    highest_version = 0
                    for file in files:
                        version_number = file[-1]
                        if version_number > highest_version:
                            highest_version = version_number
                            self.asset_attr_dic[object + '&&' + 'highest_version'] = highest_version
        #print 'asset_attr_dic = ',self.asset_attr_dic
        self.populate_window()

    def populate_window(self):
        #print 'populate_window'
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
        #print 'evaluate_versions'
        i = 0
        #print 'number_of_trackable_object = ',self.number_of_trackable_object
        while i < self.number_of_trackable_object:
            current_version_item = self.current_version_listWidget.item(i)
            #print 'current_version_item = ',current_version_item
            object_item = self.node_name_listWidget.item(i)
            current_version_item_text = current_version_item.text()
            #print 'current_version_item_text = ',current_version_item_text
            current_version_item_int = int(current_version_item_text)
            highest_version_item = self.highest_version_listWidget.item(i)
            #print 'highest_version_item = ',highest_version_item
            highest_version_item_text = highest_version_item.text()
            highest_version_item_int = int(highest_version_item_text)
            highest_version_item.setTextColor('light blue')
            if highest_version_item_int > current_version_item_int:
                object_item.setTextColor('red')
                current_version_item.setTextColor('red')
            else:
                object_item.setTextColor('light blue')
                current_version_item.setTextColor('light blue')
            i = i + 1
        self.deactivate_listWidget(self.node_name_listWidget)
        self.deactivate_listWidget(self.current_version_listWidget)
        self.deactivate_listWidget(self.highest_version_listWidget)

    def entity_name_item_press(self,item):
        item_text = item.text()
        for asset_attr in self.asset_attr_dic:
            value = self.asset_attr_dic[asset_attr]
            if value == item_text:
                asset_attr_split = asset_attr.split('&&')
                asset_name = asset_attr_split[0]
                entity_id = self.asset_attr_dic[asset_name + '&&' + 'entity_id']
        shotgun_path = 'https://thr3dcgi.shotgunstudio.com/detail/Asset/'
        shotgun_path = shotgun_path + entity_id
        webbrowser.open(shotgun_path)
        self.entity_name_listWidget.clearSelection()
        self.entity_name_listWidget.setCurrentIndex(QtCore.QModelIndex())

    def publish_path_item_press(self,item):
        item_text = item.text()
        item_text_split = item_text.split('\\')
        item_text_split_length = len(item_text_split)
        i = 1
        item_path = ''
        while i < (item_text_split_length - 1):
            item_path = item_path + '\\' + item_text_split[i]
            i = i + 1
        #item_path = item_path + '\\'
        #print 'item_path = ',item_path
        subprocess_string = 'explorer ' + item_path
        subprocess.Popen(subprocess_string)
        #subprocess.call(["open", "-R", item_path])
        self.publish_path_listWidget.clearSelection()
        self.publish_path_listWidget.setCurrentIndex(QtCore.QModelIndex())


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
        window.setFixedSize(1450,300)
        self.main_grid_layout = QtWidgets.QGridLayout(main_widget)
        titles = ['Name','C-ver','L-ver','Entity Name','Path']
        i = 0
        for title in titles:
            label = QtWidgets.QLabel(title)
            self.main_grid_layout.addWidget(label,0,i)
            i = i + 1
        spacing = 3
        self.node_name_listWidget = QtWidgets.QListWidget()
        self.node_name_listWidget.setSpacing(spacing)
        self.node_name_listWidget.setMaximumWidth(325)
        self.node_name_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.node_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.node_name_listWidget,1,0)
        self.current_version_listWidget = QtWidgets.QListWidget()
        self.current_version_listWidget.setSpacing(spacing)
        self.current_version_listWidget.setMaximumWidth(30)
        self.main_grid_layout.addWidget(self.current_version_listWidget)
        self.highest_version_listWidget = QtWidgets.QListWidget()
        self.highest_version_listWidget.setSpacing(spacing)
        self.highest_version_listWidget.setMaximumWidth(30)
        self.main_grid_layout.addWidget(self.highest_version_listWidget)
        self.entity_name_listWidget = QtWidgets.QListWidget()
        self.entity_name_listWidget.setSpacing(spacing)
        self.entity_name_listWidget.setMaximumWidth(150)
        self.entity_name_listWidget.itemClicked.connect(partial(self.entity_name_item_press))
        self.entity_name_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.entity_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.entity_name_listWidget)
        self.publish_path_listWidget = QtWidgets.QListWidget()
        self.publish_path_listWidget.setSpacing(spacing)
        self.publish_path_listWidget.itemClicked.connect(partial(self.publish_path_item_press))
        self.publish_path_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.publish_path_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.publish_path_listWidget)
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["renderLayerManagerChange", self.nodes_in_scene])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["renderLayerChange", self.nodes_in_scene])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["SelectionChanged", self.nodes_in_scene])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["SceneOpened", self.nodes_in_scene])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["NameChanged", self.nodes_in_scene])
        self.nodes_in_scene()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    asset_tracker_instance = ASSET_TRACKER()
    asset_tracker_instance.asset_tracker_UI()

#main()
