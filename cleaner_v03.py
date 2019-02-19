#---
print 'cleaner_v03'
import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class cleaner():
    def __init__(self):
        self.assigned_mtl_list = []
        self.shaders_for_deletion_list = []
    """ function to read the scene and grab all the textures and shaders, then compile them into a list"""
    def analize_nodes(self):
        selected_objects = cmds.ls(sl = True)
        VRayMtl_list = cmds.ls(type = "VRayMtl")
        phong_list = cmds.ls(type = "phong")
        blinn_list = cmds.ls(type = "blinn")
        lambert_list = cmds.ls(type = "lambert")
        surfaceShader_list = cmds.ls(type = "surfaceShader")
        vray_layered_textures = cmds.ls(type = "layeredTexture")
        vray_bump_materials = cmds.ls(type = "VRayBumpMtl")
        vray_blend_materials = cmds.ls(type = "VRayBlendMtl")
        vray_remapHsv_materials = cmds.ls(type = "remapHsv")
        gammaCorrect_materials = cmds.ls(type = "gammaCorrect")
        vray_VRayFresnel_materials = cmds.ls(type = "VRayFresnel")
        vray_dirt_materials = cmds.ls(type = "VRayDirt")
        noise_materials = cmds.ls(type = "noise")
        vray_render_elements = cmds.ls(type = "VRayRenderElement")
        vray_light_mtls = cmds.ls(type = "VRayLightMtl")
        vray_rect_lights = cmds.ls(type = "VRayLightRectShape") or []
        vray_rect_lights_transforms = []
        for vray_rect_light in vray_rect_lights:
            tform = cmds.listRelatives(vray_rect_light, parent = True)
            vray_rect_lights_transforms.append(tform[0])
        vray_dome_lights = cmds.ls(type = "VRayLightDomeShape") or []
        vray_dome_lights_transforms = []
        for vray_dome_light in vray_dome_lights:
            tform = cmds.listRelatives(vray_dome_light, parent = True)
            vray_dome_lights_transforms.append(tform[0])
        file_texture_nodes = cmds.ls(type = "file")
        ramp_nodes = cmds.ls(type = "ramp")
        reverse_materials = cmds.ls(type = "reverse")
        displacement_materials = cmds.ls(type = "VRayDisplacement")
        place2dTexture_nodes = cmds.ls(type = "place2dTexture")
        blend_colors = cmds.ls(type = "blendColors")
        VRayTriplanar_nodes = cmds.ls(type = "VRayTriplanar")
        check_connections_list = VRayMtl_list + noise_materials + phong_list + blinn_list + lambert_list + surfaceShader_list + vray_dirt_materials + vray_light_mtls + vray_render_elements + vray_layered_textures + vray_rect_lights_transforms + vray_dome_lights_transforms + file_texture_nodes + ramp_nodes + vray_bump_materials + vray_blend_materials + vray_remapHsv_materials + vray_VRayFresnel_materials + gammaCorrect_materials + reverse_materials + displacement_materials + blend_colors + VRayTriplanar_nodes
        check_connections_list.append("vraySettings")
        return(file_texture_nodes, ramp_nodes, place2dTexture_nodes, check_connections_list, VRayMtl_list, phong_list, blinn_list, lambert_list, surfaceShader_list, vray_blend_materials, vray_bump_materials, vray_remapHsv_materials, vray_VRayFresnel_materials, gammaCorrect_materials, reverse_materials, vray_layered_textures, displacement_materials, noise_materials, blend_colors, VRayTriplanar_nodes)

    """ function that checks all the shaders in the scene and measaures if they are assigned to an object. Also deals with shading engine nodes"""
    def check_shaders(self):
        self.check_textures()
        render_layers = cmds.ls(type = "renderLayer")
        analize_list = self.analize_nodes()
        selected_objects = cmds.ls(sl = True)
        unassigned_mtl_list = []
        unassigned_shading_engine_list = []
        assigned_blend_mtl_list = []
        assigned_vray_VRayMtl_materials_list = []
        assigned_vray_bump_materials_list = []
        assigned_vray_blend_materials_list = []
        self.assigned_mtl_list = []
        unassigned_mtl_list = []
        check_connections_list = analize_list[3]
        VRayMtl_list = analize_list[4]
        phong_list = analize_list[5]
        blinn_list = analize_list[6]
        lambert_list = analize_list[7]
        surfaceShader_list = analize_list[8]
        vray_blend_materials = analize_list[9]
        vray_bump_materials = analize_list[10]
        vray_VRayFresnel_materials = analize_list[12]
        displacement_materials = analize_list[16]
        shader_types = ["VRayMtl","phong","blinn","lambert","surfaceShader","VRayBumpMtl","VRayBlendMtl","VRayFresnel"]
        mtl_master_list = [VRayMtl_list,phong_list,blinn_list,lambert_list,surfaceShader_list,vray_VRayFresnel_materials,vray_bump_materials,vray_blend_materials]
        for render_layer in render_layers:
            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
            cmds.select(clear = True)
            for mtl_list in mtl_master_list:
                for mtl in mtl_list:
                    mtl_type = cmds.nodeType(mtl)
                    cmds.select(clear = True)
                    cmds.hyperShade(o = mtl)
                    objects_assigned_to_shader = cmds.ls(sl = True) or []
                    objects_assigned_to_shader_len = len(objects_assigned_to_shader)
                    connected = 1
                    if objects_assigned_to_shader_len == 0:
                        connected = 0
                        print mtl
                        connections_one = cmds.listConnections(mtl, destination = True) or []
                        for connection in connections_one:
                            if connection in self.used_tx_nodes:
                                if mtl not in self.assigned_mtl_list:
                                    self.assigned_mtl_list.append(mtl)
                            connection_type = cmds.nodeType(connection)
                            if connection_type in shader_types:
                                cmds.select(clear = True)
                                cmds.hyperShade(o = connection)
                                objects_assigned_to_shader = cmds.ls(sl = True) or []
                                objects_assigned_to_shader_len = len(objects_assigned_to_shader)
                                if objects_assigned_to_shader_len > 0:
                                    connected = 1
                                    if mtl not in self.assigned_mtl_list:
                                        self.assigned_mtl_list.append(mtl)
                                else:
                                    connections_two = cmds.listConnections(connection, destination = True)
                                    for connection in connections_two:
                                        connection_type = cmds.nodeType(connection)
                                        if connection_type in shader_types:
                                            cmds.select(clear = True)
                                            cmds.hyperShade(o = connection)
                                            objects_assigned_to_shader = cmds.ls(sl = True) or []
                                            objects_assigned_to_shader_len = len(objects_assigned_to_shader)
                                            if objects_assigned_to_shader_len > 0:
                                                connected = 1
                                                if mtl not in self.assigned_mtl_list:
                                                    self.assigned_mtl_list.append(mtl)
                                            else:
                                                connections_three = cmds.listConnections(connection, destination = True)
                                                for connection in connections_three:
                                                    connection_type = cmds.nodeType(connection)
                                                    if connection_type in shader_types:
                                                        cmds.select(clear = True)
                                                        cmds.hyperShade(o = connection)
                                                        objects_assigned_to_shader = cmds.ls(sl = True) or []
                                                        objects_assigned_to_shader_len = len(objects_assigned_to_shader)
                                                        if objects_assigned_to_shader_len > 0:
                                                            connected = 1
                                                            if mtl not in self.assigned_mtl_list:
                                                                self.assigned_mtl_list.append(mtl)
                                                        else:
                                                            connections_four = cmds.listConnections(connection, destination = True)
                                                            for connection in connections_four:
                                                                connection_type = cmds.nodeType(connection)
                                                                if connection_type in shader_types:
                                                                    cmds.select(clear = True)
                                                                    cmds.hyperShade(o = connection)
                                                                    objects_assigned_to_shader = cmds.ls(sl = True) or []
                                                                    objects_assigned_to_shader_len = len(objects_assigned_to_shader)
                                                                    if objects_assigned_to_shader_len > 0:
                                                                        connected = 1
                                                                        if mtl not in self.assigned_mtl_list:
                                                                            self.assigned_mtl_list.append(mtl)
                                                                    else:
                                                                        connections_five = cmds.listConnections(connection, destination = True)
                                                                        for connection in connections_five:
                                                                            connection_type = cmds.nodeType(connection)
                                                                            if connection_type in shader_types:
                                                                                cmds.select(clear = True)
                                                                                cmds.hyperShade(o = connection)
                                                                                objects_assigned_to_shader = cmds.ls(sl = True) or []
                                                                                objects_assigned_to_shader_len = len(objects_assigned_to_shader)
                                                                                if objects_assigned_to_shader_len > 0:
                                                                                    connected = 1
                                                                                    if mtl not in self.assigned_mtl_list:
                                                                                        self.assigned_mtl_list.append(mtl)
                    if connected == 0:
                        if mtl not in self.assigned_mtl_list:
                            if mtl not in unassigned_mtl_list:
                                unassigned_mtl_list.append(mtl)
                    else:
                        self.assigned_mtl_list.append(mtl)
                cmds.select(clear = True)
        for assigned_mtl in self.assigned_mtl_list:
            if assigned_mtl in unassigned_mtl_list:
                unassigned_mtl_list.remove(assigned_mtl)
        for unassigned_mtl in unassigned_mtl_list:
                connections = cmds.listConnections(unassigned_mtl, source = False, destination = True) or []
                for connection in connections:
                    node_type = cmds.nodeType(connection)
                    if node_type == "shadingEngine":
                        if connection not in unassigned_shading_engine_list:
                            unassigned_shading_engine_list.append(connection)
        cmds.select(clear = True)
        self.shaders_for_deletion_list = unassigned_mtl_list + unassigned_shading_engine_list
        locked_shaders = ["particleCloud1","lambert1","shaderGlow1","initialParticleSE","initialShadingGroup"]
        for locked in locked_shaders:
            if locked in self.shaders_for_deletion_list:
                self.shaders_for_deletion_list.remove(locked)
        self.check_textures_2dPlacements()
        return(self.shaders_for_deletion_list)

    """ function that checks all the textures in the scene and measaures if they are connected to a used shader. Also deals with place2dTexture nodes"""
    def check_textures(self):
        render_layers = cmds.ls(type = "renderLayer")
        analize_list = self.analize_nodes()
        selected_objects = cmds.ls(sl = True)
        self.used_tx_nodes = []
        self.unused_tx_nodes = []
        used_place2dTexture_nodes = []
        file_texture_nodes = analize_list[0]
        ramp_nodes = analize_list[1]
        place2dTexture_nodes = analize_list[2]
        check_connections_list = analize_list[3]
        for connection in check_connections_list:
            if connection in self.shaders_for_deletion_list:
                check_connections_list.remove(connection)
        vray_VRayFresnel_materials = analize_list[12]
        gammaCorrect_materials = analize_list[13]
        reverse_materials = analize_list[14]
        layered_texture_nodes = analize_list[15]
        noise_materials = analize_list[17]
        blend_colors = analize_list[18]
        VRayTriplanar_nodes = analize_list[19]
        tx_master_list = file_texture_nodes + ramp_nodes + gammaCorrect_materials + reverse_materials + layered_texture_nodes + noise_materials + blend_colors + VRayTriplanar_nodes
        self.unused_tx_nodes = tx_master_list
        unused_place2dTexture_nodes = []
        for render_layer in render_layers:
            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
            for tx in tx_master_list:
                tx_connections = cmds.listConnections(tx,source = False,destination = True) or []
                if "defaultTextureList" in tx_connections:
                    tx_connections.remove("defaultTextureList")
                if "defaultTextureList1" in tx_connections:
                    tx_connections.remove("defaultTextureList1")
                number_tx_connections = len(tx_connections)
                if number_tx_connections > 0:
                    for tx_connection in tx_connections:
                        if tx_connection in check_connections_list:
                            if tx not in self.used_tx_nodes:
                                self.used_tx_nodes.append(tx)
                            else:
                                connections_two = cmds.listConnections(tx_connection, destination = True) or []
                                for connection in connections_two:
                                    connection_type = cmds.nodeType(connection)
                                    if connection_type in check_connections_list:
                                        if tx not in used_tx_nodes:
                                            self.used_tx_nodes.append(tx)
                                        else:
                                            connections_three = cmds.listConnections(tx_connection, destination = True) or []
                                            for connection in connections_three:
                                                connection_type = cmds.nodeType(connection)
                                                if connection_type in check_connections_list:
                                                    if tx not in self.used_tx_nodes:
                                                        self.used_tx_nodes.append(tx)
        return()

    def check_textures_2dPlacements(self):
        render_layers = cmds.ls(type = "renderLayer")
        analize_list = self.analize_nodes()
        selected_objects = cmds.ls(sl = True)
        used_place2dTexture_nodes = []
        file_texture_nodes = analize_list[0]
        ramp_nodes = analize_list[1]
        place2dTexture_nodes = analize_list[2]
        check_connections_list = analize_list[3]
        for connection in check_connections_list:
            if connection in self.shaders_for_deletion_list:
                check_connections_list.remove(connection)
        vray_VRayFresnel_materials = analize_list[12]
        gammaCorrect_materials = analize_list[13]
        reverse_materials = analize_list[14]
        layered_texture_nodes = analize_list[15]
        noise_materials = analize_list[17]
        blend_colors = analize_list[18]
        VRayTriplanar_nodes = analize_list[19]
        tx_master_list = file_texture_nodes + ramp_nodes + gammaCorrect_materials + reverse_materials + layered_texture_nodes + noise_materials + blend_colors + VRayTriplanar_nodes
        self.unused_tx_nodes = tx_master_list
        unused_place2dTexture_nodes = []
        for render_layer in render_layers:
            for place2dTexture_node in place2dTexture_nodes:
                connections = cmds.listConnections(place2dTexture_node,source = False,destination = True) or []
                for connection in connections:
                    for used_tx in self.used_tx_nodes:
                        if connection == used_tx or connection in self.assigned_mtl_list:
                            if place2dTexture_node not in used_place2dTexture_nodes:
                                used_place2dTexture_nodes.append(place2dTexture_node)
            for place2dTexture_node in place2dTexture_nodes:
                if place2dTexture_node not in used_place2dTexture_nodes:
                    if place2dTexture_node not in unused_place2dTexture_nodes:
                        unused_place2dTexture_nodes.append(place2dTexture_node)
        for tx in self.used_tx_nodes:
            if tx in self.unused_tx_nodes:
                self.unused_tx_nodes.remove(tx)
        self.tx_for_deletion_list = self.unused_tx_nodes + unused_place2dTexture_nodes
        return(self.tx_for_deletion_list)

    def run_cleaner(self):

        dupes_found = 0
        clashingNames = []
        mayaResolvedName = []
        allDagNodes = cmds.ls(dag = 1)
        for node in allDagNodes:
            if len(node.split("|")) > 1:
                mayaResolvedName.append(node)
                if (node.split("|")[-1]) not in clashingNames:
                    print 'adding ',node
                    clashingNames.append(node.split("|")[-1])
        dup_nodes_size = len(clashingNames)
        if dup_nodes_size > 0:
            print "name Clash Found (check light nodes): "
            print clashingNames
            dupes_found = 1
            cmds.window(title = 'Dupes found', width = 300, height = 75, sizeable = False)
            cmds.columnLayout("mainColumn", adjustableColumn = True)
            cmds.rowLayout("nameRowLayout01", numberOfColumns = 15, parent = "mainColumn")
            cmds.text(label = ("name Clash Found (check light nodes): "))
            for name in clashingNames:
                cmds.text(label = ('' + name + ', '),font = 'boldLabelFont')
            cmds.showWindow()
        else:
            print "no dupe nodes found"
        if dupes_found != 1:
            cycle = 1
            it = 0
            complete_deletion_list = []
            while it < cycle:
                self.check_shaders()
                self.check_textures()
                for shader in self.shaders_for_deletion_list:
                    if shader != "lambert1" and shader != "initialParticleSE" and shader != "initialShadingGroup":
                        name = "shader " + shader
                        complete_deletion_list.append(name)
                        cmds.delete(shader)
                for tx in self.tx_for_deletion_list:
                    name = "texture " + tx
                    complete_deletion_list.append(name)
                    cmds.delete(tx)
                it = it + 1
            print " "
            print "---"
            complete_deletion_list_len = len(complete_deletion_list)
            if complete_deletion_list_len == 0:
                print "nothing deleted"
            for item in complete_deletion_list:
                print "deleted ",item
            #for obj in selected_objects:
                #if cmds.objExists(obj):
                    #cmds.select(obj)
            print "---"
            print "finished deleting nodes"
            print "---"
            print " "

    def save_scene(self):
        print 'save scene'
        cmds.file( save=True, type='mayaBinary' )

    def exit_cleaner(self):
        cmds.deleteUI(self.window_name)

    def cleaner_window(self):
        print "cleaner_window"
        print 'cleaner_window'
        self.window_name = 'cleaner'
        if cmds.window(self.window_name,exists = True):
            cmds.deleteUI(self.window_name)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(self.window_name)
        window.setWindowTitle(self.window_name)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        window.setFixedSize(250,50)
        self.horizontal_layout = QtWidgets.QHBoxLayout(mainWidget)
        self.save_scene_button = QtWidgets.QPushButton("save")
        self.save_scene_button.pressed.connect(partial(self.save_scene))
        self.horizontal_layout.addWidget(self.save_scene_button)
        self.exit_button = QtWidgets.QPushButton("exit")
        self.exit_button.pressed.connect(partial(self.exit_cleaner))
        self.horizontal_layout.addWidget(self.exit_button)
        self.cleaner_button = QtWidgets.QPushButton("clean")
        self.cleaner_button.pressed.connect(partial(self.run_cleaner))
        self.horizontal_layout.addWidget(self.cleaner_button)
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    clean = cleaner()
    clean.cleaner_window()
