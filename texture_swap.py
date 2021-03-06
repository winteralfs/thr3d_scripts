"""
.. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_gui.JPG
   :align: center
   :scale: 75%

Texture_swap swaps a series of selected file_in textures with another series of selected file_in textures; applying settings and connections from each original
file_in texture to its corresponding new file_in texture.

Texture_swap is launched from the lighting_tools_shelf:

.. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_lighting_shelf.JPG
   :align: center
   :scale: 75%

To swap a series of file_in textures, open the Maya hypershade and select the file_in texture you want to swap, and then the file_in texture you want it to replace. As you select
file_in textures they will appear in the texture_swap tool gui. The order to properly select the file_in textures is always the new file_in texture and then old file_in texture.

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_hypershade_one_selected.JPG
    :align: center
    :scale: 75%

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_hypershade_two_selected.JPG
    :align: center
    :scale: 75%

To run the swaps, press the button labeled 'swap_textures.'

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_hypershade_two_selected_button_press.JPG
    :align: center
    :scale: 75%

The connections and file_in settings will be transfered to the new file_in texture, including any extra attribute links.

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_after_running.JPG
    :align: center
    :scale: 75%

Multiple swaps can be loaded into the texture_swap gui and swapped all at once.

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_mutiple_selections.JPG
    :align: center
    :scale: 75%

No file_in textures are deleted, they have to be deleted manually after the texture swap is complete.

The texture swap icon can be double clicked on the lighting shelf after the file_in textures have been selected in the hypershade, as an alternate way to run the swap.
This bypasses launching the tool's GUI.  This is a faster way to work, but you will not have visual confirmation of what file_in textures will be
swapped when the action runs.

"""

import maya.mel as mel
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
from functools import partial

