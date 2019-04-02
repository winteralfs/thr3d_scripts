import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

print 'monday night'

class UV_SET_EDITOR(object):
    def __init__(self):
        self.selected_texture_text = ''

#---------- procedural tools and data gathering methods ----------

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())

    def deselect_QListWidget(self,listwidget):
        for i in range(listwidget.count()):
            item = listwidget.item(i)
            listwidget.setItemSelected(item, False)

    def activate_uv_set_listWidget(self):
        self.texture_selected_length = len(self.selected_texture_text)
        if self.texture_selected_length == 0:
            self.uv_sets_list_widget.setStyleSheet('QListWidget {background-color: #292929; color: #515151;}')
            it = 0
            while it < self.number_of_uv_sets_in_listWidget:
                item = self.uv_sets_list_widget.item(it)
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                it = it + 1
        else:
            self.uv_sets_list_widget.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
            it = 0
            while it < self.number_of_uv_sets_in_listWidget:
                item = self.uv_sets_list_widget.item(it)
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                it = it + 1

    def unlock_uv_sets_QListWidget(self):
        it = 0
        while it < self.number_of_uv_sets_in_listWidget:
            item = self.uv_sets_list_widget.item(it)
            item_text = item.text()
            if item_text == '---':
                item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            if item_text != '---':
                item.setFlags(item.flags() | Qt.ItemIsSelectable)
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
            it = it + 1

    def lock_selected_uv_sets_QListWidget(self):
        self.unlock_uv_sets_QListWidget()
        selected_uv_sets_pointers = self.uv_sets_list_widget.selectedItems()
        for selected_uv_set_pointer in selected_uv_sets_pointers:
            item = selected_uv_set_pointer
            item_text = item.text()
            item.setFlags(item.flags() & ~Qt.ItemIsEnabled)

    def map_uv_sets(self):
        self.uv_sets_maps_all = []
        for uv_set in self.uv_sets_all:
            if uv_set != '---':
                uv_set_text_split = uv_set.split(":")
                uv_set_name = uv_set_text_split[1]
                if uv_set_name == 'map1':
                    if uv_set_name not in self.uv_sets_maps_all:
                        self.uv_sets_maps_all.append(uv_set)

    def populate_uv_set_editor_window(self):
        self.evaluate_textures_in_scene()
        self.evaluate_UV_sets_in_scene()
        self.clear_layout(self.textures_list_widget)
        self.clear_layout(self.uv_sets_list_widget)
        for texture in self.all_textures:
            if texture != 'gi_std_lgt' or texture != 'reflection_sdt_lgt' or texture != 'refraction_sdt_lgt':
                self.textures_list_widget.addItem(texture)
        for uv_set in self.uv_sets_all:
            if uv_set != 'polySurfaceShape' or uv_set != 'polySurfaceShape1' or uv_set != 'polySurfaceShape2':
                self.uv_sets_list_widget.addItem(uv_set)
        self.number_of_uv_sets_in_listWidget = self.uv_sets_list_widget.count()
        self.activate_uv_set_listWidget()

    def evaluate_textures_in_scene(self):
        file_textures_all = cmds.ls(type = 'file')
        #print 'file_textures_all = ',file_textures_all
        file_textures = []
        ramp_textures_all = cmds.ls(type = 'ramp')
        ramp_textures = []
        for file in file_textures_all:
            #print ' '
            #print 'file = ',file
            valid_file = 0
            if file == 'gi_std_lgt' or file == 'reflection_sdt_lgt' or file == 'refraction_sdt_lgt':
                valid_file = 0
            file_connections = cmds.listConnections(file,source = False)
            #print 'file_connections = ',file_connections
            for connection in file_connections:
                #print 'connection = ',connection
                connection_type = cmds.nodeType(connection)
                #print 'connection_type = ',connection_type
                if connection_type == 'VRayMtl' or connection_type == 'phong' or connection_type == 'blend' or connection_type == 'layeredTexture' or connection_type == 'remapHsv' or connection_type == 'multiplyDivide' or connection_type == 'remapColor' or connection_type == 'VRayRenderElement':
                    valid_file = 1
            if valid_file == 1:
                #print 'adding ' + file + ' to list'
                file_textures.append(file)
        #print 'file_textures = ',file_textures
        for ramp in ramp_textures_all:
            light_ramp = 0
            ramp_connections = cmds.listConnections(ramp, source = False) or []
            for ramp_connection in ramp_connections:
                ramp_connection_type = cmds.nodeType(ramp_connection)
                if ramp_connection_type == 'transform':
                    ramp_connection_subs = cmds.listRelatives(ramp_connection,children = True)
                    for ramp_connection_sub in ramp_connection_subs:
                        ramp_connection_sub_type = cmds.nodeType(ramp_connection_sub)
                        if ramp_connection_sub_type == 'VRayLightRectShape':
                            light_ramp = 1
                else:
                    ramp_connections_1 = cmds.listConnections(ramp_connection, source = False) or []
                    for ramp_connection in ramp_connections_1:
                        ramp_connection_type = cmds.nodeType(ramp_connection)
                        if ramp_connection_type == 'transform':
                            ramp_connection_subs = cmds.listRelatives(ramp_connection,children = True)
                            for ramp_connection_sub in ramp_connection_subs:
                                ramp_connection_sub_type = cmds.nodeType(ramp_connection_sub)
                                if ramp_connection_sub_type == 'VRayLightRectShape':
                                    light_ramp = 1
                        else:
                            ramp_connections_2 = cmds.listConnections(ramp_connection, source = False) or []
                            for ramp_connection in ramp_connections_2:
                                ramp_connection_type = cmds.nodeType(ramp_connection)
                                if ramp_connection_type == 'transform':
                                    ramp_connection_subs = cmds.listRelatives(ramp_connection,children = True)
                                    for ramp_connection_sub in ramp_connection_subs:
                                        ramp_connection_sub_type = cmds.nodeType(ramp_connection_sub)
                                        if ramp_connection_sub_type == 'VRayLightRectShape':
                                            light_ramp = 1
                                else:
                                    ramp_connections_3 = cmds.listConnections(ramp_connection, source = False) or []
                                    for ramp_connection in ramp_connections_3:
                                        ramp_connection_type = cmds.nodeType(ramp_connection)
                                        if ramp_connection_type == 'transform':
                                            ramp_connection_subs = cmds.listRelatives(ramp_connection,children = True)
                                            for ramp_connection_sub in ramp_connection_subs:
                                                ramp_connection_sub_type = cmds.nodeType(ramp_connection_sub)
                                                if ramp_connection_sub_type == 'VRayLightRectShape':
                                                    light_ramp = 1
                                        else:
                                            ramp_connections_4 = cmds.listConnections(ramp_connection, source = False) or []
                                            for ramp_connection in ramp_connections_4:
                                                ramp_connection_type = cmds.nodeType(ramp_connection)
                                                if ramp_connection_type == 'transform':
                                                    ramp_connection_subs = cmds.listRelatives(ramp_connection,children = True)
                                                    for ramp_connection_sub in ramp_connection_subs:
                                                        ramp_connection_sub_type = cmds.nodeType(ramp_connection_sub)
                                                        if ramp_connection_sub_type == 'VRayLightRectShape':
                                                            light_ramp = 1
            if light_ramp == 0:
                ramp_textures.append(ramp)
        self.all_textures = file_textures + ramp_textures

    def evaluate_UV_sets_in_scene(self):
        self.uv_sets_all = []
        self.uv_set_name_to_address_dic = {}
        self.uv_set_selection_status_dic = {}
        transorms_objects = cmds.ls(type = 'shape')
        transorms_objects_tmp = transorms_objects
        for object in transorms_objects:
            cmds.select(clear = True)
            cmds.select(object)
            uv_sets = cmds.polyUVSet(allUVSets = True, query = True) or []
            number_of_uv_sets = len(uv_sets)
            if number_of_uv_sets > 1:
                self.uv_sets_all.append('---')
                for uv_set in uv_sets:
                    uv_sets_all_string = object + ':' + uv_set
                    self.uv_sets_all.append(uv_sets_all_string)
                    for texture in self.all_textures:
                        self.uv_set_selection_status_dic[texture + ':' + uv_sets_all_string] = 1
                number_of_uv_sets_for_object = len(uv_sets)
                it = 0
                while it <= number_of_uv_sets_for_object:
                    i = 0
                    for uv_set in uv_sets:
                        uv_set_address = object + '.uvSet[' + str(i) + '].uvSetName'
                        self.uv_set_name_to_address_dic[object + ':' + uv_set] = uv_set_address
                        i = i + 1
                    it = it + 1
        self.map_uv_sets()

