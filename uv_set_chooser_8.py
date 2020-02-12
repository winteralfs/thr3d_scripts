"""

.. image:: U:/cwinters/docs/build/html/_images/uv_set_chooser/uv_set_chooser_v01.JPG
   :align: center
   :scale: 75%

The uv_set_chooser works as an alternative to the traditional Maya relationship editor:uv_editor. It's purpose
is to function faster, and to be more interactive than the traditional GUI.

You launch the uv_set_chooser from the lighting shelf:

.. image:: U:/cwinters/docs/build/html/_images/uv_set_chooser/uv_set_chooser_lighting_shelf_v01.JPG
   :align: center
   :scale: 75%

You can link uv sets and textures from either uv set centric mode, or texture centric mode.

.. image:: U:/cwinters/docs/build/html/_images/uv_set_chooser/uv_set_chooser_texture_picked_UV_CENTRIC_v01.JPG
   :align: center
   :scale: 75%

In uv_centric mode, you select the uv set on the left, and choose what textures should use that uv set on the right.

.. image:: U:/cwinters/docs/build/html/_images/uv_set_chooser/uv_set_chooser_texture_picked_UV_CENTRIC_v01.JPG
   :align: center
   :scale: 75%

In texure_centric mode, you choose the texture on the left, and choose which uv sets that texture should use, one per object.
The objects that are currently using the chosen texture will be light blue, and all other objects will be dark grey.

.. image:: U:/cwinters/docs/build/html/_images/uv_set_chooser/uv_set_chooser_texture_picked_TEXTURE_CENTRIC_v01.JPG
   :align: center
   :scale: 75%

"""

import maya
import maya.cmds as cmds
import os
import os.path
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2


class UV_SET_EDITOR(object):
    def __init__(self):
        self.selected_item_text = ''
        self.spacer = '          '
        self.filepath = cmds.file(q=True, sn=True)
        self.filename = os.path.basename(self.filepath)
        self.raw_name, extension = os.path.splitext(self.filename)
        #self.file_name_on_disk = '/Users/alfredwinters/Desktop/' + self.raw_name + '_uv_set_status_dic_on_disk.txt'
        self.file_name_on_disk = 'U:/cwinters/uv_set_chooser_temp_files/' + self.raw_name + '_uv_set_status_dic_on_disk.txt'

