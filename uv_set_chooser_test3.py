import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

#"""
#lighting_shelf: UV_set_editor
#********************************************
#"""
print 'thursday'


class UV_SET_EDITOR(object):
    def __init__(self):
        self.selected_item_text = ''
        self.uv_set_selection_status_dic = {}
        self.uv_set_selection_status_dic_state_change = {}
        self.spacer = '          '


#---------- procedural tools and data gathering methods ----------

    def centric_state(self):
        #print 'centric_state'
        self.uv_set_selection_status_dic_state_change = self.uv_set_selection_status_dic
        self.centric_state_text = self.texture_based_uv_set_based_combobox.currentText()
        #self.texture_based_uv_set_based_combobox.setStyleSheet("""QWidget{color:#a3b3bf;}QComboBox{#a3b3bf:blue;}QLineEdit{color:#a3b3bf;}""")
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
            self.selected_items_right_text.append(selected_right_list_pointer_text)
        for pointer in self.selected_right_list_pointers:
            pointer_text = pointer.text()

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

    def lock_selected_right_QListWidget(self):
        #print 'lock_selected_right_QListWidget()'
        self.unlock_right_QListWidget()
        selected_uv_sets_pointers = self.list_widget_right.selectedItems()
        for selected_uv_set_pointer in selected_uv_sets_pointers:
            item = selected_uv_set_pointer
            item_text = item.text()
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

    def populate_windows(self):
        #print 'populate_windows()'
        self.evaluate_textures_in_scene()
        self.evaluate_UV_sets_in_scene()
        self.list_widget_left.clear()
        self.list_widget_right.clear()
        self.list_widget_texture_info.clear()
        #icon_size = 60
        font_size = 11
        if self.centric_state_text == 'texture-centric':
            #self.list_widget_left.setViewMode(QtWidgets.QListView.IconMode)
            self.list_widget_left.setWrapping(True)
            self.list_widget_right.setWrapping(False)
            self.list_widget_left.setSpacing(3)
            self.list_widget_right.setSpacing(1)
            #self.list_widget_left.setFlow(QtWidgets.QListView.LeftToRight)
            #self.list_widget_right.setFlow(QtWidgets.QListView.TopToBottom)
            for texture in self.all_textures:
                texture_item = QtWidgets.QListWidgetItem(texture)
                texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                attr_string = (texture + '.fileTextureName')
                file_node_type = cmds.nodeType(texture)
                #if file_node_type == 'file':
                    #image_path = cmds.getAttr(texture + '.fileTextureName')
                    #length_image_path = len(image_path)
                    #if length_image_path < 1:
                        #image_path = 'empty'
                    #mel_string = "filetest -f " + '"' + image_path + '"'
                    #texture_image_exists = maya.mel.eval(mel_string)
                    #if texture_image_exists != 1:
                        #image_path = "U:/cwinters/thumbnails/generic_no_texture_found_texture.jpg"
                        #image_path = "/Users/alfredwinters/Desktop/python/thumbnails/generic_no_texture_found.jpg"
                    #image_path_split = image_path.split('.')
                    #length_image_path_split = len(image_path_split)
                    #if image_path_split[length_image_path_split - 1] == 'hdr':
                        #image_path = "U:/cwinters/thumbnails/hdr_texture_found.jpg"
                #if file_node_type != 'file':
                    #if file_node_type == 'noise':
                        #image_path = 'U:/cwinters/thumbnails/generic_noise_texture.jpg'
                        #image_path = 'U:/cwinters/thumbnails/generic_ramp_thumbnail_texture_size.jpg'
                    #else:
                        #image_path = 'U:/cwinters/thumbnails/generic_ramp_texture.jpg'
                        #image_path = "/Users/alfredwinters/Desktop/python/thumbnails/generic_ramp_thumbnail_texture_size.jpg"
                #texture_pixmap = QtGui.QPixmap(image_path)
                #texture_icon = QtGui.QIcon()
                #self.list_widget_left.setIconSize(QtCore.QSize(icon_size,icon_size))
                #texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                #texture_icon.addPixmap(texture_pixmap)
                #texture_item.setIcon(texture_icon)
                #print 'texture = ',texture
                #print 'self.file_to_file_path_dic = ',self.file_to_file_path_dic
                if texture in self.file_to_file_path_dic:
                    texture_plus_file_name = self.file_to_file_path_dic[texture]
                else:
                    texture_plus_file_name = texture
                self.list_widget_left.addItem(texture_plus_file_name)
                texture_item.setTextAlignment(Qt.AlignBottom)
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
        if self.centric_state_text == 'UV-centric':
            #self.list_widget_right.setViewMode(QtWidgets.QListView.IconMode)
            self.list_widget_right.setWrapping(True)
            self.list_widget_left.setWrapping(False)
            self.list_widget_right.setSpacing(4)
            self.list_widget_left.setSpacing(1)
            #self.list_widget_right.setFlow(QtWidgets.QListView.LeftToRight)
            #self.list_widget_left.setFlow(QtWidgets.QListView.TopToBottom)
            for texture in self.all_textures:
                texture_item = QtWidgets.QListWidgetItem(texture)

                #texture_item.setTextColor(QtGui.QColor())
                texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                attr_string = (texture + '.fileTextureName')
                file_node_type = cmds.nodeType(texture)
                if file_node_type == 'file':
                    #image_path = cmds.getAttr(texture + '.fileTextureName')
                    #length_image_path = len(image_path)
                    #if length_image_path < 1:
                        #image_path = 'empty'
                    #mel_string = "filetest -f " + '"' + image_path + '"'
                    #texture_image_exists = maya.mel.eval(mel_string)
                    #if texture_image_exists == 1:
                        #texture_pixmap = QtGui.QPixmap(image_path)
                    #else:
                        #image_path = "U:/cwinters/thumbnails/generic_no_texture_found_texture.jpg"
                        #image_path = "/Users/alfredwinters/Desktop/python/thumbnails/generic_no_texture_found.jpg"
                        #texture_pixmap = QtGui.QPixmap(image_path)
                    #texture_icon = QtGui.QIcon()
                    #self.list_widget_right.setIconSize(QtCore.QSize(icon_size,icon_size))
                    texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                    #texture_icon.addPixmap(texture_pixmap)
                    #texture_item.setIcon(texture_icon)
                    self.list_widget_right.addItem(texture_item)
                    texture_item.setTextAlignment(Qt.AlignBottom)
                if file_node_type != 'file':
                    #if file_node_type == 'noise':
                        #image_path = 'U:/cwinters/thumbnails/generic_noise_texture.jpg'
                    #else:
                        #image_path = 'U:/cwinters/thumbnails/generic_ramp_texture.jpg'
                    #image_path = "/Users/alfredwinters/Desktop/python/thumbnails/generic_ramp_thumbnail_texture_size.jpg"
                    texture_item = QtWidgets.QListWidgetItem(texture)
                    #texture_pixmap = QtGui.QPixmap(image_path)
                    #texture_icon = QtGui.QIcon()
                    #self.list_widget_right.setIconSize(QtCore.QSize(icon_size,icon_size))
                    texture_item.setFont(QtGui.QFont('SansSerif', font_size))
                    #texture_icon.addPixmap(texture_pixmap)
                    #texture_item.setIcon(texture_icon)
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
                    #item.setTextColor(QtGui.QColor("#c4bebe"))
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                    item.setFont(QtGui.QFont('SansSerif', 12))
                i = i + 1
            self.initial_uv_set_name_to_address_dic_eval()
            self.activate_right_listWidget()

    def evaluate_textures_in_scene(self):
        #print 'evaluate_textures_in_scene()'
        self.file_to_file_path_dic = {}
        file_textures_all = cmds.ls(type = 'file')
        file_textures = []
        ramp_textures_all = cmds.ls(type = 'ramp')
        noise_texures_all = cmds.ls(type = 'noise')
        non_file_textures_all = ramp_textures_all + noise_texures_all
        non_file_texture_textures = []
        for file in file_textures_all:
            valid_file = 0
            if file == 'gi_std_lgt' or file == 'reflection_sdt_lgt' or file == 'refraction_sdt_lgt':
                valid_file = 0
            file_connections = cmds.listConnections(file) or []
            for connection in file_connections:
                connection_type = cmds.nodeType(connection)
                if connection_type == 'VRayMtl' or connection_type == 'phong' or connection_type == 'blend' or connection_type == 'layeredTexture' or connection_type == 'remapHsv' or connection_type == 'multiplyDivide' or connection_type == 'remapColor' or connection_type == 'VRayRenderElement':
                    valid_file = 1
            if valid_file == 1:
                #print 'file = ',file
                file_path = cmds.getAttr(file + '.fileTextureName') or 'no valid path'
                #print 'file_path = ',file_path
                file_path_split = file_path.split('/')
                #print 'file_path_split = ',file_path_split
                file_path_name = file_path_split[-1]
                #print 'file_path_name = ',file_path_name
                file_path_name_split = file_path_name.split('.')
                file_path_name = file_path_name_split[0]
                self.file_to_file_path_dic[file] = file + ' ( ' +  file_path_name + ' )'
                file_textures.append(file)
                #print 'self.file_to_file_path_dic = ',self.file_to_file_path_dic
        for non_file_texture in non_file_textures_all:
            light_ramp = 0
            non_file_texture_connections = cmds.listConnections(non_file_texture,source = False) or []
            for non_file_texture_connection in non_file_texture_connections:
                non_file_texture_connection_type = cmds.nodeType(non_file_texture_connection)
                if non_file_texture_connection_type == 'VRayLightRectShape' or non_file_texture_connection_type == 'VRayPlaceEnvTex' or non_file_texture_connection_type == 'transform' or non_file_texture_connection_type == 'VRaySettingsNode':
                    light_ramp = 1
                if non_file_texture_connection_type == 'transform':
                    non_file_texture_connection_subs = cmds.listRelatives(non_file_texture_connection,children = True, fullPath = True) or []
                    for non_file_texture_connection_sub in non_file_texture_connection_subs:
                        non_file_texture_connection_sub_type = cmds.nodeType(non_file_texture_connection_sub)
                        if non_file_texture_connection_sub_type == 'VRayLightRectShape':
                            if non_file_texture_connection_sub_type == 'VRayPlaceEnvTex':
                                light_ramp = 1
                else:
                    non_file_texture_connections_1 = cmds.listConnections(non_file_texture_connection,source = False) or []
                    for non_file_texture_connection in non_file_texture_connections_1:
                        non_file_texture_connection_type = cmds.nodeType(non_file_texture_connection)
                        if non_file_texture_connection_type == 'VRayLightRectShape' or non_file_texture_connection_type == 'VRayPlaceEnvTex' or non_file_texture_connection_type == 'transform' or non_file_texture_connection_type == 'VRaySettingsNode':
                            light_ramp = 1
                        if non_file_texture_connection_type == 'transform':
                            non_file_texture_connection_subs = cmds.listRelatives(non_file_texture_connection,children = True, fullPath = True) or []
                            for non_file_texture_connection_sub in non_file_texture_connection_subs:
                                non_file_texture_connection_sub_type = cmds.nodeType(non_file_texture_connection_sub)
                                if non_file_texture_connection_sub_type == 'VRayLightRectShape':
                                    if non_file_texture_connection_sub_type == 'VRayPlaceEnvTex':
                                        light_ramp = 1
                        else:
                            non_file_texture_connections_2 = cmds.listConnections(non_file_texture_connection,source = False) or []
                            for non_file_texture_connection in non_file_texture_connections_2:
                                non_file_texture_connection_type = cmds.nodeType(non_file_texture_connection)
                                if non_file_texture_connection_type == 'VRayLightRectShape' or non_file_texture_connection_type == 'VRayPlaceEnvTex' or non_file_texture_connection_type == 'transform' or non_file_texture_connection_type == 'VRaySettingsNode':
                                    light_ramp = 1
                                if non_file_texture_connection_type == 'transform':
                                    non_file_texture_connection_subs = cmds.listRelatives(non_file_texture_connection,children = True, fullPath = True) or []
                                    for non_file_texture_connection_sub in non_file_texture_connection_subs:
                                        non_file_texture_connection_sub_type = cmds.nodeType(non_file_texture_connection_sub)
                                        if non_file_texture_connection_sub_type == 'VRayLightRectShape':
                                            if non_file_texture_connection_sub_type == 'VRayPlaceEnvTex':
                                                light_ramp = 1
            if light_ramp == 0:
                non_file_texture_textures.append(non_file_texture)
        self.all_textures = file_textures + non_file_texture_textures

    def evaluate_UV_sets_in_scene(self):
        #print 'evaluate_UV_sets_in_scene()'
        self.uv_sets_all = []
        self.uv_set_name_to_address_dic = {}
        self.uv_set_selection_status_dic = {}
        transorms_objects = cmds.ls(type = 'shape')
        transorms_objects_tmp = transorms_objects
        for object in transorms_objects:
            object_split = object.split('Shape')
            if 'polySurface' not in object_split[0]:
                uv_sets = cmds.polyUVSet(object,allUVSets = True, query = True) or []
                number_of_uv_sets = len(uv_sets)
                if number_of_uv_sets > 0:
                    self.uv_sets_all.append('* ' + object)
                    for uv_set in uv_sets:
                        uv_sets_all_string = object + ':|:' + uv_set
                        self.uv_sets_all.append(uv_sets_all_string)
                        for texture in self.all_textures:
                            if uv_set == 'map1':
                                self.uv_set_selection_status_dic[texture + ':|:' + uv_sets_all_string] = 1
                            else:
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

    def initial_uv_set_name_to_address_dic_eval(self):
        #print 'initial_uv_set_name_to_address_dic_eval'
        assigned_uv_sets = []
        for texture in self.all_textures:
            uv_set_names_linked_to_texture = []
            uv_sets_linked_to_texture = cmds.uvLink(texture = texture, query = True) or []
            for uv_set_all in self.uv_sets_all:
                empty_uv_set_detect = len(uv_set_all)
                if empty_uv_set_detect != 2:
                    uv_set_all_split = uv_set_all.split('*')
                    if uv_set_all_split[0] != '':
                        uv_set_split = uv_set_all.split(':|:')
                        uv_set_object = uv_set_split[0]
                        uv_set = uv_set_all
                        uv_set_address_linked_to_texture = cmds.uvLink( query=True, texture = texture,queryObject = uv_set_object) or []
                        len_uv_set_address_linked_to_texture = len(uv_set_address_linked_to_texture)
                        if len_uv_set_address_linked_to_texture > 0:
                            uv_set_address_linked_to_texture = uv_set_address_linked_to_texture[0]
                            for uv_set_name in self.uv_set_name_to_address_dic:
                                address = self.uv_set_name_to_address_dic[uv_set_name]
                                if address == uv_set_address_linked_to_texture:
                                    uv_set_name_split = uv_set_name.split(':|:')
                                    name = uv_set_name_split[1]
                                    if name != 'map1':
                                        uv_set_name_split = uv_set_name.split(':|:')
                                        uv_set_name = uv_set_name_split[1]
                                        self.uv_set_selection_status_dic[texture + ':|:' + uv_set_object + ':|:' + uv_set_name] = 1
                                        self.uv_set_selection_status_dic[texture + ':|:' + uv_set_object + ':|:' + 'map1'] = 0
        for uv_set_all in self.uv_sets_all:
            empty_uv_set_detect = len(uv_set_all)
            if empty_uv_set_detect != 2:
                uv_set_all_split = uv_set_all.split('*')
                if uv_set_all_split[0] != '':
                    for texture in self.all_textures:
                        dic_string_check = texture + ':|:' + uv_set_all
                        if dic_string_check not in self.uv_set_selection_status_dic:
                            self.uv_set_selection_status_dic[texture + ':|:' + uv_full] = 0
        for us_set_carry_over in self.uv_set_selection_status_dic_state_change:
            state = self.uv_set_selection_status_dic_state_change[us_set_carry_over]
            us_set_carry_over_split = us_set_carry_over.split(':|:')
            us_set_carry_over_texture = us_set_carry_over_split[0]
            us_set_carry_over_object = us_set_carry_over_split[1]
            us_set_carry_uv_set = us_set_carry_over_split[2]
            if state == 1:
                self.uv_set_selection_status_dic[us_set_carry_over] = 1
                if us_set_carry_uv_set != 'map1':
                    self.uv_set_selection_status_dic[us_set_carry_over_texture + ':|:' + us_set_carry_over_object + ':|:' + 'map1'] = 0

