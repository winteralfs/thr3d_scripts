import maya.cmds as cmds
from functools import partial


class transferAttrsClass():
    def __init__(self,nodeOne,nodeTwo):
        
        self.nodeOne = nodeOne
        self.nodeTwo = nodeTwo
        
        #print "self.nodeOne = ",self.nodeOne        
        #print "self.nodeTwo = ",self.nodeTwo
        self.Node1Type = cmds.nodeType(self.nodeOne) or []        
    
    def xferAttrs(self):        
        if self.Node1Type == "transform":  
            if "Shape" in self.nodeOne:
                xformNode1 = cmds.listRelatives(self.nodeOne, parent = True)
                shapeNode1 = self.nodeOne
                xformNode1 = xformNode1[0]
            if "Shape" not in self.nodeOne:
                xformNode1 = cmds.listRelatives(self.nodeOne, children = True)
                shapeNode1 = xformNode1[0]
                xformNode1 = self.nodeOne                        
            if "Shape" in self.nodeTwo:
                xformNode2 = cmds.listRelatives(self.nodeTwo, parent = True)
                shapeNode2 = self.nodeTwo
                xformNode2 = xformNode2[0]    
            if "Shape" not in self.nodeTwo:
                xformNode2 = cmds.listRelatives(self.nodeTwo, children = True)
                shapeNode2 = xformNode2[0]
                xformNode2 = self.nodeTwo          

            self.XformNodeType = cmds.nodeType(xformNode1) or []
            self.shapeNodeType = cmds.nodeType(shapeNode1) or []

            if self.XformNodeType == "transform" and self.shapeNodeType == "mesh":
                attrsRem_xform = ["message","hyperLayout","borderConnections","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType"
                ,"boundingBox","instObjGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor",
                "drawOverride","renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostDriver","rotatePivot","scalePivot","rotateAxis",
                "selectHandle","rotateQuaternion"]          
                attrsRem_shape = ["message","hyperLayout","borderConnections","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode","publishedNodeInfo.publishedNodeType",
                "boundingBox","instObjGroups","instObjGroups.objectGroups.objectGrpCompList","instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","drawOverride",
                "renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostDriver","referenceObject","compInstObjGroups",
                "compInstObjGroups.compObjectGroups.compObjectGrpCompList","compInstObjGroups.compObjectGroups.compObjectGroupId","controlPoints.xValue","controlPoints.yValue",
                "controlPoints.zValue","blindDataNodes","uvSet","uvSet.uvSetName","uvSet.uvSetPoints","uvSet.uvSetPoints.uvSetPointsU","uvSet.uvSetPoints.uvSetPointsV",
                "uvSet.uvSetTweakLocation","colorSet.colorName","colorSet.clamped","colorSet.representation","colorSet.colorSetPoints","colorSet.colorSetPoints.colorSetPointsR",
                "colorSet.colorSetPoints.colorSetPointsG","colorSet.colorSetPoints.colorSetPointsB","colorSet.colorSetPoints.colorSetPointsA","collisionOffsetVelocityIncrement.collisionOffsetVelocityIncrement_Position",
                "collisionOffsetVelocityIncrement.collisionOffsetVelocityIncrement_FloatValue","collisionOffsetVelocityIncrement.collisionOffsetVelocityIncrement_Interp","collisionDepthVelocityIncrement.collisionDepthVelocityIncrement_Position",
                "collisionDepthVelocityIncrement.collisionDepthVelocityIncrement_FloatValue","collisionDepthVelocityIncrement.collisionDepthVelocityIncrement_Interp","collisionOffsetVelocityMultiplier",
                "collisionOffsetVelocityMultiplier.collisionOffsetVelocityMultiplier_Position","collisionOffsetVelocityMultiplier.collisionOffsetVelocityMultiplier_FloatValue",
                "collisionOffsetVelocityMultiplier.collisionOffsetVelocityMultiplier_Interp","collisionDepthVelocityMultiplier","collisionDepthVelocityMultiplier.collisionDepthVelocityMultiplier_Position",
                "collisionDepthVelocityMultiplier.collisionDepthVelocityMultiplier_FloatValue","collisionDepthVelocityMultiplier.collisionDepthVelocityMultiplier_Interp","outGeometryClean",
                "pnts.pntx","pnts.pnty","pnts.pntz","vrts","vrts.vrtx","vrts.vrty","vrts.vrtz","edge","edge.edg1","edge.edg2","edge.edgh","uvpt.uvpx","uvpt.uvpy","colors.colorR",
                "colors.colorG","colors.colorB","colors.colorA","normals.normalx","normals.normaly","normals.normalz","face","colorPerVertex","vertexColor.vertexColorRGB","vertexColor.vertexColorR",
                "vertexColor.vertexColorG","vertexColor.vertexColorB","vertexColor.vertexAlpha","vertexColor.vertexFaceColor","vertexColor.vertexFaceColor.vertexFaceColorRGB",
                "vertexColor.vertexFaceColor.vertexFaceColorR","vertexColor.vertexFaceColor.vertexFaceColorG","vertexColor.vertexFaceColor.vertexFaceColorB","vertexColor.vertexFaceColor.vertexFaceAlpha",
                "normalPerVertex","vertexNormal.vertexNormalXYZ","vertexNormal.vertexNormalX","vertexNormal.vertexNormalY","vertexNormal.vertexNormalZ","vertexNormal.vertexFaceNormal","vertexNormal.vertexFaceNormal.vertexFaceNormalXYZ",
                "vertexNormal.vertexFaceNormal.vertexFaceNormalX","vertexNormal.vertexFaceNormal.vertexFaceNormalY","vertexNormal.vertexFaceNormal.vertexFaceNormalZ"]           

            if self.XformNodeType == "transform" and self.shapeNodeType == "VRayLightRectShape":
                attrsRem_xform = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox",
                "borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode",
                "publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment",
                "customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ",
                "boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ",
                "center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix",
                "parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList",
                "instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","useObjectColor",
                "objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled",
                "overrideVisibility","overrideColor","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo",
                "renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps",
                "ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG",
                "ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","translate","rotate","scale","shear","rotatePivot",
                "rotatePivotTranslate","scalePivot","scalePivotTranslate","rotateAxis","transMinusRotatePivot","minTransLimit","maxTransLimit","minTransLimitEnable",
                "maxTransLimitEnable","minRotLimit","maxRotLimit","minRotLimitEnable","maxRotLimitEnable","minScaleLimit","maxScaleLimit","minScaleLimitEnable",
                "maxScaleLimitEnable","selectHandle","rotateQuaternion","mentalRayControls"]
                #"mentalRayControls"]
            
                attrsRem_shape = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox",
                "borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode",
                "publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment",
                "customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ",
                "boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ",
                "center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix",
                "parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList",
                "instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","useObjectColor",
                "objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled",
                "overrideVisibility","overrideColor","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo",
                "renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps",
                "ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG",
                "ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","referenceObject","compInstObjGroups.compObjectGroups.compObjectGrpCompList",
                "compInstObjGroups.compObjectGroups.compObjectGroupId","localPosition","worldPosition","localScale","targetPos","lightData","lightDirection","lightIntensity","compInstObjGroups"]
                #,"mentalRayControls","miRenderPassList"]
                
            if self.XformNodeType == "transform" and self.shapeNodeType == "camera":
                attrsRem_xform = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox",
                "borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode",
                "publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment",
                "customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ",
                "boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ",
                "center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix",
                "parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList",
                "instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","useObjectColor",
                "objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled",
                "overrideVisibility","overrideColor","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo",
                "renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps",
                "ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG",
                "ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","translate","rotate","scale","shear","rotatePivot",
                "rotatePivotTranslate","scalePivot","scalePivotTranslate","rotateAxis","transMinusRotatePivot","minTransLimit","maxTransLimit","minTransLimitEnable",
                "maxTransLimitEnable","minRotLimit","maxRotLimit","minRotLimitEnable","maxRotLimitEnable","minScaleLimit","maxScaleLimit","minScaleLimitEnable",
                "maxScaleLimitEnable","selectHandle","rotateQuaternion","mentalRayControls"]
                #"mentalRayControls"]
            
                attrsRem_shape = ["message","caching","isHistoricallyInteresting","nodeState","binMembership","hyperLayout","isCollapsed","blackBox",
                "borderConnections","isHierarchicalConnection","publishedNodeInfo","publishedNodeInfo.publishedNode","publishedNodeInfo.isHierarchicalNode",
                "publishedNodeInfo.publishedNodeType","rmbCommand","templateName","templatePath","viewName","iconName","viewMode","templateVersion","uiTreatment",
                "customTreatment","creator","creationDate","containerType","boundingBox","boundingBoxMin","boundingBoxMinX","boundingBoxMinY","boundingBoxMinZ",
                "boundingBoxMax","boundingBoxMaxX","boundingBoxMaxY","boundingBoxMaxZ","boundingBoxSize","boundingBoxSizeX","boundingBoxSizeY","boundingBoxSizeZ",
                "center","boundingBoxCenterX","boundingBoxCenterY","boundingBoxCenterZ","matrix","inverseMatrix","worldMatrix","worldInverseMatrix","parentMatrix",
                "parentInverseMatrix","visibility","intermediateObject","template","ghosting","instObjGroups","instObjGroups.objectGroups","instObjGroups.objectGroups.objectGrpCompList",
                "instObjGroups.objectGroups.objectGroupId","instObjGroups.objectGroups.objectGrpColor","objectColorRGB","objectColorR","objectColorG","objectColorB","useObjectColor",
                "objectColor","drawOverride","overrideDisplayType","overrideLevelOfDetail","overrideShading","overrideTexturing","overridePlayback","overrideEnabled",
                "overrideVisibility","overrideColor","lodVisibility","selectionChildHighlighting","renderInfo","identification","layerRenderable","layerOverrideColor","renderLayerInfo",
                "renderLayerInfo.renderLayerId","renderLayerInfo.renderLayerRenderable","renderLayerInfo.renderLayerColor","ghostingControl","ghostCustomSteps","ghostPreSteps","ghostPostSteps",
                "ghostStepSize","ghostFrames","ghostColorPreA","ghostColorPre","ghostColorPreR","ghostColorPreG","ghostColorPreB","ghostColorPostA","ghostColorPost","ghostColorPostR","ghostColorPostG",
                "ghostColorPostB","ghostRangeStart","ghostRangeEnd","ghostDriver","hiddenInOutliner","stereoHorizontalImageTranslate","stereoHorizontalImageTranslateEnabled","postProjection",
                "filmRollControl","imagePlane","bookmarks"]
                #"mentalRayControls","miRenderPassList"]            
            
            xformNode1Attrs = cmds.listAttr(xformNode1)
            #print "xformNode1Attrs = ",xformNode1Attrs
            for rm in attrsRem_xform:
                #print "xformNode1Attrs = ",xformNode1Attrs            
                #print "rm1 = ",rm
                xformNode1Attrs.remove(rm)                    
            shapeNode1Attrs = cmds.listAttr(shapeNode1)
            #print "shapeNode1Attrs = ",shapeNode1Attrs
            for rm in attrsRem_shape:
                #print "rm2 = ",rm
                shapeNode1Attrs.remove(rm)
            xformNode2Attrs = cmds.listAttr(xformNode2)
            #print "xformNode2Attrs = ",xformNode2Attrs
            for rm in attrsRem_xform:
                #print "xformNode2Attrs = ",xformNode2Attrs            
                #print "rm3 = ",rm
                xformNode2Attrs.remove(rm)                    
            shapeNode2Attrs = cmds.listAttr(shapeNode2)
            #print "shapeNode2Attrs = ",shapeNode2Attrs
            for rm in attrsRem_shape:
                #print "rm4 = ",rm
                shapeNode2Attrs.remove(rm)                         
    
            for xnA1 in xformNode1Attrs:
                for xnA2 in xformNode2Attrs:
                    if xnA1 == xnA2:
                        #print xnA2
                        val1 = cmds.getAttr(xformNode1 + "." + xnA1)                                           
                        typ = type(val1)
                        typ = str(typ)
                        typ = typ.replace("<type '","")
                        typ = typ.replace("'>","")                    
                        if typ == "float" or typ == "int":
                            lckState = cmds.lockNode((xformNode2 + "." + xnA2),lock = True, query = True)
                            lckState = lckState[0]                                 
                            if lckState == 0:
                                print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                            
                                cmds.setAttr((xformNode2 + "." + xnA2), val1)
                        if typ == "bool":
                            lckState = cmds.lockNode((xformNode2 + "." + xnA2),lock = True, query = True)
                            lckState = lckState[0]                                 
                            if lckState == 0:
                                print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                            
                                cmds.setAttr((xformNode2 + "." + xnA2), val1)                        
                        if typ == "list":
                            val1 = val1[0]
                            strVal1 = str(val1)
                            strVal1 = strVal1.replace("(","")
                            strVal1 = strVal1.replace(")","")                          
                            spVal1 = strVal1.split(",")
                            sizVal = len(spVal1)                        
                            if sizVal == 2:
                                strSet = (xformNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:
                                    print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                               
                                    cmds.setAttr(strSet,val1[0],val1[1])                                                     
                            if sizVal == 3:
                                strSet = (xformNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:
                                    print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                                    
                                    cmds.setAttr(strSet,val1[0],val1[1],val1[2])
                            if sizVal == 4:
                                strSet = (xformNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:                                    
                                    print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                    
                                    cmds.setAttr(strSet,val1[0],val1[1],val1[2])
            
            for xnA1 in xformNode1Attrs:
                for xnA2 in xformNode2Attrs:
                    if xnA1 == xnA2:
                        conTypes = []
                        cons = cmds.listConnections(xformNode1 + "." + xnA1) or []
                        for con in cons:
                            conType = cmds.nodeType(cons)
                            if "ramp" == conType:                                                               
                                print "connecting " + con + " to " + (xformNode2 + "." + xnA2)
                                cmds.connectAttr((con + ".outColor"),(xformNode2 + "." + xnA2),force = True)  
                                
            for xnA1 in shapeNode1Attrs:
                for xnA2 in shapeNode2Attrs:
                    if xnA1 == xnA2:
                        #print xnA2
                        val1 = cmds.getAttr(shapeNode1 + "." + xnA1)                                           
                        typ = type(val1)
                        typ = str(typ)
                        typ = typ.replace("<type '","")
                        typ = typ.replace("'>","")                    
                        if typ == "float" or typ == "int":
                            lckState = cmds.lockNode((shapeNode2 + "." + xnA2),lock = True, query = True)
                            lckState = lckState[0]                                 
                            if lckState == 0:
                                print "transfering attribute " + (shapeNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (shapeNode2 + "." + xnA2)                                                            
                                cmds.setAttr((shapeNode2 + "." + xnA2), val1)
                        if typ == "bool":
                            lckState = cmds.lockNode((shapeNode2 + "." + xnA2),lock = True, query = True)
                            lckState = lckState[0]                                 
                            if lckState == 0:
                                print "transfering attribute " + (shapeNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (shapeNode2 + "." + xnA2)                                                            
                                cmds.setAttr((shapeNode2 + "." + xnA2), val1)                        
                        if typ == "list":
                            val1 = val1[0]
                            strVal1 = str(val1)
                            strVal1 = strVal1.replace("(","")
                            strVal1 = strVal1.replace(")","")                          
                            spVal1 = strVal1.split(",")
                            sizVal = len(spVal1)                        
                            if sizVal == 2:
                                strSet = (shapeNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:
                                    print "transfering attribute " + (shapeNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (shapeNode2 + "." + xnA2)                                                               
                                    cmds.setAttr(strSet,val1[0],val1[1])                                                     
                            if sizVal == 3:
                                strSet = (shapeNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:
                                    print "transfering attribute " + (shapeNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (shapeNode2 + "." + xnA2)                                                                    
                                    cmds.setAttr(strSet,val1[0],val1[1],val1[2])
                            if sizVal == 4:
                                strSet = (shapeNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:                                    
                                    print "transfering attribute " + (shapeNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (shapeNode2 + "." + xnA2)                                    
                                    cmds.setAttr(strSet,val1[0],val1[1],val1[2])
            for xnA1 in shapeNode1Attrs:
                for xnA2 in shapeNode2Attrs:
                    if xnA1 == xnA2:
                        conTypes = []
                        cons = cmds.listConnections(shapeNode1 + "." + xnA1) or []
                        for con in cons:
                            conType = cmds.nodeType(cons)
                            if "ramp" == conType:                                                               
                                print "connecting " + con + " to " + (shapeNode2 + "." + xnA2)
                                cmds.connectAttr((con + ".outColor"),(shapeNode2 + "." + xnA2),force = True)

        if self.XformNodeType == "transform" and self.shapeNodeType == "VRayLightRectShape":
            obs = cmds.ls()
            for ob in obs:
                #print "unlinking " + shapeNode2 + " from " + ob
                cmds.lightlink(b = True, light = shapeNode2, object = ob)                 
            links = cmds.lightlink( query = True, light = shapeNode1 )
            for link in links:
                if link != "initialShadingGroup":
                    print "linking " + shapeNode2 + " to " + link
                    cmds.lightlink(make = True, light = shapeNode2, object = link)                        
                                
        if self.Node1Type == "VRayMtl":                      
            if self.Node1Type == "VRayMtl":
                xformNode1 = self.nodeOne
                xformNode2 = self.nodeTwo
                attrsRem_xform = ["message","anisotropyUVWGen","attributeAliasList"]
                #"mentalRayControls"]                          
            
            xformNode1Attrs = cmds.listAttr(xformNode1)
            #print "xformNode1Attrs = ",xformNode1Attrs
            for rm in attrsRem_xform:
                #print "xformNode1Attrs = ",xformNode1Attrs            
                #print "rm1 = ",rm
                xformNode1Attrs.remove(rm)                    
            xformNode2Attrs = cmds.listAttr(xformNode2)
            #print "xformNode2Attrs = ",xformNode2Attrs
            for rm in attrsRem_xform:
                #print "xformNode2Attrs = ",xformNode2Attrs            
                #print "rm3 = ",rm
                xformNode2Attrs.remove(rm)                                             
            for xnA1 in xformNode1Attrs:
                for xnA2 in xformNode2Attrs:
                    if xnA1 == xnA2:
                        #print xnA2
                        val1 = cmds.getAttr(xformNode1 + "." + xnA1)                                           
                        typ = type(val1)
                        typ = str(typ)
                        typ = typ.replace("<type '","")
                        typ = typ.replace("'>","")                    
                        if typ == "float" or typ == "int":
                            lckState = cmds.lockNode((xformNode2 + "." + xnA2),lock = True, query = True)
                            lckState = lckState[0]                                 
                            if lckState == 0:
                                print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                            
                                cmds.setAttr((xformNode2 + "." + xnA2), val1)
                        if typ == "bool":
                            lckState = cmds.lockNode((xformNode2 + "." + xnA2),lock = True, query = True)
                            lckState = lckState[0]                                 
                            if lckState == 0:
                                print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                            
                                cmds.setAttr((xformNode2 + "." + xnA2), val1)                        
                        if typ == "list":
                            val1 = val1[0]
                            strVal1 = str(val1)
                            strVal1 = strVal1.replace("(","")
                            strVal1 = strVal1.replace(")","")                          
                            spVal1 = strVal1.split(",")
                            sizVal = len(spVal1)                        
                            if sizVal == 2:
                                strSet = (xformNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:
                                    print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                               
                                    cmds.setAttr(strSet,val1[0],val1[1])                                                     
                            if sizVal == 3:
                                strSet = (xformNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:
                                    print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                                                    
                                    cmds.setAttr(strSet,val1[0],val1[1],val1[2])
                            if sizVal == 4:
                                strSet = (xformNode2 + "." + xnA2)
                                lckState = cmds.lockNode(strSet,lock = True, query = True)
                                lckState = lckState[0]                                 
                                if lckState == 0:                                    
                                    print "transfering attribute " + (xformNode1 + "." + xnA2) + " value of " + str(val1) + " to " + (xformNode2 + "." + xnA2)                                    
                                    cmds.setAttr(strSet,val1[0],val1[1],val1[2])            
            for xnA1 in xformNode1Attrs:
                for xnA2 in xformNode2Attrs:
                    if xnA1 == xnA2:
                        conTypes = []
                        cons = cmds.listConnections(xformNode1 + "." + xnA1) or []
                        for con in cons:
                            conType = cmds.nodeType(cons)
                            if "ramp" == conType:                                                               
                                print "connecting " + con + " to " + (xformNode2 + "." + xnA2)
                                cmds.connectAttr((con + ".outColor"),(xformNode2 + "." + xnA2),force = True)                                                                                                                                                                                                                                                         
        
def xferNode(pathMatchObject,pathChildObject,*args):
    
    nodeOne = cmds.textField(pathMatchObject,text = True,query = True)
    nodeTwo = cmds.textField(pathChildObject,text = True,query = True)                
    
    xferClassInstance = transferAttrsClass(nodeOne,nodeTwo)
    xferClassInstance.xferAttrs()
    
def objectChooseWin():    
    name = "transferAttrs"            
    windowSize = (300,100)    
    if (cmds.window(name, exists = True)):
        cmds.deleteUI(name)        
    window = cmds.window(name, title = name, width = 100, height = 50)        
    cmds.columnLayout("mainColumn", adjustableColumn = True)
    cmds.rowLayout("nameRowLayout01", numberOfColumns = 2, parent = "mainColumn")    
    cmds.text(label = "mast_obj  ")
    pathMatchObject = cmds.textField(tx = "VRayMtl1")        
    cmds.rowLayout("nameRowLayout02", numberOfColumns = 2, parent = "mainColumn")    
    cmds.text(label = "child_obj")
    pathChildObject = cmds.textField(tx = "VRayMtl2")         
    cmds.rowLayout("nameRowLayout2.5", numberOfColumns = 10, parent = "mainColumn")                              
    cmds.rowLayout("nameRowLayout4.5", numberOfColumns = 10, parent = "mainColumn")                                        
    cmds.rowLayout("nameRowLayout05", numberOfColumns = 1, parent = "mainColumn")            
    cmds.button(label = "xfer attrs", command = partial(xferNode,pathMatchObject,pathChildObject))    
    cmds.showWindow()
    
objectChooseWin() 