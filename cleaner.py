import maya.cmds as cmds

""" function to read the scene and grab all the textures and shaders, then compile them into a list"""

def analize_nodes():
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
    place2dTexture_nodes = cmds.ls(type = "place2dTexture")
    check_connections_list = VRayMtl_list + noise_materials + phong_list + blinn_list + lambert_list + surfaceShader_list + vray_dirt_materials + vray_light_mtls + vray_render_elements + vray_layered_textures + vray_rect_lights_transforms + vray_dome_lights_transforms + file_texture_nodes + ramp_nodes + vray_bump_materials + vray_blend_materials + vray_remapHsv_materials + vray_VRayFresnel_materials + gammaCorrect_materials + reverse_materials
    check_connections_list.append("vraySettings")
    return(file_texture_nodes,ramp_nodes,place2dTexture_nodes,check_connections_list,VRayMtl_list,phong_list,blinn_list,lambert_list,surfaceShader_list,vray_blend_materials,vray_bump_materials,vray_remapHsv_materials,vray_VRayFresnel_materials,gammaCorrect_materials,reverse_materials)

""" function that checks all the shaders in the scene and measaures if they are assigned to an object. Also deals with shading engine nodes"""

def check_shaders():
    analize_list = analize_nodes()
    selected_objects = cmds.ls(sl = True)
    unassigned_mtl_list = []
    unassigned_shading_engine_list = []
    assigned_blend_mtl_list = []
    assigned_vray_bump_materials_list = []
    assigned_VRayMtl_mtl_list = []
    assigned_mtl_list = []
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
    mtl_master_list = [VRayMtl_list,phong_list,blinn_list,lambert_list,surfaceShader_list,vray_VRayFresnel_materials]
    
    cmds.select(clear = True)  
    for bumpMtl in vray_bump_materials:
        cmds.select(clear = True)
        cmds.hyperShade(o = bumpMtl)
        objects_assigned_to_shader = cmds.ls(sl = True) or []
        objects_assigned_to_shader_len = len(objects_assigned_to_shader)
        if objects_assigned_to_shader_len == 0:
            connected = 0
            connections = cmds.listConnections(bumpMtl, destination = True)      
            for connection in connections:
                connection_type = cmds.nodeType(connection)
                if connection_type == "VRayBumpMtl":
                    cmds.select(clear = True)       
                    cmds.hyperShade(o = connection)
                    objects_assigned_to_shader = cmds.ls(sl = True) or []
                    objects_assigned_to_shader_len = len(objects_assigned_to_shader)
                    if objects_assigned_to_shader_len > 0:                          
                        connected = 1
                        if bumpMtl not in assigned_vray_bump_materials_list:
                            assigned_vray_bump_materials_list.append(bumpMtl)                        
            if connected == 0:
                if bumpMtl not in unassigned_mtl_list:
                    unassigned_mtl_list.append(bumpMtl)
        else:
            assigned_vray_bump_materials_list.append(bumpMtl)     
    cmds.select(clear = True)
    for blendMtl in vray_blend_materials:
        cmds.select(clear = True)
        cmds.hyperShade(o = blendMtl)
        objects_assigned_to_shader = cmds.ls(sl = True) or []
        objects_assigned_to_shader_len = len(objects_assigned_to_shader)
        num_of_bump_connections = len(assigned_vray_bump_materials_list)
        num_of_blend_connections = len(assigned_blend_mtl_list)
        connections = cmds.listConnections(blendMtl, destination = True)
        connected = 0
        if objects_assigned_to_shader_len != 0:
            connected = 1  
        if objects_assigned_to_shader_len == 0:
            if num_of_bump_connections > 0:
                for connection in connections:
                    for assigned_vray_bump_materials in assigned_vray_bump_materials_list:
                        if assigned_vray_bump_materials == connection:
                            connected = 1
            if num_of_blend_connections > 0:
                for connection in connections:
                    for assigned_blend_mtl in assigned_blend_mtl_list:
                        if assigned_blend_mtl == connection:
                            connected = 1              
        if connected == 0:
            if blendMtl not in unassigned_mtl_list:
                unassigned_mtl_list.append(blendMtl)
        if connected == 1:
            if blendMtl not in assigned_blend_mtl_list:
                assigned_blend_mtl_list.append(blendMtl)                  
    cmds.select(clear = True)
    
    for VRayMtl in VRayMtl_list:
        cmds.select(clear = True)
        cmds.hyperShade(o = VRayMtl)
        objects_assigned_to_shader = cmds.ls(sl = True) or []
        objects_assigned_to_shader_len = len(objects_assigned_to_shader)
        num_of_bump_connections = len(assigned_vray_bump_materials_list)
        num_of_blend_connections = len(assigned_blend_mtl_list)
        connections = cmds.listConnections(VRayMtl, destination = True)
        connected = 0
        if objects_assigned_to_shader_len != 0:
            connected = 1  
        if objects_assigned_to_shader_len == 0:
            if num_of_bump_connections > 0:
                for connection in connections:
                    for assigned_vray_bump_materials in assigned_vray_bump_materials_list:
                        if assigned_vray_bump_materials == connection:
                            connected = 1
            if num_of_blend_connections > 0:
                for connection in connections:
                    for assigned_blend_mtl in assigned_blend_mtl_list:
                        if assigned_blend_mtl == connection:
                            connected = 1              
        if connected == 0:
            if VRayMtl not in unassigned_mtl_list:
                unassigned_mtl_list.append(VRayMtl)
        if connected == 1:
            if VRayMtl not in assigned_VRayMtl_mtl_list:
                assigned_VRayMtl_mtl_list.append(VRayMtl)                  
    cmds.select(clear = True)    

    for mtl_list in mtl_master_list:
        for mtl in mtl_list:
            cmds.select(clear = True)
            cmds.hyperShade(o = mtl)
            objects_assigned_to_shader = cmds.ls(sl = True) or []
            objects_assigned_to_shader_len = len(objects_assigned_to_shader)
            num_of_bump_connections = len(assigned_vray_bump_materials_list)
            num_of_blend_connections = len(assigned_blend_mtl_list)
            num_of_VRayMtl_connections = len(assigned_VRayMtl_mtl_list)            
            connections = cmds.listConnections(mtl, destination = True)
            connected = 0
            if objects_assigned_to_shader_len != 0:
                connected = 1  
            if objects_assigned_to_shader_len == 0:
                if num_of_bump_connections > 0:
                    for connection in connections:
                        for assigned_vray_bump_materials in assigned_vray_bump_materials_list:
                            if assigned_vray_bump_materials == connection:
                                connected = 1
                if num_of_blend_connections > 0:
                    for connection in connections:
                        for assigned_blend_mtl in assigned_blend_mtl_list:
                            if assigned_blend_mtl == connection:
                                connected = 1
                if num_of_VRayMtl_connections > 0:
                    for connection in connections:
                        for assigned_VRayMtl_mtl in assigned_VRayMtl_mtl_list:
                            if assigned_VRayMtl_mtl == connection:
                                connected = 1                                                 
            if connected == 0:
                if mtl not in unassigned_mtl_list:
                    unassigned_mtl_list.append(mtl)
            if connected == 1:
                if mtl not in assigned_mtl_list:
                    assigned_mtl_list.append(mtl)                  
        cmds.select(clear = True)  
        for assigned_mtl in assigned_mtl_list:
            if assigned_mtl in unassigned_mtl_list:
                unassigned_mtl_list.remove(assigned_mtl)  
        for unassigned_mtl in unassigned_mtl_list:
                connections = cmds.listConnections(unassigned_mtl, source = False, destination = True)
                for connection in connections:
                    node_type = cmds.nodeType(connection)
                    if node_type == "shadingEngine":
                        if connection not in unassigned_shading_engine_list:
                            unassigned_shading_engine_list.append(connection)
        cmds.select(clear = True)
        for unassigned_mtl in unassigned_mtl_list:
                connections = cmds.listConnections(unassigned_mtl, source = False, destination = True)
                for connection in connections:
                    node_type = cmds.nodeType(connection)
                    if node_type == "shadingEngine":
                        if connection not in unassigned_shading_engine_list:
                            unassigned_shading_engine_list.append(connection)
        cmds.select(clear = True)          
        shaders_for_deletion_list = unassigned_mtl_list + unassigned_shading_engine_list
        return(shaders_for_deletion_list)

