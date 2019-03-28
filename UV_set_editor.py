import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
print 'UV_set_editor'

class UV_SET_EDITOR(object):
    def __init__(self):
        proxy = ''

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())

    def evaluate_UV_sets_in_scene(self):
        print 'gather_UV_sets_in_scene'
        self.uv_sets_all = []
        self.uv_sets_all_dic = {}
        transorms_objects = cmds.ls(type = 'transform')
        for object in transorms_objects:
            cmds.select(clear = True)
            cmds.select(object)
            uv_sets = cmds.polyUVSet(allUVSets = True, query = True) or []
            for uv_set in uv_sets:
                uv_sets_all_string = uv_set + ':' + object
                self.uv_sets_all.append(uv_sets_all_string)
                self.uv_sets_all_dic[object] = uv_set

    def evaluate_textures_in_scene(self):
        file_textures = cmds.ls(type = 'file')
        self.all_textures = file_textures

    def uv_sets_linked_to_texture(self):
        print self.uv_sets_all
        print self.all_textures
        self.texture_uv_set_dic = {}
        for texture in self.all_textures:
            uv_links = cmds.uvLink( query = True, texture = texture )
            self.texture_uv_set_dic[texture] = uv_links
        print self.texture_uv_set_dic

    def populate_uv_set_editor_window(self):
        self.clear_layout(self.textures_list_widget)
        self.clear_layout(self.uv_sets_list_widget)
        for texture in self.all_textures:
            self.textures_list_widget.addItem(texture)
        for uv_set in self.uv_sets_all:
            self.uv_sets_list_widget.addItem(uv_set)

    def texture_press(self,item):
        id_numbers = []
        self.uv_set_used_from_id_number_all = []
        item_text = item.text()
        uv_sets_used_by_clicked_texture = cmds.uvLink(query=True, texture = item_text)
        for uv_set in uv_sets_used_by_clicked_texture:
            id_number_split_1 = uv_set.split('[')
            id_number_split_1 = id_number_split_1[1]
            id_number_split_2 = id_number_split_1.split(']')
            id_number_split_2 = id_number_split_2[0]
            id_number = id_number_split_2
            id_numbers.append(id_number)
        for id in id_numbers:
            uv_set_used_from_id_number = self.uv_sets_all[int(id)]
            self.uv_set_used_from_id_number_all.append(uv_set_used_from_id_number)
            for uv_set in self.uv_set_used_from_id_number_all:
                print uv_set
        self.update_uv_set_listWidget()

    def update_uv_set_listWidget(self):
        for index in range(self.uv_sets_list_widget.count()):
            item = self.uv_sets_list_widget.item(index)
            item_text = item.text()
            for uv_set in self.uv_set_used_from_id_number_all:
                if item_text == uv_set:
                    print 'item_text = ',item_text
                    item.setBackground( QColor('red') )             

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
        self.uv_sets_list_widget.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
        self.uv_sets_list_widget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.textures_list_widget_layout.addWidget(self.uv_sets_list_widget)
        #self.texture_thumbnails_listWidget.setIconSize(QtCore.QSize(214, 214))
        #self.texture_thumbnails_listWidget.setViewMode(QtWidgets.QListView.IconMode)
        #self.textures_listWidget.itemDoubleClicked.connect(self.fCheckLaunch)
        #self.textures_listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        #swap_textures_button = QtWidgets.QPushButton('swap textures')
        #swap_textures_button.setFixedHeight(50)
        #swap_textures_button.setStyleSheet("background-color:rgb(105,110,120)")
        #swap_textures_button.setFont(QtGui.QFont('SansSerif', 12))
        #main_vertical_layout.addWidget(swap_textures_button)
        #swap_textures_button.pressed.connect(partial(self.texture_replace))
        self.populate_uv_set_editor_window()
        fg = window.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        window.move(fg.topLeft())
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.myScriptJobID = cmds.scriptJob(p = window_name, event=["SelectionChanged", self.populate_texture_window])
        window.show()

def main():
    uv_set_editor = UV_SET_EDITOR()
    uv_set_editor.evaluate_UV_sets_in_scene()
    uv_set_editor.evaluate_textures_in_scene()
    uv_set_editor.uv_sets_linked_to_texture()
    uv_set_editor.texture_linker_UI()
main()
