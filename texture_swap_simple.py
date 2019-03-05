import maya.mel as mel
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class texture_replacer():

    def __init__(self):
        chris = ''

    def texture_linker_UI(self):
        #self.stayHidden = []
        #self.lowerWindowTextures = []
        windowName = "texture_swap"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        #self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SelectionChanged", self.populateBoxes])
        window.setMinimumSize(450,650)
        window.setMaximumSize(450,650)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        verticalLayout = QtWidgets.QVBoxLayout(mainWidget)
        #TextureLabelLayout = QtWidgets.QHBoxLayout()
        #verticalLayout.addLayout(TextureLabelLayout)
        #newTextureLabel = QtWidgets.QLabel("new texture")
        #newTextureLabel.setAlignment(QtCore.Qt.AlignCenter)
        #oldTextureLabel = QtWidgets.QLabel("old texture")
        #oldTextureLabel.setAlignment(QtCore.Qt.AlignCenter)
        #TextureLabelLayout.addWidget(newTextureLabel)
        #TextureLabelLayout.addWidget(oldTextureLabel)
        textureBoxLayout = QtWidgets.QHBoxLayout()
        verticalLayout.addLayout(textureBoxLayout)
        #self.textures = self.textures_populate()
        #self.newTexBox = QtWidgets.QListWidget()
        #textureBoxLayout.addWidget(self.newTexBox)
        #self.newTexBox.setObjectName("newTexBox")
        #self.oldTexBox = QtWidgets.QListWidget()
        #textureBoxLayout.addWidget(self.oldTexBox)
        #self.oldTexBox.setObjectName("oldTexBox")
        #self.newTexBox.setIconSize(QtCore.QSize(35,35))
        #self.oldTexBox.setIconSize(QtCore.QSize(35,35))
        #self.newTexBox.setStyleSheet('QListWidget {background-color: #000000; color: #B0E0E6;}')
        #self.oldTexBox.setStyleSheet('QListWidget {background-color: #000000; color: #B0E0E6;}')
        #selItems = self.newTexBox.selectedItems()
        self.textureIconChartLayout = QtWidgets.QVBoxLayout()
        textureIconsLayout = QtWidgets.QHBoxLayout()
        self.textureIconChartLayout.addLayout(textureIconsLayout)
        verticalLayout.addLayout(self.textureIconChartLayout)
        self.textureIconChart = QtWidgets.QListWidget()
        #self.textureIconChart.setStyleSheet('QListWidget {background-color: #000000; color: #B0E0E6;}')
        #self.textureIconChart.setViewMode(QtWidgets.QListWidget.IconMode)
        #self.textureIconChart.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        #self.size = 600
        #self.textureIconChart.setIconSize(QtCore.QSize(self.size, self.size))
        #self.textureIconChart.setIconSize(QtCore.QSize(self.size, self.size))
        #self.textureIconChart.setDragEnabled(0)
        #self.textureIconChart.setMaximumWidth(321)
        textureIconsLayout.addWidget(self.textureIconChart)
        #curItem = self.newTexBox.currentItem()
        #self.oldTexBox.itemClicked.connect(self.oldTextureListChange)
        #self.newTexBox.itemClicked.connect(self.newTextureListChange)
        #self.textureIconChart.itemPressed.connect(self.highlightedTexture)
        #self.textureIconChart.itemDoubleClicked.connect(self.fCheckLaunch)
        remButtonLayout = QtWidgets.QHBoxLayout()
        verticalLayout.addLayout(remButtonLayout)
        removeBtn = QtWidgets.QPushButton('remove textures')
        remButtonLayout.addWidget(removeBtn)
        #removeBtn.clicked.connect(self.removeItemFromBox)
        removeBtn.setShortcut("Backspace")
        removeBtn.setFixedSize(0,0)
        buttonLayout = QtWidgets.QVBoxLayout()
        verticalLayout.addLayout(buttonLayout)
        replaceBtn = QtWidgets.QPushButton('swap textures')
        replaceBtn.setStyleSheet("background-color:rgb(0,100,255)")
        replaceBtn.setFixedHeight(50)
        buttonLayout.addWidget(replaceBtn)
        #replaceBtn.clicked.connect(self.textureReplace)
        #self.populateBoxes()
        fg = window.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        window.move(fg.topLeft())
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

        #self.newTexBox.setCurrentIndex(QtCore.QModelIndex())
        #oldTexBoxSize = self.oldTexBox .count()
        #i = 0
        #while i < oldTexBoxSize:
            #it =  self.oldTexBox.item(i)
            #it.setFlags(it.flags() & ~QtCore.Qt.ItemIsSelectable)
            #it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEnabled)
            #it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)
            #i = i + 1

    def textureReplace(self):
        textures_for_swap = []
        texture_selections = cmds.ls(sl = True)
        for selection in texture_selections:
          node_type = cmds.nodeType(selection)
          if node_type == 'file':
              textures_for_swap.append(selection)
          print 'textures_for_swap = ',textures_for_swap
        for texturePair in textures_for_swap:
          #splitting out the old and new texture names
          texturePair = texturePair.split("%")
          new_fileTex = textures_for_swap[0]
          old_fileTex = textures_for_swap[1]
          print " "
          print "---"
          print "textures_for_swap = ",textures_for_swap
          print new_fileTex + " swapping " + old_fileTex
          print "---"
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
                      print "setting " + str(new_fileTex) + "." + str(new_fileTexAttr) + " to " + str(old_file_texture_attr_dic[new_fileTexAttr])
                      cmds.setAttr(new_fileTex + "." + new_fileTexAttr,old_file_texture_attr_dic[new_fileTexAttr])
          cmds.select(clear = True)

def main():
    swap = texture_replacer()
    swap.texture_linker_UI()