""" function that checks all the textures in the scene and measaures if they are connected to a used shader. Also deals with place2dTexture nodes"""

def check_textures():
    analize_list = analize_nodes()
    selected_objects = cmds.ls(sl = True)
    used_tx_nodes = []
    unused_tx_nodes = []
    used_place2dTexture_nodes = []
    file_texture_nodes = analize_list[0]
    ramp_nodes = analize_list[1]
    check_connections_list = analize_list[3]
    gammaCorrect_materials = analize_list[13]
    reverse_materials = analize_list[14]
    tx_master_list = [file_texture_nodes + ramp_nodes + gammaCorrect_materials + reverse_materials]
      
    for tx_list in tx_master_list:
        for tx in tx_list:
            tx_connections = cmds.listConnections(tx,source = False,destination = True) or []
            for tx_connection in tx_connections:
                for check_connections_item in check_connections_list:
                    if tx_connection == check_connections_item:
                        if tx not in used_tx_nodes:
                            used_tx_nodes.append(tx)
        for tx in tx_list:
            if tx not in used_tx_nodes:
                if tx not in unused_tx_nodes:
                    unused_tx_nodes.append(tx)
        unused_nodes = unused_tx_nodes
        unused_place2dTexture_nodes = []
        analize_list = analize_nodes()
        place2dTexture_nodes = analize_list[2]
        check_connections_list = analize_list[3]
        for place2dTexture_node in place2dTexture_nodes:
            place2dTexture_node_connections = cmds.listConnections(place2dTexture_node,source = False,destination = True) or []
            for place2dTexture_node_connection in place2dTexture_node_connections:
                for check_connections_item in check_connections_list:
                    if place2dTexture_node_connection == check_connections_item:
                        if place2dTexture_node_connection not in used_place2dTexture_nodes:
                            used_place2dTexture_nodes.append(place2dTexture_node)
        for place2dTexture_node in place2dTexture_nodes:
            if place2dTexture_node not in used_place2dTexture_nodes:    
                unused_place2dTexture_nodes.append(place2dTexture_node)
        tx_for_deletion_list = unused_tx_nodes + unused_place2dTexture_nodes
    return(tx_for_deletion_list)

cycle = 5
it = 0
complete_deletion_list = []
while it < cycle:
    shaders_for_deletion_list = check_shaders()
    txs_for_deletion_list = check_textures()
    for shader in shaders_for_deletion_list:
        if shader != "lambert1" and shader != "initialParticleSE" and shader != "initialShadingGroup":
            name = "shader " + shader
            complete_deletion_list.append(name)
            cmds.delete(shader)
    for tx in txs_for_deletion_list:
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
print "finished deleting nodes"
print "---"
print " "