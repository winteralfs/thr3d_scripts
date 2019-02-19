import maya.cmds as cmds
from functools import partial
import re

renderLayers = cmds.ls(type = "renderLayer")
lightTypes = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
mats_VRayMtl = cmds.ls(type = "VRayMtl")
mats_phong = cmds.ls(type = "phong")
mats_blinn = cmds.ls(type = "blinn")
mats_lambert = cmds.ls(type = "lambert")
mats_surface = cmds.ls(type = "surfaceShader")
mats_disp = cmds.ls(type = "displacementShader")
dispNodes = cmds.ls(type = "VRayDisplacement")
placeNodes = cmds.ls(type = "place2dTexture")
fileNodes = cmds.ls(type = "file")
layeredTexture = cmds.ls(type = "layeredTexture")
VRayBlendMtls = cmds.ls(type = "VRayBlendMtl")
materials = mats_VRayMtl + mats_phong + mats_blinn + mats_lambert + mats_surface + placeNodes + fileNodes + mats_disp + dispNodes + layeredTexture + VRayBlendMtls
objectsCheck_g = cmds.ls(g = True)
objectsCheck_t = cmds.ls(type = "transform")
objectsCheck_cam = cmds.ls(type = "camera")
objectsCheck = objectsCheck_g + objectsCheck_t + materials + objectsCheck_cam
lites = cmds.ls(lt = True)
vrayLites = []
for o in objectsCheck:
    nt = cmds.nodeType(o)
    for lt in lightTypes:
        if nt == lt:
            vrayLites.append(o)
objectsCheck.append("vraySettings")

