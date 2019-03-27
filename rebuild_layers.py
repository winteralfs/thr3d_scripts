import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
import re

class LAYERS_WINDOW_TOOL(object):
    def __init__(self):
        self.light_types = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
        self.materials_VRayMtl = cmds.ls(type = "VRayMtl")
        self.materials_phong = cmds.ls(type = "phong")
        self.materials_blinn = cmds.ls(type = "blinn")
        self.materials_lambert = cmds.ls(type = "lambert")
        self.materials_surface_shader = cmds.ls(type = "surfaceShader")
        self.materials_displacement = cmds.ls(type = "displacementShader")
        self.displacement_nodes = cmds.ls(type = "VRayDisplacement")
        self.placement_nodes = cmds.ls(type = "place2dTexture")
        self.file_nodes = cmds.ls(type = "file")
        self.gammaCorrect_nodes = cmds.ls(type = "gammaCorrect")
        self.ramp_nodes = cmds.ls(type = "ramp")
        self.layeredTexture = cmds.ls(type = "layeredTexture")
        self.VRayBlendMtls = cmds.ls(type = "VRayBlendMtl")
        self.VRayPlaceEnvTex_nodes = cmds.ls(type = "VRayPlaceEnvTex")
        self.multiplyDivide = cmds.ls(type = "multiplyDivide")
        self.remapHsv = cmds.ls(type = "remapHsv")
        self.remapColor = cmds.ls(type = "remapColor")
        self.materials = self.materials_VRayMtl + self.materials_phong + self.materials_blinn + self.materials_lambert + self.materials_surface_shader + self.placement_nodes + self.file_nodes + self.materials_displacement + self.displacement_nodes + self.layeredTexture + self.VRayBlendMtls + self.VRayPlaceEnvTex_nodes + self.ramp_nodes + self.gammaCorrect_nodes + self.multiplyDivide + self.remapHsv + self.remapColor
        self.object_check_g = cmds.ls(g = True)
        self.object_check_transform = cmds.ls(type = "transform")
        self.object_check_cameras = cmds.ls(type = "camera")
        self.object_check = self.object_check_g + self.object_check_transform + self.materials + self.object_check_cameras
        self.lites = cmds.ls(lt = True)
        self.vray_lights = []
        for object in self.object_check:
            node_type = cmds.nodeType(object)
            for lite in self.light_types:
                if node_type == lite:
                    self.vray_lights.append(object)
        self.object_check.append("vraySettings")

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())

