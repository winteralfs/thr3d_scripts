import maya.cmds as cmds
import maya.mel as mel
from string import digits

def objectChooseWin():
    name = "object_replace"
    windowSize = (300,100)
    if (cmds.window(name, exists = True)):
        cmds.deleteUI(name)
    window = cmds.window(name, title = name, width = 100, height = 50)
    cmds.columnLayout("mainColumn", adjustableColumn = True)
    cmds.rowLayout("nameRowLayout01", numberOfColumns = 2, parent = "mainColumn")
    cmds.text(label = "object_Old  ")
    object_Old_Path = cmds.textField(tx = "object_Old")
    cmds.rowLayout("nameRowLayout02", numberOfColumns = 2, parent = "mainColumn")
    cmds.text(label = "object_New")
    object_New_Path = cmds.textField(tx = "object_New")

    def objects_CB(*args):
        object_Old = cmds.textField(object_Old_Path,q=1,tx=1)
        object_New = cmds.textField(object_New_Path,q=1,tx=1)
        objects(object_Old,object_New)
    cmds.rowLayout("nameRowLayout2.5", numberOfColumns = 10, parent = "mainColumn")
    cmds.text("--")

    cmds.rowLayout("nameRowLayout03", numberOfColumns = 10, parent = "mainColumn")
    checkBoxTranslations = cmds.checkBox(label = "translations", value = True)
    checkBoxMaterials = cmds.checkBox(label = "materials", value = True)
    checkBoxUVsets = cmds.checkBox(label = "UVsets", value = True)
    checkBoxLL = cmds.checkBox(label = "lightLinking", value = True)
    cmds.rowLayout("nameRowLayout04", numberOfColumns = 10, parent = "mainColumn")
    checkBoxObjectProps = cmds.checkBox(label = "objectProps", value = True)
    checkBoxRenderStats = cmds.checkBox(label = "renderStats", value = True)
    checkBoxExcludeListSets = cmds.checkBox(label = "sets", value = True)
    checkBoxALL = cmds.checkBox(label = "ALL+", value = True)

    cmds.rowLayout("nameRowLayout4.5", numberOfColumns = 10, parent = "mainColumn")
    cmds.text("--")
    cmds.rowLayout("nameRowLayout05", numberOfColumns = 1, parent = "mainColumn")
    cmds.button(label = "replace", command = (objects_CB))
    cmds.showWindow()

    def objects(object_Old,object_New):
        print " "
        print " "
        print "*"
        print " "
        print " "
        object_Old = object_Old
        object_New = object_New
        obj_kids_old = cmds.listRelatives(object_Old, children = True) or []
        obj_kids_new = cmds.listRelatives(object_New, children = True) or []
        obj_kids_old_len = len(obj_kids_old)
        obj_kids_new_len = len(obj_kids_new)
        if obj_kids_old_len == 0:
            object_old_split = object_Old.split("_")
            object_old_split_size = len(object_old_split)
            if "Shape" in object_old_split[object_old_split_size - 1]:
                old_kid_parent = cmds.listRelatives(object_Old, parent = True) or [[]]
                object_Old = old_kid_parent[0]
        if obj_kids_new_len == 0:
            object_new_split = object_New.split("_")
            object_new_split_size = len(object_new_split)
            if "Shape" in object_new_split[object_new_split_size - 1]:
                new_kid_parent = cmds.listRelatives(object_New, parent = True) or [[]]
                object_New = new_kid_parent[0]
        renderLayers = cmds.ls(type = 'renderLayer')
        currentRenderLayer = cmds.editRenderLayerGlobals( query = True, currentRenderLayer = True)
        print "object_Old = ",object_Old
        print "object_New = ",object_New
        print "current render layer is",currentRenderLayer
        def object_New_Center(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "New object centered in frame"
            print "---"
            print " "
            obj1 = object_Old
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            obj1_WorldSpace = cmds.xform(obj1,q = True, os = True,rotatePivot = True)
            cmds.xform(obj1,cp = True)
            obj1_WorldSpaceCentered = cmds.xform(obj1,q = True, ws = True,rotatePivot = True)
            old_transX = float(obj1_WorldSpaceCentered[0])
            old_transY = float(obj1_WorldSpaceCentered[1])
            old_transZ = float(obj1_WorldSpaceCentered[2])
            cmds.xform(obj1,rotatePivot = obj1_WorldSpace)
            obj1_WorldSpaceFixed = cmds.xform(obj1,q = True, os = True,rotatePivot = True)
            obj2 = object_New
            obj2_WorldSpace = cmds.xform(obj2,q = True, os = True,rotatePivot = True)
            cmds.xform(obj2,cp = True)
            obj2_WorldSpaceCentered = cmds.xform(obj2,q = True, ws = True,rotatePivot = True)
            new_transX = float(obj2_WorldSpaceCentered[0])
            new_transY = float(obj2_WorldSpaceCentered[1])
            new_transZ = float(obj2_WorldSpaceCentered[2])
            transXdiff = (old_transX - new_transX)
            print "transXdiff = ",transXdiff
            transYdiff = (old_transY - new_transY)
            print "transYdiff = ",transYdiff
            transZdiff = (old_transZ - new_transZ)
            print "transZdiff = ",transZdiff
            cmds.xform(obj2,r = True, t = (transXdiff,transYdiff,transZdiff))
            cmds.xform(obj2,rotatePivot = obj2_WorldSpace)
            obj2_WorldSpaceFixed = cmds.xform(obj2,q = True, os = True,rotatePivot = True)

        def master_path(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object path"
            print "---"
            print " "
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            pathOBJ = cmds.listRelatives(object_Old, fullPath = True) or []
            pathmasterObj = pathOBJ[0]
            si = len(pathOBJ)
            if si > 0:
                print pathmasterObj
            else:
                print "parent object selected"
            return pathmasterObj,object_Old,object_New,pathOBJ

        def renderLayerCheck(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object render layers"
            print "---"
            print " "
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            layerList = []
            RL = renderLayers
            sizeLayers = len(RL)
            for layer in RL:
                checkLayer = cmds.editRenderLayerMembers( layer, query = True ) or []
                checkLayerSize = len(checkLayer)
                if checkLayerSize > 0:
                    sizCkLayer = len(checkLayer)
                    for cko in checkLayer:
                        if cko == (object_Old):
                            layerList.append(layer)
            print layerList
            return layerList,object_Old,object_New

        def translations(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object transforms"
            print "---"
            print " "
            transValuesDict = {}
            objInLayers = []
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            object_Old = object_Old
            if "Shape" in object_Old:
                par = cmds.listRelatives(object_Old, parent = True)
                object_Old = par[0]
            RL = renderLayers
            for L in RL:
                objList = cmds.editRenderLayerMembers( L, query=True ) or []
                for obj in objList:
                    object_Old = object_Old
                    if object_Old == obj:
                        objInLayers.append(L)
            for lay in objInLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = lay )
                strTransX = object_Old + ".translateX"
                transX = cmds.getAttr(strTransX)
                var = object_Old + "_" + lay + "_transX"
                transValuesDict[var] = transX
                strTransY = object_Old + ".translateY"
                transY = cmds.getAttr(strTransY)
                var = object_Old + "_" + lay + "_transY"
                transValuesDict[var] = transY
                strTransZ = object_Old + ".translateZ"
                transZ = cmds.getAttr(strTransZ)
                var = object_Old + "_" + lay + "_transZ"
                transValuesDict[var] = transZ
                strRotX = object_Old + ".rotateX"
                rotX = cmds.getAttr(strRotX)
                var = object_Old + "_" + lay + "_rotX"
                transValuesDict[var] = rotX
                strRotY = object_Old + ".rotateY"
                rotY = cmds.getAttr(strRotY)
                var = object_Old + "_" + lay + "_rotY"
                transValuesDict[var] = rotY
                strRotZ = object_Old + ".rotateZ"
                rotZ = cmds.getAttr(strRotZ)
                var = object_Old + "_" + lay + "_rotZ"
                transValuesDict[var] = rotZ
                strScaleX = object_Old + ".scaleX"
                scaleX = cmds.getAttr(strScaleX)
                var = object_Old + "_" + lay + "_scaleX"
                transValuesDict[var] = scaleX
                strScaleY = object_Old + ".scaleY"
                scaleY = cmds.getAttr(strScaleY)
                var = object_Old + "_" + lay + "_scaleY"
                transValuesDict[var] = scaleY
                strScaleZ = object_Old + ".scaleZ"
                scaleZ = cmds.getAttr(strScaleZ)
                var = object_Old + "_" + lay + "_scaleZ"
                transValuesDict[var] = scaleZ
            print object_Old + " defaultRenderLayer translation values:"
            print "----"
            defVals = []
            for tv in transValuesDict:
                if "defaultRenderLayer" in tv:
                    defVals.append(tv)
            for A in defVals:
                if "transX" in A:
                    transX_val = transValuesDict[A]
            for A in defVals:
                if "transY" in A:
                    transY_val = transValuesDict[A]
            for A in defVals:
                if "transZ" in A:
                    transZ_val = transValuesDict[A]
            for A in defVals:
                if "rotX" in A:
                    rotX_val = transValuesDict[A]
            for A in defVals:
                if "rotY" in A:
                    rotY_val = transValuesDict[A]
            for A in defVals:
                if "rotZ" in A:
                    rotZ_val = transValuesDict[A]
            for A in defVals:
                if "scaleX" in A:
                    scaleX_val = transValuesDict[A]
            for A in defVals:
                if "scaleY" in A:
                    scaleY_val = transValuesDict[A]
            for A in defVals:
                if "scaleZ" in A:
                    scaleZ_val = transValuesDict[A]
            transLayerOveride = []
            for dic in transValuesDict:
                if "transX" in dic:
                    val = transValuesDict[dic]
                    if val != transX_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "transY" in dic:
                    val = transValuesDict[dic]
                    if val != transY_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "transZ" in dic:
                    val = transValuesDict[dic]
                    if val != transZ_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "rotX" in dic:
                    val = transValuesDict[dic]
                    if val != rotX_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "rotY" in dic:
                    val = transValuesDict[dic]
                    if val != rotY_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "rotZ" in dic:
                    val = transValuesDict[dic]
                    if val != rotZ_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "scaleX" in dic:
                    val = transValuesDict[dic]
                    if val != scaleX_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "scaleY" in dic:
                    val = transValuesDict[dic]
                    if val != scaleY_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "scaleZ" in dic:
                    val = transValuesDict[dic]
                    if val != scaleZ_val:
                        transLayerOveride.append(dic)
            defValList = [transX_val,transY_val,transZ_val,rotX_val,rotY_val,rotZ_val,scaleX_val,scaleY_val,scaleZ_val]
            sizL = len(transLayerOveride)
            if sizL > 0:
                print " "
                print "translation renderLayerOverides detected in:",transLayerOveride
            else:
                print " "
                print "no transform render layer overides detected"
            return transValuesDict,object_Old,object_New,defVals,defValList,objInLayers,transLayerOveride

        def excludeListSets(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object exclude sets"
            print "---"
            print " "
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            tmpOBJ = object_Old
            if "Shape" in tmpOBJ:
                object_Old_Parent = cmds.listRelatives(object_Old, parent = True) or []
                object_Old_Child = object_Old
                object_Old = object_Old_Parent
            if "Shape" not in tmpOBJ:
                objectChild = cmds.listRelatives(object_Old, children = True) or []
                object_Old_Child = objectChild
                object_Old_Parent = object_Old
            setsINC = []
            exTextures = []
            allNodes = cmds.ls(long = True, type = "VRayRenderElement")
            for node in allNodes:
                if "Extra_Tex" in node:
                    exTextures.append(node)
            for exTex in exTextures:
                listItems = cmds.listConnections(exTex) or []
                listSiz = len(listItems)
                for LI in listItems:
                    if "extratex" in LI:
                        setMembers = cmds.listConnections(LI) or []
                        for A in setMembers:
                            if object_Old == A:
                                setsINC.append(LI)
                        for A in setMembers:
                            if object_Old_Child == A:
                                setsINC.append(LI)
            sizeL = len(setsINC)
            if sizeL > 0:
                print "sets used by a VRAY Extra_Tex that contain " + object_Old + " = ", setsINC
            else:
                print object_Old + " detected in no exlude sets"
            return setsINC,object_Old,object_New

        def lightLinking(object_Old,object_New,renderLayers):
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            tmpOBJ = object_Old
            lightLinkingDict = []
            if "Shape" in tmpOBJ:
                object_Old_Parent = cmds.listRelatives(object_Old, parent = True) or []
                object_Old_Child = object_Old
                object_Old = object_Old_Parent
            if "Shape" not in tmpOBJ:
                objectChild = cmds.listRelatives(object_Old, children = True) or []
                object_Old_Child = objectChild
                object_Old_Parent = object_Old
                cmds.select(object_Old)
                ltsL = cmds.lightlink( query=True, object = object_Old)
            ltsLL = []
            ltsLL = ltsL
            print "lights linked to " + object_Old + " are:", ltsLL
            return ltsLL,object_Old,object_New

        def renderStats(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object render stats"
            print "---"
            print " "
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            objParent = cmds.listRelatives(object_Old, parent = True) or []
            objChild = cmds.listRelatives(object_Old, children = True) or []
            renderStatsDic = {}
            if "Shape" in object_Old:
                objParent = objParent
                objChild = object_Old
                object_Old = objChild
            else:
                objParent = object_Old
                objChild = objChild
                object_Old = objChild
            RLOs = cmds.ls(type = "renderLayer")
            for RL in RLOs:
                cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                print " "
                print "renderLayer = ", RL
                print " "
                castsShadowsV = object_Old[0] + ".castsShadows"
                castsShadowsVAR = cmds.getAttr(castsShadowsV)
                castsShadowsKEY = object_Old[0] + "_" + RL + "_castsShadows"
                renderStatsDic[castsShadowsKEY] = castsShadowsVAR
                receiveShadowsV = object_Old[0] + ".receiveShadows"
                receiveShadowsVAR = cmds.getAttr(receiveShadowsV)
                receiveShadowsKEY = object_Old[0] + "_" + RL + "_receiveShadows"
                renderStatsDic[receiveShadowsKEY] = receiveShadowsVAR
                motionBlurV = object_Old[0] + ".motionBlur"
                motionBlurVAR = cmds.getAttr(motionBlurV)
                motionBlurKEY = object_Old[0] + "_" + RL + "_motionBlur"
                renderStatsDic[motionBlurKEY] = motionBlurVAR
                primaryVisibilityV = object_Old[0] + ".primaryVisibility"
                primaryVisibilityVAR = cmds.getAttr(primaryVisibilityV)
                primaryVisibilityKEY = object_Old[0] + "_" + RL + "_primaryVisibility"
                renderStatsDic[primaryVisibilityKEY] = primaryVisibilityVAR
                smoothShadingV = object_Old[0] + ".smoothShading"
                smoothShadingVAR = cmds.getAttr(smoothShadingV)
                smoothShadingKEY = object_Old[0] + "_" + RL + "_smoothShading"
                renderStatsDic[smoothShadingKEY] = smoothShadingVAR
                visibleInReflectionsV = object_Old[0] + ".visibleInReflections"
                visibleInReflectionsVAR = cmds.getAttr(visibleInReflectionsV)
                visibleInReflectionsKEY = object_Old[0] + "_" + RL + "_visibleInReflections"
                renderStatsDic[visibleInReflectionsKEY] = visibleInReflectionsVAR
                visibleInRefractionsV = object_Old[0] + ".visibleInRefractions"
                visibleInRefractionssVAR = cmds.getAttr(visibleInRefractionsV)
                visibleInRefractionsKEY = object_Old[0] + "_" + RL + "_visibleInRefractions"
                renderStatsDic[visibleInRefractionsKEY] = visibleInRefractionssVAR
                doubleSidedV = object_Old[0] + ".doubleSided"
                doubleSidedVAR = cmds.getAttr(doubleSidedV)
                doubleSidedKEY = object_Old[0] + "_" + RL + "_doubleSided"
                renderStatsDic[doubleSidedKEY] = doubleSidedVAR
            defRSlist = []
            NONdefRSlist = []
            for defi in renderStatsDic:
                if "default" in defi:
                    defRSlist.append(defi)
                else:
                    NONdefRSlist.append(defi)
            for defiVar in defRSlist:
                if "castsShadows" in defiVar:
                    defaultVal_castsShadows = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "receiveShadows" in defiVar:
                    defaultVal_receiveShadows = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "motionBlur" in defiVar:
                    defaultVal_motionBlur = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "primaryVisibility" in defiVar:
                    defaultVal_primaryVisibility = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "smoothShading" in defiVar:
                    defaultVal_smoothShading = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "visibleInReflections" in defiVar:
                    defaultVal_visibleInReflections = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "visibleInRefractions" in defiVar:
                    defaultVal_refractionVisibility = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "doubleSided" in defiVar:
                    defaultVal_doubleSided = renderStatsDic[defiVar]
            RS_overRideList = []
            for NDL in NONdefRSlist:
                if "castsShadows" in NDL:
                    Val_ND_castsShadows = renderStatsDic[NDL]
                    if Val_ND_castsShadows != defaultVal_castsShadows:
                        RS_overRideList.append(NDL)
                if "receiveShadows" in NDL:
                    Val_ND_receiveShadows = renderStatsDic[NDL]
                    if Val_ND_receiveShadows != defaultVal_receiveShadows:
                        RS_overRideList.append(NDL)
                if "motionBlur" in NDL:
                    Val_ND_motionBlur = renderStatsDic[NDL]
                    if Val_ND_motionBlur != defaultVal_motionBlur:
                        RS_overRideList.append(NDL)
                if "primaryVisibility" in NDL:
                    Val_ND_primaryVisibility = renderStatsDic[NDL]
                    if Val_ND_primaryVisibility != defaultVal_primaryVisibility:
                        RS_overRideList.append(NDL)
                if "smoothShading" in NDL:
                    Val_ND_smoothShading = renderStatsDic[NDL]
                    if Val_ND_smoothShading != defaultVal_smoothShading:
                        RS_overRideList.append(NDL)
                if "visibleInReflections" in NDL:
                    Val_ND_visibleInReflections = renderStatsDic[NDL]
                    if Val_ND_visibleInReflections != defaultVal_visibleInReflections:
                        RS_overRideList.append(NDL)
                if "visibleInRefractions" in NDL:
                    Val_ND_refractionVisibility = renderStatsDic[NDL]
                    if Val_ND_refractionVisibility != defaultVal_refractionVisibility:
                        RS_overRideList.append(NDL)
                if "doubleSided" in NDL:
                    Val_ND_doubleSided = renderStatsDic[NDL]
                    if Val_ND_doubleSided != defaultVal_doubleSided:
                        RS_overRideList.append(NDL)
            print " "
            rss = len(RS_overRideList)
            if rss > 0:
                print "suspected renderState layer overides in, ", RS_overRideList
            if rss == 0:
                print "no renderState layer overides detected"
            return RS_overRideList,object_Old,object_New,defRSlist,RS_overRideList,renderStatsDic,RLOs

        def objectProptertyOverides(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object VRAY object properties"
            print "---"
            print " "
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            objParent = cmds.listRelatives(object_Old, parent = True) or []
            objChild = cmds.listRelatives(object_Old, children = True) or []
            VoBpropertyDic = {}
            defVPlist = []
            NONdefVPlist = []
            objectIDo = "False"
            vpOPid = 0
            if "Shape" in object_Old:
                objParent = objParent
                objChild = object_Old
                object_Old = objParent
            else:
                objParent = object_Old
            opList = cmds.ls(type = "VRayObjectProperties")
            OPlist = []
            for op in opList:
                chilRel = cmds.listRelatives(op) or []
                chilCon = cmds.listConnections(op) or []
                for chiRel in chilRel:
                    if object_Old in chiRel:
                        if op not in OPlist:
                            OPlist.append(op)
                for chiCon in chilCon:
                    if object_Old in chiCon:
                        if op not in OPlist:
                            OPlist.append(op)
            RLOs = cmds.ls(type = "renderLayer")
            for VP in OPlist:
                vpOPid = 0
                for RL in RLOs:
                    cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                    print " "
                    print "renderLayer = ", RL
                    print " "
                    objectIDo = cmds.getAttr(VP + ".objectIDEnabled")
                    if objectIDo == 1:
                        vpOPid = cmds.getAttr(VP + ".objectID")
                    VP_giVisibility = cmds.getAttr(VP + ".giVisibility")
                    giVisibilityKEY = VP + "_" + RL + "_giVisibility"
                    VoBpropertyDic[giVisibilityKEY] = VP_giVisibility
                    VP_primaryVisibility = cmds.getAttr(VP + ".primaryVisibility")
                    primaryVisibilityKEY = VP + "_" + RL + "_primaryVisibility"
                    VoBpropertyDic[primaryVisibilityKEY] = VP_primaryVisibility
                    VP_reflectionVisibility = cmds.getAttr(VP + ".reflectionVisibility")
                    reflectionVisibilityKEY = VP + "_" + RL + "_reflectionVisibility"
                    VoBpropertyDic[reflectionVisibilityKEY] = VP_reflectionVisibility
                    VP_refractionVisibility = cmds.getAttr(VP + ".refractionVisibility")
                    refractionVisibilityKEY = VP + "_" + RL + "_refractionVisibility"
                    VoBpropertyDic[refractionVisibilityKEY] = VP_refractionVisibility
                    VP_shadowVisibility = cmds.getAttr(VP + ".shadowVisibility")
                    shadowVisibilityKEY = VP + "_" + RL + "_shadowVisibility"
                    VoBpropertyDic[shadowVisibilityKEY] =VP_shadowVisibility
                    VP_receiveShadows  = cmds.getAttr(VP + ".receiveShadows")
                    receiveShadowsKEY = VP + "_" + RL + "_receiveShadows"
                    VoBpropertyDic[receiveShadowsKEY] = VP_receiveShadows
                    VP_generateGIMultiplier  = cmds.getAttr(VP + ".generateGIMultiplier")
                    generateGIMultiplierKEY = VP + "_" + RL + "_generateGIMultiplier"
                    VoBpropertyDic[generateGIMultiplierKEY] = VP_generateGIMultiplier
                    VP_receiveGIMultiplier  = cmds.getAttr(VP + ".receiveGIMultiplier")
                    receiveGIMultiplierKEY = VP + "_" + RL + "_receiveGIMultiplier"
                    VoBpropertyDic[receiveGIMultiplierKEY] = VP_receiveGIMultiplier
            for defiVP in VoBpropertyDic:
                if "default" in defiVP:
                    defVPlist.append(defiVP)
                else:
                    NONdefVPlist.append(defiVP)
            defaultValDic = {}
            for defiVPVar in defVPlist:
                if "giVisibility" in defiVPVar:
                    defaultVal_giVisibility = VoBpropertyDic[defiVPVar]
                    defaultValDic["giVisibility"] = defaultVal_giVisibility
            for defiVPVar in defVPlist:
                if "primaryVisibility" in defiVPVar:
                    defaultVal_primaryVisibility = VoBpropertyDic[defiVPVar]
                    defaultValDic["primaryVisibility"] = defaultVal_primaryVisibility
            for defiVPVar in defVPlist:
                if "reflectionVisibility" in defiVPVar:
                    defaultVal_reflectionVisibility = VoBpropertyDic[defiVPVar]
                    defaultValDic["reflectionVisibility"] = defaultVal_reflectionVisibility
            for defiVPVar in defVPlist:
                if "refractionVisibility" in defiVPVar:
                    defaultVal_refractionVisibility = VoBpropertyDic[defiVPVar]
                    defaultValDic["refractionVisibility"] = defaultVal_refractionVisibility
            for defiVPVar in defVPlist:
                if "shadowVisibility" in defiVPVar:
                    defaultVal_shadowVisibility = VoBpropertyDic[defiVPVar]
                    defaultValDic["shadowVisibility"] = defaultVal_shadowVisibility
            for defiVPVar in defVPlist:
                if "receiveShadows" in defiVPVar:
                    defaultVal_receiveShadows = VoBpropertyDic[defiVPVar]
                    defaultValDic["receiveShadows"] = defaultVal_receiveShadows
            for defiVPVar in defVPlist:
                if "generateGIMultiplier" in defiVPVar:
                    defaultVal_generateGIMultiplier = VoBpropertyDic[defiVPVar]
                    defaultValDic["generateGIMultiplier"] = defaultVal_generateGIMultiplier
            for defiVPVar in defVPlist:
                if "receiveGIMultiplier" in defiVPVar:
                    defaultVal_receiveGIMultiplier = VoBpropertyDic[defiVPVar]
                    defaultValDic["receiveGIMultiplier"] = defaultVal_receiveGIMultiplier
            VP_overRideList = []
            for NDL in NONdefVPlist:
                if "giVisibility" in NDL:
                    Val_ND_giVisibility = VoBpropertyDic[NDL]
                    if Val_ND_giVisibility != defaultVal_giVisibility:
                        VP_overRideList.append(NDL)
                if "primaryVisibility" in NDL:
                    Val_ND_primaryVisibility = VoBpropertyDic[NDL]
                    if Val_ND_primaryVisibility != defaultVal_primaryVisibility:
                        VP_overRideList.append(NDL)
                if "reflectionVisibility" in NDL:
                    Val_ND_reflectionVisibility = VoBpropertyDic[NDL]
                    if Val_ND_reflectionVisibility != defaultVal_reflectionVisibility:
                        VP_overRideList.append(NDL)
                if "refractionVisibility" in NDL:
                    Val_ND_refractionVisibility = VoBpropertyDic[NDL]
                    if Val_ND_refractionVisibility != defaultVal_refractionVisibility:
                        VP_overRideList.append(NDL)
                if "shadowVisibility" in NDL:
                    Val_ND_shadowVisibility = VoBpropertyDic[NDL]
                    if Val_ND_shadowVisibility != defaultVal_shadowVisibility:
                        VP_overRideList.append(NDL)
                if "receiveShadows" in NDL:
                    Val_ND_receiveShadows = VoBpropertyDic[NDL]
                    if Val_ND_receiveShadows != defaultVal_receiveShadows:
                        VP_overRideList.append(NDL)
                if "generateGIMultiplier" in NDL:
                    Val_ND_generateGIMultiplier = VoBpropertyDic[NDL]
                    if Val_ND_generateGIMultiplier != defaultVal_generateGIMultiplier:
                        VP_overRideList.append(NDL)
                if "receiveGIMultiplier" in NDL:
                    Val_ND_receiveGIMultiplier = VoBpropertyDic[NDL]
                    if Val_ND_receiveGIMultiplier != defaultVal_receiveGIMultiplier:
                        VP_overRideList.append(NDL)
            sizLL = len(VP_overRideList)
            if sizLL > 0:
                print "Suspected Vray object properties layer overides in: ", VP_overRideList
            else:
                print "no Vray object property render layer overides detecred"
            print " "
            return VP_overRideList,object_Old,object_New,VoBpropertyDic,defVPlist,defaultValDic,RLOs,OPlist,objectIDo,vpOPid

        def objectIDnode(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object ID"
            print "---"
            print " "
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            objID = "None"
            objectID_dic = {}
            if "Shape" in object_Old:
                objectIDnode = object_Old + ".vrayObjectID"
            else:
                chil = cmds.listRelatives(object_Old, children = True)
                object_Old = chil
                objectIDnode = object_Old[0] + ".vrayObjectID"
            ext = cmds.objExists(objectIDnode)
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            RLOs = cmds.ls(type = "renderLayer")
            if ext == 1:
                objID = cmds.getAttr(objectIDnode)
                print "default render layer objectID exists and is",objID
                for RL in RLOs:
                    cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                    objIDl = cmds.getAttr(objectIDnode)
                    if objIDl != objID:
                        objectID_dic[RL] = objIDl
                        print "ObjectID render layer overide detected in layers: " + RL + ":" + str(objIDl)
            else:
                print "no VRAY object ID attribute detected"
            return objID,object_Old,object_New,objectID_dic,RLOs


        def materials(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object materials"
            print "---"
            print " "
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            mats_list = {}
            mats_list_OVR = []
            LayerMats_dic = {}
            mats_dict = {}
            mats_faceDict = {}
            mats_objectList = {}
            mats_objectList_clean = []
            mats_objectList_clean_BASE = []
            spltMatList = []
            spltMatList2 = []
            layerOverM2  = {}
            RLM = cmds.ls(type = "renderLayer")
            for M in RLM:
                cmds.editRenderLayerGlobals( currentRenderLayer = M )
                cmds.select(clear = True)
                cmds.select(object_Old)
                cmds.hyperShade(smn = True)
                mats_list = cmds.ls(sl = True)
                for MM in mats_list:
                    NT = cmds.nodeType(MM)
                    if NT != "renderLayer":
                        mats_list_OVR.append(MM)
                for matsInc in mats_list_OVR:
                    cmds.select(matsInc)
                    LayerMats_dic[M] = matsInc
                    cmds.hyperShade(o = matsInc)
                    mats_objectList = cmds.ls(sl = True)
                    for mo in mats_objectList:
                        if object_Old in mo:
                            mats_objectList_clean.append(mo)
                    matAssignsExist = len(mats_objectList_clean)
                    for moc in mats_objectList_clean:
                        baseO = cmds.listRelatives(moc, parent = True)
                        if baseO not in mats_objectList_clean_BASE:
                            mats_objectList_clean_BASE.append(baseO)
                    layer_Mats_Inc = M + "_" + matsInc + "_"
                    for moc in mats_objectList_clean:
                        baseO = cmds.listRelatives(moc, parent = True)
                        if baseO not in mats_objectList_clean_BASE:
                            mats_objectList_clean_BASE.append(baseO)
                    emptyListTest = len(mats_objectList)
                    emptyListTest2 = len(mats_objectList_clean_BASE)
                    if emptyListTest > 0:
                        if emptyListTest2 > 0:
                            mats_dict[layer_Mats_Inc] = mats_objectList_clean_BASE[0]
                spltMatList.append(matsInc)
            sz = len(spltMatList)
            szz = sz - 1
            aa = 0
            layerOverM = []
            FDRL = 0
            for findDRL in RLM:
                if "defaultRenderLayer" in findDRL:
                    defaultRenderLayerPosition = FDRL
                FDRL += 1
            FDRL = int(FDRL)
            for L in RLM:
                a = 0
                for m in mats_dict:
                    if L in m:
                        key = L + "*" + str(a)
                        layerOverM2[key] = m
                        a=a+1
            RlayerOlist = []
            for LO in layerOverM2:
                if "defaultRenderLayer" in LO:
                    defVal = layerOverM2[LO]
            for LO in layerOverM2:
                valu = layerOverM2[LO]
                if defVal != valu:
                    RlayerOlist.append(LO)
            cmds.select(clear = True)
            if matAssignsExist == 0:
                print " "
                print "WARNING: no material assignments found for object: ",object_Old
                print " "
            print " "
            print "potential material layer overide detected in layers:",RlayerOlist
            print " "
            cmds.select(clear = True)
            return mats_dict,LayerMats_dic,layerOverM2,object_Old,object_New,RLM,matAssignsExist

        def UVsetLinking(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object UV sets"
            print "---"
            print " "
            UvSetTexturesDict = {}
            uvAddress = []
            setAddressOLD = ""
            uvAddDic = {}
            uvNameDic = {}
            texADDdic = {}
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            renderLayers = cmds.ls(type = "renderLayer")
            tmpOBJ = object_Old
            lightLinkingDict = []
            if "Shape" in tmpOBJ:
                object_Old_Parent = cmds.listRelatives(object_Old, parent = True) or []
                object_Old_Child = object_Old
                object_Old = object_Old_Parent
                object_Old = tmpOBJ
            if "Shape" not in tmpOBJ:
                objectChild = cmds.listRelatives(object_Old, children = True) or []
                object_Old_Child = objectChild
                object_Old_Parent = object_Old
                object_Old = object_Old_Child
            object_Old = object_Old[0]
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            cmds.select(clear = True)
            cmds.select(object_Old)
            obj_UVsets = cmds.polyUVSet( query=True, allUVSets=True )
            cmds.select(clear = True)
            textures = cmds.ls(type = "file")
            for tex in textures:
                setAddress = cmds.uvLink(query = True, texture = tex) or []
                for set in setAddress:
                    if object_Old in set:
                        setAddressOLD = set
                        setName = cmds.getAttr(setAddressOLD)
                        uvAddress.append(setAddressOLD)
                        uvAddDic[str(setAddressOLD)] = tex
                        uvNameDic[setName] = setAddressOLD
                        texADDdic[tex] = setAddressOLD
            print "obj_UVsets = ",obj_UVsets
            return uvNameDic,texADDdic,uvAddDic,uvAddress,obj_UVsets,object_Old,object_New,renderLayers

        def polySmoothOBJ(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object polySmooth detection"
            print "---"
            print " "
            object_Old_smooth_node_found = 0
            object_New_smooth_node_found = 0
            object_Old_smooth_division_level = 0
            object_New_smooth_division_level = 0
            smoothNodes = cmds.ls(type = "polySmoothFace")
            for smoothNode in smoothNodes:
                smooth_node_connections = cmds.listConnections(smoothNode,source = False, destination = True)
                for connection in smooth_node_connections:
                    if connection == object_Old:
                        object_Old_smooth_node_found = 1
                        object_Old_smooth_division_level = cmds.polySmooth(smoothNode, query = True, divisions = True)
                    if connection == object_New:
                        object_New_smooth_division_level = cmds.polySmooth(smoothNode, query = True, divisions = True)
                        object_New_smooth_node_found = 1
            return object_Old,object_New,object_Old_smooth_node_found,object_New_smooth_node_found,object_Old_smooth_division_level,object_New_smooth_division_level

        def visibilty(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object visibility"
            print "---"
            print " "
            visDic = {}
            vizPath = object_Old + ".visibility"
            for R in renderLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = R)
                vis = cmds.getAttr(vizPath)
                visDic[R] = vis
            return visDic,object_Old, object_New

        def displacementNodes(object_Old,object_New,renderLayers):
            print " "
            print "---"
            print "Master object displacement node"
            print "---"
            print " "
            vrayDisplacement_filePath = ""
            object_Old_DispNodeList = []
            vrayDispNode = []
            object_Old_DispNode = "None"
            dispNodeConnections = []
            fileConnections = []
            displacement_map_con = []
            disp_fileConnection = []
            displacement_map_connection = []
            disp_fileConnect = ""
            dispValDic = {}
            overide_dispValDic = {}
            dispLayerOR = []
            UVdic = {}
            UVdic_texSet = {}
            UVdic_label = {}
            conNodeDic = {}
            layerTexFiles = []
            layerTexDispTextures = []
            ramplayerConnects = []
            UvchooseRampC = []
            fileTextureName = ""
            def_fileTextureName = ""
            def_vrayDisplacementAmount = 0
            def_dispShift = 0
            def_vrayEdgeLength = 0
            def_dispMaxSubdivs = 0
            displacementBlackBox = 0
            overrideGlobalDisplacement = 0
            displacement_keepContinuity = 0
            layerTexDetect = 0
            rampDetect = 0
            object_Old = object_Old
            object_New = object_New
            cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
            if "Shape" in object_Old:
                parents = cmds.listRelatives(object_Old, parent = True) or []
                object_OldParent = parents
                object_Old = object_OldParent[0]
                object_OldChild = object_Old
            else:
                children = cmds.listRelatives(object_Old, children = True) or []
                object_OldParent = object_Old
                object_Old = object_Old
                object_OldChild = children
            dispNodes = cmds.ls(type = "VRayDisplacement") or []
            print "dispNodes = ",dispNodes
            for DN in dispNodes:
                dispChildren = cmds.listConnections(DN) or []
                if object_Old in dispChildren:
                    object_Old_DispNodeList.append(DN)
            lsSize = len(object_Old_DispNodeList)
            if lsSize > 0:
                object_Old_DispNode = object_Old_DispNodeList[0]
            if object_Old_DispNode != "None":
                object_Old_DispNode = object_Old_DispNodeList[0]
                object_Old_DispNode = object_Old_DispNodeList[0]
                for RL in renderLayers:
                    print " "
                    print "renderLayer = ", RL
                    print "****"
                    cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                    dispNodeConnections = cmds.listConnections(object_Old_DispNode, s = True, d = True) or []
                    for dnc in dispNodeConnections:
                        NT = cmds.nodeType(dnc)
                        if NT == "file":
                            if dnc not in displacement_map_connection:
                                displacement_map_connection = dnc
                                dcon = dnc
                                key_dcon = object_Old + "_" + RL + "_" + "dcon"
                                dispValDic[key_dcon] = dcon
                        if NT == "VRayMtl":
                            if dnc not in displacement_map_connection:
                                displacement_map_connection = dnc
                                dcon = dnc
                                key_dcon = object_Old + "_" + RL + "_" + "dcon"
                                dispValDic[key_dcon] = dcon
                        if NT == "layeredTexture":
                            layerTexDetect = 1
                            layerConnects = cmds.listConnections(dnc, destination = False)
                            for l in layerConnects:
                                if l != "defaultTextureList1":
                                    if l not in layerTexFiles:
                                        layerTexFiles.append(l)
                            for ltf in layerTexFiles:
                                gts = ltf + ".fileTextureName"
                                atExist = cmds.attributeQuery("fileTextureName", node = ltf, ex = True)
                                if atExist == 1:
                                    layerDispTex = cmds.getAttr(gts)
                                    if layerDispTex not in layerTexDispTextures:
                                        layerTexDispTextures.append(layerDispTex)
                        if NT == "ramp":
                            rampDetect = 1
                            rampNode = dnc
                            vrayDisplacement_filePath = "none"
                            disp_fileConnect = "none"
                            displacement_map_connection = rampNode
                            ramplayerConnects = cmds.listConnections(dnc, destination = False)
                            ramplayerC_2DplaceTex = ramplayerConnects[0]
                            UvchooseRampC = cmds.listConnections(ramplayerC_2DplaceTex, destination = False)
                            UvchooseRamp = UvchooseRampC[0]
                            rampCnoPlugs = cmds.listConnections(UvchooseRamp, destination = False)
                            for rcnp in rampCnoPlugs:
                                if object_Old in rcnp:
                                    rampCs = cmds.listConnections(UvchooseRamp, destination = False, plugs = True)
                                    for rcs in rampCs:
                                        if object_Old in rcs:
                                            rampUVset = rcs
                    displacement_map_connection_size = len(displacement_map_connection)
                    DNT = cmds.nodeType(displacement_map_connection)
                    if DNT == "file":
                        fileName = dnc
                        fileConnectionString = dnc + ".fileTextureName"
                        disp_fileConnect = DNT
                        key_dfc = object_Old + "_" + RL + "_" + "disp_fileConnect"
                        dispValDic[key_dfc] = disp_fileConnect
                        vrayDisplacement_filePath = cmds.getAttr(fileConnectionString)
                        texSet = cmds.uvLink( query = True, texture = dnc )
                        e = len(texSet)
                        if e > 0 :
                            label = cmds.getAttr(texSet)
                            UVdic_texSet[dnc] = texSet
                            UVdic_label[dnc] = label
                        fileConnectionString = dnc + ".fileTextureName"
                        vrayDisplacement_filePath = cmds.getAttr(fileConnectionString)
                    if DNT == "VRayMtl":
                        lc = cmds.listConnections(displacement_map_connection + ".diffuseColor", d = False, s = True)
                        disp_fileConnect = lc[0]
                        key_dfc = object_Old + "_" + RL + "_" + "disp_fileConnect"
                        dispValDic[key_dfc] = disp_fileConnect
                        texSet = cmds.uvLink( query = True, texture = lc[0] )
                        fileName = lc[0]
                        e = len(texSet)
                        if e > 0 :
                            label = cmds.getAttr(texSet)
                            UVdic_texSet[lc[0]] = texSet
                            UVdic_label[lc[0]] = label
                        fileConnectionString = lc[0] + ".fileTextureName"
                        vrayDisplacement_filePath = cmds.getAttr(fileConnectionString)
                    key_fileTextureName = object_Old + "_" + RL + "_" + "displacement_map_connection"
                    z = len(displacement_map_connection)
                    key_fileTextureName = object_Old + "_" + RL + "_" + "vrayDisplacement_filePath"
                    dispValDic[key_fileTextureName] = vrayDisplacement_filePath
                    dispAmount =  object_Old_DispNode + ".vrayDisplacementAmount"
                    dispAmountExists = cmds.attributeQuery("vrayDisplacementAmount",node = object_Old_DispNode,exists = True)
                    if dispAmountExists == 1:
                        dispAmountVal = cmds.getAttr(dispAmount)
                    else:
                        dispAmountVal = 0
                    key_dispAmount = object_Old + "_" + RL + "_" + "dispAmount"
                    dispValDic[key_dispAmount] = dispAmountVal
                    dispShift =  object_Old_DispNode + ".vrayDisplacementShift"
                    dispShiftExists = cmds.attributeQuery("vrayDisplacementShift",node = object_Old_DispNode,exists = True)
                    if dispAmountExists == 1:
                        dispShiftVal = cmds.getAttr(dispShift) or 0
                    else:
                        dispShiftVal = 0
                    key_dispShift = object_Old + "_" + RL + "_" + "dispShift"
                    dispValDic[key_dispShift] = dispShiftVal
                    dispEdgeLength =  object_Old_DispNode + ".vrayEdgeLength"
                    dispEdgeLengthExists = cmds.attributeQuery("vrayEdgeLength",node = object_Old_DispNode,exists = True)
                    if dispEdgeLengthExists == 1:
                        dispEdgeLengthVal = cmds.getAttr(dispEdgeLength) or 0
                    else:
                        dispEdgeLengthVal = 0
                    key_vrayEdgeLength = object_Old + "_" + RL + "_" + "vrayEdgeLength"
                    dispValDic[key_vrayEdgeLength] = dispEdgeLengthVal
                    dispMaxSubdivs =  object_Old_DispNode + ".vrayMaxSubdivs"
                    dispMaxSubdivsExists = cmds.attributeQuery("vrayMaxSubdivs",node = object_Old_DispNode,exists = True)
                    if dispMaxSubdivsExists == 1:
                        dispMaxSubdivsVal = cmds.getAttr(dispMaxSubdivs) or 0
                    else:
                        dispMaxSubdivsVal = 0
                    key_dispMaxSubdivs = object_Old + "_" + RL + "_" + "dispMaxSubdivs"
                    dispValDic[key_dispMaxSubdivs] = dispMaxSubdivsVal
                    overrideGlobalDisplacement = cmds.getAttr( object_Old_DispNode + ".overrideGlobalDisplacement")
                    overrideGlobalDisplacementKey = object_Old + "_" + RL + "_" + "overrideGlobalDisplacement"
                    dispValDic[overrideGlobalDisplacementKey] = overrideGlobalDisplacement
                    displacementBlackBox = cmds.getAttr( object_Old_DispNode + ".blackBox")
                    displacementBlackBoxKey = object_Old + "_" + RL + "_" + "displacementBlackBox"
                    dispValDic[displacementBlackBoxKey] = displacementBlackBox
                    vdkpcExists = cmds.attributeQuery("vrayDisplacementKeepContinuity",node = object_Old_DispNode,exists = True)
                    if vdkpcExists == 1:
                        displacement_keepContinuity = cmds.getAttr(object_Old_DispNode + ".vrayDisplacementKeepContinuity" )
                        displacement_keepContinuityKey = object_Old + "_" + RL + "_" + "displacement_keepContinuity"
                        dispValDic[displacement_keepContinuityKey] = displacement_keepContinuity
                deflayerVals = []
                for valDics in dispValDic:
                    if "defaultRenderLayer" in valDics:
                        deflayerVals.append(valDics)
                        for defLvals in deflayerVals:
                            if "dcon" in defLvals:
                                def_displacement_map_con = dispValDic[defLvals]
                            if "displacement_keepContinuity" in defLvals:
                                def_displacement_keepContinuity = dispValDic[defLvals]
                            if "displacementBlackBox" in defLvals:
                                def_displacementBlackBox = dispValDic[defLvals]
                            if "overrideGlobalDisplacement" in defLvals:
                                def_overrideGlobalDisplacement = dispValDic[defLvals]
                            if "dispAmount" in defLvals:
                                def_vrayDisplacementAmount = dispValDic[defLvals]
                            if "dispShift" in defLvals:
                                def_dispShift = dispValDic[defLvals]
                            if "vrayEdgeLength" in defLvals:
                                def_vrayEdgeLength = dispValDic[defLvals]
                            if "dispMaxSubdivs" in defLvals:
                                def_dispMaxSubdivs = dispValDic[defLvals]
                dispLayerOR = []
                for vals in dispValDic:
                    if "vrayDisplacement_filePath" in vals:
                        tempVal = dispValDic[vals]
                for r in renderLayers:
                    cmds.editRenderLayerGlobals( currentRenderLayer = r )
                    st = object_Old_DispNode + ".displacement"
                    dc = cmds.listConnections(st)
                    for d in dc:
                        t = cmds.nodeType(d)
                        if t == "VRayMtl":
                            conNodeDic[r] = d
                        if t == "file":
                            conNodeDic[r] = d
                        if t == "layeredTexture":
                            conNodeDic[r] = d
                        if t == "ramp":
                            conNodeDic[r] = d
                for c in conNodeDic:
                    if "defaultRenderLayer" in c:
                        defConnectVal = conNodeDic[c]
                for r in renderLayers:
                    if "defaultRenderLayer" not in r:
                        tval = conNodeDic[r]
                        if tval != defConnectVal:
                            print " "
                            print "possible displacement map layer override detected."
                            v = object_Old + "_" + r + "_disp_con"
                            dispLayerOR.append(v)
                            overide_dispValDic[v] = tval
                for vals in dispValDic:
                    if "displacement_keepContinuity" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_displacement_keepContinuity:
                            print "possible displacement keepContinuity layer override detected."
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "overrideGlobalDisplacement" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_overrideGlobalDisplacement:
                            print "possible overrideGlobalDisplacement layer override detected."
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "displacementBlackBox" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_displacementBlackBox:
                            print "possible displacementBlackBox layer override detected."
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "dispAmount" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_vrayDisplacementAmount:
                            print "possible dispAmount layer override detected."
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "dispShift" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_dispShift:
                            print "possible dispShift layer override detected."
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "vrayEdgeLength" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_vrayEdgeLength:
                            print "possible vrayEdgeLength layer override detected."
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "dispMaxSubdivs" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_dispMaxSubdivs:
                            print "possible dispMaxSubdivs layer override detected."
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
            else:
                print "No vray displacement nodes detected for", object_Old
            if object_Old_DispNode != "None":
                if layerTexDetect != 1 and rampDetect != 1:
                    cmds.select(clear = True)
                    shadEx = cmds.objExists("tempShader")
                    if shadEx == 1:
                        cmds.delete("tempShader")
                    tempNodeName = cmds.createNode("surfaceShader")
                    cmds.rename(tempNodeName, "tempShader")
                    cmds.select(clear = True)
                    cmds.select(object_New)
                    cmds.hyperShade(assign = "tempShader")
                    tempFileMod = fileName + ".outColor"
                    cmds.connectAttr(tempFileMod,"tempShader.outColor", force = True)
                    object_Old_children = cmds.listRelatives(object_Old, children = True)
                    object_Old_child = object_Old_children[0]
                    object_New_children = cmds.listRelatives(object_New, children = True)
                    object_New_child = object_New_children[0]
                    firstConList = []
                    secConList = []
                    thirdConList = []
                    fourthConList = []
                    firstCon = cmds.listConnections(fileName, destination = False)
                    for f in firstCon:
                        if f not in firstConList:
                            firstConList.append(f)
                    first = firstConList[0]
                    fType = cmds.nodeType(first)
                    if fType == "uvChooser":
                        firstConList = cmds.listConnections(first, destination = False, plugs = True) or []
                    else:
                        firstConList = cmds.listConnections(first, destination = False) or []
                    siz = len(firstConList)
                    if siz > 0:
                        second = firstConList[0]
                    fType = cmds.nodeType(second)
                    if fType == "uvChooser":
                        secondConList = cmds.listConnections(second, destination = False, plugs = True) or []
                        UVmapAddressOLD = secondConList[0]
                        UVmapAddressNEW = UVmapAddressOLD.replace(object_Old, object_New)
                        print " "
                        print "linking " + fileName + " to " + UVmapAddressNEW
                        print " "
                        cmds.uvLink( uvSet = UVmapAddressNEW, texture = fileName)
                    else:
                        secondConList = cmds.listConnections(second, destination = False) or []
                    shadEx2 = cmds.objExists("tempShader")
                    if shadEx2 == 1:
                        cmds.delete("tempShader")
                if  rampDetect == 1:
                    cmds.select(clear = True)
                    shadEx = cmds.objExists("tempShader")
                    if shadEx == 1:
                        cmds.delete("tempShader")
                    tempNodeName = cmds.createNode("surfaceShader")
                    cmds.rename(tempNodeName, "tempShader")
                    cmds.select(clear = True)
                    cmds.select(object_New)
                    cmds.hyperShade(assign = "tempShader")
                    tempFileMod = rampNode + ".outColor"
                    cmds.connectAttr(tempFileMod,"tempShader.outColor", force = True)
                    object_Old_children = cmds.listRelatives(object_Old, children = True)
                    object_Old_child = object_Old_children[0]
                    object_New_children = cmds.listRelatives(object_New, children = True)
                    object_New_child = object_New_children[0]
                    print " "
                    print "linking " + rampNode + " to " + rampUVset
                    print " "
                    cmds.uvLink( uvSet = rampUVset, texture = rampNode)
                    shadEx2 = cmds.objExists("tempShader")
                    if shadEx2 == 1:
                        cmds.delete("tempShader")
                if layerTexDetect == 1:
                    print "layerTextures UV calculating"
                    for dft in layerTexFiles:
                        cmds.select(clear = True)
                        shadEx = cmds.objExists("tempShader")
                        if shadEx == 1:
                            cmds.delete("tempShader")
                        tempNodeName = cmds.createNode("surfaceShader")
                        cmds.rename(tempNodeName, "tempShader")
                        fileName = dft
                        cmds.select(clear = True)
                        cmds.select(object_New)
                        cmds.hyperShade(assign = "tempShader")
                        tempFileMod = fileName + ".outColor"
                        cmds.connectAttr(tempFileMod,"tempShader.outColor", force = True)
                        object_Old_children = cmds.listRelatives(object_Old, children = True)
                        object_Old_child = object_Old_children[0]
                        object_New_children = cmds.listRelatives(object_New, children = True)
                        object_New_child = object_New_children[0]
                        firstConList = []
                        secConList = []
                        thirdConList = []
                        fourthConList = []
                        firstCon = cmds.listConnections(fileName, destination = False)
                        for f in firstCon:
                            if f not in firstConList:
                                firstConList.append(f)
                        first = firstConList[0]
                        fType = cmds.nodeType(first)
                        if fType == "uvChooser":
                            firstConList = cmds.listConnections(first, destination = False, plugs = True) or []
                        else:
                            firstConList = cmds.listConnections(first, destination = False) or []
                        siz = len(firstConList)
                        if siz > 0:
                            second = firstConList[0]
                        fType = cmds.nodeType(second)
                        if fType == "uvChooser":
                            secondConList = cmds.listConnections(second, destination = False, plugs = True) or []
                            UVmapAddressOLD = secondConList[0]
                            UVmapAddressNEW = UVmapAddressOLD.replace(object_Old, object_New)
                            print " "
                            print "linking " + fileName + " to " + UVmapAddressNEW
                            print " "
                            cmds.uvLink( uvSet = UVmapAddressNEW, texture = fileName)
                        else:
                            secondConList = cmds.listConnections(second, destination = False) or []
            return vrayDisplacement_filePath,def_vrayDisplacementAmount,def_dispShift,def_vrayEdgeLength,def_dispMaxSubdivs,dispValDic,object_Old,object_New,object_Old_DispNode,displacement_map_con,disp_fileConnection,displacementBlackBox,displacement_keepContinuity,overrideGlobalDisplacement,dispLayerOR,overide_dispValDic,renderLayers,conNodeDic,UVdic_texSet,UVdic_label,displacement_map_connection,disp_fileConnect

        def oldObjectCenter(object_Old,object_New,renderLayers):
            chris = "me"
            return(object_Old,object_New,renderLayers)

        checkAll = cmds.checkBox(checkBoxALL,value = True, query = True)
        checkTrans = cmds.checkBox(checkBoxTranslations,value = True, query = True)
        checkMats = cmds.checkBox(checkBoxMaterials,value = True, query = True)
        checkUVsets = cmds.checkBox(checkBoxUVsets,value = True, query = True)
        checkLL = cmds.checkBox(checkBoxLL,value = True, query = True)
        checkObjectProps = cmds.checkBox(checkBoxObjectProps,value = True, query = True)
        checkRenderStats = cmds.checkBox(checkBoxRenderStats,value = True, query = True)
        checkSets = cmds.checkBox(checkBoxExcludeListSets,value = True, query = True)
        if checkAll == 1:
            object_New_Center(object_Old,object_New,renderLayers)
            OBJ_1_newObjectCenter = oldObjectCenter(object_Old,object_New,renderLayers)
            OBJ_1_displacementNodes = displacementNodes(object_Old,object_New,renderLayers)
            OBJ_1_visibility = visibilty(object_Old,object_New,renderLayers)
            OBJ_1_polySmooth = polySmoothOBJ(object_Old,object_New,renderLayers)
            OBJ_1_objectIDnode = objectIDnode(object_Old,object_New,renderLayers)
            OBJ_1_Path = master_path(object_Old,object_New,renderLayers)
        print " "
        print "****"
        print "****"
        print "****"
        print "reading master_Obect info  "
        print "****"
        print "****"
        print "****"
        print " "
        object_New_Center(object_Old,object_New,renderLayers)
        OBJ_1_Path = master_path(object_Old,object_New,renderLayers)
        OBJ_1_renderLayer = renderLayerCheck(object_Old,object_New,renderLayers)
        OBJ_1_translations = translations(object_Old,object_New,renderLayers)
        OBJ_1_ELS = excludeListSets(object_Old,object_New,renderLayers)
        OBJ_1_LL = lightLinking(object_Old,object_New,renderLayers)
        OBJ_1_renderStats = renderStats(object_Old,object_New,renderLayers)
        OBJ_1_vrayObjProps = objectProptertyOverides(object_Old,object_New,renderLayers)
        OBJ_1_objectIDnode = objectIDnode(object_Old,object_New,renderLayers)
        OBJ_1_objectMaterials = materials(object_Old,object_New,renderLayers)
        OBJ_1_UVsets = UVsetLinking(object_Old,object_New,renderLayers)
        OBJ_1_polySmooth = polySmoothOBJ(object_Old,object_New,renderLayers)
        OBJ_1_visibility = visibilty(object_Old,object_New,renderLayers)
        OBJ_1_displacementNodes = displacementNodes(object_Old,object_New,renderLayers)
        OBJ_1_newObjectCenter = oldObjectCenter(object_Old,object_New,renderLayers)
        cmds.select(clear = True)
        if checkAll == 1:
            for L in renderLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = L )
                cmds.hide(OBJ_1_Path[1])
                if "defaultRenderLayer" in L:
                    cmds.editRenderLayerGlobals( currentRenderLayer = L )
        def object_New_Path(OBJ_1_Path):
            print " "
            print "---"
            print "new object object path"
            print "---"
            print " "
            print "path = ",OBJ_1_Path[0]
            s = 0
            newObjPath = cmds.listRelatives(object_New, parent = True) or []
            splitPath = OBJ_1_Path[0].split("|")
            pathOBJ = OBJ_1_Path[3]
            sz = len(splitPath)
            curParent = cmds.listRelatives(OBJ_1_Path[2], parent = True) or []
            sizC = len(curParent)
            if sizC < 1:
                curParent = OBJ_1_Path[1]
            if splitPath[sz-3] != curParent[0]:
                if sz > 3:
                    cmds.parent(OBJ_1_Path[2],splitPath[sz-3])
                    print "parenting " + OBJ_1_Path[2] + " to " + splitPath[sz-3]
                else:
                    print "object at the root level, no hierarchy detected"
                    s = len(newObjPath)
                    if s > 0:
                        cmds.parent(OBJ_1_Path[2],world = True)
            else:
                print OBJ_1_Path[2] + " already parented to the correct node."
            newPathChil = cmds.listRelatives(newObjPath,children = True)
            if s == 0:
                print "no empy parent group to delete"
            else:
                if  newPathChilSize == 0:
                    print "deleting empty parent group ",newObjPath
                    cmds.delete(newObjPath)
        def object_New_renderLayers(OBJ_1_renderLayer):
            print " "
            print "---"
            print "new object render layers"
            print "---"
            print " "
            s = len(OBJ_1_renderLayer[0])
            if s > 1:
                for L in OBJ_1_renderLayer[0]:
                    if L != "defaultRenderLayer":
                        cmds.editRenderLayerMembers( L, OBJ_1_renderLayer[2])
                        print "adding " + OBJ_1_renderLayer[2] + " to " + L
            else:
                print OBJ_1_renderLayer[2] + " is being added to the default render layer only, " + OBJ_1_renderLayer[1] + " not detected in the other layers."
        def object_New_translations(OBJ_1_TX):
            print " "
            print "---"
            print "new object transforms"
            print "---"
            print " "
            transX_attr = OBJ_1_TX[2] + ".translateX"
            transY_attr = OBJ_1_TX[2] + ".translateY"
            transZ_attr = OBJ_1_TX[2] + ".translateZ"
            rotX_attr = OBJ_1_TX[2] + ".rotateX"
            rotY_attr = OBJ_1_TX[2] + ".rotateY"
            rotZ_attr = OBJ_1_TX[2] + ".rotateZ"
            scaleX_attr = OBJ_1_TX[2] + ".scaleX"
            scaleY_attr = OBJ_1_TX[2] + ".scaleY"
            scaleZ_attr = OBJ_1_TX[2] + ".scaleZ"
            defValList = OBJ_1_TX[4]
            layerList = OBJ_1_TX[5]
            transLayerOveride = OBJ_1_TX[6]
            siiz = len(transLayerOveride)
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            cmds.setAttr(transX_attr,defValList[0])
            print " setting the TX default render layer value to " + transX_attr,defValList[0]
            cmds.setAttr(transY_attr,defValList[1])
            print " setting the TY default render layer value to " + transX_attr,defValList[1]
            cmds.setAttr(transZ_attr,defValList[2])
            print " setting the TZ default render layer value to " + transX_attr,defValList[2]
            cmds.setAttr(rotX_attr,defValList[3])
            print " setting the RX default render layer value to " + transX_attr,defValList[3]
            cmds.setAttr(rotY_attr,defValList[4])
            print " setting the RY default render layer value to " + transX_attr,defValList[4]
            cmds.setAttr(rotZ_attr,defValList[5])
            print " setting the RZ default render layer value to " + transX_attr,defValList[5]
            cmds.setAttr(scaleX_attr,defValList[6])
            print " setting the SX default render layer value to " + transX_attr,defValList[6]
            cmds.setAttr(scaleY_attr,defValList[7])
            print " setting the SY default render layer value to " + transX_attr,defValList[7]
            cmds.setAttr(scaleZ_attr,defValList[8])
            print " setting the SZ default render layer value to " + transX_attr,defValList[8]
            transValuesDict = OBJ_1_TX[0]
            for L in layerList:
                for tlo in transLayerOveride:
                    if L in tlo:
                        cmds.select(object_New)
                        cmds.xform( r=True, cp = True )
                        cmds.select(clear = True)
                        if "transX" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "transX"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".translate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".translateX"
                            cmds.setAttr(ERLAnameTX, va)
                            print " setting a TX overide value of " + str(va) + " in layer " + L
                        if "transY" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "transY"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".translate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".translateY"
                            cmds.setAttr(ERLAnameTX, va)
                        if "transZ" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "transZ"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".translate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".translateZ"
                            cmds.setAttr(ERLAnameTX, va)
                        if "rotX" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "rotX"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".rotate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".rotateX"
                            cmds.setAttr(ERLAnameTX, va)
                        if "rotY" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "rotY"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".rotate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".rotateY"
                            cmds.setAttr(ERLAnameTX, va)
                        if "rotZ" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "rotZ"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".rotate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".rotateZ"
                            cmds.setAttr(ERLAnameTX, va)
                        if "scaleX" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "scaleX"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".scale"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".scaleX"
                            cmds.setAttr(ERLAnameTX, va)
                        if "scaleY" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "scaleY"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".scale"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".scaleY"
                            cmds.setAttr(ERLAnameTX, va)
                        if "scaleZ" in tlo:
                            v = OBJ_1_TX[1] + "_" + L + "_" + "scaleZ"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".scale"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".scaleZ"
                            cmds.setAttr(ERLAnameTX, va)
            if siiz < 1:
                print " "
                print " no transform render layer overides detected"
                print " "

        def object_New_excludeListSets(OBJ_1_ELS):
            print " "
            print "---"
            print "new object exclude list"
            print "---"
            print " "
            object_New = OBJ_1_ELS[2]
            VEsets = OBJ_1_ELS[0]
            si = len(VEsets)
            if si > 0:
                for v in VEsets:
                    cmds.sets(object_New,forceElement = v, edit = True)
                    print "adding " + object_New + " to sets: " + v
            else:
                print "no exlude sets detected"

        def object_New_Light_Linking(OBJ_1_LL):
            print "---"
            print "new object light linking"
            print "---"
            LL = OBJ_1_LL[0]
            object_Old = OBJ_1_LL[1]
            object_New = OBJ_1_LL[2]
            lightGroups = []
            lights = []
            childNumDict = {}
            childNumGroup_0 = []
            childNumGroup_1 = []
            childNumGroup_2 = []
            childNumGroup_3 = []
            childNumGroup_4 = []
            childNumGroup_5 = []
            childNumGroup_6 = []
            childNumGroup_7 = []
            childNumGroup_8 = []
            childNumGroup_9 = []
            childNumGroup_10 = []
            print "LL = ",LL
            if LL != "None":
                for l in LL:
                    kind = cmds.nodeType(l)
                    childNum = cmds.listRelatives(l, children = True) or []
                    if childNum != "":
                        childNumber = len(childNum)
                        childNumDict[l] = childNumber
                        if childNumber == 1:
                            childNumGroup_1.append(l)
                            if kind == "transform":
                                if l not in lightGroups:
                                    lightGroups.append(l)
                for l in LL:
                    kind2 = cmds.nodeType(l)
                    if kind2 != "transform":
                        lights.append(l)
            cmds.lightlink(b = True, light = "defaultLightSet", object = object_New)
            if childNumGroup_1 != "None":
                for child in childNumGroup_1:
                    print "linking " + child + " to " + object_New
                    cmds.lightlink(light = child, object = object_New)
            else:
                print "no light linking detected, using defaultLightSet"
                cmds.lightlink(light = "defaultLightSet", object = object_New)

        def object_New_renderStats(OBJ_1_renderStats):
            print " "
            print "---"
            print "new object render stats"
            print "---"
            print " "
            si = len(OBJ_1_renderStats)
            object_Old = OBJ_1_renderStats[1]
            object_New = OBJ_1_renderStats[2]
            defRSlist = OBJ_1_renderStats[3]
            RS_overRideList = OBJ_1_renderStats[4]
            renderStatsDic = OBJ_1_renderStats[5]
            RLOs = OBJ_1_renderStats[6]
            if "Shape" not in object_New:
                chil = cmds.listRelatives(object_New)
                object_New = chil[0]
            old_castsShadows = 0
            old_recieveShadows = 0
            old_motionBlur = 0
            old_primaryVisibility = 0
            old_smoothShading = 0
            old_visibleInReflections = 0
            old_visibleInRefractions = 0
            old_doubleSided = 0
            for DL in defRSlist:
                if "castsShadows" in DL:
                    old_castsShadows = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for castsShadows to",old_castsShadows
                    cmds.setAttr((object_New + ".castsShadows"),old_castsShadows)
                if "recieveShadows" in DL:
                    old_recieveShadows = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for recieveShadows to",old_recieveShadows
                    cmds.setAttr((object_New + ".receiveShadows"),old_recieveShadows )
                if "motionBlur" in DL:
                    old_motionBlur = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for motionBlur to",old_motionBlur
                    cmds.setAttr((object_New + ".motionBlur"),old_motionBlur)
                if "primaryVisibility" in DL:
                    old_primaryVisibility = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for primaryVisibility to",old_primaryVisibility
                    cmds.setAttr((object_New + ".primaryVisibility"),old_primaryVisibility)
                if "smoothShading" in DL:
                    old_smoothShading = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for smoothShading to",old_smoothShading
                    cmds.setAttr((object_New + ".smoothShading"),old_smoothShading)
                if "visibleInReflections" in DL:
                    old_visibleInReflections = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for visibleInReflections to",old_visibleInReflections
                    cmds.setAttr((object_New + ".visibleInReflections"),old_visibleInReflections)
                if "visibleInRefractions" in DL:
                    old_visibleInRefractions = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for visibleInRefractions to",old_visibleInRefractions
                    cmds.setAttr((object_New + ".visibleInRefractions"),old_visibleInRefractions )
                if "doubleSided" in DL:
                    old_doubleSided = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    print "setting default value for doubleSided to",old_doubleSided
                    cmds.setAttr((object_New + ".doubleSided"),old_doubleSided)
            print " "
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_1 = RL + "_" + "castsShadows"
                    if chunk_1 in R:
                        print "** castShadows render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "castsShadows"
                        old_castsShadows_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for castsShadows in ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".castsShadows"))
                        cmds.setAttr((object_New + ".castsShadows"),old_castsShadows_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_2 = RL + "_" + "receiveShadows"
                    if chunk_2 in R:
                        print "** receiveShadows render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "receiveShadows"
                        old_receiveShadows_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for receiveShadows in ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".receiveShadows"))
                        cmds.setAttr((object_New + ".receiveShadows"),old_receiveShadows_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_3 = RL + "_" + "motionBlur"
                    if chunk_3 in R:
                        print "** motionBlur render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "motionBlur"
                        old_motionBlur_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for motionBlur in ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".motionBlur"))
                        cmds.setAttr((object_New + ".motionBlur"),old_motionBlur_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_5 = RL + "_" + "smoothShading"
                    if chunk_5 in R:
                        print "** smoothShading render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "smoothShading"
                        old_smoothShading_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for smoothShading in ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".smoothShading"))
                        cmds.setAttr((object_New + ".smoothShading"),old_smoothShading_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_6 = RL + "_" + "visibleInReflections"
                    if chunk_6 in R:
                        print "** visibleInReflections render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "visibleInReflections"
                        old_visibleInReflections_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for visibleInReflections in ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".visibleInReflections"))
                        cmds.setAttr((object_New + ".visibleInReflections"),old_visibleInReflections_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_4 = RL + "_" + "primaryVisibility"
                    if chunk_4 in R:
                        print "** primaryVisibility render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "primaryVisibility"
                        old_primaryVisibility_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for primaryVisibility in ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".primaryVisibility"))
                        cmds.setAttr((object_New + ".primaryVisibility"),old_primaryVisibility_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_5 = RL + "_" + "visibleInRefractions"
                    if chunk_5 in R:
                        print "** visibleInRefractions render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "visibleInRefractions"
                        old_visibleInRefractions_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for visibleInRefractions in ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".visibleInRefractions"))
                        cmds.setAttr((object_New + ".visibleInRefractions"),old_visibleInRefractions_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_6 = RL + "_" + "doubleSided"
                    if chunk_6 in R:
                        print "** doubleSided render layer overide detected **"
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "doubleSided"
                        old_doubleSided_lovr = renderStatsDic[ovrKey]
                        print "setting a render layer overide for doubleSided in layer, ", RL
                        cmds.editRenderLayerAdjustment((object_New + ".doubleSided"))
                        cmds.setAttr((object_New + ".doubleSided"),old_doubleSided_lovr)

        def object_New_VRAY_objectPropOverides(OBJ_1_vrayObjProps):
            object_Old = OBJ_1_vrayObjProps[1]
            object_New = OBJ_1_vrayObjProps[2]
            VoBpropertyDic = OBJ_1_vrayObjProps[3]
            VP_overRideList = OBJ_1_vrayObjProps[0]
            defVPlist = OBJ_1_vrayObjProps[4]
            defaultValDic = OBJ_1_vrayObjProps[5]
            RLOs = OBJ_1_vrayObjProps[6]
            OPlist = OBJ_1_vrayObjProps[7]
            objectIDo = OBJ_1_vrayObjProps[8]
            vpOPid = OBJ_1_vrayObjProps[9]
            print " "
            print "---"
            print "new object VRAY object properties"
            print "---"
            print " "
            cmds.select(object_New)
            VPnode = cmds.vray("objectProperties", "add_single")
            cmds.select(clear = True)
            defVPlistSize = len(defVPlist)
            if defVPlistSize < 1:
                print "no Vray object properties associated with " + object_New + " detected"
            print " "
            for OP in defVPlist:
                cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
                print "setting overide object ID to ",objectIDo
                objectIDpath = VPnode[0] + ".objectIDEnabled"
                cmds.setAttr(objectIDpath,objectIDo)
                if objectIDo == 1:
                    print "setting Object ID to ",vpOPid
                    objectIDpath = VPnode[0] + ".objectID"
                    cmds.setAttr(objectIDpath,vpOPid)
                if "giVisibility" in OP:
                    print "setting default giVisibility"
                    val = defaultValDic["giVisibility"]
                    SApath = VPnode[0] + ".giVisibility"
                    print val
                    cmds.setAttr(SApath,val)
                if "primaryVisibility" in OP:
                    print "setting default primaryVisibility"
                    val = defaultValDic["primaryVisibility"]
                    SApath = VPnode[0] + ".primaryVisibility"
                    print val
                    cmds.setAttr(SApath,val)
                if "reflectionVisibility" in OP:
                    print "setting default reflectionVisibility"
                    val = defaultValDic["reflectionVisibility"]
                    SApath = VPnode[0] + ".reflectionVisibility"
                    print val
                    cmds.setAttr(SApath,val)
                if "refractionVisibility" in OP:
                    print "setting default refractionVisibility"
                    val = defaultValDic["refractionVisibility"]
                    SApath = VPnode[0] + ".refractionVisibility"
                    print val
                    cmds.setAttr(SApath,val)
                if "shadowVisibility" in OP:
                    print "setting default shadowVisibility"
                    val = defaultValDic["shadowVisibility"]
                    SApath = VPnode[0] + ".shadowVisibility"
                    print val
                    cmds.setAttr(SApath,val)
                if "receiveShadows" in OP:
                    print "setting default receiveShadows"
                    val = defaultValDic["receiveShadows"]
                    SApath = VPnode[0] + ".receiveShadows"
                    print val
                    cmds.setAttr(SApath,val)
                if "generateGIMultiplier" in OP:
                    print "setting default generateGIMultiplier"
                    val = defaultValDic["generateGIMultiplier"]
                    SApath = VPnode[0] + ".generateGIMultiplier"
                    print val
                    cmds.setAttr(SApath,val)
                if "receiveGIMultiplier" in OP:
                    print "setting default receiveGIMultiplier"
                    val = defaultValDic["receiveGIMultiplier"]
                    SApath = VPnode[0] + ".receiveGIMultiplier"
                    print val
                    cmds.setAttr(SApath,val)
                    for RL in RLOs:
                        if "defaultRenderLayer" not in RL:
                            for VPL in VP_overRideList:
                                if RL in VPL:
                                    if "giVisibility" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "giVisibility"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for giVisibility in", RL
                                        setApath = VPnode[0] + ".giVisibility"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)
                                    if "primaryVisibility" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "primaryVisibility"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for primaryVisibility in", RL
                                        setApath = VPnode[0] + ".primaryVisibility"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)
                                    if "reflectionVisibility" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "reflectionVisibility"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for reflectionVisibility in", RL
                                        setApath = VPnode[0] + ".reflectionVisibility"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)
                                    if "refractionVisibility" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "refractionVisibility"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for refractionVisibility in", RL
                                        setApath = VPnode[0] + ".refractionVisibility"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)
                                        testAttr = cmds.getAttr(setApath)
                                    if "shadowVisibility" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "shadowVisibility"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for shadowVisibility in", RL
                                        setApath = VPnode[0] + ".shadowVisibility"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)
                                    if "receiveShadows" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "receiveShadows"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for receiveShadows in", RL
                                        setApath = VPnode[0] + ".receiveShadows"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)
                                    if "generateGIMultiplier" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "generateGIMultiplier"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for generateGIMultiplier in", RL
                                        setApath = VPnode[0] + ".generateGIMultiplier"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)
                                    if "receiveGIMultiplier" in VPL:
                                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                                        setApathKEY = OPlist[0] + "_" + RL + "_" + "receiveGIMultiplier"
                                        valO = VoBpropertyDic[setApathKEY]
                                        print "setting overide for receiveGIMultiplier in", RL
                                        setApath = VPnode[0] + ".receiveGIMultiplier"
                                        cmds.editRenderLayerAdjustment(setApath)
                                        cmds.setAttr(setApath,valO)

        def object_New_objectID(OBJ_1_objectIDnode):
            print " "
            print "---"
            print "new object VRAY object ID"
            print "---"
            print " "
            objectID = OBJ_1_objectIDnode[0]
            objectID_dic = OBJ_1_objectIDnode[3]
            RLOs = OBJ_1_objectIDnode[4]
            object_Old = OBJ_1_objectIDnode[1]
            object_New = OBJ_1_objectIDnode[2]
            objParent = cmds.listRelatives(object_New, parent = True) or []
            objChild = cmds.listRelatives(object_New, children = True) or []
            VoBpropertyDic = {}
            if "Shape" in object_New:
                objParent = objParent
                objChild = object_Old
                obj = objParent
            else:
                objParent = object_Old
            string = "vray addAttributesFromGroup " + objChild[0] + " vray_objectID 1"
            melCmd = string
            if objectID != "None":
                mel.eval(melCmd)
                cmds.setAttr((objChild[0] + ".vrayObjectID"),objectID)
                print "Default render layer VRAY object ID attribute created and set to:",objectID
                for RL in RLOs:
                    if "DefaultRenderLayer" not in RL:
                        if RL in objectID_dic:
                            val = objectID_dic[RL]
                            cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                            cmds.editRenderLayerAdjustment((objChild[0] + ".vrayObjectID"))
                            cmds.setAttr((objChild[0] + ".vrayObjectID"),val)
                            print "Setting an object ID attribute render layer overide of " + str(val) + " for layer, " + RL
            else:
                print "no VRAY object ID attribute detected"

        def object_New_materials(OBJ_1_objectMaterials):
            print " "
            print "---"
            print "new object materials"
            print "---"
            print " "
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            mats_dict = OBJ_1_objectMaterials[0]
            LayerMats_dic = OBJ_1_objectMaterials[1]
            layerOverM = OBJ_1_objectMaterials[2]
            object_Old = OBJ_1_objectMaterials[3]
            object_New = OBJ_1_objectMaterials[4]
            RLM = OBJ_1_objectMaterials[5]
            matAssignsExist = OBJ_1_objectMaterials[6]
            defMatList = []
            valOLD = []
            valNEW = []
            if matAssignsExist != 0:
                for defMats in mats_dict:
                    if "defaultRenderLayer" in defMats:
                        defMatList.append(defMats)
                for dMat in defMatList:
                    valOLD.append(mats_dict[dMat])
                valOLD = valOLD[0]
                for VO in valOLD:
                    oldVO = object_Old
                    newVO = oldVO.replace(object_Old, object_New)
                    if newVO not in valNEW:
                        valNEW.append(newVO)
                for va in valNEW:
                    tmp = va.replace(object_New, object_Old)
                    cmds.select(tmp)
                    cmds.hyperShade(smn = True)
                    tmpMat = cmds.ls(sl = True)
                    tmpMat_clean = []
                    for tm in tmpMat:
                        tmnt = cmds.nodeType(tm)
                        if tmnt != "renderLayer":
                            tmpMat_clean.append(tm)
                    for t in tmpMat_clean:
                        if "Layer" not in t:
                            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
                            cmds.select(clear = True)
                            cmds.select(va)
                            cmds.hyperShade(assign=t)
                            print " "
                            print "assigning " + t + " to " + va
                            print " "
                            cmds.select(clear = True)
                for L in LayerMats_dic:
                    if "defaultRenderLayer" not in L:
                        lay = L.split("*")
                        oKey = LayerMats_dic[L]
                        compVal = LayerMats_dic[L]
                        listCompare = defMatList[0]
                        if compVal not in listCompare:
                            print " "
                            print "setting a material overide in layer:",L
                            print " "
                            cmds.editRenderLayerGlobals( currentRenderLayer = L)
                            mat = LayerMats_dic[L]
                            cmds.select(object_New)
                            cmds.hyperShade(assign = mat)
                            cmds.select(clear = True)
            if matAssignsExist == 0:
                print "WARNING: no materials assigned to ",object_New

        def object_New_UVsetLinking(OBJ_1_UVsets):
            print " "
            print "---"
            print "new object UVsets"
            print "---"
            print " "
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            object_Old = OBJ_1_UVsets[5]
            object_New = OBJ_1_UVsets[6]
            uvNameDic = OBJ_1_UVsets[0]
            texADDdic = OBJ_1_UVsets[1]
            uvAddDic = OBJ_1_UVsets[2]
            uvAddress = OBJ_1_UVsets[3]
            obj_UVsets = OBJ_1_UVsets[4]
            renderLayers = OBJ_1_UVsets[7]
            UV_sets_object_New = []
            uvAddress_NEW = []
            uvNameDic_NEW = {}
            uvAddDic_NEW = {}
            texADDdic_NEW = {}
            textures = cmds.ls(type = "file")
            for tex in textures:
                setAddress = cmds.uvLink(query = True, texture = tex) or []
                for set in setAddress:
                    if object_Old in set:
                        setAddressNEW = set
                        setName = cmds.getAttr(setAddressNEW)
                        uvAddress_NEW.append(setAddressNEW)
                        uvAddDic_NEW[str(setAddressNEW)] = tex
                        uvNameDic_NEW[setName] = setAddressNEW
                        texADDdic_NEW[tex] = setAddressNEW
            UV_sets_NAME_object_New = cmds.polyUVSet( object_New, query = True, allUVSets = True )
            print "UV sets found for " + object_New + " : ",UV_sets_NAME_object_New
            print " "
            setList = []
            NO_setIND_dic = {}
            NO_indices = cmds.polyUVSet(object_New, query = True, allUVSetsIndices = True )
            a = 0
            for uv in UV_sets_NAME_object_New:
                NO_setIND_dic[uv] = NO_indices[a]
                a = (a + 1)
            for texDicNEW in texADDdic_NEW:
                for texDicOLD in texADDdic:
                    if texDicNEW == texDicOLD:
                        OLDuvlink = texADDdic[texDicOLD]
                        name_OLDuvlink = cmds.getAttr(OLDuvlink)
                        for name in UV_sets_NAME_object_New:
                            if name == name_OLDuvlink:
                                for NO in NO_setIND_dic:
                                    if name == NO:
                                        ind = NO_setIND_dic[name]
                                        set_string = object_New + ".uvSet[" + str(ind) + "]" + ".uvSetName"
                                        n = cmds.getAttr(set_string)
                                        print "setting a UVset link for texture map " + texDicNEW + " to the UV set " + n
                                        g = cmds.getAttr(set_string)
                                        cmds.uvLink(uvSet = set_string, texture = texDicNEW)

        def object_New_polySmoothOBJ(OBJ_1_polySmooth):
            print " "
            print "---"
            print "New object polySmooth attribute"
            print "---"
            print " "
            object_Old = OBJ_1_polySmooth[0]
            object_New = OBJ_1_polySmooth[1]
            object_Old_smooth_node_found = OBJ_1_polySmooth[2]
            object_New_smooth_node_found = OBJ_1_polySmooth[3]
            object_Old_smooth_division_level = OBJ_1_polySmooth[4]
            object_New_smooth_division_level = OBJ_1_polySmooth[5]
            if object_Old_smooth_node_found == 1:
                if object_New_smooth_node_found == 0:
                    cmds.polySmooth(object_New ,mth = 0, sdt = 2, ovb = 1, ofb = 1, ofc = 1, ost = 0, ocr = 0, dv = object_Old_smooth_division_level, bnr = 1, c = 1, kb = 1, ksb = 1, khe = 0, kt = 1, kmb = 1, suv = 1, peh = 0, sl = 1, dpe = 1, ps = .1, ro = 1, ch = 1)
                    print "applyig a smoothing node to " + object_New + " at division level ", object_Old_smooth_division_level
                else:
                    print "smoothing node detected for " + object_New + ", NO additional smoothing applied"
            else:
                print "no smoothing detected for " + object_Old + ", applying no smoothing to, " + object_New


        def object_New_visibility(OBJ_1_visibility):
            print " "
            print "---"
            print "New object visibility"
            print "---"
            print " "
            visDic = OBJ_1_visibility[0]
            object_Old = OBJ_1_visibility[1]
            object_New = OBJ_1_visibility[2]
            RLs = cmds.ls(type = "renderLayer")
            visPathNew = object_New + ".visibility"
            defVisVal = visDic["defaultRenderLayer"]
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            print "setting the default renderLayer visibility to " + str(defVisVal)
            cmds.setAttr(visPathNew,defVisVal)
            for r in RLs:
                cmds.editRenderLayerGlobals( currentRenderLayer = r)
                if r != "defaultRenderLayer":
                    if r in visDic:
                        visVal = visDic[r]
                        if visVal != defVisVal:
                            cmds.editRenderLayerAdjustment((object_New + ".visibility"))
                            print "setting the visibility for " + object_New + "to" + str(visVal) + " in layer " + r
                            cmds.setAttr(visPathNew,visVal)

        def object_New_displacementNode(OBJ_1_displacementNodes):
            print " "
            print "---"
            print "New object displacement node"
            print "---"
            print " "
            object_Old_DispNode = OBJ_1_displacementNodes[8]
            if object_Old_DispNode != "None":
                vrayDisplacement_filePath = OBJ_1_displacementNodes[0]
                def_vrayDisplacementAmount = OBJ_1_displacementNodes[1]
                def_dispShift = OBJ_1_displacementNodes[2]
                def_vrayEdgeLength = OBJ_1_displacementNodes[3]
                def_dispMaxSubdivs = OBJ_1_displacementNodes[4]
                dispValDic = OBJ_1_displacementNodes[5]
                object_Old = OBJ_1_displacementNodes[6]
                object_New = OBJ_1_displacementNodes[7]
                disp_fileConnection = OBJ_1_displacementNodes[10]
                displacementBlackBox = OBJ_1_displacementNodes[11]
                displacement_keepContinuity = OBJ_1_displacementNodes[12]
                overrideGlobalDisplacement = OBJ_1_displacementNodes[13]
                dispLayerOR = OBJ_1_displacementNodes[14]
                overide_dispValDic = OBJ_1_displacementNodes[15]
                renderLayers = OBJ_1_displacementNodes[16]
                conNodeDic = OBJ_1_displacementNodes[17]
                UVdic_texSet = OBJ_1_displacementNodes[18]
                UVdic_label = OBJ_1_displacementNodes[19]
                displacement_map_connection = OBJ_1_displacementNodes[20]
                print "displacement_map_connection = ",displacement_map_connection
                disp_fileConnect = OBJ_1_displacementNodes[21]
                print "disp_fileConnect = ",disp_fileConnect
                displacement_map_con = conNodeDic["defaultRenderLayer"]
                cmds.select(object_New)
                newDispNode = cmds.vray("objectProperties", "add_single","VRayDisplacement")
                cmds.select(clear = True)
                cmds.vray("addAttributesFromGroup", newDispNode[0], "vray_displacement", 1)
                cmds.vray("addAttributesFromGroup", newDispNode[0], "vray_subquality", 1)
                ze = len(displacement_map_con)
                print "default render layer displacement settings:"
                print " "
                if ze > 0:
                    print "setting displacement node connection to:",displacement_map_con
                    texString = (displacement_map_con + ".outColor" + " " + newDispNode[0] + ".displacement" )
                    texString2 = "connectAttr -force " + texString
                    mel.eval(texString2)
                print "setting overrideGlobalDisplacement to " + str(overrideGlobalDisplacement)
                cmds.setAttr((newDispNode[0] + ".overrideGlobalDisplacement"),overrideGlobalDisplacement)
                print "setting displacementBlackBox to " + str(displacementBlackBox)
                cmds.setAttr((newDispNode[0] + ".blackBox"),displacementBlackBox)
                print "setting vrayDisplacementKeepContinuity to " + str(displacement_keepContinuity)
                cmds.setAttr((newDispNode[0] + ".vrayDisplacementKeepContinuity"),displacement_keepContinuity)
                print "setting vrayDisplacementAmount to " + str(def_vrayDisplacementAmount)
                cmds.setAttr((newDispNode[0] + ".vrayDisplacementAmount"),def_vrayDisplacementAmount)
                print "setting vrayDisplacementShift to " + str(def_dispShift)
                cmds.setAttr((newDispNode[0] + ".vrayDisplacementShift"),def_dispShift)
                print "setting vrayEdgeLength to " + str(def_vrayEdgeLength)
                cmds.setAttr((newDispNode[0] + ".vrayEdgeLength"),def_vrayEdgeLength)
                print "setting vrayMaxSubdivs to " + str(def_dispMaxSubdivs)
                cmds.setAttr((newDispNode[0] + ".vrayMaxSubdivs"),def_dispMaxSubdivs)
                for L in renderLayers:
                    if "defaultRenderLayer" not in L:
                        if L in str(overide_dispValDic) and "dispAmount" in str(overide_dispValDic):
                            for over in overide_dispValDic:
                                if L in over and "disp_con" in over:
                                    print " "
                                    print "layer overides*"
                                    print " "
                                    print "setting a layer overide in " + L + " of displacement file connection to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".displacement"))
                                    displacement_map_conO = conNodeDic[L]
                                    texString = (displacement_map_conO + ".outColor" + " " + newDispNode[0] + ".displacement" )
                                    texString2 = "connectAttr -force " + texString
                                    mel.eval(texString2)
                            for over in overide_dispValDic:
                                if L in over and "dispAmount" in over:
                                    print "setting a layer overide in " + L + " of vrayDisplacementAmount to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayDisplacementAmount"))
                                    cmds.setAttr((newDispNode[0] + ".vrayDisplacementAmount"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "dispMaxSubdivs" in over:
                                    print "setting a layer overide in " + L + " of vrayMaxSubdivs to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayMaxSubdivs"))
                                    cmds.setAttr((newDispNode[0] + ".vrayMaxSubdivs"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "dispShift" in over:
                                    print "setting a layer overide in " + L + " of vrayDisplacementShift to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayDisplacementShift"))
                                    cmds.setAttr((newDispNode[0] + ".vrayDisplacementShift"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "vrayEdgeLength" in over:
                                    print "setting a layer overide in " + L + " of vrayEdgeLength to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayEdgeLength"))
                                    cmds.setAttr((newDispNode[0] + ".vrayEdgeLength"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "overrideGlobalDisplacement" in over:
                                    print "setting a layer overide in " + L + " of overrideGlobalDisplacement to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".overrideGlobalDisplacement"))
                                    cmds.setAttr((newDispNode[0] + ".overrideGlobalDisplacement"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "displacement_keepContinuity" in over:
                                    print "setting a layer overide in " + L + " of vrayDisplacementKeepContinuity to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayDisplacementKeepContinuity"))
                                    cmds.setAttr((newDispNode[0] + ".vrayDisplacementKeepContinuity"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "displacementBlackBox" in over:
                                    print "setting a layer overide in " + L + " of blackBox to " + str(overide_dispValDic[over])
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".blackBox"))
                                    cmds.setAttr((newDispNode[0] + ".blackBox"),overide_dispValDic[over])
            else:
                print "no displacement detected"
            print "changing render layer too",currentRenderLayer
            cmds.editRenderLayerGlobals( currentRenderLayer = currentRenderLayer )
        print " "
        print "************"
        print "************"
        print "adjusting new object  "
        print "************"
        print "************"
        print " "
        OBJ_1_renderLayer = renderLayerCheck(object_Old,object_New,renderLayers)
        if checkAll == 1:
            object_New_Path(OBJ_1_Path)
            object_New_renderLayers(OBJ_1_renderLayer)
            object_New_objectID(OBJ_1_objectIDnode)
            object_New_polySmoothOBJ(OBJ_1_polySmooth)
            object_New_visibility(OBJ_1_visibility)
            object_New_displacementNode(OBJ_1_displacementNodes)
        if checkTrans == 1:
            object_New_translations(OBJ_1_translations)
        if checkMats == 1:
            object_New_materials(OBJ_1_objectMaterials)
        if checkUVsets == 1:
            object_New_UVsetLinking(OBJ_1_UVsets)
        if checkLL == 1:
            object_New_Light_Linking(OBJ_1_LL)
        if checkObjectProps == 1:
            object_New_VRAY_objectPropOverides(OBJ_1_vrayObjProps)
        if checkRenderStats == 1:
            object_New_renderStats(OBJ_1_renderStats)
        if checkSets == 1:
            object_New_excludeListSets(OBJ_1_ELS)
        print " "
        print " "
        print "****"
        print " finished matching object_New to object_Old "
        print "****"
        print " "
        print " "
        print " "
        print " "

objectChooseWin()
