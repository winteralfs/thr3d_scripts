"""
.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI.JPG
   :align: center
   :scale: 50%

Asset tracker is used to track a scene's assets current and latest version numbers, their entity names, and their publish paths. 'C-ver' for
the current version, 'L-ver' for the latest version:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_lighting_shelf.JPG
   :align: center
   :scale: 50%

Light blue indicates the version of the asset in the scene matches the latest version found on the network. It is up to date.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_teal.jpg
   :align: center
   :scale: 50%

Red indicates the version of the asset in the scene is lower than the version found on the network. It is not up to date, and a newer
version is available.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_red.jpg
   :align: center
   :scale: 50%

Yellow indicates a version of the asset was found to exist in a more current year on the network, as in the asset in the scene is from
2017, but a version exists in the 2019 area of the network. If the asset is also out of date, the 'C-ver' will be red, and if it is
current, it will be light blue.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_yellow.jpg
   :align: center
   :scale: 50%

Orange indicates the publish_path for the asset is not valid, the directory does not exist on the network. If this is the case, an 'X' will
replace a number in the L-ver collumn as the latest version of the asset can not be determined.

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_orange.jpg
   :align: center
   :scale: 50%

Clicking the asset's name will highlight the path to the latest version of the asset: The path can be clicked to open that directory:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_highlighted.JPG
   :align: center
   :scale: 50%

Clicking the publish path of an asset will open that directory:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_network.JPG
   :align: center
   :scale: 50%

Clicking the entity name of the asset will open up the Shotgun page for that asset:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_GUI_shotgun_link.JPG
   :align: center
   :scale: 50%

If an asset shows up in the tracker that is not displayed in the outliner, toggle on the 'Hidden in Outliner'
option under the Display tab at the top of the outliner window:

.. image:: U:/cwinters/docs/build/html/_images/asset_tracker/asset_tracker_Maya_ignore_hidden_in_outliner.JPG
   :align: center
   :scale: 50%



------
"""

import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import subprocess
import webbrowser
import shiboken2

print 'asset_tracker'
#print 'fri'

class ASSET_TRACKER(object):
    def __init__(self):
        shape_nodes = cmds.ls(type = 'shape')
        print 'shape_nodes = ',shape_nodes
        bad_shape_node_names = ['std_lgt_core_Shape']
        size_shape_nodes = len(shape_nodes)
        print 'size_shape_nodes = ',size_shape_nodes
        camera_shapes = cmds.ls(type = 'camera')
        self.shape_nodes_no_cameras = []
        i = 0
        while i < size_shape_nodes:
            print i
            print 'shape_nodes[i] = ',shape_nodes[i]
            shape_node = shape_nodes[i]
            print 'shape_node = ',shape_node
            if shape_node not in camera_shapes and shape_node not in bad_shape_node_names and 'polySurface' not in shape_node and '_annotationShape' not in shape_node:
                print '** removing ' + shape_node
                self.shape_nodes_no_cameras.append(shape_node)
            print 'self.shape_nodes_no_cameras = ',self.shape_nodes_no_cameras
            i = i + 1
        raw_group_nodes = []
        self.group_nodes = []
        transform_nodes = cmds.ls(type = 'transform')
        print 'transform_nodes = ',transform_nodes
        for transform_node in transform_nodes:
            print 'transform_node = ',transform_node
            children = cmds.listRelatives(transform_node, children = True)
            print 'children = ',children
            group_node = 1
            for child in children:
                if child in shape_nodes:
                    group_node = 0
            if group_node == 1:
                raw_group_nodes.append(transform_node)
        print 'raw_group_nodes = ',raw_group_nodes
        

    def asset_tracker_UI(self):
        print ''

def main():
    asset_tracker_instance = ASSET_TRACKER()
    asset_tracker_instance.asset_tracker_UI()

#main()
