print 'renamer_v04'
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class RENAME(object):
    def __init__(self,rename_suffix):
        self.rename_suffix = rename_suffix

    def lista_connections(self,connection):
        connections_upstream = cmds.listConnections(connection)
        for connection in connections_upstream:
            self.connection_type = cmds.nodeType(connection)
            for node_type in self.node_types:
                if self.connection_type == node_type:
                    if self.connection_type == 'VRayMtl':
                        if connection not in self.connection_check:
                            self.connection_check.append(connection)
                    if self.connection_type == 'VRayBlendMtl':
                        self.blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                        i = 0
                        for blend_connection in self.blend_connections:
                            blend_connection_split = blend_connection.split('.')
                            if blend_connection_split[1] == 'self.base_material':
                                self.blend_connections_list_num = i + 1
                            i = i + 1
                        self.base_material = self.blend_connections[self.blend_connections_list_num]
                        self.base_material_split = self.base_material.split('.')
                        self.base_material = self.base_material_split[0]
            return(self.connection_type)

    def find_shading_engines(self):
        self.node_types = ['VRayMtl','VRayBumpMtl','VRayBlendMtl','phong','lambert','blinn','surfaceShader','layeredTexture']
        self.shading_engines_connections_dic = {}
        self.base_material_dic = {}
        self.blend_connections_list_num = 0
        self.shading_engines = cmds.ls(type = 'shadingEngine')
        self.shading_engines.remove('initialParticleSE')
        self.shading_engines.remove('initialShadingGroup')
        for shading_engine in self.shading_engines:
            self.base_material = ''
            self.connection_check = []
            if shading_engine != 'initialParticleSE':
                if shading_engine != 'initialShadingGroup':
                    connections = cmds.listConnections(shading_engine)
                    for connection in connections:
                        self.connection_type = cmds.nodeType(connection)
                        for node_type in self.node_types:
                            if self.connection_type == node_type:
                                if self.connection_type == 'VRayMtl':
                                    if connection not in self.connection_check:
                                        self.connection_check.append(connection)
                                if self.connection_type == 'VRayBlendMtl':
                                    self.blend_connections = cmds.listConnections(connection,plugs = True,destination = False,connections = True)
                                    i = 0
                                    for blend_connection in self.blend_connections:
                                        blend_connection_split = blend_connection.split('.')
                                        if blend_connection_split[1] == 'self.base_material':
                                            self.blend_connections_list_num = i + 1
                                        i = i + 1
                                        self.base_material = self.blend_connections[self.blend_connections_list_num]
                                        self.base_material_split = self.base_material.split('.')
                                        self.base_material = self.base_material_split[0]
                                if self.connection_type != 'VRayMtl':
                                    self.connection_type = self.lista_connections(connection)
                                    if self.connection_type != 'VRayMtl':
                                        self.connection_type = self.lista_connections(connection)
                                        if self.connection_type != 'VRayMtl':
                                            self.connection_type = self.lista_connections(connection)
                                            if self.connection_type != 'VRayMtl':
                                                self.connection_type = self.lista_connections(connection)

            self.base_material_size = len(self.base_material)
            self.connection_check_size = len(self.connection_check)
            if self.base_material_size == 0:
                if self.connection_check_size != 0:
                    self.base_material = self.connection_check[0]
                    self.base_material_dic[shading_engine] = self.base_material
                    self.shading_engines_connections_dic[shading_engine] = self.connection_check
            else:
                self.base_material_dic[shading_engine] = self.base_material
        print 'self.shading_engines',self.shading_engines                                                                                                                        #print 'self.base_material = ',self.base_material
        print 'self.self.base_material_dic = ',self.base_material_dic
        for shading_engine in self.shading_engines:
            print 'shading_engine = ',shading_engine
            print 'self.self.base_material_dic = ',self.base_material_dic
            print 'renaming ' + shading_engine + ' to ' + self.base_material_dic[shading_engine]
            cmds.rename(shading_engine, (self.base_material_dic[shading_engine] + '_SE'))


    def renamer_window(self):
        windowName = "renamer"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        window.setFixedSize(200,50)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        vertical_layout_main = QtWidgets.QVBoxLayout(mainWidget)
        renamer_button = QtWidgets.QPushButton('rename_shading_engine_nodes')
        vertical_layout_main.addWidget(renamer_button)
        window.show()

rename = RENAME('chris')
rename.renamer_window()
