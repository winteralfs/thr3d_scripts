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

    def populate_texture_window(self):
        self.arrowPath = QtGui.QPixmap("U:/cwinters/thumbnails/_arrow.jpg")
        arrow_scale_amount_width = 30
        arrow_scale_amount_height = 134
        texture_scale_amount = 500
        arrowItem = QtWidgets.QListWidgetItem("")
        arrowPixmap = QtGui.QPixmap(self.arrowPath)
        arrowPixmap = arrowPixmap.scaled(arrow_scale_amount_width,arrow_scale_amount_height)
        arrowIcon = QtGui.QIcon()
        arrowIcon.addPixmap(arrowPixmap)
        arrowItem.setIcon(arrowIcon)
        print 'populate_texture_window'
        self.textures_for_swap = []
        self.textures_for_swap_dic = {}
        texture_selections = cmds.ls(sl = True)
        for selection in texture_selections:
            node_type = cmds.nodeType(selection)
            if node_type == 'file':
              self.textures_for_swap.append(selection)
            print 'textures_for_swap = ',self.textures_for_swap
        for texture in self.textures_for_swap:
            print 'texture = ',texture
            image_name_path = cmds.getAttr(texture + '.fileTextureName')
            print 'image_name_path = ',image_name_path
            self.textures_for_swap_dic[texture] = image_name_path
            texture_item = QtWidgets.QListWidgetItem(texture)
            texture_pixmap = QtGui.QPixmap(image_name_path)
            texture_pixmap_scaled = texture_pixmap.scaled(texture_scale_amount,texture_scale_amount)
            texture_icon = QtGui.QIcon()
            texture_icon.addPixmap(texture_pixmap_scaled)
            texture_item.setIcon(texture_icon)
            print 'adding texture'
            self.texture_thumbnails_listWidget.addItem(texture_item)
            print 'adding arrow'
            self.texture_thumbnails_listWidget.addItem(arrowItem)
        print self.textures_for_swap_dic

    def texture_linker_UI(self):
        windowName = "texture_swap"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        window.setMinimumSize(450,650)
        window.setMaximumSize(450,650)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        main_vertical_layout = QtWidgets.QVBoxLayout(mainWidget)
        self.texture_thumbnails_listWidget = QtWidgets.QListWidget()
        main_vertical_layout.addWidget(self.texture_thumbnails_listWidget)
        #button_layout = QtWidgets.QVBoxLayout()
        #main_vertical_layout.addLayout(button_layout)
        bob = QtWidgets.QPushButton('bob textures')
        #swap_textures_button.setStyleSheet("background-color:rgb(10,100,255)")
        #swap_textures_button.setFixedHeight(50)
        main_vertical_layout.addWidget(bob)
        #print 'swap_textures_button = ',swap_textures_button
        bob.clicked.connect(partial(self.texture_replace))
        #self.populate_texture_window()
        #fg = window.frameGeometry()
        #cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        #fg.moveCenter(cp)
        #window.move(fg.topLeft())
        #window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        #self.texture_replace()
        window.show()

    def texture_replace(self):
        print 'bob'
        #print 'self.textures_for_swap = ',self.textures_for_swap
        #for texture_pair in self.textures_for_swap:
          #splitting out the old and new texture names
          #new_fileTex = self.textures_for_swap[0]
          #old_fileTex = self.textures_for_swap[1]
          #print " "
          #print "---"
          #print "textures_for_swap = ",self.textures_for_swap
          #print new_fileTex + " swapping " + old_fileTex
          #print "---"
          #starting the replace
          #source_connections_modified = []
          #destination_connections_modified = []
          ##grab the old texure incoming connections
          #connections_source_old = cmds.listConnections(old_fileTex, plugs = True, connections = True, destination = False)or []
          ##grab the old texure outgoing connections
          #connections_destination_old = cmds.listConnections(old_fileTex, connections = True, plugs = True, source = False) or []
          ##how many incoming connections and outgoing connections are there
          #connection_source_size = len(connections_source_old)
          #connection_destination_size = len(connections_destination_old)
          ##if the incoming connections source size is more than 0, replace the old texture in the incoming connections list
          #if connection_source_size != 0:
             # for connection in connections_source_old:
                 # connection_modified = connection.replace(old_fileTex,new_fileTex)
                 # source_connections_modified.append(connection_modified)
          #if the outgoing connections size is more than 0, replace the old texture in the outgoing connections list
          #if connection_destination_size != 0:
             # for connection in connections_destination_old:
                 # connection_modified = connection.replace(old_fileTex,new_fileTex)
                  #destination_connections_modified.append(connection_modified)
          #source_connections_modified_size = len(source_connections_modified)
          #connect the old source node to the new texture
          #inIter = 0
          #outIter = 1
          #while outIter < source_connections_modified_size:
             # if connections_source_old[outIter] != "defaultColorMgtGlobals.cmEnabled" and connections_source_old[outIter] != "defaultColorMgtGlobals.configFileEnabled" and connections_source_old[outIter] != "defaultColorMgtGlobals.configFilePath" and connections_source_old[outIter] != "defaultColorMgtGlobals.workingSpaceName":
                 # print "connecting " + connections_source_old[outIter] + " to "  + source_connections_modified[inIter]
                 # cmds.connectAttr(connections_source_old[outIter],source_connections_modified[inIter],force = True)
              #outIter = outIter + 2
              #inIter = inIter + 2
          #destination_connections_modified_size = len(destination_connections_modified)
          #connect the new texture to the old destination node
          #inIter = 0
          #outIter = 1
          #while outIter < destination_connections_modified_size:
             # if ".message" not in destination_connections_modified[inIter]:
                  #print "connecting " + destination_connections_modified[inIter] + " to " + connections_destination_old[outIter]
                  #cmds.connectAttr(destination_connections_modified[inIter],connections_destination_old[outIter], force = True)
              #outIter = outIter + 2
              #inIter = inIter + 2
          #transferAttr settings for new texture
          #old_file_texture_attr_dic = {}
          #new_file_texture_attr_dic = {}
          #old_file_texture_attrs = cmds.listAttr(old_fileTex,k = True)
          #attrAppend = ["filter","filterOffset","filterType"]
          #attrRemove = ["aiUserOptions","defaultColorMgtGlobals.cmEnabled","defaultColorMgtGlobals.configFileEnabled","defaultColorMgtGlobals.configFilePath","workingSpaceName"]
          #for attr in attrAppend:
              #old_file_texture_attrs.append(attr)
          #for attr in attrRemove:
              #if attr in old_file_texture_attrs:
                  #old_file_texture_attrs.remove(attr)
          #new_file_texture_attrs = cmds.listAttr(new_fileTex,k = True)
          #for attr in attrAppend:
              #new_file_texture_attrs.append(attr)
          #for attr in attrRemove:
             # if attr in new_file_texture_attrs:
                 # new_file_texture_attrs.remove(attr)
          #for oldFileAttr in old_file_texture_attrs:
              #oldFileAttrValue = cmds.getAttr(old_fileTex + "." + oldFileAttr)
              #old_file_texture_attr_dic[oldFileAttr] = oldFileAttrValue
          #for new_fileTexAttr in new_file_texture_attrs:
              #new_fileTexAttr_Value = cmds.getAttr(new_fileTex + "." + new_fileTexAttr)
              #new_file_texture_attr_dic[new_fileTexAttr] = new_fileTexAttr_Value
          #for new_fileTexAttr in new_file_texture_attrs:
              #if new_fileTexAttr in new_file_texture_attr_dic:
                  #attrExists = cmds.attributeQuery(new_fileTexAttr,node = new_fileTex,exists = True)
                  #if attrExists == 1:
                      #print "setting " + str(new_fileTex) + "." + str(new_fileTexAttr) + " to " + str(old_file_texture_attr_dic[new_fileTexAttr])
                      #cmds.setAttr(new_fileTex + "." + new_fileTexAttr,old_file_texture_attr_dic[new_fileTexAttr])
          #cmds.select(clear = True)
          #self.texture_thumbnails_listWidget.clear()

def main():
    swap = texture_replacer()
    swap.texture_linker_UI()
