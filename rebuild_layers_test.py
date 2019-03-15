import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
import re

print 'adding lower buttons'

render_layers = cmds.ls(type = "renderLayer")
light_types = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
materials_VRayMtl = cmds.ls(type = "VRayMtl")
materials_phong = cmds.ls(type = "phong")
materials_blinn = cmds.ls(type = "blinn")
materials_lambert = cmds.ls(type = "lambert")
materials_surface_shader = cmds.ls(type = "surfaceShader")
materials_displacement = cmds.ls(type = "displacementShader")
displacement_nodes = cmds.ls(type = "VRayDisplacement")
placement_nodes = cmds.ls(type = "place2dTexture")
file_nodes = cmds.ls(type = "file")
layered_textures = cmds.ls(type = "layeredTexture")
VRayBlendMtls = cmds.ls(type = "VRayBlendMtl")
materials = materials_VRayMtl + materials_phong + materials_blinn + materials_lambert + materials_surface_shader + placement_nodes + file_nodes + materials_displacement + displacement_nodes + layered_textures + VRayBlendMtls
object_check_g = cmds.ls(g = True)
object_check_t = cmds.ls(type = "transform")
object_check_cam = cmds.ls(type = "camera")
object_check = object_check_g + object_check_t + materials + object_check_cam
lites = cmds.ls(lt = True)
vray_lights = []
for o in object_check:
    nt = cmds.nodeType(o)
    for lt in light_types:
        if nt == lt:
            vray_lights.append(o)
object_check.append("vraySettings")

