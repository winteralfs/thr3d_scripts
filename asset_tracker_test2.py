"""
lighting_shelf: asset_tracker
********************************************
"""

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

print 'asset_tracker'

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
        self.latest_version_path_feedback_listWidget.clear()
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
        self.highest_version_path_dic = {}
        self.publish_path_year_dic = {}
        self.nineteen_exists_dic = {}
        int_check = ['0','01','001','1','01','001','2','02','002','03','003','3','04','004','4','05','005','5','06','006','6','07','007','7','08','008','8','09','009','9','010','0010','10','011','0011','11','012','0012','12','013','0013','13','014','0014','14','015','0015','15','016','0016','16','017','0017','17','018','0018','18','019','0019','19','020','0020','20','021','0021','21','022','0022','22','023','0023','23','024','0024','24','025','0025','25']
        attrs = ['publish_type','publish_id','entity_id','version','publish_path','entity_name','task_type','task_id','publish_file']
        for object in self.trackable_objects:
            #print 'object = ',object
            higher_version_found = 0
            node_type = cmds.nodeType(object)
            for attr in attrs:
                attr_exists = cmds.attributeQuery(attr,node = object,exists = True)
                if attr_exists == 1:
                    value = cmds.getAttr(object + '.' + attr)
                    self.asset_attr_dic[object + '&&' + attr] = str(value)
                    if attr == 'publish_path':
                        self.files_in_19_folder = 0
                        value_split = value.split('\\')
                        self.publish_path_year_dic[object] = value_split[5]
                        publish_path_value_split = value.split('\\')
                        publish_path_value_split_length = len(publish_path_value_split)
                        year_versions_path = ''
                        i = 0
                        if node_type != 'file':
                            publish_path_value_split_length_minus = 6
                        if node_type == 'file':
                            publish_path_value_split_length_minus = 9
                        while i < (publish_path_value_split_length - publish_path_value_split_length_minus):
                            if i == 0:
                                year_versions_path
                            if i > 0:
                                year_versions_path = year_versions_path +'\\' + publish_path_value_split[i]
                            i = i + 1
                        eighteen_year_versions = []
                        nineteen_year_versions = []
                        eighteen_version_number_full_string = ''
                        nineteen_version_number_full_string = ''
                        year_versions = cmds.getFileList(folder = year_versions_path) or []
                        highest_version = 0
                        #print 'year_versions = ',year_versions
                        for year_version in year_versions:
                            #print 'year_version = ',year_version
                            publish_path_value_split_length = len(publish_path_value_split)
                            if year_version != '.DS_Store':
                                if '19' in year_version:
                                    #print 'adding 19 to nineteen_exists_dic'
                                    self.nineteen_exists_dic[object] = 1
                                if node_type == 'file':
                                    publish_path_value_split_length = publish_path_value_split_length - 2
                                if node_type != 'file':
                                    publish_path_value_split_length = publish_path_value_split_length - 1
                                publish_path_value_dir = ''
                                i = 1
                                while i < publish_path_value_split_length:
                                    if i == 5:
                                            publish_path_value_dir = publish_path_value_dir + '\\' + year_version
                                    else:
                                        publish_path_value_dir = publish_path_value_dir + '\\' + publish_path_value_split[i]
                                    i = i + 1
                                publish_path_value_dir = publish_path_value_dir + '\\'
                                files = []
                                files = cmds.getFileList(folder = publish_path_value_dir) or []
                                number_of_files= len(files)
                                if number_of_files == 0:
                                    if higher_version_found != 1:
                                        files = ['X']
                                        self.asset_attr_dic[object + '&&' + 'highest_version'] = 'X'
                                publish_path_value_dir_split = publish_path_value_dir.split('\\')
                                temp_year_used = publish_path_value_dir_split[5]
                                #print 'temp_year_used = ',temp_year_used
                                if number_of_files != 0:
                                    if node_type != 'file':
                                        for file in files:
                                            if file != '.DS_Store':
                                                file_full = file
                                                file_split = file.split('.')
                                                file = file_split[0]
                                                file_split_ = file.split('_')
                                                number_of_file_splits_ = len(file_split_)
                                                number_of_file_splits_ = number_of_file_splits_ - 1
                                                file = file_split_[number_of_file_splits_]
                                                version_number = file
                                                #print 'version_number = ',version_number
                                                #print 'highest_version = ',highest_version
                                                if version_number in int_check:
                                                    if int(version_number) > int(highest_version):
                                                        highest_version = str(version_number)
                                                        #print 'setting higher version_number = ',version_number
                                                        #print 'setting higher highest_version = ',highest_version
                                                        zero_check = highest_version[0]
                                                        if zero_check == '0':
                                                            highest_version = highest_version[1:]
                                                            zero_check_2 = highest_version[0]
                                                            if zero_check_2 == '0':
                                                                highest_version = highest_version[1:]
                                                        self.asset_attr_dic[object + '&&' + 'highest_version'] = highest_version
                                                        highest_path_string = (object + ':  ' + publish_path_value_dir + file_full)
                                                        self.highest_version_path_dic[object] = highest_path_string
                                                        higher_version_found = 1
                                                        self.highest_value_year = temp_year_used
                                    #print 'self.highest_value_year = ',self.highest_value_year
                                    if node_type == 'file':
                                        folder_files = []
                                        for file in files:
                                            if file.startswith('v'):
                                                folder_files.append(file)
                                        for folder_file in folder_files:
                                            if file != '.DS_Store':
                                                version_number = folder_file[-1]
                                                if int(version_number) > int(highest_version):
                                                    highest_version = version_number
                                                    self.asset_attr_dic[object + '&&' + 'highest_version'] = highest_version
                                                    highest_path_string = (object + ':  ' + publish_path_value_dir + file)
                                                    self.highest_version_path_dic[object] = highest_path_string
                                                    higher_version_found = 1
                                                    self.highest_value_year = temp_year_used
        #print 'self.nineteen_exists_dic = ',self.nineteen_exists_dic
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

    def latest_version_path_feedback_listWidget_populate(self):
        number_of_objects = self.node_name_listWidget.count()
        i = 0
        while i < number_of_objects:
            item = self.node_name_listWidget.item(i)
            item_text = item.text()
            for highest_version_path_item in self.highest_version_path_dic:
                if highest_version_path_item == item_text:
                    highest_version_path_item_path = self.highest_version_path_dic[highest_version_path_item]
                    self.latest_version_path_feedback_listWidget.addItem(highest_version_path_item_path)
            i = i + 1
        self.deactivate_listWidget(self.latest_version_path_feedback_listWidget)

    def evaluate_versions(self):
        #print 'evaluate_versions'
        i = 0
        while i < self.number_of_trackable_object:
            object_item = self.node_name_listWidget.item(i)
            object_item_text = object_item.text()
            current_version_item = self.current_version_listWidget.item(i)
            current_version_item_text = current_version_item.text()
            current_version_item_int = int(current_version_item_text)
            highest_version_item = self.highest_version_listWidget.item(i)
            highest_version_item_text = highest_version_item.text()
            publish_path_item = self.publish_path_listWidget.item(i)
            if highest_version_item_text != 'X':
                highest_version_item_int = int(highest_version_item_text)
                highest_version_item.setTextColor('light blue')
                if highest_version_item_int > current_version_item_int:
                    object_item.setTextColor('red')
                    current_version_item.setTextColor('red')
                else:
                    object_item.setTextColor('light blue')
                    current_version_item.setTextColor('light blue')
                #print ' '
                #print 'object_item_text = ',object_item_text
                #print 'self.publish_path_year_dic = ',self.publish_path_year_dic
                #print 'self.highest_value_year: = ',self.highest_value_year
                for publish_year in self.publish_path_year_dic:
                    if publish_year == object_item_text:
                        #print 'publish_year matches object_item_text'
                        publish_year_value = self.publish_path_year_dic[object_item_text]
                        if '18' in publish_year_value and '19' in self.highest_value_year:
                            print '18 detected in publish_year_value and 19 detected in self.highest_value_year'
                            highest_version_item.setTextColor('yellow')
                            publish_path_item.setTextColor('yellow')
                #print 'self.nineteen_exists_dic = ',self.nineteen_exists_dic
                #print 'self.publish_path_year_dic = ',self.publish_path_year_dic
                #print ' '
                for nineteen_exists in self.nineteen_exists_dic:
                    if nineteen_exists == object_item_text:
                        #print 'nineteen_exists matches object_item_text'
                        #print 'self.publish_path_year_dic = ',self.publish_path_year_dic
                        publish_year_value = self.publish_path_year_dic[object_item_text]
                        if '18' in publish_year_value:
                            #print '18 in self.publish_path_year_dic'
                            highest_version_item.setTextColor('yellow')
                            publish_path_item.setTextColor('yellow')
            if highest_version_item_text == 'X':
                object_item.setTextColor('orange')
                current_version_item.setTextColor('orange')
                highest_version_item.setTextColor('orange')
                publish_path_item.setTextColor('orange')
            i = i + 1
        self.latest_version_path_feedback_listWidget_populate()
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
        subprocess_string = 'explorer ' + item_path
        subprocess.Popen(subprocess_string)
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
        window.setFixedWidth(1450)
        self.main_grid_layout = QtWidgets.QGridLayout(main_widget)
        titles = ['Name (red indicates a newer version of the asset exists)','C-ver','L-ver','Entity Name','Published Path (orange indicates an invalid path, yellow indicates a version of this assets exists in a 19 directory)']
        i = 0
        for title in titles:
            label = QtWidgets.QLabel(title)
            self.main_grid_layout.addWidget(label,0,i)
            i = i + 1
        spacing = 3
        self.node_name_listWidget = QtWidgets.QListWidget()
        self.node_name_listWidget.setSpacing(spacing)
        self.node_name_listWidget.setMaximumWidth(325)
        self.node_name_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.node_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.node_name_listWidget,1,0)
        self.current_version_listWidget = QtWidgets.QListWidget()
        self.current_version_listWidget.setSpacing(spacing)
        self.current_version_listWidget.setMaximumWidth(50)
        self.main_grid_layout.addWidget(self.current_version_listWidget)
        self.highest_version_listWidget = QtWidgets.QListWidget()
        self.highest_version_listWidget.setSpacing(spacing)
        self.highest_version_listWidget.setMaximumWidth(50)
        self.main_grid_layout.addWidget(self.highest_version_listWidget)
        self.entity_name_listWidget = QtWidgets.QListWidget()
        self.entity_name_listWidget.setSpacing(spacing)
        self.entity_name_listWidget.setMaximumWidth(150)
        self.entity_name_listWidget.itemClicked.connect(partial(self.entity_name_item_press))
        self.entity_name_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.entity_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.entity_name_listWidget)
        self.publish_path_listWidget = QtWidgets.QListWidget()
        self.publish_path_listWidget.setSpacing(spacing)
        self.publish_path_listWidget.itemClicked.connect(partial(self.publish_path_item_press))
        self.publish_path_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.publish_path_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.publish_path_listWidget)
        label_full_paths_listWidget = QtWidgets.QLabel('Full paths to the latest versions of the assets')
        self.main_grid_layout.addWidget(label_full_paths_listWidget,2,0,1,5)
        self.latest_version_path_feedback_listWidget = QtWidgets.QListWidget()
        self.latest_version_path_feedback_listWidget.setSpacing(spacing)
        self.latest_version_path_feedback_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.latest_version_path_feedback_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.latest_version_path_feedback_listWidget,3,0,1,5)
        self.node_name_listWidget.verticalScrollBar().valueChanged.connect(self.current_version_listWidget.verticalScrollBar().setValue)
        self.node_name_listWidget.verticalScrollBar().valueChanged.connect(self.highest_version_listWidget.verticalScrollBar().setValue)
        self.node_name_listWidget.verticalScrollBar().valueChanged.connect(self.entity_name_listWidget.verticalScrollBar().setValue)
        self.node_name_listWidget.verticalScrollBar().valueChanged.connect(self.publish_path_listWidget.verticalScrollBar().setValue)
        self.node_name_listWidget.verticalScrollBar().valueChanged.connect(self.latest_version_path_feedback_listWidget.verticalScrollBar().setValue)
        self.current_version_listWidget.verticalScrollBar().valueChanged.connect(self.node_name_listWidget.verticalScrollBar().setValue)
        self.current_version_listWidget.verticalScrollBar().valueChanged.connect(self.highest_version_listWidget.verticalScrollBar().setValue)
        self.current_version_listWidget.verticalScrollBar().valueChanged.connect(self.entity_name_listWidget.verticalScrollBar().setValue)
        self.current_version_listWidget.verticalScrollBar().valueChanged.connect(self.publish_path_listWidget.verticalScrollBar().setValue)
        self.current_version_listWidget.verticalScrollBar().valueChanged.connect(self.latest_version_path_feedback_listWidget.verticalScrollBar().setValue)
        self.highest_version_listWidget.verticalScrollBar().valueChanged.connect(self.node_name_listWidget.verticalScrollBar().setValue)
        self.highest_version_listWidget.verticalScrollBar().valueChanged.connect(self.current_version_listWidget.verticalScrollBar().setValue)
        self.highest_version_listWidget.verticalScrollBar().valueChanged.connect(self.entity_name_listWidget.verticalScrollBar().setValue)
        self.highest_version_listWidget.verticalScrollBar().valueChanged.connect(self.publish_path_listWidget.verticalScrollBar().setValue)
        self.highest_version_listWidget.verticalScrollBar().valueChanged.connect(self.latest_version_path_feedback_listWidget.verticalScrollBar().setValue)
        self.entity_name_listWidget.verticalScrollBar().valueChanged.connect(self.node_name_listWidget.verticalScrollBar().setValue)
        self.entity_name_listWidget.verticalScrollBar().valueChanged.connect(self.current_version_listWidget.verticalScrollBar().setValue)
        self.entity_name_listWidget.verticalScrollBar().valueChanged.connect(self.highest_version_listWidget.verticalScrollBar().setValue)
        self.entity_name_listWidget.verticalScrollBar().valueChanged.connect(self.publish_path_listWidget.verticalScrollBar().setValue)
        self.entity_name_listWidget.verticalScrollBar().valueChanged.connect(self.latest_version_path_feedback_listWidget.verticalScrollBar().setValue)
        self.publish_path_listWidget.verticalScrollBar().valueChanged.connect(self.node_name_listWidget.verticalScrollBar().setValue)
        self.publish_path_listWidget.verticalScrollBar().valueChanged.connect(self.current_version_listWidget.verticalScrollBar().setValue)
        self.publish_path_listWidget.verticalScrollBar().valueChanged.connect(self.highest_version_listWidget.verticalScrollBar().setValue)
        self.publish_path_listWidget.verticalScrollBar().valueChanged.connect(self.entity_name_listWidget.verticalScrollBar().setValue)
        self.publish_path_listWidget.verticalScrollBar().valueChanged.connect(self.latest_version_path_feedback_listWidget.verticalScrollBar().setValue)
        self.latest_version_path_feedback_listWidget.verticalScrollBar().valueChanged.connect(self.node_name_listWidget.verticalScrollBar().setValue)
        self.latest_version_path_feedback_listWidget.verticalScrollBar().valueChanged.connect(self.current_version_listWidget.verticalScrollBar().setValue)
        self.latest_version_path_feedback_listWidget.verticalScrollBar().valueChanged.connect(self.highest_version_listWidget.verticalScrollBar().setValue)
        self.latest_version_path_feedback_listWidget.verticalScrollBar().valueChanged.connect(self.entity_name_listWidget.verticalScrollBar().setValue)
        self.latest_version_path_feedback_listWidget.verticalScrollBar().valueChanged.connect(self.publish_path_listWidget.verticalScrollBar().setValue)
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
