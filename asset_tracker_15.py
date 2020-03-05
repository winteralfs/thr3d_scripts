"""
.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI.JPG
   :align: center
   :scale: 50%

Asset tracker is used to track a scene's assets current and latest version numbers, their entity names, and their publish paths. 'C-ver' for
the current version, 'L-ver' for the latest version:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_lighting_shelf.JPG
   :align: center
   :scale: 50%

Light blue indicates the version of the asset in the scene matches the latest version found on the network. It is up to date.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_teal.jpg
   :align: center
   :scale: 50%

Red indicates the version of the asset in the scene is lower than the version found on the network. It is not up to date, and a newer
version is available.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_red.jpg
   :align: center
   :scale: 50%

Yellow indicates a version of the asset was found to exist in a more current year on the network, as in the asset in the scene is from
2017, but a version exists in the 2019 area of the network. If the asset is also out of date, the 'C-ver' will be red, and if it is
current, it will be light blue.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_yellow.jpg
   :align: center
   :scale: 50%

Orange indicates the publish_path for the asset is not valid, the directory does not exist on the network. If this is the case, an 'X' will
replace a number in the L-ver collumn as the latest version of the asset can not be determined.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_orange.jpg
   :align: center
   :scale: 50%

Clicking the asset's name will highlight the path to the latest version of the asset: The path can be clicked to open that directory:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_highlighted.JPG
   :align: center
   :scale: 50%

Clicking the publish path of an asset will open that directory:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_network.JPG
   :align: center
   :scale: 50%

Clicking the entity name of the asset will open up the Shotgun page for that asset:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_shotgun_link.JPG
   :align: center
   :scale: 50%

If an asset shows up in the tracker that is not displayed in the outliner, toggle on the 'Hidden in Outliner'
option under the Display tab at the top of the outliner window:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_Maya_ignore_hidden_in_outliner.JPG
   :align: center
   :scale: 50%



------
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

#print 'asset_tracker'
#print 'sunday'

class ASSET_TRACKER(object):
    def __init__(self):
        shape_nodes = cmds.ls(type = 'shape')
        self.group_nodes = []
        self.valid_transform_objects = []
        bad_file_nodes = ['gi_std_lgt','reflection_sdt_lgt','refraction_sdt_lgt']
        self.file_nodes = []
        transform_nodes = cmds.ls(type = 'transform')
        #camera_nodes = cmds.ls(type = 'camera')
        #vray_light_nodes = cmds.ls(type = 'VRayLightRectShape')
        #print 'transform_nodes = ',transform_nodes
        #print 'camera_nodes = ',camera_nodes
        #print 'light_nodes = ',light_nodes
        for transform_node in transform_nodes:
            #print 'transform_node = ',transform_node
            children = cmds.listRelatives(transform_node, children = True) or []
            #print 'children = ',children
            group_node = 1
            for child in children:
                if child in shape_nodes:
                    group_node = 0
                    attrs = cmds.listAttr(transform_node)
                    for attr in attrs:
                        if attr == 'entity_id':
                            if transform_node not in self.valid_transform_objects:
                                self.valid_transform_objects.append(transform_node)
            if group_node == 1:
                self.group_nodes.append(transform_node)
        file_nodes_raw = cmds.ls(type = 'file')
        for file_node in file_nodes_raw:
            if file_node not in bad_file_nodes:
                self.file_nodes.append(file_node)
        #print 'self.valid_transform_objects = ',self.valid_transform_objects
        #print 'self.group_nodes = ',self.group_nodes
        #print 'self.file_nodes = ',self.file_nodes

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
        #print 'self.valid_transform_objects = ',self.valid_transform_objects
        #print 'self.file_nodes = ',self.file_nodes
        objects = self.valid_transform_objects + self.file_nodes
        #print 'objects = ',objects
        self.trackable_objects = []
        for object in objects:
            if object not in self.group_nodes:
                self.trackable_objects.append(object)
        #print 'self.trackable_objects = ',self.trackable_objects
        self.number_of_trackable_object = len(self.trackable_objects)
        self.gather_attributes()

    def gather_attributes(self):
        #print 'gather_attributes'
        self.asset_attr_dic = {}
        self.highest_version_path_dic = {}
        self.publish_path_year_dic = {}
        self.year_exists_dic = {}
        self.bad_publish_path_list = []
        self.alt_version_found_list = []
        int_check = ['0','01','001','1','01','001','2','02','002','03','003','3','04','004','4','05','005','5','06','006','6','07','007','7','08','008','8','09','009','9','010','0010','10','011','0011','11','012','0012','12','013','0013','13','014','0014','14','015','0015','15','016','0016','16','017','0017','17','018','0018','18','019','0019','19','020','0020','20','021','0021','21','022','0022','22','023','0023','23','024','0024','24','025','0025','25']
        attrs = ['publish_type','publish_id','entity_id','version','publish_path','entity_name','task_type','task_id','publish_file']
        for object in self.trackable_objects:
            higher_version_found = 0
            year_exists_list = []
            print ' '
            print 'object = ',object
            node_type = cmds.nodeType(object)
            for attr in attrs:
                print 'attr = ',attr
                attr_exists = cmds.attributeQuery(attr,node = object,exists = True)
                if attr_exists == 1:
                    print 'attr_exists = 1'
                    value = cmds.getAttr(object + '.' + attr)
                    self.asset_attr_dic[object + '&&' + attr] = str(value)
                    if attr == 'publish_path':
                        #print 'attr = ',attr
                        #print 'value = ',value
                        self.alt_version_higher = 0
                        #print 'value = ',value
                        if 'isln-smb' in value:
                            #print 'isln-smb in ' + value
                            self.alt_path = value.replace('isln-smb','gfs')
                        else:
                            #print 'isln-smb not in ' + value + ' using GFS'
                            self.alt_path = value.replace('gfs','isln-smb')
                        #print 'self.alt_path = ',self.alt_path
                        ii = 0
                        while ii < 2:
                            #print ' '
                            #print 'ii while loop'
                            #print 'ii = ',ii
                            #print 'value = ',value
                            if ii == 1:
                                value = self.alt_path
                            self.files_in_19_folder = 0
                            #print 'value = ',value
                            value_split = value.split('\\')
                            #value_split = value.split('/')
                            #print 'value_split = ',value_split
                            #self.publish_path_year_dic[object] = value_split[9]
                            self.publish_path_year_dic[object] = value_split[5]
                            #print 'self.publish_path_year_dic = ', self.publish_path_year_dic
                            #print 'self.publish_path_year_dic[object] = ', self.publish_path_year_dic[object]
                            #publish_year = value_split[5]
                            publish_year = value_split[5]
                            publish_path_value_split = value.split('\\')
                            #publish_path_value_split = value.split('/')
                            publish_path_value_split_length = len(publish_path_value_split)
                            year_versions_path = ''
                            product_texture_found = 0
                            Kraft_texture_found = 0
                            Kroger_texture_found = 0
                            #print 'A value = ',value
                            if 'Product' in value:
                                #print 'Product detected'
                                product_texture_found = 1
                            if 'Kraft' in value:
                                #print 'Kraft detected'
                                Kraft_texture_found = 1
                            if 'Kroger' in value:
                                #print 'Kroger detected'
                                Kroger_texture_found = 1
                            i = 0
                            publish_path_value_forward_length = 5
                            #publish_path_value_forward_length = 9
                            #print 'B value = ',value
                            while i < publish_path_value_forward_length:
                                #print 'i = ',i
                                if i == 0:
                                    year_versions_path
                                if i > 0:
                                    #print 'i = ',i
                                    #print 'publish_path_value_split = ',publish_path_value_split
                                    #year_versions_path = year_versions_path +'/' + publish_path_value_split[i]
                                    year_versions_path = year_versions_path +'\\' + publish_path_value_split[i]
                                    #print 'year_versions_path = ',year_versions_path
                                i = i + 1
                            year_versions_path = year_versions_path + '\\'
                            print 'year_versions_path final = ',year_versions_path
                            eighteen_year_versions = []
                            nineteen_year_versions = []
                            eighteen_version_number_full_string = ''
                            nineteen_version_number_full_string = ''
                            year_versions = cmds.getFileList(folder = year_versions_path) or []
                            #print 'year_versions = ',year_versions
                            highest_version = 0
                            #print 'year_versions = ',year_versions
                            for year_version in year_versions:
                                #print ' '
                                #print 'year verson loop'
                                #print 'year_version = ',year_version
                                #print 'value = ',value
                                publish_path_value_split_length = len(publish_path_value_split)
                                if year_version != '.DS_Store':
                                    if '18' in year_version:
                                        #print 'adding 18 to year_exists_dic'
                                        self.year_exists_dic[object] = year_exists_list.append('18')
                                    if '19' in year_version:
                                        #print 'adding 19 to year_exists_dic'
                                        self.year_exists_dic[object] = year_exists_list.append('19')
                                    if year_version != '.DS_Store':
                                        if '20' in year_version:
                                            #print 'adding 20 to year_exists_dic'
                                            self.year_exists_dic[object] = year_exists_list.append('20')
                                    if node_type == 'file':
                                        #print 'node type = file'
                                        publish_path_value_split_length = publish_path_value_split_length - 2
                                        #print 'publish_path_value_split_length = ',publish_path_value_split_length
                                    if node_type != 'file':
                                        publish_path_value_split_length = publish_path_value_split_length - 1
                                    publish_path_value_dir = ''
                                    i = 1
                                    #print 'year_version = ',year_version
                                    #print 'publish_path_value_split_length = ',publish_path_value_split_length
                                    while i < publish_path_value_split_length:
                                        #if i == 9:
                                        if i == 5:
                                                #publish_path_value_dir = publish_path_value_dir + '/' + year_version
                                                publish_path_value_dir = publish_path_value_dir + '\\' + year_version
                                        else:
                                            #publish_path_value_dir = publish_path_value_dir + '/' + publish_path_value_split[i]
                                            publish_path_value_dir = publish_path_value_dir + '\\' + publish_path_value_split[i]
                                        i = i + 1
                                    #publish_path_value_dir = publish_path_value_dir + '/'
                                    publish_path_value_dir = publish_path_value_dir + '\\'
                                    #print 'publish_path_value_dir = ',publish_path_value_dir
                                    files = []
                                    files = cmds.getFileList(folder = publish_path_value_dir) or []
                                    #print 'files = ',files
                                    number_of_files= len(files)
                                    #print 'number_of_files = ',number_of_files
                                    #publish_path_value_dir_split = publish_path_value_dir.split('/')
                                    publish_path_value_dir_split = publish_path_value_dir.split('\\')
                                    #temp_year_used = publish_path_value_dir_split[9]
                                    temp_year_used = publish_path_value_dir_split[5]
                                    #print 'temp_year_used = ',temp_year_used
                                    #print '1 publish_path_value_dir = ',publish_path_value_dir
                                    if number_of_files != 0:
                                        bad_file_type_list = ['.DS_Store','workarea','cache','die','photo','scan','_workarea','_cache','_die','_photo','_scan','version']
                                        #print 'node_type = ',node_type
                                        if node_type != 'file':
                                            #print 'node type != file'
                                            #print ' '
                                            #print 'files = ',files
                                            for file in files:
                                                #print 'file = ',file
                                                if file not in bad_file_type_list:
                                                    #print 'not one of the bad file types'
                                                    #print 'file = ',file
                                                    file_full = file
                                                    file_split = file.split('.')
                                                    file = file_split[0]
                                                    file_split_ = file.split('_')
                                                    number_of_file_splits_ = len(file_split_)
                                                    number_of_file_splits_ = number_of_file_splits_ - 1
                                                    #print 'file_split_ = ',file_split_
                                                    file = file_split_[number_of_file_splits_]
                                                    #print ' file_split_[number_of_file_splits_] = ', file_split_[number_of_file_splits_]
                                                    version_number = file
                                                    #print 'version_number = ',version_number
                                                    #print 'highest_version = ',highest_version
                                                    if version_number in int_check:
                                                        if int(version_number) > int(highest_version) or int(version_number) == int(highest_version) and '17' in publish_year and '18' in temp_year_used or int(version_number) == int(highest_version) and '17' in publish_year and '19' in temp_year_used or int(version_number) == int(highest_version) and '17' in publish_year and '20' in temp_year_used or int(version_number) == int(highest_version) and '18' in publish_year and '19' in temp_year_used or int(version_number) == int(highest_version) and '18' in publish_year and '20' in temp_year_used or int(version_number) == int(highest_version) and '19' in publish_year and '20' in temp_year_used:
                                                            highest_version = str(version_number)
                                                            #print 'setting higher version_number = ',version_number
                                                            #print 'setting higher highest_version = ',highest_version
                                                            zero_check = highest_version[0]
                                                            if zero_check == '0':
                                                                highest_version = highest_version[1:]
                                                                zero_check_2 = highest_version[0]
                                                                if zero_check_2 == '0':
                                                                    highest_version = highest_version[1:]
                                                            if ii == 0:
                                                                #print 'C1 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                                #print 'C1 publish_path_value_dir = ',publish_path_value_dir
                                                                self.asset_attr_dic[object + '&&' + 'highest_version'] = highest_version
                                                                highest_path_string = (object + ':  ' + publish_path_value_dir + file_full)
                                                                #print 'ii = 0 highest_path_string = ',highest_path_string
                                                                self.highest_version_path_dic[object] = highest_path_string
                                                                higher_version_found = 1
                                                                self.highest_value_year = temp_year_used
                                                                #print 'C2 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                                #print 'C2 highest_path_string = ',highest_path_string
                                                                #print 'C2 publish_path_value_dir = ',publish_path_value_dir
                                                            if ii == 1:
                                                                #print 'D2a1 highest_path_string = ',highest_path_string
                                                                #print 'D2a1 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                                #print 'D2a1 publish_path_value_dir = ',publish_path_value_dir
                                                                self.asset_attr_dic['alt_path_' + object + '&&' + 'highest_version'] = highest_version
                                                                #print 'D2a2 highest_path_string = ',highest_path_string
                                                                #print 'D2a2 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                                #print 'D2a2 publish_path_value_dir = ',publish_path_value_dir
                                                                highest_path_string = (object + ':  ' + publish_path_value_dir + file_full)
                                                                #print 'D2a3 highest_path_string = ',highest_path_string
                                                                #print 'D2a3 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                                #print 'ii = 1 highest_path_string = ',highest_path_string
                                                                self.highest_version_path_dic[object] = highest_path_string
                                                                #print 'D2a4 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                                higher_version_found = 1
                                                                #print 'D2a4 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                                self.highest_value_year = temp_year_used
                                                                #print 'D2a4 self.highest_version_path_dic = ',self.highest_version_path_dic
                                                            #print 'self.highest_value_year = ',self.highest_value_year
                                        #print 'end self.highest_version_path_dic = ',self.highest_version_path_dic
                                        if node_type == 'file':
                                            #print 'node type = file'
                                            folder_files = []
                                            for file in files:
                                                if file.startswith('v'):
                                                    folder_files.append(file)
                                            #print 'folder_files = ',folder_files
                                            for folder_file in folder_files:
                                                #print 'folder_file = ',folder_file
                                                if folder_file not in bad_file_type_list:
                                                    #print 'not one of the bad file types'
                                                    version_number = folder_file[-1]
                                                    #print 'version_number = ',version_number
                                                    #print 'highest_version = ',highest_version
                                                    #print 'temp_year_used = ',temp_year_used
                                                    if int(version_number) > int(highest_version) or int(version_number) == int(highest_version) and '17' in publish_year and '18' in temp_year_used or int(version_number) == int(highest_version) and '17' in publish_year and '19' in temp_year_used or int(version_number) == int(highest_version) and '17' in publish_year and '20' in temp_year_used or int(version_number) == int(highest_version) and '18' in publish_year and '19' in temp_year_used or int(version_number) == int(highest_version) and '18' in publish_year and '20' in temp_year_used or int(version_number) == int(highest_version) and '19' in publish_year and '20' in temp_year_used:
                                                        highest_version = version_number
                                                        #print 'highest_version = ',highest_version
                                                        if ii == 0:
                                                            #print 'ii = ',ii
                                                            self.asset_attr_dic[object + '&&' + 'highest_version'] = highest_version
                                                            highest_path_string = (object + ':  ' + publish_path_value_dir + folder_file)
                                                            self.highest_version_path_dic[object] = highest_path_string
                                                            higher_version_found = 1
                                                            self.highest_value_year = temp_year_used
                                                        if ii == 1:
                                                            #print 'ii = ',ii
                                                            self.asset_attr_dic['alt_path_' + object + '&&' + 'highest_version'] = highest_version
                                                            highest_path_string = (object + ':  ' + publish_path_value_dir + folder_file)
                                                            self.highest_version_path_dic[object] = highest_path_string
                                                            higher_version_found = 1
                                                            self.highest_value_year = temp_year_used
                                                        #print 'self.highest_value_year = ',self.highest_value_year
                            #print 'self.highest_version_path_dic = ',self.highest_version_path_dic
                            publish_path_value_dir = value = cmds.getAttr(object + '.' + attr)
                            #print '2 publish_path_value_dir = ',publish_path_value_dir
                            #print 'node_type = ',node_type
                            #print 'product_texture_found = ',product_texture_found
                            if node_type == 'file':
                                #print 'node_type = file'
                                if product_texture_found == 0 and Kroger_texture_found == 0:
                                    publish_path_value_split_length = publish_path_value_split_length - 2
                                if product_texture_found == 1 and Kroger_texture_found == 0:
                                    publish_path_value_split_length = publish_path_value_split_length - 2
                                if product_texture_found == 1 and Kroger_texture_found == 1:
                                    #print 'product texture found and Kroger texture found'
                                    publish_path_value_split_length = publish_path_value_split_length - 0
                                #publish_path_value_split_length = publish_path_value_split_length + 3
                            if node_type != 'file':
                                publish_path_value_split_length = publish_path_value_split_length - 1
                            publish_path_value_dir = ''
                            i = 1
                            #print 'publish_path_value_split_length = ',publish_path_value_split_length
                            #publish_path_value_split_length = 13
                            while i < publish_path_value_split_length:
                                #publish_path_value_dir = publish_path_value_dir + '/' + publish_path_value_split[i]
                                publish_path_value_dir = publish_path_value_dir + '\\' + publish_path_value_split[i]
                                i = i + 1
                            #publish_path_value_dir = publish_path_value_dir + '/'
                            publish_path_value_dir = publish_path_value_dir + '\\'
                            #print 'publish_path_value_dir = ',publish_path_value_dir
                            files = cmds.getFileList(folder = publish_path_value_dir) or []
                            #print 'files = ',files
                            number_of_files= len(files)
                            #print 'number_of_files = ',number_of_files
                            if number_of_files == 0:
                                #print 'num of files = 0, setting X'
                                if ii == 0:
                                    self.asset_attr_dic[object + '&&' + 'highest_version'] = 'X'
                                if ii == 1:
                                    self.asset_attr_dic['alt_path_' + object + '&&' + 'highest_version'] = 'X'
                            #print 'self.asset_attr_dic = ',self.asset_attr_dic
                            ii = ii + 1
                        #print 'object = ',object
                        print 'highest_version = ',highest_version
                        #print 'self.asset_attr_dic = ',self.asset_attr_dic
                        check_isln_value = self.asset_attr_dic[object + '&&' + 'highest_version']
                        print 'check_isln_value = ',check_isln_value
                        check_gfs_value = self.asset_attr_dic['alt_path_' + object + '&&' + 'highest_version']
                        print 'check_gfs_value = ',check_gfs_value
                        if check_gfs_value > check_isln_value:
                            self.alt_version_higher = 1
                            self.alt_version_found_list.append(object)
                        if self.alt_version_higher == 0:
                            #print 'end value = ',value
                            gfs_value = self.highest_version_path_dic[object]
                            isln_value = gfs_value.replace('gfs','isln-smb')
                            print 'self.highest_version_path_dic = ',self.highest_version_path_dic
                            self.highest_version_path_dic[object] = isln_value
                            print 'self.highest_version_path_dic = ',self.highest_version_path_dic
            #print '2 self.asset_attr_dic = ',self.asset_attr_dic
            #print 'THIS self.highest_version_path_dic = ',self.highest_version_path_dic
            for asset_attr in self.asset_attr_dic:
                #print 'asset_attr = ',asset_attr
                if 'alt_path_' not in asset_attr:
                    #print 'alt_path not in asset_attr'
                    if 'highest_version' in asset_attr:
                        #print 'highest version found in asset_attr'
                        #print 'object = ',object
                        #print object + '&&' + 'highest_version'
                        #print 'self.asset_attr_dic = ',self.asset_attr_dic
                        version = self.asset_attr_dic[object + '&&' + 'highest_version']
                        if 'X' in version:
                            if object not in self.bad_publish_path_list:
                                self.bad_publish_path_list.append(object)
        #print 'gather_attributes self.asset_attr_dic = ',self.asset_attr_dic
        #print 'gather_attributes self.highest_version_path_dic = ',self.highest_version_path_dic
        self.populate_window()

    def populate_window(self):
        #print 'populate_window'
        self.alt_path_list = []
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
                    alt_path_highest_version_value = 0
                    highest_version_value = 0
                    if attr == 'highest_version':
                        for asset_attr in self.asset_attr_dic:
                            if asset_attr == asset_name + '&&highest_version' or asset_attr == 'alt_path_' + asset_name + '&&highest_version':
                                if 'alt_path_' in asset_attr:
                                    #print 'ALT PATH'
                                    alt_path_highest_version_value = self.asset_attr_dic[asset_attr]
                                    #print 'alt_path_highest_version_value = ',alt_path_highest_version_value
                                else:
                                    #print 'REGULAR VERSION'
                                    highest_version_value = self.asset_attr_dic[asset]
                                    #print 'highest_version_value = ',highest_version_value
                        if alt_path_highest_version_value > highest_version_value:
                            #print 'alt_path is higher than regular path, using ' + alt_path_highest_version_value
                            highest_version_value = alt_path_highest_version_value
                            self.alt_path_list.append(asset_name)
                        #print 'END highest_version_value = ',highest_version_value
                        self.highest_version_listWidget.addItem(highest_version_value)
                    if attr == 'entity_name':
                        entity_name_value = self.asset_attr_dic[asset]
                        self.entity_name_listWidget.addItem(entity_name_value)
                    if attr == 'publish_path':
                        publish_path_value = self.asset_attr_dic[asset]
                        self.publish_path_listWidget.addItem(publish_path_value)
        self.evaluate_versions()

    def latest_version_path_feedback_listWidget_populate(self):
        #print 'latest_version_path_feedback_listWidget_populate'
        number_of_objects = self.node_name_listWidget.count()
        i = 0
        while i < number_of_objects:
            has_a_higher_version = 0
            item = self.node_name_listWidget.item(i)
            item_text = item.text()
            #print 'self.alt_path_list = ',self.alt_path_list
            #print 'item_text = ',item_text
            #print 'self.highest_version_path_dic = ',self.highest_version_path_dic
            for highest_version_path_item in self.highest_version_path_dic:
                if highest_version_path_item == item_text:
                    if item_text in self.alt_path_list:
                        highest_version_path_item_path = self.highest_version_path_dic[highest_version_path_item]
                        highest_version_path_item_path = highest_version_path_item_path.replace('isln-smb','gfs')
                        #highest_version_path_item_path_split = highest_version_path_item_path.split(':')
                        #highest_version_path_item_path = highest_version_path_item_path_split[1]
                        #highest_version_path_item_path = highest_version_path_item_path.replace(' ','')
                        #print 'highest_version_path_item_path = ',highest_version_path_item_path
                    else:
                        highest_version_path_item_path = self.highest_version_path_dic[highest_version_path_item]
                        #print 'highest_version_path_item_path = ',highest_version_path_item_path
                    self.latest_version_path_feedback_listWidget.addItem(highest_version_path_item_path)
                    has_a_higher_version = 1
            if item_text in self.bad_publish_path_list:
                if has_a_higher_version == 0:
                    bad_publish_path_string = item_text + ':  no valid publish path detected, can not find the latest version of the object'
                    self.latest_version_path_feedback_listWidget.addItem(bad_publish_path_string)
            i = i + 1
        number_of_objects = self.latest_version_path_feedback_listWidget.count()
        i = 0
        while i < number_of_objects:
            item = self.latest_version_path_feedback_listWidget.item(i)
            item.setTextColor(QtGui.QColor("#5E5E5E"))
            i = i + 1
        #self.deactivate_listWidget(self.latest_version_path_feedback_listWidget)

    def evaluate_versions(self):
        #print 'evaluate_versions'
        i = 0
        while i < self.number_of_trackable_object:
            #print 'self.asset_attr_dic = ',self.asset_attr_dic
            object_item = self.node_name_listWidget.item(i)
            object_item_text = object_item.text()
            #print 'object_item_text = ',object_item_text
            #print 'self.alt_version_higher = ', self.alt_version_higher
            current_version_item = self.current_version_listWidget.item(i)
            current_version_item_text = current_version_item.text()
            current_version_item_int = int(current_version_item_text)
            highest_version_item = self.highest_version_listWidget.item(i)
            highest_version_item_text = highest_version_item.text()
            entity_name_item = self.entity_name_listWidget.item(i)
            publish_path_item = self.publish_path_listWidget.item(i)
            #print 'highest_version_item_text = ',highest_version_item_text
            if highest_version_item_text != 'X':
                if highest_version_item_text != 'none':
                    highest_version_item_int = int(highest_version_item_text)
                    highest_version_item.setTextColor('light blue')
                    if highest_version_item_int > current_version_item_int:
                        object_item.setTextColor('red')
                        current_version_item.setTextColor('red')
                        entity_name_item.setTextColor('red')
                        publish_path_item.setTextColor('red')
                        #print 'object_item_text = ',object_item_text
                        #print 'self.alt_version_found_list = ',self.alt_version_found_list
                        if object_item_text in self.alt_version_found_list:
                            object_item.setTextColor('pink')
                            current_version_item.setTextColor('pink')
                            entity_name_item.setTextColor('pink')
                            publish_path_item.setTextColor('pink')
                    else:
                        object_item.setTextColor('light blue')
                        current_version_item.setTextColor('light blue')
                        entity_name_item.setTextColor('light blue')
                        publish_path_item.setTextColor('light blue')
                    #print ' '
                    #print 'object_item_text = ',object_item_text
                    #print 'self.publish_path_year_dic = ',self.publish_path_year_dic
                    #print 'self.highest_value_year: = ',self.highest_value_year
                    for publish_year in self.publish_path_year_dic:
                        if publish_year == object_item_text:
                            #print 'publish_year matches object_item_text'
                            publish_year_value = self.publish_path_year_dic[object_item_text]
                            if '17' in publish_year_value and '18' in self.highest_value_year or '17' in publish_year_value and '19' in self.highest_value_year or '17' in publish_year_value and '20' in self.highest_value_year or '18' in publish_year_value and '19' in self.highest_value_year or '18' in publish_year_value and '20' in self.highest_value_year or '19' in publish_year_value and '20' in self.highest_value_year:
                                #print 'older version detected in publish_year_value and newer version detected in self.highest_value_year'
                                highest_version_item.setTextColor('yellow')
                                entity_name_item.setTextColor('yellow')
                                publish_path_item.setTextColor('yellow')
                    #print 'self.publish_path_year_dic = ',self.publish_path_year_dic
                    #print ' '
                    publish_year_value = self.publish_path_year_dic[object_item_text]
                    year_exists_list = self.publish_path_year_dic[object_item_text]
                    if '17' in publish_year_value:
                        if '18' in year_exists_list or '19' in year_exists_list or '20' in year_exists_list:
                            #print '18 in self.publish_path_year_dic'
                            highest_version_item.setTextColor('yellow')
                            entity_name_item.setTextColor('yellow')
                            publish_path_item.setTextColor('yellow')
                    if '18' in publish_year_value:
                        if '19' in year_exists_list or '20' in year_exists_list:
                            #print '19 in self.publish_path_year_dic'
                            highest_version_item.setTextColor('yellow')
                            entity_name_item.setTextColor('yellow')
                            publish_path_item.setTextColor('yellow')
                    if '19' in publish_year_value:
                        if '20' in year_exists_list:
                            #print '20 in self.publish_path_year_dic'
                            highest_version_item.setTextColor('yellow')
                            entity_name_item.setTextColor('yellow')
                            publish_path_item.setTextColor('yellow')
            if highest_version_item_text == 'X':
                object_item.setTextColor('orange')
                current_version_item.setTextColor('orange')
                highest_version_item.setTextColor('orange')
                entity_name_item.setTextColor('orange')
                publish_path_item.setTextColor('orange')
            i = i + 1
        self.latest_version_path_feedback_listWidget_populate()
        #self.deactivate_listWidget(self.node_name_listWidget)
        self.deactivate_listWidget(self.current_version_listWidget)
        self.deactivate_listWidget(self.highest_version_listWidget)

    def node_name_listWidget_item_pressed(self,item):
        #print 'node_name_listWidget_item_pressed'
        item_text = item.text()
    #    print 'item_text = ',item_text
        i = 0
        latest_version_path_feedback_listWidget = self.latest_version_path_feedback_listWidget.count()
        while i < latest_version_path_feedback_listWidget:
            latest_version_path_feedback_listWidget_item = self.latest_version_path_feedback_listWidget.item(i)
            latest_version_path_feedback_listWidget_item_text = latest_version_path_feedback_listWidget_item.text()
            #print 'latest_version_path_feedback_listWidget_item_text = ',latest_version_path_feedback_listWidget_item_text
            latest_version_path_feedback_listWidget_item.setTextColor(QtGui.QColor("#5E5E5E"))
            latest_version_path_feedback_listWidget_item_text_split = latest_version_path_feedback_listWidget_item_text.split(':')
            latest_version_path_feedback_listWidget_item_text = latest_version_path_feedback_listWidget_item_text_split[0]
            if item_text == latest_version_path_feedback_listWidget_item_text:
                #print 'item_text = ',item_text
                #print 'latest_version_path_feedback_listWidget_item_text = ',latest_version_path_feedback_listWidget_item_text
                latest_version_path_feedback_listWidget_item.setTextColor('light blue')
            i = i + 1

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
        #print 'publish_path_item_press = '
        item_text = item.text()
        #item_text_split = item_text.split('/')
        item_text_split = item_text.split('\\')
        item_text_split_length = len(item_text_split)
        i = 1
        item_path = ''
        while i < (item_text_split_length - 1):
            #item_path = item_path + '/' + item_text_split[i]
            item_path = item_path + '\\' + item_text_split[i]
            i = i + 1
        subprocess_string = 'explorer ' + item_path
        #print 'subprocess_string = ',subprocess_string
        subprocess.Popen(subprocess_string)
        self.publish_path_listWidget.clearSelection()
        self.publish_path_listWidget.setCurrentIndex(QtCore.QModelIndex())

    def latest_version_path_feedback_listWidget_populate_item_press(self,item):
        #print 'latest_version_path_feedback_listWidget_populate_item_press'
        item_text = item.text()
        #print 'item_text = ',item_text
        item_text_split = item_text.split(': ')
        #print 'item_text_split = ',item_text_split
        item_text_path = item_text_split[1]
        #print 'item_text_path = ',item_text_path
        #item_text_path_split = item_text_path.split('/')
        item_text_path_split = item_text_path.split('\\')
        #print 'item_text_path_split = ',item_text_path_split
        item_text_split_length = len(item_text_path_split)
        i = 1
        item_path = ''
        while i < (item_text_split_length - 1):
            #item_path = item_path + '/' + item_text_path_split[i]
            item_path = item_path + '\\' + item_text_path_split[i]
            i = i + 1
        subprocess_string = 'explorer ' + item_path
        #print 'subprocess_string = ',subprocess_string
        subprocess.Popen(subprocess_string)
        for i in range(self.latest_version_path_feedback_listWidget.count()):
            item = self.latest_version_path_feedback_listWidget.item(i)
            self.latest_version_path_feedback_listWidget.setItemSelected(item, False)
        self.latest_version_path_feedback_listWidget.clearSelection()
        self.latest_version_path_feedback_listWidget.setCurrentIndex(QtCore.QModelIndex())

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
        titles = ['Name (red indicates a newer version of the asset exists)','C-ver','L-ver','Entity Name','Published Path ( yellow indicates a version of this asset exists in a more recent year directory, orange indicates an invalid publish path is linked to the asset)']
        i = 0
        for title in titles:
            label = QtWidgets.QLabel(title)
            self.main_grid_layout.addWidget(label,0,i)
            i = i + 1
        spacing = 3
        self.node_name_listWidget = QtWidgets.QListWidget()
        self.node_name_listWidget.setSpacing(spacing)
        self.node_name_listWidget.setMinimumHeight(500)
        self.node_name_listWidget.setMaximumWidth(325)
        self.node_name_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.node_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.node_name_listWidget.itemClicked.connect(partial(self.node_name_listWidget_item_pressed))
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
        #self.entity_name_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.entity_name_listWidget)
        self.publish_path_listWidget = QtWidgets.QListWidget()
        self.publish_path_listWidget.setSpacing(spacing)
        self.publish_path_listWidget.itemClicked.connect(partial(self.publish_path_item_press))
        self.publish_path_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.publish_path_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.main_grid_layout.addWidget(self.publish_path_listWidget)
        label_full_paths_listWidget = QtWidgets.QLabel('Full paths to the latest versions of the assets')
        self.main_grid_layout.addWidget(label_full_paths_listWidget,2,0,1,5)
        self.latest_version_path_feedback_listWidget = QtWidgets.QListWidget()
        self.latest_version_path_feedback_listWidget.setMinimumHeight(400)
        self.latest_version_path_feedback_listWidget.setSpacing(spacing)
        self.latest_version_path_feedback_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.latest_version_path_feedback_listWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.latest_version_path_feedback_listWidget.itemClicked.connect(partial(self.latest_version_path_feedback_listWidget_populate_item_press))
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
