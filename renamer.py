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
        node_types = ['VRayMtl','VRayBumpMtl','VRayBlendMtl','phong','lambert','blinn','surfaceShader','layeredTexture']
        shading_engines_connections_dic = {}
        shading_engines = cmds.ls(type = 'shadingEngine')
        for shading_engine in shading_engines:
            connection_check = []
            print 'shading_engine = ',shading_engine
            if shading_engine != 'initialParticleSE':
                if shading_engine != 'initialShadingGroup':
                    connections = cmds.listConnections(shading_engine)
                    print 'connections = ',connections
                    for connection in connections:
                        print " "
                        print 'connection = ',connection
                        connection_type = cmds.nodeType(connection)
                        print 'connection_type = ', connection_type
                        for node_type in node_types:
                            print 'node_type = ',node_type
                            if connection_type == node_type:
                                if connection not in connection_check:
                                    print ' '
                                    print '**adding ' + connection + ' to connection_check**'
                                    print ' '
                                    connection_check.append(connection_type)
            shading_engines_connections_dic[shading_engine] = connection_check
        print shading_engines_connections_dic

rename = RENAME('chris')
rename.find_shading_engines()