#---------- procedural tools and data gathering methods ----------

    def centric_state(self):
        #print 'centric_state'
        self.uv_set_selection_status_dic_state_change = self.uv_set_selection_status_dic
        self.centric_state_text = self.texture_based_uv_set_based_combobox.currentText()
        self.right_label.setText('textures')
        if self.centric_state_text == 'texture-centric':
            self.left_label.setText('textures')
            self.right_label.setText('uv sets')
        if self.centric_state_text == 'UV-centric':
            self.left_label.setText('uv sets')
            self.right_label.setText('textures')
        self.selected_item_text = ''
        self.list_widget_texture_info.clear()
        self.populate_windows()

    def selected_items_right_listWidget(self):
        #print 'selected_items_right_listWidget()'
        self.selected_items_right_text = []
        self.selected_right_list_pointers = self.list_widget_right.selectedItems()
        for selected_right_list_pointer in self.selected_right_list_pointers:
            selected_right_list_pointer_text = selected_right_list_pointer.text()
            for file in self.file_to_file_path_dic:
                item_sub = self.file_to_file_path_dic[file]
                if item_sub == selected_right_list_pointer_text:
                    selected_right_list_pointer_text = file
            self.selected_items_right_text.append(selected_right_list_pointer_text)
        for pointer in self.selected_right_list_pointers:
            pointer_text = pointer.text()
            for file in self.file_to_file_path_dic:
                item_sub = self.file_to_file_path_dic[file]
                if item_sub == pointer_text:
                    pointer_text = file

    def deselect_QListWidget(self,listwidget):
        #print 'deselect right list widget items()'
        for i in range(listwidget.count()):
            item = listwidget.item(i)
            listwidget.setItemSelected(item, False)

    def activate_right_listWidget(self):
        #print 'activate_right_listWidget()'
        self.item_selected_length = len(self.selected_item_text)
        if self.item_selected_length == 0:
            self.list_widget_right.setStyleSheet('QListWidget {background-color: #292929; color: #515151;}')
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                it = it + 1
        else:
            self.list_widget_right.setStyleSheet('QListWidget {background-color: #292929; color: #726f6f;}')
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                it = it + 1

    def unlock_right_QListWidget(self):
        #print 'unlock_right_QListWidget()'
        it = 0
        while it < self.number_of_items_in_right_listWidget:
            item = self.list_widget_right.item(it)
            item_text = item.text()
            if '*' in item_text:
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            if '*' not in item_text:
                item.setFlags(item.flags() | Qt.ItemIsSelectable)
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
            it = it + 1
        self.deactivate_empty_lines()

    def lock_selected_right_QListWidget(self):
        #print 'lock_selected_right_QListWidget()'
        self.unlock_right_QListWidget()
        selected_uv_sets_pointers = self.list_widget_right.selectedItems()
        for selected_uv_set_pointer in selected_uv_sets_pointers:
            item = selected_uv_set_pointer
            item_text = item.text()
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

    def deactivate_empty_lines(self):
        #print 'deactivate_empty_lines'
        if self.centric_state_text == 'texture-centric':
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item_text = item.text()
                #print 'item_text = ',item_text
                item_len = len(item_text)
                #print 'item_len = ',item_len
                if item_len == 2:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                it = it + 1
        if self.centric_state_text == 'UV-centric':
            it = 0
            while it < self.number_of_items_in_left_listWidget:
                item = self.list_widget_left.item(it)
                item_text = item.text()
                #print 'item_text = ',item_text
                item_len = len(item_text)
                #print 'item_len = ',item_len
                if item_len == 2:
                    item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                it = it + 1

    def populate_windows(self):
        #print 'populate_windows()'
        self.evaluate_textures_in_scene()
        self.evaluate_UV_sets_in_scene()
        self.list_widget_left.clear()
        self.list_widget_right.clear()
        self.list_widget_texture_info.clear()
        font_size = 11
        if self.centric_state_text == 'texture-centric':
            self.list_widget_left.setWrapping(False)
            self.list_widget_right.setWrapping(False)
            self.list_widget_left.setSpacing(3)
            self.list_widget_right.setSpacing(1)
            for texture in self.all_textures:
                texture_item = QtWidgets.QListWidgetItem(texture)
                texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                attr_string = (texture + '.fileTextureName')
                file_node_type = cmds.nodeType(texture)
                if texture in self.file_to_file_path_dic:
                    texture_plus_file_name = self.file_to_file_path_dic[texture]
                else:
                    texture_plus_file_name = texture
                self.list_widget_left.addItem(texture_plus_file_name)
                #texture_item.setTextAlignment(Qt.AlignBottom)
            for uv_set in self.uv_sets_all:
                empty_uv_set_detect = len(uv_set)
                if '*' not in uv_set and empty_uv_set_detect != 2:
                    uv_set_split = uv_set.split(':|:')
                    uv_set_short_name = uv_set_split[1]
                    uv_set_short_name = self.spacer + uv_set_short_name
                    self.list_widget_right.addItem(uv_set_short_name)
                else:
                    self.list_widget_right.addItem(uv_set)
            self.number_of_items_in_left_listWidget = self.list_widget_left.count()
            self.number_of_items_in_right_listWidget = self.list_widget_right.count()
            i = 0
            while i < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(i)
                item_text = item.text()
                if '*' in item_text:
                    item.setFont(QtGui.QFont('SansSerif', 12))
                i = i + 1
            self.activate_right_listWidget()
            self.initial_uv_set_name_to_address_dic_eval()
            self.deactivate_empty_lines()
        if self.centric_state_text == 'UV-centric':
            self.list_widget_right.setWrapping(True)
            self.list_widget_left.setWrapping(False)
            self.list_widget_right.setSpacing(4)
            self.list_widget_left.setSpacing(1)
            for texture in self.all_textures:
                texture_item = QtWidgets.QListWidgetItem(texture)
                texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                attr_string = (texture + '.fileTextureName')
                file_node_type = cmds.nodeType(texture)
                if texture in self.file_to_file_path_dic:
                    texture_plus_file_name = self.file_to_file_path_dic[texture]
                else:
                    texture_plus_file_name = texture
                if file_node_type == 'file':
                    texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                    self.list_widget_right.addItem(texture_plus_file_name)
                    texture_item.setTextAlignment(Qt.AlignBottom)
                if file_node_type != 'file':
                    texture_item = QtWidgets.QListWidgetItem(texture)
                    texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                    self.list_widget_right.addItem(texture_item)
                    texture_item.setTextAlignment(Qt.AlignBottom)
            for uv_set in self.uv_sets_all:
                empty_uv_set_detect = len(uv_set)
                if '*' not in uv_set and empty_uv_set_detect != 2:
                    uv_set_split = uv_set.split(':|:')
                    uv_set_short_name = uv_set_split[1]
                    uv_set_short_name = self.spacer + uv_set_short_name
                    self.list_widget_left.addItem(uv_set_short_name)
                else:
                    self.list_widget_left.addItem(uv_set)
            self.number_of_items_in_left_listWidget = self.list_widget_left.count()
            self.number_of_items_in_right_listWidget = self.list_widget_right.count()
            i = 0
            while i < self.number_of_items_in_left_listWidget:
                item = self.list_widget_left.item(i)
                item_text = item.text()
                if '*' in item_text:
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                    item.setFont(QtGui.QFont('SansSerif', 12))
                else:
                    item.setTextColor(QtGui.QColor('#515b8c'))
                i = i + 1
            self.initial_uv_set_name_to_address_dic_eval()
            self.activate_right_listWidget()
            self.deactivate_empty_lines()

    def evaluate_textures_in_scene(self):
        #print 'evaluate_textures_in_scene()'
        self.file_to_file_path_dic = {}
        self.all_textures = []
        valid_connection_types = ['VRayMtl','phong','blinn','lambert','surfaceShader','blend','VRayBlendMtl','layeredTexture','remapHsv','multiplyDivide','remapColor','gammaCorrect','VRayBumpMtl']
        bad_connection_types = ['VRayPlaceEnvTex']
        file_textures_all = cmds.ls(type = 'file')
        ramp_textures_all = cmds.ls(type = 'ramp')
        noise_texures_all = cmds.ls(type = 'noise')
        textures_all = file_textures_all + ramp_textures_all + noise_texures_all
        for texture in textures_all:
            #print 'texture = ',texture
            valid_file = 0
            texture_connections = cmds.listConnections(texture,source = False) or []
            #print 'texture_connections = ',texture_connections
            for texture_connection in texture_connections:
                #print 'texture_connection = ',texture_connection
                texture_connection_type = cmds.nodeType(texture_connection)
                #print 'texture_connection_type = ',texture_connection_type
                if texture_connection_type in valid_connection_types:
                    #print ' 0 setting light_ramp to 1'
                    if texture_connection_type not in bad_connection_types:
                        valid_file = 1
                else:
                    texture_connections_1 = cmds.listConnections(texture_connection,source = False) or []
                    #print 'texture_connections_1 = ',texture_connections_1
                    for texture_connection in texture_connections_1:
                        #print 'texture_connection = ',texture_connection
                        texture_connection_type = cmds.nodeType(texture_connection)
                        #print 'texture_connection_type = ',texture_connection_type
                        if texture_connection_type in valid_connection_types:
                            if texture_connection_type not in bad_connection_types:
                                valid_file = 1
                        else:
                            texture_connections_2 = cmds.listConnections(texture_connections_1,source = False) or []
                            for texture_connection in texture_connections_2:
                                texture_connection_type = cmds.nodeType(texture_connection)
                                if texture_connection_type in valid_connection_types:
                                    if texture_connection_type not in bad_connection_types:
                                        valid_file = 1
                                else:
                                    texture_connections_3 = cmds.listConnections(texture_connections_2,source = False) or []
                                    for texture_connection in texture_connections_3:
                                        texture_connection_type = cmds.nodeType(texture_connection)
                                        if texture_connection_type in valid_connection_types:
                                            if texture_connection_type not in bad_connection_types:
                                                valid_file = 1
                                        else:
                                            texture_connections_4 = cmds.listConnections(texture_connections_3,source = False) or []
                                            for texture_connection in texture_connections_3:
                                                texture_connection_type = cmds.nodeType(texture_connection)
                                                if texture_connection_type in valid_connection_types:
                                                    if texture_connection_type not in bad_connection_types:
                                                        valid_file = 1
            placement_connections = cmds.listConnections(texture, source = True, destination = False)
            #print 'texture = ',texture
            #print 'placement_connections = ',placement_connections
            VRayPlaceEnvTex_node_found = 0
            for connection in placement_connections:
                type = cmds.nodeType(connection)
                if type == 'VRayPlaceEnvTex':
                    VRayPlaceEnvTex_node_found = 1
                    #print 'VRayPlaceEnvTex_node_found'
            if valid_file == 1:
                if VRayPlaceEnvTex_node_found == 0:
                    #print 'appending ' + texture
                    self.all_textures.append(texture)
        #print 'self.all_textures = ', self.all_textures

    def write_UV_sets_state_file_to_disk(self):
        #print '* write_UV_sets_state_file_to_disk *'
        if os.path.isfile(self.file_name_on_disk) and os.access(self.file_name_on_disk, os.R_OK):
            #print ' removing file!'
            os.remove(self.file_name_on_disk)
        uv_set_status_dic_on_disk = open(self.file_name_on_disk,'a')
        #uv_set_status_dic_on_disk_content = uv_set_status_dic_on_disk.readlines()
        #uv_set_status_dic_on_disk_length = len(file_name_on_disk_contents)
        for uv_set in self.uv_set_selection_status_dic:
            #redundant = 0
            #print 'uv_set = ',uv_set
            #i = 0
            #while i < uv_set_status_dic_on_disk_length:
                #file_line = uv_set_status_dic_on_disk_content[i]
                #print 'file_line = ',file_line
                #print 'uv_set = ',uv_set
                #if file_line == uv_set:
                    #redundant = 1
                #i = i+1
            #if redundant == 0:
            uv_set_status_dic_on_disk.write(uv_set + '\n')
            uv_set_status_dic_on_disk.write(str(self.uv_set_selection_status_dic[uv_set]) + '\n')
        uv_set_status_dic_on_disk.close()

    def read_UV_sets_state_file_from_disk(self):
        #print '* read_UV_sets_state_file_from_disk *'
        file_name_on_disk = open(self.file_name_on_disk)
        self.uv_set_selection_status_dic_from_disk = {}
        #if file_name_on_disk == 'r':
        file_name_on_disk_contents = file_name_on_disk.readlines()
        #print 'file_name_on_disk_contents = ',file_name_on_disk_contents
        file_name_on_disk_contents_size = len(file_name_on_disk_contents)
        #print 'file_name_on_disk_contents_size = ',file_name_on_disk_contents_size
        i = 0
        while i < file_name_on_disk_contents_size:
            file_name_on_disk_contents_replaced_newline = file_name_on_disk_contents[i].replace('\n','')
            file_name_on_disk_contents_newline_plus_one = file_name_on_disk_contents[i+1].replace('\n','')
            self.uv_set_selection_status_dic_from_disk[file_name_on_disk_contents_replaced_newline] = file_name_on_disk_contents_newline_plus_one
            i = i+2
        file_name_on_disk.close()
        #print 'end read file self.uv_set_selection_status_dic_from_disk = ', self.uv_set_selection_status_dic_from_disk

    def evaluate_UV_sets_in_scene(self):
        #print ' '
        #print 'evaluate_UV_sets_in_scene()'
        self.uv_sets_all = []
        #print 'resetting uv_set_selection_status_dic'
        #print 'resetting self.uv_set_selection_status_dic_state_change'
        self.uv_set_name_to_address_dic = {}
        self.uv_set_selection_status_dic = {}
        self.uv_set_selection_status_dic_state_change = {}
        #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        transforms_all = []
        transforms_all_tmp = cmds.ls(type = 'shape')
        #print 'transforms_all_tmp = ',transforms_all_tmp
        transforms_all_tmp_no_shape = []
        except_nodes = ['std_lgt_core','locator','camera']
        except_shape_types = ['VRayLightRectShape','locator','camera']
        shape_name_dic = {}
        for transform in transforms_all_tmp:
            if 'polySurface' not in transform:
                node_type = cmds.nodeType(transform)
                if node_type not in except_shape_types:
                    #print 'transform = ',transform
                    if transform not in except_nodes or 'imagePLane1' not in transform:
                        transform_split = transform.split('Shape')
                        shape_name_dic[transform_split[0]] = transform_split[1]
                    #print 'transform_split',transform_split
                    if transform not in transforms_all_tmp_no_shape:
                        #print 'adding ',transform
                        if transform_split[0] not in transforms_all_tmp_no_shape:
                            transforms_all_tmp_no_shape.append(transform_split[0])
        #print 'transforms_all_tmp_no_shape = ',transforms_all_tmp_no_shape
        for transform_all_no_shape in transforms_all_tmp_no_shape:
            #print 'transform_all_no_shape = ',transform_all_no_shape
            if transform_all_no_shape not in except_nodes:
                transform_all_no_shape = transform_all_no_shape + 'Shape' + shape_name_dic[transform_all_no_shape]
            if transform_all_no_shape not in transforms_all:
                #print 'appendig ',transform_all_no_shape
                transforms_all.append(transform_all_no_shape)
        #print 'transforms_all = ',transforms_all
        transorms_objects = []
        bad_transform_nodes = []
        for transform in transforms_all:
            if 'imagePlane' not in transform:
                #print 'transform = ',transform
                transform_connections = cmds.listConnections(transform) or []
                #print 'transform_connections  = ',transform_connections
                number_of_transform_connections = len(transform_connections)
                if number_of_transform_connections == 0:
                    #print 'num transform connections == 0'
                    if transform not in bad_transform_nodes:
                        bad_transform_nodes.append(transform)
                if number_of_transform_connections == 1:
                    #print 'num transform connections == 1'
                    for transform_connection in transform_connections:
                        #print 'transform_connection = ',transform_connection
                        if transform_connection == 'hyperGraphLayout':
                            if transform not in bad_transform_nodes:
                                bad_transform_nodes.append(transform)
            #print 'bad_transform_nodes = ',bad_transform_nodes
        for transform_node in transforms_all:
            if 'imagePlane' not in transform_node:
                if transform_node not in bad_transform_nodes:
                    if transform_node not in transorms_objects:
                        transorms_objects.append(transform_node)
        for object in transorms_objects:
            #print 'xxx'
            #print 'self.uv_set_selection_status_dic = ', self.uv_set_selection_status_dic
            object_split = object.split('Shape')
            if 'polySurface' not in object_split[0]:
                uv_sets = cmds.polyUVSet(object,allUVSets = True, query = True) or []
                for uv_set in uv_sets:
                    rename_uv_set = 0
                    if uv_set != '':
                        for character in uv_set:
                            if character == ' ':
                                rename_uv_set = 1
                    if rename_uv_set == 1:
                        uv_set_no_space_name = uv_set.replace(' ','_')
                        #print 'space in name found, renaming ' + uv_set + ' to ' + uv_set_no_space_name
                        cmds.polyUVSet(object,rename = True, newUVSet = uv_set_no_space_name, uvSet = uv_set)
                uv_sets = []
                #print ' '
                #print '---'
                #print 'object = ',object
                uv_sets = cmds.polyUVSet(object,allUVSets = True, query = True) or []
                #print '2 uv_sets = ',uv_sets
                #print '---'
                #print ' '
                number_of_uv_sets = len(uv_sets)
                if number_of_uv_sets > 0:
                    self.uv_sets_all.append('* ' + object)
                    for uv_set in uv_sets:
                        uv_sets_all_string = object + ':|:' + uv_set
                        self.uv_sets_all.append(uv_sets_all_string)
                        for texture in self.all_textures:
                            if uv_set == 'map1':
                                #print 'setting ' + texture + ':|:' + uv_sets_all_string + 'to 1'
                                self.uv_set_selection_status_dic[texture + ':|:' + uv_sets_all_string] = 1
                            else:
                                #print 'setting ' + texture + ':|:' + uv_sets_all_string + 'to 0'
                                self.uv_set_selection_status_dic[texture + ':|:' + uv_sets_all_string] = 0
                    self.uv_sets_all.append('  ')
                    number_of_uv_sets_for_object = len(uv_sets)
                    uv_set_index_nums = cmds.polyUVSet(object,query=True, allUVSetsIndices=True)
                    for uv_set_index_num in uv_set_index_nums:
                        uv_set_index_num = str(uv_set_index_num)
                        uv_set_index_num.replace('L','')
                    it = 0
                    while it <= number_of_uv_sets_for_object:
                        i = 0
                        for uv_set in uv_sets:
                            uv_set_index = uv_set_index_nums[i]
                            uv_set_address = object + '.uvSet[' + str(uv_set_index) + '].uvSetName'
                            self.uv_set_name_to_address_dic[object + ':|:' + uv_set] = uv_set_address
                            i = i + 1
                        it = it + 1
        #print 'end evaluate_UV_sets_in_scene self.uv_set_selection_status_dic = ', self.uv_set_selection_status_dic
        #print ' '

    def initial_uv_set_name_to_address_dic_eval(self):
        #print 'initial_uv_set_name_to_address_dic_eval'
        #print 'start initial_uv_set_name_to_address_dic_eval self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        assigned_uv_sets = []
        for texture in self.all_textures:
            #print ' '
            #print 'A initial_uv_set_name_to_address_dic_eval self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
            #print 'texture = ',texture
            uv_set_names_linked_to_texture = []
            uv_sets_linked_to_texture = cmds.uvLink(texture = texture, query = True) or []
            #print 'uv_sets_linked_to_texture = ',uv_sets_linked_to_texture
            #print 'self.uv_sets_all = ',self.uv_sets_all
            #print ' '
            for uv_set_all in self.uv_sets_all:
                #print ' '
                #print 'uv_set_all = ',uv_set_all
                #print 'uv_sets_linked_to_texture = ',uv_sets_linked_to_texture
                empty_uv_set_detect = len(uv_sets_linked_to_texture)
                #print 'empty_uv_set_detect = ',empty_uv_set_detect
                if empty_uv_set_detect != 2 and empty_uv_set_detect > 0:
                    #print 'two uv sets NOT linked_to_texture and not zero uv sets'
                    uv_set_all_split = uv_set_all.split('*')
                    #print '1 uv_set_all_split = ',uv_set_all_split
                    if uv_set_all_split[0] != '':
                        uv_set_all_split_two = uv_set_all.split(':|:')
                        uv_set_object = uv_set_all_split_two[0]
                        uv_sets_linked_to_texture_split = uv_sets_linked_to_texture[0].split('.')
                        len_uv_sets_linked_to_texture = len(uv_sets_linked_to_texture)
                        if len_uv_sets_linked_to_texture > 0:
                            #print 'len_uv_set_address_linked_to_object > 0'
                            for uv_set_name in self.uv_set_name_to_address_dic:
                                #print ' '
                                #print 'uv_set_name = ',uv_set_name
                                address = self.uv_set_name_to_address_dic[uv_set_name]
                                #print 'address = ',address
                                address_split = address.split('.')
                                #print 'address_split = ',address_split
                                address_object = address_split[0]
                                address_address = address_split[1]
                                #print 'address_object = ',address_object
                                #print 'address_address = ',address_address
                                #print 'address = ',address
                                address_split = address.split('.')
                                address_object_raw = address_object
                                #address_object_raw = address_object[:-1]
                                #print 'address_object_raw = ',address_object_raw
                                uv_set_object_plus_address = uv_set_object + '.' + uv_sets_linked_to_texture_split[1]
                                #print 'uv_set_object_plus_address = ',uv_set_object_plus_address
                                address_object_plus_address = address_object + '.' + address_address
                                #print 'address_object_plus_address = ',address_object_plus_address
                                address_object_raw_plus_address = address_object_raw + '.' + address_address
                                #print 'address_object_raw_plus_address = ',address_object_raw_plus_address
                                if uv_set_object_plus_address == address_object_plus_address or uv_set_object_plus_address == address_object_raw_plus_address:
                                    #print address_object + ' == ' + uv_set_object + ' or ' + address_object_raw + ' == ' + uv_set_object
                                    #print 'uv_set_name = ',uv_set_name
                                    uv_set_name_split = uv_set_name.split(':|:')
                                    #print 'uv_set_name_split = ',uv_set_name_split
                                    name = uv_set_name_split[1]
                                    #print 'name = ',name
                                    if name != 'map1':
                                        #print 'name != map1'
                                        uv_set_name_split = uv_set_name.split(':|:')
                                        uv_set_name = uv_set_name_split[1]
                                        #print 'uv_set_name = ',uv_set_name
                                        #print 'setting '+ texture + ':|:' + uv_set_object + ':|:' + uv_set_name + ' to 1'
                                        self.uv_set_selection_status_dic[texture + ':|:' + uv_set_object + ':|:' + uv_set_name] = 1
                                        #print 'setting '+ texture + ':|:' + uv_set_object + ':|:map1 to 0'
                                        self.uv_set_selection_status_dic[texture + ':|:' + uv_set_object + ':|:' + 'map1'] = 0
                if empty_uv_set_detect == 2 and empty_uv_set_detect > 0:
                    #print 'two uv sets LINKED to texture and not zero uv sets'
                    for uv_set_linked_to_texture in uv_sets_linked_to_texture:
                        #print ' '
                        #print 'uv_set_linked_to_texture = ',uv_set_linked_to_texture
                        uv_set_linked_to_texture_split_star = uv_set_linked_to_texture.split('*')
                        #print 'uv_set_linked_to_texture_split_star = ',uv_set_linked_to_texture_split_star
                        if uv_set_linked_to_texture_split_star[0] != '':
                            uv_set_linked_to_texture_split_dot = uv_set_linked_to_texture.split('.')
                            uv_set_linked_to_texture_split_dot_object = uv_set_linked_to_texture_split_dot[0]
                            #print 'uv_set_linked_to_texture_split_dot_object = ',uv_set_linked_to_texture_split_dot_object
                            uv_set_linked_to_texture_split_dot_address = uv_set_linked_to_texture_split_dot[1]
                            #print 'uv_set_linked_to_texture_split_dot_address = ',uv_set_linked_to_texture_split_dot_address
                            uv_set_linked_to_texture_split_dot_object_split_dot = uv_set_linked_to_texture_split_dot_object[0].split('.')
                            len_uv_set_linked_to_texture_split_dot_object_split_dot = len(uv_set_linked_to_texture_split_dot_object_split_dot)
                            uv_set_linked_to_texture_compare = uv_set_linked_to_texture_split_dot_object + '.' + uv_set_linked_to_texture_split_dot_address
                            if len_uv_set_linked_to_texture_split_dot_object_split_dot > 0:
                                #print 'len_uv_set_linked_to_texture_object_split_dot > 0'
                                for uv_set_name_to_address_dic in self.uv_set_name_to_address_dic:
                                    #print '***'
                                    #print 'uv_set_name_to_address_dic = ',uv_set_name_to_address_dic
                                    uv_set_name_to_address_dic_address = self.uv_set_name_to_address_dic[uv_set_name_to_address_dic]
                                    #print 'uv_set_name_to_address_dic_address = ',uv_set_name_to_address_dic_address
                                    uv_set_name_to_address_dic_address_split = uv_set_name_to_address_dic_address.split('.')
                                    #uv_set_name_to_address_dic_address_split_colon = uv_set_name_to_address_dic_address.split(':|:')
                                    #uv_set_name_to_address_dic_address_set_name = uv_set_name_to_address_dic_address_split_colon[1]
                                    #print 'uv_set_name_to_address_dic_address_set_name = ',uv_set_name_to_address_dic_address_set_name
                                    #print 'uv_set_name_to_address_dic_address_split = ',uv_set_name_to_address_dic_address_split
                                    uv_set_name_to_address_dic_address_split_object = uv_set_name_to_address_dic_address_split[0]
                                    uv_set_name_to_address_dic_address_split_object_address = uv_set_name_to_address_dic_address_split[1]
                                    #print 'uv_set_name_to_address_dic_address_split_object = ',uv_set_name_to_address_dic_address_split_object
                                    #print 'uv_set_name_to_address_dic_address_split_object_address = ',uv_set_name_to_address_dic_address_split_object_address
                                    #print 'uv_sets_linked_to_texture = ', uv_sets_linked_to_texture
                                    uv_set_linked_to_texture_split_dot = uv_set_linked_to_texture.split('.')
                                    #print 'uv_set_linked_to_texture_split_dot = ',uv_set_linked_to_texture_split_dot
                                    uv_set_name_to_address_dic_compare = uv_set_name_to_address_dic_address_split_object + '.' + uv_set_name_to_address_dic_address_split_object_address
                                    #print 'uv_set_linked_to_texture_compare = ',uv_set_linked_to_texture_compare
                                    #print 'uv_set_name_to_address_dic_compare = ',uv_set_name_to_address_dic_compare
                                    if uv_set_linked_to_texture_compare == uv_set_name_to_address_dic_compare:
                                        #print 'MATCH'
                                        #print 'uv_set_name_to_address_dic = ',uv_set_name_to_address_dic
                                        uv_set_name_to_address_dic_split = uv_set_name_to_address_dic.split(':|:')
                                        #print 'uv_set_name_to_address_dic_split = ',uv_set_name_to_address_dic_split
                                        UV_set_name_dic = uv_set_name_to_address_dic_split[1]
                                        #print 'UV_set_name_dic = ',UV_set_name_dic
                                        if UV_set_name_dic != 'map1':
                                            #print 'UV_set_name_dic != map1'
                                            #UV_set_name_dic_split = UV_set_name_dic.split(':|:')
                                            #UV_set_name_dic_split = UV_set_name_dic_split[1]
                                            #print 'uv_set_name = ',uv_set_name
                                            #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
                                            #print 'setting '+ texture + ':|:' + uv_set_name_to_address_dic_address_split_object + ':|:' + UV_set_name_dic + ' to 1'
                                            self.uv_set_selection_status_dic[texture + ':|:' + uv_set_name_to_address_dic_address_split_object + ':|:' + UV_set_name_dic] = 1
                                            #print 'setting '+ texture + ':|:' + uv_set_name_to_address_dic_address_split_object + ':|:map1 to 0'
                                            self.uv_set_selection_status_dic[texture + ':|:' + uv_set_name_to_address_dic_address_split_object + ':|:' + 'map1'] = 0
        for uv_set_all in self.uv_sets_all:
            #print 'uv_set_all = ',uv_set_all
            empty_uv_set_detect = len(uv_set_all)
            #print 'empty_uv_set_detect = ',empty_uv_set_detect
            if empty_uv_set_detect != 2:
                #print 'empty_uv_set_detect != 2'
                uv_set_all_split = uv_set_all.split('*')
                if uv_set_all_split[0] != '':
                    #print 'uv_set_all_split[0] not empty'
                    for texture in self.all_textures:
                        #print 'texture = ',texture
                        dic_string_check = texture + ':|:' + uv_set_all
                        #print 'dic_string_check = ',dic_string_check
                        if dic_string_check not in self.uv_set_selection_status_dic:
                            #print 'dic_string_check not in self.uv_set_selection_status_dic'
                            #print 'adding it and setting it to 0'
                            self.uv_set_selection_status_dic[texture + ':|:' + uv_full] = 0
        #print 'C initial_uv_set_name_to_address_dic_eval self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        for us_set_carry_over in self.uv_set_selection_status_dic_state_change:
            state = self.uv_set_selection_status_dic_state_change[us_set_carry_over]
            us_set_carry_over_split = us_set_carry_over.split(':|:')
            us_set_carry_over_texture = us_set_carry_over_split[0]
            us_set_carry_over_object = us_set_carry_over_split[1]
            us_set_carry_uv_set = us_set_carry_over_split[2]
            if state == str(1) or state == 1:
                self.uv_set_selection_status_dic[us_set_carry_over] = 1
                if us_set_carry_uv_set != 'map1':
                    self.uv_set_selection_status_dic[us_set_carry_over_texture + ':|:' + us_set_carry_over_object + ':|:' + 'map1'] = 0
        #print '1 initial_uv_set_name_to_address_dic_eval self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        if os.path.isfile(self.file_name_on_disk) and os.access(self.file_name_on_disk, os.R_OK):
            #print "File exists and is readable/there"
            self.read_UV_sets_state_file_from_disk()
            #print '** self.uv_set_selection_status_dic_from_disk = ', self.uv_set_selection_status_dic_from_disk
            for uv_set_selection_status in self.uv_set_selection_status_dic:
                uv_set_selection_status_split = uv_set_selection_status.split(':|:')
                uv_set_selection_status_texture = uv_set_selection_status_split[0]
                uv_set_selection_status_texture_linked_UV_sets = cmds.uvLink( query = True, texture = uv_set_selection_status_texture)
                uv_set_selection_status_texture_linked_UV_sets_size = len(uv_set_selection_status_texture_linked_UV_sets)
                #if uv_set_selection_status_texture_linked_UV_sets_size == 0:
                for uv_set_selection_from_disk in self.uv_set_selection_status_dic_from_disk:
                    if uv_set_selection_status == uv_set_selection_from_disk:
                        uv_set_selection_status_from_disk = self.uv_set_selection_status_dic_from_disk[uv_set_selection_status]
                        self.uv_set_selection_status_dic[uv_set_selection_status] = uv_set_selection_status_from_disk
        #else:
            #print self.file_name_on_disk + ' does not exist'
        #print 'after readiing file self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