#---

    def overides_information_function(self):
        #print 'overides_information_function'
        vray_settings_overrides_dic = {}
        transform_layer_overrides = {}
        material_assignment_overrides = {}
        self.material_overrides_dic = {}
        camera_overrides_dic = {}
        light_overrides_dic = {}
        render_stat_overrides = {}
        vray_object_property_overrides = {}
        vray_settings_overrides_dic = self.vray_settings_overrides()
        object_translations = self.translations()
        #print 'object_translations = ',object_translations
        transform_layer_overrides = object_translations[3]
        #print 'transform_layer_overrides = ',transform_layer_overrides
        self.material_assignments = self.material_assignments()
        #print 'OBJ_1_self.material_assignments = ',OBJ_1_self.material_assignments
        self.material_assignment_overrides = self.material_assignments[3]
        #print 'material_assignment_overrides = ',material_assignment_overrides
        self.material_overrides_dic = self.material_overrides()
        #self.material_overrides_dic.update(material_assignment_overrides)
        self.ramp_overrides = self.ramp_overrides_method()
        camera_overrides_dic = self.camera_overides()
        light_overrides_dic = self.light_overrides()
        render_stat_overrides = self.render_stat_overrides()
        vray_object_property_overrides = self.vray_object_prop_overrides()
        #print 'vray_settings_overrides_dic = ',vray_settings_overrides_dic
        #print 'transform_layer_overrides = ',transform_layer_overrides
        #print 'self.material_overrides_dic = ',self.material_overrides_dic
        #print 'light_overrides_dic = ',light_overrides_dic
        #print 'render_stat_overrides = ',render_stat_overrides
        #print 'vray_object_property_overrides = ',vray_object_property_overrides
        #print 'camera_overrides_dic = ',camera_overrides_dic
        return(vray_settings_overrides_dic,transform_layer_overrides,self.material_overrides_dic,light_overrides_dic,render_stat_overrides,vray_object_property_overrides,camera_overrides_dic)

    def overides_information_summary(self,object_type,remove_attr_List,attr_overrides_dic,object_label):
        render_layer_ramp_overrides = {}
        object_label = object_label
        self.object_type = object_type
        #print " "
        #print " "
        print "self.object_type = ",self.object_type
        object_list = self.object_check
        if self.object_type == "camera" or self.object_type == "VRayLightRectShape" or self.object_type == "spotLight" or self.object_type == "ambientLight" or self.object_type == "directionalLight" or self.object_type == "pointLight" or self.object_type == "VRayMtl" or self.object_type == "blinn" or self.object_type == "phong" or self.object_type == "lambert" or self.object_type == "surfaceShader" or self.object_type == "displacementShader" or self.object_type == "VRayDisplacement" or self.object_type == "place2dTexture" or self.object_type == "file" or self.object_type == "layeredTexture" or self.object_type == "VRayBlendMtl" or self.object_type == "VRayPlaceEnvTex" or self.object_type == "self.multiplyDivide" or self.object_type == "self.remapHsv" or self.object_type == "self.remapColor":
            self.object_list = cmds.ls(type = self.object_type)
        if self.object_type == "VRaySettingsNode":
            self.object_list = []
            self.object_list.append("vraySettings")
        self.attr_overrides_dic = attr_overrides_dic
        self.remove_attr_List = remove_attr_List

    def attr_override_detect(self,object_label):
        for object in self.object_list:
            layered_texture_overrides = []
            default_ramp = "none"
            override_ramp = "none"
            connections_count = 1
            it_list_count = 1
            it_list = []
            count_overrides_dic = {}
            node_type = cmds.nodeType(object)
            if node_type == self.object_type:
                attrs = cmds.listAttr(object)
                for remove_attr in self.remove_attr_List:
                    #print 'remove_attr = ',remove_attr
                    attrs.remove(remove_attr)
                if self.object_type == "layeredTexture":
                    current_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
                    overrides = cmds.editRenderLayerAdjustment(current_layer, query = True, layer = True)
                    count_overrides_base = 0
                    for render_layer in self.render_layers:
                        layered_texture_overrides = []
                        count_overrides = cmds.editRenderLayerAdjustment(render_layer, query = True, layer = True)
                        for override in count_overrides:
                            override_split = override.split('.')
                            override_check = override_split[0]
                            override_check_type = cmds.nodeType(override_check)
                            if override_check_type == 'layeredTexture':
                                layered_texture_overrides.append(override)
                        count_overrides_number = 0
                        count_overrides_number = len(layered_texture_overrides)
                        if count_overrides_number > count_overrides_base:
                            count_overrides_base = count_overrides_number
                    connections = cmds.listConnections(object, source = True,destination = False) or []
                    connections_count = len(connections)
                    for connection in connections:
                        cn_string = connection + ".outColor"
                        connection_info = cmds.connectionInfo(cn_string,destinationFromSource = True) or []
                        for ci in connection_info:
                            if object in ci:
                                it_num_split_a = ci.split("[")
                                it_num_split_b = it_num_split_a[1].split("]")
                                it_num = it_num_split_b[0]
                                it_list.append(it_num)
                it = 0
                if self.object_type == 'layeredTexture':
                    it_list_count = count_overrides_base
                else:
                    it_list_count = 1
                while it < it_list_count:
                    for attr in attrs:
                        if self.object_type == "layeredTexture" and attr != 'alphaIsLuminance':
                            attr_split = attr.split('.')
                            attr_string = object + "." + (attr_split[0] + '[' + str(it) + ']' + '.' + attr_split[1])
                        else:
                            attr_string = object + "." + attr
                        cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                        default_attr_value = cmds.getAttr(attr_string)
                        attr_connections = cmds.listConnections(attr_string,destination = False) or []
                        default_ramp_found = 0
                        for connection in attr_connections:
                            connection_type = cmds.nodeType(connection)
                            if connection_type == "ramp" or connection_type == "fractal" or connection_type == "noise" or connection_type == "file" or connection_type == "checker" or connection_type == "cloud" or connection_type == "brownian" or connection_type == "bulge" or connection_type == "VRayMtl" or connection_type == "blinn" or connection_type == "phong" or connection_type == "lambert" or connection_type == "surfaceShader" or connection_type == "gammaCorrect":
                                default_ramp_found = 1
                                default_ramp = connection
                        for render_layer in self.render_layers:
                            if render_layer != "defaultRenderLayer":
                                cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                                attr_connections = cmds.listConnections(attr_string,destination = False) or []
                                override_ramp_found = 0
                                for attr_connection in attr_connections:
                                    attr_type = cmds.nodeType(attr_connection)
                                    if attr_type == "ramp" or attr_type == "fractal" or attr_type == "noise" or attr_type == "file" or attr_type == "checker" or attr_type == "cloud" or attr_type == "brownian" or attr_type == "bulge" or attr_type == "VRayMtl" or attr_type == "blinn" or attr_type == "phong" or attr_type == "lambert" or attr_type == "surfaceShader" or attr_type == "gammaCorrect":
                                        override_ramp_found = 1
                                        override_ramp = attr_connection
                                override_attr_value = cmds.getAttr(attr_string)
                                if self.object_type == "layeredTexture" and attr != 'alphaIsLuminance':
                                    attr_split = attr.split('.')
                                    attr_layered_texture_string = attr_split[0] + '[' + str(it) + ']' + '.' + attr_split[1]
                                    attr_dic_string = object_label + "_overide*" + object + '.' + attr_layered_texture_string + "**" + render_layer + "_"
                                else:
                                    attr_dic_string = object_label + "_overide*" + object + "." + attr + "**" + render_layer + "_"
                                if default_ramp_found == 0 and override_ramp_found == 0:
                                    if default_attr_value != override_attr_value:
                                        self.attr_overrides_dic[attr_dic_string] = override_attr_value
                                if default_ramp_found == 0 and override_ramp_found == 1:
                                    attr_dic_string = object_label + "_overide_ramp_added*" + attr_string + "**" + render_layer + "_"
                                    self.attr_overrides_dic[attr_dic_string] = override_ramp
                                if default_ramp_found == 1 and override_ramp_found == 0:
                                    override_attr_value = cmds.getAttr(attr_string)
                                    attr_dic_string = object_label + "_overide_ramp_removed*" + attr_string + "**" + render_layer + "_"
                                    self.attr_overrides_dic[attr_dic_string] = override_attr_value
                                if default_ramp_found == 1 and override_ramp_found == 1:
                                    override_ramp = attr_connection
                                    if override_ramp != default_ramp:
                                        attr_dic_string = object_label + "_overide_ramp_mismatch*" + attr_string + "**" + render_layer + "_"
                                        self.attr_overrides_dic[attr_dic_string] = override_ramp
                                    if override_ramp == default_ramp:
                                        render_layer_overrides = cmds.listConnections(render_layer + ".adjustments", p = True, c = True) or []
                                        render_layer_ramp_overrides = []
                                        for connection in render_layer_overrides:
                                            type = cmds.nodeType(connection)
                                            if type == "ramp":
                                                if connection not in render_layer_ramp_overrides:
                                                    render_layer_ramp_overrides.append(connection)
                                            for i in range(0, len(render_layer_overrides), 2):
                                                rl_connection = render_layer_overrides[i]
                                                override_Attr = render_layer_overrides[i+1]
                                                override_index = rl_connection.split("]")[0]
                                                override_index = override_index.split("[")[-1]
                                                override_value = cmds.getAttr(render_layer + ".adjustments[%s].value" %override_index)
                                                attr_dic_string =  object_label + "_" + attr + "_rampOveride" + "*" + override_Attr + "**" + render_layer + "_"
                                                if attr_dic_string not in self.attr_overrides_dic and override_ramp in override_Attr:
                                                    self.attr_overrides_dic[attr_dic_string] = override_value
                    it = it + 1
        return(self.attr_overrides_dic)

    def translations(self):
        transform_default_values_dic = {}
        object_in_layers = []
        transform_layer_overrides = []
        transform_override_values_dic = {}
        transform_layer_dic = {}
        cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
        render_layer = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
        for object in self.object_check_transform:
            #print 'object = ',object
            string_translateX = object + ".translateX"
            translateX = cmds.getAttr(string_translateX)
            var = object + "$" + render_layer + "$translateX"
            transform_default_values_dic[var] = translateX
            string_translateY = object + ".translateY"
            translateY = cmds.getAttr(string_translateY)
            var = object + "$" + render_layer + "$translateY"
            transform_default_values_dic[var] = translateY
            string_translateZ = object + ".translateZ"
            translateZ = cmds.getAttr(string_translateZ)
            var = object + "$" + render_layer + "$translateZ"
            transform_default_values_dic[var] = translateZ
            str_rotateX = object + ".rotateX"
            rotateX = cmds.getAttr(str_rotateX)
            var = object + "$" + render_layer + "$rotateX"
            transform_default_values_dic[var] = rotateX
            string_rotateY = object + ".rotateY"
            rotateY = cmds.getAttr(string_rotateY)
            var = object + "$" + render_layer + "$rotateY"
            transform_default_values_dic[var] = rotateY
            string_rotateZ = object + ".rotateZ"
            rotateZ = cmds.getAttr(string_rotateZ)
            var = object + "$" + render_layer + "$rotateZ"
            transform_default_values_dic[var] = rotateZ
            string_scaleX = object + ".scaleX"
            scaleX = cmds.getAttr(string_scaleX)
            var = object + "$" + render_layer + "$scaleX"
            transform_default_values_dic[var] = scaleX
            string_scaleY = object + ".scaleY"
            scaleY = cmds.getAttr(string_scaleY)
            var = object + "$" + render_layer + "$scaleY"
            transform_default_values_dic[var] = scaleY
            string_scaleZ = object + ".scaleZ"
            scaleZ = cmds.getAttr(string_scaleZ)
            var = object + "$" + render_layer + "$scaleZ"
            transform_default_values_dic[var] = scaleZ
        #print 'transform_default_values_dic = ',transform_default_values_dic
        for object in self.object_check_transform:
            for render_layer in self.render_layers:
                cmds.editRenderLayerGlobals( currentRenderLayer = render_layer )
                render_layer = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
                if "defaultRenderLayer" != render_layer:
                    string_translateX = object + ".translateX"
                    translateX = cmds.getAttr(string_translateX)
                    var = object + "$" + render_layer + "$translateX"
                    transform_override_values_dic[var] = translateX
                    string_translateY = object + ".translateY"
                    translateY = cmds.getAttr(string_translateY)
                    var = object + "$" + render_layer + "$translateY"
                    transform_override_values_dic[var] = translateY
                    string_translateZ = object + ".translateZ"
                    translateZ = cmds.getAttr(string_translateZ)
                    var = object + "$" + render_layer + "$translateZ"
                    transform_override_values_dic[var] = translateZ
                    str_rotateX = object + ".rotateX"
                    rotateX = cmds.getAttr(str_rotateX)
                    var = object + "$" + render_layer + "$rotateX"
                    transform_override_values_dic[var] = rotateX
                    string_rotateY = object + ".rotateY"
                    rotateY = cmds.getAttr(string_rotateY)
                    var = object + "$" + render_layer + "$rotateY"
                    transform_override_values_dic[var] = rotateY
                    string_rotateZ = object + ".rotateZ"
                    rotateZ = cmds.getAttr(string_rotateZ)
                    var = object + "$" + render_layer + "$rotateZ"
                    transform_override_values_dic[var] = rotateZ
                    string_scaleX = object + ".scaleX"
                    scaleX = cmds.getAttr(string_scaleX)
                    var = object + "$" + render_layer + "$scaleX"
                    transform_override_values_dic[var] = scaleX
                    string_scaleY = object + ".scaleY"
                    scaleY = cmds.getAttr(string_scaleY)
                    var = object + "$" + render_layer + "$scaleY"
                    transform_override_values_dic[var] = scaleY
                    string_scaleZ = object + ".scaleZ"
                    scaleZ = cmds.getAttr(string_scaleZ)
                    var = object + "$" + render_layer + "$scaleZ"
                    transform_override_values_dic[var] = scaleZ
        #print 'transform_override_values_dic = ',transform_override_values_dic
        for transform_value in transform_override_values_dic:
            transform_values_split = transform_value.split("$")
            for transform_defualt_value in transform_default_values_dic:
                transform_defualt_value_split = transform_defualt_value.split("$")
                if transform_values_split[0] == transform_defualt_value_split[0] and transform_values_split[2] == transform_defualt_value_split[2]:
                    value = transform_override_values_dic[transform_value]
                    value_default = transform_default_values_dic[transform_defualt_value]
                    if value != value_default:
                        transform_layer_overrides.append(transform_value)
                        transform_layer_dic["transO$" + transform_value] = value

        return transform_default_values_dic,transform_override_values_dic,transform_layer_overrides,transform_layer_dic

    def material_assignments(self):
        self.materials_list = []
        self.materials_list_overrides = []
        material_layer_overrides = []
        self.materials_defualt_dic = {}
        self.materials_override_dic = {}
        self.materials_layer_dic = {}
        for object in self.object_check:
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            render_layer = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
            for render_layer in self.render_layers:
                cmds.editRenderLayerGlobals( currentRenderLayer = render_layer )
                if render_layer == "defaultRenderLayer":
                    cmds.select(clear = True)
                    cmds.select(object)
                    cmds.hyperShade(smn = True)
                    self.materials_list = cmds.ls(sl = True)
                    for material in self.materials_list:
                        node_type = cmds.nodeType(material)
                        if node_type != "renderLayer":
                            if material not in self.materials_list_overrides:
                                self.materials_list_overrides.append(material)
                            override_dic_key = object + "$" + render_layer + "$"
                            self.materials_defualt_dic[override_dic_key] = material
                else:
                    cmds.select(clear = True)
                    cmds.select(object)
                    cmds.hyperShade(smn = True)
                    self.materials_list = cmds.ls(sl = True)
                    for material in self.materials_list:
                        node_type = cmds.nodeType(material)
                        if node_type != "renderLayer":
                            if material not in self.materials_list_overrides:
                                self.materials_list_overrides.append(material)
                            override_dic_key = object + "$" + render_layer + "$"
                            self.materials_override_dic[override_dic_key] = material
        for material_override_dic in self.materials_override_dic:
           material_value_split = material_override_dic.split("$")
           for material_default_dic in self.materials_defualt_dic:
               material_defualt_value_split = material_default_dic.split("$")
               if material_value_split[0] == material_defualt_value_split[0]:
                    material_override = self.materials_override_dic[material_override_dic]
                    material_default = self.materials_defualt_dic[material_default_dic]
                    if material_override != material_default:
                        material_layer_overrides.append(material_override_dic)
                        material_dic_string = material_override_dic + ".materialAssignment"
                        if material_dic_string not in self.materials_layer_dic and "Shape" not in material_dic_string:
                            self.materials_layer_dic[material_dic_string] = material_override
        return(self.materials_list_overrides,self.materials_list_overrides,self.materials_override_dic,material_layer_overrides,self.materials_layer_dic)

    def material_overrides(self):
        self.material_overrides_dic = {}
        attr_overrides_dic = self.material_overrides_dic
        object_label = "material_overide"

        object_type = "VRayMtl"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","outColor","outColorR","outColorG","outColorB","outApiType","outApiClassification","outTransparency",
        "outTransparencyR","outTransparencyG","outTransparencyB","reflectionsMaxDepth","refractionsMaxDepth","swatchAutoUpdate","swatchAlwaysRender","swatchExplicitUpdate","swatchMaxRes","color","diffuseColorR"
        ,"diffuseColorG","diffuseColorB","diffuseColorAmount","roughnessAmount","illumColor","illumColorR","illumColorG","illumColorB","illumGI","compensateExposure","reflectionColor","reflectionColorR","reflectionColorG"
        ,"reflectionColorB","reflectionColorAmount","reflectionExitColor","reflectionExitColorR","reflectionExitColorG","reflectionExitColorB","hilightGlossinessLock","hilightGlossiness","reflectionGlossiness","reflectionSubdivs"
        ,"reflectionAffectAlpha","reflInterpolation","reflMapMinRate","reflMapMaxRate","reflMapColorThreshold","reflMapNormalThreshold","reflMapSamples","useFresnel","lockFresnelIORToRefractionIOR","fresnelIOR","reflectOnBackSide"
        ,"softenEdge","fixDarkEdges","glossyFresnel","ggxTailFalloff","ggxOldTailFalloff","anisotropy","anisotropyUVWGen","anisotropyRotation","refractionColor","refractionColorR","refractionColorG","refractionColorB","refractionColorAmount"
        ,"refractionExitColor","refractionExitColorR","refractionExitColorG","refractionExitColorB","refractionExitColorOn","refractionGlossiness","refractionSubdivs","refractionIOR","refrDispersionOn","refrDispersionAbbe","refrInterpolation"
        ,"refrMapMinRate","refrMapMaxRate","refrMapColorThreshold","refrMapNormalThreshold","refrMapSamples","fogColor","fogColorR","fogColorG","fogColorB","fogMult","fogBias","affectShadows","affectAlpha","traceReflections","traceRefractions"
        ,"cutoffThreshold","brdfType","bumpMapType","bumpMap","bumpMapR","bumpMapG","bumpMapB","bumpMult","bumpShadows","bumpDeltaScale","sssOn","translucencyColor","translucencyColorR","translucencyColorG","translucencyColorB","thickness","scatterCoeff"
        ,"scatterDir","scatterLevels","scatterSubdivs","sssEnvironment","opacityMap","opacityMapR","opacityMapG","opacityMapB","doubleSided","useIrradianceMap","reflectionDimDistanceOn","reflectionDimDistance","reflectionDimFallOff","attributeAliasList"]
        attr_check = ["color","diffuseColorAmount","opacityMap","roughnessAmount","illumColor","illumGI","compensateExposure","brdfType","reflectionColor","reflectionColorAmount","hilightGlossinessLock",
        "hilightGlossiness","reflectionGlossiness","useFresnel","glossyFresnel","lockFresnelIORToRefractionIOR","refractionColor","refractionColorAmount","refractionGlossiness","refractionIOR",
        "fogColor","fogMult","fogBias","affectShadows","sssOn","translucencyColor","scatterSubdivs","scatterDir","scatterLevels","scatterCoeff","thickness","sssEnvironment","traceRefractions",
        "refractionExitColorOn","refractionsMaxDepth","affectAlpha","refrDispersionOn","refrDispersionAbbe","bumpMapType","bumpMap","bumpMult","bumpShadows","bumpDeltaScale","cutoffThreshold",
        "doubleSided","useIrradianceMap","fixDarkEdges","caching","nodeState","reflMapMinRate","reflMapMaxRate","reflMapColorThreshold","reflMapNormalThreshold","reflMapSamples"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "blinn"
        remove_attr_List = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "eccentricity", "specularRollOff", "reflectionRolloff"]
        attr_check = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","eccentricity","specularRollOff","specularColor","reflectivity","reflectedColor"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "phong"
        remove_attr_List = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "cosinePower"]
        attr_check = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","cosinePower","specularColor","reflectivity","reflectedColor"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "lambert"
        remove_attr_List = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB"]
        attr_check = ["color","transparency","ambientColor","incandescence","diffuse","translucence","translucenceDepth","translucenceFocus"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "surfaceShader"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outMatteOpacity","outMatteOpacityR","outMatteOpacityG","outMatteOpacityB","outGlowColor","outGlowColorR","outGlowColorG","outGlowColorB","materialAlphaGain"]
        attr_check = ["outColor","outTransparency","outGlowColor","outMatteOpacity"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "place2dTexture"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","uvCoord","uCoord","vCoord","vertexUvOne","vertexUvOneU","vertexUvOneV","vertexUvTwo","vertexUvTwoU","vertexUvTwoV","vertexUvThree","vertexUvThreeU","vertexUvThreeV","vertexCameraOne","vertexCameraOneX","vertexCameraOneY","vertexCameraOneZ","uvFilterSize","uvFilterSizeX","uvFilterSizeY","coverage","coverageU","coverageV","translateFrame","translateFrameU","translateFrameV","rotateFrame","mirrorU","mirrorV","stagger","wrapU","wrapV","repeatUV","repeatU","repeatV","offset","offsetU","offsetV","rotateUV","noiseUV","noiseU","noiseV","fast","outUV","outU","outV","outUvFilterSize","outUvFilterSizeX","outUvFilterSizeY","doTransform"]
        attr_check = ["coverageU","coverageV","translateFrameU","translateFrameV","rotateFrame","mirrorU","mirrorV","wrapU","wrapV","stagger","repeatU","repeatV","offsetU","offsetV","rotateUV","noiseU","noiseV","fast"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "file"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","filter","filterOffset","invert","alphaIsLuminance","colorGain","colorGainR","colorGainG","colorGainB","colorOffset","colorOffsetR","colorOffsetG","colorOffsetB","alphaGain","alphaOffset","defaultColor","defaultColorR","defaultColorG","defaultColorB","outColor","outColorR","outColorG","outColorB","outAlpha","fileTextureName","fileTextureNamePattern","computedFileTextureNamePattern","disableFileLoad","useFrameExtension","frameExtension","frameOffset","useHardwareTextureCycling","startCycleExtension","endCycleExtension","byCycleIncrement","forceSwatchGen","filterType","filterWidth","preFilter","preFilterRadius","useCache","useMaximumRes","uvTilingMode","explicitUvTiles","explicitUvTiles.explicitUvTileName","explicitUvTiles.explicitUvTilePosition","explicitUvTiles.explicitUvTilePositionU","explicitUvTiles.explicitUvTilePositionV","baseExplicitUvTilePosition","baseExplicitUvTilePositionU","baseExplicitUvTilePositionV","uvTileProxyDirty","uvTileProxyGenerate","uvTileProxyQuality","coverage","coverageU","coverageV","translateFrame","translateFrameU","translateFrameV","rotateFrame","doTransform","mirrorU","mirrorV","stagger","wrapU","wrapV","repeatUV","repeatU","repeatV","offset","offsetU","offsetV","rotateUV","noiseUV","noiseU","noiseV","blurPixelation","vertexCameraOne","vertexCameraOneX","vertexCameraOneY","vertexCameraOneZ","vertexCameraTwo","vertexCameraTwoX","vertexCameraTwoY","vertexCameraTwoZ","vertexCameraThree","vertexCameraThreeX","vertexCameraThreeY","vertexCameraThreeZ","vertexUvOne","vertexUvOneU","vertexUvOneV","vertexUvTwo","vertexUvTwoU","vertexUvTwoV","vertexUvThree","vertexUvThreeU","vertexUvThreeV","objectType","rayDepth","primitiveId","pixelCenter","pixelCenterX","pixelCenterY","exposure","hdrMapping","hdrExposure","dirtyPixelRegion","ptexFilterType","ptexFilterWidth","ptexFilterBlur","ptexFilterSharpness","ptexFilterInterpolateLevels","colorProfile","colorSpace","ignoreColorSpaceFileRules","workingSpace","colorManagementEnabled","colorManagementConfigFileEnabled","colorManagementConfigFilePath","outSize","outSizeX","outSizeY","fileHasAlpha","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","infoBits"]
        attr_check = ["exposure","defaultColor","colorGain","colorOffset","alphaGain","alphaOffset","alphaIsLuminance","invert"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "gammaCorrect"
        #print 'running gamma correct'
        remove_attr_List = ['message','caching','frozen','isHistoricallyInteresting','nodeState','binMembership','value','valueX','valueY','valueZ','gamma','gammaX','gammaY','gammaZ','renderPassMode','outValue','outValueX','outValueY','outValueZ','aiUserOptions','aiValue','aiValueX','aiValueY','aiValueZ','aiGamma','aiGammaX','aiGammaY','aiGammaZ']
        attr_check = ['value','gammaX','gammaY','gammaZ']
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "VRayPlaceEnvTex"
        remove_attr_List = ['message','caching','frozen','isHistoricallyInteresting','nodeState','binMembership','mappingType','horFlip','verFlip','horRotation','verRotation','outUV','outU','outV','outApiType','outApiClassification','useTransform','transform','groundOn','groundPosition','groundPosition0','groundPosition1','groundPosition2','groundRadius']
        attr_check = ['horRotation','verRotation']
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "layeredTexture"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","inputs","inputs.color","inputs.colorR","inputs.colorG","inputs.colorB","inputs.alpha","inputs.blendMode","inputs.isVisible","outColor","outColorR","outColorG","outColorB","outAlpha","hardwareColor","hardwareColorR","hardwareColorG","hardwareColorB","alphaIsLuminance","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB"]
        attr_check = ["alphaIsLuminance","inputs.isVisible","inputs.alpha","inputs.color","inputs.blendMode"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "VRayBlendMtl"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","swatchAutoUpdate","swatchAlwaysRender","swatchExplicitUpdate","swatchMaxRes","base_material","base_materialR","base_materialG","base_materialB","color","colorR","colorG","colorB","viewportColor","viewportColorR","viewportColorG","viewportColorB","coat_material_0","coat_material_0R","coat_material_0G","coat_material_0B","blend_amount_0","blend_amount_0R","blend_amount_0G","blend_amount_0B","coat_material_1","coat_material_1R","coat_material_1G","coat_material_1B","blend_amount_1","blend_amount_1R","blend_amount_1G","blend_amount_1B","coat_material_2","coat_material_2R","coat_material_2G","coat_material_2B","blend_amount_2","blend_amount_2R","blend_amount_2G","blend_amount_2B","coat_material_3","coat_material_3R","coat_material_3G","coat_material_3B","blend_amount_3","blend_amount_3R","blend_amount_3G","blend_amount_3B","coat_material_4","coat_material_4R","coat_material_4G","coat_material_4B","blend_amount_4","blend_amount_4R","blend_amount_4G","blend_amount_4B","coat_material_5","coat_material_5R","coat_material_5G","coat_material_5B","blend_amount_5","blend_amount_5R","blend_amount_5G","blend_amount_5B","coat_material_6","coat_material_6R","coat_material_6G","coat_material_6B","blend_amount_6","blend_amount_6R","blend_amount_6G","blend_amount_6B","coat_material_7","coat_material_7R","coat_material_7G","coat_material_7B","blend_amount_7","blend_amount_7R","blend_amount_7G","blend_amount_7B","coat_material_8","coat_material_8R","coat_material_8G","coat_material_8B","blend_amount_8","blend_amount_8R","blend_amount_8G","blend_amount_8B","additive_mode","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outApiType","outApiClassification"]
        attr_check = ["base_material","additive_mode","coat_material_0","blend_amount_0","coat_material_1","blend_amount_1","coat_material_2","blend_amount_2","coat_material_3","blend_amount_3","coat_material_4","blend_amount_4","coat_material_5","blend_amount_5","coat_material_6","blend_amount_6","coat_material_7","blend_amount_7","coat_material_8","blend_amount_8"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "displacementShader"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","displacementMode","displacement","vectorDisplacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","yIsUp","tangent","tangentX","tangentY","tangentZ"]
        attr_check = ["displacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","tangentX","tangentY","tangentZ","nodeState","caching","displacementMode"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "VRayDisplacement"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","dagSetMembers","dnSetMembers","memberWireframeColor","annotation","isLayer","verticesOnlySet","edgesOnlySet","facetsOnlySet","editPointsOnlySet","renderableOnlySet","partition","groupNodes","usedBy","displacement","overrideGlobalDisplacement","outApiType","outApiClassification","vraySeparator_vray_displacement","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementType","vrayDisplacementAmount","vrayDisplacementShift","vrayDisplacementKeepContinuity","vrayEnableWaterLevel","vrayWaterLevel","vrayDisplacementCacheNormals","vray2dDisplacementResolution","vray2dDisplacementPrecision","vray2dDisplacementTightBounds","vray2dDisplacementMultiTile","vray2dDisplacementFilterTexture","vray2dDisplacementFilterBlur","vrayDisplacementUseBounds","vrayDisplacementMinValue","vrayDisplacementMinValueR","vrayDisplacementMinValueG","vrayDisplacementMinValueB","vrayDisplacementMaxValue","vrayDisplacementMaxValueR","vrayDisplacementMaxValueG","vrayDisplacementMaxValueB","vraySeparator_vray_subquality","vrayOverrideGlobalSubQual","vrayViewDep","vrayEdgeLength","vrayMaxSubdivs"]
        attr_check = ["overrideGlobalDisplacement","displacement","caching","nodeState","blackBox","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementType","vrayDisplacementAmount","vrayDisplacementShift","vrayEdgeLength","vrayMaxSubdivs","vrayDisplacementUseBounds"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        material_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        return(self.material_overrides_dic)

    def ramp_overrides_method(self):
        self.ramp_overrides = []
        for render_layer in self.render_layers:
            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
            self.overrides =  cmds.editRenderLayerAdjustment(render_layer, query = True, layer = True) or []
            #print 'self.overrides = ',self.overrides
            for ramp in self.ramp_nodes:
                #print 'ramp = ',ramp
                for override in self.overrides:
                    #print 'override = ',override
                    if ramp in override:
                        #print 'override = ',override
                        override_value = cmds.getAttr(override)
                        override_value_type = type(override_value) is list
                        #print 'anal override_value = ',override_value
                        #print 'anal override_value_type = ',override_value_type
                        if override_value_type == 1:
                            override_value = override_value[0]
                            #print 'list = ', override_value
                        #else:
                            #print 'non list = ', override_value
                        ramp_override_string = render_layer + '&&' + ramp  + '&&' + override + '&&' + str(override_value)
                        #print 'ramp_override_string = ',ramp_override_string
                        self.ramp_overrides.append(ramp_override_string)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)
        return(self.ramp_overrides)

    def camera_overides(self):
        camera_overrides_dic = {}
        attr_overrides_dic = camera_overrides_dic
        object_label = "camera_overide"
        object_type = "camera"
        remove_attr_List =  ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "hyperLayout", "isCollapsed", "blackBox", "borderConnections", "isHierarchicalConnection", "publishedNodeInfo", "publishedNodeInfo.publishedNode", "publishedNodeInfo.isHierarchicalNode", "publishedNodeInfo.publishedNodeType", "rmbCommand", "templateName", "templatePath", "viewName", "iconName", "viewMode", "templateVersion", "uiTreatment", "customTreatment", "creator", "creationDate", "containerType", "boundingBox", "boundingBoxMin", "boundingBoxMinX", "boundingBoxMinY", "boundingBoxMinZ", "boundingBoxMax", "boundingBoxMaxX", "boundingBoxMaxY", "boundingBoxMaxZ", "boundingBoxSize", "boundingBoxSizeX", "boundingBoxSizeY", "boundingBoxSizeZ", "center", "boundingBoxCenterX", "boundingBoxCenterY", "boundingBoxCenterZ", "matrix", "inverseMatrix", "worldMatrix", "worldInverseMatrix", "parentMatrix", "parentInverseMatrix", "visibility", "intermediateObject", "template", "ghosting", "instObjGroups", "instObjGroups.objectGroups", "instObjGroups.objectGroups.objectGrpCompList", "instObjGroups.objectGroups.objectGroupId", "instObjGroups.objectGroups.objectGrpColor", "objectColorRGB", "objectColorR", "objectColorG", "objectColorB", "useObjectColor", "objectColor", "drawOverride", "overrideDisplayType", "overrideLevelOfDetail", "overrideShading", "overrideTexturing", "overridePlayback", "overrideEnabled", "overrideVisibility", "overrideColor", "lodVisibility", "selectionChildHighlighting", "renderInfo", "identification", "layerRenderable", "layerOverrideColor", "renderLayerInfo", "renderLayerInfo.renderLayerId", "renderLayerInfo.renderLayerRenderable", "renderLayerInfo.renderLayerColor", "ghostingControl", "ghostCustomSteps", "ghostPreSteps", "ghostPostSteps", "ghostStepSize", "ghostFrames", "ghostColorPreA", "ghostColorPre", "ghostColorPreR", "ghostColorPreG", "ghostColorPreB", "ghostColorPostA", "ghostColorPost", "ghostColorPostR", "ghostColorPostG", "ghostColorPostB", "ghostRangeStart", "ghostRangeEnd", "ghostDriver", "hiddenInOutliner", "renderable", "cameraAperture", "horizontalFilmAperture", "verticalFilmAperture", "shakeOverscan", "shakeOverscanEnabled", "filmOffset", "horizontalFilmOffset", "verticalFilmOffset", "shakeEnabled", "shake", "horizontalShake", "verticalShake", "stereoHorizontalImageTranslateEnabled", "stereoHorizontalImageTranslate", "postProjection", "preScale", "filmTranslate", "filmTranslateH", "filmTranslateV", "filmRollControl", "filmRollPivot", "horizontalRollPivot", "verticalRollPivot", "filmRollValue", "filmRollOrder", "postScale", "filmFit", "filmFitOffset", "overscan", "panZoomEnabled", "renderPanZoom", "pan", "horizontalPan", "verticalPan", "zoom", "focalLength", "lensSqueezeRatio", "cameraScale", "triggerUpdate", "nearClipPlane", "farClipPlane", "fStop", "focusDistance", "shutterAngle", "centerOfInterest", "orthographicWidth", "imageName", "depthName", "maskName", "tumblePivot", "tumblePivotX", "tumblePivotY", "tumblePivotZ", "usePivotAsLocalSpace", "imagePlane", "homeCommand", "bookmarks", "locatorScale", "displayGateMaskOpacity", "displayGateMask", "displayFilmGate", "displayResolution", "displaySafeAction", "displaySafeTitle", "displayFieldChart", "displayFilmPivot", "displayFilmOrigin", "clippingPlanes", "bestFitClippingPlanes", "depthOfField", "motionBlur", "orthographic", "journalCommand", "image", "depth", "transparencyBasedDepth", "threshold", "depthType", "useExploreDepthFormat", "mask", "displayGateMaskColor", "displayGateMaskColorR", "displayGateMaskColorG", "displayGateMaskColorB", "backgroundColor", "backgroundColorR", "backgroundColorG", "backgroundColorB", "focusRegionScale", "displayCameraNearClip", "displayCameraFarClip", "displayCameraFrustum", "cameraPrecompTemplate", "vraySeparator_vray_cameraPhysical", "vrayCameraPhysicalOn", "vrayCameraPhysicalType", "vrayCameraPhysicalFilmWidth", "vrayCameraPhysicalFocalLength", "vrayCameraPhysicalSpecifyFOV", "vrayCameraPhysicalFOV", "vrayCameraPhysicalZoomFactor", "vrayCameraPhysicalDistortionType", "vrayCameraPhysicalDistortion", "vrayCameraPhysicalLensFile", "vrayCameraPhysicalDistortionMap", "vrayCameraPhysicalDistortionMapR", "vrayCameraPhysicalDistortionMapG", "vrayCameraPhysicalDistortionMapB", "vrayCameraPhysicalFNumber", "vrayCameraPhysicalHorizLensShift", "vrayCameraPhysicalLensShift", "vrayCameraPhysicalLensAutoVShift", "vrayCameraPhysicalShutterSpeed", "vrayCameraPhysicalShutterAngle", "vrayCameraPhysicalShutterOffset", "vrayCameraPhysicalLatency", "vrayCameraPhysicalISO", "vrayCameraPhysicalSpecifyFocus", "vrayCameraPhysicalFocusDistance", "vrayCameraPhysicalExposure", "vrayCameraPhysicalWhiteBalance", "vrayCameraPhysicalWhiteBalanceR", "vrayCameraPhysicalWhiteBalanceG", "vrayCameraPhysicalWhiteBalanceB", "vrayCameraPhysicalVignetting", "vrayCameraPhysicalVignettingAmount", "vrayCameraPhysicalBladesEnable", "vrayCameraPhysicalBladesNum", "vrayCameraPhysicalBladesRotation", "vrayCameraPhysicalCenterBias", "vrayCameraPhysicalAnisotropy", "vrayCameraPhysicalUseDof", "vrayCameraPhysicalUseMoBlur", "vrayCameraPhysicalApertureMap", "vrayCameraPhysicalApertureMapR", "vrayCameraPhysicalApertureMapG", "vrayCameraPhysicalApertureMapB", "vrayCameraPhysicalApertureMapAffectsExposure", "vrayCameraPhysicalOpticalVignetting", "vraySeparator_vray_cameraOverrides", "vrayCameraOverridesOn", "vrayCameraType", "vrayCameraOverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve",'aiFiltermap','aiShutterCurve.aiShutterCurveX','aiShutterCurve.aiShutterCurveY','aiPosition.aiPositionX','aiPosition.aiPositionY','aiPosition.aiPositionZ','aiLookAt.aiLookAtX','aiLookAt.aiLookAtY','aiLookAt.aiLookAtZ','aiUp.aiUpX','aiUp.aiUpY','aiUp.aiUpZ','aiScreenWindowMin.aiScreenWindowMinX','aiScreenWindowMin.aiScreenWindowMinY','aiScreenWindowMax.aiScreenWindowMaxX','aiScreenWindowMax.aiScreenWindowMaxY']
        #'aiFiltermap','aiShutterCurve.aiShutterCurveX','aiShutterCurve.aiShutterCurveY','aiPosition.aiPositionX','aiPosition.aiPositionY','aiPosition.aiPositionZ','aiLookAt.aiLookAtX','aiLookAt.aiLookAtY','aiLookAt.aiLookAtZ','aiUp.aiUpX','aiUp.aiUpY','aiUp.aiUpZ','aiScreenWindowMin.aiScreenWindowMinX','aiScreenWindowMin.aiScreenWindowMinY','aiScreenWindowMax.aiScreenWindowMaxX','aiScreenWindowMax.aiScreenWindowMaxY'
        attr_check = ["vraySeparator_vray_cameraPhysical","vrayCameraPhysicalOn","vrayCameraPhysicalType","vrayCameraPhysicalFilmWidth","vrayCameraPhysicalFocalLength","vrayCameraPhysicalSpecifyFOV","vrayCameraPhysicalFOV","vrayCameraPhysicalZoomFactor","vrayCameraPhysicalDistortionType","vrayCameraPhysicalDistortion","vrayCameraPhysicalLensFile","vrayCameraPhysicalDistortionMap","vrayCameraPhysicalDistortionMapR",
        "vrayCameraPhysicalDistortionMapG","vrayCameraPhysicalDistortionMapB","vrayCameraPhysicalFNumber","vrayCameraPhysicalHorizLensShift","vrayCameraPhysicalLensShift","vrayCameraPhysicalLensAutoVShift","vrayCameraPhysicalShutterSpeed","vrayCameraPhysicalShutterAngle","vrayCameraPhysicalShutterOffset","vrayCameraPhysicalLatency","vrayCameraPhysicalISO","vrayCameraPhysicalSpecifyFocus","vrayCameraPhysicalFocusDistance",
        "vrayCameraPhysicalExposure","vrayCameraPhysicalWhiteBalance","vrayCameraPhysicalWhiteBalanceR","vrayCameraPhysicalWhiteBalanceG","vrayCameraPhysicalWhiteBalanceB","vrayCameraPhysicalVignetting","vrayCameraPhysicalVignettingAmount","vrayCameraPhysicalBladesEnable","vrayCameraPhysicalBladesNum","vrayCameraPhysicalBladesRotation","vrayCameraPhysicalCenterBias","vrayCameraPhysicalAnisotropy","vrayCameraPhysicalUseDof","vrayCameraPhysicalUseMoBlur"
        ,"vrayCameraPhysicalApertureMap","vrayCameraPhysicalApertureMapR","vrayCameraPhysicalApertureMapG","vrayCameraPhysicalApertureMapB","vrayCameraPhysicalApertureMapAffectsExposure","vrayCameraPhysicalOpticalVignetting","vraySeparator_vray_cameraOverrides","vrayCameraOverridesOn","vrayCameraType", "vrayCameraOverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve","renderable"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        camera_overides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        return(camera_overrides_dic)

    def light_overrides(self):
        light_overrides_dic = {}
        attr_overrides_dic = light_overrides_dic
        object_label = "light_overide"
        object_type = "VRayLightRectShape"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType"
        ,"rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY",
        "boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template"
        ,"ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","useObjectColor","objectColor","drawOverride",
        "overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","overrideColor","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo"
        ,"renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB"
        ,"ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","renderType","renderVolume","visibleFraction","motionBlur","visibleInReflections","visibleInRefractions","castsShadows","receiveShadows"
        ,"maxVisibilitySamplesOverride","maxVisibilitySamples","geometryAntialiasingOverride","antialiasingLevel","shadingSamplesOverride","shadingSamples","maxShadingSamples","volumeSamplesOverride","volumeSamples","depthJitter","ignoreSelfShadowing","primaryVisibility","referenceObject","compInstObjGroups"
        ,"compInstObjGroups.compObjectGroups","compInstObjGroups.compObjectGroups.compObjectGrpCompList","compInstObjGroups.compObjectGroups.compObjectGroupId","underWorldObject","localPosition","localPositionX","localPositionY","localPositionZ","worldPosition","worldPosition.worldPositionX","worldPosition.worldPositionY"
        ,"worldPosition.worldPositionZ","localScale","localScaleX","localScaleY","localScaleZ","units","colorMode","shapeType","directionalPreview","showTex","targetDist","targetPos","targetPosX","targetPosY","targetPosZ","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity",
        "lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","enabled","lightColor","colorR","colorG","colorB","temperature","uSize","vSize","shadows","shadowColor","shadowColorR","shadowColorG","shadowColorB","intensityMult"
        ,"directional","directionalPreviewLength","doubleSided","invisible","affectDiffuse","affectSpecular","affectReflections","ignoreLightNormals","noDecay","skylightPortal","simpleSkylightPortal","storeWithIrradianceMap","rectTex","rectTexR","rectTexG","rectTexB","rectTexA","useRectTex","multiplyByTheLightColor","texResolution"
        ,"texAdaptive","subdivs","shadowBias","cutoffThreshold","locatorScale","photonSubdivs","causticsSubdivs","diffuseMult","causticMult","diffuseContrib","specularContrib","useMIS","vrayOverrideMBSamples","vrayMBSamples","outA","outAX","outAY","outAZ","outApiType","outApiClassification","outTemperatureColor","outTemperatureColorR"
        ,"outTemperatureColorG","outTemperatureColorB","emitDiffuse","emitSpecular","decayRate","attributeAliasList","pickTexture"]
        attr_check = ["lightColor","intensityMult","shapeType","uSize","vSize","directional","useRectTex","rectTex","noDecay","doubleSided","invisible","skylightPortal","simpleSkylightPortal","affectDiffuse","affectSpecular","affectReflections","shadows","shadowColor","shadowBias","visibility","colorR","colorG","colorB","emitDiffuse","emitSpecular",
        "decayRate","attributeAliasList","diffuseContrib","specularContrib","enabled"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        light_overrides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "spotLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","coneAngle","penumbraAngle","dropoff","barnDoors","leftBarnDoor","rightBarnDoor","topBarnDoor","bottomBarnDoor","useDecayRegions","startDistance1","endDistance1","startDistance2","endDistance2","startDistance3","endDistance3","fogSpread","fogIntensity","objectType","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","rayDirection","rayDirectionX","rayDirectionY","rayDirectionZ","fogGeometry","lightGlow","psIllumSamples"]
        attr_check = ["color","intensity","emitDiffuse","emitSpecular","decayRate","coneAngle","penumbraAngle","dropoff","shadowColor","useRayTraceShadows","lightRadius","shadowRays","rayDepthLimit","useDepthMapShadows","dmapResolution","useMidDistDmap","useDmapAutoFocus","dmapFocus","dmapFilterSize","dmapBias","fogShadowIntensity","volumeShadowSamples"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        light_overrides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "ambientLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","ambientShade","objectType","shadowRadius","castSoftShadows","normalCamera","normalCameraX","normalCameraY","normalCameraZ","receiveShadows"]
        attr_check = ["color","intensity","ambientShade"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        light_overrides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "directionalLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","useLightPosition","objectType","lightAngle","pointWorld","pointWorldX","pointWorldY","pointWorldZ"]
        attr_check = ["color","intensity","emitDiffuse","emitSpecular"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        light_overrides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        object_type = "pointLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","fogGeometry","fogRadius","lightGlow","objectType","fogType","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","fogIntensity"]
        attr_check = ["color","intensity","emitDiffuse","emitSpecular","decayRate"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        light_overrides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        return(light_overrides_dic)

    def vray_settings_overrides(self):
        vray_settings_overrides_dic = {}
        attr_overrides_dic = vray_settings_overrides_dic
        object_label = "vs"
        cmds.loadPlugin('vrayformaya', quiet=True)
        cmds.pluginInfo('vrayformaya', edit=True, autoload=True)
        cmds.setAttr("defaultRenderGlobals.ren", "vray", type = "string")

        object_type = "VRaySettingsNode"
        remove_attr_List =  cmds.listAttr("vraySettings")
        attr_check = ["cam_envtexBg","cam_envtexGi","cam_envtexReflect","cam_envtexRefract","cam_envtexSecondaryMatte","globopt_geom_displacement","globopt_light_doLights","globopt_light_doHiddenLights","globopt_light_doDefaultLights",
        "globopt_light_doShadows","globopt_light_ignoreLightLinking","globopt_light_disableSelfIllumination","photometricScale","globopt_mtl_reflectionRefraction","globopt_mtl_glossy","globopt_mtl_transpMaxLevels","globopt_mtl_transpCutoff"
        ,"globopt_mtl_doMaps","globopt_mtl_filterMaps","bumpMultiplier","texFilterScaleMultiplier","globopt_ray_bias","globopt_ray_maxIntens_on","gi_texFilteringMultiplier","cam_overrideEnvtex","cam_overrideEnvtexSecondaryMatte",
        "ddisplac_amount","ddisplac_edgeLength","ddisplac_maxSubdivs","giOn","reflectiveCaustics","refractiveCaustics","secondaryMultiplier","secondaryEngine","saturation","contrast","contrastBase","aoOn","aoAmount","aoRadius","aoSubdivs",
        "giRayDistOn","giRayDist","causticsOn","causticsMultiplier","causticsSearchDistance","causticsMaxPhotons","causticsMaxDensity","minShadeRate"]
        for attr in attr_check:
            remove_attr_List.remove(attr)
        vray_settings_overrides = self.overides_information_summary(object_type,remove_attr_List,attr_overrides_dic,object_label)
        self.attr_override_detect(object_label)

        return(vray_settings_overrides_dic)

    def objects_in_render_layer(self):
        object_in_layer_dic = {}
        for render_layer in self.render_layers:
            objects_in_layer = cmds.editRenderLayerMembers(render_layer, query = True) or []
            for object in self.object_check:
                for objects in objects_in_layer:
                    if object == objects:
                        object_layer_string = object + "_" + render_layer
                        object_in_layer_dic[object_layer_string] = render_layer

        return(object_in_layer_dic)

    def render_stat_overrides(self):
        render_stat_override_dic = {}
        exclude_list = ["camera","ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight","VRayLightSphereShape","VRayLightRectShape","VRayLightDomeShape","VRayLightIESShape"]
        siz = len(self.object_check_g)
        render_layer = 0
        while render_layer < siz:
            for object in self.object_check_g:
                object_type = cmds.objectType(object)
                for exclude_node in exclude_list:
                    if exclude_node == object_type:
                        self.object_check_g.remove(object)
            render_layer = render_layer + 1
        for object in self.object_check_g:
            object_type = cmds.objectType(object)
            if object_type != "locator":
                Render_Stat_List = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions","doubleSided"]
                for render_stat in Render_Stat_List:
                    attr_string = object + "." + render_stat
                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                    value_default = cmds.getAttr(attr_string)
                    for render_layer in self.render_layers:
                        if render_layer != "defaultRenderLayer":
                            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                            value = cmds.getAttr(attr_string)
                            if value != value_default:
                                dic_string = object + "**" + "render_stats" + "**" +  render_stat + "**" + render_layer
                                render_stat_override_dic[dic_string] = value
            return(render_stat_override_dic)

    def vray_object_prop_overrides(self):
        vray_object_props = cmds.ls(type = "VRayObjectProperties")
        vray_object_property_overrides_dic = {}
        object_props = ["overrideMBSamples","mbSamples","objectIDEnabled","objectID","skipExportEnabled","skipExport","ignore",
        "useIrradianceMap","generateGI","generateGIMultiplier","receiveGI","receiveGIMultiplier","giSubdivsMultiplier","giSubdivsMultiplier","generateCaustics",
        "receiveCaustics","causticsMultiplier","giVisibility","primaryVisibility","reflectionVisibility","refractionVisibility","shadowVisibility","receiveShadows","matteSurface",
        "alphaContribution","generateRenderElements","shadows","affectAlpha","shadowTintColor","shadowBrightness","reflectionAmount","refractionAmount","giAmount","noGIOnOtherMattes",
        "matteForSecondaryRays","giSurfaceID","useReflectionExclude","reflectionListIsInclusive","useRefractionExclude","refractionListIsInclusive","blackBox",
        "rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType"]
        for vray_object_prop in vray_object_props:
            for op in object_props:
                cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
                value_string = vray_object_prop + "." + op
                value_default = cmds.getAttr(value_string)
                for render_layer in self.render_layers:
                    if render_layer != "defaultRenderLayer":
                        cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                        value = cmds.getAttr(value_string)
                        if value != value_default:
                            dic_string = vray_object_prop + "**" + "vrayObjProp" + "**" + op + "**" + render_layer
                            vray_object_property_overrides_dic[dic_string] = value
        return(vray_object_property_overrides_dic)

    def rebuild_selected_layer(self):
        rebuild_selected_layer = 1
        self.rebuild_layers(rebuild_selected_layer)

    def rebuild_all_layers(self):
        rebuild_selected_layer = 0
        self.rebuild_layers(rebuild_selected_layer)

    def rebuild_layers(self,rebuild_selected_layer):
        active_layers = []
        self.unlock_cameras()
        for mPanel in self.panels:
            cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        start_layer = self.initial_layer
        if rebuild_selected_layer == 1:
            active_layers.append(start_layer)
        if rebuild_selected_layer == 0:
            active_layers = self.render_layers
        object_check = self.object_check_g + self.object_check_transform + self.object_check_cameras
        light_types = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
        overrides = self.overides_information_function()
        vray_object_props = cmds.ls(type = "VRayObjectProperties")
        render_stats = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions"]
        vraySettings = cmds.listAttr("vraySettings")
        vraySettings_overrides =  overrides[0] or []
        transform_overrides = overrides[1] or []
        material_overrides = overrides[2] or []
        #print 'material_overrides = ',material_overrides
        camera_overrides = overrides[6] or []
        light_overrides = overrides[3] or []
        render_stats_overrides = overrides[4] or []
        vray_object_prop_overrides = overrides[5] or []
        for render_layer in active_layers:
            if render_layer != "defaultRenderLayer":
                objects_in_layer = cmds.editRenderLayerMembers( render_layer, fn = True,query=True ) or []
                objects_visibility_dic = {}
                for object in object_check:
                    visibility_example = cmds.attributeQuery("visibility",node = object,exists = True)
                    if visibility_example == 1:
                        cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                        visibility_string = (object + ".visibility")
                        visibility_state = cmds.getAttr(visibility_string)
                        string_key = (object + "%" + str(visibility_state))
                        objects_visibility_dic[string_key] = visibility_state
                cmds.createRenderLayer(objects_in_layer, name = (render_layer + "_copy"))
                cmds.editRenderLayerGlobals(currentRenderLayer = (render_layer + "_copy"))
                cmds.rename(render_layer,("**_" + render_layer + "_old"))
                cmds.rename((render_layer + "_copy"),render_layer)
                for object_in_layer in objects_in_layer:
                    cmds.editRenderLayerMembers((render_layer),object_in_layer)
                for object in self.object_check:
                    for object_visibility_dic in objects_visibility_dic:
                         object_visibility_dic_split = object_visibility_dic.split("%")
                         if object_visibility_dic_split[0] == object:
                             if object_visibility_dic_split[1] == "True":
                                ste = 1
                             if object_visibility_dic_split[1] == "False":
                                ste = 0
                             node_type = cmds.nodeType(object_visibility_dic_split[0])
                             if node_type != "camera":
                                 lock_state = cmds.lockNode(object_visibility_dic_split[0],lock = True, query = True)
                                 lock_state = lock_state[0]
                                 if lock_state == 0:
                                     cmds.setAttr((object_visibility_dic_split[0] + ".visibility"),ste)
                for transform_override in transform_overrides:
                    transform_override_split = transform_override.split("$")
                    layer = transform_override_split[2]
                    for object in self.object_check:
                        if object == transform_override_split[1]:
                            if layer == render_layer:
                                value = transform_overrides[transform_override]
                                if "translate" in transform_override_split[3]:
                                    cmds.editRenderLayerAdjustment(object + ".translate")
                                    cmds.setAttr((object + "." + transform_override_split[3]),value)
                                if "rotate" in transform_override_split[3]:
                                    cmds.editRenderLayerAdjustment(object + ".rotate")
                                    cmds.setAttr((object + "." + transform_override_split[3]),value)
                                if "scale" in transform_override_split[3]:
                                    cmds.editRenderLayerAdjustment(object + ".scale")
                                    cmds.setAttr((object + "." + transform_override_split[3]),value)
                for lo in light_overrides:
                    #print 'lo = ',lo
                    ramp_removed_found = 0
                    if "ramp_removed" in lo or "ramp_mismatch" in lo:
                        ramp_removed_found = 1
                    #print 'ramp_removed_found = ',ramp_removed_found
                    light_override_original = lo
                    light_override_original_split = lo.split("**")
                    lo = light_override_original_split[0]
                    layer = light_override_original_split[1]
                    layer = layer[:-1]
                    light_override_original_split = lo.split("*")
                    lo = light_override_original_split[1]
                    light_override_object_split = lo.split(".")
                    for object in self.object_check:
                        if "spotLight" in object or "ambientLight" in object or "directionalLight" in object or "pointLight" in object:
                            kid = cmds.listRelatives(object,children = True)
                            object = kid[0]
                        if object == light_override_object_split[0]:
                            if layer == render_layer:
                                value = light_overrides[light_override_original]
                                typ = type(value)
                                kind_list = type(value) is list
                                kind_int = type(value) is int
                                kind_float = type(value) is float
                                kind_bool = type(value) is bool
                                kind_unicode = type(value) is unicode
                                if kind_list == 1:
                                    value_sub = value[0]
                                    value_a = value_sub[0]
                                    value_b = value_sub[1]
                                    value_c = value_sub[2]
                                    cmds.editRenderLayerAdjustment(lo)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(light_override_original_split[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    #print 'object = ',object
                                    #print 'typ = ',typ
                                    #print 'kind_list = ',kind_list
                                    #print 'light_override_original_split[1] = ',light_override_original_split[1]
                                    #print 'value_a = ',value_a
                                    #print 'value_b = ',value_b
                                    #print 'value_c = ',value_c
                                    check_for_rectText_split = light_override_original_split[1].split('.')
                                    #print 'check_for_rectText_split = ',check_for_rectText_split
                                    check_for_rectText = check_for_rectText_split[1]
                                    #print 'check_for_rectText = ',check_for_rectText
                                    if ramp_removed_found == 0:
                                        if check_for_rectText != 'rectTex':
                                            #print 'executing setAttr'
                                            cmds.setAttr(light_override_original_split[1],value_a,value_b,value_c)
                                if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                    cmds.editRenderLayerAdjustment(lo)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(light_override_original_split[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    cmds.setAttr(light_override_original_split[1],value)
                                if kind_unicode == 1:
                                    cmds.editRenderLayerAdjustment(lo)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(light_override_original_split[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    if "intensity" in lo or "penumbraAngle" in lo or "dropoff" in lo:
                                        cmds.connectAttr((value + ".outAlpha"),lo,force = True)
                                    else:
                                        cmds.connectAttr((value + ".outColor"),lo,force = True)
                for mo in material_overrides:
                    #print ' '
                    #print ' '
                    #print 'material_overrides = ',material_overrides
                    #print 'rebuilding layers MO '
                    #print 'mo = ',mo
                    if "material_overide" in mo:
                        ramp_removed_found = 0
                        if "ramp_removed" in mo:
                            #print 'ramp_removed'
                            ramp_removed_found = 1
                        mo_original = mo
                        #print 'mo_original = ',mo_original
                        mo_split = mo.split("**")
                        #print 'mo_split = ',mo_split
                        layer = mo_split[1]
                        #print '[1] layer = ',layer
                        layer = layer[:-1]
                        #print 'after :-1 layer = ',layer
                        mo_split_two = mo.split("*")
                        mo = mo_split_two[1]
                        #print 'mo = ',mo
                        mo_object_split = mo.split(".")
                        for material in self.materials:
                            #print 'material = ',material
                            if material == mo_object_split[0]:
                                #print 'mo_object_split[0] = ',mo_object_split[0]
                                #print 'layer = ',layer
                                #print 'render_layer = ',render_layer
                                if layer == render_layer:
                                    #print 'layer = render_layer'
                                    value = material_overrides[mo_original]
                                    #print 'value = ',value
                                    typ = type(value)
                                    #print 'typ = ',typ
                                    kind_list = type(value) is list
                                    kind_int = type(value) is int
                                    kind_float = type(value) is float
                                    kind_bool = type(value) is bool
                                    kind_unicode = type(value) is unicode
                                    if kind_list == 1:
                                        value_sub = value[0]
                                        value_a = value_sub[0]
                                        value_b = value_sub[1]
                                        value_c = value_sub[2]
                                        cmds.editRenderLayerAdjustment(mo)
                                        if ramp_removed_found == 1:
                                            #print 'ramp_removed_found = 1'
                                            a = 1
                                            destination_connections = cmds.listConnections(mo_split_two[1], destination = False, plugs = True, connections = True) or []
                                            destination_connections_size = len(destination_connections)
                                            #print 'destination_connections_size = ',destination_connections_size
                                            while a < destination_connections_size:
                                                #print 'disconnectAttr connections ',destination_connections[1] + ' ' + destination_connections[0]
                                                cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                                a = a + 1
                                        #print 'setting ',mo_split_two[1] + str(value_a) + str(value_b) + str(value_c)
                                        cmds.setAttr(mo_split_two[1],value_a,value_b,value_c)
                                    if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                        #print 'kind = float, int, or bool'
                                        cmds.editRenderLayerAdjustment(mo,layer = render_layer)
                                        if ramp_removed_found == 1:
                                            a = 1
                                            destination_connections = cmds.listConnections(mo_split_two[1], destination = False, plugs = True, connections = True) or []
                                            destination_connections_size = len(destination_connections)
                                            while a < destination_connections_size:
                                                cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                                a = a + 1
                                        #print 'setting ',mo_split_two[1] + str(value)
                                        cmds.setAttr(mo_split_two[1],value)
                                    if kind_unicode == 1:
                                        cmds.editRenderLayerAdjustment(mo)
                                        if ramp_removed_found == 1:
                                            a = 1
                                            destination_connections = cmds.listConnections(mo_split_two[1], destination = False, plugs = True, connections = True) or []
                                            destination_connections_size = len(destination_connections)
                                            while a < destination_connections_size:
                                                cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                                a = a + 1
                                        cmds.connectAttr((value + ".outColor"),mo,force = True)
                    if "materialAssignment" in mo:
                        mo_original = mo
                        mo_split_two = mo.split("$")
                        layer = mo_split_two[1]
                        mo = mo_split_two[2]
                        moAo = mo_split_two[0]
                        for material in self.materials:
                            if material == mo_split_two[0]:
                                if layer == render_layer:
                                    value = material_overrides[mo_original]
                                    typ = type(value)
                                    cmds.select(moAo)
                                    cmds.hyperShade(assign = value)
                for rs in render_stats_overrides:
                    rs_original = rs
                    rs_split = rs.split("**")
                    layer = rs_split[3]
                    rs = rs_split[0]
                    rs_split_two = rs_split[2]
                    rs_attr = rs_split_two
                    rs = rs + "." + rs_split_two
                    for rS in render_stats:
                        if rs_attr == rS:
                            if layer == render_layer:
                                value = render_stats_overrides[rs_original]
                                typ = type(value)
                                kind_list = type(value) is list
                                kind_int = type(value) is int
                                kind_float = type(value) is float
                                kind_bool = type(value) is bool
                                kind_unicode = type(value) is unicode
                                if kind_list == 1:
                                    value_sub = value[0]
                                    value_a = value_sub[0]
                                    value_b = value_sub[1]
                                    value_c = value_sub[2]
                                    cmds.editRenderLayerAdjustment(rs)
                                    cmds.setAttr(rs,value_a,value_b,value_c)
                                if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                    cmds.editRenderLayerAdjustment(rs)
                                    cmds.setAttr(rs,value)
                                if kind_unicode == 1:
                                    cmds.editRenderLayerAdjustment(rs)
                                    cmds.connectAttr((value + ".outColor"),rs,force = True)
                for vray_object_prop in vray_object_prop_overrides:
                    vray_object_prop_original = vray_object_prop
                    vray_object_prop_original_split = vray_object_prop.split("**")
                    layer = vray_object_prop_original_split[3]
                    vray_object_prop = vray_object_prop_original_split[0]
                    vrpFull = vray_object_prop + "." + vray_object_prop_original_split[2]
                    for vrpB in vray_object_props:
                        if vray_object_prop == vrpB:
                            if layer == render_layer:
                                value = vray_object_prop_overrides[vray_object_prop_original]
                                typ = type(value)
                                kind_list = type(value) is list
                                kind_int = type(value) is int
                                kind_float = type(value) is float
                                kind_bool = type(value) is bool
                                kind_unicode = type(value) is unicode
                                if kind_list == 1:
                                    value_sub = value[0]
                                    value_a = value_sub[0]
                                    value_b = value_sub[1]
                                    value_c = value_sub[2]
                                    cmds.editRenderLayerAdjustment(vrpFull)
                                    cmds.setAttr(vrpFull,value_a,value_b,value_c)
                                if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                    cmds.editRenderLayerAdjustment(vrpFull)
                                    cmds.setAttr(vrpFull,value)
                                if kind_unicode == 1:
                                    cmds.editRenderLayerAdjustment(vrpFull)
                                    cmds.connectAttr((value + ".outColor"),vrpFull,force = True)
                for vray_render_setting in vraySettings_overrides:
                    ramp_removed_found = 0
                    if "ramp_removed" in vray_render_setting:
                        ramp_removed_found = 1
                    vray_render_setting_original = vray_render_setting
                    vray_render_setting_split = vray_render_setting.split("**")
                    vray_render_setting = vray_render_setting_split[0]
                    layer = vray_render_setting_split[1]
                    layer = layer[:-1]
                    vray_render_setting_split = vray_render_setting.split("*")
                    vray_render_setting = vray_render_setting_split[1]
                    vray_render_setting_full = vray_render_setting
                    for vray_render_setting_two in vraySettings:
                        vray_render_setting_two = "vraySettings." + vray_render_setting_two
                        if vray_render_setting == vray_render_setting_two:
                            if layer == render_layer:
                                value = vraySettings_overrides[vray_render_setting_original]
                                typ = type(value)
                                kind_list = type(value) is list
                                kind_int = type(value) is int
                                kind_float = type(value) is float
                                kind_bool = type(value) is bool
                                kind_unicode = type(value) is unicode
                                if kind_list == 1:
                                    value_sub = value[0]
                                    value_a = value_sub[0]
                                    value_b = value_sub[1]
                                    value_c = value_sub[2]
                                    cmds.editRenderLayerAdjustment(vray_render_setting_full)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(vray_render_setting_split[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    cmds.setAttr(vray_render_setting_full,value_a,value_b,value_c)
                                if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                    cmds.editRenderLayerAdjustment(vray_render_setting_full)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(vray_render_setting_split[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    cmds.setAttr(vray_render_setting_full,value)
                                if kind_unicode == 1:
                                    cmds.editRenderLayerAdjustment(vray_render_setting_full)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(vray_render_setting_split[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    cmds.connectAttr((value + ".outColor"),vray_render_setting_full, force = True)
                for ramp_override in self.ramp_overrides:
                    #print 'ramp_override = ',ramp_override
                    ramp_override_split = ramp_override.split('&&')
                    #print 'ramp_override_split = ',ramp_override_split
                    ramp_override_layer = ramp_override_split[0]
                    #print 'ramp_override_layer = ',ramp_override_layer
                    ramp_override_ramp = ramp_override_split[1]
                    #print 'ramp_override_ramp = ',ramp_override_ramp
                    ramp_override_attr = ramp_override_split[2]
                    #print 'ramp_override_attr = ',ramp_override_attr
                    ramp_override_value = ramp_override_split[3]
                    #print 'ramp_override_value = ',ramp_override_value
                    cmds.editRenderLayerAdjustment(ramp_override_attr)
                    if ramp_override_layer == render_layer:
                        override_value_split = ramp_override_value.split(',')
                        #print 'override_value_split = ',override_value_split
                        size_of_override_value = len(override_value_split)
                        if size_of_override_value > 1:
                            override_value_split[0] = override_value_split[0].replace('(','')
                            override_value_split[2] = override_value_split[2].replace(')','')
                            override_value_split[0] = float(override_value_split[0])
                            override_value_split[1] = float(override_value_split[1])
                            override_value_split[2] = float(override_value_split[2])
                            #print 'ramp_override_attr = ',ramp_override_attr
                            #print 'override_value_split[0] = ',override_value_split[0]
                            #print 'override_value_split[2] = ',override_value_split[2]
                            #print 'override_value_split[0] = ',override_value_split[0]
                            #print 'override_value_split[1] = ',override_value_split[1]
                            #print 'override_value_split[2] = ',override_value_split[2]
                            cmds.setAttr(ramp_override_attr,override_value_split[0],override_value_split[1],override_value_split[2], type = 'double3')
                        if size_of_override_value < 2:
                            ramp_override_value = float(ramp_override_value)
                            #print 'ramp_override_attr = ',ramp_override_attr
                            #print 'ramp_override_value = ',ramp_override_value
                            cmds.setAttr(ramp_override_attr,ramp_override_value)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)
        self.fix_cam_layer_assignments()

#---
    def add_object_to_all_layers(self):
        selected_objects = cmds.ls(sl = True)
        for selected_object in selected_objects:
            for render_layer in self.render_layers:
                if render_layer != "defaultRenderLayer":
                    cmds.editRenderLayerMembers(render_layer, selected_object)
        cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def remove_object_from_all_layers(self):
        selected_objects = cmds.ls(sl = True)
        for selected_object in selected_objects:
            for render_layer in self.render_layers:
                if render_layer != "defaultRenderLayer":
                    cmds.editRenderLayerMembers(render_layer, selected_object, remove = True)
        cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def make_object_visible_in_all_layers(self):
        #for mPanel in self.panels:
            #cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        selected_objects = cmds.ls(sl = True)
        for selected_object in selected_objects:
            for render_layer in self.render_layers:
                if render_layer != "defaultRenderLayer":
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                    cmds.setAttr(selected_object + '.visibility', 1)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)


    def hide_object_in_all_layers(self):
        #for mPanel in self.panels:
            #cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        selected_objects = cmds.ls(sl = True)
        for selected_object in selected_objects:
            for render_layer in self.render_layers:
                if render_layer != "defaultRenderLayer":
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                    cmds.setAttr(selected_object + '.visibility', 0)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def convert_layer_names(self):
        for render_layer in self.render_layers:
            if render_layer == "C1N1":
                cmds.rename("C1N1","Ft")
            if render_layer == "C7N1":
                cmds.rename("C7N1","Bk")
            if render_layer == "C1C1":
                cmds.rename("C1C1","FtTp")
            if render_layer == "C1L1":
               cmds.rename("C1L1","FtLtTp")
            if render_layer == "C1R1":
                cmds.rename("C1R1","FtRtTp")
            if render_layer == "C2N1":
                cmds.rename("C2N1","Lt")
            if render_layer == "C8N1":
                cmds.rename("C8N1","Rt")
            if render_layer == "C3N1":
                cmds.rename("C3N1","Tp")
            if render_layer == "C9N1":
                cmds.rename("C9N1","Bt")

    def unlock_cameras(self):
        cams = cmds.ls(type = "camera")
        for camera in self.cameras:
            parent_node = cmds.listRelatives(camera, parent = True)
            parent_lock_state = cmds.lockNode(parent_node[0],lock = True, query = True)
            parent_lock_state = parent_lock_state[0]
            if parent_lock_state == 1:
                cmds.lockNode(parent_node[0], lock = 0)
            if "Shape" in camera:
                parent_node = cmds.listRelatives(camera, parent = True)
                parent_node = parent_node[0]
            else:
                parent_node = camera
            cmds.lockNode(camera, lock = 0)
            visibility_example = cmds.attributeQuery("visibility", node = camera, exists = True)
            renderable_example = cmds.attributeQuery("renderable", node = camera, exists = True)
            if visibility_example == 1:
                cmds.setAttr(parent_node + ".visibility", lock = 0)
            cmds.setAttr(parent_node + ".renderable", lock = 0)

    def evaluate_objects_in_render_layers(self):
        #print 'evaluate_objects_in_render_layers'
        #for mPanel in self.panels:
            #cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        selected_objects = cmds.ls(sl = True)
        for OIL_button in self.OIL_button_pointer_dic:
            for render_layer in self.render_layers:
                render_layer_linked_to_pointer = self.OIL_button_pointer_dic[OIL_button]
                if render_layer_linked_to_pointer == render_layer:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                    for object in selected_objects:
                        object_in_render_layer_check = cmds.editRenderLayerMembers(render_layer, object, query = True) or []
                        if object in object_in_render_layer_check:
                            #print 'setting OIL button for layer: ' + render_layer + ' to False'
                            OIL_button.setChecked(False)
                        else:
                            #print 'setting OIL button for layer: ' + render_layer + ' to True'
                            OIL_button.setChecked(True)
        cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def evaluate_objects_visible_in_render_layers(self):
        #print 'evaluate_objects_visible_in_render_layers'
        #for mPanel in self.panels:
            #cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        selected_objects = cmds.ls(sl = True)
        for OVL_button in self.OVL_button_pointer_dic:
            for render_layer in self.render_layers:
                render_layer_linked_to_pointer = self.OVL_button_pointer_dic[OVL_button]
                if render_layer_linked_to_pointer == render_layer:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                    for object in selected_objects:
                        if cmds.attributeQuery('visibility',node = object,exists = True):
                            object_visibility_check = cmds.getAttr(object + '.visibility')
                            if object_visibility_check == 1:
                                OVL_button.setChecked(False)
                            else:
                                OVL_button.setChecked(True)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def OIL_toggle_object_in_render_layer(self,OIL_button):
        #print 'OIL_toggle_object_in_render_layer'
        #for mPanel in self.panels:
            #cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        selected_objects = cmds.ls(sl = True)
        for render_layer in self.render_layers:
            render_layer_linked_to_button = self.OIL_button_pointer_dic[OIL_button]
        for render_layer in self.render_layers:
            if render_layer_linked_to_button == render_layer:
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                for object in selected_objects:
                    if OIL_button.isChecked():
                        cmds.editRenderLayerMembers(render_layer, object)
                    else:
                        cmds.editRenderLayerMembers(render_layer, object, remove = True)
        cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)
        self.populate_gui()


    def OVL_object_toggle_visibility_in_render_layer(self,OVL_button):
        #print 'OVL_toggle_visible_in_render_layer'
        #for mPanel in self.panels:
            #cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        selected_objects = cmds.ls(sl = True)
        for render_layer in self.render_layers:
            render_layer_linked_to_button = self.OVL_button_pointer_dic[OVL_button]
        for render_layer in self.render_layers:
            render_layer_linked_to_button = self.OVL_button_pointer_dic[OVL_button]
            if render_layer_linked_to_button == render_layer:
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                for object in selected_objects:
                    cmds.editRenderLayerAdjustment(object + ".visibility")
                    if OVL_button.isChecked():
                        cmds.setAttr(object + '.visibility', 1)
                    else:
                        cmds.setAttr(object + '.visibility', 0)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)
        self.populate_gui()

    def fix_cam_layer_assignments(self):
        #print 'button_fix_cam_layer_assignments'
        camera_list_modified = cmds.ls(type = "camera")
        camera_list_modified.append("perspShape")
        camera_list_modified.append("topShape")
        camera_list_modified.append("frontShape")
        camera_list_modified.append("sideShape")
        for render_layer in self.render_layers:
            if render_layer == "defaultRenderLayer":
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                for cam in camera_list_modified:
                    if cam == "perspShape":
                        cmds.setAttr(cam + ".renderable",1)
            if render_layer != "defaultRenderLayer":
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                var = 0
                for cam in camera_list_modified:
                    if "FtTp" in cam or "FtRt" in cam or "FtLt" in cam in cam or "FtLtTp" in cam or "FtRtTp" in cam or "Ft" in cam or "Bk" in cam or "Rt" in cam or "Lt" in cam or "Tp" in cam or "Bt" in cam:
                        var = 0
                    if "C1N1" in cam or "C1N1Shape" in cam or "C7N1" in cam or "C7N1Shape" in cam or "C2N1" in cam or "C2N1Shape" in cam  or "C8N1" in cam  or "C8N1Shape" in cam  or "C3N1" in cam or "C3N1Shape" in cam  or "C9N1" in cam  or "C9N1Shape" in cam or "C1C1" in cam or "C1C1Shape" in cam or "C1L1" in cam  or "C1L1Shape" in cam or "C1R1" in cam or "C1R1Shape" in cam or "C1N2" in cam or "C1NShape2" in cam or "C1N2Shape" in cam or "C1N4" in cam or "C1NShape4" in cam or "C1N4Shape" in cam:
                        var = 1
                    if "C1N1Shape1" in cam or "C7N1Shape1" in cam or "C2N1Shape1" in cam or "C8N1Shape1" in cam or "C3N1Shape1" in cam or "C9N1Shape1" in cam or "C1C1Shape1" in cam or "C1L1Shape1" in cam or "C1R1Shape1" in cam or "C1N2Shape1" in cam or "C1N4Shape1" in cam:
                        var = 2
                    if "perspShape2" in cam or "topShape2" in cam or "frontShape2" in cam or "sideShape2" in cam or "backShape1" in cam or "backShape2" in cam:
                        var = 3
                    if var == 0:
                        if cam == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape":
                            camera_layer_compare = cam.split("Shape")
                            camera_layer_compare = camera_layer_compare[0] +  camera_layer_compare[1]
                        else:
                            camera_split = cam.split("_")
                            camera_cut = camera_split[0]
                            camera_layer_compare = camera_cut
                    if var == 1:
                        if cam == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape":
                            camera_layer_compare = cam.split("Shape")
                            camera_layer_compare = camera_layer_compare[0] + camera_layer_compare[1]
                        else:
                            camera_split = cam.split("_")
                            camera_cut = camera_split[1]
                            camera_layer_compare = camera_cut.split("Shape")
                            camera_layer_compare = camera_layer_compare[0] + camera_layer_compare[1]
                    if var == 2:
                        if cam == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape":
                            camera_layer_compare = cam.split("Shape")
                            camera_layer_compare = camera_layer_compare[0] + camera_layer_compare[1]
                        else:
                            camera_split = cam.split("_")
                            camera_cut = camera_split[1]
                            camera_layer_compare = camera_cut.split("Shape")
                            camera_layer_compare = camera_layer_compare[0]
                    if var == 3:
                        if cam == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape" or cam == "backShape1" or cam == "backShape2":
                            if "2" not in cam:
                                camera_layer_compare = cam.split("Shape")
                                camera_layer_compare = camera_layer_compare[0] + camera_layer_compare[1]
                            if "2" in cam:
                                camera_layer_compare = cam.split("Shape")
                                camera_layer_compare = camera_layer_compare[0]
                        else:
                            camera_layer_compare = camera_cut.split("Shape")
                            camera_layer_compare = camera_layer_compare[0]
                    camera_layer_compareSPb = camera_layer_compare.split("Shape")
                    camera_layer_compareSPb = camera_layer_compareSPb[0]
                    if camera_layer_compare == render_layer or (camera_layer_compareSPb + "_BTY") == render_layer or (camera_layer_compareSPb + "_REF") == render_layer or (camera_layer_compareSPb + "_SHD") == render_layer or (camera_layer_compareSPb + "_REF_MATTE") == render_layer or ("BTY_" + camera_layer_compareSPb) == render_layer:
                        cmds.editRenderLayerAdjustment(cam + ".renderable")
                        cmds.setAttr(cam + ".renderable",1)
                    else:
                        cmds.editRenderLayerAdjustment(cam + ".renderable")
                        cmds.setAttr(cam + ".renderable",0)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def render_layer_change(self,button_render_layer):
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                render_layer_linked_to_button = self.render_layer_button_pointer_dic[button_render_layer]
                if render_layer_linked_to_button == render_layer:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)

    def evaluate_cameras(self):
        #print 'evaluate cameras'
        self.renderable_cameras_dic = {}
        for render_layer in self.render_layers:
            renderable_cameras = []
            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
            for camera in self.cameras:
                camera_renderable = cmds.getAttr(camera + '.renderable')
                if camera_renderable == 1:
                    renderable_cameras.append(camera)
            self.renderable_cameras_dic[render_layer] = renderable_cameras
            cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def set_render_camera(self):
        #print 'set_render_camera'
        for render_layer in self.render_layers:
            camera_comboBox_pointer = self.render_layer_camera_comboBox_dic[render_layer]
            chosen_camera = camera_comboBox_pointer.currentText()
            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
            for camera in self.cameras:
                if camera == chosen_camera:
                    cmds.editRenderLayerAdjustment((camera + '.renderable'))
                    cmds.setAttr((camera + '.renderable'), 1)
                else:
                    cmds.editRenderLayerAdjustment((camera + '.renderable'),remove = True)
                    cmds.setAttr(camera + '.renderable', 0)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def populate_gui(self):
        #print 'populate_gui'
        self.panels = cmds.getPanel( type = "modelPanel" )
        self.render_layer_camera_comboBox_dic = {}
        self.render_layer_button_pointer_dic = {}
        self.OIL_button_pointer_dic = {}
        self.OVL_button_pointer_dic = {}
        render_layer_order_dict = {}
        render_layers_in_order = []
        self.cameras = cmds.ls(type = 'camera') or []
        self.render_layers = cmds.ls(type = "renderLayer")
        for layer in self.render_layers:
            render_layer_order_number = cmds.getAttr(layer + ".displayOrder")
            render_layer_order_dict[layer] = render_layer_order_number
        number_of_render_layers = len(self.render_layers)
        i = 0
        while i <= number_of_render_layers:
            for layer in render_layer_order_dict:
                layer_number = render_layer_order_dict[layer]
                if layer_number == i:
                    render_layers_in_order.append(layer)
            i = i + 1
        render_layers_in_order.reverse()
        self.render_layers = render_layers_in_order
        self.initial_layer = cmds.editRenderLayerGlobals(query = True, currentRenderLayer = True)
        if "defaultRenderLayer" == self.render_layers[0]:
            self.render_layers.reverse()
        self.render_layers.remove('defaultRenderLayer')
        self.clear_layout(self.vertical_layout)
        self.evaluate_cameras()
        for render_layer in self.render_layers:
            self.render_layer_layout = QtWidgets.QHBoxLayout()
            self.vertical_layout.addLayout(self.render_layer_layout)
            button_OIL = QtWidgets.QPushButton('OIL')
            button_OIL.setCheckable(True)
            button_OIL.setStyleSheet("QPushButton {background:rgb(120,150,180);} QPushButton::checked{background-color: rgb(40, 40, 40);""border:0px solid rgb(80, 170, 20)};")
            button_OIL.toggle()
            self.OIL_button_pointer_dic[button_OIL] = render_layer
            button_OIL.setFixedSize(30,21)
            self.render_layer_layout.addWidget(button_OIL)
            button_OVL = QtWidgets.QPushButton('OVL')
            button_OVL.setCheckable(True)
            button_OVL.setStyleSheet("QPushButton {background:rgb(120,150,180);} QPushButton::checked{background-color: rgb(40, 40, 40);""border:0px solid rgb(80, 170, 20)};")
            button_OVL.toggle()
            self.OVL_button_pointer_dic[button_OVL] = render_layer
            button_OVL.setFixedSize(30,21)
            self.render_layer_layout.addWidget(button_OVL)
            button_render_layer = QtWidgets.QPushButton(render_layer)
            self.render_layer_button_pointer_dic[button_render_layer] = render_layer
            button_render_layer.setFixedSize(325,21)
            if render_layer == self.initial_layer:
                button_render_layer.setStyleSheet("background-color: rgb(100, 150, 190);")
            self.render_layer_layout.addWidget(button_render_layer)
            camera_comboBox = self.cameras_combobox = QtWidgets.QComboBox()
            self.render_layer_camera_comboBox_dic[render_layer] = camera_comboBox
            self.cameras_combobox.activated[str].connect(lambda:self.set_render_camera())
            self.cameras_combobox.setFixedSize(150,21)
            self.cameras_combobox.clear()
            self.render_layer_layout.addWidget(self.cameras_combobox)
            for camera in self.cameras:
                self.cameras_combobox.addItem(camera)
            renderable_cameras = self.renderable_cameras_dic[render_layer] or []
            number_of_renderable_cameras = len(renderable_cameras)
            i = 0
            for camera in self.cameras:
                if number_of_renderable_cameras > 0:
                    if camera == renderable_cameras[0]:
                        self.cameras_combobox.setCurrentIndex(i)
                i = i + 1
            if number_of_renderable_cameras > 1:
                self.cameras_combobox.setStyleSheet("background-color: rgb(130, 10, 10);")
            if number_of_renderable_cameras > 0:
                camera = renderable_cameras[0]
                camera_split = camera.split('_')
                if camera_split[0] != render_layer:
                    self.cameras_combobox.setStyleSheet("background-color: rgb(130, 10, 10);")
        self.vertical_layout.addLayout(self.layout_bottom)
        button_add_object_to_all_layers = QtWidgets.QPushButton('add selection to all render layers')
        self.layout_bottom.addWidget(button_add_object_to_all_layers)
        button_add_object_to_all_layers.pressed.connect(partial(self.add_object_to_all_layers))
        button_remove_objects_from_all_layers = QtWidgets.QPushButton('remove selection from all render layers')
        self.layout_bottom.addWidget(button_remove_objects_from_all_layers)
        button_remove_objects_from_all_layers.pressed.connect(partial(self.remove_object_from_all_layers))
        button_make_object_visible_in_all_layers = QtWidgets.QPushButton('show selection in all render layers')
        self.layout_bottom.addWidget(button_make_object_visible_in_all_layers)
        button_make_object_visible_in_all_layers.pressed.connect(partial(self.make_object_visible_in_all_layers))
        button_hide_object_in_all_layers = QtWidgets.QPushButton('hide selection in all render layers')
        self.layout_bottom.addWidget(button_hide_object_in_all_layers)
        button_hide_object_in_all_layers.pressed.connect(partial(self.hide_object_in_all_layers))
        button_convert_layer_names = QtWidgets.QPushButton('convert layer names')
        self.layout_bottom.addWidget(button_convert_layer_names)
        button_convert_layer_names.pressed.connect(partial(self.convert_layer_names))
        button_unlock_cameras = QtWidgets.QPushButton('unlock cameras')
        self.layout_bottom.addWidget(button_unlock_cameras)
        button_unlock_cameras.pressed.connect(partial(self.unlock_cameras))
        button_fix_cam_layer_assignments = QtWidgets.QPushButton('fix the render camera to render layer assignments')
        self.layout_bottom.addWidget(button_fix_cam_layer_assignments)
        button_fix_cam_layer_assignments.pressed.connect(partial(self.fix_cam_layer_assignments))
        rebuild_selected_render_layer = QtWidgets.QPushButton('rebuild selected render layer')
        self.layout_bottom.addWidget(rebuild_selected_render_layer)
        rebuild_selected_render_layer.pressed.connect(partial(self.rebuild_selected_layer))
        rebuild_all_layers = QtWidgets.QPushButton('rebuild all render layers')
        self.layout_bottom.addWidget(rebuild_all_layers)
        rebuild_all_layers.pressed.connect(partial(self.rebuild_all_layers))
        for render_layer_button in self.render_layer_button_pointer_dic:
            render_layer_button.pressed.connect(partial(self.render_layer_change,render_layer_button))
        for OIL_button in self.OIL_button_pointer_dic:
            OIL_button.pressed.connect(partial(self.OIL_toggle_object_in_render_layer,OIL_button))
        for OVL_button in self.OVL_button_pointer_dic:
            OVL_button.pressed.connect(partial(self.OVL_object_toggle_visibility_in_render_layer,OVL_button))
        self.evaluate_objects_in_render_layers()
        self.evaluate_objects_visible_in_render_layers()

    def window_gen(self):
        #print 'window_gen'
        self.window_name = "render layers tool"
        if cmds.window(self.window_name,exists = True):
            cmds.deleteUI(self.window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(self.window_name)
        window.setWindowTitle(self.window_name)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        #window.setFixedSize(550,400)
        self.vertical_layout = QtWidgets.QVBoxLayout(mainWidget)
        self.vertical_layout.setMargin(0)
        self.vertical_layout.setSpacing(0)
        self.layout_bottom = QtWidgets.QVBoxLayout()
        self.layout_bottom.setMargin(0)
        self.layout_bottom.setSpacing(0)
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["NameChanged", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerManagerChange", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerChange", self.populate_gui])
        self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["SelectionChanged", self.populate_gui])
        self.populate_gui()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    layers_tool_inst = LAYERS_WINDOW_TOOL()
    layers_tool_inst.window_gen()

main()
