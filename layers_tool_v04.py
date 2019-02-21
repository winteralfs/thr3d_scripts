print 'layers_tool_v04'

import maya.cmds as cmds
from functools import partial
import re

render_layers = cmds.ls(type = "renderLayer")
light_types = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
mats_VRayMtl = cmds.ls(type = "VRayMtl")
mats_phong = cmds.ls(type = "phong")
mats_blinn = cmds.ls(type = "blinn")
mats_lambert = cmds.ls(type = "lambert")
mats_surface = cmds.ls(type = "surfaceShader")
mats_disp = cmds.ls(type = "displacementShader")
displacement_nodes = cmds.ls(type = "VRayDisplacement")
place_nodes = cmds.ls(type = "place2dTexture")
file_nodes = cmds.ls(type = "file")
layeredTexture = cmds.ls(type = "layeredTexture")
mats_VRayBlendMtls = cmds.ls(type = "VRayBlendMtl")
materials = mats_VRayMtl + mats_phong + mats_blinn + mats_lambert + mats_surface + place_nodes + file_nodes + mats_disp + displacement_nodes + layeredTexture + mats_VRayBlendMtls
objects_check_g = cmds.ls(g = True)
objects_check_t = cmds.ls(type = "transform")
objects_check_cam = cmds.ls(type = "camera")
objects_check = objects_check_g + objects_check_t + materials + objects_check_cam
lites = cmds.ls(lt = True)
vray_lites = []
for o in objects_check:
    nt = cmds.nodeType(o)
    for lt in light_types:
        if nt == lt:
            vray_lites.append(o)
objects_check.append("vraySettings")

