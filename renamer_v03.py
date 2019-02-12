print 'renamer_v02'
import maya.cmds as cmds
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
        base_material_dic = {}
        self.shading_engines = cmds.ls(type = 'shadingEngine')
        self.shading_engines.remove('initialParticleSE')
        self.shading_engines.remove('initialShadingGroup')        
        for shading_engine in self.shading_engines:
            base_material = ''
            connection_check = []
            #print ' '
            #print 'shading_engine = ',shading_engine
            if shading_engine != 'initialParticleSE':
                if shading_engine != 'initialShadingGroup':
                    connections = cmds.listConnections(shading_engine)
                    for connection in connections:
                        connection_type = cmds.nodeType(connection)
                        for node_type in node_types:
                            if connection_type == node_type:
                                if connection_type == 'VRayMtl':
                                    if connection not in connection_check:
                                        #print ' '
                                        #print '0 **adding ' + connection + ' to connection_check**'
                                        #print ' '
                                        connection_check.append(connection)
                                if connection_type == 'VRayBlendMtl':
                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                    i = 0
                                    for blend_connection in blend_connections:
                                        blend_connection_split = blend_connection.split('.')
                                        if blend_connection_split[1] == 'base_material':
                                            blend_connections_list_num = i + 1
                                        i = i + 1
                                        base_material = blend_connections[blend_connections_list_num]
                                        base_material_split = base_material.split('.')
                                        base_material = base_material_split[0]
                                        #print 'base_material = ',base_material
                                if connection_type != 'VRayMtl':
                                    connections_upstream_1 = cmds.listConnections(connection)
                                    for connection in connections_upstream_1:
                                        connection_type = cmds.nodeType(connection)
                                        for node_type in node_types:
                                            if connection_type == node_type:
                                                if connection_type == 'VRayMtl':
                                                    if connection not in connection_check:
                                                        #print '0 **adding ' + connection + ' to connection_check**'
                                                        connection_check.append(connection)
                                                if connection_type == 'VRayBlendMtl':
                                                    #print 'found blend',connection
                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                    i = 0
                                                    for blend_connection in blend_connections:
                                                        blend_connection_split = blend_connection.split('.')
                                                        if blend_connection_split[1] == 'base_material':
                                                            blend_connections_list_num = i + 1
                                                        i = i + 1
                                                    base_material = blend_connections[blend_connections_list_num]
                                                    base_material_split = base_material.split('.')
                                                    base_material = base_material_split[0]
                                                    #print 'base_material = ',base_material
                                                if connection_type != 'VRayMtl':
                                                    connections_upstream_2 = cmds.listConnections(connection)
                                                    for connection in connections_upstream_2:
                                                        connection_type = cmds.nodeType(connection)
                                                        for node_type in node_types:
                                                            if connection_type == node_type:
                                                                if connection_type == 'VRayMtl':
                                                                    if connection not in connection_check:
                                                                        #print '1 **adding ' + connection + ' to connection_check**'
                                                                        connection_check.append(connection)
                                                                if connection_type == 'VRayBlendMtl':
                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                    i = 0
                                                                    for blend_connection in blend_connections:
                                                                        blend_connection_split = blend_connection.split('.')
                                                                        if blend_connection_split[1] == 'base_material':
                                                                            blend_connections_list_num = i + 1
                                                                        i = i + 1
                                                                        base_material = blend_connections[blend_connections_list_num]
                                                                        base_material_split = base_material.split('.')
                                                                        base_material = base_material_split[0]
                                                                        #print 'base_material = ',base_material
                                                                if connection_type != 'VRayMtl':
                                                                    connections_upstream_3 = cmds.listConnections(connection)
                                                                    for connection in connections_upstream_3:
                                                                        connection_type = cmds.nodeType(connection)
                                                                        for node_type in node_types:
                                                                            if connection_type == node_type:
                                                                                if connection_type == 'VRayMtl':
                                                                                    if connection not in connection_check:
                                                                                        #print '2 **adding ' + connection + ' to connection_check**'
                                                                                        connection_check.append(connection)
                                                                                if connection_type == 'VRayBlendMtl':
                                                                                    #print 'found blend',connection
                                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                                    i = 0
                                                                                    for blend_connection in blend_connections:
                                                                                        blend_connection_split = blend_connection.split('.')
                                                                                        if blend_connection_split[1] == 'base_material':
                                                                                            blend_connections_list_num = i + 1
                                                                                        i = i + 1
                                                                                        base_material = blend_connections[blend_connections_list_num]
                                                                                        base_material_split = base_material.split('.')
                                                                                        base_material = base_material_split[0]
                                                                                        #print 'base_material = ',base_material
                                                                                if connection_type != 'VRayMtl':
                                                                                    connections_upstream_4 = cmds.listConnections(connection)
                                                                                    for connection in connections_upstream_4:
                                                                                        connection_type = cmds.nodeType(connection)
                                                                                        for node_type in node_types:
                                                                                            if connection_type == node_type:
                                                                                                if connection_type == 'VRayMtl':
                                                                                                    if connection not in connection_check:
                                                                                                        #print '3 **adding ' + connection + ' to connection_check**'
                                                                                                        connection_check.append(connection)
                                                                                                if connection_type == 'VRayBlendMtl':
                                                                                                    #print 'found blend',connection
                                                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                                                    i = 0
                                                                                                    for blend_connection in blend_connections:
                                                                                                        blend_connection_split = blend_connection.split('.')
                                                                                                        if blend_connection_split[1] == 'base_material':
                                                                                                            blend_connections_list_num = i + 1
                                                                                                        i = i + 1
                                                                                                        base_material = blend_connections[blend_connections_list_num]
                                                                                                        base_material_split = base_material.split('.')
                                                                                                        base_material = base_material_split[0]
                                                                                                        #print 'base_material = ',base_material
                                                                                                if connection_type != 'VRayMtl':
                                                                                                    connections_upstream_5 = cmds.listConnections(connection)
                                                                                                    for connection in connections_upstream_5:
                                                                                                        connection_type = cmds.nodeType(connection)
                                                                                                        for node_type in node_types:
                                                                                                            if connection_type == node_type:
                                                                                                                if connection_type == 'VRayMtl':
                                                                                                                    if connection not in connection_check:
                                                                                                                        #print '4 **adding ' + connection + ' to connection_check**'
                                                                                                                        connection_check.append(connection)
                                                                                                                if connection_type == 'VRayBlendMtl':
                                                                                                                    #print 'found blend',connection
                                                                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                                                                    i = 0
                                                                                                                    for blend_connection in blend_connections:
                                                                                                                        blend_connection_split = blend_connection.split('.')
                                                                                                                        if blend_connection_split[1] == 'base_material':
                                                                                                                            blend_connections_list_num = i + 1
                                                                                                                        i = i + 1
                                                                                                                        base_material = blend_connections[blend_connections_list_num]
                                                                                                                        base_material_split = base_material.split('.')
                                                                                                                        base_material = base_material_split[0]
            base_material_size = len(base_material)
            connection_check_size = len(connection_check)
            if base_material_size == 0:
                if connection_check_size != 0:
                    base_material = connection_check[0]
                    base_material_dic[shading_engine] = base_material
                    shading_engines_connections_dic[shading_engine] = connection_check
            else:
                base_material_dic[shading_engine] = base_material
        print 'self.shading_engines',self.shading_engines                                                                                                                        #print 'base_material = ',base_material
        print 'base_material_dic = ',base_material_dic
        for shading_engine in self.shading_engines:
            print 'shading_engine = ',shading_engine
            print 'base_material_dic = ',base_material_dic
            print 'renaming ' + shading_engine + ' to ' + base_material_dic[shading_engine]
            cmds.rename(shading_engine, (base_material_dic[shading_engine] + '_SE'))

rename = RENAME('chris')
rename.find_shading_engines()
