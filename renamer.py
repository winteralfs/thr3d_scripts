print 'renamer_v05'
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class RENAME(object):
    def __init__(self,rename_suffix):
        self.rename_suffix = rename_suffix
        self.end_split_check_list = ['MTL','MAT','MATERIAL','SHADER','mtl','mat','material','Material','shader','Shader','material1','MATERIAL1','Material1','mat1','MAT1','MTL1','mtl1','Mat1','Mat','mt','MT']

    def find_shading_engines(self):
        self.postfix = self.postfix_line_edit.displayText() or ''
        node_types = ['VRayMtl','VRayBumpMtl','VRayBlendMtl','phong','lambert','blinn','surfaceShader','layeredTexture']
        shading_engines_connections_dic = {}
        base_material_dic = {}
        self.shading_engines = cmds.ls(type = 'shadingEngine')
        #print self.shading_engines
        engine_to_be_removed = []
        for shading_engine in self.shading_engines:
            #print ' '
            #print shading_engine
            valid_engine = 0
            connections = cmds.listConnections(shading_engine)
            for connection in connections:
                connection_type = cmds.nodeType(connection)
                for check_type in node_types:
                    if connection_type == check_type:
                        valid_engine = 1
            if valid_engine == 0:
                engine_to_be_removed.append(shading_engine)
        for shading_engine in engine_to_be_removed:
            #print 'removing ' + shading_engine + ' from shading_engine list'
            self.shading_engines.remove(shading_engine)
        #print self.shading_engines
        #print ' '
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
                                if connection_type == 'VRayMtl' or connection_type == 'blinn' or connection_type == 'phong' or connection_type == 'lambert' or connection_type == 'surfaceShader':
                                    if connection not in connection_check:
                                        #print ' '
                                        #print '0 **adding ' + connection + ' to connection_check**'
                                        #print ' '
                                        connection_check.append(connection)
                                if connection_type == 'VRayBlendMtl':
                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True) or []
                                    num_blend_connections = len(blend_connections)
                                    if num_blend_connections == 0:
                                        base_material_dic[shading_engine] = connection
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
                                if connection_type != 'VRayMtl' or connection_type != 'blinn':
                                    connections_upstream_1 = cmds.listConnections(connection)
                                    for connection in connections_upstream_1:
                                        connection_type = cmds.nodeType(connection)
                                        for node_type in node_types:
                                            if connection_type == node_type:
                                                if connection_type == 'VRayMtl' or connection_type == 'blinn' or connection_type == 'phong' or connection_type == 'lambert' or connection_type == 'surfaceShader':
                                                    if connection not in connection_check:
                                                        #print '0 **adding ' + connection + ' to connection_check**'
                                                        connection_check.append(connection)
                                                if connection_type == 'VRayBlendMtl':
                                                    #print 'found blend',connection
                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True) or []
                                                    num_blend_connections = len(blend_connections)
                                                    if num_blend_connections == 0:
                                                        base_material_dic[shading_engine] = connection
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
                                                if connection_type != 'VRayMtl' or connection_type != 'blinn' or connection_type != 'blinn' or connection_type != 'phong' or connection_type != 'lambert' or connection_type != 'surfaceShader':
                                                    connections_upstream_2 = cmds.listConnections(connection)
                                                    for connection in connections_upstream_2:
                                                        connection_type = cmds.nodeType(connection)
                                                        for node_type in node_types:
                                                            if connection_type == node_type:
                                                                if connection_type == 'VRayMtl' or connection_type == 'blinn' or connection_type == 'phong' or connection_type == 'lambert' or connection_type == 'surfaceShader':
                                                                    if connection not in connection_check:
                                                                        #print '1 **adding ' + connection + ' to connection_check**'
                                                                        connection_check.append(connection)
                                                                if connection_type == 'VRayBlendMtl':
                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                    num_blend_connections = len(blend_connections)
                                                                    if num_blend_connections == 0:
                                                                        base_material_dic[shading_engine] = connection
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
                                                                if connection_type != 'VRayMtl' or connection_type != 'blinn' or connection_type != 'blinn' or connection_type != 'phong' or connection_type != 'lambert' or connection_type != 'surfaceShader':
                                                                    connections_upstream_3 = cmds.listConnections(connection)
                                                                    for connection in connections_upstream_3:
                                                                        connection_type = cmds.nodeType(connection)
                                                                        for node_type in node_types:
                                                                            if connection_type == node_type:
                                                                                if connection_type == 'VRayMtl' or connection_type == 'blinn' or connection_type == 'phong' or connection_type == 'lambert' or connection_type == 'surfaceShader':
                                                                                    if connection not in connection_check:
                                                                                        #print '2 **adding ' + connection + ' to connection_check**'
                                                                                        connection_check.append(connection)
                                                                                if connection_type == 'VRayBlendMtl':
                                                                                    #print 'found blend',connection
                                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                                    num_blend_connections = len(blend_connections)
                                                                                    if num_blend_connections == 0:
                                                                                        base_material_dic[shading_engine] = connection
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
                                                                                if connection_type != 'VRayMtl' or connection_type != 'blinn' or connection_type != 'blinn' or connection_type != 'phong' or connection_type != 'lambert' or connection_type != 'surfaceShader':
                                                                                    connections_upstream_4 = cmds.listConnections(connection)
                                                                                    for connection in connections_upstream_4:
                                                                                        connection_type = cmds.nodeType(connection)
                                                                                        for node_type in node_types:
                                                                                            if connection_type == node_type:
                                                                                                if connection_type == 'VRayMtl' or connection_type == 'blinn' or connection_type == 'phong' or connection_type == 'lambert' or connection_type == 'surfaceShader':
                                                                                                    if connection not in connection_check:
                                                                                                        #print '3 **adding ' + connection + ' to connection_check**'
                                                                                                        connection_check.append(connection)
                                                                                                if connection_type == 'VRayBlendMtl':
                                                                                                    #print 'found blend',connection
                                                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                                                    num_blend_connections = len(blend_connections)
                                                                                                    if num_blend_connections == 0:
                                                                                                        base_material_dic[shading_engine] = connection
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
                                                                                                if connection_type != 'VRayMtl' or connection_type != 'blinn' or connection_type != 'blinn' or connection_type != 'phong' or connection_type != 'lambert' or connection_type != 'surfaceShader':
                                                                                                    connections_upstream_5 = cmds.listConnections(connection)
                                                                                                    for connection in connections_upstream_5:
                                                                                                        connection_type = cmds.nodeType(connection)
                                                                                                        for node_type in node_types:
                                                                                                            if connection_type == node_type:
                                                                                                                if connection_type == 'VRayMtl' or connection_type == 'blinn' or connection_type == 'phong' or connection_type == 'lambert' or connection_type == 'surfaceShader':
                                                                                                                    if connection not in connection_check:
                                                                                                                        #print '4 **adding ' + connection + ' to connection_check**'
                                                                                                                        connection_check.append(connection)
                                                                                                                if connection_type == 'VRayBlendMtl':
                                                                                                                    #print 'found blend',connection
                                                                                                                    blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                                                                                                    num_blend_connections = len(blend_connections)
                                                                                                                    if num_blend_connections == 0:
                                                                                                                        base_material_dic[shading_engine] = connection
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
        for shading_engine in self.shading_engines:
            selectable = 'True'
            if selectable == 'True':
                shading_engine = cmds.rename(shading_engine, (base_material_dic[shading_engine] + '_SG'))
                #print '0 shading_engine = ',shading_engine
                if self.postfix in shading_engine:
                    if self.postfix != '':
                        #print 'postfix = ',self.postfix
                        shading_engine_no_postfix = shading_engine.replace(('_' + self.postfix),'')
                        shading_engine = cmds.rename(shading_engine,shading_engine_no_postfix)
                #print '1 shading_engine = ',shading_engine
                for end_split_check in self.end_split_check_list:
                    if end_split_check in shading_engine:
                        #print 'end_split_check = ',end_split_check
                        shading_engine_no_end_split_check = shading_engine.replace(('_' + end_split_check),'')
                        #print 'shading_engine_no_end_split_check',shading_engine_no_end_split_check
                        shading_engine = cmds.rename(shading_engine,shading_engine_no_end_split_check)
                #print '2 shading_engine = ',shading_engine

    def shader_list(self):
        locked_shaders = ['lambert1']
        VRayMtl_list = cmds.ls(type = 'VRayMtl')
        phong_list = cmds.ls(type = 'phong')
        blinn_list = cmds.ls(type = 'blinn')
        lambert_blinn_list = cmds.ls(type = 'lambert')
        surface_shader_list = cmds.ls(type = 'surfaceShader')
        blend_material_list = cmds.ls(type = 'VRayBlendMtl')
        bump_material_list = cmds.ls(type = 'VRayBumpMtl')
        displacement_list = cmds.ls(type = 'displacementShader')
        light_material_list = cmds.ls(type = 'VRayLightMtl')
        self.postfix_master_list = VRayMtl_list + phong_list + lambert_blinn_list + surface_shader_list + blend_material_list + bump_material_list + displacement_list + light_material_list
        for shader in locked_shaders:
            self.postfix_master_list.remove(shader)

    def set_postfix(self):
        self.shader_list()
        self.postfix = self.postfix_line_edit.displayText() or ''
        empty_field_test = len(self.postfix)
        if empty_field_test == 0:
            self.postfix = 'EMPTY FIELD'
        for material in self.postfix_master_list:
            material_name_split = material.split('_')
            len_split = len(material_name_split)
            end_split = material_name_split[(len_split - 1)]
            if self.postfix not in self.end_split_check_list:
                self.end_split_check_list.append(self.postfix)
            if end_split in self.end_split_check_list:
                    replace_str = '_' + end_split
                    new_material_name = material.replace(replace_str,'')
                    cmds.rename(material,new_material_name)
        self.shader_list()
        for material in self.postfix_master_list:
            print 'material = ',material
            if self.postfix != 'EMPTY FIELD':
                cmds.rename(material,(material + '_' + self.postfix))

    def renamer_window(self):
        windowName = "renamer"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        window.setFixedSize(200,100)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        vertical_layout_main = QtWidgets.QVBoxLayout(mainWidget)
        horiz_layout_main = QtWidgets.QHBoxLayout(mainWidget)
        renamer_button = QtWidgets.QPushButton('rename shading engine nodes')
        renamer_button.pressed.connect(partial(self.find_shading_engines))
        vertical_layout_main.addWidget(renamer_button)
        self.postfix_line_edit = QtWidgets.QLineEdit()
        self.postfix_line_edit.setFixedSize(50,30)
        horiz_layout_main.addWidget(self.postfix_line_edit)
        vertical_layout_main.addLayout(horiz_layout_main)
        postfix_button = QtWidgets.QPushButton('set postfix on shaders')
        postfix_button.pressed.connect(partial(self.set_postfix))
        horiz_layout_main.addWidget(postfix_button)
        window.show()

rename = RENAME('chris')
rename.renamer_window()