#---------- UV set selection methods ----------

    def item_press(self,item):
        #print 'item_press()'
        if self.centric_state_text == 'texture-centric':
            self.deselect_QListWidget(self.list_widget_right)
            self.texture_linked_uv_sets = []
            self.selected_item_text = item.text()
            self.activate_right_listWidget()
            for file in self.file_to_file_path_dic:
                item = self.file_to_file_path_dic[file]
                if item == self.selected_item_text:
                    self.selected_item_text = file
            uv_set_addresses_linked_to_selected_texture = cmds.uvLink( query = True, texture = self.selected_item_text)
            number_of_linked_uv_sets = len(uv_set_addresses_linked_to_selected_texture)
            for uv_set_name_to_address in self.uv_set_name_to_address_dic:
                uv_set_address = self.uv_set_name_to_address_dic[uv_set_name_to_address]
                if uv_set_address in uv_set_addresses_linked_to_selected_texture:
                    self.texture_linked_uv_sets.append(uv_set_name_to_address)
            self.update_right_listWidget()
        if self.centric_state_text == 'UV-centric':
            self.selected_item_text = item.text()
            self.activate_right_listWidget()
            if '*' not in self.selected_item_text:
                self.selected_item_text = self.selected_item_text.replace('          ','')
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
        if self.centric_state_text == 'texture-centric':
            self.unlock_right_QListWidget()
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item_text = item.text()
                empty_uv_set_detect = len(item_text)
                if empty_uv_set_detect != 2:
                    item_text_split = item_text.split('*')
                    if '*' in item_text:
                        item.setTextColor(QtGui.QColor("#c4bebe"))
                        item_object = item_text_split[1]
                        item_object = item_object[1:]
                    if item_text_split[0] != '':
                        num_of_spaces = len(self.spacer)
                        item_text = item_text[num_of_spaces:]
                        combined_object_uv_set_name = (self.selected_item_text + ':|:' + (item_object + ':|:' + item_text))
                        item_text_selection_status = self.uv_set_selection_status_dic[combined_object_uv_set_name]
                        if item_text_selection_status == 1:
                            item.setSelected(True)
                            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                        if item_text_selection_status == 0:
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
                selected_index = self.list_widget_left.selectedIndexes()
                for ind in selected_index:
                    selected_row = ind.row()
                i = 0
                while i < self.number_of_items_in_left_listWidget:
                    item_uv_set = self.list_widget_left.item(i)
                    item_uv_set_text = item_uv_set.text()
                    item_uv_set_text = item_uv_set_text.replace('          ','')
                    item_uv_set_text_split = item_uv_set_text.split('*')
                    if '*' in item_uv_set_text:
                        item_object = item_uv_set_text_split[1]
                    if item_uv_set_text_split[0] != '':
                        if i == selected_row:
                            if item_uv_set_text == self.selected_item_text:
                                self.selected_item_text =  self.selected_item_text.replace('          ','')
                                item_object = item_object.replace(' ','')
                                item_text_selection_status_dic_key = (item_text + ':|:' + (item_object  + ':|:' + self.selected_item_text))
                                print 'item_text_selection_status_dic_key = ',item_text_selection_status_dic_key
                                print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
                                item_text_selection_status = self.uv_set_selection_status_dic[item_text_selection_status_dic_key]
                                if item_text_selection_status == 0:
                                    item.setSelected(False)
                                if item_text_selection_status == 1:
                                    item.setSelected(True)
                                    item_text = item.text()
                                    self.selected_right_list_textures.append(item_text)
                                    combined_selected_item_text = item_object + ':|:' + self.selected_item_text
                                    selected_item_text_split = combined_selected_item_text.split(':|:')
                                    selected_item_text_uv_set = selected_item_text_split[1]
                                    selected_item_text_uv_set = selected_item_text_uv_set.replace('          ','')
                                    if selected_item_text_uv_set == 'map1':
                                        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                    i = i + 1
                it = it + 1
            self.texture_to_object_color_adjust()

    def right_listWidget_selection_eval(self):
        #print 'right_listWidget_selection_eval()'
        if self.centric_state_text == 'texture-centric':
            selected_uv_sets_pointers = self.list_widget_right.selectedItems()
            uv_set_pointers = []
            selected_right_pointers = []
            selected_uv_set_names = []
            uv_set_object_name_dic = {}
            uv_set_pointer_dic = {}
            it = 0
            size_of_left_selection = len(self.selected_item_text)
            if size_of_left_selection > 0:
                while it < self.number_of_items_in_right_listWidget:
                    item = self.list_widget_right.item(it)
                    uv_set_pointers.append(item)
                    item_text = item.text()
                    item_text_split = item_text.split('*')
                    if '*' in item_text:
                        item_object = item_text_split[1]
                        item_object = item_object[1:]
                    if item_text_split[0] != '':
                        uv_set_split = item_text.split(':|:')
                        uv_set_object_name = item_object
                        uv_set_object_name_dic[item_text] = uv_set_object_name
                    it = it + 1
                for selected_uv_set_pointer in selected_uv_sets_pointers:
                    selected_right_pointers.append(selected_uv_set_pointer)
                    it_text = selected_uv_set_pointer.text()
                    it_text = it_text.replace('          ','')
                    selected_uv_set_names.append(it_text)
                    selected_index = self.list_widget_right.selectedIndexes()
                    for ind in selected_index:
                        selected_row = ind.row()
                    i = 0
                    for uv_set_pointer in uv_set_pointers:
                        uv_set_text = uv_set_pointer.text()
                        item_text_split = uv_set_text.split('*')
                        if '*' in uv_set_text:
                            item_object = item_text_split[1]
                            item_object = item_object[1:]
                        if item_text_split[0] != '':
                            if i == selected_row:
                                selected_uv_set_object_name = item_object
                        i = i + 1
                    for uv_set_pointer in uv_set_pointers:
                        if str(uv_set_pointer) != str(selected_uv_set_pointer):
                            uv_set_name = uv_set_pointer.text()
                            uv_set_name = uv_set_name.replace('          ','')
                            item_text_split = uv_set_name.split('*')
                            if '*' in uv_set_name:
                                item_object = item_text_split[1]
                            if item_text_split[0] != '':
                                if item_object == selected_uv_set_object_name:
                                    uv_set_pointer.setSelected(False)
                                    self.uv_set_selection_status_dic[self.selected_item_text + ':|:' + item_object + ':|:' + uv_set_name] = 0
                    self.unlock_right_QListWidget()
                    selected_uv_set_pointer.setSelected(True)
                    it_text_combined =  selected_uv_set_object_name + ':|:' + it_text
                    self.uv_set_selection_status_dic[self.selected_item_text + ':|:' + it_text_combined] = 1
            selected_uv_sets_pointers = self.list_widget_right.selectedItems()
            for selected_uv_sets_pointer in selected_uv_sets_pointers:
                pointer_text = selected_uv_sets_pointer.text()
                selected_uv_sets_pointer.setFlags(selected_uv_sets_pointer.flags() & ~Qt.ItemIsEnabled)
            self.link_texture_to_uv_set()
        if self.centric_state_text == 'UV-centric':
            size_of_left_selection = len(self.selected_item_text)
            if size_of_left_selection > 0:
                self.selected_item_text = self.selected_item_text.replace('          ','')
                selected_index = self.list_widget_left.selectedIndexes()
                for ind in selected_index:
                    selected_row = ind.row()
                i = 0
                while i < self.number_of_items_in_left_listWidget:
                    uv_set_sub = self.list_widget_left.item(i)
                    uv_set_sub_text = uv_set_sub.text()
                    uv_set_sub_text = uv_set_sub_text.replace('          ','')
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
                    self.uv_set_selection_status_dic[selected_item_right_text + ':|:' + self.selected_item_text] = 1
                    for uv_set_selection in self.uv_set_selection_status_dic:
                        uv_set_selection_split = uv_set_selection.split(':|:')
                        uv_set_selection_texture = uv_set_selection_split[0]
                        uv_set_selection_object = uv_set_selection_split[1]
                        uv_set = uv_set_selection_split[2]
                        if uv_set_selection_object == selected_item_text_object:
                            if uv_set_selection_texture == selected_item_right_text:
                                if uv_set != selected_item_text_uv_set:
                                    self.uv_set_selection_status_dic[uv_set_selection] = 0
                for texture in self.all_textures:
                    if texture not in self.selected_items_right_text:
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

    def link_texture_to_uv_set(self):
        #print 'link_texture_to_uv_set()'
        for uv_set_selection in self.uv_set_selection_status_dic:
            selection_status = self.uv_set_selection_status_dic[uv_set_selection]
            if selection_status == 0:
                uv_set_selection_split = uv_set_selection.split(':|:')
                texture = uv_set_selection_split[0]
                object = uv_set_selection_split[1]
                uv_set = uv_set_selection_split[2]
                object = object.replace(' ','')
                texture_linked_uv_set_address = self.uv_set_name_to_address_dic[object + ':|:' + uv_set]
                cmds.uvLink(b = True, uvSet = texture_linked_uv_set_address,texture = texture)
            if selection_status == 1:
                uv_set_selection_split = uv_set_selection.split(':|:')
                texture = uv_set_selection_split[0]
                object = uv_set_selection_split[1]
                uv_set = uv_set_selection_split[2]
                object = object.replace(' ','')
                texture_linked_uv_set_address = self.uv_set_name_to_address_dic[object + ':|:' + uv_set]
                cmds.uvLink(make = True, uvSet = texture_linked_uv_set_address,texture = texture)

    def texture_to_object_color_adjust(self):
        print 'texture_to_object_color_adjust'
        linked_objects_to_texture_dic = {}
        object_material_string = ''
        self.list_widget_texture_info.clear()
        if self.centric_state_text == 'texture-centric':
            selected_textures = []
            selected_texture = self.selected_item_text
            print 'selected_texture = ',selected_texture
            connected_materials = self.connected_materials(selected_texture)
            cmds.select(clear = True)
            object_material_string = ''
            print 'connected_materials  = ',connected_materials
            assigned_objects = []
            for material in connected_materials:
                assigned_objects = []
                print ' '
                print 'material = ',material
                current_selection = cmds.ls(selection = True) or []
                cmds.hyperShade(objects = material)
                assigned_object = (cmds.ls(selection = True)) or []
                print 'material = ',material
                number_of_selected_objects = len(assigned_object)
                if number_of_selected_objects > 0:
                    assigned_objects.append(assigned_object[0])
                    print 'assigned_objects = ',assigned_objects
                print 'material = ',material
                number_of_assigned_objects = len(assigned_objects)
                for object in assigned_objects:
                    if '.f[' in object:
                        object_split= object.split('.f[')
                        object = object_split[0]
                    print 'object = ',object
                    print 'material = ',material
                    object_material_string = object_material_string + object + ': ' + material + '  ,  '
                    print 'object_material_string = ',object_material_string
            linked_objects_to_texture_dic[selected_texture] = assigned_objects
            object_material_string = object_material_string[:-4]
            print 'object_material_string = ',object_material_string
            texture_information_string = object_material_string
            texture_information_string_size = len(texture_information_string)
            print 'texture_information_string_size = ',texture_information_string_size
            if texture_information_string_size == 0:
                connected_materials_size = len(connected_materials)
                if connected_materials_size == 0:
                    texture_information_string = 'texture linked to no material and used by no object'
                else:
                    texture_information_string = str(connected_materials[0]) + ' * texture used by no object '
            print 'texture_information_string = ',texture_information_string
            self.list_widget_texture_info.addItem(texture_information_string)
            #print 'self.number_of_items_in_right_listWidget = ',self.number_of_items_in_right_listWidget
            it = 0
            made_object_highlight = 0
            while it < self.number_of_items_in_right_listWidget:
                print ' '
                item = self.list_widget_right.item(it)
                item_text = item.text()
                if item_text == '':
                    item.setFlags(item.flags() | Qt.ItemIsEnabled)
                    item.setFlags(item.flags() | Qt.ItemIsEditable)
                print 'item_text = ',item_text
                print 'making ' + item_text + ' grey'
                item.setTextColor(QtGui.QColor("#515151"))
                print 'made_object_highlight = ',made_object_highlight
                if made_object_highlight == 1:
                    if '*' not in item_text:
                        print 'making ' + item_text + ' lowlight'
                        item.setTextColor(QtGui.QColor('#515b8c'))
                #print 'linked_objects_to_texture_dic = ',linked_objects_to_texture_dic
                for linked_object_to_texture_dic in linked_objects_to_texture_dic:
                    print 'linked_object_to_texture_dic = ',linked_object_to_texture_dic
                    print 'selected_texture = ',selected_texture
                    if linked_object_to_texture_dic == selected_texture:
                        print 'linked_object_to_texture_dic = selected_texture'
                        objects = linked_objects_to_texture_dic[selected_texture]
                        print 'objects = ',objects
                        for object in objects:
                            print 'object = ',object
                            print 'item_text = ',item_text
                            if '*' in item_text:
                                print 'setting made_object_highlight to 0'
                                made_object_highlight = 0
                            if '.f[' in object:
                                object_split = object.split('.f[')
                                object = object_split[0]
                            if 'Shape' in item_text:
                                item_text_split = item_text.split('Shape')
                                item_text = item_text_split[0]
                            if object in item_text:
                                print 'object in item_text'
                                print 'making ' + item_text + ' highlight'
                                item.setTextColor(QtGui.QColor('#7c98cf'))
                                print 'setting made_object_highlight to 1'
                                made_object_highlight = 1
                        #print 'setting made_object_highlight to 0'
                        #made_object_highlight = 0
                    #else:
                        #print 'setting made_object_highlight to 0'
                        #made_object_highlight = 0
                it = it + 1
        if self.centric_state_text == 'UV-centric':
            selected_textures = []
            selected_uv_set = self.selected_item_text
            #print 'selected_uv_set = ',selected_uv_set
            selected_index = self.list_widget_left.selectedIndexes()
            for ind in selected_index:
                selected_row = ind.row()
            i = 0
            while i < self.number_of_items_in_left_listWidget:
                item_uv_set = self.list_widget_left.item(i)
                item_uv_set_text = item_uv_set.text()
                item_uv_set_text = item_uv_set_text.replace('          ','')
                item_uv_set_text_split = item_uv_set_text.split('*')
                if '*' in item_uv_set_text:
                    item_object = item_uv_set_text_split[1]
                if item_uv_set_text_split[0] != '':
                    if i == selected_row:
                        if item_uv_set_text == self.selected_item_text:
                            selected_object = item_object
                i = i + 1
            self.linked_objects_to_texture_to_materials_dic = {}
            connected_materials_list = []
            for selected_texture in self.selected_right_list_textures:
                connected_material = self.connected_materials(selected_texture)
                connected_materials_list.append(connected_material)
                assigned_objects = ''
                for material in connected_materials_list:
                    for mat in material:
                        current_selection = cmds.ls(selection = True)
                        cmds.select(clear = True)
                        cmds.hyperShade(objects = mat)
                        assigned_objects = cmds.ls(selection = True)
                        for object in assigned_objects:
                            if object == selected_object:
                                object_material_string = object_material_string + ' , ' + selected_texture + ':' + mat
                        linked_objects_to_texture_dic[selected_texture] = assigned_objects
            object_material_string = object_material_string[2:]
            texture_information_string = object_material_string
            texture_information_string_size = len(texture_information_string)
            #print 'texture_information_string_size = ',texture_information_string_size
            if texture_information_string_size < 12:
                texture_information_string = 'textures used by no material'
            self.list_widget_texture_info.addItem(texture_information_string)
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                #item.setTextColor(QtGui.QColor(self.low_light_color))
                item_text = item.text()
                #print 'item_text = ',item_text
                #print 'selected_texture = ',selected_texture
                #print 'linked_objects_to_texture_dic = ',linked_objects_to_texture_dic
                for linked_object_to_texture_dic in linked_objects_to_texture_dic:
                    if linked_object_to_texture_dic == selected_texture:
                        objects = linked_objects_to_texture_dic[selected_texture]
                        #print 'objects = ',objects
                        #for object in objects:
                            #if object in item_text:
                                #item.setTextColor(QtGui.QColor(self.high_light_color))
                            #else:
                                #item.setTextColor(QtGui.QColor(self.low_light_color))
                it = it + 1
        it = 0
        while it < self.list_widget_texture_info.count():
            item = self.list_widget_texture_info.item(it)
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            it = it + 1
        cmds.select(clear = True)
        #for selection in current_selection:
            #cmds.select(selection,add = True)

    def connected_materials(self,selected_texture):
        material_types = ['lambert','phong','blinn','surfaceShader','VRayMtl']
        connected_materials = []
        connections_0 = cmds.listConnections(selected_texture,source = False, plugs = True) or []
        for connection in connections_0:
            connection_type = cmds.nodeType(connection)
            if connection_type in material_types:
                if connection not in connected_materials:
                    connected_materials.append(connection)
            connections_1 = cmds.listConnections(connection,source = False,plugs = True) or []
            for connection in connections_1:
                connection_type = cmds.nodeType(connection)
                if connection_type in material_types:
                    if connection not in connected_materials:
                        connected_materials.append(connection)
                connections_2 = cmds.listConnections(connection,source = False,plugs = True) or []
                for connection in connections_2:
                    connection_type = cmds.nodeType(connection)
                    if connection_type in material_types:
                        if connection not in connected_materials:
                            connected_materials.append(connection)
                    connections_3 = cmds.listConnections(connection,source = False,plugs = True) or []
                    for connection in connections_3:
                        connection_type = cmds.nodeType(connection)
                        if connection_type in material_types:
                            if connection not in connected_materials:
                                connected_materials.append(connection)
                    connections_4 = cmds.listConnections(connection,source = False,plugs = True) or []
                    for connection in connections_4:
                        connection_type = cmds.nodeType(connection)
                        if connection_type in material_types:
                            if connection not in connected_materials:
                                connected_materials.append(connection)
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
        main_vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        combo_box_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(combo_box_layout)
        self.label_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.label_layout)
        self.texture_based_uv_set_based_combobox = QtWidgets.QComboBox()
        self.texture_based_uv_set_based_combobox.setMaximumWidth(180)
        self.texture_based_uv_set_based_combobox.setMinimumHeight(18)
        #self.texture_based_uv_set_based_combobox.setStyleSheet("""QWidget{background-color: yellow;}QComboBox{background-color: blue;}QLineEdit{background-color: red;}""")
        #self.texture_based_uv_set_based_combobox.setStyleSheet("""QWidget{color:#a3b3bf;}QComboBox{color:#a3b3bf;}QLineEdit{color:#a3b3bf;}""")
        #self.texture_based_uv_set_based_combobox.setStyleSheet("""QWidget{color:#a3b3bf;}QComboBox{color:#a3b3bf;}QLineEdit{color:#a3b3bf;}""")
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
        main_vertical_layout.addWidget(self.list_widget_texture_info)
        #self.myScriptJobID = cmds.scriptJob(p = window_name, event=["SelectionChanged", self.populate_windows])
        #self.myScriptJobID = cmds.scriptJob(p = window_name, event=["NameChanged", self.populate_windows])
        self.populate_windows()
        self.right_listWidget_selection_eval()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    uv_set_editor = UV_SET_EDITOR()
    uv_set_editor.texture_linker_UI()
#main()