#---------- UV set selection methods ----------

    def item_press(self,item):
        #print 'item_press()'
        if self.centric_state_text == 'texture-centric':
        #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
            self.deselect_QListWidget(self.list_widget_right)
            self.texture_linked_uv_sets = []
            self.selected_item_text = item.text()
            #print 'self.selected_item_text = ',self.selected_item_text
            self.activate_right_listWidget()
            for file in self.file_to_file_path_dic:
                #print 'file = ',file
                item = self.file_to_file_path_dic[file]
                #print 'item = ',item
                if item == self.selected_item_text:
                    #print item + ' ==' + self.selected_item_text
                    self.selected_item_text = file
            uv_set_addresses_linked_to_selected_texture = cmds.uvLink( query = True, texture = self.selected_item_text) or []
            #print '* uv_set_addresses_linked_to_selected_texture = ',uv_set_addresses_linked_to_selected_texture
            number_of_linked_uv_sets = len(uv_set_addresses_linked_to_selected_texture)
            #print '* number_of_linked_uv_sets = ',number_of_linked_uv_sets
            if number_of_linked_uv_sets == 0:
                #print '* number of linked UV sets = 0, reading file'
                linked_UV_sets = []
                #print '* self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
                for uv_set in self.uv_set_selection_status_dic:
                    #print '* uv_set = ',uv_set
                    state = self.uv_set_selection_status_dic[uv_set]
                    #print '* state = ',state
                    if state == str(1) or state == 1:
                        #print 'state = 1, adding to linked_UV_sets'
                        linked_UV_sets.append(uv_set)
                #print '* linked_UV_sets = ',linked_UV_sets
                for linked_UV_set in linked_UV_sets:
                    #print '* linked_UV_set = ',linked_UV_set
                    #print '* self.uv_set_name_to_address_dic = ',self.uv_set_name_to_address_dic
                    linked_UV_set_split = linked_UV_set.split(':|:')
                    linked_UV_set_adjusted = linked_UV_set_split[1] + ':|:' + linked_UV_set_split[2]
                    #print 'linked_UV_set_adjusted = ',linked_UV_set_adjusted
                    address = self.uv_set_name_to_address_dic[linked_UV_set_adjusted]
                    #print '* address = ',address
                    uv_set_addresses_linked_to_selected_texture.append(address)
                    #print '* after file read, uv_set_addresses_linked_to_selected_texture = ',uv_set_addresses_linked_to_selected_texture
            for uv_set_name_to_address in self.uv_set_name_to_address_dic:
                #print '* uv_set_name_to_address = ',uv_set_name_to_address
                uv_set_address = self.uv_set_name_to_address_dic[uv_set_name_to_address]
                #print '* uv_set_address = ',uv_set_address
                if uv_set_address in uv_set_addresses_linked_to_selected_texture:
                    #print '* uv_set_address = ',uv_set_address
                    #print '* uv_set_address in uv_set_addresses_linked_to_selected_texture'
                    #print '* appending ' + uv_set_address + ' to ' + 'self.texture_linked_uv_sets'
                    self.texture_linked_uv_sets.append(uv_set_name_to_address)
            #print '* self.texture_linked_uv_sets = ',self.texture_linked_uv_sets
            self.update_right_listWidget()
        if self.centric_state_text == 'UV-centric':
            self.selected_item_text = item.text()
            self.activate_right_listWidget()
            if '*' not in self.selected_item_text:
                self.selected_item_text = self.selected_item_text.replace(' ','')
                i = 0
                while i < self.number_of_items_in_left_listWidget:
                    item = self.list_widget_left.item(i)
                    item_text = item.text()
                    empty_uv_set_detect = len(item_text)
                    item_text_split = item_text.split('*')
                    if '*' in item_text:
                        item_object  = item_text_split[1]
                        item_object  = item_object[1:]
                    if item_text_split[0] != '':
                        if item_text == self.selected_item_text:
                            combined_object_uv_set_name = (self.selected_item_text + ':|:' + (item_object  + ':|:' + item_text))
                            selected_uv_set_address = self.uv_set_name_to_address_dic[combined_object_uv_set_name]
                            self.textures_linked_to_selected_uv_set = cmds.uvLink( query=True, uvSet = selected_uv_set_address)
                    i = i + 1
                self.update_right_listWidget()

    def deselect_item(self,selected_item):
        selected_item.setSelected(False)

    def update_right_listWidget(self):
        #print 'update_right_listWidget()'
        #print 'XX self.uv_set_selection_status_dic = ', self.uv_set_selection_status_dic
        if self.centric_state_text == 'texture-centric':
            self.unlock_right_QListWidget()
            it = 0
            #print 'XX self.number_of_items_in_right_listWidget = ',self.number_of_items_in_right_listWidget
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item_text = item.text()
                #print 'XX item_text = ',item_text
                empty_uv_set_detect = len(item_text)
                #print 'empty_uv_set_detect = ',empty_uv_set_detect
                if empty_uv_set_detect != 2:
                    item_text_split = item_text.split('*')
                    #print 'item_text_split = ',item_text_split
                    if '*' in item_text:
                        item.setTextColor(QtGui.QColor("#c4bebe"))
                        item_object = item_text_split[1]
                        item_object = item_object[1:]
                        #print 'item_object = ',item_object
                    if item_text_split[0] != '':
                        #print item_text_split[0] + ' is not empty'
                        num_of_spaces = len(self.spacer)
                        #print 'num_of_spaces = ',num_of_spaces
                        item_text = item_text[num_of_spaces:]
                        #print 'item_text = ',item_text
                        combined_object_uv_set_name = (self.selected_item_text + ':|:' + (item_object + ':|:' + item_text))
                        #print 'combined_object_uv_set_name = ',combined_object_uv_set_name
                        item_text_selection_status = self.uv_set_selection_status_dic[combined_object_uv_set_name]
                        #print 'XX item_text_selection_status = ',item_text_selection_status
                        #print 'item_text_selection_status = ',item_text_selection_status
                        if item_text_selection_status == str(1) or item_text_selection_status == 1:
                            #print 'XX item_text_selection_status = 1, setting ' + str(item) + ' to selected'
                            item.setSelected(True)
                            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                        if item_text_selection_status == str(0) or item_text_selection_status == 0:
                            #print 'XX item_text_selection_status = 0, setting ' + str(item) + ' to deselected'
                            item.setSelected(False)
                it = it + 1
            self.texture_to_object_color_adjust()
        if self.centric_state_text == 'UV-centric':
            self.selected_right_list_textures = []
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                item_text = item.text()
                for file in self.file_to_file_path_dic:
                    item_sub = self.file_to_file_path_dic[file]
                    if item_sub == item_text:
                        item_text = file
                selected_index = self.list_widget_left.selectedIndexes()
                #print 'selected_index = ',selected_index
                selected_row = 0
                for ind in selected_index:
                    selected_row = ind.row()
                i = 0
                #print 'selected_row = ',selected_row
                if selected_row != 0:
                    while i < self.number_of_items_in_left_listWidget:
                        item_uv_set = self.list_widget_left.item(i)
                        item_uv_set_text = item_uv_set.text()
                        item_uv_set_text = item_uv_set_text.replace(' ','')
                        item_uv_set_text_split = item_uv_set_text.split('*')
                        if '*' in item_uv_set_text:
                            item_object = item_uv_set_text_split[1]
                        if item_uv_set_text_split[0] != '':
                            if i == selected_row:
                                if item_uv_set_text == self.selected_item_text:
                                    item_text_selection_status_dic_key = (item_text + ':|:' + (item_object  + ':|:' + self.selected_item_text))
                                    item_text_selection_status = self.uv_set_selection_status_dic[item_text_selection_status_dic_key]
                                    if item_text_selection_status == str(0) or item_text_selection_status == 0:
                                        item.setSelected(False)
                                    if item_text_selection_status == str(1) or item_text_selection_status == 1:
                                        item.setSelected(True)
                                        item_text = item.text()
                                        self.selected_right_list_textures.append(item_text)
                                        combined_selected_item_text = item_object + ':|:' + self.selected_item_text
                                        selected_item_text_split = combined_selected_item_text.split(':|:')
                                        selected_item_text_uv_set = selected_item_text_split[1]
                                        selected_item_text_uv_set = selected_item_text_uv_set.replace(' ','')
                                        if selected_item_text_uv_set == 'map1':
                                            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                        i = i + 1
                it = it + 1
                #self.texture_to_object_color_adjust()

    def right_listWidget_selection_eval(self):
        #print ' '
        #print 'right_listWidget_selection_eval()'
        if self.centric_state_text == 'texture-centric':
            #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
            selected_uv_sets_pointers = self.list_widget_right.selectedItems()
            #print 'selected_uv_sets_pointers = ',selected_uv_sets_pointers
            uv_set_pointers = []
            selected_right_pointers = []
            selected_uv_set_names = []
            uv_set_object_name_dic = {}
            uv_set_pointer_dic = {}
            it = 0
            size_of_left_selection = len(self.selected_item_text)
            #print 'size_of_left_selection = ',size_of_left_selection
            if size_of_left_selection > 0:
                while it < self.number_of_items_in_right_listWidget:
                    item = self.list_widget_right.item(it)
                    #print 'item = ',item
                    uv_set_pointers.append(item)
                    item_text = item.text()
                    #print 'item_text = ',item_text
                    item_text_split = item_text.split('*')
                    #print 'item_text_split = ',item_text_split
                    if '*' in item_text:
                        #print '* in item_text'
                        item_object = item_text_split[1]
                        item_object = item_object[1:]
                    if item_text_split[0] != '':
                        #print item_text_split[0] + ' != ' + ' empty'
                        uv_set_split = item_text.split(':|:')
                        uv_set_object_name = item_object
                        uv_set_object_name_dic[item_text] = uv_set_object_name
                    it = it + 1
                for selected_uv_set_pointer in selected_uv_sets_pointers:
                    selected_right_pointers.append(selected_uv_set_pointer)
                    it_text = selected_uv_set_pointer.text()
                    it_text = it_text.replace(' ','')
                    #print 'it_text = ',it_text
                    selected_uv_set_names.append(it_text)
                    #print 'selected_uv_set_names = ',selected_uv_set_names
                    selected_index = self.list_widget_right.selectedIndexes()
                    #print 'selected_index = ',selected_index
                    for ind in selected_index:
                        selected_row = ind.row()
                        #print 'selected_row = ',selected_row
                    i = 0
                    for uv_set_pointer in uv_set_pointers:
                        uv_set_text = uv_set_pointer.text()
                        #print 'uv_set_text = ',uv_set_text
                        item_text_split = uv_set_text.split('*')
                        if '*' in uv_set_text:
                            #print ' * in ',uv_set_text
                            item_object = item_text_split[1]
                            item_object = item_object[1:]
                            #print 'item_object = ',item_object
                        if item_text_split[0] != '':
                            #print ' i = ',i
                            #print 'selected_row = ',selected_row
                            if i == selected_row:
                                #print 'i == ',selected_row
                                #print 'selected_uv_set_object_name = item_object'
                                selected_uv_set_object_name = item_object
                        i = i + 1
                    for uv_set_pointer in uv_set_pointers:
                        #print 'uv_set_pointer = ',uv_set_pointer
                        if str(uv_set_pointer) != str(selected_uv_set_pointer):
                            #print str(uv_set_pointer) + ' != ' + str(selected_uv_set_pointer)
                            uv_set_name = uv_set_pointer.text()
                            #print 'uv_set_name = ',uv_set_name
                            uv_set_name = uv_set_name.replace(' ','')
                            #print 'uv_set_name = ',uv_set_name
                            item_text_split = uv_set_name.split('*')
                            #print 'item_text_split = ',item_text_split
                            if '*' in uv_set_name:
                                item_object = item_text_split[1]
                                #print 'item_object = ',item_object
                            if item_text_split[0] != '':
                                if item_object == selected_uv_set_object_name:
                                    #print item_object + ' == ' + selected_uv_set_object_name
                                    uv_set_pointer.setSelected(False)
                                    #print str(uv_set_pointer) + 'setSelected to ' + 'false'
                                    self.uv_set_selection_status_dic[self.selected_item_text + ':|:' + item_object + ':|:' + uv_set_name] = 0
                                    #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
                    self.unlock_right_QListWidget()
                    #print str(selected_uv_set_pointer) + ' setSelected to ' + 'true'
                    selected_uv_set_pointer.setSelected(True)
                    it_text_combined =  selected_uv_set_object_name + ':|:' + it_text
                    #print 'it_text_combined = ',it_text_combined
                    self.uv_set_selection_status_dic[self.selected_item_text + ':|:' + it_text_combined] = 1
                    #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
            selected_uv_sets_pointers = self.list_widget_right.selectedItems()
            #print 'selected_uv_sets_pointers = ',selected_uv_sets_pointers
            for selected_uv_sets_pointer in selected_uv_sets_pointers:
                pointer_text = selected_uv_sets_pointer.text()
                #print 'pointer_text = ',pointer_text
                selected_uv_sets_pointer.setFlags(selected_uv_sets_pointer.flags() & ~Qt.ItemIsEnabled)
            self.link_texture_to_uv_set()
        #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        if self.centric_state_text == 'UV-centric':
            size_of_left_selection = len(self.selected_item_text)
            if size_of_left_selection > 0:
                self.selected_item_text = self.selected_item_text.replace(' ','')
                selected_index = self.list_widget_left.selectedIndexes()
                for ind in selected_index:
                    selected_row = ind.row()
                i = 0
                while i < self.number_of_items_in_left_listWidget:
                    uv_set_sub = self.list_widget_left.item(i)
                    uv_set_sub_text = uv_set_sub.text()
                    uv_set_sub_text = uv_set_sub_text.replace(' ','')
                    item_text_sub_split = uv_set_sub_text.split('*')
                    if '*' in uv_set_sub_text:
                        sub_item_object = item_text_sub_split[1]
                    if item_text_sub_split[0] != '':
                        if i == selected_row:
                            selected_uv_set_object_name = sub_item_object
                            if uv_set_sub_text == self.selected_item_text:
                                self.selected_item_text = selected_uv_set_object_name + ':|:' + self.selected_item_text
                    i = i + 1
                selected_item_text_split = self.selected_item_text.split(':|:')
                selected_item_text_object = selected_item_text_split[0]
                selected_item_text_uv_set = selected_item_text_split[1]
                self.selected_items_right_listWidget()
                for selected_item_right_text in self.selected_items_right_text:
                    for file in self.file_to_file_path_dic:
                        item_sub = self.file_to_file_path_dic[file]
                        if item_sub == selected_item_right_text:
                            selected_item_right_text = file
                    self.uv_set_selection_status_dic[selected_item_right_text + ':|:' + self.selected_item_text] = 1
                    for uv_set_selection in self.uv_set_selection_status_dic:
                        uv_set_selection_split = uv_set_selection.split(':|:')
                        uv_set_selection_texture = uv_set_selection_split[0]
                        for file in self.file_to_file_path_dic:
                            item_sub = self.file_to_file_path_dic[file]
                            if item_sub == uv_set_selection_texture:
                                uv_set_selection_texture = file
                        uv_set_selection_object = uv_set_selection_split[1]
                        uv_set = uv_set_selection_split[2]
                        if uv_set_selection_object == selected_item_text_object:
                            if uv_set_selection_texture == selected_item_right_text:
                                if uv_set != selected_item_text_uv_set:
                                    self.uv_set_selection_status_dic[uv_set_selection] = 0
                for texture in self.all_textures:
                    if texture not in self.selected_items_right_text:
                        for file in self.file_to_file_path_dic:
                            item_sub = self.file_to_file_path_dic[file]
                            if item_sub == texture:
                                texture = file
                        self.uv_set_selection_status_dic[texture + ':|:' + self.selected_item_text] = 0
                selected_dics = []
                unselected_dics = []
                for uv_set_selection in self.uv_set_selection_status_dic:
                    selection_status = self.uv_set_selection_status_dic[uv_set_selection]
                    if selection_status == 1:
                        if uv_set_selection not in selected_dics:
                            selected_dics.append(uv_set_selection)
                    if selection_status == 0:
                        if uv_set_selection not in unselected_dics:
                            unselected_dics.append(uv_set_selection)
                for unselected_uv_set in unselected_dics:
                    uv_set_selection_split = unselected_uv_set.split(':|:')
                    unselected_texture = uv_set_selection_split[0]
                    for file in self.file_to_file_path_dic:
                        item_sub = self.file_to_file_path_dic[file]
                        if item_sub == unselected_texture:
                            unselected_texture = file
                    unselected_object = uv_set_selection_split[1]
                    unselected_uv = uv_set_selection_split[2]
                    map1_object = ''
                    if unselected_uv == 'map1':
                        unselected_uv_set_map1 = unselected_uv_set
                        map1_object = unselected_object
                        no_select = 1
                        for selected_dic in selected_dics:
                            selected_dic_split = selected_dic.split(':|:')
                            selected_dic_texture = selected_dic_split[0]
                            for file in self.file_to_file_path_dic:
                                item_sub = self.file_to_file_path_dic[file]
                                if item_sub == selected_dic_texture:
                                    selected_dic_texture = file
                            selected_dic_object = selected_dic_split[1]
                            selected_dic_uv_set = selected_dic_split[2]
                            if selected_dic_texture == unselected_texture:
                                if selected_dic_object == map1_object:
                                    no_select = 0
                        if no_select == 1:
                            self.uv_set_selection_status_dic[unselected_uv_set_map1] = 1
                selected_item_text_split = self.selected_item_text.split(':|:')
                uv_set = selected_item_text_split[1]
                if selected_item_text_uv_set == 'map1':
                    selected_right_pointers = self.list_widget_right.selectedItems()
                    for pointer in selected_right_pointers:
                        pointer.setFlags(pointer.flags() & ~Qt.ItemIsEnabled)
                self.link_texture_to_uv_set()
        #print 'end right_listWidget_selection_eval self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic

    def link_texture_to_uv_set(self):
        #print ' '
        #print ' '
        #print 'link_texture_to_uv_set()'
        #print 'start link_texture_to_uv_set uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        for uv_set_selection in self.uv_set_selection_status_dic:
            #print ' '
            #print 'x'
            #print ' '
            #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
            #print 'uv_set_selection = ',uv_set_selection
            selection_status = self.uv_set_selection_status_dic[uv_set_selection]
            #print 'selection_status = ',selection_status
            if selection_status == 0:
                #print 'selection_status equals 0'
                uv_set_selection_split = uv_set_selection.split(':|:')
                #print 'uv_set_selection_split = ',uv_set_selection_split
                texture = uv_set_selection_split[0]
                #print 'texture = ',texture
                for file in self.file_to_file_path_dic:
                    #print 'file = ',file
                    item_sub = self.file_to_file_path_dic[file]
                    #print 'item_sub = ',item_sub
                    #print 'texture = ',texture
                    if item_sub == texture:
                        #print 'item_sub = ',item_sub
                        texture = file
                        #print 'texture = ',texture
                object = uv_set_selection_split[1]
                #print 'object = ',object
                uv_set = uv_set_selection_split[2]
                #print 'uv_set = ',uv_set
                texture_linked_uv_set_address = self.uv_set_name_to_address_dic[object + ':|:' + uv_set]
                #print 'texture_linked_uv_set_address = ',texture_linked_uv_set_address
                #print '** breaking connection between ' + str(texture_linked_uv_set_address) + ' and ' + texture
                cmds.uvLink(b = True, uvSet = texture_linked_uv_set_address,texture = texture)
            if selection_status == 1:
                #print 'selection_status = 1'
                uv_set_selection_split = uv_set_selection.split(':|:')
                #print 'uv_set_selection_split = ',uv_set_selection_split
                texture = uv_set_selection_split[0]
                #print 'texture = ',texture
                for file in self.file_to_file_path_dic:
                    #print 'file = ',file
                    item_sub = self.file_to_file_path_dic[file]
                    #print 'item_sub = ',item_sub
                    #print 'texture = ',texture
                    if item_sub == texture:
                        #print 'item_sub = ',item_sub
                        texture = file
                        #print 'texture = ',texture
                object = uv_set_selection_split[1]
                #print 'object = ',object
                uv_set = uv_set_selection_split[2]
                #print 'uv_set = ',uv_set
                #print 'self.uv_set_name_to_address_dic = ',self.uv_set_name_to_address_dic
                texture_linked_uv_set_address = self.uv_set_name_to_address_dic[object + ':|:' + uv_set]
                texture_linked_uv_set_address_split = texture_linked_uv_set_address.split('.')
                #print 'texture_linked_uv_set_address_split = ',texture_linked_uv_set_address_split
                mesh_name = texture_linked_uv_set_address_split[0]
                mesh_name_minus_post_number = mesh_name[:-1]
                #print 'mesh_name_minus_post_number = ',mesh_name_minus_post_number
                texture_linked_uv_set_address_minus_post = mesh_name_minus_post_number + '.' + texture_linked_uv_set_address_split[1] + '.' + texture_linked_uv_set_address_split[2]
                #print '** texture_linked_uv_set_address = ',texture_linked_uv_set_address
                #print 'linking ' + str(texture_linked_uv_set_address) + ' to ' + texture
                cmds.uvLink(make = True, uvSet = texture_linked_uv_set_address,texture = texture)
                texture_linked_uv_set_address_minus_post_exists = cmds.objExists(texture_linked_uv_set_address_minus_post)
                #print 'texture_linked_uv_set_address_minus_post_exists = ',texture_linked_uv_set_address_minus_post_exists
                if texture_linked_uv_set_address_minus_post_exists == 1:
                    #print 'linking ' + str(texture_linked_uv_set_address_minus_post) + ' to ' + texture
                    cmds.uvLink(make = True, uvSet = texture_linked_uv_set_address_minus_post,texture = texture)
        self.write_UV_sets_state_file_to_disk()
        #print 'end link_texture_to_uv_set uv_set_selection_status_dic = ',self.uv_set_selection_status_dic

    def texture_to_object_color_adjust(self):
        #print 'texture_to_object_color_adjust'
        linked_objects_to_texture_dic = {}
        object_material_string = ''
        self.list_widget_texture_info.clear()
        if self.centric_state_text == 'texture-centric':
            selected_textures = []
            selected_texture = self.selected_item_text
            connected_materials = self.connected_materials(selected_texture)
            #print 'connected_materials = ',connected_materials
            cmds.select(clear = True)
            object_material_string = ''
            assigned_objects = []
            for material in connected_materials:
                #print 'material = ',material
                material_and_plugs = material
                material_split = material.split('.')
                material = material_split[0]
                current_selection = cmds.ls(selection = True) or []
                cmds.hyperShade(objects = material)
                material_assigned_objects = (cmds.ls(selection = True)) or []
                number_of_selected_objects = len(material_assigned_objects)
                if number_of_selected_objects > 0:
                    for material_assigned_object in material_assigned_objects:
                        assigned_objects.append(material_assigned_object)
                for object in material_assigned_objects:
                    if '.f[' in object:
                        object_split= object.split('.f[')
                        object = object_split[0]
                    object_material_string = object_material_string + object + ': ' + material_and_plugs + '        '
            linked_objects_to_texture_dic[selected_texture] = assigned_objects
            object_material_string = object_material_string[:-4]
            texture_information_string = object_material_string
            texture_information_string_size = len(texture_information_string)
            if texture_information_string_size == 0:
                connected_materials_size = len(connected_materials)
                if connected_materials_size == 0:
                    texture_information_string = 'texture linked to no material and used by no object'
                else:
                    texture_information_string = str(connected_materials[0]) + ' * texture used by no object '
            #print 'texture_information_string = ', texture_information_string
            #print 'adding ' + texture_information_string + ' to GUI'
            self.list_widget_texture_info.addItem(texture_information_string)
            it = 0
            made_object_highlight = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item_text = item.text()
                if item_text == '':
                    item.setFlags(item.flags() | Qt.ItemIsEnabled)
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                item.setTextColor(QtGui.QColor("#515151"))
                if made_object_highlight == 1:
                    if '*' not in item_text:
                        item.setTextColor(QtGui.QColor('#515b8c'))
                for linked_object_to_texture_dic in linked_objects_to_texture_dic:
                    if linked_object_to_texture_dic == selected_texture:
                        objects = linked_objects_to_texture_dic[selected_texture]
                        for object in objects:
                            if '*' in item_text:
                                made_object_highlight = 0
                            if '.f[' in object:
                                object_split = object.split('.f[')
                                object = object_split[0]
                            if 'Shape' in object:
                                object_split = object.split('Shape')
                                object = object_split[0]
                            if 'Shape' in item_text:
                                item_text_split = item_text.split('Shape')
                                item_text = item_text_split[0]
                            if object in item_text and '*' in item_text:
                                item.setTextColor(QtGui.QColor('#7c98cf'))
                                made_object_highlight = 1
                            item_text_no_star = item_text.replace('*','')
                            item_text_no_star = item_text_no_star.replace(' ','')
                            for object in objects:
                                object = object.replace('Shape','')
                                if item_text_no_star == object:
                                    made_object_highlight = 1
                it = it + 1
        if self.centric_state_text == 'UV-centric':
            selected_textures = []
            connected_materials_all = []
            texture_information_string = ''
            #print 'self.selected_right_list_textures = ',self.selected_right_list_textures
            number_of_selected_right_list_textures = len(self.selected_right_list_textures)
            i = 0
            for selected_texture in self.selected_right_list_textures:
                #print ' '
                #print 'selected_texture = ',selected_texture
                connected_materials = self.connected_materials(selected_texture)
                #print 'connected_materials  = ',connected_materials
                for material in connected_materials:
                    if material not in connected_materials_all:
                        connected_materials_all.append(selected_texture + ':' + material)
                cmds.select(clear = True)
                number_of_materials_assigned = len(connected_materials_all)
                if number_of_materials_assigned == 0:
                    if i == 0:
                        texture_information_string = selected_texture + ':texture linked to no material'
                    else:
                        texture_information_string = texture_information_string + '        ' + selected_texture + ':texture linked to no material'
                i = i + 1
            object_material_string = ''
            #print 'connected_materials_all  = ',connected_materials_all
            assigned_objects = []
            for material in connected_materials_all:
                #print '---'
                #print 'material = ',material
                material_and_plugs = material
                material_texture_split = material.split(':')
                #print 'material_texture_split = ',material_texture_split
                material_pure = material_texture_split[1]
                #print 'material_pure = ',material_pure
                material_pure_and_plugs = material_pure
                #print 'material_pure_and_plugs = ',material_pure_and_plugs
                material_pure_and_plugs_split = material_pure_and_plugs.split('.')
                #print 'material_pure_and_plugs_split = ',material_pure_and_plugs_split
                material_pure = material_pure_and_plugs_split[0]
                #print 'material_pure = ',material_pure
                current_selection = cmds.ls(selection = True) or []
                #print 'current_selection = ',current_selection
                cmds.hyperShade(objects = material_pure)
                material_assigned_objects = (cmds.ls(selection = True)) or []
                #print 'material_assigned_objects = ',material_assigned_objects
                number_of_selected_objects = len(material_assigned_objects)
                if number_of_selected_objects > 0:
                    for material_assigned_object in material_assigned_objects:
                        assigned_objects.append(material_assigned_object)
                #print 'assigned_objects = ',assigned_objects
                i = 0
                texture_information_string = material_and_plugs
                for object in material_assigned_objects:
                    if '.f[' in object:
                        object_split= object.split('.f[')
                        object = object_split[0]
                    #print 'object = ',object
                    if i == (number_of_selected_objects - 1):
                        object_material_string = object_material_string + object + ' : ' + material_and_plugs + '        '
                    #print 'object_material_string = ',object_material_string
                    #print 'assigned_objects = ',assigned_objects
                    linked_objects_to_texture_dic[selected_texture] = assigned_objects
                    #print 'linked_objects_to_texture_dic = ',linked_objects_to_texture_dic
                    #object_material_string = object_material_string[:-4]
                    #print 'object_material_string = ',object_material_string
                    texture_information_string = object_material_string
                    texture_information_string_size = len(texture_information_string)
                    #print 'texture_information_string_size = ',texture_information_string_size
                    if texture_information_string_size == 0:
                        connected_materials_size = len(connected_materials)
                        if connected_materials_size == 0:
                            texture_information_string = 'texture linked to no material and used by no object'
                        else:
                            texture_information_string = selected_texture + ':' + str(connected_materials[0]) + ' * texture used by no object '
                    i = i + 1
            self.list_widget_texture_info.addItem(texture_information_string)
        it = 0
        while it < self.number_of_items_in_right_listWidget:
            item = self.list_widget_right.item(it)
            item_text = item.text()
            for linked_object_to_texture_dic in linked_objects_to_texture_dic:
                if linked_object_to_texture_dic == selected_texture:
                    objects = linked_objects_to_texture_dic[selected_texture]
            it = it + 1
        it = 0
        while it < self.list_widget_texture_info.count():
            item = self.list_widget_texture_info.item(it)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            it = it + 1
        cmds.select(clear = True)
        self.deactivate_empty_lines()
        #print 'END texture_to_object_color_adjust'

    def connected_materials(self,selected_texture):
        #print '-- connected_materials --'
        #print 'selected_texture = ',selected_texture
        material_types = ['lambert','phong','blinn','surfaceShader','VRayMtl','layeredTexture','VRayBlendMtl','VRayBumpMtl']
        bad_connection_names_list = ['hyperShadePrimaryNodeEditorSavedTabsInfo','materialInfo','defaultShaderList1','defaultTextureList1','initialShadingGroup','particleCloud','initialParticleSE','message']
        connected_materials = []
        connected_shading_engines = []
        material_plug_string_links = []
        for file in self.file_to_file_path_dic:
            item_sub = self.file_to_file_path_dic[file]
            if item_sub == selected_texture:
                selected_texture = file
        selected_texture_connections = cmds.listConnections(selected_texture,source = False) or []
        #print 'selected_texture_connections = ',selected_texture_connections
        selected_texture_connections_clean = list(selected_texture_connections)
        for selected_texture_connection in selected_texture_connections:
            #print 'selected_texture_connection = ',selected_texture_connection
            if selected_texture_connection in bad_connection_names_list:
                #print 'removing ', selected_texture_connection
                selected_texture_connections_clean.remove(selected_texture_connection)
        #print 'selected_texture_connections_clean = ',selected_texture_connections_clean
        material_plug_string_links = list(selected_texture_connections_clean)
        material_plug_string_links.append(selected_texture)
        for connection in selected_texture_connections_clean:
            connections_0 = cmds.listConnections(connection,source = False) or []
            for connection in connections_0:
                material_plug_string_links.append(connection)
                connection_type = cmds.nodeType(connection)
                if connection_type == 'shadingEngine':
                    if connection not in connected_shading_engines:
                        connected_shading_engines.append(connection)
                else:
                    connections_1 = cmds.listConnections(connection,source = False) or []
                    #print 'connections_1 = ',connections_1
                    for connection in connections_1:
                        material_plug_string_links.append(connection)
                        connection_type = cmds.nodeType(connection)
                        if connection_type == 'shadingEngine':
                            if connection not in connected_shading_engines:
                                connected_shading_engines.append(connection)
                        else:
                            connections_2 = cmds.listConnections(connection,source = False) or []
                            #print 'connections_2 = ',connections_2
                            for connection in connections_2:
                                material_plug_string_links.append(connection)
                                connection_type = cmds.nodeType(connection)
                                if connection_type == 'shadingEngine':
                                    if connection not in connected_shading_engines:
                                        connected_shading_engines.append(connection)
                                else:
                                    connections_3 = cmds.listConnections(connection,source = False) or []
                                    #print 'connections_3 = ',connections_3
                                    for connection in connections_3:
                                        material_plug_string_links.append(connection)
                                        connection_type = cmds.nodeType(connection)
                                        if connection_type == 'shadingEngine':
                                            if connection not in connected_shading_engines:
                                                connected_shading_engines.append(connection)
                                        else:
                                            connections_4 = cmds.listConnections(connection,source = False) or []
                                            #print 'connections_4 = ',connections_4
                                            for connection in connections_4:
                                                material_plug_string_links.append(connection)
                                                connection_type = cmds.nodeType(connection)
                                                if connection_type == 'shadingEngine':
                                                    if connection not in connected_shading_engines:
                                                        connected_shading_engines.append(connection)
                                                else:
                                                    connections_5 = cmds.listConnections(connection,source = False) or []
                                                    #print 'connections_5 = ',connections_5
                                                    for connection in connections_5:
                                                        material_plug_string_links.append(connection)
                                                        connection_type = cmds.nodeType(connection)
                                                        if connection_type == 'shadingEngine':
                                                            if connection not in connected_shading_engines:
                                                                connected_shading_engines.append(connection)
        #print 'connected_shading_engines = ',connected_shading_engines
        material_plug_string_strings = []
        for shading_engine in connected_shading_engines:
            #print ' '
            #print 'xx'
            #print ' '
            #print 'shading_engine = ',shading_engine
            #print 'erasing material_plug_string_strings'
            shading_engine_connections = cmds.listConnections(shading_engine,destination = False) or []
            #print 'shading_engine_connections = ',shading_engine_connections
            for shading_engine_connection_0 in shading_engine_connections:
                #print 'shading_engine_connection_0 = ',shading_engine_connection_0
                shading_engine_connection_0_type = cmds.nodeType(shading_engine_connection_0)
                if shading_engine_connection_0_type in material_types:
                    shading_engine_connections_1 = cmds.listConnections(shading_engine_connection_0,destination = False,connections = True,plugs = True) or []
                    #print 'shading_engine_connections_1 = ',shading_engine_connections_1
                    i = 0
                    for shading_engine_connection_1 in shading_engine_connections_1:
                        shading_engine_connection_1_split = shading_engine_connection_1.split('.')
                        shading_engine_connection_1 = shading_engine_connection_1_split[0]
                        shading_engine_connection_1_plug = shading_engine_connection_1_split[1]
                        shading_engine_connection_1_type = cmds.nodeType(shading_engine_connection_1)
                        if shading_engine_connection_1_type in material_types:
                            #print 'shading_engine_connection_0 = ',shading_engine_connection_0
                            #print 'shading_engine_connection_1 = ',shading_engine_connection_1
                            if shading_engine_connection_0 == shading_engine_connection_1:
                                #print '---'
                                material_plug_string = shading_engine_connection_0 + '.' + shading_engine_connection_1_plug
                                #print 'material_plug_string = ',material_plug_string
                                texture_check_connections_0 = cmds.listConnections(shading_engine_connection_0,destination = False) or []
                                #print 'selected_texture = ',selected_texture
                                #print 'texture_check_connections_0 = ',texture_check_connections_0
                                texture_check_connection = texture_check_connections_0[i]
                                #print ' '
                                #print 'MAIN texture_check_connection = ',texture_check_connection
                                #print 'material_plug_string_links = ',material_plug_string_links
                                if texture_check_connection in material_plug_string_links:
                                    #print 'match 1a'
                                    if selected_texture in texture_check_connection:
                                        #print 'match 1b'
                                        #print 'appending ',material_plug_string
                                        #print 'adding ' + material_plug_string + ' to material_plug_string_strings'
                                        material_plug_string_strings.append(material_plug_string)
                                    else:
                                        texture_check_connections_1 = cmds.listConnections(texture_check_connection,destination = False) or []
                                        #print 'texture_check_connections_1 = ',texture_check_connections_1
                                        for texture_check_connection in texture_check_connections_1:
                                            #print 'texture_check_connection = ',texture_check_connection
                                            #print 'material_plug_string_links = ',material_plug_string_links
                                            if texture_check_connection in material_plug_string_links:
                                                #print 'match 2a'
                                                if selected_texture in texture_check_connection:
                                                    #print 'match 2b'
                                                    #print 'appending ',material_plug_string
                                                    #print 'adding ' + material_plug_string + ' to material_plug_string_strings'
                                                    material_plug_string_strings.append(material_plug_string)
                                                else:
                                                    texture_check_connections_2 = cmds.listConnections(texture_check_connection,destination = False) or []
                                                    #print 'texture_check_connections_2 = ',texture_check_connections_2
                                                    for texture_check_connection in texture_check_connections_2:
                                                        #print 'texture_check_connection = ',texture_check_connection
                                                        #print 'material_plug_string_links = ',material_plug_string_links
                                                        if texture_check_connection in material_plug_string_links:
                                                            #print 'match 3a'
                                                            if selected_texture in texture_check_connection:
                                                                #print 'match 3b'
                                                                #print 'appending ',material_plug_string
                                                                #print 'adding ' + material_plug_string + ' to material_plug_string_strings'
                                                                material_plug_string_strings.append(material_plug_string)
                                                            else:
                                                                texture_check_connections_3 = cmds.listConnections(texture_check_connection,destination = False) or []
                                                                #print 'texture_check_connections_3 = ',texture_check_connections_3
                                                                for texture_check_connection in texture_check_connections_3:
                                                                    #print 'texture_check_connection = ',texture_check_connection
                                                                    #print 'material_plug_string_links = ',material_plug_string_links
                                                                    if texture_check_connection in material_plug_string_links:
                                                                        #print 'match 4a'
                                                                        if selected_texture in texture_check_connection:
                                                                            #print 'match 4b'
                                                                            #print 'appending ',material_plug_string
                                                                            #print 'adding ' + material_plug_string + ' to material_plug_string_strings'
                                                                            material_plug_string_strings.append(material_plug_string)
                                                                        else:
                                                                            texture_check_connections_4 = cmds.listConnections(texture_check_connection,destination = False) or []
                                                                            #print 'texture_check_connections_4 = ',texture_check_connections_4
                                                                            for texture_check_connection in texture_check_connections_4:
                                                                                #print 'texture_check_connection = ',texture_check_connection
                                                                                #print 'material_plug_string_links = ',material_plug_string_links
                                                                                if texture_check_connection in material_plug_string_links:
                                                                                    #print 'match 5a'
                                                                                    if selected_texture in texture_check_connection:
                                                                                        #print 'match 5b'
                                                                                        #print 'appending ',material_plug_string
                                                                                        #print 'adding ' + material_plug_string + ' to material_plug_string_strings'
                                                                                        material_plug_string_strings.append(material_plug_string)
                                                                                    else:
                                                                                        texture_check_connections_5 = cmds.listConnections(texture_check_connection,destination = False) or []
                                                                                        #print 'texture_check_connections_5 = ',texture_check_connections_5
                                                                                        #print 'material_plug_string_links = ',material_plug_string_links
                                                                                        for texture_check_connection in texture_check_connections_5:
                                                                                            #print 'texture_check_connection = ',texture_check_connection
                                                                                            if texture_check_connection in material_plug_string_links:
                                                                                                #print 'match 6a'
                                                                                                if selected_texture in texture_check_connection:
                                                                                                    #print 'match 6b'
                                                                                                    #print 'appending ',material_plug_string
                                                                                                    #print 'adding ' + material_plug_string + ' to material_plug_string_strings'
                                                                                                    material_plug_string_strings.append(material_plug_string)
                                i = i + 1
        #print 'material_plug_string_strings = ',material_plug_string_strings
        for material_plug_string_string in material_plug_string_strings:
            if material_plug_string_string not in connected_materials:
                connected_materials.append(material_plug_string_string)
        #print '-- end connected_materials --'
        return(connected_materials)

