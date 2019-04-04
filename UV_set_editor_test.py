import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

print 'UV set editor test night'

class UV_SET_EDITOR(object):
    def __init__(self):
        self.selected_item_text = ''

#---------- procedural tools and data gathering methods ----------

    def centric_state(self):
        self.centric_state_text = self.texture_based_uv_set_based_combobox.currentText()
        self.right_label.setText('textures')
        if self.centric_state_text == 'texture-centric':
            self.left_label.setText('textures')
            self.right_label.setText('uv sets')
        if self.centric_state_text == 'UV-centric':
            self.left_label.setText('uv sets')
            self.right_label.setText('textures')
        self.selected_item_text = ''
        self.populate_windows()

    def deselect_QListWidget(self,listwidget):
        print ' '
        print 'xxx'
        print 'deselect right list widget items()'
        for i in range(listwidget.count()):
            item = listwidget.item(i)
            listwidget.setItemSelected(item, False)

    def activate_right_listWidget(self):
        print ' '
        print 'xxx'
        print 'activate_right_listWidget()'
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
            self.list_widget_right.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item.setFlags(item.flags() | Qt.ItemIsEnabled)
                item.setFlags(item.flags() | Qt.ItemIsEditable)
                it = it + 1

    def unlock_right_QListWidget(self):
        print ' '
        print 'xxx'
        print 'unlock_right_QListWidget()'
        if self.centric_state_text == 'texture-centric':
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
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

    def lock_selected_right_QListWidget(self):
        print ' '
        print 'xxx'
        print 'lock_selected_right_QListWidget()'
        if self.centric_state_text == 'texture-centric':
            self.unlock_right_QListWidget()
            selected_uv_sets_pointers = self.list_widget_right.selectedItems()
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

    def populate_windows(self):
        print ' '
        print 'xxx'
        print 'populate_windows()'
        self.evaluate_textures_in_scene()
        self.evaluate_UV_sets_in_scene()
        self.list_widget_left.clear()
        self.list_widget_right.clear()
        if self.centric_state_text == 'texture-centric':
            for texture in self.all_textures:
                self.list_widget_left.addItem(texture)
            for uv_set in self.uv_sets_all:
                self.list_widget_right.addItem(uv_set)
            self.number_of_items_in_left_listWidget = self.list_widget_left.count()
            self.number_of_items_in_right_listWidget = self.list_widget_right.count()
            self.activate_right_listWidget()
        if self.centric_state_text == 'UV-centric':
            for texture in self.all_textures:
                self.list_widget_right.addItem(texture)
            for uv_set in self.uv_sets_all:
                self.list_widget_left.addItem(uv_set)
            self.number_of_items_in_left_listWidget = self.list_widget_left.count()
            self.number_of_items_in_right_listWidget = self.list_widget_right.count()
            i = 0
            while i < self.number_of_items_in_left_listWidget:
                item = self.list_widget_left.item(i)
                item_text = item.text()
                if item_text == '---':
                    item.setTextColor(QtGui.QColor("#858585"))
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                i = i + 1
            self.activate_right_listWidget()

    def evaluate_textures_in_scene(self):
        print ' '
        print 'xxx'
        print 'evaluate_textures_in_scene()'
        file_textures_all = cmds.ls(type = 'file')
        file_textures = []
        ramp_textures_all = cmds.ls(type = 'ramp')
        ramp_textures = []
        for file in file_textures_all:
            valid_file = 0
            if file == 'gi_std_lgt' or file == 'reflection_sdt_lgt' or file == 'refraction_sdt_lgt':
                valid_file = 0
            file_connections = cmds.listConnections(file,source = False) or []
            for connection in file_connections:
                connection_type = cmds.nodeType(connection)
                if connection_type == 'VRayMtl' or connection_type == 'phong' or connection_type == 'blend' or connection_type == 'layeredTexture' or connection_type == 'remapHsv' or connection_type == 'multiplyDivide' or connection_type == 'remapColor' or connection_type == 'VRayRenderElement':
                    valid_file = 1
            if valid_file == 1:
                file_textures.append(file)
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
        print ' '
        print 'xxx'
        print 'evaluate_UV_sets_in_scene()'
        self.uv_sets_all = []
        self.uv_set_name_to_address_dic = {}
        self.uv_set_selection_status_dic = {}
        transorms_objects = cmds.ls(type = 'shape')
        transorms_objects_tmp = transorms_objects
        for object in transorms_objects:
            if object != 'polySurfaceShape' and object != 'polySurfaceShape1' and object != 'polySurfaceShape2 ' and object != 'polySurfaceShape3' and object != 'polySurfaceShape4' and object != 'polySurfaceShape5':
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
                            if self.centric_state_text == 'texture-centric':
                                self.uv_set_selection_status_dic[texture + ':' + uv_sets_all_string] = 1
                            if self.centric_state_text == 'UV-centric':
                                self.uv_set_selection_status_dic[texture + ':' + uv_sets_all_string] = 0
                    number_of_uv_sets_for_object = len(uv_sets)
                    it = 0
                    while it <= number_of_uv_sets_for_object:
                        i = 0
                        for uv_set in uv_sets:
                            uv_set_address = object + '.uvSet[' + str(i) + '].uvSetName'
                            self.uv_set_name_to_address_dic[object + ':' + uv_set] = uv_set_address
                            i = i + 1
                        it = it + 1
        #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        #print 'self.uv_set_name_to_address_dic = ',self.uv_set_name_to_address_dic
        self.map_uv_sets()