def overides_information_function(render_layers):
    class ATTR_OVERRIDES_CLASS:
        def __init__(self,render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check):
            render_layer_ramp_overrides = {}
            self.object_label = object_label
            self.render_layers = render_layers
            self.object_type = object_type
            print " "
            print " "
            print "self.object_type = ",self.object_type
            object_list = object_check
            if self.object_type == "camera" or self.object_type == "VRayLightRectShape" or self.object_type == "spotLight" or self.object_type == "ambientLight" or self.object_type == "directionalLight" or self.object_type == "pointLight" or self.object_type == "VRayMtl" or self.object_type == "blinn" or self.object_type == "phong" or self.object_type == "lambert" or self.object_type == "surfaceShader" or self.object_type == "displacementShader" or self.object_type == "VRayDisplacement" or self.object_type == "place2dTexture" or self.object_type == "file" or self.object_type == "layered_textures" or self.object_type == "VRayBlendMtl":
                self.object_list = cmds.ls(type = self.object_type)
            if self.object_type == "VRaySettingsNode":
                self.object_list = []
                self.object_list.append("vraySettings")
            self.attr_overrides_DIC = attr_overrides_DIC
            self.remove_attr_List = remove_attr_List

        def attr_override_detect(self):
            for obj in self.object_list:
                default_ramp = "none"
                override_ramp = "none"
                cns_count = 1
                it_list_count = 1
                it_list = []
                nt = cmds.nodeType(obj)
                if nt == self.object_type:
                    attrs = cmds.listAttr(obj)
                    for rem in self.remove_attr_List:
                        attrs.remove(rem)
                    if self.object_type == "layered_textures":
                        cns = cmds.listConnections(obj, source = True,destination = False) or []
                        cns_count = len(cns)
                        for cn in cns:
                            cn_string = cn + ".outColor"
                            connection_info = cmds.connectionInfo(cn_string,destinationFromSource = True) or []
                            for ci in connection_info:
                                if obj in ci:
                                    it_num_split_A = ci.split("[")
                                    it_num_split_B = it_num_split_A[1].split("]")
                                    it_num = it_num_split_B[0]
                                    it_list.append(it_num)
                                    it_list_count = len(it_list)
                    it = 0
                    while it < it_list_count:
                        for attr in attrs:
                            attr_string = obj + "." + attr
                            if attr == "inputs.isVisible" or attr == "inputs.alpha" or attr == "inputs.color" or attr == "inputs.blendMode":
                                it_list_2 = len(it_list)
                                if it_list_2 != 0:
                                    it_list_n = it_list[it]
                                    attr = attr.replace("inputs.","")
                                    attr_string = obj + "." + "inputs[" + str(it_list_n) + "]." + attr
                                    attr = ("inputs[" + str(it_list_n) + "]." + attr)
                            cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                            default_attr_value = cmds.getAttr(attr_string)
                            attr_connections = cmds.listConnections(attr_string,destination = False) or []
                            default_ramp_found = 0
                            for conn in attr_connections:
                                connection_type = cmds.nodeType(conn)
                                if connection_type == "ramp" or connection_type == "fractal" or connection_type == "noise" or connection_type == "file" or connection_type == "checker" or connection_type == "cloud" or connection_type == "brownian" or connection_type == "bulge" or connection_type == "VRayMtl" or connection_type == "blinn" or connection_type == "phong" or connection_type == "lambert" or connection_type == "surfaceShader":
                                    default_ramp_found = 1
                                    default_ramp = conn
                            for rl in render_layers:
                                if rl != "defaultRenderLayer":
                                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                                    cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                                    attr_connections = cmds.listConnections(attr_string,destination = False) or []
                                    override_ramp_found = 0
                                    for attrConn in attr_connections:
                                        attrType = cmds.nodeType(attrConn)
                                        if attrType == "ramp" or attrType == "fractal" or attrType == "noise" or attrType == "file" or attrType == "checker" or attrType == "cloud" or attrType == "brownian" or attrType == "bulge" or attrType == "VRayMtl" or attrType == "blinn" or attrType == "phong" or attrType == "lambert" or attrType == "surfaceShader":
                                            override_ramp_found = 1
                                            override_ramp = attrConn
                                    override_attr_value = cmds.getAttr(attr_string)
                                    if default_ramp_found == 0 and override_ramp_found == 0:
                                        if default_attr_value != override_attr_value:
                                            attr_DIC_string = self.object_label + "_overide*" + obj + "." + attr + "**" + rl + "_"
                                            self.attr_overrides_DIC[attr_DIC_string] = override_attr_value
                                    if default_ramp_found == 0 and override_ramp_found == 1:
                                        attr_DIC_string = self.object_label + "_overide_rampAdded*" + obj + "." + attr + "**" + rl + "_"
                                        self.attr_overrides_DIC[attr_DIC_string] = override_ramp
                                    if default_ramp_found == 1 and override_ramp_found == 0:
                                        override_attr_value = cmds.getAttr(attr_string)
                                        attr_DIC_string = self.object_label + "_overide_rampRemoved*" + obj + "." + attr + "**" + rl + "_"
                                        self.attr_overrides_DIC[attr_DIC_string] = override_attr_value
                                    if default_ramp_found == 1 and override_ramp_found == 1:
                                        override_ramp = attrConn
                                        if override_ramp != default_ramp:
                                            attr_DIC_string = self.object_label + "_overide_rampMismatch*" + obj + "." + attr + "**" + rl + "_"
                                            self.attr_overrides_DIC[attr_DIC_string] = override_ramp
                                        if override_ramp == default_ramp:
                                            render_layer_overrides = cmds.listConnections(rl + ".adjustments", p = True, c = True) or []
                                            render_layer_ramp_overrides = []
                                            for cn in render_layer_overrides:
                                                t = cmds.nodeType(cn)
                                                if t == "ramp":
                                                    if cn not in render_layer_ramp_overrides:
                                                        render_layer_ramp_overrides.append(cn)
                                                for i in range(0, len(render_layer_overrides), 2):
                                                    rl_connection = render_layer_overrides[i]
                                                    override_Attr = render_layer_overrides[i+1]
                                                    override_index = rl_connection.split("]")[0]
                                                    override_index = override_index.split("[")[-1]
                                                    override_value = cmds.getAttr(rl + ".adjustments[%s].value" %override_index)
                                                    attr_DIC_string =  self.object_label + "_" + attr + "_rampOveride" + "*" + override_Attr + "**" + rl
                                                    if attr_DIC_string not in self.attr_overrides_DIC and override_ramp in override_Attr:
                                                        self.attr_overrides_DIC[attr_DIC_string] = override_value
                        it = it + 1
            return(self.attr_overrides_DIC)


    def translations(object_check, render_layers):
        transform_default_values_DIC = {}
        object_in_layers = []
        transform_layer_overrides = []
        transform_override_values_DIC = {}
        transform_layer_DIC = {}
        cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
        lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
        for ob in object_check_t:
            string_translateX = ob + ".translateX"
            translateX = cmds.getAttr(string_translateX)
            var = ob + "$" + lay + "$translateX"
            transform_default_values_DIC[var] = translateX
            string_translateY = ob + ".translateY"
            translateY = cmds.getAttr(string_translateY)
            var = ob + "$" + lay + "$translateY"
            transform_default_values_DIC[var] = translateY
            string_translateZ = ob + ".translateZ"
            translateZ = cmds.getAttr(string_translateZ)
            var = ob + "$" + lay + "$translateZ"
            transform_default_values_DIC[var] = translateZ
            strrotateX = ob + ".rotateX"
            rotateX = cmds.getAttr(strrotateX)
            var = ob + "$" + lay + "$rotateX"
            transform_default_values_DIC[var] = rotateX
            string_rotateY = ob + ".rotateY"
            rotateY = cmds.getAttr(string_rotateY)
            var = ob + "$" + lay + "$rotateY"
            transform_default_values_DIC[var] = rotateY
            string_rotateZ = ob + ".rotateZ"
            rotateZ = cmds.getAttr(string_rotateZ)
            var = ob + "$" + lay + "$rotateZ"
            transform_default_values_DIC[var] = rotateZ
            string_scaleX = ob + ".scaleX"
            scaleX = cmds.getAttr(string_scaleX)
            var = ob + "$" + lay + "$scaleX"
            transform_default_values_DIC[var] = scaleX
            string_scaleY = ob + ".scaleY"
            scaleY = cmds.getAttr(string_scaleY)
            var = ob + "$" + lay + "$scaleY"
            transform_default_values_DIC[var] = scaleY
            string_scaleZ = ob + ".scaleZ"
            scaleZ = cmds.getAttr(string_scaleZ)
            var = ob + "$" + lay + "$scaleZ"
            transform_default_values_DIC[var] = scaleZ
        for ob in object_check_t:
            for lay in render_layers:
                cmds.editRenderLayerGlobals( currentRenderLayer = lay )
                lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
                if "defaultRenderLayer" != lay:
                    string_translateX = ob + ".translateX"
                    translateX = cmds.getAttr(string_translateX)
                    var = ob + "$" + lay + "$translateX"
                    transform_override_values_DIC[var] = translateX
                    string_translateY = ob + ".translateY"
                    translateY = cmds.getAttr(string_translateY)
                    var = ob + "$" + lay + "$translateY"
                    transform_override_values_DIC[var] = translateY
                    string_translateZ = ob + ".translateZ"
                    translateZ = cmds.getAttr(string_translateZ)
                    var = ob + "$" + lay + "$translateZ"
                    transform_override_values_DIC[var] = translateZ
                    strrotateX = ob + ".rotateX"
                    rotateX = cmds.getAttr(strrotateX)
                    var = ob + "$" + lay + "$rotateX"
                    transform_override_values_DIC[var] = rotateX
                    string_rotateY = ob + ".rotateY"
                    rotateY = cmds.getAttr(string_rotateY)
                    var = ob + "$" + lay + "$rotateY"
                    transform_override_values_DIC[var] = rotateY
                    string_rotateZ = ob + ".rotateZ"
                    rotateZ = cmds.getAttr(string_rotateZ)
                    var = ob + "$" + lay + "$rotateZ"
                    transform_override_values_DIC[var] = rotateZ
                    string_scaleX = ob + ".scaleX"
                    scaleX = cmds.getAttr(string_scaleX)
                    var = ob + "$" + lay + "$scaleX"
                    transform_override_values_DIC[var] = scaleX
                    string_scaleY = ob + ".scaleY"
                    scaleY = cmds.getAttr(string_scaleY)
                    var = ob + "$" + lay + "$scaleY"
                    transform_override_values_DIC[var] = scaleY
                    string_scaleZ = ob + ".scaleZ"
                    scaleZ = cmds.getAttr(string_scaleZ)
                    var = ob + "$" + lay + "$scaleZ"
                    transform_override_values_DIC[var] = scaleZ
        for transform_value in transform_override_values_DIC:
            transform_values_split = transform_value.split("$")
            for transform_defualt_value in transform_default_values_DIC:
                transform_defualt_value_split = transform_defualt_value.split("$")
                if transform_values_split[0] == transform_defualt_value_split[0] and transform_values_split[2] == transform_defualt_value_split[2]:
                    valu = transform_override_values_DIC[transform_value]
                    valuDef = transform_default_values_DIC[transform_defualt_value]
                    if valu != valuDef:
                        transform_layer_overrides.append(transform_value)
                        transform_layer_DIC["transO$" + transform_value] = valu
        return transform_default_values_DIC,transform_override_values_DIC,transform_layer_overrides,object_check,render_layers,transform_layer_DIC

    def material_assignments(object_check, render_layers):
        materials_list = []
        materials_list_overrides = []
        material_layer_overrides = []
        materials_defualt_DIC = {}
        materials_override_DIC = {}
        materials_layer_DIC = {}
        for ob in object_check:
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
            for L in render_layers:
                cmds.editRenderLayerGlobals( currentRenderLayer = L )
                if L == "defaultRenderLayer":
                    cmds.select(clear = True)
                    cmds.select(ob)
                    cmds.hyperShade(smn = True)
                    materials_list = cmds.ls(sl = True)
                    for MM in materials_list:
                        NT = cmds.nodeType(MM)
                        if NT != "renderLayer":
                            if MM not in materials_list_overrides:
                                materials_list_overrides.append(MM)
                            override_DIC_key = ob + "$" + L + "$"
                            materials_defualt_DIC[override_DIC_key] = MM
                else:
                    cmds.select(clear = True)
                    cmds.select(ob)
                    cmds.hyperShade(smn = True)
                    materials_list = cmds.ls(sl = True)
                    for MM in materials_list:
                        NT = cmds.nodeType(MM)
                        if NT != "renderLayer":
                            if MM not in materials_list_overrides:
                                materials_list_overrides.append(MM)
                            override_DIC_key = ob + "$" + L + "$"
                            materials_override_DIC[override_DIC_key] = MM
        for material_override_DIC in materials_override_DIC:
           material_value_split = material_override_DIC.split("$")
           for material_defualt_DIC in materials_defualt_DIC:
               material_defualt_value_split = material_defualt_DIC.split("$")
               if material_value_split[0] == material_defualt_value_split[0]:
                    mat_oth = materials_override_DIC[material_override_DIC]
                    mat_def = materials_defualt_DIC[material_defualt_DIC]
                    if mat_oth != mat_def:
                        material_layer_overrides.append(material_override_DIC)
                        material_DIC_string = material_override_DIC + ".materialAssignment"
                        if material_DIC_string not in materials_layer_DIC and "Shape" not in material_DIC_string:
                            materials_layer_DIC[material_DIC_string] = mat_oth
        return(materials_list_overrides,materials_list_overrides,materials_override_DIC,material_layer_overrides,materials_layer_DIC)

    def material_overrides(object_check,render_layers):
        materialsOverideDIC = {}
        attr_overrides_DIC = materialsOverideDIC
        object_label = "mtlOveride"

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
        attrCheck = ["color","diffuseColorAmount","opacityMap","roughnessAmount","illumColor","illumGI","compensateExposure","brdfType","reflectionColor","reflectionColorAmount","hilightGlossinessLock",
        "hilightGlossiness","reflectionGlossiness","useFresnel","glossyFresnel","lockFresnelIORToRefractionIOR","refractionColor","refractionColorAmount","refractionGlossiness","refractionIOR",
        "fogColor","fogMult","fogBias","affectShadows","sssOn","translucencyColor","scatterSubdivs","scatterDir","scatterLevels","scatterCoeff","thickness","sssEnvironment","traceRefractions",
        "refractionExitColorOn","refractionsMaxDepth","affectAlpha","refrDispersionOn","refrDispersionAbbe","bumpMapType","bumpMap","bumpMult","bumpShadows","bumpDeltaScale","cutoffThreshold",
        "doubleSided","useIrradianceMap","fixDarkEdges","caching","nodeState","reflMapMinRate","reflMapMaxRate","reflMapColorThreshold","reflMapNormalThreshold","reflMapSamples"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "blinn"
        remove_attr_List = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "eccentricity", "specularRollOff", "reflectionRolloff"]
        attrCheck = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","eccentricity","specularRollOff","specularColor","reflectivity","reflectedColor"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "phong"
        remove_attr_List = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "cosinePower"]
        attrCheck = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","cosinePower","specularColor","reflectivity","reflectedColor"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "lambert"
        remove_attr_List = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB"]
        attrCheck = ["color","transparency","ambientColor","incandescence","diffuse","translucence","translucenceDepth","translucenceFocus"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "surfaceShader"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outMatteOpacity","outMatteOpacityR","outMatteOpacityG","outMatteOpacityB","outGlowColor","outGlowColorR","outGlowColorG","outGlowColorB","materialAlphaGain"]
        attrCheck = ["outColor","outTransparency","outGlowColor","outMatteOpacity"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "place2dTexture"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","uvCoord","uCoord","vCoord","vertexUvOne","vertexUvOneU","vertexUvOneV","vertexUvTwo","vertexUvTwoU","vertexUvTwoV","vertexUvThree","vertexUvThreeU","vertexUvThreeV","vertexCameraOne","vertexCameraOneX","vertexCameraOneY","vertexCameraOneZ","uvFilterSize","uvFilterSizeX","uvFilterSizeY","coverage","coverageU","coverageV","translateFrame","translateFrameU","translateFrameV","rotateFrame","mirrorU","mirrorV","stagger","wrapU","wrapV","repeatUV","repeatU","repeatV","offset","offsetU","offsetV","rotateUV","noiseUV","noiseU","noiseV","fast","outUV","outU","outV","outUvFilterSize","outUvFilterSizeX","outUvFilterSizeY","doTransform"]
        attrCheck = ["coverageU","coverageV","translateFrameU","translateFrameV","rotateFrame","mirrorU","mirrorV","wrapU","wrapV","stagger","repeatU","repeatV","offsetU","offsetV","rotateUV","noiseU","noiseV","fast"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "file"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","filter","filterOffset","invert","alphaIsLuminance","colorGain","colorGainR","colorGainG","colorGainB","colorOffset","colorOffsetR","colorOffsetG","colorOffsetB","alphaGain","alphaOffset","defaultColor","defaultColorR","defaultColorG","defaultColorB","outColor","outColorR","outColorG","outColorB","outAlpha","fileTextureName","fileTextureNamePattern","computedFileTextureNamePattern","disableFileLoad","useFrameExtension","frameExtension","frameOffset","useHardwareTextureCycling","startCycleExtension","endCycleExtension","byCycleIncrement","forceSwatchGen","filterType","filterWidth","preFilter","preFilterRadius","useCache","useMaximumRes","uvTilingMode","explicitUvTiles","explicitUvTiles.explicitUvTileName","explicitUvTiles.explicitUvTilePosition","explicitUvTiles.explicitUvTilePositionU","explicitUvTiles.explicitUvTilePositionV","baseExplicitUvTilePosition","baseExplicitUvTilePositionU","baseExplicitUvTilePositionV","uvTileProxyDirty","uvTileProxyGenerate","uvTileProxyQuality","coverage","coverageU","coverageV","translateFrame","translateFrameU","translateFrameV","rotateFrame","doTransform","mirrorU","mirrorV","stagger","wrapU","wrapV","repeatUV","repeatU","repeatV","offset","offsetU","offsetV","rotateUV","noiseUV","noiseU","noiseV","blurPixelation","vertexCameraOne","vertexCameraOneX","vertexCameraOneY","vertexCameraOneZ","vertexCameraTwo","vertexCameraTwoX","vertexCameraTwoY","vertexCameraTwoZ","vertexCameraThree","vertexCameraThreeX","vertexCameraThreeY","vertexCameraThreeZ","vertexUvOne","vertexUvOneU","vertexUvOneV","vertexUvTwo","vertexUvTwoU","vertexUvTwoV","vertexUvThree","vertexUvThreeU","vertexUvThreeV","objectType","rayDepth","primitiveId","pixelCenter","pixelCenterX","pixelCenterY","exposure","hdrMapping","hdrExposure","dirtyPixelRegion","ptexFilterType","ptexFilterWidth","ptexFilterBlur","ptexFilterSharpness","ptexFilterInterpolateLevels","colorProfile","colorSpace","ignoreColorSpaceFileRules","workingSpace","colorManagementEnabled","colorManagementConfigFileEnabled","colorManagementConfigFilePath","outSize","outSizeX","outSizeY","fileHasAlpha","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","infoBits"]
        attrCheck = ["exposure","defaultColor","colorGain","colorOffset","alphaGain","alphaOffset","alphaIsLuminance","invert"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "layered_textures"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","inputs","inputs.color","inputs.colorR","inputs.colorG","inputs.colorB","inputs.alpha","inputs.blendMode","inputs.isVisible","outColor","outColorR","outColorG","outColorB","outAlpha","hardwareColor","hardwareColorR","hardwareColorG","hardwareColorB","alphaIsLuminance","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB"]
        attrCheck = ["alphaIsLuminance","inputs.isVisible","inputs.alpha","inputs.color","inputs.blendMode"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "VRayBlendMtl"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","swatchAutoUpdate","swatchAlwaysRender","swatchExplicitUpdate","swatchMaxRes","base_material","base_materialR","base_materialG","base_materialB","color","colorR","colorG","colorB","viewportColor","viewportColorR","viewportColorG","viewportColorB","coat_material_0","coat_material_0R","coat_material_0G","coat_material_0B","blend_amount_0","blend_amount_0R","blend_amount_0G","blend_amount_0B","coat_material_1","coat_material_1R","coat_material_1G","coat_material_1B","blend_amount_1","blend_amount_1R","blend_amount_1G","blend_amount_1B","coat_material_2","coat_material_2R","coat_material_2G","coat_material_2B","blend_amount_2","blend_amount_2R","blend_amount_2G","blend_amount_2B","coat_material_3","coat_material_3R","coat_material_3G","coat_material_3B","blend_amount_3","blend_amount_3R","blend_amount_3G","blend_amount_3B","coat_material_4","coat_material_4R","coat_material_4G","coat_material_4B","blend_amount_4","blend_amount_4R","blend_amount_4G","blend_amount_4B","coat_material_5","coat_material_5R","coat_material_5G","coat_material_5B","blend_amount_5","blend_amount_5R","blend_amount_5G","blend_amount_5B","coat_material_6","coat_material_6R","coat_material_6G","coat_material_6B","blend_amount_6","blend_amount_6R","blend_amount_6G","blend_amount_6B","coat_material_7","coat_material_7R","coat_material_7G","coat_material_7B","blend_amount_7","blend_amount_7R","blend_amount_7G","blend_amount_7B","coat_material_8","coat_material_8R","coat_material_8G","coat_material_8B","blend_amount_8","blend_amount_8R","blend_amount_8G","blend_amount_8B","additive_mode","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outApiType","outApiClassification"]
        attrCheck = ["base_material","additive_mode","coat_material_0","blend_amount_0","coat_material_1","blend_amount_1","coat_material_2","blend_amount_2","coat_material_3","blend_amount_3","coat_material_4","blend_amount_4","coat_material_5","blend_amount_5","coat_material_6","blend_amount_6","coat_material_7","blend_amount_7","coat_material_8","blend_amount_8"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "displacementShader"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","displacementMode","displacement","vectorDisplacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","yIsUp","tangent","tangentX","tangentY","tangentZ"]
        attrCheck = ["displacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","tangentX","tangentY","tangentZ","nodeState","caching","displacementMode"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        object_type = "VRayDisplacement"
        remove_attr_List = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","dagSetMembers","dnSetMembers","memberWireframeColor","annotation","isLayer","verticesOnlySet","edgesOnlySet","facetsOnlySet","editPointsOnlySet","renderableOnlySet","partition","groupNodes","usedBy","displacement","overrideGlobalDisplacement","outApiType","outApiClassification","vraySeparator_vray_displacement","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementType","vrayDisplacementAmount","vrayDisplacementShift","vrayDisplacementKeepContinuity","vrayEnableWaterLevel","vrayWaterLevel","vrayDisplacementCacheNormals","vray2dDisplacementResolution","vray2dDisplacementPrecision","vray2dDisplacementTightBounds","vray2dDisplacementMultiTile","vray2dDisplacementFilterTexture","vray2dDisplacementFilterBlur","vrayDisplacementUseBounds","vrayDisplacementMinValue","vrayDisplacementMinValueR","vrayDisplacementMinValueG","vrayDisplacementMinValueB","vrayDisplacementMaxValue","vrayDisplacementMaxValueR","vrayDisplacementMaxValueG","vrayDisplacementMaxValueB","vraySeparator_vray_subquality","vrayOverrideGlobalSubQual","vrayViewDep","vrayEdgeLength","vrayMaxSubdivs"]
        attrCheck = ["overrideGlobalDisplacement","displacement","caching","nodeState","blackBox","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementType","vrayDisplacementAmount","vrayDisplacementShift","vrayEdgeLength","vrayMaxSubdivs","vrayDisplacementUseBounds"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        matOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        materialsOverideDIC = matOverides.attr_override_detect()

        return(materialsOverideDIC)

    def cameraOverides(object_check,render_layers):
        cameraOveridesDIC = {}
        attr_overrides_DIC = cameraOveridesDIC
        object_label = "camera_overide"
        object_type = "camera"
        remove_attr_List =  ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "hyperLayout", "isCollapsed", "blackBox", "borderConnections", "isHierarchicalConnection", "publishedNodeInfo", "publishedNodeInfo.publishedNode", "publishedNodeInfo.isHierarchicalNode", "publishedNodeInfo.publishedNodeType", "rmbCommand", "templateName", "templatePath", "viewName", "iconName", "viewMode", "templateVersion", "uiTreatment", "customTreatment", "creator", "creationDate", "containerType", "boundingBox", "boundingBoxMin", "boundingBoxMinX", "boundingBoxMinY", "boundingBoxMinZ", "boundingBoxMax", "boundingBoxMaxX", "boundingBoxMaxY", "boundingBoxMaxZ", "boundingBoxSize", "boundingBoxSizeX", "boundingBoxSizeY", "boundingBoxSizeZ", "center", "boundingBoxCenterX", "boundingBoxCenterY", "boundingBoxCenterZ", "matrix", "inverseMatrix", "worldMatrix", "worldInverseMatrix", "parentMatrix", "parentInverseMatrix", "visibility", "intermediateObject", "template", "ghosting", "instObjGroups", "instObjGroups.objectGroups", "instObjGroups.objectGroups.objectGrpCompList", "instObjGroups.objectGroups.objectGroupId", "instObjGroups.objectGroups.objectGrpColor", "objectColorRGB", "objectColorR", "objectColorG", "objectColorB", "useObjectColor", "objectColor", "drawOverride", "overrideDisplayType", "overrideLevelOfDetail", "overrideShading", "overrideTexturing", "overridePlayback", "overrideEnabled", "overrideVisibility", "overrideColor", "lodVisibility", "selectionChildHighlighting", "renderInfo", "identification", "layerRenderable", "layerOverrideColor", "renderLayerInfo", "renderLayerInfo.renderLayerId", "renderLayerInfo.renderLayerRenderable", "renderLayerInfo.renderLayerColor", "ghostingControl", "ghostCustomSteps", "ghostPreSteps", "ghostPostSteps", "ghostStepSize", "ghostFrames", "ghostColorPreA", "ghostColorPre", "ghostColorPreR", "ghostColorPreG", "ghostColorPreB", "ghostColorPostA", "ghostColorPost", "ghostColorPostR", "ghostColorPostG", "ghostColorPostB", "ghostRangeStart", "ghostRangeEnd", "ghostDriver", "hiddenInOutliner", "renderable", "cameraAperture", "horizontalFilmAperture", "verticalFilmAperture", "shakeOverscan", "shakeOverscanEnabled", "filmOffset", "horizontalFilmOffset", "verticalFilmOffset", "shakeEnabled", "shake", "horizontalShake", "verticalShake", "stereoHorizontalImageTranslateEnabled", "stereoHorizontalImageTranslate", "postProjection", "preScale", "filmTranslate", "filmTranslateH", "filmTranslateV", "filmRollControl", "filmRollPivot", "horizontalRollPivot", "verticalRollPivot", "filmRollValue", "filmRollOrder", "postScale", "filmFit", "filmFitOffset", "overscan", "panZoomEnabled", "renderPanZoom", "pan", "horizontalPan", "verticalPan", "zoom", "focalLength", "lensSqueezeRatio", "cameraScale", "triggerUpdate", "nearClipPlane", "farClipPlane", "fStop", "focusDistance", "shutterAngle", "centerOfInterest", "orthographicWidth", "imageName", "depthName", "maskName", "tumblePivot", "tumblePivotX", "tumblePivotY", "tumblePivotZ", "usePivotAsLocalSpace", "imagePlane", "homeCommand", "bookmarks", "locatorScale", "displayGateMaskOpacity", "displayGateMask", "displayFilmGate", "displayResolution", "displaySafeAction", "displaySafeTitle", "displayFieldChart", "displayFilmPivot", "displayFilmOrigin", "clippingPlanes", "bestFitClippingPlanes", "depthOfField", "motionBlur", "orthographic", "journalCommand", "image", "depth", "transparencyBasedDepth", "threshold", "depthType", "useExploreDepthFormat", "mask", "displayGateMaskColor", "displayGateMaskColorR", "displayGateMaskColorG", "displayGateMaskColorB", "backgroundColor", "backgroundColorR", "backgroundColorG", "backgroundColorB", "focusRegionScale", "displayCameraNearClip", "displayCameraFarClip", "displayCameraFrustum", "cameraPrecompTemplate", "vraySeparator_vray_cameraPhysical", "vrayCameraPhysicalOn", "vrayCameraPhysicalType", "vrayCameraPhysicalFilmWidth", "vrayCameraPhysicalFocalLength", "vrayCameraPhysicalSpecifyFOV", "vrayCameraPhysicalFOV", "vrayCameraPhysicalZoomFactor", "vrayCameraPhysicalDistortionType", "vrayCameraPhysicalDistortion", "vrayCameraPhysicalLensFile", "vrayCameraPhysicalDistortionMap", "vrayCameraPhysicalDistortionMapR", "vrayCameraPhysicalDistortionMapG", "vrayCameraPhysicalDistortionMapB", "vrayCameraPhysicalFNumber", "vrayCameraPhysicalHorizLensShift", "vrayCameraPhysicalLensShift", "vrayCameraPhysicalLensAutoVShift", "vrayCameraPhysicalShutterSpeed", "vrayCameraPhysicalShutterAngle", "vrayCameraPhysicalShutterOffset", "vrayCameraPhysicalLatency", "vrayCameraPhysicalISO", "vrayCameraPhysicalSpecifyFocus", "vrayCameraPhysicalFocusDistance", "vrayCameraPhysicalExposure", "vrayCameraPhysicalWhiteBalance", "vrayCameraPhysicalWhiteBalanceR", "vrayCameraPhysicalWhiteBalanceG", "vrayCameraPhysicalWhiteBalanceB", "vrayCameraPhysicalVignetting", "vrayCameraPhysicalVignettingAmount", "vrayCameraPhysicalBladesEnable", "vrayCameraPhysicalBladesNum", "vrayCameraPhysicalBladesRotation", "vrayCameraPhysicalCenterBias", "vrayCameraPhysicalAnisotropy", "vrayCameraPhysicalUseDof", "vrayCameraPhysicalUseMoBlur", "vrayCameraPhysicalApertureMap", "vrayCameraPhysicalApertureMapR", "vrayCameraPhysicalApertureMapG", "vrayCameraPhysicalApertureMapB", "vrayCameraPhysicalApertureMapAffectsExposure", "vrayCameraPhysicalOpticalVignetting", "vraySeparator_vray_cameraOverrides", "vrayCameraOverridesOn", "vrayCameraType", "vrayCameraOverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve",]
        attrCheck = ["vraySeparator_vray_cameraPhysical","vrayCameraPhysicalOn","vrayCameraPhysicalType","vrayCameraPhysicalFilmWidth","vrayCameraPhysicalFocalLength","vrayCameraPhysicalSpecifyFOV","vrayCameraPhysicalFOV","vrayCameraPhysicalZoomFactor","vrayCameraPhysicalDistortionType","vrayCameraPhysicalDistortion","vrayCameraPhysicalLensFile","vrayCameraPhysicalDistortionMap","vrayCameraPhysicalDistortionMapR",
        "vrayCameraPhysicalDistortionMapG","vrayCameraPhysicalDistortionMapB","vrayCameraPhysicalFNumber","vrayCameraPhysicalHorizLensShift","vrayCameraPhysicalLensShift","vrayCameraPhysicalLensAutoVShift","vrayCameraPhysicalShutterSpeed","vrayCameraPhysicalShutterAngle","vrayCameraPhysicalShutterOffset","vrayCameraPhysicalLatency","vrayCameraPhysicalISO","vrayCameraPhysicalSpecifyFocus","vrayCameraPhysicalFocusDistance",
        "vrayCameraPhysicalExposure","vrayCameraPhysicalWhiteBalance","vrayCameraPhysicalWhiteBalanceR","vrayCameraPhysicalWhiteBalanceG","vrayCameraPhysicalWhiteBalanceB","vrayCameraPhysicalVignetting","vrayCameraPhysicalVignettingAmount","vrayCameraPhysicalBladesEnable","vrayCameraPhysicalBladesNum","vrayCameraPhysicalBladesRotation","vrayCameraPhysicalCenterBias","vrayCameraPhysicalAnisotropy","vrayCameraPhysicalUseDof","vrayCameraPhysicalUseMoBlur"
        ,"vrayCameraPhysicalApertureMap","vrayCameraPhysicalApertureMapR","vrayCameraPhysicalApertureMapG","vrayCameraPhysicalApertureMapB","vrayCameraPhysicalApertureMapAffectsExposure","vrayCameraPhysicalOpticalVignetting","vraySeparator_vray_cameraOverrides","vrayCameraOverridesOn","vrayCameraType", "vrayCameraOverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve","renderable"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        cameraOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        cameraOveridesDIC = cameraOverides.attr_override_detect()

        return(cameraOveridesDIC)

    def lightOverides(object_check,render_layers):
        lightOveridesDIC = {}
        attr_overrides_DIC = lightOveridesDIC
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
        attrCheck = ["lightColor","intensityMult","shapeType","uSize","vSize","directional","useRectTex","rectTex","noDecay","doubleSided","invisible","skylightPortal","simpleSkylightPortal","affectDiffuse","affectSpecular","affectReflections","shadows","shadowColor","shadowBias","visibility","colorR","colorG","colorB","emitDiffuse","emitSpecular",
        "decayRate","attributeAliasList","diffuseContrib","specularContrib","enabled"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        lightOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        lightOveridesDIC = lightOverides.attr_override_detect()

        object_type = "spotLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","coneAngle","penumbraAngle","dropoff","barnDoors","leftBarnDoor","rightBarnDoor","topBarnDoor","bottomBarnDoor","useDecayRegions","startDistance1","endDistance1","startDistance2","endDistance2","startDistance3","endDistance3","fogSpread","fogIntensity","objectType","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","rayDirection","rayDirectionX","rayDirectionY","rayDirectionZ","fogGeometry","lightGlow","psIllumSamples"]
        attrCheck = ["color","intensity","emitDiffuse","emitSpecular","decayRate","coneAngle","penumbraAngle","dropoff","shadowColor","useRayTraceShadows","lightRadius","shadowRays","rayDepthLimit","useDepthMapShadows","dmapResolution","useMidDistDmap","useDmapAutoFocus","dmapFocus","dmapFilterSize","dmapBias","fogShadowIntensity","volumeShadowSamples"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        lightOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        lightOveridesDIC = lightOverides.attr_override_detect()

        object_type = "ambientLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","ambientShade","objectType","shadowRadius","castSoftShadows","normalCamera","normalCameraX","normalCameraY","normalCameraZ","receiveShadows"]
        attrCheck = ["color","intensity","ambientShade"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        lightOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        lightOveridesDIC = lightOverides.attr_override_detect()

        object_type = "directionalLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","useLightPosition","objectType","lightAngle","pointWorld","pointWorldX","pointWorldY","pointWorldZ"]
        attrCheck = ["color","intensity","emitDiffuse","emitSpecular"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        lightOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        lightOveridesDIC = lightOverides.attr_override_detect()

        object_type = "pointLight"
        remove_attr_List = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","fogGeometry","fogRadius","lightGlow","objectType","fogType","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","fogIntensity"]
        attrCheck = ["color","intensity","emitDiffuse","emitSpecular","decayRate"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        lightOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        lightOveridesDIC = lightOverides.attr_override_detect()

        return(lightOveridesDIC)

    def vraySettingsOverides(object_check,render_layers):
        vraySettingsOverrideDic = {}
        attr_overrides_DIC = vraySettingsOverrideDic
        object_label = "vs"
        cmds.loadPlugin('vrayformaya', quiet=True)
        cmds.pluginInfo('vrayformaya', edit=True, autoload=True)
        cmds.setAttr("defaultRenderGlobals.ren", "vray", type = "string")

        object_type = "VRaySettingsNode"
        remove_attr_List =  cmds.listAttr("vraySettings")
        attrCheck = ["cam_envtexBg","cam_envtexGi","cam_envtexReflect","cam_envtexRefract","cam_envtexSecondaryMatte","globopt_geom_displacement","globopt_light_doLights","globopt_light_doHiddenLights","globopt_light_doDefaultLights",
        "globopt_light_doShadows","globopt_light_ignoreLightLinking","globopt_light_disableSelfIllumination","photometricScale","globopt_mtl_reflectionRefraction","globopt_mtl_glossy","globopt_mtl_transpMaxLevels","globopt_mtl_transpCutoff"
        ,"globopt_mtl_doMaps","globopt_mtl_filterMaps","bumpMultiplier","texFilterScaleMultiplier","globopt_ray_bias","globopt_ray_maxIntens_on","gi_texFilteringMultiplier","cam_overrideEnvtex","cam_overrideEnvtexSecondaryMatte",
        "ddisplac_amount","ddisplac_edgeLength","ddisplac_maxSubdivs","giOn","reflectiveCaustics","refractiveCaustics","secondaryMultiplier","secondaryEngine","saturation","contrast","contrastBase","aoOn","aoAmount","aoRadius","aoSubdivs",
        "giRayDistOn","giRayDist","causticsOn","causticsMultiplier","causticsSearchDistance","causticsMaxPhotons","causticsMaxDensity","minShadeRate"]
        for attr in attrCheck:
            remove_attr_List.remove(attr)
        vraySettingsOverides = ATTR_OVERRIDES_CLASS(render_layers,object_type,remove_attr_List,attr_overrides_DIC,object_label,object_check)
        vraySettingsOverrideDic = vraySettingsOverides.attr_override_detect()

        return(vraySettingsOverrideDic)

    def objsInRenderLayer(object_check,renderLayer):
        obsInLayerDic = {}
        for rl in render_layers:
            obsInLayer = cmds.editRenderLayerMembers(rl, query = True) or []
            for obj in object_check:
                for obs in obsInLayer:
                    if obj == obs:
                        obsIlaySTRING = obj + "_" + rl
                        obsInLayerDic[obsIlaySTRING] = rl

        return(obsInLayerDic)

    def Render_stat_Overides(object_check_g, render_layers):
        RenderStatOverrideDic = {}
        excludeList = ["camera","ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight","VRayLightSphereShape","VRayLightRectShape","VRayLightDomeShape","VRayLightIESShape"]
        siz = len(object_check_g)
        l = 0
        while l < siz:
            for object in object_check_g:
                objectT = cmds.objectType(object)
                for excld in excludeList:
                    if excld == objectT:
                        object_check_g.remove(object)
            l = l + 1
        for object in object_check_g:
            object_type = cmds.objectType(object)
            if object_type != "locator":
                Render_Stat_List = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions","doubleSided"]
                for rsl in Render_Stat_List:
                    attr_string = object + "." + rsl
                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                    defValue = cmds.getAttr(attr_string)
                    for rl in render_layers:
                        if rl != "defaultRenderLayer":
                            cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                            layValue = cmds.getAttr(attr_string)
                            if layValue != defValue:
                                dicString = object + "**" + "renderStats" + "**" +  rsl + "**" + rl
                                RenderStatOverrideDic[dicString] = layValue
            return(RenderStatOverrideDic)

    def vrayObjectPropO(render_layers):
        VrayObjectProps = cmds.ls(type = "VRayObjectProperties")
        vrayObjectPropertyOvrideDIC = {}
        Object_Props = ["overrideMBSamples","mbSamples","objectIDEnabled","objectID","skipExportEnabled","skipExport","ignore",
        "useIrradianceMap","generateGI","generateGIMultiplier","receiveGI","receiveGIMultiplier","giSubdivsMultiplier","giSubdivsMultiplier","generateCaustics",
        "receiveCaustics","causticsMultiplier","giVisibility","primaryVisibility","reflectionVisibility","refractionVisibility","shadowVisibility","receiveShadows","matteSurface",
        "alphaContribution","generateRenderElements","shadows","affectAlpha","shadowTintColor","shadowBrightness","reflectionAmount","refractionAmount","giAmount","noGIOnOtherMattes",
        "matteForSecondaryRays","giSurfaceID","useReflectionExclude","reflectionListIsInclusive","useRefractionExclude","refractionListIsInclusive","blackBox",
        "rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType"]
        for vop in VrayObjectProps:
            for op in Object_Props:
                cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
                valString = vop + "." + op
                defVal = cmds.getAttr(valString)
                for rl in render_layers:
                    if rl != "defaultRenderLayer":
                        cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                        oVal = cmds.getAttr(valString)
                        if oVal != defVal:
                            dicString = vop + "**" + "vrayObjProp" + "**" + op + "**" + rl
                            vrayObjectPropertyOvrideDIC[dicString] = oVal
        return(vrayObjectPropertyOvrideDIC)

    vraySettingsOverrideDic = {}
    transform_layer_overrides = {}
    matAssignmentLayOveridesmatAssignmentLayOverides = {}
    materialsOverideDIC = {}
    cameraOveridesDIC = {}
    lightOveridesDIC = {}
    Render_Stats_Overides = {}
    vrayObjectPropertyOverides = {}

    VScount = 1
    Tcount = 1
    Mcount = 1
    Ccount = 1
    Lcount = 1
    Rcount = 1
    VPcount = 1

    if VScount == 1:
        vraySettingsOverrideDic = vraySettingsOverides(object_check,render_layers)
    if Tcount == 1:
        OBJ_1_translations = translations(object_check, render_layers)
        transform_layer_overrides = OBJ_1_translations[5]
    if Mcount == 1:
        OBJ_1_materialsAssignments = material_assignments(object_check, render_layers)
        matAssignmentLayOverides = OBJ_1_materialsAssignments[4]

        materialsOverideDIC = material_overrides(object_check,render_layers)
        materialsOverideDIC.update(matAssignmentLayOverides)
    if Ccount == 1:
        cameraOveridesDIC = cameraOverides(object_check,render_layers)
    if Lcount == 1:
        lightOveridesDIC = lightOverides(object_check,render_layers)
    if Rcount == 1:
        OBJ_1_Render_Stats = Render_stat_Overides(object_check_g, render_layers)
        Render_Stats_Overides = OBJ_1_Render_Stats
    if VPcount == 1:
        OBJ_1_VrayObjectProps = vrayObjectPropO(render_layers)
        vrayObjectPropertyOverides = OBJ_1_VrayObjectProps

    return(vraySettingsOverrideDic,transform_layer_overrides,materialsOverideDIC,lightOveridesDIC,Render_Stats_Overides,vrayObjectPropertyOverides,cameraOveridesDIC)


#--- overide section over ----

def activeBut(rl,check,buttSize_Add_Obj,butts,ButtSizeAdj,butts_addOBJ,buttSize_Add_Obj_adj,butts_delOBJ,buttSize_del_OBJ,buttSize_del_Obj_adj,butts_addOBJ_ALL,butts_delOBJ_ALL,*args):
    global initialLayer
    initialLayer = rl

    cmds.editRenderLayerGlobals(currentRenderLayer = initialLayer)
    pressed = butts[ButtSizeAdj]
    pressed_action = "defaultRenderLayer"

    if rl != "defaultRenderLayer":
        pressed_addObbj = butts_addOBJ[buttSize_Add_Obj_adj]
        pressed_delOBJ = butts_delOBJ[buttSize_del_Obj_adj]

    for bu in butts:
        if bu == pressed:
            cmds.button(bu,bgc = (.5,.8,1), edit = True)
        else:
            cmds.button(bu,bgc = (.25,.25,.25), edit = True)

    for but in butts_addOBJ:
        if pressed_action != rl:
            cmds.button(but,bgc = (.4,.4,.4),label = " add selection",edit = True)
        else:
            cmds.button(but,bgc = (.2,.2,.2), label = "object in layer",edit = True)

    for but in butts_addOBJ_ALL:
        if pressed_action != rl:
            cmds.button(but,bgc = (.4,.4,.4),label = " add selection -all layers",edit = True)
        else:
            cmds.button(but,bgc = (.2,.2,.2), label = "object in layer",edit = True)

    for but in butts_delOBJ:
        if pressed_action != rl:
            cmds.button(but,bgc = (.4,.4,.4),label = " remove selection",edit = True)
        else:
            cmds.button(but,bgc = (.2,.2,.2),label = "can not remove",edit = True)

    for but in butts_delOBJ_ALL:
        if pressed_action != rl:
            cmds.button(but,bgc = (.4,.4,.4),label = "remove selection -all layers",edit = True)
        else:
            cmds.button(but,bgc = (.2,.2,.2),label = "can not remove",edit = True)


def OBpress(O_but,render_layers,txtFieldList,vraySetBut,transformObut,materialsObut,cameraObut,lightObut,renderStatsObut,vrayObjectPropertiesObut,*args):

    overidesDic = overides_information_function(render_layers,vraySetBut,transformObut,materialsObut,cameraObut,lightObut,renderStatsObut,vrayObjectPropertiesObut)
    vraySettingOVeride = overidesDic[0] or []
    transformsOVeride = overidesDic[1] or []
    materialsOVeride = overidesDic[2] or []
    lightsOVeride = overidesDic[3] or []
    renderStatsOVeride = overidesDic[4] or []
    vrayObjectPropertiesOVeride = overidesDic[5] or []
    cameraOVeride = overidesDic[6] or []
    VScount = cmds.checkBox(vraySetBut,value = True,query = True)
    Tcount = cmds.checkBox(transformObut,value = True,query = True)
    Mcount = cmds.checkBox(materialsObut,value = True,query = True)
    Ccount = cmds.checkBox(cameraObut,value = True,query = True)
    Lcount = cmds.checkBox(lightObut,value = True,query = True)
    Rcount = cmds.checkBox(renderStatsObut,value = True,query = True)
    VPcount = cmds.checkBox(vrayObjectPropertiesObut,value = True,query = True)
    if VScount == 0:
        vraySettingOVeride = ""
    if Tcount == 0:
        transformsOVeride = ""
    if Mcount == 0:
        materialsOVeride = ""
    if Ccount == 0:
        cameraOVeride = ""
    if Lcount == 0:
        lightsOVeride = ""
    if Rcount == 0:
        renderStatsOVeride = ""
    if VPcount == 0:
        vrayObjectPropertiesOVeride = ""
    for render_layer in render_layers:
        vraySettingOVerideL = []
        vraySettingOVerideLstr = ""
        transformsOVerideL = []
        transformsOVerideLstr = ""
        materialsOVerideL = []
        materialsOVerideLstr = ""
        cameraOVerideL= []
        cameraOVerideLstr = ""
        lightsOVerideL= []
        lightsOVerideLstr = ""
        renderStatsOVerideL = []
        renderStatsOVerideLstr = ""
        vrayObjectPropertiesOVerideL = []
        vrayObjectPropertiesOVerideLstr = ""
        vraySettingOVerideVal = 0
        transformsOVerideVal = 0
        materialsOVerideVal = 0
        cameraOVerideVal = 0
        lightsOVerideVal = 0
        renderStatsOVerideVal = 0
        vrayObjectPropertiesOVerideVal = 0
        vraySettingOVerideLstrALL = []
        transformsOVerideLstrALL = []
        materialsOVerideLstrALL = []
        cameraOVerideLstrALL = []
        lightsOVerideLstrALL = []
        renderStatsOVerideLstrALL = []
        vrayObjectPropertiesOVerideLstrALL = []
        for vso in vraySettingOVeride:
            vsoSplit = vso.split("**")
            match = vsoSplit[1]
            match = match[:-1]
            if render_layer  == match:
                vraySettingOVerideVal = vraySettingOVeride[vso]
                vraySettingOVerideVal = str(vraySettingOVerideVal) + " "
                splt = vso.split("**")
                vso = splt[0]
                vso = vso + ": " + vraySettingOVerideVal + ", "
                vso = vso.replace(".:",":")
                vraySettingOVerideLstrALL.append(vso)
        for to in transformsOVeride:
            toSplit = to.split("$")
            match = toSplit[2]
            if render_layer == match:
                transformsOVerideVal = transformsOVeride[to]
                transformsOVerideVal = str(transformsOVerideVal) + " "
                toS = to.split("$")
                to = toS[1] + "." + toS[3]
                to = to + ": " + transformsOVerideVal + ", "
                transformsOVerideLstrALL.append(to)
        for mo in materialsOVeride:
            if "materialAssignment" in mo:
                materialsOVerideVal = materialsOVeride[mo]
                materialsOVerideVal = str(materialsOVerideVal) + " "
                moS = mo.split("$")
                mo = moS[1] + moS[2]
                mo = mo + ": " + materialsOVerideVal + ", "
                if mo not in materialsOVerideLstrALL:
                    materialsOVerideLstrALL.append(mo)
            else:
                moSplit = mo.split("**")
                match = moSplit[1]
                match = match[:-1]
                if render_layer == match:
                    materialsOVerideVal = materialsOVeride[mo]
                    materialsOVerideVal = str(materialsOVerideVal) + " "
                    splt = mo.split("**")
                    mo = splt[0]
                    mo = mo + ": " + materialsOVerideVal + ", "
                    mo = mo.replace(".:",":")
                    materialsOVerideLstrALL.append(mo)
        for co in cameraOVeride:
            coSplit = co.split("**")
            match = coSplit[1]
            match = match[:-1]
            if render_layer == match:
                cameraOVerideVal = cameraOVeride[co]
                cameraOVerideVal = str(cameraOVerideVal) + " "
                splt = co.split("**")
                co = splt[0]
                co = co + ": " + cameraOVerideVal + ", "
                co = co.replace(".:",":")
                cameraOVerideLstrALL.append(co)
        for lo in lightsOVeride:
            loSplit = lo.split("**")
            match = loSplit[1]
            match = match[:-1]
            if render_layer == match:
                lightsOVerideVal = lightsOVeride[lo]
                lightsOVerideVal = str(lightsOVerideVal) + " "
                splt = lo.split("**")
                lo = splt[0]
                lo = lo + ": " + lightsOVerideVal + ", "
                lo = lo.replace(".:",":")
                lightsOVerideLstrALL.append(lo)
        for rso in renderStatsOVeride:
            rsoSplit = rso.split("**")
            match = rsoSplit[3]
            if render_layer == match:
                renderStatsOVerideVal = renderStatsOVeride[rso]
                renderStatsOVerideVal = str(renderStatsOVerideVal) + " "
                rsoS = rso.split("**")
                rso = rsoS[0] + "." + rsoS[2]
                rso = rso + ": " + renderStatsOVerideVal + ", "
                renderStatsOVerideLstrALL.append(rso)
        for vpo in vrayObjectPropertiesOVeride:
            vpoSplit = vpo.split("**")
            match = vpoSplit[3]
            if render_layer == match:
                vrayObjectPropertiesOVerideVal = vrayObjectPropertiesOVeride[vpo]
                vrayObjectPropertiesOVerideVal = str(vrayObjectPropertiesOVerideVal) + " "
                vpoS = vpo.split("**")
                vpo = vpoS[1]+ "." + vpoS[2]
                vpo = vpo + ": " + vrayObjectPropertiesOVerideVal + ", "
                vrayObjectPropertiesOVerideLstrALL.append(vpo)
        overidesDicCombo = vraySettingOVerideLstrALL + transformsOVerideLstrALL + materialsOVerideLstrALL + cameraOVerideLstrALL + lightsOVerideLstrALL + renderStatsOVerideLstrALL + vrayObjectPropertiesOVerideLstrALL
        odcALL = []
        oddStrCombo = ""
        for txtF in txtFieldList:
            txtFsplit = txtF.split("|")
            matchSplit = txtFsplit[2]
            if render_layer == matchSplit:
                for odc in overidesDicCombo:
                    oddStrCombo = oddStrCombo + " " + odc
                cmds.textField(txtF, text = oddStrCombo, edit = True)

def copyOneLayer(render_layers,vraySetBut,transformObut,materialsObut,cameraObut,lightObut,renderStatsObut,vrayObjectPropertiesObut,materials,*args):
    copyAllLay = "A"
    copyLayers(render_layers,vraySetBut,transformObut,materialsObut,cameraObut,lightObut,renderStatsObut,vrayObjectPropertiesObut,materials,copyAllLay)

def copyAllLayers(render_layers,materials,*args):
    copyAllLay = "B"
    copyLayers(render_layers,materials,copyAllLay)

def copyLayers(render_layers,materials,copyAllLay,*args):
    activeLayers = []
    unlockNodes()
    panels = cmds.getPanel( type = "modelPanel" )
    for mPanel in panels:
        cmds.modelEditor(mPanel, edit = True, allObjects = 0)
    initialLayer = cmds.editRenderLayerGlobals(query = True, currentRenderLayer = True)
    startLayer = initialLayer
    if copyAllLay == "A":
        activeLayers.append(startLayer)
    if copyAllLay == "B":
        activeLayers = render_layers
    object_checkCL_g = cmds.ls(g = True)
    object_checkCL_t = cmds.ls(type = "transform")
    object_checkCL_cam = cmds.ls(type = "camera")
    object_checkCL = object_check_g + object_check_t + object_check_cam
    light_types = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
    overides = overides_information_function(render_layers)
    VrayObjectProps = cmds.ls(type = "VRayObjectProperties")
    renderStats = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions"]
    vraySettings = cmds.listAttr("vraySettings")
    vraySettingsO =  overides[0] or []
    transformO = overides[1] or []
    materialO = overides[2] or []
    cameraO = overides[6] or []
    lightO = overides[3] or []
    renderStatsO = overides[4] or []
    vrayObjPropsO = overides[5] or []
    for render_layerl in activeLayers:
        if render_layerl != "defaultRenderLayer":
            obsInLay = cmds.editRenderLayerMembers( render_layerl, fn = True,query=True ) or []
            obsVizDic = {}
            for obCL in object_checkCL:
                visibility_example = cmds.attributeQuery("visibility",node = obCL,exists = True)
                if visibility_example == 1:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layerl)
                    vizString = (obCL + ".visibility")
                    visState = cmds.getAttr(vizString)
                    strKey = (obCL + "%" + str(visState))
                    obsVizDic[strKey] = visState
            cmds.createRenderLayer(obsInLay, name = (render_layerl + "_copy"))
            cmds.editRenderLayerGlobals(currentRenderLayer = (render_layerl + "_copy"))
            cmds.rename(render_layerl,("**_" + render_layerl + "_old"))
            cmds.rename((render_layerl + "_copy"),render_layerl)
            for objL in obsInLay:
                cmds.editRenderLayerMembers((render_layerl),objL)
            for ob in object_check:
                for obvd in obsVizDic:
                     obvdSP = obvd.split("%")
                     if obvdSP[0] == ob:
                         if obvdSP[1] == "True":
                            ste = 1
                         if obvdSP[1] == "False":
                            ste = 0
                         nodeTY = cmds.nodeType(obvdSP[0])
                         if nodeTY != "camera":
                             lockState = cmds.lockNode(obvdSP[0],lock = True, query = True)
                             lockState = lockState[0]
                             if lockState == 0:
                                 cmds.setAttr((obvdSP[0] + ".visibility"),ste)
            for tfo in transformO:
                tfoSP = tfo.split("$")
                layer = tfoSP[2]
                for ob in object_check:
                    if ob == tfoSP[1]:
                        if layer == render_layerl:
                            val = transformO[tfo]
                            if "translate" in tfoSP[3]:
                                cmds.editRenderLayerAdjustment(ob + ".translate")
                                cmds.setAttr((ob + "." + tfoSP[3]),val)
                            if "rotate" in tfoSP[3]:
                                cmds.editRenderLayerAdjustment(ob + ".rotate")
                                cmds.setAttr((ob + "." + tfoSP[3]),val)
                            if "scale" in tfoSP[3]:
                                cmds.editRenderLayerAdjustment(ob + ".scale")
                                cmds.setAttr((ob + "." + tfoSP[3]),val)
            for lo in lightO:
                rr_found = 0
                if "rampRemoved" in lo or "rampMismatch" in lo:
                    rr_found = 1
                loOrig = lo
                loSP = lo.split("**")
                lo = loSP[0]
                layer = loSP[1]
                layer = layer[:-1]
                loSP = lo.split("*")
                lo = loSP[1]
                loOBsp = lo.split(".")
                for ob in object_check:
                    if "spotLight" in ob or "ambientLight" in ob or "directionalLight" in ob or "pointLight" in ob:
                        kid = cmds.listRelatives(ob,children = True)
                        ob = kid[0]
                    if ob == loOBsp[0]:
                        if layer == render_layerl:
                            val = lightO[loOrig]
                            typ = type(val)
                            kindLS = type(val) is list
                            kindInt = type(val) is int
                            kindFL = type(val) is float
                            kindBoo = type(val) is bool
                            kindUni = type(val) is unicode
                            if kindLS == 1:
                                valsub = val[0]
                                valA = valsub[0]
                                valB = valsub[1]
                                valC = valsub[2]
                                cmds.editRenderLayerAdjustment(lo)
                                if rr_found == 1:
                                    a = 1
                                    dest_cons = cmds.listConnections(loSP[1], destination = False, plugs = True, connections = True) or []
                                    dest_cons_size = len(dest_cons)
                                    while a < dest_cons_size:
                                        cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                        a = a + 1
                                cmds.setAttr(loSP[1],valA,valB,valC)
                            if kindFL == 1 or kindInt == 1 or kindBoo == 1:
                                cmds.editRenderLayerAdjustment(lo)
                                if rr_found == 1:
                                    a = 1
                                    dest_cons = cmds.listConnections(loSP[1], destination = False, plugs = True, connections = True) or []
                                    dest_cons_size = len(dest_cons)
                                    while a < dest_cons_size:
                                        cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                        a = a + 1
                                cmds.setAttr(loSP[1],val)
                            if kindUni == 1:
                                cmds.editRenderLayerAdjustment(lo)
                                if rr_found == 1:
                                    a = 1
                                    dest_cons = cmds.listConnections(loSP[1], destination = False, plugs = True, connections = True) or []
                                    dest_cons_size = len(dest_cons)
                                    while a < dest_cons_size:
                                        cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                        a = a + 1
                                if "intensity" in lo or "penumbraAngle" in lo or "dropoff" in lo:
                                    cmds.connectAttr((val + ".outAlpha"),lo,force = True)
                                else:
                                    cmds.connectAttr((val + ".outColor"),lo,force = True)
            for mo in materialO:
                if "mtlOveride_overide" in mo:
                    rr_found = 0
                    if "rampRemoved" in mo:
                        rr_found = 1
                    moOrig = mo
                    moSPL = mo.split("**")
                    layer = moSPL[1]
                    layer = layer[:-1]
                    moSP = mo.split("*")
                    mo = moSP[1]
                    moOBsp = mo.split(".")
                    for mats in materials:
                        if mats == moOBsp[0]:
                            if layer == render_layerl:
                                val = materialO[moOrig]
                                typ = type(val)
                                kindLS = type(val) is list
                                kindInt = type(val) is int
                                kindFL = type(val) is float
                                kindBoo = type(val) is bool
                                kindUni = type(val) is unicode
                                if kindLS == 1:
                                    valsub = val[0]
                                    valA = valsub[0]
                                    valB = valsub[1]
                                    valC = valsub[2]
                                    cmds.editRenderLayerAdjustment(mo)
                                    if rr_found == 1:
                                        a = 1
                                        dest_cons = cmds.listConnections(moSP[1], destination = False, plugs = True, connections = True) or []
                                        dest_cons_size = len(dest_cons)
                                        while a < dest_cons_size:
                                            cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                            a = a + 1
                                    cmds.setAttr(moSP[1],valA,valB,valC)
                                if kindFL == 1 or kindInt == 1 or kindBoo == 1:
                                    cmds.editRenderLayerAdjustment(mo,layer = render_layerl)
                                    if rr_found == 1:
                                        a = 1
                                        dest_cons = cmds.listConnections(moSP[1], destination = False, plugs = True, connections = True) or []
                                        dest_cons_size = len(dest_cons)
                                        while a < dest_cons_size:
                                            cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                            a = a + 1
                                    cmds.setAttr(moSP[1],val)
                                if kindUni == 1:
                                    cmds.editRenderLayerAdjustment(mo)
                                    if rr_found == 1:
                                        a = 1
                                        dest_cons = cmds.listConnections(moSP[1], destination = False, plugs = True, connections = True) or []
                                        dest_cons_size = len(dest_cons)
                                        while a < dest_cons_size:
                                            cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                            a = a + 1
                                    cmds.connectAttr((val + ".outColor"),mo,force = True)
                if "materialAssignment" in mo:
                    moOrig = mo
                    moSP = mo.split("$")
                    layer = moSP[1]
                    mo = moSP[2]
                    moAo = moSP[0]
                    for mats in materials:
                        if mats == moSP[0]:
                            if layer == render_layerl:
                                val = materialO[moOrig]
                                typ = type(val)
                                cmds.select(moAo)
                                cmds.hyperShade(assign = val)
            for rs in renderStatsO:
                rsOrig = rs
                rsSP = rs.split("**")
                layer = rsSP[3]
                rs = rsSP[0]
                rsB = rsSP[2]
                rsAttr = rsB
                rs = rs + "." + rsB
                for rS in renderStats:
                    if rsAttr == rS:
                        if layer == render_layerl:
                            val = renderStatsO[rsOrig]
                            typ = type(val)
                            kindLS = type(val) is list
                            kindInt = type(val) is int
                            kindFL = type(val) is float
                            kindBoo = type(val) is bool
                            kindUni = type(val) is unicode
                            if kindLS == 1:
                                valsub = val[0]
                                valA = valsub[0]
                                valB = valsub[1]
                                valC = valsub[2]
                                cmds.editRenderLayerAdjustment(rs)
                                cmds.setAttr(rs,valA,valB,valC)
                            if kindFL == 1 or kindInt == 1 or kindBoo == 1:
                                cmds.editRenderLayerAdjustment(rs)
                                cmds.setAttr(rs,val)
                            if kindUni == 1:
                                cmds.editRenderLayerAdjustment(rs)
                                cmds.connectAttr((val + ".outColor"),rs,force = True)
            for vrp in vrayObjPropsO:
                vrpOrig = vrp
                vrpSP = vrp.split("**")
                layer = vrpSP[3]
                vrp = vrpSP[0]
                vrpFull = vrp + "." + vrpSP[2]
                for vrpB in VrayObjectProps:
                    if vrp == vrpB:
                        if layer == render_layerl:
                            val = vrayObjPropsO[vrpOrig]
                            typ = type(val)
                            kindLS = type(val) is list
                            kindInt = type(val) is int
                            kindFL = type(val) is float
                            kindBoo = type(val) is bool
                            kindUni = type(val) is unicode
                            if kindLS == 1:
                                valsub = val[0]
                                valA = valsub[0]
                                valB = valsub[1]
                                valC = valsub[2]
                                cmds.editRenderLayerAdjustment(vrpFull)
                                cmds.setAttr(vrpFull,valA,valB,valC)
                            if kindFL == 1 or kindInt == 1 or kindBoo == 1:
                                cmds.editRenderLayerAdjustment(vrpFull)
                                cmds.setAttr(vrpFull,val)
                            if kindUni == 1:
                                cmds.editRenderLayerAdjustment(vrpFull)
                                cmds.connectAttr((val + ".outColor"),vrpFull,force = True)
            for vrs in vraySettingsO:
                rr_found = 0
                if "rampRemoved" in vrs:
                    rr_found = 1
                vrsOrig = vrs
                vrsSP = vrs.split("**")
                vrs = vrsSP[0]
                layer = vrsSP[1]
                layer = layer[:-1]
                vrsSP = vrs.split("*")
                vrs = vrsSP[1]
                vrsFull = vrs
                for vrsB in vraySettings:
                    vrsB = "vraySettings." + vrsB
                    if vrs == vrsB:
                        if layer == render_layerl:
                            val = vraySettingsO[vrsOrig]
                            typ = type(val)
                            kindLS = type(val) is list
                            kindInt = type(val) is int
                            kindFL = type(val) is float
                            kindBoo = type(val) is bool
                            kindUni = type(val) is unicode
                            if kindLS == 1:
                                valsub = val[0]
                                valA = valsub[0]
                                valB = valsub[1]
                                valC = valsub[2]
                                cmds.editRenderLayerAdjustment(vrsFull)
                                if rr_found == 1:
                                    a = 1
                                    dest_cons = cmds.listConnections(vrsSP[1], destination = False, plugs = True, connections = True) or []
                                    dest_cons_size = len(dest_cons)
                                    while a < dest_cons_size:
                                        cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                        a = a + 1
                                cmds.setAttr(vrsFull,valA,valB,valC)
                            if kindFL == 1 or kindInt == 1 or kindBoo == 1:
                                cmds.editRenderLayerAdjustment(vrsFull)
                                if rr_found == 1:
                                    a = 1
                                    dest_cons = cmds.listConnections(vrsSP[1], destination = False, plugs = True, connections = True) or []
                                    dest_cons_size = len(dest_cons)
                                    while a < dest_cons_size:
                                        cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                        a = a + 1
                                cmds.setAttr(vrsFull,val)
                            if kindUni == 1:
                                cmds.editRenderLayerAdjustment(vrsFull)
                                if rr_found == 1:
                                    a = 1
                                    dest_cons = cmds.listConnections(vrsSP[1], destination = False, plugs = True, connections = True) or []
                                    dest_cons_size = len(dest_cons)
                                    while a < dest_cons_size:
                                        cmds.disconnectAttr(dest_cons[1],dest_cons[0])
                                        a = a + 1
                                cmds.connectAttr((val + ".outColor"),vrsFull, force = True)
        cmds.editRenderLayerGlobals(currentRenderLayer = initialLayer)
        layer_switcher()

class LAYERS_WINDOW_TOOL():
    def __init__(self):
        chris = ''

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clear_layout(item.layout())

    def add_object_to_all_layers(self):
        selected_objects = cmds.ls(sl = True)
        for selected_object in selected_objects:
            for render_layer in self.render_layers:
                if render_layer != "defaultRenderLayer":
                    cmds.editRenderLayerMembers(render_layer, selected_object)

    def remove_object_from_all_layers(self):
        selected_objects = cmds.ls(sl = True)
        for selected_object in selected_objects:
            for render_layer in self.render_layers:
                if render_layer != "defaultRenderLayer":
                    cmds.editRenderLayerMembers(render_layer, selected_object, remove = True)

    def make_object_visible_in_all_layers(self):
        selected_objects = cmds.ls(sl = True)
        for selected_object in selected_objects:
            for render_layer in self.render_layers:
                if render_layer != "defaultRenderLayer":
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                    cmds.setAttr(selected_object + '.visibility', 1)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)


    def hide_object_in_all_layers(self):
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

    def fixCams(self):
        for render_layer in self.render_layers:
            cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
            if render_layer == "defaultRenderLayer":
                for camera in self.cameras:
                    if camera == "perspShape":
                        cmds.setAttr(camera + ".renderable",1)
            if render_layer != "defaultRenderLayer":
                for camera in self.cameras:
                    if "FtTp" in camera or "FtRt" in camera or "FtLt" in camera in camera or "FtLtTp" in camera or "FtRtTp" in camera or "Ft" in camera or "Bk" in camera or "Rt" in camera or "Lt" in camera or "Tp" in camera or "Bt" in camera:
                        var = 0
                    if "C1N1" in camera or "C1N1Shape" in camera or "C7N1" in camera or "C7N1Shape" in camera or "C2N1" in camera or "C2N1Shape" in camera  or "C8N1" in camera  or "C8N1Shape" in camera  or "C3N1" in camera or "C3N1Shape" in camera  or "C9N1" in camera  or "C9N1Shape" in camera or "C1C1" in camera or "C1C1Shape" in camera or "C1L1" in camera  or "C1L1Shape" in camera or "C1R1" in camera or "C1R1Shape" in camera or "C1N2" in camera or "C1NShape2" in camera or "C1N2Shape" in camera or "C1N4" in camera or "C1NShape4" in camera or "C1N4Shape" in camera:
                        var = 1
                    if "C1N1Shape1" in camera or "C7N1Shape1" in camera or "C2N1Shape1" in camera or "C8N1Shape1" in camera or "C3N1Shape1" in camera or "C9N1Shape1" in camera or "C1C1Shape1" in camera or "C1L1Shape1" in camera or "C1R1Shape1" in camera or "C1N2Shape1" in camera or "C1N4Shape1" in camera:
                        var = 2
                    if "perspShape2" in camera or "topShape2" in camera or "frontShape2" in camera or "sideShape2" in camera or "backShape1" in camera or "backShape2" in camera:
                        var = 3
                    if var == 0:
                        if camera == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape":
                            camera_split = camera.split("Shape")
                            camera_split = camera_split[0] +  camera_split[1]
                        else:
                            camera_split = cam.split("_")
                            camCut = camera_split[0]
                            camera_split = camCut
                    if var == 1:
                        if camera == "perspShape" or camera == "topShape" or camera == "frontShape" or camera == "sideShape":
                            camera_split = camera.split("Shape")
                            camera_split = camera_split[0] + camera_split[1]
                        else:
                            camera_split = camera.split("_")
                            camCut = camera_split[1]
                            camera_split = camCut.split("Shape")
                            camera_split = camera_split[0] + camera_split[1]
                    if var == 2:
                        if camera == "perspShape" or camera == "topShape" or camera == "frontShape" or camera == "sideShape":
                            camera_split = camera.split("Shape")
                            camera_split = camera_split[0] + camera_split[1]
                        else:
                            camera_split = camera.split("_")
                            camCut = camera_split[1]
                            camera_split = camCut.split("Shape")
                            camera_split = camera_split[0]
                    if var == 3:
                        if camera == "perspShape" or camera == "topShape" or camera == "frontShape" or camera == "sideShape" or camera == "backShape1" or camera == "backShape2":
                            if "2" not in camera:
                                camera_split = camera.split("Shape")
                                camera_split = camera_split[0] + camera_split[1]
                            if "2" in camera:
                                camera_split = camera.split("Shape")
                                camera_split = camera_split[0]
                        else:
                            camera_split = camCut.split("Shape")
                            camera_split = camera_split[0]
                    camera_splitSPb = camera_split.split("Shape")
                    camera_splitSPb = camera_splitSPb[0]
                    if camera_split == render_layer or (camera_splitSPb + "_BTY") == render_layer or (camera_splitSPb + "_REF") == render_layer or (camera_splitSPb + "_SHD") == render_layer or (camera_splitSPb + "_REF_MATTE") == render_layer or ("BTY_" + camera_splitSPb) == render_layer:
                        cmds.editRenderLayerAdjustment(camera + ".renderable")
                        cmds.setAttr(camera + ".renderable",1)
                    else:
                        cmds.editRenderLayerAdjustment(camera + ".renderable")
                        cmds.setAttr(camera + ".renderable",0)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def evaluate_objects_in_render_layers(self):
        #print 'evaluate_objects_in_render_layers'
        selected_objects = cmds.ls(sl = True)
        for OIL_button in self.OIL_button_pointer_dic:
            for render_layer in self.render_layers:
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                if render_layer != 'defaultRenderLayer':
                    render_layer_linked_to_pointer = self.OIL_button_pointer_dic[OIL_button]
                    if render_layer_linked_to_pointer == render_layer:
                        for object in selected_objects:
                            object_in_render_layer_check = cmds.editRenderLayerMembers(render_layer, object, query = True) or []
                            if object in object_in_render_layer_check:
                                OIL_button.setChecked(False)
                            else:
                                OIL_button.setChecked(True)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def evaluate_objects_visible_in_render_layers(self):
        #print 'evaluate_objects_visible_in_render_layers'
        selected_objects = cmds.ls(sl = True)
        for OVL_button in self.OVL_button_pointer_dic:
            for render_layer in self.render_layers:
                cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                if render_layer != 'defaultRenderLayer':
                    render_layer_linked_to_pointer = self.OVL_button_pointer_dic[OVL_button]
                    if render_layer_linked_to_pointer == render_layer:
                        for object in selected_objects:
                            object_visibility_in_render_layer = cmds.getAttr(object + '.visibility')
                            if object_visibility_in_render_layer == 1:
                                OVL_button.setChecked(False)
                            else:
                                OVL_button.setChecked(True)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)

    def OIL_toggle_object_in_render_layer(self,OIL_button):
        #print 'OIL_add_object'
        selected_objects = cmds.ls(sl = True)
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                render_layer_linked_to_button = self.OIL_button_pointer_dic[OIL_button]
                if render_layer_linked_to_button == render_layer:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                    for object in selected_objects:
                        if OIL_button.isChecked():
                            cmds.editRenderLayerMembers(render_layer, object)
                        else:
                            cmds.editRenderLayerMembers(render_layer, object, remove = True)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)
        self.populate_gui()


    def OVL_object_toggle_visibility_in_render_layer(self,OVL_button):
        #print 'OVL_object_made_visible_in_render_layer'
        selected_objects = cmds.ls(sl = True)
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                render_layer_linked_to_button = self.OVL_button_pointer_dic[OVL_button]
                if render_layer_linked_to_button == render_layer:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)
                    for object in selected_objects:
                        if OVL_button.isChecked():
                            cmds.setAttr(object + '.visibility', 1)
                        else:
                            cmds.setAttr(object + '.visibility', 0)
        cmds.editRenderLayerGlobals(currentRenderLayer = self.initial_layer)
        self.populate_gui()

    def render_layer_change(self,render_layer_button):
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                render_layer_linked_to_button = self.render_layer_button_pointer_dic[render_layer_button]
                if render_layer_linked_to_button == render_layer:
                    cmds.editRenderLayerGlobals(currentRenderLayer = render_layer)

    def evaluate_cameras(self):
        #print 'evaluate cameras'
        self.renderable_cameras_dic = {}
        renderable_cameras = []
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
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
            if render_layer != 'defaultRenderLayer':
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
        self.clear_layout(self.vertical_layout)
        self.evaluate_cameras()
        for render_layer in self.render_layers:
            if render_layer != 'defaultRenderLayer':
                self.render_layer_layout = QtWidgets.QHBoxLayout()
                self.vertical_layout.addLayout(self.render_layer_layout)
                button_OIL = QtWidgets.QPushButton('OIL')
                button_OIL.setCheckable(True)
                #button_OIL.setChecked(True)
                button_OIL.setStyleSheet("QPushButton {background:rgb(120,150,180);} QPushButton::checked{background-color: rgb(40, 40, 40);""border:0px solid rgb(80, 170, 20)};")
                button_OIL.toggle()
                self.OIL_button_pointer_dic[button_OIL] = render_layer
                button_OIL.setFixedSize(30,21)
                self.render_layer_layout.addWidget(button_OIL)
                button_OVL = QtWidgets.QPushButton('OVL')
                button_OVL.setCheckable(True)
                #button_OVL.setChecked(True)
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
                i = 0
                renderable_cameras = self.renderable_cameras_dic[render_layer] or []
                for camera in self.cameras:
                    if camera == renderable_cameras[0]:
                        self.cameras_combobox.setCurrentIndex(i)
                    i = i + 1
                if len(renderable_cameras) > 1:
                    self.cameras_combobox.setStyleSheet("background-color: rgb(130, 10, 10);")
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
        button_make_object_visible_in_all_layers = QtWidgets.QPushButton('make selection visible in all render layers')
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
        #button_fix_cam_layer_assignments.pressed.connect(partial(self.fix_cam_layer_assignments))
        rebuild_selected_render_layer = QtWidgets.QPushButton('rebuild selected render layer')
        self.layout_bottom.addWidget(rebuild_selected_render_layer)
        #rebuild_selected_render_layer.pressed.connect(partial(self.rebuild_selected_render_layer))
        rebuild_all_layers = QtWidgets.QPushButton('rebuild all render layers')
        self.layout_bottom.addWidget(rebuild_all_layers)
        #rebuild_selected_render_layer.pressed.connect(partial(self.rebuild_selected_render_layer))
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
        #self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["NameChanged", self.populate_gui])
        #self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerManagerChange", self.populate_gui])
        #self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerChange", self.populate_gui])
        #self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["SelectionChanged", self.populate_gui])
        self.populate_gui()
        window.show()

def main():
    layers_tool_inst = LAYERS_WINDOW_TOOL()
    layers_tool_inst.window_gen()

main()