#---------- UV set selection methods ----------

    def texture_press(self,item):
        self.deselect_QListWidget(self.uv_sets_list_widget)
        self.texture_linked_uv_sets = []
        self.selected_texture_text = item.text()
        self.activate_uv_set_listWidget()
        uv_set_addresses_linked_to_selected_texture = cmds.uvLink( query = True, texture = self.selected_texture_text)
        number_of_linked_uv_sets = len(uv_set_addresses_linked_to_selected_texture)
        for uv_set_name_to_address in self.uv_set_name_to_address_dic:
            uv_set_address = self.uv_set_name_to_address_dic[uv_set_name_to_address]
            if uv_set_address in uv_set_addresses_linked_to_selected_texture:
                self.texture_linked_uv_sets.append(uv_set_name_to_address)
        self.update_uv_set_listWidget()

    def update_uv_set_listWidget(self):
        self.deselect_QListWidget(self.uv_sets_list_widget)
        self.unlock_uv_sets_QListWidget()
        it = 0
        while it < self.number_of_uv_sets_in_listWidget:
            item = self.uv_sets_list_widget.item(it)
            item_text = item.text()
            if item_text == '---':
                item.setTextColor(QtGui.QColor("#858585"))
            if item_text != '---':
                item_text_split = item_text.split(":")
                item_text_name = item_text_split[1]
                item_text_object = item_text_split[0]
                item_text_selection_status = self.uv_set_selection_status_dic[self.selected_texture_text + ':' + item_text]
                linked_uv_set_object = ''
                for linked_uv_set in self.texture_linked_uv_sets:
                    if linked_uv_set == item_text:
                        linked_uv_set_split = linked_uv_set.split(":")
                        linked_uv_set_object = linked_uv_set_split[0]
                        item.setSelected(True)
                        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                if item_text_object != linked_uv_set_object:
                    if item_text_selection_status == 0:
                        item.setSelected(False)
                    if item_text_selection_status == 1:
                        item.setSelected(True)
            it = it + 1

    def uv_set_listWidget_conflict_detect(self):
        selected_uv_sets_pointers = self.uv_sets_list_widget.selectedItems()
        uv_set_pointers = []
        selected_uv_set_pointers = []
        selected_uv_set_names = []
        uv_set_object_name_dic = {}
        uv_set_pointer_dic = {}
        it = 0
        while it < self.number_of_uv_sets_in_listWidget:
            item = self.uv_sets_list_widget.item(it)
            uv_set_pointers.append(item)
            item_text = item.text()
            uv_set_split = item_text.split(':')
            uv_set_object_name = uv_set_split[0]
            uv_set_object_name_dic[item_text] = uv_set_object_name
            it = it + 1
        for selected_uv_set_pointer in selected_uv_sets_pointers:
            selected_uv_set_pointers.append(selected_uv_set_pointer)
            it_text = selected_uv_set_pointer.text()
            selected_uv_set_names.append(it_text)
            selected_uv_set_split = it_text.split(':')
            selected_uv_set_object_name = selected_uv_set_split[0]
            for uv_set_pointer in uv_set_pointers:
                if str(uv_set_pointer) != str(selected_uv_set_pointer):
                    uv_set_name = uv_set_pointer.text()
                    object_name = uv_set_object_name_dic[uv_set_name]
                    if object_name == selected_uv_set_object_name:
                        uv_set_pointer.setSelected(False)
                        self.uv_set_selection_status_dic[self.selected_texture_text + ':' + uv_set_name] = 0
            self.unlock_uv_sets_QListWidget()
            selected_uv_set_pointer.setSelected(True)
            self.uv_set_selection_status_dic[self.selected_texture_text + ':' + it_text] = 1

    def link_texture_to_uv_set(self):
        selected_uv_sets = []
        self.uv_set_listWidget_conflict_detect()
        selected_uv_set_pointers = self.uv_sets_list_widget.selectedItems()
        for pointer in selected_uv_set_pointers:
            uv_set_text = pointer.text()
            selected_uv_sets.append(uv_set_text)
        for uv_set_name_to_address in self.uv_set_name_to_address_dic:
            for selected_uv_set in selected_uv_sets:
                if selected_uv_set == uv_set_name_to_address:
                    texture_linked_uv_set_address = self.uv_set_name_to_address_dic[selected_uv_set]
                    cmds.uvLink(make = True, uvSet = texture_linked_uv_set_address,texture = self.selected_texture_text)
        self.lock_selected_uv_sets_QListWidget()

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
        window.setFixedSize(600,200)
        main_vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        label_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(label_layout)
        texture_label = QtWidgets.QLabel('textures')
        uv_set_label = QtWidgets.QLabel('uv sets')
        label_layout.addWidget(texture_label)
        label_layout.addWidget(uv_set_label)
        self.textures_list_widget_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.textures_list_widget_layout)
        self.uv_sets_list_widget_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.uv_sets_list_widget_layout)
        self.textures_list_widget = QtWidgets.QListWidget()
        self.textures_list_widget.itemClicked.connect(partial(self.texture_press))
        self.textures_list_widget.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
        self.textures_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textures_list_widget_layout.addWidget(self.textures_list_widget)
        self.uv_sets_list_widget = QtWidgets.QListWidget()
        self.uv_sets_list_widget.setSelectionMode(self.uv_sets_list_widget.MultiSelection)
        self.uv_sets_list_widget.selectionModel().selectionChanged.connect(self.link_texture_to_uv_set)
        self.uv_sets_list_widget.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
        self.uv_sets_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textures_list_widget_layout.addWidget(self.uv_sets_list_widget)
        self.populate_uv_set_editor_window()
        self.uv_set_listWidget_conflict_detect()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    uv_set_editor = UV_SET_EDITOR()
    uv_set_editor.texture_linker_UI()
main()
