"""
lighting_shelf: texture_swap
********************************************
"""

import maya.mel as mel
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
from functools import partial

class texture_replacer():

    def __init__(self):
        chris = ''

    def fCheckLaunch(self,curr):
        fCheckText = curr.text()
        if fCheckText != "":
            fCheckTexPath = self.textures_for_swap_dic[fCheckText]
            cmds.fcheck(fCheckTexPath)

    def populate_texture_window(self):
        self.texture_thumbnails_listWidget.clear()
        placement_range_for_arrow = [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88,90,92,94,96,98,100]
        self.textures_for_swap = []
        self.textures_for_swap_dic = {}
        texture_selections = cmds.ls(sl = True)
        for selection in texture_selections:
            node_type = cmds.nodeType(selection)
            if node_type == 'file':
              self.textures_for_swap.append(selection)
        i = 0
        for texture in self.textures_for_swap:
            self.arrowPath = QtGui.QPixmap("U:/cwinters/thumbnails/arrow.jpg")
            #arrow_scale_amount_width = 30
            #arrow_scale_amount_height = 134
            arrowItem = QtWidgets.QListWidgetItem()
            arrowPixmap = QtGui.QPixmap(self.arrowPath)
            #arrowPixmap = arrowPixmap.scaled(arrow_scale_amount_width,arrow_scale_amount_height)
            arrowIcon = QtGui.QIcon()
            arrowIcon.addPixmap(arrowPixmap)
            arrowItem.setIcon(arrowIcon)
            image_name_path = cmds.getAttr(texture + '.fileTextureName')
            self.textures_for_swap_dic[texture] = image_name_path
            texture_item = QtWidgets.QListWidgetItem(texture)
            texture_pixmap = QtGui.QPixmap(image_name_path)
            texture_icon = QtGui.QIcon()
            texture_icon.addPixmap(texture_pixmap)
            texture_item.setIcon(texture_icon)
            texture_item.setFont(QtGui.QFont('SansSerif', 10))
            texture_item.setFlags(texture_item.flags() &~ QtCore.Qt.ItemIsSelectable)
            arrowItem.setFlags(arrowItem.flags() &~ QtCore.Qt.ItemIsSelectable)
            if i in placement_range_for_arrow:
                self.texture_thumbnails_listWidget.addItem(texture_item)
                self.texture_thumbnails_listWidget.addItem(arrowItem)
            else:
                self.texture_thumbnails_listWidget.addItem(texture_item)
            i = i + 1

    def texture_linker_UI(self):
        window_name = "texture_swap"
        if cmds.window(window_name,exists = True):
            cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(window_name)
        window.setWindowTitle(window_name)
        main_widget = QtWidgets.QWidget()
        window.setCentralWidget(main_widget)
        window.setFixedSize(500,700)
        main_vertical_layout = QtWidgets.QVBoxLayout(main_widget)
        self.texture_thumbnails_listWidget = QtWidgets.QListWidget()
        self.texture_thumbnails_listWidget.setStyleSheet('QListWidget {background-color: #292929; color: #B0E0E6;}')
        self.texture_thumbnails_listWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.texture_thumbnails_listWidget.setIconSize(QtCore.QSize(214, 214))
        self.texture_thumbnails_listWidget.setViewMode(QtWidgets.QListView.IconMode)
        main_vertical_layout.addWidget(self.texture_thumbnails_listWidget)
        self.texture_thumbnails_listWidget.itemDoubleClicked.connect(self.fCheckLaunch)
        self.texture_thumbnails_listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        swap_textures_button = QtWidgets.QPushButton('swap textures')
        swap_textures_button.setFixedHeight(50)
        swap_textures_button.setStyleSheet("background-color:rgb(105,110,120)")
        swap_textures_button.setFont(QtGui.QFont('SansSerif', 12))
        main_vertical_layout.addWidget(swap_textures_button)
        swap_textures_button.pressed.connect(partial(self.texture_replace))
        self.populate_texture_window()
        fg = window.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        window.move(fg.topLeft())
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.myScriptJobID = cmds.scriptJob(p = window_name, event=["SelectionChanged", self.populate_texture_window])
        window.show()

    def texture_replace(self):
        number_of_textures = len(self.textures_for_swap)
        i = 0
        while i < number_of_textures:
          #splitting out the old and new texture names
          new_fileTex = self.textures_for_swap[i]
          old_fileTex = self.textures_for_swap[i+1]
          print " "
          print new_fileTex + " swapping with " + old_fileTex
          #print "---"
          #starting the replace
          source_connections_modified = []
          destination_connections_modified = []
          #grab the old texure incoming connections
          connections_source_old = cmds.listConnections(old_fileTex, plugs = True, connections = True, destination = False)or []
          #grab the old texure outgoing connections
          connections_destination_old = cmds.listConnections(old_fileTex, connections = True, plugs = True, source = False) or []
          #how many incoming connections and outgoing connections are there
          connection_source_size = len(connections_source_old)
          connection_destination_size = len(connections_destination_old)
          #if the incoming connections source size is more than 0, replace the old texture in the incoming connections list
          if connection_source_size != 0:
              for connection in connections_source_old:
                  connection_modified = connection.replace(old_fileTex,new_fileTex)
                  source_connections_modified.append(connection_modified)
          #if the outgoing connections size is more than 0, replace the old texture in the outgoing connections list
          if connection_destination_size != 0:
              for connection in connections_destination_old:
                  connection_modified = connection.replace(old_fileTex,new_fileTex)
                  destination_connections_modified.append(connection_modified)
          source_connections_modified_size = len(source_connections_modified)
          #connect the old source node to the new texture
          inIter = 0
          outIter = 1
          while outIter < source_connections_modified_size:
              if connections_source_old[outIter] != "defaultColorMgtGlobals.cmEnabled" and connections_source_old[outIter] != "defaultColorMgtGlobals.configFileEnabled" and connections_source_old[outIter] != "defaultColorMgtGlobals.configFilePath" and connections_source_old[outIter] != "defaultColorMgtGlobals.workingSpaceName":
                  #print "connecting " + connections_source_old[outIter] + " to "  + source_connections_modified[inIter]
                  cmds.connectAttr(connections_source_old[outIter],source_connections_modified[inIter],force = True)
              outIter = outIter + 2
              inIter = inIter + 2
          destination_connections_modified_size = len(destination_connections_modified)
          #connect the new texture to the old destination node
          inIter = 0
          outIter = 1
          while outIter < destination_connections_modified_size:
              if ".message" not in destination_connections_modified[inIter]:
                  #print "connecting " + destination_connections_modified[inIter] + " to " + connections_destination_old[outIter]
                  cmds.connectAttr(destination_connections_modified[inIter],connections_destination_old[outIter], force = True)
              outIter = outIter + 2
              inIter = inIter + 2
          #transferAttr settings for new texture
          old_file_texture_attr_dic = {}
          new_file_texture_attr_dic = {}
          old_file_texture_attrs = cmds.listAttr(old_fileTex,k = True)
          attrAppend = ["filter","filterOffset","filterType"]
          attrRemove = ["aiUserOptions","defaultColorMgtGlobals.cmEnabled","defaultColorMgtGlobals.configFileEnabled","defaultColorMgtGlobals.configFilePath","workingSpaceName"]
          for attr in attrAppend:
              old_file_texture_attrs.append(attr)
          for attr in attrRemove:
              if attr in old_file_texture_attrs:
                  old_file_texture_attrs.remove(attr)
          new_file_texture_attrs = cmds.listAttr(new_fileTex,k = True)
          for attr in attrAppend:
              new_file_texture_attrs.append(attr)
          for attr in attrRemove:
              if attr in new_file_texture_attrs:
                  new_file_texture_attrs.remove(attr)
          for oldFileAttr in old_file_texture_attrs:
              oldFileAttrValue = cmds.getAttr(old_fileTex + "." + oldFileAttr)
              old_file_texture_attr_dic[oldFileAttr] = oldFileAttrValue
          for new_fileTexAttr in new_file_texture_attrs:
              new_fileTexAttr_Value = cmds.getAttr(new_fileTex + "." + new_fileTexAttr)
              new_file_texture_attr_dic[new_fileTexAttr] = new_fileTexAttr_Value
          for new_fileTexAttr in new_file_texture_attrs:
              if new_fileTexAttr in new_file_texture_attr_dic:
                  attrExists = cmds.attributeQuery(new_fileTexAttr,node = new_fileTex,exists = True)
                  if attrExists == 1:
                      #print "setting " + str(new_fileTex) + "." + str(new_fileTexAttr) + " to " + str(old_file_texture_attr_dic[new_fileTexAttr])
                      cmds.setAttr(new_fileTex + "." + new_fileTexAttr,old_file_texture_attr_dic[new_fileTexAttr])
          i = i + 2
        cmds.select(clear = True)
        self.texture_thumbnails_listWidget.clear()
        new_fileTex = ''
        old_fileTex = ''

def main():
    swap = texture_replacer()
    swap.texture_linker_UI()

#main()
