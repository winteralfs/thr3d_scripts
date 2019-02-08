import maya.cmds as cmds

print 'changes eight'

class rigClass():
    def __init__(self,obj,renLays,lightRigName,lightType,numLights,lights,transform,rotates,scales,lightColor,intensityMultiplier,Usize,Vsize,directional,directionalPreviewLength,usRectTex,rectTexColor,noDecay,doubleSided,invisible,affectDiffuse,affectSpecular,affectReflections,diffuseContrib,specularContrib,scaler,rampNames,ramps,rampAssigns,overides,obsNotInLay,vizaNotInLay,lightLinks):
        self.objects = cmds.ls(type = "transform")
        self.obj = obj
        self.renLays = renLays
        self.lightRigName = lightRigName
        self.lightType = lightType
        self.numLights = numLights
        self.lights = lights
        self.transform = transform
        self.rotates = rotates
        self.scales = scales
        self.lightColor = lightColor
        self.intensityMultiplier = intensityMultiplier
        self.Usize = Usize
        self.Vsize = Vsize
        self.directional = directional
        self.directionalPreviewLength = directionalPreviewLength
        self.usRectTex = usRectTex
        self.rectTexColor = rectTexColor
        self.noDecay = noDecay
        self.doubleSided = doubleSided
        self.invisible = invisible
        self.affectDiffuse = affectDiffuse
        self.affectSpecular = affectSpecular
        self.affectReflections = affectReflections
        self.diffuseContrib = diffuseContrib
        self.specularContrib = specularContrib
        self.scaler = scaler
        self.rampNames = rampNames
        self.ramps = ramps
        self.rampAssigns = rampAssigns
        self.overides = overides
        self.obsNotInLay = obsNotInLay
        self.vizaNotInLay = vizaNotInLay
        self.lightLinks = lightLinks

    def rigGen(self):
        it = 0
        groupNode = cmds.group(em = True, name = self.lightRigName)

        while it < self.numLights:
            newNode = cmds.shadingNode(self.lightType, asLight=True)
            kidsG = cmds.listRelatives(newNode, children = True)
            if "Shape" in kidsG[0]:
                parentG = newNode
            if "Shape" not in kidsG[0]:
                parentG = cmds.listRelatives(newNode, parent = True)
            cmds.rename(parentG,self.lights[it])
            cmds.parent(self.lights[it],groupNode)
            it = it + 1

        cmds.select(groupNode)
        cmds.xform(centerPivots = True)
        for rl in self.renLays:
            if rl == "Ft":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers(rl, groupNode)
            if rl == "Bk":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers( rl,groupNode)
                cmds.editRenderLayerAdjustment(groupNode + ".rotate")
                cmds.setAttr((groupNode + ".rotateY"),180)
                cmds.editRenderLayerMembers(rl,groupNode)
            if rl == "Lt":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers(rl,groupNode)
                cmds.editRenderLayerAdjustment(groupNode + ".rotate")
                cmds.setAttr((groupNode + ".rotateY"),-90)
                cmds.editRenderLayerMembers(rl,groupNode)
            if rl == "Rt":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers(rl,groupNode)
                cmds.editRenderLayerAdjustment(groupNode + ".rotate")
                cmds.setAttr((groupNode + ".rotateY"),90)
                cmds.editRenderLayerMembers(rl,groupNode)
            if rl == "Tp":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerAdjustment(groupNode + ".rotate")
                cmds.setAttr((groupNode + ".rotateX"),-90)
                cmds.editRenderLayerMembers(rl,groupNode)
            if rl == "Bt":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers(rl,groupNode)
                cmds.editRenderLayerAdjustment(groupNode + ".rotate")
                cmds.setAttr((groupNode + ".rotateX"),90)
            if rl == "FtLtTp":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers(rl,groupNode)
            if rl == "FtRtTp":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers(rl,groupNode)
            if rl == "FtTp":
                cmds.editRenderLayerGlobals(currentRenderLayer = rl)
                cmds.editRenderLayerMembers(rl,groupNode)
        cmds.select(clear = True)

        it = 0
        while it < self.numLights:
            trans = self.transform[it]
            rot = self.rotates[it]
            sca = self.scales[it]
            lightColor = self.lightColor[it]
            im = self.intensityMultiplier[it]
            Usz = self.Usize[it]
            Vsz = self.Vsize[it]
            dir = self.directional[it]
            dirPL = self.directionalPreviewLength[it]
            useRectTex = self.usRectTex[it]
            rectTexColor = self.rectTexColor[it]
            noDecay = self.noDecay[it]
            doubleSided = self.doubleSided[it]
            invisible = self.invisible[it]
            affectDiffuse = self.affectDiffuse[it]
            affectSpecular = self.affectSpecular[it]
            affectReflections = self.affectReflections[it]
            diffuseContrib = self.diffuseContrib[it]
            specularContrib = self.specularContrib[it]
            scaler = self.scaler

            bbox = cmds.exactWorldBoundingBox(self.obj)
            xBBsize = bbox[3] - bbox[0]
            yBBsize = bbox[4] - bbox[1]
            zBBsize = bbox[5] - bbox[2]

            scalerX = 1
            scalerY = 1
            scalerZ = 1

            scalerX = xBBsize/30
            scalerY = yBBsize/22
            scalerZ = zBBsize/6

            cmds.select(self.lights[it])
            cmds.xform(t = ((trans[0]*scalerX),(trans[1]*(scalerY*.88)),(trans[2]*scalerZ)), ro = (rot[0],rot[1],rot[2]))
            cmds.select(clear = True)
            cmds.setAttr((self.lights[it] + ".lightColor"),lightColor[0],lightColor[1],lightColor[2])
            cmds.setAttr((self.lights[it] + ".intensityMult"),im)
            cmds.setAttr((self.lights[it] + ".uSize"),Usz * (scalerX/1.1))
            cmds.setAttr((self.lights[it] + ".vSize"),Vsz * (scalerY/1.1))
            cmds.setAttr((self.lights[it] + ".directional"),dir)
            cmds.setAttr((self.lights[it] + ".directionalPreviewLength"),dirPL)
            cmds.setAttr((self.lights[it] + ".useRectTex"),useRectTex)
            cmds.setAttr((self.lights[it] + ".rectTex"),rectTexColor[0],rectTexColor[1],rectTexColor[2])
            if useRectTex == 1:
                for ra in self.rampAssigns:
                    if ra == self.lights[it]:
                        #print "connecting " +  self.rampAssigns[self.lights[it]] + ".outColor" + " to " + self.lights[it] + "Shape.rectTex"
                        cmds.connectAttr(self.rampAssigns[self.lights[it]] + ".outColor", self.lights[it] + "Shape.rectTex")
                        cmds.setAttr(self.lights[it] + "Shape" + ".showTex",1)
            cmds.setAttr((self.lights[it] + ".noDecay"),noDecay)
            cmds.setAttr((self.lights[it] + ".doubleSided"),doubleSided)
            cmds.setAttr((self.lights[it] + ".invisible"),invisible)
            cmds.setAttr((self.lights[it] + ".affectDiffuse"),affectDiffuse)
            cmds.setAttr((self.lights[it] + ".affectSpecular"),affectSpecular)
            cmds.setAttr((self.lights[it] + ".affectReflections"),affectReflections)
            cmds.setAttr((self.lights[it] + ".diffuseContrib"),diffuseContrib)
            cmds.setAttr((self.lights[it] + ".specularContrib"),specularContrib)
            for vznl in self.vizaNotInLay:
                vzSplit = vznl.split("%")
                vzLight = vzSplit[0]
                vzLayer = vzSplit[1]
                if vzLight == self.lights[it]:
                    cmds.editRenderLayerGlobals(currentRenderLayer = vzLayer)
                    cmds.setAttr(vzLight + ".visibility",0)
                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
            for onil in self.obsNotInLay:
                ilSplit = onil.split("%")
                ilLight = ilSplit[0]
                ilLayer = ilSplit[1]
                if ilLight == self.lights[it]:
                    cmds.editRenderLayerGlobals(currentRenderLayer = ilLayer)
                    cmds.setAttr(ilLight + ".visibility",0)
                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")
            for ll in self.lightLinks:
               if ll == self.lights[it]:
                    for obs in self.objects:
                        cmds.lightlink(b = True,light=(ll),object = obs)
                    cmds.lightlink(light=(ll),object =(self.lightLinks[ll]))
                    cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")

            for ors in self.overides:
                orsNameSp = ors.split("%")
                orLight = orsNameSp[0]
                overLay = orsNameSp[1]
                if orLight == self.lights[it]:
                    ovrAttr = orsNameSp[2]
                    overKnd = orsNameSp[3]
                    ovrAttrAmt = orsNameSp[4]
                    cmds.editRenderLayerGlobals(currentRenderLayer = overLay)
                    attrEx = cmds.attributeQuery(ovrAttr,node = orLight, exists = True)
                    attrExShape = cmds.attributeQuery(ovrAttr,node = (orLight + "Shape"), exists = True)
                    if attrEx == 1:
                        cmds.editRenderLayerAdjustment(orLight + "." + (ovrAttr[:-1]))
                        if overKnd == "int":
                            cmds.setAttr((orLight + "." + ovrAttr),int(ovrAttrAmt))
                        if overKnd == "flt":
                            cmds.setAttr((orLight + "." + ovrAttr),float(ovrAttrAmt))
                        if overKnd == "tup":
                            cmds.setAttr((orLight + "." + ovrAttr),tupple(ovrAttrAmt))
                        if overKnd == "str":
                            cmds.setAttr((orLight + "." + ovrAttr),str(ovrAttrAmt))
                        if overKnd == "con":
                            cmds.setAttr((orLight + "." + ovrAttr),str(ovrAttrAmt))
                    if attrExShape == 1:
                        cmds.editRenderLayerAdjustment(orLight + "Shape." + ovrAttr)
                        if overKnd == "int":
                            cmds.setAttr((orLight + "Shape." + ovrAttr),int(ovrAttrAmt))
                        if overKnd == "flt":
                            cmds.setAttr((orLight + "Shape." + ovrAttr),float(ovrAttrAmt))
                        if overKnd == "tup":
                            cmds.setAttr((orLight + "Shape." + ovrAttr),tupple(ovrAttrAmt))
                        if overKnd == "str":
                            cmds.setAttr((orLight + "Shape." + ovrAttr),str(ovrAttrAmt))
                        if overKnd == "con":
                            cmds.setAttr((orLight + "Shape." + ovrAttr),str(ovrAttrAmt))
            cmds.editRenderLayerGlobals(currentRenderLayer = "defaultRenderLayer")

            it = it + 1

