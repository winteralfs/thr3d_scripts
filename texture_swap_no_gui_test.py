"""
texture_swap
********************************************

.. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_gui.JPG
   :align: center
   :scale: 75%

texture_swap in a tool that swaps a series of selected file_in textures with another series of selected file_in textures; applying settings and connections from the original
file_in textures to the new series of file_in textures.

texture_swap can be launched from the lighting_tools_shelf:

.. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_lighting_shelf.JPG
   :align: center
   :scale: 75%

to swap a series of file_in textures, open the Maya hypershade and select a file_in texture you want to swap and then the file_in texture you want it to replace. As you select
file_in textures they will appear in the texture_swap tool gui. The order to properly select is always the new file_in texture and then old file_in texture, A then B, A and then B.

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_hypershade_one_selected.JPG
    :align: center
    :scale: 75%

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_hypershade_two_selected.JPG
    :align: center
    :scale: 75%

to activate the swapping action for all the file_in textures in the texture_swap gui, press the button labeled 'swap_textures.'

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_hypershade_two_selected_button_press.JPG
    :align: center
    :scale: 75%

The connections and file_in settings will be transfered to the new file_in texture, including extra attribute links.

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_after_running.JPG
    :align: center
    :scale: 75%

multiple swaps can be loaded into the texture_swap gui and swapped all at once.

 .. image:: U:/cwinters/docs/build/html/_images/texture_swap/texture_swap_mutiple_selections.JPG
    :align: center
    :scale: 75%

for safety, no file_in textures are deleted, they have to be deleted manually after swapping.

"""

import maya.mel as mel
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
from functools import partial

class texture_replacer_no_gui():

    def __init__(self):
        chris = ''

    def texture_replace_no_gui(self):
        number_of_textures = 2
        textures_to_swap = []
        viable_node_types = ['file']
        textures = cmds.ls(selection = True)
        for texture in textures:
            object_type = cmds.nodeType(texture)
            if object_type in viable_node_types:
                textures_to_swap.append(texture)
        number_of_selected_textures = len(textures_to_swap)
        if number_of_selected_textures == 10:
            i = 0
            while i < number_of_textures:
              #splitting out the old and new texture names
              new_fileTex = textures_to_swap[i]
              old_fileTex = textures_to_swap[i+1]
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
            new_fileTex = ''
            old_fileTex = ''

def main():
    swap = texture_replacer_no_gui()
    swap.texture_replace_no_gui()

#main()