def overide_info_function(render_layers):
    class ATTR_OVERRIDES_CLASS:
        def __init__(self,render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check):
            rll_ramp_overrides = {}
            self.obj_label = obj_label
            self.render_layers = render_layers
            self.obj_type = obj_type
            print " "
            print "self.obj_type = ",self.obj_type
            obj_list = objects_check
            if self.obj_type == "camera" or self.obj_type == "VRayLightRectShape" or self.obj_type == "spotLight" or self.obj_type == "ambientLight" or self.obj_type == "directionalLight" or self.obj_type == "pointLight" or self.obj_type == "VRayMtl" or self.obj_type == "blinn" or self.obj_type == "phong" or self.obj_type == "lambert" or self.obj_type == "surfaceShader" or self.obj_type == "displacementShader" or self.obj_type == "VRayDisplacement" or self.obj_type == "place2dTexture" or self.obj_type == "file" or self.obj_type == "gammaCorrect" or self.obj_type == "layeredTexture" or self.obj_type == "VRayBlendMtl":
                self.obj_list = cmds.ls(type = self.obj_type)
            if self.obj_type == "VRaySettingsNode":
                self.obj_list = []
                self.obj_list.append("vraySettings")
            self.attr_overrides_dic = attr_overrides_dic
            self.rem_attr_list = rem_attr_list

        def attr_override_detect(self):
            for obj in self.obj_list:
                default_ramp = "none"
                override_ramp = "none"
                cns_count = 1
                it_list_count = 1
                it_list = []
                nt = cmds.nodeType(obj)
                if nt == self.obj_type:
                    attrs = cmds.listAttr(obj)
                    for rem in self.rem_attr_list:
                        print 'rem = ',rem
                        attrs.remove(rem)
                    if self.obj_type == "layeredTexture":
                        cns = cmds.listConnections(obj, source = True,destination = False) or []
                        cns_count = len(cns)
                        for cn in cns:
                            cn_string = cn + ".outColor"
                            conInfo = cmds.connectionInfo(cn_string,destinationFromSource = True) or []
                            for ci in conInfo:
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
                            default_attr_valueue = cmds.getAttr(attr_string)
                            attr_connections = cmds.listConnections(attr_string,destination = False) or []
                            default_ramp_found = 0
                            for conn in attr_connections:
                                conn_type = cmds.nodeType(conn)
                                if conn_type == "ramp" or conn_type == "fractal" or conn_type == "noise" or conn_type == "file" or conn_type == "checker" or conn_type == "cloud" or conn_type == "brownian" or conn_type == "bulge" or conn_type == "VRayMtl" or conn_type == "blinn" or conn_type == "phong" or conn_type == "lambert" or conn_type == "surfaceShader":
                                    default_ramp_found = 1
                                    default_ramp = conn
                            for rl in render_layers:
                                if rl != "defaultRenderLayer":
                                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                                    cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                                    attr_connections = cmds.listConnections(attr_string,destination = False) or []
                                    override_rampFound = 0
                                    for attr_conn in attr_connections:
                                        attr_type = cmds.nodeType(attr_conn)
                                        if attr_type == "ramp" or attr_type == "fractal" or attr_type == "noise" or attr_type == "file" or attr_type == "checker" or attr_type == "cloud" or attr_type == "brownian" or attr_type == "bulge" or attr_type == "VRayMtl" or attr_type == "blinn" or attr_type == "phong" or attr_type == "lambert" or attr_type == "surfaceShader":
                                            override_rampFound = 1
                                            override_ramp = attr_conn
                                    override_attr_valueue = cmds.getAttr(attr_string)
                                    if default_ramp_found == 0 and override_rampFound == 0:
                                        if default_attr_valueue != override_attr_valueue:
                                            attr_dic_string = self.obj_label + "_overide*" + obj + "." + attr + "**" + rl + "_"
                                            self.attr_overrides_dic[attr_dic_string] = override_attr_valueue
                                    if default_ramp_found == 0 and override_rampFound == 1:
                                        attr_dic_string = self.obj_label + "_overide_rampAdded*" + obj + "." + attr + "**" + rl + "_"
                                        self.attr_overrides_dic[attr_dic_string] = override_ramp
                                    if default_ramp_found == 1 and override_rampFound == 0:
                                        override_attr_valueue = cmds.getAttr(attr_string)
                                        attr_dic_string = self.obj_label + "_overide_rampRemoved*" + obj + "." + attr + "**" + rl + "_"
                                        self.attr_overrides_dic[attr_dic_string] = override_attr_valueue
                                    if default_ramp_found == 1 and override_rampFound == 1:
                                        override_ramp = attr_conn
                                        if override_ramp != default_ramp:
                                            attr_dic_string = self.obj_label + "_overide_rampMismatch*" + obj + "." + attr + "**" + rl + "_"
                                            self.attr_overrides_dic[attr_dic_string] = override_ramp
                                        if override_ramp == default_ramp:
                                            rll_overrides = cmds.listConnections(rl + ".adjustments", p = True, c = True) or []
                                            rll_ramp_overrides = []
                                            for cn in rll_overrides:
                                                t = cmds.nodeType(cn)
                                                if t == "ramp":
                                                    if cn not in rll_ramp_overrides:
                                                        rll_ramp_overrides.append(cn)
                                                for i in range(0, len(rll_overrides), 2):
                                                    rl_conn = rll_overrides[i]
                                                    override_attr = rll_overrides[i+1]
                                                    override_index = rl_conn.split("]")[0]
                                                    override_index = override_index.split("[")[-1]
                                                    override_valueue = cmds.getAttr(rl + ".adjustments[%s].valueue" %override_index)
                                                    attr_dic_string =  self.obj_label + "_" + attr + "_rampOveride" + "*" + override_attr + "**" + rl
                                                    if attr_dic_string not in self.attr_overrides_dic and override_ramp in override_attr:
                                                        self.attr_overrides_dic[attr_dic_string] = override_valueue
                        it = it + 1
            return(self.attr_overrides_dic)


    def translations(objects_check, render_layers):
        translation_default_valueues_dic = {}
        object_in_layers = []
        transform_layer_overrides = []
        transform_valueues_dic_oth = {}
        transform_layer_dic = {}
        cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
        lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
        for ob in objects_check_t:
            strtranslateX = ob + ".translateX"
            translateX = cmds.getAttr(strtranslateX)
            var = ob + "$" + lay + "$translateX"
            translation_default_valueues_dic[var] = translateX
            strtranslateY = ob + ".translateY"
            translateY = cmds.getAttr(strtranslateY)
            var = ob + "$" + lay + "$translateY"
            translation_default_valueues_dic[var] = translateY
            strtranslateZ = ob + ".translateZ"
            translateZ = cmds.getAttr(strtranslateZ)
            var = ob + "$" + lay + "$translateZ"
            translation_default_valueues_dic[var] = translateZ
            strrotateX = ob + ".rotateX"
            rotateX = cmds.getAttr(strrotateX)
            var = ob + "$" + lay + "$rotateX"
            translation_default_valueues_dic[var] = rotateX
            strrotateY = ob + ".rotateY"
            rotateY = cmds.getAttr(strrotateY)
            var = ob + "$" + lay + "$rotateY"
            translation_default_valueues_dic[var] = rotateY
            strrotateZ = ob + ".rotateZ"
            rotateZ = cmds.getAttr(strrotateZ)
            var = ob + "$" + lay + "$rotateZ"
            translation_default_valueues_dic[var] = rotateZ
            strScaleX = ob + ".scaleX"
            scaleX = cmds.getAttr(strScaleX)
            var = ob + "$" + lay + "$scaleX"
            translation_default_valueues_dic[var] = scaleX
            strScaleY = ob + ".scaleY"
            scaleY = cmds.getAttr(strScaleY)
            var = ob + "$" + lay + "$scaleY"
            translation_default_valueues_dic[var] = scaleY
            strScaleZ = ob + ".scaleZ"
            scaleZ = cmds.getAttr(strScaleZ)
            var = ob + "$" + lay + "$scaleZ"
            translation_default_valueues_dic[var] = scaleZ
        for ob in objects_check_t:
            for lay in render_layers:
                cmds.editRenderLayerGlobals( currentRenderLayer = lay )
                lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
                if "defaultRenderLayer" != lay:
                    strtranslateX = ob + ".translateX"
                    translateX = cmds.getAttr(strtranslateX)
                    var = ob + "$" + lay + "$translateX"
                    transform_valueues_dic_oth[var] = translateX
                    strtranslateY = ob + ".translateY"
                    translateY = cmds.getAttr(strtranslateY)
                    var = ob + "$" + lay + "$translateY"
                    transform_valueues_dic_oth[var] = translateY
                    strtranslateZ = ob + ".translateZ"
                    translateZ = cmds.getAttr(strtranslateZ)
                    var = ob + "$" + lay + "$translateZ"
                    transform_valueues_dic_oth[var] = translateZ
                    strrotateX = ob + ".rotateX"
                    rotateX = cmds.getAttr(strrotateX)
                    var = ob + "$" + lay + "$rotateX"
                    transform_valueues_dic_oth[var] = rotateX
                    strrotateY = ob + ".rotateY"
                    rotateY = cmds.getAttr(strrotateY)
                    var = ob + "$" + lay + "$rotateY"
                    transform_valueues_dic_oth[var] = rotateY
                    strrotateZ = ob + ".rotateZ"
                    rotateZ = cmds.getAttr(strrotateZ)
                    var = ob + "$" + lay + "$rotateZ"
                    transform_valueues_dic_oth[var] = rotateZ
                    strScaleX = ob + ".scaleX"
                    scaleX = cmds.getAttr(strScaleX)
                    var = ob + "$" + lay + "$scaleX"
                    transform_valueues_dic_oth[var] = scaleX
                    strScaleY = ob + ".scaleY"
                    scaleY = cmds.getAttr(strScaleY)
                    var = ob + "$" + lay + "$scaleY"
                    transform_valueues_dic_oth[var] = scaleY
                    strScaleZ = ob + ".scaleZ"
                    scaleZ = cmds.getAttr(strScaleZ)
                    var = ob + "$" + lay + "$scaleZ"
                    transform_valueues_dic_oth[var] = scaleZ
        for transvalue in transform_valueues_dic_oth:
            transvalueSplit = transvalue.split("$")
            for transvalueDef in translation_default_valueues_dic:
                transvalueDefSplit = transvalueDef.split("$")
                if transvalueSplit[0] == transvalueDefSplit[0] and transvalueSplit[2] == transvalueDefSplit[2]:
                    valueu = transform_valueues_dic_oth[transvalue]
                    valueuDef = translation_default_valueues_dic[transvalueDef]
                    if valueu != valueuDef:
                        transform_layer_overrides.append(transvalue)
                        transform_layer_dic["transO$" + transvalue] = valueu
        return translation_default_valueues_dic,transform_valueues_dic_oth,transform_layer_overrides,objects_check,render_layers,transform_layer_dic

    def material_assignments(objects_check, render_layers):
        mats_list = []
        mats_list_overrides = []
        material_layer_overrides = []
        materials_default_dic = {}
        materials_override_dic = {}
        material_layers_dic = {}
        for ob in objects_check:
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
            for L in render_layers:
                cmds.editRenderLayerGlobals( currentRenderLayer = L )
                if L == "defaultRenderLayer":
                    cmds.select(clear = True)
                    cmds.select(ob)
                    cmds.hyperShade(smn = True)
                    mats_list = cmds.ls(sl = True)
                    for MM in mats_list:
                        NT = cmds.nodeType(MM)
                        if NT != "renderLayer":
                            if MM not in mats_list_overrides:
                                mats_list_overrides.append(MM)
                            dictKeyOTH = ob + "$" + L + "$"
                            materials_default_dic[dictKeyOTH] = MM
                else:
                    cmds.select(clear = True)
                    cmds.select(ob)
                    cmds.hyperShade(smn = True)
                    mats_list = cmds.ls(sl = True)
                    for MM in mats_list:
                        NT = cmds.nodeType(MM)
                        if NT != "renderLayer":
                            if MM not in mats_list_overrides:
                                mats_list_overrides.append(MM)
                            dictKeyOTH = ob + "$" + L + "$"
                            materials_override_dic[dictKeyOTH] = MM
        for material_override_dic in materials_override_dic:
           material_valueue_split = material_override_dic.split("$")
           for material_default_dic in materials_default_dic:
               material_default_value_split = material_default_dic.split("$")
               if material_valueue_split[0] == material_default_value_split[0]:
                    material_override = materials_override_dic[material_override_dic]
                    material_default = materials_default_dic[material_default_dic]
                    if material_override != material_default:
                        material_layer_overrides.append(material_override_dic)
                        material_dic_string = material_override_dic + ".materialAssignment"
                        if material_dic_string not in material_layers_dic and "Shape" not in material_dic_string:
                            material_layers_dic[material_dic_string] = material_override
        return(mats_list_overrides,mats_list_overrides,materials_override_dic,material_layer_overrides,material_layers_dic)

    def material_overrides(objects_check,render_layers):
        materials_overrides_dic = {}
        attr_overrides_dic = materials_overrides_dic
        obj_label = "mtlOveride"

        obj_type = "VRayMtl"
        rem_attr_list = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","outColor","outColorR","outColorG","outColorB","outApiType","outApiClassification","outTransparency",
        "outTransparencyR","outTransparencyG","outTransparencyB","reflectionsMaxDepth","refractionsMaxDepth","swatchAutoUpdate","swatchAlwaysRender","swatchExplicitUpdate","swatchMaxRes","color","diffuseColorR"
        ,"diffuseColorG","diffuseColorB","diffuseColorAmount","roughnessAmount","illumColor","illumColorR","illumColorG","illumColorB","illumGI","compensateExposure","reflectionColor","reflectionColorR","reflectionColorG"
        ,"reflectionColorB","reflectionColorAmount","reflectionExitColor","reflectionExitColorR","reflectionExitColorG","reflectionExitColorB","hilightGlossinessLock","hilightGlossiness","reflectionGlossiness","reflectionSubdivs"
        ,"reflectionAffectAlpha","reflInterpolation","reflMapMinRate","reflMapMaxRate","reflMapColorThreshold","reflMapNormalThreshold","reflMapSamples","useFresnel","lockFresnelIORToRefractionIOR","fresnelIOR","reflectOnBackSide"
        ,"softenEdge","fixDarkEdges","glossyFresnel","ggxTailFalloff","ggxOldTailFalloff","anisotropy","anisotropyUVWGen","anisotropyRotation","refractionColor","refractionColorR","refractionColorG","refractionColorB","refractionColorAmount"
        ,"refractionExitColor","refractionExitColorR","refractionExitColorG","refractionExitColorB","refractionExitColorOn","refractionGlossiness","refractionSubdivs","refractionIOR","refrDispersionOn","refrDispersionAbbe","refrInterpolation"
        ,"refrMapMinRate","refrMapMaxRate","refrMapColorThreshold","refrMapNormalThreshold","refrMapSamples","fogColor","fogColorR","fogColorG","fogColorB","fogMult","fogBias","affectShadows","affectAlpha","traceReflections","traceRefractions"
        ,"cutoffThreshold","brdftype","bumpMaptype","bumpMap","bumpMapR","bumpMapG","bumpMapB","bumpMult","bumpShadows","bumpDeltaScale","sssOn","translucencyColor","translucencyColorR","translucencyColorG","translucencyColorB","thickness","scatterCoeff"
        ,"scatterDir","scatterLevels","scatterSubdivs","sssEnvironment","opacityMap","opacityMapR","opacityMapG","opacityMapB","doubleSided","useIrradianceMap","reflectionDimDistanceOn","reflectionDimDistance","reflectionDimFallOff","attributeAliasList"]
        attr_check = ["color","diffuseColorAmount","opacityMap","roughnessAmount","illumColor","illumGI","compensateExposure","brdftype","reflectionColor","reflectionColorAmount","hilightGlossinessLock",
        "hilightGlossiness","reflectionGlossiness","useFresnel","glossyFresnel","lockFresnelIORToRefractionIOR","refractionColor","refractionColorAmount","refractionGlossiness","refractionIOR",
        "fogColor","fogMult","fogBias","affectShadows","sssOn","translucencyColor","scatterSubdivs","scatterDir","scatterLevels","scatterCoeff","thickness","sssEnvironment","traceRefractions",
        "refractionExitColorOn","refractionsMaxDepth","affectAlpha","refrDispersionOn","refrDispersionAbbe","bumpMaptype","bumpMap","bumpMult","bumpShadows","bumpDeltaScale","cutoffThreshold",
        "doubleSided","useIrradianceMap","fixDarkEdges","caching","nodeState","reflMapMinRate","reflMapMaxRate","reflMapColorThreshold","reflMapNormalThreshold","reflMapSamples"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "blinn"
        rem_attr_list = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "eccentricity", "specularRollOff", "reflectionRolloff"]
        attr_check = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","eccentricity","specularRollOff","specularColor","reflectivity","reflectedColor"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "phong"
        rem_attr_list = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "cosinePower"]
        attr_check = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","cosinePower","specularColor","reflectivity","reflectedColor"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "lambert"
        rem_attr_list = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB"]
        attr_check = ["color","transparency","ambientColor","incandescence","diffuse","translucence","translucenceDepth","translucenceFocus"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "surfaceShader"
        rem_attr_list = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outMatteOpacity","outMatteOpacityR","outMatteOpacityG","outMatteOpacityB","outGlowColor","outGlowColorR","outGlowColorG","outGlowColorB","materialAlphaGain"]
        attr_check = ["outColor","outTransparency","outGlowColor","outMatteOpacity"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "place2dTexture"
        rem_attr_list = ['message','caching','frozen','isHistoricallyInteresting','nodeState','binMembership','uvCoord','uCoord','vCoord','vertexUvOne','vertexUvOneU','vertexUvOneV','vertexUvTwo','vertexUvTwoU','vertexUvTwoV','vertexUvThree','vertexUvThreeU','vertexUvThreeV','vertexCameraOne','vertexCameraOneX','vertexCameraOneY','vertexCameraOneZ','uvFilterSize','uvFilterSizeX','uvFilterSizeY','coverage','coverageU','coverageV','translateFrame','translateFrameU','translateFrameV','rotateFrame','mirrorU','mirrorV','stagger','wrapU','wrapV','repeatUV','repeatU','offsetU','offsetV','rotateUV','noiseU','noiseV','fast']
        attr_check = ["coverageU","coverageV","translateFrameU","translateFrameV","rotateFrame","mirrorU","mirrorV","wrapU","wrapV","stagger","repeatU","repeatV","offsetU","offsetV","rotateUV","noiseU","noiseV","fast"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "file"
        rem_attr_list = ['message','caching','frozen','isHistoricallyInteresting','nodeState','binMembership','uvCoord','uCoord','vCoord','uvFilterSize','uvFilterSizeX','uvFilterSizeY','filter','filterOffset','invert','alphaIsLuminance','colorGain','colorGainR','colorGainG','colorGainB','colorOffset','colorOffsetR','colorOffsetG','colorOffsetB','alphaGain','alphaOffset','defaultColor','defaultColorR','defaultColorG','defaultColorB','outColor','outColorR','outColorG','outColorB','outAlpha','fileTextureName','fileTextureNamePattern','computedFileTextureNamePattern','disableFileLoad','useFrameExtension','frameExtension','frameOffset','useHardwareTextureCycling','startCycleExtension','endCycleExtension','byCycleIncrement','forceSwatchGen','filterType','filterWidth','preFilter','preFilterRadius','useCache','useMaximumRes','uvTilingMode','explicitUvTiles','explicitUvTiles.explicitUvTileName','explicitUvTiles.explicitUvTilePosition','explicitUvTiles.explicitUvTilePositionU','explicitUvTiles.explicitUvTilePositionV','baseExplicitUvTilePosition','baseExplicitUvTilePositionU','baseExplicitUvTilePositionV','uvTileProxyDirty','uvTileProxyGenerate','uvTileProxyQuality','coverage','coverageU','coverageV','translateFrame','translateFrameU','translateFrameV','rotateFrame','doTransform','mirrorU','mirrorV','stagger','wrapU','wrapV','repeatUV','repeatU','repeatV','offset','offsetU','offsetV','rotateUV','noiseUV','noiseU','noiseV','blurPixelation','vertexCameraOne','vertexCameraOneX','vertexCameraOneY','vertexCameraOneZ','vertexCameraTwo','vertexCameraTwoX','vertexCameraTwoY','vertexCameraTwoZ','vertexCameraThree','vertexCameraThreeX','vertexCameraThreeY','vertexCameraThreeZ','vertexUvOne','vertexUvOneU','vertexUvOneV','vertexUvTwo','vertexUvTwoU','vertexUvTwoV','vertexUvThree','vertexUvThreeU','vertexUvThreeV','objectType','rayDepth','primitiveId','pixelCenter','pixelCenterX','pixelCenterY','exposure','hdrMapping','hdrExposure','dirtyPixelRegion','ptexFilterType','ptexFilterWidth','ptexFilterBlur','ptexFilterSharpness','ptexFilterInterpolateLevels','colorProfile','colorSpace','ignoreColorSpaceFileRules','workingSpace','colorManagementEnabled','colorManagementConfigFileEnabled','colorManagementConfigFilePath','outSize','outSizeX','outSizeY','fileHasAlpha','outTransparency','outTransparencyR','outTransparencyG','outTransparencyB','infoBits']
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "gammaCorrect"
        rem_attr_list = ['message','caching','frozen','isHistoricallyInteresting','nodeState','binMembership','value','valueX','valueY','valueZ','gamma','gammaX','gammaY','gammaZ','renderPassMode','outValue','outValueX','outValueY','outValueZ']
        attr_check = ["valueue","gammaX","gammaY","gammaZ","renderPassMode"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "layeredTexture"
        rem_attr_list = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","inputs","inputs.color","inputs.colorR","inputs.colorG","inputs.colorB","inputs.alpha","inputs.blendMode","inputs.isVisible","outColor","outColorR","outColorG","outColorB","outAlpha","hardwareColor","hardwareColorR","hardwareColorG","hardwareColorB","alphaIsLuminance","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB"]
        attr_check = ["alphaIsLuminance","inputs.isVisible","inputs.alpha","inputs.color","inputs.blendMode"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "VRayBlendMtl"
        rem_attr_list = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","swatchAutoUpdate","swatchAlwaysRender","swatchExplicitUpdate","swatchMaxRes","base_material","base_materialR","base_materialG","base_materialB","color","colorR","colorG","colorB","viewportColor","viewportColorR","viewportColorG","viewportColorB","coat_material_0","coat_material_0R","coat_material_0G","coat_material_0B","blend_amount_0","blend_amount_0R","blend_amount_0G","blend_amount_0B","coat_material_1","coat_material_1R","coat_material_1G","coat_material_1B","blend_amount_1","blend_amount_1R","blend_amount_1G","blend_amount_1B","coat_material_2","coat_material_2R","coat_material_2G","coat_material_2B","blend_amount_2","blend_amount_2R","blend_amount_2G","blend_amount_2B","coat_material_3","coat_material_3R","coat_material_3G","coat_material_3B","blend_amount_3","blend_amount_3R","blend_amount_3G","blend_amount_3B","coat_material_4","coat_material_4R","coat_material_4G","coat_material_4B","blend_amount_4","blend_amount_4R","blend_amount_4G","blend_amount_4B","coat_material_5","coat_material_5R","coat_material_5G","coat_material_5B","blend_amount_5","blend_amount_5R","blend_amount_5G","blend_amount_5B","coat_material_6","coat_material_6R","coat_material_6G","coat_material_6B","blend_amount_6","blend_amount_6R","blend_amount_6G","blend_amount_6B","coat_material_7","coat_material_7R","coat_material_7G","coat_material_7B","blend_amount_7","blend_amount_7R","blend_amount_7G","blend_amount_7B","coat_material_8","coat_material_8R","coat_material_8G","coat_material_8B","blend_amount_8","blend_amount_8R","blend_amount_8G","blend_amount_8B","additive_mode","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outApiType","outApiClassification"]
        attr_check = ["base_material","additive_mode","coat_material_0","blend_amount_0","coat_material_1","blend_amount_1","coat_material_2","blend_amount_2","coat_material_3","blend_amount_3","coat_material_4","blend_amount_4","coat_material_5","blend_amount_5","coat_material_6","blend_amount_6","coat_material_7","blend_amount_7","coat_material_8","blend_amount_8"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "displacementShader"
        rem_attr_list = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","displacementMode","displacement","vectorDisplacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","yIsUp","tangent","tangentX","tangentY","tangentZ"]
        attr_check = ["displacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","tangentX","tangentY","tangentZ","nodeState","caching","displacementMode"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        obj_type = "VRayDisplacement"
        rem_attr_list = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishednodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containertype","dagSetMembers","dnSetMembers","memberWireframeColor","annotation","isLayer","verticesOnlySet","edgesOnlySet","facetsOnlySet","editPointsOnlySet","renderableOnlySet","partition","groupNodes","usedBy","displacement","overrideGlobalDisplacement","outApiType","outApiClassification","vraySeparator_vray_displacement","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementtype","vrayDisplacementAmount","vrayDisplacementShift","vrayDisplacementKeepContinuity","vrayEnableWaterLevel","vrayWaterLevel","vrayDisplacementCacheNormals","vray2dDisplacementResolution","vray2dDisplacementPrecision","vray2dDisplacementTightBounds","vray2dDisplacementMultiTile","vray2dDisplacementFilterTexture","vray2dDisplacementFilterBlur","vrayDisplacementUseBounds","vrayDisplacementMinvalueue","vrayDisplacementMinvalueueR","vrayDisplacementMinvalueueG","vrayDisplacementMinvalueueB","vrayDisplacementMaxvalueue","vrayDisplacementMaxvalueueR","vrayDisplacementMaxvalueueG","vrayDisplacementMaxvalueueB","vraySeparator_vray_subquality","vrayOverrideGlobalSubQual","vrayViewDep","vrayEdgeLength","vrayMaxSubdivs"]
        attr_check = ["overrideGlobalDisplacement","displacement","caching","nodeState","blackBox","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementtype","vrayDisplacementAmount","vrayDisplacementShift","vrayEdgeLength","vrayMaxSubdivs","vrayDisplacementUseBounds"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        material_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        materials_overrides_dic = material_overrides.attr_override_detect()

        return(materials_overrides_dic)

    def camera_overrides(objects_check,render_layers):
        camera_overrides_dic = {}
        attr_overrides_dic = camera_overrides_dic
        obj_label = "camera_overide"
        obj_type = "camera"
        rem_attr_list =  ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "hyperLayout", "isCollapsed", "blackBox", "borderConnections", "isHierarchicalConnection", "publishedNodeInfo", "publishedNodeInfo.publishedNode", "publishedNodeInfo.isHierarchicalNode", "publishedNodeInfo.publishednodeType", "rmbCommand", "templateName", "templatePath", "viewName", "iconName", "viewMode", "templateVersion", "uiTreatment", "customTreatment", "creator", "creationDate", "containertype", "boundingBox", "boundingBoxMin", "boundingBoxMinX", "boundingBoxMinY", "boundingBoxMinZ", "boundingBoxMax", "boundingBoxMaxX", "boundingBoxMaxY", "boundingBoxMaxZ", "boundingBoxSize", "boundingBoxSizeX", "boundingBoxSizeY", "boundingBoxSizeZ", "center", "boundingBoxCenterX", "boundingBoxCenterY", "boundingBoxCenterZ", "matrix", "inverseMatrix", "worldMatrix", "worldInverseMatrix", "parentMatrix", "parentInverseMatrix", "visibility", "intermediateObject", "template", "ghosting", "instObjGroups", "instObjGroups.objectGroups", "instObjGroups.objectGroups.objectGrpCompList", "instObjGroups.objectGroups.objectGroupId", "instObjGroups.objectGroups.objectGrpColor", "objectColorRGB", "objectColorR", "objectColorG", "objectColorB", "useObjectColor", "objectColor", "drawOverride", "overrideDisplaytype", "overrideLevelOfDetail", "overrideShading", "overrideTexturing", "overridePlayback", "overrideEnabled", "overrideVisibility", "overrideColor", "lodVisibility", "selectionChildHighlighting", "renderInfo", "identification", "layerRenderable", "layerOverrideColor", "renderLayerInfo", "renderLayerInfo.renderLayerId", "renderLayerInfo.renderLayerRenderable", "renderLayerInfo.renderLayerColor", "ghostingControl", "ghostCustomSteps", "ghostPreSteps", "ghostPostSteps", "ghostStepSize", "ghostFrames", "ghostColorPreA", "ghostColorPre", "ghostColorPreR", "ghostColorPreG", "ghostColorPreB", "ghostColorPostA", "ghostColorPost", "ghostColorPostR", "ghostColorPostG", "ghostColorPostB", "ghostRangeStart", "ghostRangeEnd", "ghostDriver", "hiddenInOutliner", "renderable", "cameraAperture", "horizontalFilmAperture", "verticalFilmAperture", "shakeOverscan", "shakeOverscanEnabled", "filmOffset", "horizontalFilmOffset", "verticalFilmOffset", "shakeEnabled", "shake", "horizontalShake", "verticalShake", "stereoHorizontalImageTranslateEnabled", "stereoHorizontalImageTranslate", "postProjection", "preScale", "filmTranslate", "filmTranslateH", "filmTranslateV", "filmRollControl", "filmRollPivot", "horizontalRollPivot", "verticalRollPivot", "filmRollvalueue", "filmRollOrder", "postScale", "filmFit", "filmFitOffset", "overscan", "panZoomEnabled", "renderPanZoom", "pan", "horizontalPan", "verticalPan", "zoom", "focalLength", "lensSqueezeRatio", "cameraScale", "triggerUpdate", "nearClipPlane", "farClipPlane", "fStop", "focusDistance", "shutterAngle", "centerOfInterest", "orthographicWidth", "imageName", "depthName", "maskName", "tumblePivot", "tumblePivotX", "tumblePivotY", "tumblePivotZ", "usePivotAsLocalSpace", "imagePlane", "homeCommand", "bookmarks", "locatorScale", "displayGateMaskOpacity", "displayGateMask", "displayFilmGate", "displayResolution", "displaySafeAction", "displaySafeTitle", "displayFieldChart", "displayFilmPivot", "displayFilmOrigin", "clippingPlanes", "bestFitClippingPlanes", "depthOfField", "motionBlur", "orthographic", "journalCommand", "image", "depth", "transparencyBasedDepth", "threshold", "depthtype", "useExploreDepthFormat", "mask", "displayGateMaskColor", "displayGateMaskColorR", "displayGateMaskColorG", "displayGateMaskColorB", "backgroundColor", "backgroundColorR", "backgroundColorG", "backgroundColorB", "focusRegionScale", "displayCameraNearClip", "displayCameraFarClip", "displayCameraFrustum", "cameraPrecompTemplate", "vraySeparator_vray_cameraPhysical", "vrayCameraPhysicalOn", "vrayCameraPhysicaltype", "vrayCameraPhysicalFilmWidth", "vrayCameraPhysicalFocalLength", "vrayCameraPhysicalSpecifyFOV", "vrayCameraPhysicalFOV", "vrayCameraPhysicalZoomFactor", "vrayCameraPhysicalDistortiontype", "vrayCameraPhysicalDistortion", "vrayCameraPhysicalLensFile", "vrayCameraPhysicalDistortionMap", "vrayCameraPhysicalDistortionMapR", "vrayCameraPhysicalDistortionMapG", "vrayCameraPhysicalDistortionMapB", "vrayCameraPhysicalFNumber", "vrayCameraPhysicalHorizLensShift", "vrayCameraPhysicalLensShift", "vrayCameraPhysicalLensAutoVShift", "vrayCameraPhysicalShutterSpeed", "vrayCameraPhysicalShutterAngle", "vrayCameraPhysicalShutterOffset", "vrayCameraPhysicalLatency", "vrayCameraPhysicalISO", "vrayCameraPhysicalSpecifyFocus", "vrayCameraPhysicalFocusDistance", "vrayCameraPhysicalExposure", "vrayCameraPhysicalWhiteBalance", "vrayCameraPhysicalWhiteBalanceR", "vrayCameraPhysicalWhiteBalanceG", "vrayCameraPhysicalWhiteBalanceB", "vrayCameraPhysicalVignetting", "vrayCameraPhysicalVignettingAmount", "vrayCameraPhysicalBladesEnable", "vrayCameraPhysicalBladesNum", "vrayCameraPhysicalBladesRotation", "vrayCameraPhysicalCenterBias", "vrayCameraPhysicalAnisotropy", "vrayCameraPhysicalUseDof", "vrayCameraPhysicalUseMoBlur", "vrayCameraPhysicalApertureMap", "vrayCameraPhysicalApertureMapR", "vrayCameraPhysicalApertureMapG", "vrayCameraPhysicalApertureMapB", "vrayCameraPhysicalApertureMapAffectsExposure", "vrayCameraPhysicalOpticalVignetting", "vraySeparator_vray_camera_overridesverrides", "vraycamera_overridesverridesOn", "vrayCameratype", "vraycamera_overridesverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve",]
        attr_check = ["vraySeparator_vray_cameraPhysical","vrayCameraPhysicalOn","vrayCameraPhysicaltype","vrayCameraPhysicalFilmWidth","vrayCameraPhysicalFocalLength","vrayCameraPhysicalSpecifyFOV","vrayCameraPhysicalFOV","vrayCameraPhysicalZoomFactor","vrayCameraPhysicalDistortiontype","vrayCameraPhysicalDistortion","vrayCameraPhysicalLensFile","vrayCameraPhysicalDistortionMap","vrayCameraPhysicalDistortionMapR",
        "vrayCameraPhysicalDistortionMapG","vrayCameraPhysicalDistortionMapB","vrayCameraPhysicalFNumber","vrayCameraPhysicalHorizLensShift","vrayCameraPhysicalLensShift","vrayCameraPhysicalLensAutoVShift","vrayCameraPhysicalShutterSpeed","vrayCameraPhysicalShutterAngle","vrayCameraPhysicalShutterOffset","vrayCameraPhysicalLatency","vrayCameraPhysicalISO","vrayCameraPhysicalSpecifyFocus","vrayCameraPhysicalFocusDistance",
        "vrayCameraPhysicalExposure","vrayCameraPhysicalWhiteBalance","vrayCameraPhysicalWhiteBalanceR","vrayCameraPhysicalWhiteBalanceG","vrayCameraPhysicalWhiteBalanceB","vrayCameraPhysicalVignetting","vrayCameraPhysicalVignettingAmount","vrayCameraPhysicalBladesEnable","vrayCameraPhysicalBladesNum","vrayCameraPhysicalBladesRotation","vrayCameraPhysicalCenterBias","vrayCameraPhysicalAnisotropy","vrayCameraPhysicalUseDof","vrayCameraPhysicalUseMoBlur"
        ,"vrayCameraPhysicalApertureMap","vrayCameraPhysicalApertureMapR","vrayCameraPhysicalApertureMapG","vrayCameraPhysicalApertureMapB","vrayCameraPhysicalApertureMapAffectsExposure","vrayCameraPhysicalOpticalVignetting","vraySeparator_vray_camera_overridesverrides","vraycamera_overridesverridesOn","vrayCameratype", "vraycamera_overridesverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve","renderable"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        camera_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        camera_overrides_dic = camera_overrides.attr_override_detect()

        return(camera_overrides_dic)

    def light_overrides(objects_check,render_layers):
        light_overrides_dic = {}
        attr_overrides_dic = light_overrides_dic
        obj_label = "light_overide"
        obj_type = "VRayLightRectShape"
        rem_attr_list = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishednodeType"
        ,"rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containertype","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY",
        "boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template"
        ,"ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","useObjectColor","objectColor","drawOverride",
        "overrideDisplaytype","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","overrideColor","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo"
        ,"renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB"
        ,"ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","rendertype","renderVolume","visibleFraction","motionBlur","visibleInReflections","visibleInRefractions","castsShadows","receiveShadows"
        ,"maxVisibilitySamplesOverride","maxVisibilitySamples","geometryAntialiasingOverride","antialiasingLevel","shadingSamplesOverride","shadingSamples","maxShadingSamples","volumeSamplesOverride","volumeSamples","depthJitter","ignoreSelfShadowing","primaryVisibility","referenceObject","compInstObjGroups"
        ,"compInstObjGroups.compObjectGroups","compInstObjGroups.compObjectGroups.compObjectGrpCompList","compInstObjGroups.compObjectGroups.compObjectGroupId","underWorldObject","localPosition","localPositionX","localPositionY","localPositionZ","worldPosition","worldPosition.worldPositionX","worldPosition.worldPositionY"
        ,"worldPosition.worldPositionZ","localScale","localScaleX","localScaleY","localScaleZ","units","colorMode","shapetype","directionalPreview","showTex","targetDist","targetPos","targetPosX","targetPosY","targetPosZ","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity",
        "lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","enabled","lightColor","colorR","colorG","colorB","temperature","uSize","vSize","shadows","shadowColor","shadowColorR","shadowColorG","shadowColorB","intensityMult"
        ,"directional","directionalPreviewLength","doubleSided","invisible","affectDiffuse","affectSpecular","affectReflections","ignoreLightNormals","noDecay","skylightPortal","simpleSkylightPortal","storeWithIrradianceMap","rectTex","rectTexR","rectTexG","rectTexB","rectTexA","useRectTex","multiplyByTheLightColor","texResolution"
        ,"texAdaptive","subdivs","shadowBias","cutoffThreshold","locatorScale","photonSubdivs","causticsSubdivs","diffuseMult","causticMult","diffuseContrib","specularContrib","useMIS","vrayOverrideMBSamples","vrayMBSamples","outA","outAX","outAY","outAZ","outApiType","outApiClassification","outTemperatureColor","outTemperatureColorR"
        ,"outTemperatureColorG","outTemperatureColorB","emitDiffuse","emitSpecular","decayRate","attributeAliasList","pickTexture"]
        attr_check = ["lightColor","intensityMult","shapetype","uSize","vSize","directional","useRectTex","rectTex","noDecay","doubleSided","invisible","skylightPortal","simpleSkylightPortal","affectDiffuse","affectSpecular","affectReflections","shadows","shadowColor","shadowBias","visibility","colorR","colorG","colorB","emitDiffuse","emitSpecular",
        "decayRate","attributeAliasList","diffuseContrib","specularContrib","enabled"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        light_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        light_overrides_dic = light_overrides.attr_override_detect()

        obj_type = "spotLight"
        rem_attr_list = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishednodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containertype","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplaytype","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","coneAngle","penumbraAngle","dropoff","barnDoors","leftBarnDoor","rightBarnDoor","topBarnDoor","bottomBarnDoor","useDecayRegions","startDistance1","endDistance1","startDistance2","endDistance2","startDistance3","endDistance3","fogSpread","fogIntensity","object_type","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","rayDirection","rayDirectionX","rayDirectionY","rayDirectionZ","fogGeometry","lightGlow","psIllumSamples"]
        attr_check = ["color","intensity","emitDiffuse","emitSpecular","decayRate","coneAngle","penumbraAngle","dropoff","shadowColor","useRayTraceShadows","lightRadius","shadowRays","rayDepthLimit","useDepthMapShadows","dmapResolution","useMidDistDmap","useDmapAutoFocus","dmapFocus","dmapFilterSize","dmapBias","fogShadowIntensity","volumeShadowSamples"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        light_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        light_overrides_dic = light_overrides.attr_override_detect()

        obj_type = "ambientLight"
        rem_attr_list = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishednodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containertype","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplaytype","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","ambientShade","object_type","shadowRadius","castSoftShadows","normalCamera","normalCameraX","normalCameraY","normalCameraZ","receiveShadows"]
        attr_check = ["color","intensity","ambientShade"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        light_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        light_overrides_dic = light_overrides.attr_override_detect()

        obj_type = "directionalLight"
        rem_attr_list = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishednodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containertype","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplaytype","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","useLightPosition","object_type","lightAngle","pointWorld","pointWorldX","pointWorldY","pointWorldZ"]
        attr_check = ["color","intensity","emitDiffuse","emitSpecular"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        light_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        light_overrides_dic = light_overrides.attr_override_detect()

        obj_type = "pointLight"
        rem_attr_list = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishednodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containertype","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplaytype","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","fogGeometry","fogRadius","lightGlow","object_type","fogtype","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","fogIntensity"]
        attr_check = ["color","intensity","emitDiffuse","emitSpecular","decayRate"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        light_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        light_overrides_dic = light_overrides.attr_override_detect()

        return(light_overrides_dic)

    def vraySettings_overrides(objects_check,render_layers):
        vray_settings_overrides_dic = {}
        attr_overrides_dic = vray_settings_overrides_dic
        obj_label = "vs"
        cmds.loadPlugin('vrayformaya', quiet=True)
        cmds.pluginInfo('vrayformaya', edit=True, autoload=True)
        cmds.setAttr("defaultRenderGlobals.ren", "vray", type = "string")

        obj_type = "VRaySettingsNode"
        rem_attr_list =  cmds.listAttr("vraySettings")
        attr_check = ["cam_envtexBg","cam_envtexGi","cam_envtexReflect","cam_envtexRefract","cam_envtexSecondaryMatte","globopt_geom_displacement","globopt_light_doLights","globopt_light_doHiddenLights","globopt_light_doDefaultLights",
        "globopt_light_doShadows","globopt_light_ignoreLightLinking","globopt_light_disableSelfIllumination","photometricScale","globopt_mtl_reflectionRefraction","globopt_mtl_glossy","globopt_mtl_transpMaxLevels","globopt_mtl_transpCutoff"
        ,"globopt_mtl_doMaps","globopt_mtl_filterMaps","bumpMultiplier","texFilterScaleMultiplier","globopt_ray_bias","globopt_ray_maxIntens_on","gi_texFilteringMultiplier","cam_overrideEnvtex","cam_overrideEnvtexSecondaryMatte",
        "ddisplac_amount","ddisplac_edgeLength","ddisplac_maxSubdivs","giOn","reflectiveCaustics","refractiveCaustics","secondaryMultiplier","secondaryEngine","saturation","contrast","contrastBase","aoOn","aoAmount","aoRadius","aoSubdivs",
        "giRayDistOn","giRayDist","causticsOn","causticsMultiplier","causticsSearchDistance","causticsMaxPhotons","causticsMaxDensity","minShadeRate"]
        for attr in attr_check:
            rem_attr_list.remove(attr)
        vraySettings_overrides = ATTR_OVERRIDES_CLASS(render_layers,obj_type,rem_attr_list,attr_overrides_dic,obj_label,objects_check)
        vray_settings_overrides_dic = vraySettings_overrides.attr_override_detect()

        return(vray_settings_overrides_dic)

    def objects_in_render_layer(objects_check,renderLayer):
        objects_in_layer_dic = {}
        for rl in render_layers:
            objects_in_layer = cmds.editRenderLayerMembers(rl, query = True) or []
            for obj in objects_check:
                for obs in objects_in_layer:
                    if obj == obs:
                        objects_in_layer_string = obj + "_" + rl
                        objects_in_layer_dic[objects_in_layer_string] = rl

        return(objects_in_layer_dic)

    def render_stat_overrides(objects_check_g, render_layers):
        Render_stat_overrides_dic = {}
        exclude_list = ["camera","ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight","VRayLightSphereShape","VRayLightRectShape","VRayLightDomeShape","VRayLightIESShape"]
        siz = len(objects_check_g)
        l = 0
        while l < siz:
            for object in objects_check_g:
                object_T = cmds.objecttype(object)
                for exclude in exclude_list:
                    if exclude == object_T:
                        objects_check_g.remove(object)
            l = l + 1
        for object in objects_check_g:
            obj_type = cmds.object_type(object)
            if obj_type != "locator":
                Render_Stat_List = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions","doubleSided"]
                for rsl in Render_Stat_List:
                    attr_string = object + "." + rsl
                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                    default_valueueue = cmds.getAttr(attr_string)
                    for rl in render_layers:
                        if rl != "defaultRenderLayer":
                            cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                            layer_valueue = cmds.getAttr(attr_string)
                            if layer_valueue != default_valueueue:
                                dic_string = object + "**" + "render_stats" + "**" +  rsl + "**" + rl
                                Render_stat_overrides_dic[dic_string] = layer_valueue
            return(Render_stat_overrides_dic)

    def vrayObjectProp_overrides(render_layers):
        Vray_object_props = cmds.ls(type = "VRayObjectProperties")
        vray_object_property_overrides_dic = {}
        Object_Props = ["overrideMBSamples","mbSamples","objectIDEnabled","objectID","skipExportEnabled","skipExport","ignore",
        "useIrradianceMap","generateGI","generateGIMultiplier","receiveGI","receiveGIMultiplier","giSubdivsMultiplier","giSubdivsMultiplier","generateCaustics",
        "receiveCaustics","causticsMultiplier","giVisibility","primaryVisibility","reflectionVisibility","refractionVisibility","shadowVisibility","receiveShadows","matteSurface",
        "alphaContribution","generateRenderElements","shadows","affectAlpha","shadowTintColor","shadowBrightness","reflectionAmount","refractionAmount","giAmount","noGIOnOtherMattes",
        "matteForSecondaryRays","giSurfaceID","useReflectionExclude","reflectionListIsInclusive","useRefractionExclude","refractionListIsInclusive","blackBox",
        "rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containertype"]
        for vop in Vray_object_props:
            for op in Object_Props:
                cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
                valueue_string = vop + "." + op
                default_valueue = cmds.getAttr(valueue_string)
                for rl in render_layers:
                    if rl != "defaultRenderLayer":
                        cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                        override_valueue = cmds.getAttr(valueue_string)
                        if override_valueue != default_valueue:
                            dic_string = vop + "**" + "vrayObjProp" + "**" + op + "**" + rl
                            vray_object_property_overrides_dic[dic_string] = override_valueue
        return(vray_object_property_overrides_dic)

    vray_settings_overrides_dic = {}
    transform_layer_overrides = {}
    mat_assignment_layer_overides = {}
    materials_overrides_dic = {}
    camera_overrides_dic = {}
    light_overrides_dic = {}
    Render_Stats_Overides = {}
    vray_object_property_overrides = {}

    vray_settings_overrides_dic = vraySettings_overrides(objects_check,render_layers)
    OBJ_1_translations = translations(objects_check, render_layers)
    transform_layer_overrides = OBJ_1_translations[5]
    OBJ_1_materialsAssignments = material_assignments(objects_check, render_layers)
    matAssignmentLayOverides = OBJ_1_materialsAssignments[4]
    materials_overrides_dic = material_overrides(objects_check,render_layers)
    materials_overrides_dic.update(matAssignmentLayOverides)
    camera_overrides_dic = camera_overrides(objects_check,render_layers)
    light_overrides_dic = light_overrides(objects_check,render_layers)
    OBJ_1_Render_Stats = render_stat_overrides(objects_check_g, render_layers)
    Render_Stats_Overides = OBJ_1_Render_Stats
    OBJ_1_Vray_object_props = vrayObjectProp_overrides(render_layers)
    vray_object_property_overrides = OBJ_1_Vray_object_props

    return(vray_settings_overrides_dic,transform_layer_overrides,materials_overrides_dic,light_overrides_dic,Render_Stats_Overides,vray_object_property_overrides,camera_overrides_dic)


#--- overide section over ----

def analize_cameras():
    render_cam_dic = {}
    render_layers = cmds.ls(type = "renderLayer")
    camera_list = cmds.ls(type = "camera")
    camera_list.append("none")
    camera_list_on = []

    for rl in render_layers:
        cmds.editRenderLayerGlobals(currentRenderLayer = rl)
        for camm in camera_list:
            if camm != "none":
                name = camm + ".renderable"
                state = cmds.getAttr(name)
                if state == 1:
                    camera_list_on.append(camm)
                    render_cam_dicSTR = rl + "_" + camm
                    render_cam_dic[render_cam_dicSTR] = (camm + "_" + rl)
    return(render_cam_dic,camera_list)

def set_render_camera(rl,camera_list,renCamMenu,render_layers,*args):
    global initial_layer
    layer_split = renCamMenu.split("|")
    lay = layer_split[2]
    cmds.editRenderLayerGlobals(currentRenderLayer = lay)
    menu_valueue = cmds.optionMenu(renCamMenu,v = True, query = True)
    render_cam_string = menu_valueue + ".renderable"
    camera_state_dic = {}
    camera_list_modifed = cmds.ls(type = "camera")
    camera_list_modifed.append("perspShape")
    camera_list_modifed.append("topShape")
    camera_list_modifed.append("frontShape")
    camera_list_modifed.append("sideShape")
    for rll in render_layers:
        cmds.editRenderLayerGlobals(currentRenderLayer = rll)
        for camm in camera_list_modifed:
            render_state = cmds.getAttr(camm + ".renderable")
            curent_layer = cmds.editRenderLayerGlobals(currentRenderLayer = True,query = True)
            if render_state == 1:
                camera_state_dic[(camm + "&" + rll)] = render_state
    cmds.editRenderLayerGlobals(currentRenderLayer = lay)
    set_camera = "none"
    if lay == "defaultRenderLayer":
        for cam in camera_list_modifed:
            if cam == menu_valueue:
                cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                cmds.setAttr((cam + ".renderable"),1)
                set_camera = cam
            else:
                cmds.setAttr(cam + ".renderable",0)
    if lay != "defaultRenderLayer":
        cmds.editRenderLayerGlobals(currentRenderLayer = lay)
        for cam in camera_list_modifed:
            if cam == menu_valueue:
                cmds.editRenderLayerAdjustment(cam + ".renderable")
                cmds.setAttr((cam + ".renderable"),1)
                set_camera = cam
    cmds.editRenderLayerGlobals( currentRenderLayer = initial_layer)
    camColorCheck(renCamMenu,set_camera)

def fix_camera_names(*args):
    global initial_layer
    intialLayer = cmds.editRenderLayerGlobals(currentRenderLayer = True, query = True)
    render_layers = cmds.ls(type = "renderLayer")
    camera_list_modifed = cmds.ls(type = "camera")
    camera_list_modifed.append("perspShape")
    camera_list_modifed.append("topShape")
    camera_list_modifed.append("frontShape")
    camera_list_modifed.append("sideShape")
    for rll in render_layers:
        if rll == "defaultRenderLayer":
            cmds.editRenderLayerGlobals(currentRenderLayer = rll)
            for cam in camera_list_modifed:
                if cam == "perspShape":
                    cmds.setAttr(cam + ".renderable",1)
        if rll != "defaultRenderLayer":
            cmds.editRenderLayerGlobals(currentRenderLayer = rll)
            for cam in camera_list_modifed:
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
                if camera_layer_compare == rll or (camera_layer_compareSPb + "_BTY") == rll or (camera_layer_compareSPb + "_REF") == rll or (camera_layer_compareSPb + "_SHD") == rll or (camera_layer_compareSPb + "_REF_MATTE") == rll or ("BTY_" + camera_layer_compareSPb) == rll:
                    cmds.editRenderLayerAdjustment(cam + ".renderable")
                    cmds.setAttr(cam + ".renderable",1)
                else:
                    cmds.editRenderLayerAdjustment(cam + ".renderable")
                    cmds.setAttr(cam + ".renderable",0)
    cmds.editRenderLayerGlobals(currentRenderLayer = initial_layer)
    layer_switcher()


def camColorCheck(renCamMenu,set_camera):
    render_camera_split = renCamMenu.split("|")
    layer_label = render_camera_split[2]
    cam = set_camera
    camNum = 1
    var = 4
    if "FtTp" in cam  or "FtRt" in cam or "FtLt" in cam or "FtLtTp" in cam or "FtRtTp" in cam or "Ft" in cam or "Bk" in cam or "Rt" in cam or "Lt" in cam or "Tp" in cam or "Bt" in cam:
        var = 0
    if "C1N1" in cam or "C1N1Shape" in cam or "C7N1" in cam or "C7N1Shape" in cam or "C2N1" in cam or "C2N1Shape" in cam  or "C8N1" in cam  or "C8N1Shape" in cam  or "C3N1" in cam or "C3N1Shape" in cam  or "C9N1" in cam  or "C9N1Shape" in cam or "C1C1" in cam or "C1C1Shape" in cam or "C1L1" in cam  or "C1L1Shape" in cam or "C1R1" in cam or "C1R1Shape" in cam or "C1N2" in cam or "C1NShape2" in cam or "C1N2Shape" in cam or "C1N4" in cam or "C1NShape4" in cam or "C1N4Shape" in cam:
        var = 1
    if "C1N1Shape1" in cam or "C7N1Shape1" in cam or "C2N1Shape1" in cam or "C8N1Shape1" in cam or "C3N1Shape1" in cam or "C9N1Shape1" in cam or "C1C1Shape1" in cam or "C1L1Shape1" in cam or "C1R1Shape1" in cam or "C1N2Shape1" in cam or "C1N4Shape1" in cam:
        var = 2
    if "C1NShape1" in cam or "C7NShape1" in cam or "C2NShape1" in cam or "C8NShape1" in cam or "C3NShape1" in cam or "C9NShape1" in cam or "C1CShape1" in cam or "C1LShape1" in cam or "C1RShape1" in cam or "C1NShape1" in cam or "C1NShape1" in cam:
        var = 3
    cam_reg_ex_A = ""
    if layer_label != "defaultRenderLayer":
        if var == 0:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camera_reg_ex_split = set_camera.split("Shape")
                cam_reg_ex_A = camera_reg_ex_split[0]
                cam_reg_ex_A_split = cam_reg_ex_A.split("_")
                cam_reg_ex_A = cam_reg_ex_A_split[0]
            else:
                cam_reg_ex_A = cam
        if var == 1:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camera_reg_ex_split = set_camera.split("Shape")
                cam_reg_ex_A = camera_reg_ex_split[0] + camera_reg_ex_split[1]
                cam_reg_ex_A_split = cam_reg_ex_A.split("_")
                cam_reg_ex_A = cam_reg_ex_A_split[1]
            else:
                cam_reg_ex_A = cam
        if var == 2:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camRegEx = cam + "_"
                camera_reg_ex_split = camRegEx.split("_")
                camRegEx = camera_reg_ex_split[1]
                camRegEx = camRegEx.split("Shape")
                cam_reg_ex_A = camRegEx[0]
            else:
                cam_reg_ex_A = cam
        if var == 3:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camera_reg_ex_split = set_camera.split("Shape")
                cam_reg_ex_A = camera_reg_ex_split[0] + camera_reg_ex_split[1]
                cam_reg_ex_A_split = cam_reg_ex_A.split("_")
                cam_reg_ex_A = cam_reg_ex_A_split[1]
            else:
                cam_reg_ex_A = cam
        if var == 4:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camera_reg_ex_split = set_camera.split("Shape")
                cam_reg_ex_A = camera_reg_ex_split[0]
            else:
                cam_reg_ex_A = cam
        if layer_label != "defaultRenderLayer":
            if camNum > 1:
                cmds.optionMenu(renCamMenu, v = cam, bgc = (1,.0,0),edit = True)
            if camNum == 1 and layer_label == (cam_reg_ex_A) or layer_label == (cam_reg_ex_A + "_BTY") or layer_label == (cam_reg_ex_A + "_REF") or layer_label == (cam_reg_ex_A + "_SHD") or layer_label == (cam_reg_ex_A + "_REF_MATTE") or layer_label == ("BTY_" + cam_reg_ex_A):
                cmds.optionMenu(renCamMenu, v = cam, bgc = (.5,.5,.5),edit = True)
            else:
                cmds.optionMenu(renCamMenu, v = cam , bgc = (1,0,0),edit = True)
        else:
            cmds.optionMenu(renCamMenu, v = cam, bgc = (.5,.5,.5),edit = True)

def unlock_nodes(*args):
    cams = cmds.ls(type = "camera")
    for cam in cams:
        parentNode = cmds.listRelatives(cam, parent = True)
        p_lock_state = cmds.lockNode(parentNode[0],lock = True, query = True)
        p_lock_state = p_lock_state[0]
        if p_lock_state == 1:
            cmds.lockNode(parentNode[0], lock = 0)
        if "Shape" in cam:
            dad = cmds.listRelatives(cam, parent = True)
            dad = dad[0]
        else:
            dad = cam
        cmds.lockNode(cam, lock = 0)
        visibility_exists = cmds.attributeQuery("visibility", node = cam, exists = True)
        renderable_exists = cmds.attributeQuery("renderable", node = cam, exists = True)
        if visibility_exists == 1:
            cmds.setAttr(dad + ".visibility", lock = 0)
        cmds.setAttr(dad + ".renderable", lock = 0)

def copy_all_layers(render_layers,*args):
    copy_all_layer = "B"
    copy_layers(render_layers,copy_all_layer)

def copy_layers(render_layers,copy_all_layer,*args):
    active_layers = []
    unlock_nodes()
    panels = cmds.getPanel( type = "modelPanel" )
    for m_panel in panels:
        cmds.modelEditor(m_panel, edit = True, allObjects = 0)
    initial_layer = cmds.editRenderLayerGlobals(query = True, currentRenderLayer = True)
    start_layer = initial_layer
    if copy_all_layer == "A":
        active_layers.append(start_layer)
    if copy_all_layer == "B":
        active_layers = render_layers
    objects_check_cl_g = cmds.ls(g = True)
    objects_check_cl_t = cmds.ls(type = "transform")
    objects_check_cl_cam = cmds.ls(type = "camera")
    objects_check_cl = objects_check_g + objects_check_t + objects_check_cam
    light_types = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
    overides = overide_info_function(render_layers)
    Vray_object_props = cmds.ls(type = "VRayObjectProperties")
    render_stats = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions"]
    vraySettings = cmds.listAttr("vraySettings")
    vraySettings_overrides =  overides[0] or []
    transform_overrides = overides[1] or []
    material_overrides = overides[2] or []
    camera_overrides = overides[6] or []
    light_overrides = overides[3] or []
    render_stat_overrides = overides[4] or []
    vray_object_prop_overrides = overides[5] or []
    for rlll in active_layers:
        if rlll != "defaultRenderLayer":
            objects_in_layer = cmds.editRenderLayerMembers( rlll, fn = True,query=True ) or []
            objects_visibility_dic = {}
            for obCL in objects_check_cl:
                visibility_exists = cmds.attributeQuery("visibility",node = obCL,exists = True)
                if visibility_exists == 1:
                    cmds.editRenderLayerGlobals(currentRenderLayer = rlll)
                    visibility_string = (obCL + ".visibility")
                    visibility_state = cmds.getAttr(visibility_string)
                    string_key = (obCL + "%" + str(visibility_state))
                    objects_visibility_dic[string_key] = visibility_state
            cmds.createRenderLayer(objects_in_layer, name = (rlll + "_copy"))
            cmds.editRenderLayerGlobals(currentRenderLayer = (rlll + "_copy"))
            cmds.rename(rlll,("**_" + rlll + "_old"))
            cmds.rename((rlll + "_copy"),rlll)
            cmds.delete(("**_" + rlll + "_old"))
            for objL in objects_in_layer:
                cmds.editRenderLayerMembers((rlll),objL)
            for ob in objects_check:
                for obvd in objects_visibility_dic:
                     obvd_split = obvd.split("%")
                     if obvd_split[0] == ob:
                         if obvd_split[1] == "True":
                            ste = 1
                         if obvd_split[1] == "False":
                            ste = 0
                         nodeTY = cmds.nodeType(obvd_split[0])
                         if nodeTY != "camera":
                             lock_state = cmds.lockNode(obvd_split[0],lock = True, query = True)
                             lock_state = lock_state[0]
                             if lock_state == 0:
                                 cmds.setAttr((obvd_split[0] + ".visibility"),ste)
            for tfo in transform_overrides:
                transform_overrides_split = tfo.split("$")
                layer = transform_overrides_split[2]
                for ob in objects_check:
                    if ob == transform_overrides_split[1]:
                        if layer == rlll:
                            value = transform_overrides[tfo]
                            if "translate" in transform_overrides_split[3]:
                                cmds.editRenderLayerAdjustment(ob + ".translate")
                                cmds.setAttr((ob + "." + transform_overrides_split[3]),value)
                            if "rotate" in transform_overrides_split[3]:
                                cmds.editRenderLayerAdjustment(ob + ".rotate")
                                cmds.setAttr((ob + "." + transform_overrides_split[3]),value)
                            if "scale" in transform_overrides_split[3]:
                                cmds.editRenderLayerAdjustment(ob + ".scale")
                                cmds.setAttr((ob + "." + transform_overrides_split[3]),value)
            for lo in light_overrides:
                ramp_removed_found = 0
                if "rampRemoved" in lo or "rampMismatch" in lo:
                    ramp_removed_found = 1
                light_override_original = lo
                light_override_original_split = lo.split("**")
                lo = light_override_original_split[0]
                layer = light_override_original_split[1]
                layer = layer[:-1]
                light_override_original_split = lo.split("*")
                lo = light_override_original_split[1]
                light_override_object_split = lo.split(".")
                for ob in objects_check:
                    if "spotLight" in ob or "ambientLight" in ob or "directionalLight" in ob or "pointLight" in ob:
                        kid = cmds.listRelatives(ob,children = True)
                        ob = kid[0]
                    if ob == light_override_object_split[0]:
                        if layer == rlll:
                            value = light_overrides[light_override_original]
                            type = type(value)
                            kind_list = type(value) is list
                            kind_int = type(value) is int
                            kind_float = type(value) is float
                            kind_bool = type(value) is bool
                            kind_uni = type(value) is unicode
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
                            if kind_uni == 1:
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
                if "mtlOveride_overide" in mo:
                    ramp_removed_found = 0
                    if "rampRemoved" in mo:
                        ramp_removed_found = 1
                    material_override_original = mo
                    material_override_split = mo.split("**")
                    layer = material_override_split[1]
                    layer = layer[:-1]
                    material_override_SPLIT = mo.split("*")
                    mo = material_override_SPLIT[1]
                    material_override_object_split = mo.split(".")
                    for mats in materials:
                        if mats == material_override_object_split[0]:
                            if layer == rlll:
                                value = material_overrides[material_override_original]
                                type = type(value)
                                kind_list = type(value) is list
                                kind_int = type(value) is int
                                kind_float = type(value) is float
                                kind_bool = type(value) is bool
                                kind_uni = type(value) is unicode
                                if kind_list == 1:
                                    value_sub = value[0]
                                    value_a = value_sub[0]
                                    value_b = value_sub[1]
                                    value_c = value_sub[2]
                                    cmds.editRenderLayerAdjustment(mo)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(material_override_SPLIT[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    cmds.setAttr(material_override_SPLIT[1],value_a,value_b,value_c)
                                if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                    cmds.editRenderLayerAdjustment(mo,layer = rlll)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(material_override_SPLIT[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    cmds.setAttr(material_override_SPLIT[1],value)
                                if kind_uni == 1:
                                    cmds.editRenderLayerAdjustment(mo)
                                    if ramp_removed_found == 1:
                                        a = 1
                                        destination_connections = cmds.listConnections(material_override_SPLIT[1], destination = False, plugs = True, connections = True) or []
                                        destination_connections_size = len(destination_connections)
                                        while a < destination_connections_size:
                                            cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                            a = a + 1
                                    cmds.connectAttr((value + ".outColor"),mo,force = True)
                if "materialAssignment" in mo:
                    material_override_original = mo
                    material_override_SPLIT = mo.split("$")
                    layer = material_override_SPLIT[1]
                    mo = material_override_SPLIT[2]
                    material_assignment_override = material_override_SPLIT[0]
                    for mats in materials:
                        if mats == material_override_SPLIT[0]:
                            if layer == rlll:
                                value = material_overrides[material_override_original]
                                type = type(value)
                                cmds.select(material_assignment_override)
                                cmds.hyperShade(assign = value)
            for rs in render_stat_overrides:
                render_stat_original = rs
                render_stat_split = rs.split("**")
                layer = render_stat_split[3]
                rs = render_stat_split[0]
                render_stat_b = render_stat_split[2]
                render_stat_attr = render_stat_b
                rs = rs + "." + render_stat_b
                for rS in render_stats:
                    if render_stat_attr == rS:
                        if layer == rlll:
                            value = render_stat_overrides[render_stat_original]
                            type = type(value)
                            kind_list = type(value) is list
                            kind_int = type(value) is int
                            kind_float = type(value) is float
                            kind_bool = type(value) is bool
                            kind_uni = type(value) is unicode
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
                            if kind_uni == 1:
                                cmds.editRenderLayerAdjustment(rs)
                                cmds.connectAttr((value + ".outColor"),rs,force = True)
            for vrp in vray_object_prop_overrides:
                vray_object_prop_original = vrp
                vray_object_prop_split = vrp.split("**")
                layer = vray_object_prop_split[3]
                vrp = vray_object_prop_split[0]
                vray_object_prop_full = vrp + "." + vray_object_prop_split[2]
                for vrp_b in Vray_object_props:
                    if vrp == vrp_b:
                        if layer == rlll:
                            value = vray_object_prop_overrides[vray_object_prop_original]
                            type = type(value)
                            kind_list = type(value) is list
                            kind_int = type(value) is int
                            kind_float = type(value) is float
                            kind_bool = type(value) is bool
                            kind_uni = type(value) is unicode
                            if kind_list == 1:
                                value_sub = value[0]
                                value_a = value_sub[0]
                                value_b = value_sub[1]
                                value_c = value_sub[2]
                                cmds.editRenderLayerAdjustment(vray_object_prop_full)
                                cmds.setAttr(vray_object_prop_full,value_a,value_b,value_c)
                            if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                cmds.editRenderLayerAdjustment(vray_object_prop_full)
                                cmds.setAttr(vray_object_prop_full,value)
                            if kind_uni == 1:
                                cmds.editRenderLayerAdjustment(vray_object_prop_full)
                                cmds.connectAttr((value + ".outColor"),vray_object_prop_full,force = True)
            for vrs in vraySettings_overrides:
                ramp_removed_found = 0
                if "rampRemoved" in vrs:
                    ramp_removed_found = 1
                vraySettings_stat_original = vrs
                vraySettings_stat_split = vrs.split("**")
                vrs = vraySettings_stat_split[0]
                layer = vraySettings_stat_split[1]
                layer = layer[:-1]
                vraySettings_stat_split = vrs.split("*")
                vrs = vraySettings_stat_split[1]
                vrsFull = vrs
                for vrender_stat_b in vraySettings:
                    vrender_stat_b = "vraySettings." + vrender_stat_b
                    if vrs == vrender_stat_b:
                        if layer == rlll:
                            value = vraySettings_overrides[vraySettings_stat_original]
                            type = type(value)
                            kind_list = type(value) is list
                            kind_int = type(value) is int
                            kind_float = type(value) is float
                            kind_bool = type(value) is bool
                            kind_uni = type(value) is unicode
                            if kind_list == 1:
                                value_sub = value[0]
                                value_a = value_sub[0]
                                value_b = value_sub[1]
                                value_c = value_sub[2]
                                cmds.editRenderLayerAdjustment(vrsFull)
                                if ramp_removed_found == 1:
                                    a = 1
                                    destination_connections = cmds.listConnections(vraySettings_stat_split[1], destination = False, plugs = True, connections = True) or []
                                    destination_connections_size = len(destination_connections)
                                    while a < destination_connections_size:
                                        cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                        a = a + 1
                                cmds.setAttr(vrsFull,value_a,value_b,value_c)
                            if kind_float == 1 or kind_int == 1 or kind_bool == 1:
                                cmds.editRenderLayerAdjustment(vrsFull)
                                if ramp_removed_found == 1:
                                    a = 1
                                    destination_connections = cmds.listConnections(vraySettings_stat_split[1], destination = False, plugs = True, connections = True) or []
                                    destination_connections_size = len(destination_connections)
                                    while a < destination_connections_size:
                                        cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                        a = a + 1
                                cmds.setAttr(vrsFull,value)
                            if kind_uni == 1:
                                cmds.editRenderLayerAdjustment(vrsFull)
                                if ramp_removed_found == 1:
                                    a = 1
                                    destination_connections = cmds.listConnections(vraySettings_stat_split[1], destination = False, plugs = True, connections = True) or []
                                    destination_connections_size = len(destination_connections)
                                    while a < destination_connections_size:
                                        cmds.disconnectAttr(destination_connections[1],destination_connections[0])
                                        a = a + 1
                                cmds.connectAttr((value + ".outColor"),vrsFull, force = True)
            print ' '
            print '*** rebuilt layer ', rlll
            print ' '
        cmds.editRenderLayerGlobals(currentRenderLayer = initial_layer)
        fix_camera_names()
        layer_switcher()

def check_render_layers(render_layer_override_compare_1,render_layer_override_compare_2,check_layer_field_result,text_field_list,*args):
    menu1 = cmds.optionMenu(render_layer_override_compare_1,valueue = True,query = True)
    menu2 = cmds.optionMenu(render_layer_override_compare_2,valueue = True,query = True)
    override_menu_1 = ""
    override_menu_2 = ""
    for txtF in text_field_list:
        txtFsp = txtF.split("|")
        txtFsp = txtFsp[2]
        if txtFsp == menu1:
            override_menu_1 = cmds.textField(txtF,text = True, query = True)
        if txtFsp == menu2:
            override_menu_2 = cmds.textField(txtF,text = True, query = True)
        override_menu_1_split = override_menu_1.split(",")
        override_menu_2_split = override_menu_2.split(",")
        diff_1_edit = []
        diff_2_edit = []
        diff = (list(set(override_menu_1_split) - set(override_menu_2_split)))
        for d in diff:
            d = d.replace("u' ","")
            d = d.replace(" '","")
            d = d.replace(" '","")
            if d != "":
                d = "diff:" + d
                diff_1_edit.append(d)
        diff_2 = (list(set(override_menu_2_split) - set(override_menu_1_split)))
        for d2 in diff_2:
            d2 = d2.replace("u' ","")
            d2 = d2.replace(" '","")
            d2 = d2.replace(" '","")
            if d2 != "":
                d2 = "diff_2:" + d2
                diff_2_edit.append(d2)
        diff_combo = diff_1_edit + diff_2_edit
        diff_combo = str(diff_combo)
        diff_combo = diff_combo.replace("[u'","")
        diff_combo = diff_combo.replace("u'","")
        diff_combo = diff_combo.replace(" '","")
        diff_combo = diff_combo.replace("]","")
    check_layer_field_result = cmds.textField(check_layer_field_result,text = diff_combo, edit = True)

def layer_switcher():
    global initial_layer
    set_camera = ""
    render_layers = cmds.ls(type = "renderLayer")
    initial_layer = cmds.editRenderLayerGlobals(query = True, currentRenderLayer = True)
    cam_info = analize_cameras()
    cam_field_text_raw = cam_info[0]
    render_cams = cam_info[1]
    name = "rebuild_render_layers"
    if (cmds.window(name, exists = True)):
        cmds.deleteUI(name)
    window = cmds.window(name, title = name, sizeable = False, widthHeight=(250, 50))
    cmds.columnLayout("mainColumn", adjustableColumn = True)
    render_lays = cmds.ls(type = "renderLayer")
    cmds.rowLayout(("objects1"), numberOfColumns = 1, parent = "mainColumn")
    button_copy_all_Layers = cmds.button(label = "copyALL_Layers")
    cmds.button(button_copy_all_Layers, command = partial(copy_all_layers,render_layers), edit = True)
    cmds.editRenderLayerGlobals(currentRenderLayer = initial_layer)
    panels = cmds.getPanel( type = "modelPanel" )
    for m_panel in panels:
        cmds.modelEditor(m_panel, edit = True, allObjects = 1)
    rl = initial_layer
    cmds.showWindow()

def main():
    layer_switcher()

#main()