print 'monday'

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
            key_words = ['alpha','substrate','matte','mettalic']
            vray_gamma_node_exists_old = cmds.attributeQuery('vrayFileGammaValue',node = old_fileTex,exists = True)
            vray_gamma_node_exists_new = cmds.attributeQuery('vrayFileGammaValue',node = new_fileTex,exists = True)
            if vray_gamma_node_exists_new == 0:
              if vray_gamma_node_exists_old == 1:
                  file_path_name = cmds.getAttr(new_fileTex + '.fileTextureName')
                  for key_word in key_words:
                      if key_word not in file_path_name:
                          cmds.vray("addAttributesFromGroup", new_fileTex, "vray_file_gamma", 1)
            print " "
            print new_fileTex + " swapping with " + old_fileTex
            print "---"
            #starting the replace

            #transferAttr settings for new texture
            old_file_texture_attr_dic = {}
            new_file_texture_attr_dic = {}
            old_file_texture_attrs = cmds.listAttr(old_fileTex,k = True)
            attrAppend = ["filter","filterOffset","filterType"]
            attrRemove = ["aiUserOptions","defaultColorMgtGlobals.cmEnabled","defaultColorMgtGlobals.configFileEnabled","defaultColorMgtGlobals.configFilePath","workingSpaceName","filter","filterOffset","filterType","frameOffset","oldFileAttr_mod"]
            for attr in attrAppend:
                old_file_texture_attrs.append(attr)
            for attr in attrRemove:
                if attr in old_file_texture_attrs:
                    old_file_texture_attrs.remove(attr)
            #print 'old_file_texture_attrs = ',old_file_texture_attrs
            new_file_texture_attrs = cmds.listAttr(new_fileTex,k = True)
            for attr in attrAppend:
                new_file_texture_attrs.append(attr)
            for attr in attrRemove:
                if attr in new_file_texture_attrs:
                    new_file_texture_attrs.remove(attr)
            for new_fileTexAttr in new_file_texture_attrs:
                new_fileTexAttr_Value = cmds.getAttr(new_fileTex + "." + new_fileTexAttr)
                new_file_texture_attr_dic[new_fileTexAttr] = new_fileTexAttr_Value
            #print 'old_file_texture_attrs = ',old_file_texture_attrs
            connected_oldFileAttrs = ['exposure','defaultColorR','defaultColorG','defaultColorB','colorGainR','colorGainG','colorGainB','colorOffsetR','colorOffsetG','colorOffsetB','alphaGain','alphaOffset']
            connected_oldFileAttrs_connected = []
            RGB_attrs = ['defaultColorR','defaultColorG','defaultColorB','colorGainR','colorGainG','colorGainB','colorOffsetR','colorOffsetG','colorOffsetB']
            oldFileAttr_RGB_list = []
            oldFileAttr_connections = []
            for oldFileAttr in old_file_texture_attrs:
                #print 'old_fileTex = ',old_fileTex
                #print 'oldFileAttr = ',oldFileAttr
                if oldFileAttr in connected_oldFileAttrs:
                    if oldFileAttr in RGB_attrs:
                        oldFileAttr = oldFileAttr[:-1]
                    #print oldFileAttr
                    #print '(*old_fileTex + "." + oldFileAttr) = ',(old_fileTex + "." + oldFileAttr)
                    oldFileAttr_connections = cmds.listConnections((old_fileTex + "." + oldFileAttr)) or []
                #print '*oldFileAttr_connections = ',oldFileAttr_connections
                number_oldFileAttr_connections = len(oldFileAttr_connections)
                #print '*number_oldFileAttr_connections = ',number_oldFileAttr_connections
                if number_oldFileAttr_connections == 0:
                    oldFileAttrValue = cmds.getAttr(old_fileTex + "." + oldFileAttr)
                    old_file_texture_attr_dic[oldFileAttr] = oldFileAttrValue
                if number_oldFileAttr_connections > 0:
                    oldFileAttr_RGB_list.append(oldFileAttr)
                    #print '* oldFileAttr_RGB_list = ',oldFileAttr_RGB_list
            #print 'connected_oldFileAttrs = ',connected_oldFileAttrs
            #print 'oldFileAttr_RGB_list = ',oldFileAttr_RGB_list
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
                    print "connecting " + connections_source_old[outIter] + " to "  + source_connections_modified[inIter]
                    cmds.connectAttr(connections_source_old[outIter],source_connections_modified[inIter],force = True)
                outIter = outIter + 2
                inIter = inIter + 2
            destination_connections_modified_size = len(destination_connections_modified)
            #connect the new texture to the old destination node
            inIter = 0
            outIter = 1
            while outIter < destination_connections_modified_size:
                if ".message" not in destination_connections_modified[inIter]:
                    print "connecting " + destination_connections_modified[inIter] + " to " + connections_destination_old[outIter]
                    cmds.connectAttr(destination_connections_modified[inIter],connections_destination_old[outIter], force = True)
                outIter = outIter + 2
                inIter = inIter + 2
            print 'new_file_texture_attr_dic = ',new_file_texture_attr_dic
            for new_fileTexAttr in new_file_texture_attrs:
                #print ' '
                #print 'new_fileTexAttr = ',new_fileTexAttr
                #print 'oldFileAttr_RGB_list = ',oldFileAttr_RGB_list
                if new_fileTexAttr in RGB_attrs:
                    new_fileTexAttr_mod = new_fileTexAttr[:-1]
                else:
                    new_fileTexAttr_mod = new_fileTexAttr
                #print 'new_fileTexAttr_mod = ',new_fileTexAttr_mod
                if new_fileTexAttr_mod not in oldFileAttr_RGB_list:
                    #print 'new_file_texture_attr_dic = ',new_file_texture_attr_dic
                    #if new_fileTexAttr in new_file_texture_attr_dic:
                    attrExists = cmds.attributeQuery(new_fileTexAttr,node = new_fileTex,exists = True)
                    if attrExists == 1:
                      #print 'unlocking, new_fileTex + "." + new_fileTexAttr = ',new_fileTex + "." + new_fileTexAttr
                      cmds.setAttr(new_fileTex + "." + new_fileTexAttr, lock=0 )
                      #print 'new_fileTexAttr = ',new_fileTexAttr
                      #print 'old_file_texture_attr_dic = ',old_file_texture_attr_dic
                      print "setting " + str(new_fileTex) + "." + str(new_fileTexAttr) + " to " + str(old_file_texture_attr_dic[new_fileTexAttr_mod])
                      attr_value = old_file_texture_attr_dic[new_fileTexAttr_mod]
                      #print 'attr_value = ',attr_value
                      if 'defaultColor' in new_fileTexAttr or 'colorGain' in new_fileTexAttr or 'colorOffset' in new_fileTexAttr:
                          #print 'found RGB list attr'
                          if 'R' == new_fileTexAttr[-1]:
                              #print 'found R'
                              attr_value = attr_value[0]
                              #print 'attr_value = ',attr_value
                              attr_value = attr_value[0]
                              #print 'attr_value = ',attr_value
                          if 'G' == new_fileTexAttr[-1]:
                              #print 'found G'
                              attr_value = attr_value[0]
                              #print 'attr_value = ',attr_value
                              attr_value = attr_value[1]
                              #print 'attr_value = ',attr_value
                          if 'B' == new_fileTexAttr[-1]:
                              #print 'found B'
                              attr_value = attr_value[0]
                              #print 'attr_value = ',attr_value
                              attr_value = attr_value[2]
                              #print 'attr_value = ',attr_value
                      #print 'attr_value = ',attr_value
                      cmds.setAttr(new_fileTex + "." + new_fileTexAttr,attr_value)
                else:
                    print '!! found a connection for ' + new_fileTexAttr
            i = i + 2
        cmds.select(clear = True)
        self.texture_thumbnails_listWidget.clear()
        new_fileTex = ''
        old_fileTex = ''

def main():
    swap = texture_replacer()
    swap.texture_linker_UI()

#main()
