import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

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
                #item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
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
            self.textures_list_widget.addItem(texture)
        for uv_set in self.uv_sets_all:
            self.uv_sets_list_widget.addItem(uv_set)
        self.number_of_uv_sets_in_listWidget = self.uv_sets_list_widget.count()
        self.activate_uv_set_listWidget()

    def evaluate_textures_in_scene(self):
        file_textures = cmds.ls(type = 'file')
        ramp_textures = cmds.ls(type = 'ramp')
        self.all_textures = file_textures + ramp_textures

    def evaluate_UV_sets_in_scene(self):
        self.uv_sets_all = []
        self.uv_set_name_to_address_dic = {}
        transorms_objects = cmds.ls(type = 'shape')
        for object in transorms_objects:
            cmds.select(clear = True)
            cmds.select(object)
            uv_sets = cmds.polyUVSet(allUVSets = True, query = True) or []
            for uv_set in uv_sets:
                uv_sets_all_string = object + ':' + uv_set
                self.uv_sets_all.append(uv_sets_all_string)
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
        #print 'texture_press '
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
        #print 'update_uv_set_listWidget '
        self.deselect_QListWidget(self.uv_sets_list_widget)
        self.unlock_uv_sets_QListWidget()
        it = 0
        while it < self.number_of_uv_sets_in_listWidget:
            item = self.uv_sets_list_widget.item(it)
            item_text = item.text()
            for uv_set in self.texture_linked_uv_sets:
                if uv_set == item_text:
                    uv_set_split = uv_set.split(":")
                    uv_set_object = uv_set_split[0]
                    item.setSelected(True)
                    item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                    for uv_set_map1 in self.uv_sets_maps_all:
                        uv_set_map1_split = uv_set_map1.split(":")
                        uv_set_map1_name = uv_set_map1_split[1]
                        uv_set_map1_object = uv_set_map1_split[0]
                        if uv_set_map1_object != uv_set_object:
                            it = 0
                            while it < self.number_of_uv_sets_in_listWidget:
                                item = self.uv_sets_list_widget.item(it)
                                item_text = item.text()
                                if item_text == uv_set_map1:
                                    item.setSelected(True)
                                it = it + 1
            it = it + 1

    def uv_set_listWidget_conflict_detect(self):
        #print 'uv_set_listWidget_conflict_detect '
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
            self.unlock_uv_sets_QListWidget()
            selected_uv_set_pointer.setSelected(True)
            #self.lock_selected_uv_sets_QListWidget()

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
