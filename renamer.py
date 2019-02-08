import maya.cmds as cmds
print 'renamer!'
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class RENAME(object):
    def __init__(self,rename_suffix):
        self.rename_suffix = rename_suffix

    def find_shading_engines(self):
        node_types = ['VRayMtl']
        shading_engines_relatives_dic = {}
        shading_engines = cmds.ls(type = 'shadingEngine')
        for shading_engine in shading_engines:
            relatives = []
            print shading_engine
            if shading_engine != 'initialParticleSE':
                if shading_engine != 'initialShadingGroup':
                    relatives = cmds.listConnections(shading_engine)
                    for relative in relatives:
                        print 'relative = ',relative
                        relative_type = cmds.nodeType(relative)
                        for node_type in node_types:
                            if relative_type == node_type:
                                relatives.append(relative_type)
                    shading_engines_relatives_dic[shading_engine] = relatives
        print shading_engines_relatives_dic

rename = RENAME('chris')
rename.find_shading_engines()