def rampsGen(rampNames):
    ramps = []
    #rampNames = ["layTex_hor","layTex_ver","layTex_circle","layTex_horBars","layTex_verBars","layTex_square","ramp_leftSideDiffuse","ramp_edgeSpec","ramp_RightSideDiffuse","ramp_RightSpec","ramp_LeftSpec","ramp_BackEdge","ramp_TopSpec"]
    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_hor")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[0])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(plac2d + ".rotateUV",90)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_leftSideDiffuse")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[6])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type",1)
    cmds.setAttr(ramp + ".colorEntryList[1].position",1)
    cmds.setAttr(ramp + ".colorEntryList[0].position",0)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_RightSideDiffuse")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[8])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type",1)
    cmds.setAttr(ramp + ".colorEntryList[1].position",0)
    cmds.setAttr(ramp + ".colorEntryList[0].position",1)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_ver")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[1])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_circle")
    ramp = cmds.createNode("ramp",name = "ramp_circle")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[2])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type",4)
    cmds.setAttr(ramp + ".colorEntryList[1].position",.2)
    cmds.setAttr(ramp + ".colorEntryList[0].position",.7)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_circle")
    ramp = cmds.createNode("ramp",name = "ramp_edgeSpec")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[7])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type")
    cmds.setAttr(ramp + ".colorEntryList[2].position",.57)
    cmds.setAttr(ramp + ".colorEntryList[1].position",.5)
    cmds.setAttr(ramp + ".colorEntryList[0].position",.4)
    cmds.setAttr(ramp + ".colorEntryList[2].color",0,0,0)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(ramp + ".interpolation",4)
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_RightSpec")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[9])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type",2)
    cmds.setAttr(ramp + ".colorEntryList[1].position",.668)
    cmds.setAttr(ramp + ".colorEntryList[0].position",0)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    cmds.setAttr(plac2d + ".repeatU",-1)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_LeftSpec")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[10])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type",2)
    cmds.setAttr(ramp + ".colorEntryList[1].position",.668)
    cmds.setAttr(ramp + ".colorEntryList[0].position",0)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_BackEdge")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[11])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type",0)
    cmds.setAttr(ramp + ".colorEntryList[1].position",.5)
    cmds.setAttr(ramp + ".colorEntryList[2].position",.666)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp + ".colorEntryList[2].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d = cmds.createNode("place2dTexture",name = "place2dTexture_hor")
    ramp = cmds.createNode("ramp",name = "ramp_TopSpec")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[11])
    cmds.connectAttr((plac2d + ".outUV"),(ramp + ".uvCoord"))
    cmds.connectAttr((plac2d + ".outUvFilterSize"),(ramp + ".uvFilterSize"))
    cmds.connectAttr((ramp + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp + ".type",0)
    cmds.setAttr(ramp + ".colorEntryList[0].position",0)
    cmds.setAttr(ramp + ".colorEntryList[1].position",.5)
    cmds.setAttr(ramp + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(ramp + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(plac2d + ".rotateUV",0)
    ramps.append(lay2D)

    plac2d_1 = cmds.createNode("place2dTexture",name = "place2dTexture_horBars_1")
    ramp_1 = cmds.createNode("ramp",name = "ramp_horBars_1")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[3])
    cmds.connectAttr((plac2d_1 + ".outUV"),(ramp_1 + ".uvCoord"))
    cmds.connectAttr((plac2d_1 + ".outUvFilterSize"),(ramp_1 + ".uvFilterSize"))
    cmds.connectAttr((ramp_1 + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp_1 + ".colorEntryList[1].position",.6)
    cmds.setAttr(ramp_1 + ".colorEntryList[0].position",.8)
    cmds.setAttr(ramp_1 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_1 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    plac2d_2 = cmds.createNode("place2dTexture",name = "place2dTexture_horBars_2")
    ramp_2 = cmds.createNode("ramp",name = "ramp_horBars_2")
    cmds.connectAttr((plac2d_2 + ".outUV"),(ramp_2 + ".uvCoord"))
    cmds.connectAttr((plac2d_2 + ".outUvFilterSize"),(ramp_2 + ".uvFilterSize"))
    cmds.connectAttr((ramp_2 + ".outColor"),(lay2D + ".inputs[1].color"))
    cmds.setAttr(ramp_2 + ".colorEntryList[1].position",.6)
    cmds.setAttr(ramp_2 + ".colorEntryList[0].position",.8)
    cmds.setAttr(ramp_2 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_2 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d_2 + ".rotateUV",180)
    cmds.setAttr(lay2D + ".inputs[0].blendMode",6)
    ramps.append(lay2D)

    plac2d_1 = cmds.createNode("place2dTexture",name = "place2dTexture_verBars_1")
    ramp_1 = cmds.createNode("ramp",name = "ramp_verBars_1")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[4])
    cmds.connectAttr((plac2d_1 + ".outUV"),(ramp_1 + ".uvCoord"))
    cmds.connectAttr((plac2d_1 + ".outUvFilterSize"),(ramp_1 + ".uvFilterSize"))
    cmds.connectAttr((ramp_1 + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp_1 + ".colorEntryList[1].position",.6)
    cmds.setAttr(ramp_1 + ".colorEntryList[0].position",.8)
    cmds.setAttr(ramp_1 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_1 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    plac2d_2 = cmds.createNode("place2dTexture",name = "place2dTexture_verBars_2")
    ramp_2 = cmds.createNode("ramp",name = "ramp_verBars_2")
    cmds.connectAttr((plac2d_2 + ".outUV"),(ramp_2 + ".uvCoord"))
    cmds.connectAttr((plac2d_2 + ".outUvFilterSize"),(ramp_2 + ".uvFilterSize"))
    cmds.connectAttr((ramp_2 + ".outColor"),(lay2D + ".inputs[1].color"))
    cmds.setAttr(ramp_2 + ".colorEntryList[1].position",.6)
    cmds.setAttr(ramp_2 + ".colorEntryList[0].position",.8)
    cmds.setAttr(ramp_2 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_2 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d_1 + ".rotateUV",90)
    cmds.setAttr(plac2d_2 + ".rotateUV",-90)
    cmds.setAttr(lay2D + ".inputs[0].blendMode",6)
    ramps.append(lay2D)

    plac2d_1 = cmds.createNode("place2dTexture",name = "place2dTexture_horBars_1")
    ramp_1 = cmds.createNode("ramp",name = "ramp_horBars_1")
    lay2D = cmds.createNode("layeredTexture", name = rampNames[5])
    cmds.connectAttr((plac2d_1 + ".outUV"),(ramp_1 + ".uvCoord"))
    cmds.connectAttr((plac2d_1 + ".outUvFilterSize"),(ramp_1 + ".uvFilterSize"))
    cmds.connectAttr((ramp_1 + ".outColor"),(lay2D + ".inputs[0].color"))
    cmds.setAttr(ramp_1 + ".colorEntryList[1].position",.8)
    cmds.setAttr(ramp_1 + ".colorEntryList[0].position",1)
    cmds.setAttr(ramp_1 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_1 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d + ".rotateUV",0)
    plac2d_2 = cmds.createNode("place2dTexture",name = "place2dTexture_horBars_2")
    ramp_2 = cmds.createNode("ramp",name = "ramp_horBars_2")
    cmds.connectAttr((plac2d_2 + ".outUV"),(ramp_2 + ".uvCoord"))
    cmds.connectAttr((plac2d_2 + ".outUvFilterSize"),(ramp_2 + ".uvFilterSize"))
    cmds.connectAttr((ramp_2 + ".outColor"),(lay2D + ".inputs[1].color"))
    cmds.setAttr(ramp_2 + ".colorEntryList[1].position",.8)
    cmds.setAttr(ramp_2 + ".colorEntryList[0].position",1)
    cmds.setAttr(ramp_2 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_2 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d_2 + ".rotateUV",180)
    cmds.setAttr(lay2D + ".inputs[0].blendMode",6)
    plac2d_3 = cmds.createNode("place2dTexture",name = "place2dTexture_verBars_1")
    ramp_3 = cmds.createNode("ramp",name = "ramp_verBars_1")
    cmds.connectAttr((plac2d_3 + ".outUV"),(ramp_3 + ".uvCoord"))
    cmds.connectAttr((plac2d_3 + ".outUvFilterSize"),(ramp_3 + ".uvFilterSize"))
    cmds.connectAttr((ramp_3 + ".outColor"),(lay2D + ".inputs[2].color"))
    cmds.setAttr(ramp_3 + ".colorEntryList[1].position",.8)
    cmds.setAttr(ramp_3 + ".colorEntryList[0].position",1)
    cmds.setAttr(ramp_3 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_3 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d_3 + ".rotateUV",90)
    plac2d_4 = cmds.createNode("place2dTexture",name = "place2dTexture_verBars_2")
    ramp_4 = cmds.createNode("ramp",name = "ramp_verBars_2")
    cmds.connectAttr((plac2d_4 + ".outUV"),(ramp_4 + ".uvCoord"))
    cmds.connectAttr((plac2d_4 + ".outUvFilterSize"),(ramp_4 + ".uvFilterSize"))
    cmds.connectAttr((ramp_4 + ".outColor"),(lay2D + ".inputs[3].color"))
    cmds.setAttr(ramp_4 + ".colorEntryList[1].position",.8)
    cmds.setAttr(ramp_4 + ".colorEntryList[0].position",1)
    cmds.setAttr(ramp_4 + ".colorEntryList[1].color",1,1,1)
    cmds.setAttr(ramp_4 + ".colorEntryList[0].color",0,0,0)
    cmds.setAttr(plac2d_4 + ".rotateUV",-90)
    cmds.setAttr(lay2D + ".inputs[0].blendMode",6)
    cmds.setAttr(lay2D + ".inputs[1].blendMode",6)
    cmds.setAttr(lay2D + ".inputs[2].blendMode",6)
    cmds.setAttr(lay2D + ".inputs[3].blendMode",1)
    ramps.append(lay2D)

    return(ramps)


def lightRig_box_nicoderm():
    obj = cmds.ls(sl = True) or "Product_Master_Group"
    renLays = ["Ft","Bk","Lt","Rt","Tp","Bt","FtTp","FtRtTp","FtLtTp"]
    lightRigName = "lightRig_box"
    lightType = "VRayLightRectShape"
    numLights = 10
    lights = ["front_light_diff","top_light_spec","top_light_dif","back_light","left_light_spec","right_light_spec","bottom_light","left_light_dif","right_light_dif","edgeSpec_light","","","","","","","","","",""]
    transform = [(0,12,25),(0,24,-9),(0,36,0),(0,10,-7),(-25,9,5),(25,9,5),(0,-3.6,0),(-32,12.5,5),(33,12.5,4),(0,28,15),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
    rotates = [(0,0,0),(-104,0,0),(-90,0,0),(-6,180,0),(0,-45,0),(0,45,0),(90,0,0),(0,-108,0),(0,-252,0),(-18.5,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0),(0,0,0)]
    scales = [(1,1,1),(1,1,1),(1,1,1,),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1)]
    lightColor = [(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1)]
    intensityMultiplier = [1.2,.06,4,1,2,2,.8,8,8,.125,1,1,1,1,1,1,1,1,1,1]
    Usize = [30,24,25,24,18,18,12,18,18,24,1,1,1,1,1,1,1,1,1,1,1]
    Vsize = [30,6,12,16,16,16,12,16,16,15,7.5,1,1,1,1,1,1,1,1,1,1]
    directional = [0,.45,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
    directionalPreviewLength = [1,10,1,1,1,1,1,1,1,10,1,1,1,1,1,1,1,1,1,1]
    usRectTex = [0,1,0,1,1,1,0,1,1,1,0,0,0,0,0,0,0,0,0,0]
    rectTexColor = [(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1),(1,1,1)]
    noDecay = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    doubleSided = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    invisible = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    affectDiffuse = [1,0,1,1,0,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1]
    affectSpecular = [0,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    affectReflections = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    diffuseContrib = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    specularContrib = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    scaler = 1
    rampNames = ["layTex_hor","layTex_ver","layTex_circle","layTex_horBars","layTex_verBars","layTex_square","ramp_leftSideDiffuse","ramp_edgeSpec","ramp_RightSideDiffuse","ramp_RightSpec","ramp_LeftSpec","ramp_BackEdge","ramp_TopSpec"]
    ramps = rampsGen(rampNames)
    #{lights[0]:rampNames[0]}
    rampAssigns = {lights[1]:rampNames[12],lights[3]:rampNames[11],lights[4]:rampNames[10],lights[5]:rampNames[9],lights[7]:rampNames[6],lights[8]:rampNames[8],lights[9]:rampNames[7]}
    #{lights[0]:renLays[1] + "%intensityMult" + "%flt" + "%" + "3"}
    overides = [lights[3] + "%" + renLays[5] + "%" + "translateZ" + "%flt" + "%" + "-20.5",lights[4] + "%" + renLays[4] + "%" + "translateX" + "%flt" + "%" + "-20",lights[5] + "%" + renLays[4] + "%" + "translateX" + "%flt" + "%" + "20",lights[3] + "%" + renLays[3] + "%" + "translateZ" + "%flt" + "%" + "-20",lights[3] + "%" + renLays[7] + "%" + "intensityMult" + "%flt" + "%" + ".1",lights[3] + "%" + renLays[8] + "%" + "intensityMult" + "%flt" + "%" + ".1",lights[9] + "%" + renLays[1] + "%" + "intensityMult" + "%flt" + "%" + ".05",lights[0] + "%" + renLays[4] + "%" + "translateY" + "%flt" + "%" + "0",lights[0] + "%" + renLays[5] + "%" + "translateY" + "%flt" + "%" + "0",lights[0] + "%" + renLays[4] + "%" + "translateZ" + "%flt" + "%" + "28",lights[0] + "%" + renLays[5] + "%" + "translateZ" + "%flt" + "%" + "12"]
    #[(lights[2] + "%" + renLays[2])]
    obsNotInLay = []
    #[(lights[2] + "%" + renLays[2])]
    vizaNotInLay = [(lights[2] + "%" + renLays[2]),(lights[2] + "%" + renLays[3]),(lights[2] + "%" + renLays[4]),(lights[2] + "%" + renLays[5]),(lights[4] + "%" + renLays[4]),(lights[4] + "%" + renLays[5]),(lights[5] + "%" + renLays[4]),(lights[5] + "%" + renLays[5]),(lights[6] + "%" + renLays[4]),(lights[6] + "%" + renLays[5]),(lights[7] + "%" + renLays[4]),(lights[7] + "%" + renLays[5]),(lights[9] + "%" + renLays[2]),(lights[9] + "%" + renLays[3]),(lights[9] + "%" + renLays[4]),(lights[9] + "%" + renLays[5]),(lights[1] + "%" + renLays[4]),(lights[2] + "%" + renLays[4]),(lights[3] + "%" + renLays[4]),(lights[4] + "%" + renLays[4]),(lights[5] + "%" + renLays[4]),(lights[6] + "%" + renLays[4]),(lights[7] + "%" + renLays[4]),(lights[8] + "%" + renLays[4]),(lights[9] + "%" + renLays[4]),(lights[1] + "%" + renLays[5]),(lights[2] + "%" + renLays[5]),(lights[3] + "%" + renLays[5]),(lights[4] + "%" + renLays[5]),(lights[5] + "%" + renLays[5]),(lights[6] + "%" + renLays[5]),(lights[7] + "%" + renLays[5]),(lights[8] + "%" + renLays[5]),(lights[9] + "%" + renLays[5]),(lights[1] + "%" + renLays[2]),(lights[1] + "%" + renLays[2]),(lights[2] + "%" + renLays[2]),(lights[3] + "%" + renLays[2]),(lights[4] + "%" + renLays[2]),(lights[5] + "%" + renLays[2]),(lights[6] + "%" + renLays[2]),(lights[7] + "%" + renLays[2]),(lights[8] + "%" + renLays[2]),(lights[9] + "%" + renLays[3]),(lights[1] + "%" + renLays[3]),(lights[1] + "%" + renLays[3]),(lights[2] + "%" + renLays[3]),(lights[3] + "%" + renLays[3]),(lights[4] + "%" + renLays[3]),(lights[5] + "%" + renLays[3]),(lights[6] + "%" + renLays[3]),(lights[7] + "%" + renLays[3]),(lights[8] + "%" + renLays[3]),(lights[9] + "%" + renLays[3])]
    #{lights[0]:"pSphere2"}
    lightLinks = {lights[0]:"Product_Master_Group", lights[1]:"Product_Master_Group",lights[2]:"Product_Master_Group",lights[3]:"Product_Master_Group",lights[4]:"Product_Master_Group",lights[5]:"Product_Master_Group",lights[6]:"Product_Master_Group",lights[7]:"Product_Master_Group",lights[8]:"Product_Master_Group",lights[9]:"Product_Master_Group"}
    box_Nicoderm = rigClass(obj,renLays,lightRigName,lightType,numLights,lights,transform,rotates,scales,lightColor,intensityMultiplier,Usize,Vsize,directional,directionalPreviewLength,usRectTex,rectTexColor,noDecay,doubleSided,invisible,affectDiffuse,affectSpecular,affectReflections,diffuseContrib,specularContrib,scaler,rampNames,ramps,rampAssigns,overides,obsNotInLay,vizaNotInLay,lightLinks)
    box_Nicoderm.rigGen()

lightRig_box_nicoderm()