def overideInfoFunc(renderLayers):
    class attrOverideClass:
        def __init__(self,renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck):
            rllRampOverides = {}
            self.objLabel = objLabel
            self.renderLayers = renderLayers
            self.objType = objType
            print " "
            print " "
            print "self.objType = ",self.objType
            objList = objectsCheck
            if self.objType == "camera" or self.objType == "VRayLightRectShape" or self.objType == "spotLight" or self.objType == "ambientLight" or self.objType == "directionalLight" or self.objType == "pointLight" or self.objType == "VRayMtl" or self.objType == "blinn" or self.objType == "phong" or self.objType == "lambert" or self.objType == "surfaceShader" or self.objType == "displacementShader" or self.objType == "VRayDisplacement" or self.objType == "place2dTexture" or self.objType == "file" or self.objType == "gammaCorrect" or self.objType == "layeredTexture" or self.objType == "VRayBlendMtl":
                self.objList = cmds.ls(type = self.objType)
            if self.objType == "VRaySettingsNode":
                self.objList = []
                self.objList.append("vraySettings")
            self.attrOveridesDIC = attrOveridesDIC
            self.remAttrList = remAttrList

        def attrOverideDetect(self):
            for obj in self.objList:
                defRamp = "none"
                oRamp = "none"
                cns_count = 1
                it_list_count = 1
                it_list = []
                nt = cmds.nodeType(obj)
                if nt == self.objType:
                    attrs = cmds.listAttr(obj)
                    for rem in self.remAttrList:
                        attrs.remove(rem)
                    if self.objType == "layeredTexture":
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
                            attrString = obj + "." + attr
                            if attr == "inputs.isVisible" or attr == "inputs.alpha" or attr == "inputs.color" or attr == "inputs.blendMode":
                                it_list_2 = len(it_list)
                                if it_list_2 != 0:
                                    it_list_n = it_list[it]
                                    attr = attr.replace("inputs.","")
                                    attrString = obj + "." + "inputs[" + str(it_list_n) + "]." + attr
                                    attr = ("inputs[" + str(it_list_n) + "]." + attr)
                            cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                            defAttrVal = cmds.getAttr(attrString)
                            attrConns = cmds.listConnections(attrString,destination = False) or []
                            defRampFound = 0
                            for conn in attrConns:
                                connType = cmds.nodeType(conn)
                                if connType == "ramp" or connType == "fractal" or connType == "noise" or connType == "file" or connType == "checker" or connType == "cloud" or connType == "brownian" or connType == "bulge" or connType == "VRayMtl" or connType == "blinn" or connType == "phong" or connType == "lambert" or connType == "surfaceShader":
                                    defRampFound = 1
                                    defRamp = conn
                            for rl in renderLayers:
                                if rl != "defaultRenderLayer":
                                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                                    cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                                    attrConns = cmds.listConnections(attrString,destination = False) or []
                                    oRampFound = 0
                                    for attrConn in attrConns:
                                        attrType = cmds.nodeType(attrConn)
                                        if attrType == "ramp" or attrType == "fractal" or attrType == "noise" or attrType == "file" or attrType == "checker" or attrType == "cloud" or attrType == "brownian" or attrType == "bulge" or attrType == "VRayMtl" or attrType == "blinn" or attrType == "phong" or attrType == "lambert" or attrType == "surfaceShader":
                                            oRampFound = 1
                                            oRamp = attrConn
                                    oAttrVal = cmds.getAttr(attrString)
                                    if defRampFound == 0 and oRampFound == 0:
                                        if defAttrVal != oAttrVal:
                                            attrDICstring = self.objLabel + "_overide*" + obj + "." + attr + "**" + rl + "_"
                                            self.attrOveridesDIC[attrDICstring] = oAttrVal
                                    if defRampFound == 0 and oRampFound == 1:
                                        attrDICstring = self.objLabel + "_overide_rampAdded*" + obj + "." + attr + "**" + rl + "_"
                                        self.attrOveridesDIC[attrDICstring] = oRamp
                                    if defRampFound == 1 and oRampFound == 0:
                                        oAttrVal = cmds.getAttr(attrString)
                                        attrDICstring = self.objLabel + "_overide_rampRemoved*" + obj + "." + attr + "**" + rl + "_"
                                        self.attrOveridesDIC[attrDICstring] = oAttrVal
                                    if defRampFound == 1 and oRampFound == 1:
                                        oRamp = attrConn
                                        if oRamp != defRamp:
                                            attrDICstring = self.objLabel + "_overide_rampMismatch*" + obj + "." + attr + "**" + rl + "_"
                                            self.attrOveridesDIC[attrDICstring] = oRamp
                                        if oRamp == defRamp:
                                            rllOverides = cmds.listConnections(rl + ".adjustments", p = True, c = True) or []
                                            rllRampOverides = []
                                            for cn in rllOverides:
                                                t = cmds.nodeType(cn)
                                                if t == "ramp":
                                                    if cn not in rllRampOverides:
                                                        rllRampOverides.append(cn)
                                                for i in range(0, len(rllOverides), 2):
                                                    rlConn = rllOverides[i]
                                                    ovrAttr = rllOverides[i+1]
                                                    ovrIndex = rlConn.split("]")[0]
                                                    ovrIndex = ovrIndex.split("[")[-1]
                                                    ovrVal = cmds.getAttr(rl + ".adjustments[%s].value" %ovrIndex)
                                                    attrDICstring =  self.objLabel + "_" + attr + "_rampOveride" + "*" + ovrAttr + "**" + rl
                                                    if attrDICstring not in self.attrOveridesDIC and oRamp in ovrAttr:
                                                        self.attrOveridesDIC[attrDICstring] = ovrVal
                        it = it + 1
            return(self.attrOveridesDIC)


    def translations(objectsCheck, renderLayers):
        transValuesDictDEF = {}
        objInLayers = []
        transLayOverides = []
        transValuesDictOTH = {}
        translayDict = {}
        cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
        lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
        for ob in objectsCheck_t:
            strtranslateX = ob + ".translateX"
            translateX = cmds.getAttr(strtranslateX)
            var = ob + "$" + lay + "$translateX"
            transValuesDictDEF[var] = translateX
            strtranslateY = ob + ".translateY"
            translateY = cmds.getAttr(strtranslateY)
            var = ob + "$" + lay + "$translateY"
            transValuesDictDEF[var] = translateY
            strtranslateZ = ob + ".translateZ"
            translateZ = cmds.getAttr(strtranslateZ)
            var = ob + "$" + lay + "$translateZ"
            transValuesDictDEF[var] = translateZ
            strrotateX = ob + ".rotateX"
            rotateX = cmds.getAttr(strrotateX)
            var = ob + "$" + lay + "$rotateX"
            transValuesDictDEF[var] = rotateX
            strrotateY = ob + ".rotateY"
            rotateY = cmds.getAttr(strrotateY)
            var = ob + "$" + lay + "$rotateY"
            transValuesDictDEF[var] = rotateY
            strrotateZ = ob + ".rotateZ"
            rotateZ = cmds.getAttr(strrotateZ)
            var = ob + "$" + lay + "$rotateZ"
            transValuesDictDEF[var] = rotateZ
            strScaleX = ob + ".scaleX"
            scaleX = cmds.getAttr(strScaleX)
            var = ob + "$" + lay + "$scaleX"
            transValuesDictDEF[var] = scaleX
            strScaleY = ob + ".scaleY"
            scaleY = cmds.getAttr(strScaleY)
            var = ob + "$" + lay + "$scaleY"
            transValuesDictDEF[var] = scaleY
            strScaleZ = ob + ".scaleZ"
            scaleZ = cmds.getAttr(strScaleZ)
            var = ob + "$" + lay + "$scaleZ"
            transValuesDictDEF[var] = scaleZ
        for ob in objectsCheck_t:
            for lay in renderLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = lay )
                lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
                if "defaultRenderLayer" != lay:
                    strtranslateX = ob + ".translateX"
                    translateX = cmds.getAttr(strtranslateX)
                    var = ob + "$" + lay + "$translateX"
                    transValuesDictOTH[var] = translateX
                    strtranslateY = ob + ".translateY"
                    translateY = cmds.getAttr(strtranslateY)
                    var = ob + "$" + lay + "$translateY"
                    transValuesDictOTH[var] = translateY
                    strtranslateZ = ob + ".translateZ"
                    translateZ = cmds.getAttr(strtranslateZ)
                    var = ob + "$" + lay + "$translateZ"
                    transValuesDictOTH[var] = translateZ
                    strrotateX = ob + ".rotateX"
                    rotateX = cmds.getAttr(strrotateX)
                    var = ob + "$" + lay + "$rotateX"
                    transValuesDictOTH[var] = rotateX
                    strrotateY = ob + ".rotateY"
                    rotateY = cmds.getAttr(strrotateY)
                    var = ob + "$" + lay + "$rotateY"
                    transValuesDictOTH[var] = rotateY
                    strrotateZ = ob + ".rotateZ"
                    rotateZ = cmds.getAttr(strrotateZ)
                    var = ob + "$" + lay + "$rotateZ"
                    transValuesDictOTH[var] = rotateZ
                    strScaleX = ob + ".scaleX"
                    scaleX = cmds.getAttr(strScaleX)
                    var = ob + "$" + lay + "$scaleX"
                    transValuesDictOTH[var] = scaleX
                    strScaleY = ob + ".scaleY"
                    scaleY = cmds.getAttr(strScaleY)
                    var = ob + "$" + lay + "$scaleY"
                    transValuesDictOTH[var] = scaleY
                    strScaleZ = ob + ".scaleZ"
                    scaleZ = cmds.getAttr(strScaleZ)
                    var = ob + "$" + lay + "$scaleZ"
                    transValuesDictOTH[var] = scaleZ
        for transVal in transValuesDictOTH:
            transValSplit = transVal.split("$")
            for transValDef in transValuesDictDEF:
                transValDefSplit = transValDef.split("$")
                if transValSplit[0] == transValDefSplit[0] and transValSplit[2] == transValDefSplit[2]:
                    valu = transValuesDictOTH[transVal]
                    valuDef = transValuesDictDEF[transValDef]
                    if valu != valuDef:
                        transLayOverides.append(transVal)
                        translayDict["transO$" + transVal] = valu
        return transValuesDictDEF,transValuesDictOTH,transLayOverides,objectsCheck,renderLayers,translayDict

    def materialAssignments(objectsCheck, renderLayers):
        mats_list = []
        mats_list_OVR = []
        matLayOverides = []
        materialsDictDEF = {}
        materialsDictOTH = {}
        matsLayDict = {}
        for ob in objectsCheck:
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            lay = cmds.editRenderLayerGlobals(q = True, currentRenderLayer = True)
            for L in renderLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = L )
                if L == "defaultRenderLayer":
                    cmds.select(clear = True)
                    cmds.select(ob)
                    cmds.hyperShade(smn = True)
                    mats_list = cmds.ls(sl = True)
                    for MM in mats_list:
                        NT = cmds.nodeType(MM)
                        if NT != "renderLayer":
                            if MM not in mats_list_OVR:
                                mats_list_OVR.append(MM)
                            dictKeyOTH = ob + "$" + L + "$"
                            materialsDictDEF[dictKeyOTH] = MM
                else:
                    cmds.select(clear = True)
                    cmds.select(ob)
                    cmds.hyperShade(smn = True)
                    mats_list = cmds.ls(sl = True)
                    for MM in mats_list:
                        NT = cmds.nodeType(MM)
                        if NT != "renderLayer":
                            if MM not in mats_list_OVR:
                                mats_list_OVR.append(MM)
                            dictKeyOTH = ob + "$" + L + "$"
                            materialsDictOTH[dictKeyOTH] = MM
        for matsDictOth in materialsDictOTH:
           matsValSplit = matsDictOth.split("$")
           for matsDictDEF in materialsDictDEF:
               matsValDEFSplit = matsDictDEF.split("$")
               if matsValSplit[0] == matsValDEFSplit[0]:
                    matOth = materialsDictOTH[matsDictOth]
                    matDef = materialsDictDEF[matsDictDEF]
                    if matOth != matDef:
                        matLayOverides.append(matsDictOth)
                        matsDictString = matsDictOth + ".materialAssignment"
                        if matsDictString not in matsLayDict and "Shape" not in matsDictString:
                            matsLayDict[matsDictString] = matOth
        return(mats_list_OVR,mats_list_OVR,materialsDictOTH,matLayOverides,matsLayDict)

    def materialOverides(objectsCheck,renderLayers):
        materialsOverideDIC = {}
        attrOveridesDIC = materialsOverideDIC
        objLabel = "mtlOveride"

        objType = "VRayMtl"
        remAttrList = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","outColor","outColorR","outColorG","outColorB","outApiType","outApiClassification","outTransparency",
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
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "blinn"
        remAttrList = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "eccentricity", "specularRollOff", "reflectionRolloff"]
        attrCheck = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","eccentricity","specularRollOff","specularColor","reflectivity","reflectedColor"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "phong"
        remAttrList = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB", "reflectionLimit", "specularColor", "specularColorR", "specularColorG", "specularColorB", "reflectivity", "reflectedColor", "reflectedColorR", "reflectedColorG", "reflectedColorB", "triangleNormalCamera", "triangleNormalCameraX", "triangleNormalCameraY", "triangleNormalCameraZ", "reflectionSpecularity", "cosinePower"]
        attrCheck = ["color","transparency","ambientColor","normalCamera","diffuse","translucence","translucenceDepth","translucenceFocus","cosinePower","specularColor","reflectivity","reflectedColor"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "lambert"
        remAttrList = ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "objectId", "primitiveId", "raySampler", "rayDepth", "rayInstance", "refractionLimit", "refractiveIndex", "mediumRefractiveIndex", "refractions", "diffuse", "rayDirection", "rayDirectionX", "rayDirectionY", "rayDirectionZ", "color", "colorR", "colorG", "colorB", "transparency", "transparencyR", "transparencyG", "transparencyB", "ambientColor", "ambientColorR", "ambientColorG", "ambientColorB", "incandescence", "incandescenceR", "incandescenceG", "incandescenceB", "translucence", "translucenceFocus", "translucenceDepth", "opacityDepth", "glowIntensity", "vrOverwriteDefaults", "vrFillObject", "vrEdgeWeight", "vrEdgeColor", "vrEdgeColorR", "vrEdgeColorG", "vrEdgeColorB", "vrEdgeStyle", "vrEdgePriority", "vrHiddenEdges", "vrHiddenEdgesOnTransparent", "vrOutlinesAtIntersections", "materialAlphaGain", "hideSource", "surfaceThickness", "shadowAttenuation", "transparencyDepth", "lightAbsorbance", "chromaticAberration", "outColor", "outColorR", "outColorG", "outColorB", "outTransparency", "outTransparencyR", "outTransparencyG", "outTransparencyB", "outGlowColor", "outGlowColorR", "outGlowColorG", "outGlowColorB", "pointCamera", "pointCameraX", "pointCameraY", "pointCameraZ", "normalCamera", "normalCameraX", "normalCameraY", "normalCameraZ", "lightDataArray", "lightDataArray.lightDirection", "lightDataArray.lightDirectionX", "lightDataArray.lightDirectionY", "lightDataArray.lightDirectionZ", "lightDataArray.lightIntensity", "lightDataArray.lightIntensityR", "lightDataArray.lightIntensityG", "lightDataArray.lightIntensityB", "lightDataArray.lightAmbient", "lightDataArray.lightDiffuse", "lightDataArray.lightSpecular", "lightDataArray.lightShadowFraction", "lightDataArray.preShadowIntensity", "lightDataArray.lightBlindData", "matteOpacityMode", "matteOpacity", "outMatteOpacity", "outMatteOpacityR", "outMatteOpacityG", "outMatteOpacityB", "hardwareShader", "hardwareShaderR", "hardwareShaderG", "hardwareShaderB"]
        attrCheck = ["color","transparency","ambientColor","incandescence","diffuse","translucence","translucenceDepth","translucenceFocus"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "surfaceShader"
        remAttrList = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outMatteOpacity","outMatteOpacityR","outMatteOpacityG","outMatteOpacityB","outGlowColor","outGlowColorR","outGlowColorG","outGlowColorB","materialAlphaGain"]
        attrCheck = ["outColor","outTransparency","outGlowColor","outMatteOpacity"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "place2dTexture"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","uvCoord","uCoord","vCoord","vertexUvOne","vertexUvOneU","vertexUvOneV","vertexUvTwo","vertexUvTwoU","vertexUvTwoV","vertexUvThree","vertexUvThreeU","vertexUvThreeV","vertexCameraOne","vertexCameraOneX","vertexCameraOneY","vertexCameraOneZ","uvFilterSize","uvFilterSizeX","uvFilterSizeY","coverage","coverageU","coverageV","translateFrame","translateFrameU","translateFrameV","rotateFrame","mirrorU","mirrorV","stagger","wrapU","wrapV","repeatUV","repeatU","repeatV","offset","offsetU","offsetV","rotateUV","noiseUV","noiseU","noiseV","fast","outUV","outU","outV","outUvFilterSize","outUvFilterSizeX","outUvFilterSizeY","doTransform"]
        attrCheck = ["coverageU","coverageV","translateFrameU","translateFrameV","rotateFrame","mirrorU","mirrorV","wrapU","wrapV","stagger","repeatU","repeatV","offsetU","offsetV","rotateUV","noiseU","noiseV","fast"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "file"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","filter","filterOffset","invert","alphaIsLuminance","colorGain","colorGainR","colorGainG","colorGainB","colorOffset","colorOffsetR","colorOffsetG","colorOffsetB","alphaGain","alphaOffset","defaultColor","defaultColorR","defaultColorG","defaultColorB","outColor","outColorR","outColorG","outColorB","outAlpha","fileTextureName","fileTextureNamePattern","computedFileTextureNamePattern","disableFileLoad","useFrameExtension","frameExtension","frameOffset","useHardwareTextureCycling","startCycleExtension","endCycleExtension","byCycleIncrement","forceSwatchGen","filterType","filterWidth","preFilter","preFilterRadius","useCache","useMaximumRes","uvTilingMode","explicitUvTiles","explicitUvTiles.explicitUvTileName","explicitUvTiles.explicitUvTilePosition","explicitUvTiles.explicitUvTilePositionU","explicitUvTiles.explicitUvTilePositionV","baseExplicitUvTilePosition","baseExplicitUvTilePositionU","baseExplicitUvTilePositionV","uvTileProxyDirty","uvTileProxyGenerate","uvTileProxyQuality","coverage","coverageU","coverageV","translateFrame","translateFrameU","translateFrameV","rotateFrame","doTransform","mirrorU","mirrorV","stagger","wrapU","wrapV","repeatUV","repeatU","repeatV","offset","offsetU","offsetV","rotateUV","noiseUV","noiseU","noiseV","blurPixelation","vertexCameraOne","vertexCameraOneX","vertexCameraOneY","vertexCameraOneZ","vertexCameraTwo","vertexCameraTwoX","vertexCameraTwoY","vertexCameraTwoZ","vertexCameraThree","vertexCameraThreeX","vertexCameraThreeY","vertexCameraThreeZ","vertexUvOne","vertexUvOneU","vertexUvOneV","vertexUvTwo","vertexUvTwoU","vertexUvTwoV","vertexUvThree","vertexUvThreeU","vertexUvThreeV","objectType","rayDepth","primitiveId","pixelCenter","pixelCenterX","pixelCenterY","exposure","hdrMapping","hdrExposure","dirtyPixelRegion","ptexFilterType","ptexFilterWidth","ptexFilterBlur","ptexFilterSharpness","ptexFilterInterpolateLevels","colorProfile","colorSpace","ignoreColorSpaceFileRules","workingSpace","colorManagementEnabled","colorManagementConfigFileEnabled","colorManagementConfigFilePath","outSize","outSizeX","outSizeY","fileHasAlpha","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","infoBits"]
        attrCheck = ["exposure","defaultColor","colorGain","colorOffset","alphaGain","alphaOffset","alphaIsLuminance","invert"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "gammaCorrect"
        remAttrList = ['message','caching','frozen','isHistoricallyInteresting','nodeState','binMembership','value','valueX','valueY','valueZ','gamma','gammaX','gammaY','gammaZ','renderPassMode','outValue','outValueX','outValueY','outValueZ']
        attrCheck = ["value","gammaX","gammaY","gammaZ","renderPassMode"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "layeredTexture"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","inputs","inputs.color","inputs.colorR","inputs.colorG","inputs.colorB","inputs.alpha","inputs.blendMode","inputs.isVisible","outColor","outColorR","outColorG","outColorB","outAlpha","hardwareColor","hardwareColorR","hardwareColorG","hardwareColorB","alphaIsLuminance","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB"]
        attrCheck = ["alphaIsLuminance","inputs.isVisible","inputs.alpha","inputs.color","inputs.blendMode"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "VRayBlendMtl"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","swatchAutoUpdate","swatchAlwaysRender","swatchExplicitUpdate","swatchMaxRes","base_material","base_materialR","base_materialG","base_materialB","color","colorR","colorG","colorB","viewportColor","viewportColorR","viewportColorG","viewportColorB","coat_material_0","coat_material_0R","coat_material_0G","coat_material_0B","blend_amount_0","blend_amount_0R","blend_amount_0G","blend_amount_0B","coat_material_1","coat_material_1R","coat_material_1G","coat_material_1B","blend_amount_1","blend_amount_1R","blend_amount_1G","blend_amount_1B","coat_material_2","coat_material_2R","coat_material_2G","coat_material_2B","blend_amount_2","blend_amount_2R","blend_amount_2G","blend_amount_2B","coat_material_3","coat_material_3R","coat_material_3G","coat_material_3B","blend_amount_3","blend_amount_3R","blend_amount_3G","blend_amount_3B","coat_material_4","coat_material_4R","coat_material_4G","coat_material_4B","blend_amount_4","blend_amount_4R","blend_amount_4G","blend_amount_4B","coat_material_5","coat_material_5R","coat_material_5G","coat_material_5B","blend_amount_5","blend_amount_5R","blend_amount_5G","blend_amount_5B","coat_material_6","coat_material_6R","coat_material_6G","coat_material_6B","blend_amount_6","blend_amount_6R","blend_amount_6G","blend_amount_6B","coat_material_7","coat_material_7R","coat_material_7G","coat_material_7B","blend_amount_7","blend_amount_7R","blend_amount_7G","blend_amount_7B","coat_material_8","coat_material_8R","coat_material_8G","coat_material_8B","blend_amount_8","blend_amount_8R","blend_amount_8G","blend_amount_8B","additive_mode","outColor","outColorR","outColorG","outColorB","outTransparency","outTransparencyR","outTransparencyG","outTransparencyB","outApiType","outApiClassification"]
        attrCheck = ["base_material","additive_mode","coat_material_0","blend_amount_0","coat_material_1","blend_amount_1","coat_material_2","blend_amount_2","coat_material_3","blend_amount_3","coat_material_4","blend_amount_4","coat_material_5","blend_amount_5","coat_material_6","blend_amount_6","coat_material_7","blend_amount_7","coat_material_8","blend_amount_8"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "displacementShader"
        remAttrList = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","displacementMode","displacement","vectorDisplacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","yIsUp","tangent","tangentX","tangentY","tangentZ"]
        attrCheck = ["displacement","vectorDisplacementX","vectorDisplacementY","vectorDisplacementZ","scale","vectorEncoding","vectorSpace","tangentX","tangentY","tangentZ","nodeState","caching","displacementMode"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        objType = "VRayDisplacement"
        remAttrList = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","dagSetMembers","dnSetMembers","memberWireframeColor","annotation","isLayer","verticesOnlySet","edgesOnlySet","facetsOnlySet","editPointsOnlySet","renderableOnlySet","partition","groupNodes","usedBy","displacement","overrideGlobalDisplacement","outApiType","outApiClassification","vraySeparator_vray_displacement","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementType","vrayDisplacementAmount","vrayDisplacementShift","vrayDisplacementKeepContinuity","vrayEnableWaterLevel","vrayWaterLevel","vrayDisplacementCacheNormals","vray2dDisplacementResolution","vray2dDisplacementPrecision","vray2dDisplacementTightBounds","vray2dDisplacementMultiTile","vray2dDisplacementFilterTexture","vray2dDisplacementFilterBlur","vrayDisplacementUseBounds","vrayDisplacementMinValue","vrayDisplacementMinValueR","vrayDisplacementMinValueG","vrayDisplacementMinValueB","vrayDisplacementMaxValue","vrayDisplacementMaxValueR","vrayDisplacementMaxValueG","vrayDisplacementMaxValueB","vraySeparator_vray_subquality","vrayOverrideGlobalSubQual","vrayViewDep","vrayEdgeLength","vrayMaxSubdivs"]
        attrCheck = ["overrideGlobalDisplacement","displacement","caching","nodeState","blackBox","vrayDisplacementNone","vrayDisplacementStatic","vrayDisplacementType","vrayDisplacementAmount","vrayDisplacementShift","vrayEdgeLength","vrayMaxSubdivs","vrayDisplacementUseBounds"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        matOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        materialsOverideDIC = matOverides.attrOverideDetect()

        return(materialsOverideDIC)

    def cameraOverides(objectsCheck,renderLayers):
        cameraOveridesDIC = {}
        attrOveridesDIC = cameraOveridesDIC
        objLabel = "camera_overide"
        objType = "camera"
        remAttrList =  ["message", "caching", "isHistoricallyInteresting", "nodeState", "binMembership", "hyperLayout", "isCollapsed", "blackBox", "borderConnections", "isHierarchicalConnection", "publishedNodeInfo", "publishedNodeInfo.publishedNode", "publishedNodeInfo.isHierarchicalNode", "publishedNodeInfo.publishedNodeType", "rmbCommand", "templateName", "templatePath", "viewName", "iconName", "viewMode", "templateVersion", "uiTreatment", "customTreatment", "creator", "creationDate", "containerType", "boundingBox", "boundingBoxMin", "boundingBoxMinX", "boundingBoxMinY", "boundingBoxMinZ", "boundingBoxMax", "boundingBoxMaxX", "boundingBoxMaxY", "boundingBoxMaxZ", "boundingBoxSize", "boundingBoxSizeX", "boundingBoxSizeY", "boundingBoxSizeZ", "center", "boundingBoxCenterX", "boundingBoxCenterY", "boundingBoxCenterZ", "matrix", "inverseMatrix", "worldMatrix", "worldInverseMatrix", "parentMatrix", "parentInverseMatrix", "visibility", "intermediateObject", "template", "ghosting", "instObjGroups", "instObjGroups.objectGroups", "instObjGroups.objectGroups.objectGrpCompList", "instObjGroups.objectGroups.objectGroupId", "instObjGroups.objectGroups.objectGrpColor", "objectColorRGB", "objectColorR", "objectColorG", "objectColorB", "useObjectColor", "objectColor", "drawOverride", "overrideDisplayType", "overrideLevelOfDetail", "overrideShading", "overrideTexturing", "overridePlayback", "overrideEnabled", "overrideVisibility", "overrideColor", "lodVisibility", "selectionChildHighlighting", "renderInfo", "identification", "layerRenderable", "layerOverrideColor", "renderLayerInfo", "renderLayerInfo.renderLayerId", "renderLayerInfo.renderLayerRenderable", "renderLayerInfo.renderLayerColor", "ghostingControl", "ghostCustomSteps", "ghostPreSteps", "ghostPostSteps", "ghostStepSize", "ghostFrames", "ghostColorPreA", "ghostColorPre", "ghostColorPreR", "ghostColorPreG", "ghostColorPreB", "ghostColorPostA", "ghostColorPost", "ghostColorPostR", "ghostColorPostG", "ghostColorPostB", "ghostRangeStart", "ghostRangeEnd", "ghostDriver", "hiddenInOutliner", "renderable", "cameraAperture", "horizontalFilmAperture", "verticalFilmAperture", "shakeOverscan", "shakeOverscanEnabled", "filmOffset", "horizontalFilmOffset", "verticalFilmOffset", "shakeEnabled", "shake", "horizontalShake", "verticalShake", "stereoHorizontalImageTranslateEnabled", "stereoHorizontalImageTranslate", "postProjection", "preScale", "filmTranslate", "filmTranslateH", "filmTranslateV", "filmRollControl", "filmRollPivot", "horizontalRollPivot", "verticalRollPivot", "filmRollValue", "filmRollOrder", "postScale", "filmFit", "filmFitOffset", "overscan", "panZoomEnabled", "renderPanZoom", "pan", "horizontalPan", "verticalPan", "zoom", "focalLength", "lensSqueezeRatio", "cameraScale", "triggerUpdate", "nearClipPlane", "farClipPlane", "fStop", "focusDistance", "shutterAngle", "centerOfInterest", "orthographicWidth", "imageName", "depthName", "maskName", "tumblePivot", "tumblePivotX", "tumblePivotY", "tumblePivotZ", "usePivotAsLocalSpace", "imagePlane", "homeCommand", "bookmarks", "locatorScale", "displayGateMaskOpacity", "displayGateMask", "displayFilmGate", "displayResolution", "displaySafeAction", "displaySafeTitle", "displayFieldChart", "displayFilmPivot", "displayFilmOrigin", "clippingPlanes", "bestFitClippingPlanes", "depthOfField", "motionBlur", "orthographic", "journalCommand", "image", "depth", "transparencyBasedDepth", "threshold", "depthType", "useExploreDepthFormat", "mask", "displayGateMaskColor", "displayGateMaskColorR", "displayGateMaskColorG", "displayGateMaskColorB", "backgroundColor", "backgroundColorR", "backgroundColorG", "backgroundColorB", "focusRegionScale", "displayCameraNearClip", "displayCameraFarClip", "displayCameraFrustum", "cameraPrecompTemplate", "vraySeparator_vray_cameraPhysical", "vrayCameraPhysicalOn", "vrayCameraPhysicalType", "vrayCameraPhysicalFilmWidth", "vrayCameraPhysicalFocalLength", "vrayCameraPhysicalSpecifyFOV", "vrayCameraPhysicalFOV", "vrayCameraPhysicalZoomFactor", "vrayCameraPhysicalDistortionType", "vrayCameraPhysicalDistortion", "vrayCameraPhysicalLensFile", "vrayCameraPhysicalDistortionMap", "vrayCameraPhysicalDistortionMapR", "vrayCameraPhysicalDistortionMapG", "vrayCameraPhysicalDistortionMapB", "vrayCameraPhysicalFNumber", "vrayCameraPhysicalHorizLensShift", "vrayCameraPhysicalLensShift", "vrayCameraPhysicalLensAutoVShift", "vrayCameraPhysicalShutterSpeed", "vrayCameraPhysicalShutterAngle", "vrayCameraPhysicalShutterOffset", "vrayCameraPhysicalLatency", "vrayCameraPhysicalISO", "vrayCameraPhysicalSpecifyFocus", "vrayCameraPhysicalFocusDistance", "vrayCameraPhysicalExposure", "vrayCameraPhysicalWhiteBalance", "vrayCameraPhysicalWhiteBalanceR", "vrayCameraPhysicalWhiteBalanceG", "vrayCameraPhysicalWhiteBalanceB", "vrayCameraPhysicalVignetting", "vrayCameraPhysicalVignettingAmount", "vrayCameraPhysicalBladesEnable", "vrayCameraPhysicalBladesNum", "vrayCameraPhysicalBladesRotation", "vrayCameraPhysicalCenterBias", "vrayCameraPhysicalAnisotropy", "vrayCameraPhysicalUseDof", "vrayCameraPhysicalUseMoBlur", "vrayCameraPhysicalApertureMap", "vrayCameraPhysicalApertureMapR", "vrayCameraPhysicalApertureMapG", "vrayCameraPhysicalApertureMapB", "vrayCameraPhysicalApertureMapAffectsExposure", "vrayCameraPhysicalOpticalVignetting", "vraySeparator_vray_cameraOverrides", "vrayCameraOverridesOn", "vrayCameraType", "vrayCameraOverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve",]
        attrCheck = ["vraySeparator_vray_cameraPhysical","vrayCameraPhysicalOn","vrayCameraPhysicalType","vrayCameraPhysicalFilmWidth","vrayCameraPhysicalFocalLength","vrayCameraPhysicalSpecifyFOV","vrayCameraPhysicalFOV","vrayCameraPhysicalZoomFactor","vrayCameraPhysicalDistortionType","vrayCameraPhysicalDistortion","vrayCameraPhysicalLensFile","vrayCameraPhysicalDistortionMap","vrayCameraPhysicalDistortionMapR",
        "vrayCameraPhysicalDistortionMapG","vrayCameraPhysicalDistortionMapB","vrayCameraPhysicalFNumber","vrayCameraPhysicalHorizLensShift","vrayCameraPhysicalLensShift","vrayCameraPhysicalLensAutoVShift","vrayCameraPhysicalShutterSpeed","vrayCameraPhysicalShutterAngle","vrayCameraPhysicalShutterOffset","vrayCameraPhysicalLatency","vrayCameraPhysicalISO","vrayCameraPhysicalSpecifyFocus","vrayCameraPhysicalFocusDistance",
        "vrayCameraPhysicalExposure","vrayCameraPhysicalWhiteBalance","vrayCameraPhysicalWhiteBalanceR","vrayCameraPhysicalWhiteBalanceG","vrayCameraPhysicalWhiteBalanceB","vrayCameraPhysicalVignetting","vrayCameraPhysicalVignettingAmount","vrayCameraPhysicalBladesEnable","vrayCameraPhysicalBladesNum","vrayCameraPhysicalBladesRotation","vrayCameraPhysicalCenterBias","vrayCameraPhysicalAnisotropy","vrayCameraPhysicalUseDof","vrayCameraPhysicalUseMoBlur"
        ,"vrayCameraPhysicalApertureMap","vrayCameraPhysicalApertureMapR","vrayCameraPhysicalApertureMapG","vrayCameraPhysicalApertureMapB","vrayCameraPhysicalApertureMapAffectsExposure","vrayCameraPhysicalOpticalVignetting","vraySeparator_vray_cameraOverrides","vrayCameraOverridesOn","vrayCameraType", "vrayCameraOverrideFOV", "vrayCameraFOV", "vrayCameraHeight", "vrayCameraVerticalFOV", "vrayCameraAutoFit", "vrayCameraDist", "vrayCameraCurve","renderable"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        cameraOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        cameraOveridesDIC = cameraOverides.attrOverideDetect()

        return(cameraOveridesDIC)

    def lightOverides(objectsCheck,renderLayers):
        lightOveridesDIC = {}
        attrOveridesDIC = lightOveridesDIC
        objLabel = "light_overide"
        objType = "VRayLightRectShape"
        remAttrList = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType"
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
            remAttrList.remove(attr)
        lightOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        lightOveridesDIC = lightOverides.attrOverideDetect()

        objType = "spotLight"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","coneAngle","penumbraAngle","dropoff","barnDoors","leftBarnDoor","rightBarnDoor","topBarnDoor","bottomBarnDoor","useDecayRegions","startDistance1","endDistance1","startDistance2","endDistance2","startDistance3","endDistance3","fogSpread","fogIntensity","objectType","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","rayDirection","rayDirectionX","rayDirectionY","rayDirectionZ","fogGeometry","lightGlow","psIllumSamples"]
        attrCheck = ["color","intensity","emitDiffuse","emitSpecular","decayRate","coneAngle","penumbraAngle","dropoff","shadowColor","useRayTraceShadows","lightRadius","shadowRays","rayDepthLimit","useDepthMapShadows","dmapResolution","useMidDistDmap","useDmapAutoFocus","dmapFocus","dmapFilterSize","dmapBias","fogShadowIntensity","volumeShadowSamples"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        lightOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        lightOveridesDIC = lightOverides.attrOverideDetect()

        objType = "ambientLight"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","ambientShade","objectType","shadowRadius","castSoftShadows","normalCamera","normalCameraX","normalCameraY","normalCameraZ","receiveShadows"]
        attrCheck = ["color","intensity","ambientShade"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        lightOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        lightOveridesDIC = lightOverides.attrOverideDetect()

        objType = "directionalLight"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","useLightPosition","objectType","lightAngle","pointWorld","pointWorldX","pointWorldY","pointWorldZ"]
        attrCheck = ["color","intensity","emitDiffuse","emitSpecular"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        lightOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        lightOveridesDIC = lightOverides.attrOverideDetect()

        objType = "pointLight"
        remAttrList = ["message","caching","frozen","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox","borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment","customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ","boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ","center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix","parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","wireColorRGB","wireColorR","wireColorG","wireColorB","useObjectColor","objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled","overrideVisibility","hideOnPlayback","overrideRGBColors","overrideColor","overrideColorRGB","overrideColorR","overrideColorG","overrideColorB","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps","ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG","ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","useOutlinerColor","outlinerColor","outlinerColorR","outlinerColorG","outlinerColorB","color","colorR","colorG","colorB","intensity","useRayTraceShadows","shadowColor","shadColorR","shadColorG","shadColorB","shadowRays","rayDepthLimit","centerOfIllumination","pointCamera","pointCameraX","pointCameraY","pointCameraZ","matrixWorldToEye","matrixEyeToWorld","objectId","primitiveId","raySampler","rayDepth","renderState","locatorScale","uvCoord","uCoord","vCoord","uvFilterSize","uvFilterSizeX","uvFilterSizeY","infoBits","lightData","lightDirection","lightDirectionX","lightDirectionY","lightDirectionZ","lightIntensity","lightIntensityR","lightIntensityG","lightIntensityB","lightAmbient","lightDiffuse","lightSpecular","lightShadowFraction","preShadowIntensity","lightBlindData","opticalFXvisibility","opticalFXvisibilityR","opticalFXvisibilityG","opticalFXvisibilityB","rayInstance","decayRate","emitDiffuse","emitSpecular","lightRadius","castSoftShadows","useDepthMapShadows","reuseDmap","useMidDistDmap","dmapFilterSize","dmapResolution","dmapBias","dmapFocus","dmapWidthFocus","useDmapAutoFocus","volumeShadowSamples","fogShadowIntensity","useDmapAutoClipping","dmapNearClipPlane","dmapFarClipPlane","useOnlySingleDmap","useXPlusDmap","useXMinusDmap","useYPlusDmap","useYMinusDmap","useZPlusDmap","useZMinusDmap","dmapUseMacro","dmapName","dmapLightName","dmapSceneName","dmapFrameExt","writeDmap","lastWrittenDmapAnimExtName","receiveShadows","fogGeometry","fogRadius","lightGlow","objectType","fogType","pointWorld","pointWorldX","pointWorldY","pointWorldZ","farPointWorld","farPointWorldX","farPointWorldY","farPointWorldZ","fogIntensity"]
        attrCheck = ["color","intensity","emitDiffuse","emitSpecular","decayRate"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        lightOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        lightOveridesDIC = lightOverides.attrOverideDetect()

        return(lightOveridesDIC)

    def vraySettingsOverides(objectsCheck,renderLayers):
        vraySettingsOverrideDic = {}
        attrOveridesDIC = vraySettingsOverrideDic
        objLabel = "vs"
        cmds.loadPlugin('vrayformaya', quiet=True)
        cmds.pluginInfo('vrayformaya', edit=True, autoload=True)
        cmds.setAttr("defaultRenderGlobals.ren", "vray", type = "string")

        objType = "VRaySettingsNode"
        remAttrList =  cmds.listAttr("vraySettings")
        attrCheck = ["cam_envtexBg","cam_envtexGi","cam_envtexReflect","cam_envtexRefract","cam_envtexSecondaryMatte","globopt_geom_displacement","globopt_light_doLights","globopt_light_doHiddenLights","globopt_light_doDefaultLights",
        "globopt_light_doShadows","globopt_light_ignoreLightLinking","globopt_light_disableSelfIllumination","photometricScale","globopt_mtl_reflectionRefraction","globopt_mtl_glossy","globopt_mtl_transpMaxLevels","globopt_mtl_transpCutoff"
        ,"globopt_mtl_doMaps","globopt_mtl_filterMaps","bumpMultiplier","texFilterScaleMultiplier","globopt_ray_bias","globopt_ray_maxIntens_on","gi_texFilteringMultiplier","cam_overrideEnvtex","cam_overrideEnvtexSecondaryMatte",
        "ddisplac_amount","ddisplac_edgeLength","ddisplac_maxSubdivs","giOn","reflectiveCaustics","refractiveCaustics","secondaryMultiplier","secondaryEngine","saturation","contrast","contrastBase","aoOn","aoAmount","aoRadius","aoSubdivs",
        "giRayDistOn","giRayDist","causticsOn","causticsMultiplier","causticsSearchDistance","causticsMaxPhotons","causticsMaxDensity","minShadeRate"]
        for attr in attrCheck:
            remAttrList.remove(attr)
        vraySettingsOverides = attrOverideClass(renderLayers,objType,remAttrList,attrOveridesDIC,objLabel,objectsCheck)
        vraySettingsOverrideDic = vraySettingsOverides.attrOverideDetect()

        return(vraySettingsOverrideDic)

    def objsInRenderLayer(objectsCheck,renderLayer):
        obsInLayerDic = {}
        for rl in renderLayers:
            obsInLayer = cmds.editRenderLayerMembers(rl, query = True) or []
            for obj in objectsCheck:
                for obs in obsInLayer:
                    if obj == obs:
                        obsIlaySTRING = obj + "_" + rl
                        obsInLayerDic[obsIlaySTRING] = rl

        return(obsInLayerDic)

    def Render_stat_Overides(objectsCheck_g, renderLayers):
        RenderStatOverrideDic = {}
        excludeList = ["camera","ambientLight","directionalLight","pointLight","spotLight","areaLight","volumeLight","VRayLightSphereShape","VRayLightRectShape","VRayLightDomeShape","VRayLightIESShape"]
        siz = len(objectsCheck_g)
        l = 0
        while l < siz:
            for object in objectsCheck_g:
                objectT = cmds.objectType(object)
                for excld in excludeList:
                    if excld == objectT:
                        objectsCheck_g.remove(object)
            l = l + 1
        for object in objectsCheck_g:
            objType = cmds.objectType(object)
            if objType != "locator":
                Render_Stat_List = ["castsShadows","receiveShadows","motionBlur","primaryVisibility","smoothShading","visibleInReflections","visibleInRefractions","doubleSided"]
                for rsl in Render_Stat_List:
                    attrString = object + "." + rsl
                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                    defValue = cmds.getAttr(attrString)
                    for rl in renderLayers:
                        if rl != "defaultRenderLayer":
                            cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                            layValue = cmds.getAttr(attrString)
                            if layValue != defValue:
                                dicString = object + "**" + "renderStats" + "**" +  rsl + "**" + rl
                                RenderStatOverrideDic[dicString] = layValue
            return(RenderStatOverrideDic)

    def vrayObjectPropO(renderLayers):
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
                for rl in renderLayers:
                    if rl != "defaultRenderLayer":
                        cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                        oVal = cmds.getAttr(valString)
                        if oVal != defVal:
                            dicString = vop + "**" + "vrayObjProp" + "**" + op + "**" + rl
                            vrayObjectPropertyOvrideDIC[dicString] = oVal
        return(vrayObjectPropertyOvrideDIC)

    vraySettingsOverrideDic = {}
    transLayOverides = {}
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
        vraySettingsOverrideDic = vraySettingsOverides(objectsCheck,renderLayers)
    if Tcount == 1:
        OBJ_1_translations = translations(objectsCheck, renderLayers)
        transLayOverides = OBJ_1_translations[5]
    if Mcount == 1:
        OBJ_1_materialsAssignments = materialAssignments(objectsCheck, renderLayers)
        matAssignmentLayOverides = OBJ_1_materialsAssignments[4]

        materialsOverideDIC = materialOverides(objectsCheck,renderLayers)
        materialsOverideDIC.update(matAssignmentLayOverides)
    if Ccount == 1:
        cameraOveridesDIC = cameraOverides(objectsCheck,renderLayers)
    if Lcount == 1:
        lightOveridesDIC = lightOverides(objectsCheck,renderLayers)
    if Rcount == 1:
        OBJ_1_Render_Stats = Render_stat_Overides(objectsCheck_g, renderLayers)
        Render_Stats_Overides = OBJ_1_Render_Stats
    if VPcount == 1:
        OBJ_1_VrayObjectProps = vrayObjectPropO(renderLayers)
        vrayObjectPropertyOverides = OBJ_1_VrayObjectProps

    return(vraySettingsOverrideDic,transLayOverides,materialsOverideDIC,lightOveridesDIC,Render_Stats_Overides,vrayObjectPropertyOverides,cameraOveridesDIC)


#--- overide section over ----

def camAnalize():
    camRenDic = {}
    renderLayers = cmds.ls(type = "renderLayer")
    camList = cmds.ls(type = "camera")
    camList.append("none")
    camListOn = []

    for rl in renderLayers:
        cmds.editRenderLayerGlobals(currentRenderLayer = rl)
        for camm in camList:
            if camm != "none":
                name = camm + ".renderable"
                state = cmds.getAttr(name)
                if state == 1:
                    camListOn.append(camm)
                    camRenDicSTR = rl + "_" + camm
                    camRenDic[camRenDicSTR] = (camm + "_" + rl)
    return(camRenDic,camList)

def setRenCam(rl,camList,renCamMenu,renderLayers,*args):
    global initialLayer
    laySP = renCamMenu.split("|")
    lay = laySP[2]
    cmds.editRenderLayerGlobals(currentRenderLayer = lay)
    menuValue = cmds.optionMenu(renCamMenu,v = True, query = True)
    renCamSTR = menuValue + ".renderable"
    camStatedic = {}
    camListMod = cmds.ls(type = "camera")
    camListMod.append("perspShape")
    camListMod.append("topShape")
    camListMod.append("frontShape")
    camListMod.append("sideShape")
    for rll in renderLayers:
        cmds.editRenderLayerGlobals(currentRenderLayer = rll)
        for camm in camListMod:
            renState = cmds.getAttr(camm + ".renderable")
            curLay = cmds.editRenderLayerGlobals(currentRenderLayer = True,query = True)
            if renState == 1:
                camStatedic[(camm + "&" + rll)] = renState
    cmds.editRenderLayerGlobals(currentRenderLayer = lay)
    setCam = "none"
    if lay == "defaultRenderLayer":
        for cam in camListMod:
            if cam == menuValue:
                cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
                cmds.setAttr((cam + ".renderable"),1)
                setCam = cam
            else:
                cmds.setAttr(cam + ".renderable",0)
    if lay != "defaultRenderLayer":
        cmds.editRenderLayerGlobals(currentRenderLayer = lay)
        for cam in camListMod:
            if cam == menuValue:
                cmds.editRenderLayerAdjustment(cam + ".renderable")
                cmds.setAttr((cam + ".renderable"),1)
                setCam = cam
    cmds.editRenderLayerGlobals( currentRenderLayer = initialLayer)
    camColorCheck(renCamMenu,setCam)

def fixCams(*args):
    print 'fixCams running'
    global initialLayer
    intialLayer = cmds.editRenderLayerGlobals(currentRenderLayer = True, query = True)
    renderLayers = cmds.ls(type = "renderLayer")
    camListMod = cmds.ls(type = "camera")
    camListMod.append("perspShape")
    camListMod.append("topShape")
    camListMod.append("frontShape")
    camListMod.append("sideShape")
    for rll in renderLayers:
        if rll == "defaultRenderLayer":
            cmds.editRenderLayerGlobals(currentRenderLayer = rll)
            for cam in camListMod:
                if cam == "perspShape":
                    cmds.setAttr(cam + ".renderable",1)
        if rll != "defaultRenderLayer":
            cmds.editRenderLayerGlobals(currentRenderLayer = rll)
            for cam in camListMod:
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
                        camLayCompare = cam.split("Shape")
                        camLayCompare = camLayCompare[0] +  camLayCompare[1]
                    else:
                        camSP = cam.split("_")
                        camCut = camSP[0]
                        camLayCompare = camCut
                if var == 1:
                    if cam == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape":
                        camLayCompare = cam.split("Shape")
                        camLayCompare = camLayCompare[0] + camLayCompare[1]
                    else:
                        camSP = cam.split("_")
                        camCut = camSP[1]
                        camLayCompare = camCut.split("Shape")
                        camLayCompare = camLayCompare[0] + camLayCompare[1]
                if var == 2:
                    if cam == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape":
                        camLayCompare = cam.split("Shape")
                        camLayCompare = camLayCompare[0] + camLayCompare[1]
                    else:
                        camSP = cam.split("_")
                        camCut = camSP[1]
                        camLayCompare = camCut.split("Shape")
                        camLayCompare = camLayCompare[0]
                if var == 3:
                    if cam == "perspShape" or cam == "topShape" or cam == "frontShape" or cam == "sideShape" or cam == "backShape1" or cam == "backShape2":
                        if "2" not in cam:
                            camLayCompare = cam.split("Shape")
                            camLayCompare = camLayCompare[0] + camLayCompare[1]
                        if "2" in cam:
                            camLayCompare = cam.split("Shape")
                            camLayCompare = camLayCompare[0]
                    else:
                        camLayCompare = camCut.split("Shape")
                        camLayCompare = camLayCompare[0]
                camLayCompareSPb = camLayCompare.split("Shape")
                camLayCompareSPb = camLayCompareSPb[0]
                if camLayCompare == rll or (camLayCompareSPb + "_BTY") == rll or (camLayCompareSPb + "_REF") == rll or (camLayCompareSPb + "_SHD") == rll or (camLayCompareSPb + "_REF_MATTE") == rll or ("BTY_" + camLayCompareSPb) == rll:
                    cmds.editRenderLayerAdjustment(cam + ".renderable")
                    print 'setting ' + cam + ' for ' + rll + ' to 1 '
                    cmds.setAttr(cam + ".renderable",1)
                else:
                    cmds.editRenderLayerAdjustment(cam + ".renderable")
                    cmds.setAttr(cam + ".renderable",0)
    cmds.editRenderLayerGlobals(currentRenderLayer = initialLayer)
    layer_switcher()


def camColorCheck(renCamMenu,setCam):
    renCamSp = renCamMenu.split("|")
    layerLabel = renCamSp[2]
    cam = setCam
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
    camRegExA = ""
    if layerLabel != "defaultRenderLayer":
        if var == 0:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camRegExSp = setCam.split("Shape")
                camRegExA = camRegExSp[0]
                camRegExAsp = camRegExA.split("_")
                camRegExA = camRegExAsp[0]
            else:
                camRegExA = cam
        if var == 1:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camRegExSp = setCam.split("Shape")
                camRegExA = camRegExSp[0] + camRegExSp[1]
                camRegExAsp = camRegExA.split("_")
                camRegExA = camRegExAsp[1]
            else:
                camRegExA = cam
        if var == 2:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camRegEx = cam + "_"
                camRegExSp = camRegEx.split("_")
                camRegEx = camRegExSp[1]
                camRegEx = camRegEx.split("Shape")
                camRegExA = camRegEx[0]
            else:
                camRegExA = cam
        if var == 3:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camRegExSp = setCam.split("Shape")
                camRegExA = camRegExSp[0] + camRegExSp[1]
                camRegExAsp = camRegExA.split("_")
                camRegExA = camRegExAsp[1]
            else:
                camRegExA = cam
        if var == 4:
            if cam != "perspShape" and cam != "topShape" and cam != "frontShape" and cam != "sideShape":
                camRegExSp = setCam.split("Shape")
                camRegExA = camRegExSp[0]
            else:
                camRegExA = cam
        if layerLabel != "defaultRenderLayer":
            if camNum > 1:
                cmds.optionMenu(renCamMenu, v = cam, bgc = (1,.0,0),edit = True)
            if camNum == 1 and layerLabel == (camRegExA) or layerLabel == (camRegExA + "_BTY") or layerLabel == (camRegExA + "_REF") or layerLabel == (camRegExA + "_SHD") or layerLabel == (camRegExA + "_REF_MATTE") or layerLabel == ("BTY_" + camRegExA):
                cmds.optionMenu(renCamMenu, v = cam, bgc = (.5,.5,.5),edit = True)
            else:
                cmds.optionMenu(renCamMenu, v = cam , bgc = (1,0,0),edit = True)
        else:
            cmds.optionMenu(renCamMenu, v = cam, bgc = (.5,.5,.5),edit = True)

def unlockNodes(*args):
    cams = cmds.ls(type = "camera")
    for cam in cams:
        parentNode = cmds.listRelatives(cam, parent = True)
        Plockstate = cmds.lockNode(parentNode[0],lock = True, query = True)
        Plockstate = Plockstate[0]
        if Plockstate == 1:
            cmds.lockNode(parentNode[0], lock = 0)
        if "Shape" in cam:
            dad = cmds.listRelatives(cam, parent = True)
            dad = dad[0]
        else:
            dad = cam
        cmds.lockNode(cam, lock = 0)
        vizEx = cmds.attributeQuery("visibility", node = cam, exists = True)
        renEx = cmds.attributeQuery("renderable", node = cam, exists = True)
        if vizEx == 1:
            cmds.setAttr(dad + ".visibility", lock = 0)
        cmds.setAttr(dad + ".renderable", lock = 0)

def copyAllLayers(renderLayers,*args):
    copyAllLay = "B"
    copyLayers(renderLayers,copyAllLay)

def copyLayers(renderLayers,copyAllLay,*args):
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
        activeLayers = renderLayers
    objectsCheckCL_g = cmds.ls(g = True)
    objectsCheckCL_t = cmds.ls(type = "transform")
    objectsCheckCL_cam = cmds.ls(type = "camera")
    objectsCheckCL = objectsCheck_g + objectsCheck_t + objectsCheck_cam
    lightTypes = ["volumeLight","areaLight","spotLight","pointLight","directionalLight","ambientLight","VRayLightRectShape"]
    overides = overideInfoFunc(renderLayers)
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
    for rlll in activeLayers:
        if rlll != "defaultRenderLayer":
            obsInLay = cmds.editRenderLayerMembers( rlll, fn = True,query=True ) or []
            obsVizDic = {}
            for obCL in objectsCheckCL:
                vizEx = cmds.attributeQuery("visibility",node = obCL,exists = True)
                if vizEx == 1:
                    cmds.editRenderLayerGlobals(currentRenderLayer = rlll)
                    vizString = (obCL + ".visibility")
                    visState = cmds.getAttr(vizString)
                    strKey = (obCL + "%" + str(visState))
                    obsVizDic[strKey] = visState
            cmds.createRenderLayer(obsInLay, name = (rlll + "_copy"))
            cmds.editRenderLayerGlobals(currentRenderLayer = (rlll + "_copy"))
            cmds.rename(rlll,("**_" + rlll + "_old"))
            cmds.rename((rlll + "_copy"),rlll)
            cmds.delete(("**_" + rlll + "_old"))
            for objL in obsInLay:
                cmds.editRenderLayerMembers((rlll),objL)
            for ob in objectsCheck:
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
                for ob in objectsCheck:
                    if ob == tfoSP[1]:
                        if layer == rlll:
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
                for ob in objectsCheck:
                    if "spotLight" in ob or "ambientLight" in ob or "directionalLight" in ob or "pointLight" in ob:
                        kid = cmds.listRelatives(ob,children = True)
                        ob = kid[0]
                    if ob == loOBsp[0]:
                        if layer == rlll:
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
                            if layer == rlll:
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
                                    cmds.editRenderLayerAdjustment(mo,layer = rlll)
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
                            if layer == rlll:
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
                        if layer == rlll:
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
                        if layer == rlll:
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
                        if layer == rlll:
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
        fixCams()
        layer_switcher()

def checkRenderLayers(renLayOverCompare1,renLayOverCompare2,checkLayerFieldResult,txtFieldList,*args):
    menu1 = cmds.optionMenu(renLayOverCompare1,value = True,query = True)
    menu2 = cmds.optionMenu(renLayOverCompare2,value = True,query = True)
    oversMenu1 = ""
    oversMenu2 = ""
    for txtF in txtFieldList:
        txtFsp = txtF.split("|")
        txtFsp = txtFsp[2]
        if txtFsp == menu1:
            oversMenu1 = cmds.textField(txtF,text = True, query = True)
        if txtFsp == menu2:
            oversMenu2 = cmds.textField(txtF,text = True, query = True)
        oversMenu1SP = oversMenu1.split(",")
        oversMenu2SP = oversMenu2.split(",")
        diff1Edit = []
        diff2Edit = []
        diff = (list(set(oversMenu1SP) - set(oversMenu2SP)))
        for d in diff:
            d = d.replace("u' ","")
            d = d.replace(" '","")
            d = d.replace(" '","")
            if d != "":
                d = "diff:" + d
                diff1Edit.append(d)
        diff2 = (list(set(oversMenu2SP) - set(oversMenu1SP)))
        for d2 in diff2:
            d2 = d2.replace("u' ","")
            d2 = d2.replace(" '","")
            d2 = d2.replace(" '","")
            if d2 != "":
                d2 = "diff2:" + d2
                diff2Edit.append(d2)
        diffCombo = diff1Edit + diff2Edit
        diffCombo = str(diffCombo)
        diffCombo = diffCombo.replace("[u'","")
        diffCombo = diffCombo.replace("u'","")
        diffCombo = diffCombo.replace(" '","")
        diffCombo = diffCombo.replace("]","")
    checkLayerFieldResult = cmds.textField(checkLayerFieldResult,text = diffCombo, edit = True)

def layer_switcher():
    global initialLayer
    setCam = ""
    renderLayers = cmds.ls(type = "renderLayer")
    initialLayer = cmds.editRenderLayerGlobals(query = True, currentRenderLayer = True)
    camInfo = camAnalize()
    camFieldTextRaw = camInfo[0]
    renderCams = camInfo[1]
    name = "rebuild_render_layers"
    if (cmds.window(name, exists = True)):
        cmds.deleteUI(name)
    window = cmds.window(name, title = name, sizeable = False, widthHeight=(250, 50))
    cmds.columnLayout("mainColumn", adjustableColumn = True)
    renderLays = cmds.ls(type = "renderLayer")
    cmds.rowLayout(("objects1"), numberOfColumns = 1, parent = "mainColumn")
    but_copyALL_Layers = cmds.button(label = "copyALL_Layers")
    cmds.button(but_copyALL_Layers, command = partial(copyAllLayers,renderLayers), edit = True)
    cmds.editRenderLayerGlobals(currentRenderLayer = initialLayer)
    panels = cmds.getPanel( type = "modelPanel" )
    for mPanel in panels:
        cmds.modelEditor(mPanel, edit = True, allObjects = 1)
    rl = initialLayer
    cmds.showWindow()

def main():
    layer_switcher()

#main()