#---------- UV set selection methods ----------

    def item_press(self,item):
        print ' '
        print 'xxx'
        print 'ITEM PRESS()'
        if self.centric_state_text == 'texture-centric':
            self.deselect_QListWidget(self.list_widget_right)
            self.texture_linked_uv_sets = []
            self.selected_item_text = item.text()
            self.activate_right_listWidget()
            uv_set_addresses_linked_to_selected_texture = cmds.uvLink( query = True, texture = self.selected_item_text)
            number_of_linked_uv_sets = len(uv_set_addresses_linked_to_selected_texture)
            for uv_set_name_to_address in self.uv_set_name_to_address_dic:
                uv_set_address = self.uv_set_name_to_address_dic[uv_set_name_to_address]
                if uv_set_address in uv_set_addresses_linked_to_selected_texture:
                    self.texture_linked_uv_sets.append(uv_set_name_to_address)
            self.update_right_listWidget()
        #if self.centric_state_text == 'UV-centric':
            #print 'uv_centric press'
            #self.selected_item_text = item.text()
            #print 'self.selected_item_text = ',self.selected_item_text
            #self.activate_right_listWidget()
            #selected_uv_set_address = self.uv_set_name_to_address_dic[self.selected_item_text]
            #print 'selected_uv_set_address = ',selected_uv_set_address
            #self.textures_linked_to_selected_uv_set = cmds.uvLink( query=True, uvSet = selected_uv_set_address)
            #print 'self.textures_linked_to_selected_uv_set = ',self.textures_linked_to_selected_uv_set
            #self.update_right_listWidget()

    def update_right_listWidget(self):
        print ' '
        print 'xxx'
        print 'update_right_listWidget()'
        print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
        if self.centric_state_text == 'texture-centric':
            self.deselect_QListWidget(self.list_widget_right)
            self.unlock_right_QListWidget()
            it = 0
            while it < self.number_of_items_in_right_listWidget:
                item = self.list_widget_right.item(it)
                item_text = item.text()
                if item_text == '---':
                    item.setTextColor(QtGui.QColor("#858585"))
                if item_text != '---':
                    item_text_split = item_text.split(":")
                    item_text_name = item_text_split[1]
                    item_text_object = item_text_split[0]
                    #print 'self.selected_item_text = ',self.selected_item_text
                    #print 'item_text = ',item_text
                    item_text_selection_status = self.uv_set_selection_status_dic[self.selected_item_text + ':' + item_text]
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
        #if self.centric_state_text == 'UV-centric':
            #self.deselect_QListWidget(self.list_widget_right)
            #it = 0
            #while it < self.number_of_items_in_right_listWidget:
                #item = self.list_widget_right.item(it)
                #item_text = item.text()
                #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
                #print 'self.selected_item_text = ',self.selected_item_text
                #print 'item_text = ',item_text
                #item_text_selection_status = self.uv_set_selection_status_dic[item_text + ":" + self.selected_item_text]
                #print 'item_text_selection_status = ',item_text_selection_status
                #linked_uv_set_object = ''
                #for texture in self.textures_linked_to_selected_uv_set:
                    #if texture == item_text:
                        #print 'item_text_selection_status = ',item_text_selection_status
                        #if item_text_selection_status == 0:
                            #print 'setting ' + item_text + ' to unselected'
                            #item.setSelected(False)
                        #if item_text_selection_status == 1:
                            #print 'setting ' + item_text + ' to selected'
                            #item.setSelected(True)
                #it = it + 1
        #print 'self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic

    def right_listWidget_conflict_detect(self):
        print ' '
        print 'xxx'
        print 'right_listWidget_conflict_detect()'
        selected_uv_sets_pointers = self.list_widget_right.selectedItems()
        uv_set_pointers = []
        selected_right_pointers = []
        selected_uv_set_names = []
        uv_set_object_name_dic = {}
        uv_set_pointer_dic = {}
        it = 0
        while it < self.number_of_items_in_right_listWidget:
            item = self.list_widget_right.item(it)
            uv_set_pointers.append(item)
            item_text = item.text()
            uv_set_split = item_text.split(':')
            uv_set_object_name = uv_set_split[0]
            uv_set_object_name_dic[item_text] = uv_set_object_name
            it = it + 1
        for selected_uv_set_pointer in selected_uv_sets_pointers:
            selected_right_pointers.append(selected_uv_set_pointer)
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
                        self.uv_set_selection_status_dic[self.selected_item_text + ':' + uv_set_name] = 0
            self.unlock_right_QListWidget()
            selected_uv_set_pointer.setSelected(True)
            self.uv_set_selection_status_dic[self.selected_item_text + ':' + it_text] = 1
        print 'uv_set_selection_status_dic = ',self.uv_set_selection_status_dic

    def link_texture_to_uv_set(self):
        print ' '
        print 'xxx'
        print 'link_texture_to_uv_set()'
        if self.centric_state_text == 'texture-centric':
            selected_uv_sets = []
            self.right_listWidget_conflict_detect()
            selected_right_pointers = self.list_widget_right.selectedItems()
            for pointer in selected_right_pointers:
                pointer_text = pointer.text()
                selected_uv_sets.append(pointer_text)
            for uv_set_name_to_address in self.uv_set_name_to_address_dic:
                for selected_uv_set in selected_uv_sets:
                    if selected_uv_set == uv_set_name_to_address:
                        texture_linked_uv_set_address = self.uv_set_name_to_address_dic[selected_uv_set]
                        cmds.uvLink(make = True, uvSet = texture_linked_uv_set_address,texture = self.selected_item_text)
            self.lock_selected_right_QListWidget()
        #if self.centric_state_text == 'UV-centric':
            #selected_textures = []
            #print 'link_texture_to_uv_set - UV-centric'
            #print '1 self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic
            #print 'selected uv set is ',self.selected_item_text
            #selected_right_pointers = self.list_widget_right.selectedItems()
            #print 'selected_right_pointers = ',selected_right_pointers
            #for selected_pointer in selected_right_pointers:
                #selected_pointer_text = selected_pointer.text()
                #selected_textures.append(selected_pointer_text)
                #print 'selected_pointer_text = ',selected_pointer_text
                #print 'setting ' + selected_pointer_text + ' to selected'
                #selected_pointer.setSelected(True)
                #self.uv_set_selection_status_dic[selected_pointer_text + ':' + self.selected_item_text] = 1
                #selected_uv_set_address = self.uv_set_name_to_address_dic[self.selected_item_text]
                #print 'linking ' + self.selected_item_text + ' to uv_set ' + selected_pointer_text
                #cmds.uvLink(make = True, uvSet = selected_uv_set_address,texture = selected_pointer_text)
            #i = 0
            #print '---'
            #print 'unselecting'
            #print 'uv set = ',self.selected_item_text
            #print 'selected_textures = ',selected_textures
            #while i < self.number_of_items_in_right_listWidget:
                #item = self.list_widget_right.item(i)
                #item_text = item.text()
                #print 'item_text =', item_text
                #if item_text not in selected_textures:
                    #selection_status = self.uv_set_selection_status_dic[item_text + ':' + self.selected_item_text]
                    #print 'selection_status = ',selection_status
                    #if selection_status == 0:
                        #print 'setting ' + item_text + ' to unselected'
                        #item.setSelected(False)
                        #print 'item_text = ', item_text
                        #print 'self.selected_item_text = ',self.selected_item_text
                        #print 'setting selection status of ' + (item_text + ':' + self.selected_item_text) + 'to 0'
                        #self.uv_set_selection_status_dic[item_text + ':' + self.selected_item_text] = 0
                        #uv_set_address = self.uv_set_name_to_address_dic[self.selected_item_text]
                        #print 'unlinking ' + item_text + 'from ' + self.selected_item_text
                        #cmds.uvLink(b = True, uvSet = uv_set_address,texture = item_text)
                    #else:
                        #item.setSelected(True)
                #i = i + 1
            #print '2 self.uv_set_selection_status_dic = ',self.uv_set_selection_status_dic

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
        window.setFixedSize(1000,300)
        main_vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        combo_box_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(combo_box_layout)
        self.label_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.label_layout)
        self.texture_based_uv_set_based_combobox = QtWidgets.QComboBox()
        self.texture_based_uv_set_based_combobox.setMaximumWidth(150)
        self.texture_based_uv_set_based_combobox.setMinimumHeight(18)
        combo_box_layout.setAlignment(QtCore.Qt.AlignLeft)
        combo_box_layout.addWidget(self.texture_based_uv_set_based_combobox)
        self.texture_based_uv_set_based_combobox.addItem("texture-centric")
        self.texture_based_uv_set_based_combobox.addItem("UV-centric")
        self.texture_based_uv_set_based_combobox.activated[str].connect(lambda:self.centric_state())
        self.centric_state_text = self.texture_based_uv_set_based_combobox.currentText()
        self.left_label = QtWidgets.QLabel('textures')
        self.right_label = QtWidgets.QLabel('uv sets')
        self.label_layout.addWidget(self.left_label)
        self.label_layout.addWidget(self.right_label)
        self.list_layout = QtWidgets.QHBoxLayout(main_widget)
        main_vertical_layout.addLayout(self.list_layout)
        self.list_widget_left = QtWidgets.QListWidget()
        self.list_widget_left.itemClicked.connect(partial(self.item_press))
        self.list_widget_left.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
        self.list_widget_left.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.list_layout.addWidget(self.list_widget_left)
        self.list_widget_right = QtWidgets.QListWidget()
        self.list_widget_right.setSelectionMode(self.list_widget_right.MultiSelection)
        self.list_widget_right.selectionModel().selectionChanged.connect(self.link_texture_to_uv_set)
        self.list_widget_right.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
        self.list_widget_right.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.list_layout.addWidget(self.list_widget_right)
        self.populate_windows()
        self.right_listWidget_conflict_detect()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    uv_set_editor = UV_SET_EDITOR()
    uv_set_editor.texture_linker_UI()
main()