#---------- window ----------

    def texture_linker_UI(self):
        window_name = "uv_set_editor"
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
        window.setFixedWidth(1015)
        window.setMinimumHeight(500)
        main_vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        combo_box_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(combo_box_layout)
        self.label_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.label_layout)
        self.texture_based_uv_set_based_combobox = QtWidgets.QComboBox()
        self.texture_based_uv_set_based_combobox.setMaximumWidth(180)
        self.texture_based_uv_set_based_combobox.setMinimumHeight(18)
        self.texture_based_uv_set_based_combobox.setStyleSheet("""QWidget{color:#a3b3bf;}QComboBox{color:#a3b3bf;}QLineEdit{color:#a3b3bf;}""")
        combo_box_layout.setAlignment(QtCore.Qt.AlignLeft)
        combo_box_layout.addWidget(self.texture_based_uv_set_based_combobox)
        self.texture_based_uv_set_based_combobox.addItem("texture-centric")
        self.texture_based_uv_set_based_combobox.addItem("UV-centric")
        self.texture_based_uv_set_based_combobox.activated[str].connect(lambda:self.centric_state())
        self.centric_state_text = self.texture_based_uv_set_based_combobox.currentText()
        self.left_label = QtWidgets.QLabel('textures')
        self.left_label.setStyleSheet('QLabel {color:#a3b3bf;}')
        self.right_label = QtWidgets.QLabel('uv sets')
        self.right_label.setStyleSheet('QLabel {color:#a3b3bf;}')
        self.label_layout.addWidget(self.left_label)
        self.label_layout.addWidget(self.right_label)
        self.list_layout = QtWidgets.QHBoxLayout(main_widget)
        self.list_layout_left = QtWidgets.QHBoxLayout(main_widget)
        self.list_layout_right = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.list_layout)
        self.list_layout.addLayout(self.list_layout_left)
        self.list_layout.addLayout(self.list_layout_right)
        self.list_widget_left = QtWidgets.QListWidget()
        self.list_widget_left.itemClicked.connect(partial(self.item_press))
        self.list_widget_left.setStyleSheet('QListWidget {background-color: #292929; color:#7a95c9;}')
        self.list_widget_left.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.list_widget_left.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_layout_left.addWidget(self.list_widget_left)
        self.list_widget_right = QtWidgets.QListWidget()
        self.list_widget_right.setSelectionMode(self.list_widget_right.MultiSelection)
        self.list_widget_right.itemClicked.connect(self.right_listWidget_selection_eval)
        self.list_widget_right.setStyleSheet('QListWidget {background-color: #292929; color:#7a95c9;}')
        self.list_widget_right.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.list_widget_right.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_layout_right.addWidget(self.list_widget_right)
        self.list_widget_texture_info = QtWidgets.QListWidget()
        self.list_widget_texture_info.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.list_widget_texture_info.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.list_widget_texture_info.setMaximumHeight(40)
        self.list_widget_texture_info.setStyleSheet('QListWidget {background-color: #292929; color:#8c4c7f;}')
        self.list_widget_texture_info.setFocusPolicy(QtCore.Qt.NoFocus)
        #main_vertical_layout.addWidget(self.list_widget_texture_info)
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["SceneOpened", self.populate_windows])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["DagObjectCreated", self.populate_windows])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["NameChanged", self.populate_windows])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["Undo", self.populate_windows])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["Redo", self.populate_windows])
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["SetModified", self.populate_windows])
        self.populate_windows()
        self.right_listWidget_selection_eval()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    uv_set_editor = UV_SET_EDITOR()
    uv_set_editor.texture_linker_UI()

#main()
