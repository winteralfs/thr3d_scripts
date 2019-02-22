import maya.cmds as cmds
import pymel.core as pm

def cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    print "p2d1 = ",p2d1
    print "p2d2 = ",p2d2

    box = 0

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)

    cutOutRampOneName = cmds.shadingNode("ramp", name="cu_circle", asTexture=True)
    pm.setAttr((cutOutRampOneName + ".type"), 4)

    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutRampOneName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutRampOneName + ".uvFilterSize")

    pm.setAttr((cutOutRampOneName + ".interpolation"), 4)

    blurMult = blurAmount * .05

    pm.setAttr((cutOutRampOneName + ".colorEntryList[1].color"), 1,1,1, type="double3")
    pm.setAttr((cutOutRampOneName + ".colorEntryList[0].color"), (0 + blurMult), (0 + blurMult), (0 + blurMult), type="double3")
    pm.setAttr((cu_p2d1 + ".rotateUV"), 0)
    pm.setAttr((cutOutRampOneName + ".colorEntryList[0].position"),0)
    pm.setAttr((cutOutRampOneName + ".colorEntryList[1].position"), 1)
    pm.setAttr((cutOutRampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampOneName + ".colorEntryList[0].color"), (0 + blurMult),(0 + blurMult), (0 + blurMult), type="double3")

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .01

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(cutOutRampOneName + ".colorEntryList[0].position",(.2 - blurMult))
        pm.setAttr(cutOutRampOneName + ".colorEntryList[1].position",(.5 + blurMult))
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 > 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 > 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)



def cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    box = 1

    print "p2d1 = ",p2d1
    print "p2d2 = ",p2d2

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4

    CO_layerTexHubName = cmds.shadingNode("layeredTexture", name="CO_twoRampNode", asTexture=True)

    cutOutRampOneName = cmds.shadingNode("ramp", name="cu_box", asTexture=True)
    pm.setAttr((cutOutRampOneName + ".type"), 1)

    cutOutRampTwoName = cmds.shadingNode("ramp", name="cu_box", asTexture=True)
    pm.setAttr((cutOutRampTwoName + ".type"), 1)

    cutOutRampThirdName = cmds.shadingNode("ramp", name="cu_box", asTexture=True)
    pm.setAttr((cutOutRampThirdName + ".type"), 1)

    cutOutRampFourName = cmds.shadingNode("ramp", name="cu_box", asTexture=True)
    pm.setAttr((cutOutRampThirdName + ".type"), 1)

    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)

    cu_p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d2 + ".repeatU", 1)

    cu_p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d3 + ".repeatU", 1)

    cu_p2d4 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d4 + ".repeatU", 1)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutRampOneName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutRampOneName + ".uvFilterSize")

    cmds.connectAttr(cu_p2d2 + ".outUV", cutOutRampTwoName + ".uvCoord")
    cmds.connectAttr(cu_p2d2 + ".outUvFilterSize", cutOutRampTwoName + ".uvFilterSize")

    cmds.connectAttr(cu_p2d3 + ".outUV", cutOutRampThirdName + ".uvCoord")
    cmds.connectAttr(cu_p2d3 + ".outUvFilterSize", cutOutRampThirdName + ".uvFilterSize")

    cmds.connectAttr(cu_p2d4 + ".outUV", cutOutRampFourName + ".uvCoord")
    cmds.connectAttr(cu_p2d4 + ".outUvFilterSize", cutOutRampFourName + ".uvFilterSize")

    pm.connectAttr((cutOutRampOneName + ".outColor"), (CO_layerTexHubName  + ".inputs[0].color"), force=True)
    pm.connectAttr((cutOutRampTwoName + ".outColor"), (CO_layerTexHubName  + ".inputs[1].color"), force=True)
    pm.connectAttr((cutOutRampThirdName + ".outColor"), (CO_layerTexHubName  + ".inputs[2].color"), force=True)
    pm.connectAttr((cutOutRampFourName + ".outColor"), (CO_layerTexHubName  + ".inputs[3].color"), force=True)

    pm.setAttr(CO_layerTexHubName + ".inputs[0]blendMode", 4)
    pm.setAttr(CO_layerTexHubName + ".inputs[1]blendMode", 4)
    pm.setAttr(CO_layerTexHubName + ".inputs[2]blendMode", 4)
    pm.setAttr(CO_layerTexHubName + ".inputs[3]blendMode", 0)

    pm.setAttr((cutOutRampOneName + ".interpolation"), 4)

    blurMult = blurAmount * .02

    pm.setAttr((cutOutRampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((cu_p2d1 + ".rotateUV"), 90)
    pm.setAttr((cutOutRampOneName + ".colorEntryList[0].position"),.25 + blurMult)
    pm.setAttr((cutOutRampOneName + ".colorEntryList[1].position"), .2)
    pm.setAttr((cutOutRampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")


    pm.setAttr((cutOutRampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((cu_p2d2 + ".rotateUV"), 270)
    pm.setAttr((cutOutRampTwoName + ".colorEntryList[0].position"),.25 + blurMult)
    pm.setAttr((cutOutRampTwoName + ".colorEntryList[1].position"), .2)
    pm.setAttr((cutOutRampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")


    pm.setAttr((cutOutRampThirdName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampThirdName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((cu_p2d3 + ".rotateUV"), 0)
    pm.setAttr((cutOutRampThirdName + ".colorEntryList[0].position"),.25 + blurMult)
    pm.setAttr((cutOutRampThirdName + ".colorEntryList[1].position"), .2)
    pm.setAttr((cutOutRampThirdName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampThirdName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")


    pm.setAttr((cutOutRampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((cu_p2d4 + ".rotateUV"), 270)
    pm.setAttr((cutOutRampFourName + ".colorEntryList[0].position"),.25 + blurMult)
    pm.setAttr((cutOutRampFourName + ".colorEntryList[1].position"), .2)
    pm.setAttr((cutOutRampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((cutOutRampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .05

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:
        print "box cutout"
        print "CO_layerTexHubName = ",CO_layerTexHubName
        print "layerTexHubName = ",layerTexHubName
        cmds.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(cutOutRampOneName + ".colorEntryList[0].position",(.25 + blurMult))
        pm.setAttr(cutOutRampTwoName + ".colorEntryList[0].position",(.25 + blurMult))
        pm.setAttr(cutOutRampThirdName + ".colorEntryList[0].position",(.25 + blurMult))
        pm.setAttr(cutOutRampFourName + ".colorEntryList[0].position",(.25 + blurMult))
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 > 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 > 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

def cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    box = 0

    cutOutRampOneName = " "
    cutOutRampTwoName = " "

    cutOutNoiseName = cmds.shadingNode("noise", name="noise", asTexture=True)
    cutOutRampOneName = cutOutNoiseName
    pm.setAttr((cutOutNoiseName + ".filterOffset"), blurAmount)

    if blurAmount > 0:
        blurMult = blurAmount
        print "noise blurMult = ",blurMult
        blurRatio = cmds.getAttr((cutOutNoiseName + ".ratio"))
        blurAmp = cmds.getAttr((cutOutNoiseName + ".amplitude"))
        print "noise blurRatio = ",blurRatio
        print "noise blurAmp = ",blurAmp
        print "blurMult = ",blurMult
        print "newAmp = ",(blurAmp/blurMult)
        print "newRatio = ",(blurRatio/blurMult)
        pm.setAttr((cutOutNoiseName + ".amplitude"), (blurAmp/blurMult))
        pm.setAttr((cutOutNoiseName + ".ratio"), (blurRatio/blurMult) )

        if blurMult == 1:

            pm.setAttr((cutOutNoiseName + ".amplitude"), .85)
            pm.setAttr((cutOutNoiseName + ".ratio"), .55)

        if blurMult < 3:
            pm.setAttr((cutOutNoiseName + ".falloff"), 0)
        if blurMult > 3 and blurMult < 7:
            pm.setAttr((cutOutNoiseName + ".falloff"), 1)
        if blurMult > 7:
            pm.setAttr((cutOutNoiseName + ".falloff"), 2)


    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutNoiseName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutNoiseName + ".uvFilterSize")


    #pm.setAttr((cutOutNoiseName + ".interpolation"), 4)

    #pm.setAttr((cutOutNoiseName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((p2d1 + ".rotateUV"), 0)
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[0].position"),0)
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[1].position"), 1)
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .01

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 > 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 > 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

def cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    box = 0

    cutOutRampOneName = " "
    cutOutRampTwoName = " "

    cutOutNoiseName = cmds.shadingNode("fractal", name="noise", asTexture=True)
    cutOutRampOneName = cutOutNoiseName
    #pm.setAttr((cutOutNoiseName + ".type"), 4)

    if blurAmount > 0:

        blurMult = blurAmount
        print "noise blurMult = ",blurMult
        blurRatio = cmds.getAttr((cutOutNoiseName + ".ratio"))
        blurAmp = cmds.getAttr((cutOutNoiseName + ".amplitude"))
        print "noise blurRatio = ",blurRatio
        print "noise blurAmp = ",blurAmp
        print "blurMult = ",blurMult
        print "newAmp = ",(blurAmp/blurMult)
        print "newRatio = ",(blurRatio/blurMult)
        pm.setAttr((cutOutNoiseName + ".amplitude"), (blurAmp/blurMult))
        pm.setAttr((cutOutNoiseName + ".ratio"), (blurRatio/blurMult) )

        if blurMult == 1:

            pm.setAttr((cutOutNoiseName + ".amplitude"), .85)
            pm.setAttr((cutOutNoiseName + ".ratio"), .55)


    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutNoiseName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutNoiseName + ".uvFilterSize")

    pm.setAttr((p2d1 + ".rotateUV"), 0)

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .01

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 > 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 > 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

def cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    box = 0

    #print "cutout = ",cutout

    cutOutRampOneName = " "
    cutOutRampTwoName = " "

    if cutout == 5:

        rU = 4
        rV = 4

    if cutout == 6:

        rU = 1
        rV = 4

    if cutout == 7:

        rU = 4
        rV = 1

    cutOutNoiseName = cmds.shadingNode("grid", name="grid", asTexture=True)
    cutOutRampOneName = cutOutNoiseName
    #pm.setAttr((cutOutNoiseName + ".type"), 4)

    blurMult = blurAmount
    blurMultColor = blurAmount * .2

    if blurAmount != 0:

        #print "blurAmount = ",blurAmount
        print "blurMult = ",blurMult
        print "blurMultColor = ",(blurAmount * .25)
        pm.setAttr((cutOutNoiseName + ".filterOffset"), (blurMult * .04))
        pm.setAttr((cutOutNoiseName + ".uWidth"), (blurMult * .07))
        pm.setAttr((cutOutNoiseName + ".vWidth"), (blurMult * .07))
        blurLineColor = cmds.getAttr((cutOutNoiseName + ".lineColor"))
        blurLineColor = blurLineColor[0]
        #print "blurLineColor1 = ",blurLineColor[0]
        print "new color = ",(blurMultColor/blurLineColor[0])
        blurFillColor = cmds.getAttr((cutOutNoiseName + ".fillerColor"))
        blurFillColor = blurFillColor[0]
        nfc = ((blurMultColor/10) + blurFillColor[0])
        print "blurFillColor1 = ",blurFillColor[0]
        print "nfc = ",nfc
        pm.setAttr((cutOutNoiseName + ".lineColor"), (blurLineColor[0]/blurMultColor), (blurLineColor[1]/blurMultColor), (blurLineColor[2]/blurMultColor),type="double3")
        pm.setAttr((cutOutNoiseName + ".fillerColor"), (nfc + blurFillColor[0]), (nfc + blurFillColor[0]), (nfc + blurFillColor[0]),type="double3")


    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutNoiseName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutNoiseName + ".uvFilterSize")

    pm.setAttr((cu_p2d1 + ".repeatU"), rU)
    pm.setAttr((cu_p2d1 + ".repeatV"), rV)

    pm.setAttr((p2d1 + ".rotateUV"), 0)
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[0].position"),0)

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .01

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 > 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 > 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

def cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    box = 0

    cutOutNoiseName = cmds.shadingNode("file", name="leaves", asTexture=True)
    cutOutRampOneName = cutOutNoiseName
    pm.setAttr((cutOutNoiseName + ".fileTextureName"), "U:\\cwinters\\thumbnails\\leavesLarge.jpg")
    #pm.setAttr((cutOutNoiseName + ".fileTextureName"), "//Users//alfredwinters//Desktop//thumbnails//leavesLarge.jpg")

    if blurAmount != 0:

        pm.setAttr((cutOutNoiseName + ".filterOffset"), blurAmount * .05)

    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)
    cmds.setAttr(cu_p2d1 + ".repeatV", 2)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".coverage", cutOutNoiseName + ".coverage")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutNoiseName + ".uvFilterSize")
    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutNoiseName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".vertexCameraOne", cutOutNoiseName + ".vertexCameraOne")
    cmds.connectAttr(cu_p2d1 + ".vertexUvThree", cutOutNoiseName + ".vertexUvThree")
    cmds.connectAttr(cu_p2d1 + ".vertexUvTwo", cutOutNoiseName + ".vertexUvTwo")
    cmds.connectAttr(cu_p2d1 + ".vertexUvOne", cutOutNoiseName + ".vertexUvOne")
    cmds.connectAttr(cu_p2d1 + ".noiseUV", cutOutNoiseName + ".noiseUV")
    cmds.connectAttr(cu_p2d1 + ".rotateUV", cutOutNoiseName + ".rotateUV")
    cmds.connectAttr(cu_p2d1 + ".offset", cutOutNoiseName + ".offset")
    cmds.connectAttr(cu_p2d1 + ".repeatUV", cutOutNoiseName + ".repeatUV")
    cmds.connectAttr(cu_p2d1 + ".wrapV", cutOutNoiseName + ".wrapV")
    cmds.connectAttr(cu_p2d1 + ".wrapU", cutOutNoiseName + ".wrapU")
    cmds.connectAttr(cu_p2d1 + ".stagger", cutOutNoiseName + ".stagger")
    cmds.connectAttr(cu_p2d1 + ".mirrorU", cutOutNoiseName + ".mirrorU")
    cmds.connectAttr(cu_p2d1 + ".mirrorV", cutOutNoiseName + ".mirrorV")
    cmds.connectAttr(cu_p2d1 + ".rotateFrame", cutOutNoiseName + ".rotateFrame")
    cmds.connectAttr(cu_p2d1 + ".translateFrame", cutOutNoiseName + ".translateFrame")

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .01

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 > 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 > 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

def cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    box = 0

    cutOutRampOneName = " "
    cutOutRampTwoName = " "

    if cutout == 9:
        rU = 3
        rV = 3

    if cutout == 10:
        rU = 1
        rV = 3

    if cutout == 11:
        rU = 3
        rV = 1

    cutOutNoiseName = cmds.shadingNode("bulge", name="bulge", asTexture=True)
    cutOutRampOneName = cutOutNoiseName
    #pm.setAttr((cutOutNoiseName + ".type"), 4)

    if blurAmount != 0:

        #print "blurAmount = ",blurAmount
        blurMult = (blurAmount * .05)
        print "blurMult = ",blurMult

        pm.setAttr((cutOutNoiseName + ".filterOffset"), blurMult)
        pm.setAttr((cutOutNoiseName + ".uWidth"), blurMult)
        pm.setAttr((cutOutNoiseName + ".vWidth"), blurMult)

        newColorGain = 1

        if blurAmount > 0 and blurAmount < 2:
            newColorGain = .9

        if blurAmount > 2 and blurAmount < 4:
            newColorGain = .7

        if blurAmount > 4 and blurAmount < 6:
            newColorGain = .6

        if blurAmount > 6 and blurAmount < 8:
            newColorGain = .5

        if blurAmount > 8 and blurAmount < 10:
            newColorGain = .3

        pm.setAttr((cutOutNoiseName + ".colorGain"), newColorGain, newColorGain, newColorGain,type = "double3")


    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutNoiseName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutNoiseName + ".uvFilterSize")

    pm.setAttr((cu_p2d1 + ".repeatU"),rU)
    pm.setAttr((cu_p2d1 + ".repeatV"),rV)

    pm.setAttr((p2d1 + ".rotateUV"), 0)
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[0].position"),0)

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .01

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 > 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 > 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

def cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount,*args):

    box = 0

    cutOutRampOneName = " "
    cutOutRampTwoName = " "

    if cutout == 12:

        rU = 3
        rV = 3

    if cutout == 13:

        rU = 1
        rV = 3

    if cutout == 14:

        rU = 3
        rV = 1

    cutOutNoiseName = cmds.shadingNode("checker", name="checker", asTexture=True)
    cutOutRampOneName = cutOutNoiseName
    #pm.setAttr((cutOutNoiseName + ".type"), 4)

    if blurAmount != 0:

        #print "blurAmount = ",blurAmount
        blurMult = (blurAmount * .07)
        print "blurMult = ",blurMult

        pm.setAttr((cutOutNoiseName + ".filterOffset"), blurMult)
        #pm.setAttr((cutOutNoiseName + ".uWidth"), blurMult)
        #pm.setAttr((cutOutNoiseName + ".vWidth"), blurMult)

        newColorGain = 1

        if blurAmount > 0 and blurAmount < 2:
            newColorGain = .9

        if blurAmount > 2 and blurAmount < 4:
            newColorGain = .7

        if blurAmount > 4 and blurAmount < 6:
            newColorGain = .6

        if blurAmount > 6 and blurAmount < 8:
            newColorGain = .5

        if blurAmount > 8 and blurAmount < 10:
            newColorGain = .3

        pm.setAttr((cutOutNoiseName + ".colorGain"), newColorGain, newColorGain, newColorGain,type = "double3")

    cu_p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(cu_p2d1 + ".repeatU", 1)

    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(cu_p2d1 + ".outUV", cutOutNoiseName + ".uvCoord")
    cmds.connectAttr(cu_p2d1 + ".outUvFilterSize", cutOutNoiseName + ".uvFilterSize")

    pm.setAttr((cu_p2d1 + ".repeatU"), rU)
    pm.setAttr((cu_p2d1 + ".repeatV"), rV)

    pm.setAttr((cu_p2d1 + ".rotateUV"), 0)
    #pm.setAttr((cutOutNoiseName + ".colorEntryList[0].position"),0)

    print "rampOneName = ",rampOneName
    print "rampTwoName = ",rampTwoName
    print "layerTexHubName = ",layerTexHubName
    print "rampThreeName = ",rampThreeName
    print "rampFourName = ",rampFourName

    ln1 = len(rampOneName)
    ln2 = len(rampTwoName)
    ln3 = len(rampThreeName)
    ln4 = len(rampFourName)

    print "ln1 = ",ln1
    print "ln2 = ",ln2
    print "ln3 = ",ln3
    print "ln4 = ",ln4
    print "box = ",box

    if blurAmount != 0:
        blurMult = blurAmount * .01

    if ln1 == 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 > 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 > 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[4].color"), force=True)
        #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[4]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 > 1 and ln4 == 0 and box == 0:
        print "ln1 > 0 ln2 > 0 ln3 > 0 and ln4 == 0 box = 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        cmds.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)


    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 0 trig"
        cmds.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        cmds.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        cmds.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 0:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 0 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((cutOutRampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 == 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 = 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 0)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    if ln1 > 0 and ln2 > 0 and ln3 > 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 > 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

    if ln1 > 0 and ln2 > 0 and ln3 == 0 and ln4 == 0 and box == 1:

        print "ln1 > 0 ln2 > 0 ln3 == 0 ln4 == 0 box == 1 trig"
        print "rampOneName = ",rampOneName
        print "cutOutRampOneName = ",cutOutRampOneName
        print "layerTexHubName = ",layerTexHubName

        pm.connectAttr((CO_layerTexHubName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
        pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
        pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
        pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)
        #pm.setAttr(layerTexHubName + ".inputs[3]blendMode", 0)

def rampGenWin():

    name = "Ramp_Generator"

    intp = 4
    cutout = 0

    windowSize = (30, 75)

    if (cmds.window(name, exists=True)):
        cmds.deleteUI(name)

    window = cmds.window(name, title=name, width=30, height=75,resizeToFitChildren = True,sizeable = False )

    def intpVal_buildOneRampHorNode(intp,cutout,lightGenField):

        def sub_intpVal_buildOneRampHorNode(*args):

            cutout = 0
            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildOneRampHorNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildOneRampHorNode

    def intpVal_buildOneRampVerNode(intp,cutout,lightGenField):

        def sub_intpVal_buildOneRampVerNode(*args):

            cutout = 0

            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue


            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildOneRampVerNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildOneRampVerNode

    def intpVal_buildOneRampDiagLNode(intp,cutout,lightGenField):

        def sub_intpVal_buildOneRampDiagLNode(*args):

            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildOneRampDiagLNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildOneRampDiagLNode

    def intpVal_buildOneRampDiagRNode(intp,cutout,lightGenField):

        def sub_intpVal_buildOneRampDiagRNode(*args):

            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue
            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildOneRampDiagRNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildOneRampDiagRNode

#--

    def intpVal_buildTwoRampHorNode(intp,cutout,lightGenField):

        def sub_intpVal_buildTwoRampHorNode(*args):

            cutout = 0
            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            ##print "blurAmount = ",blurAmount

            buildTwoRampHorNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildTwoRampHorNode

    def intpVal_buildTwoRampVerNode(intp,cutout,lightGenField):

        def sub_intpVal_buildTwoRampVerNode(*args):

            cutout = 0

            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue


            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            ##print "blurAmount = ",blurAmount

            buildTwoRampVerNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildTwoRampVerNode

    def intpVal_buildTwoRampDiagLNode(intp,cutout,lightGenField):

        def sub_intpVal_buildTwoRampDiagLNode(*args):

            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildTwoRampDiagLNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildTwoRampDiagLNode

    def intpVal_buildTwoRampDiagRNode(intp,cutout,lightGenField):

        def sub_intpVal_buildTwoRampDiagRNode(*args):

            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue
            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildTwoRampDiagRNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildTwoRampDiagRNode

    def intpVal_buildFourRampNode(intp,cutout,lightGenField):

        def sub_intpVal_buildFourRampNode(*args):

            cutout = 0

            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildFourRampNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildFourRampNode

    def intpVal_buildFourRampHardTBnode(intp,cutout,lightGenField):

        def sub_intpVal_buildFourRampHardTBnode(*args):

            cutout = 0

            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildFourRampHardTBnode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildFourRampHardTBnode

    def intpVal_buildFourRampHardSnode(intp,cutout,lightGenField):

        def sub_intpVal_buildFourRampHardSnode(*args):

            cutout = 0

            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildFourRampHardSnode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildFourRampHardSnode

    def intpVal_buildFourRampDoublesNode(intp,cutout,lightGenField):

        def sub_intpVal_buildFourRampDoublesNode(*args):

            cutout = 0

            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildFourRampDoublesNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildFourRampDoublesNode

    def intpVal_buildDiscRampNode(intp,cutout,lightGenField):

        def sub_intpVal_buildDiscRampNode(*args):

            cutout = 0
            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildDiscRampNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildDiscRampNode

    def intpVal_buildDiscTightRampNode(intp,cutout,lightGenField):

        def sub_intpVal_buildDiscTightRampNode(*args):

            cutout = 0
            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildDiscTightRampNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildDiscTightRampNode

    def intpVal_buildDiscHORBDSrampNode(intp,cutout,lightGenField):

        def sub_intpVal_buildDiscHORBDSrampNode(*args):

            cutout = 0
            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildDiscHORBDSrampNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildDiscHORBDSrampNode

    def intpVal_buildDiscVERBDSrampNode(intp,cutout,lightGenField):

        def sub_intpVal_buildDiscVERBDSrampNode(*args):

            cutout = 0
            intp = 4

            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildDiscVERBDSrampNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildDiscVERBDSrampNode

    def intpVal_buildSoftBOXrampNode(intp,cutout,lightGenField):

        def sub_intpVal_buildSoftBOXrampNode(*args):

            cutout = 0
            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildSoftBOXrampNode(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildSoftBOXrampNode

    def intpVal_buildSoftBOXrampNodeBarnHor(intp,cutout,lightGenField):

        def sub_intpVal_buildSoftBOXrampNodeHor(*args):

            cutout = 0
            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildSoftBOXrampNodeHor(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildSoftBOXrampNodeHor

    def intpVal_buildSoftBOXrampNodeBarnVert(intp,cutout,lightGenField):

        def sub_intpVal_buildSoftBOXrampNodeVert(*args):

            cutout = 0
            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildSoftBOXrampNodeVert(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildSoftBOXrampNodeVert

    def intpVal_buildSoftBOXrampNodeBarnDiag(intp,cutout,lightGenField):

        def sub_intpVal_buildSoftBOXrampNodeDiag(*args):

            cutout = 0
            intp = 4
            intpVal = cmds.optionMenu(oMenuName, v=True, query=True)
            cutoutVal = cmds.optionMenu(cutOutMenuName, v=True, query=True)
            lightGenFieldValue = cmds.textField(lightGenField,text = True,query = True)

            print "intpVal = ", intpVal
            print "cutoutVal = ", cutoutVal
            #print "lightGenFieldValue = ",lightGenFieldValue

            if intpVal == "none":
                intp = 0

            if intpVal == "linear":
                intp = 1

            if intpVal == "exp up":
                intp = 2

            if intpVal == "exp down":
                intp = 3

            if intpVal == "smooth":
                intp = 4

            if intpVal == "bump":
                intp = 5

            if intpVal == "spike":
                intp = 6

            #==cutout

            if cutoutVal == "none":

                cutout = 0

            if cutoutVal == "circle":

                cutout = 1

            if cutoutVal == "box":

                cutout = 2

            if cutoutVal == "noise_1":

                cutout = 3

            if cutoutVal == "noise_2":

                cutout = 4

            if cutoutVal == "grid_1":

                cutout = 5

            if cutoutVal == "grid_2":

                cutout = 6

            if cutoutVal == "grid_3":

                cutout = 7

            if cutoutVal == "leaves":

                cutout = 8

            if cutoutVal == "bulge_1":

                cutout = 9

            if cutoutVal == "bulge_2":

                cutout = 10

            if cutoutVal == "bulge_3":

                cutout = 11

            if cutoutVal == "checker_1":

                cutout = 12

            if cutoutVal == "checker_2":

                cutout = 13

            if cutoutVal == "checker_3":

                cutout = 14

            blurAmount = cmds.floatField(blurField,query = True, value = True)

            #print "blurAmount = ",blurAmount

            buildSoftBOXrampNodeDiag(intp,cutout,blurAmount,lightGenFieldValue)

        return sub_intpVal_buildSoftBOXrampNodeDiag

    cmds.columnLayout("mainColumn", adjustableColumn=True)

    cmds.rowLayout("nameRowLayout-1", numberOfColumns = 4, parent="mainColumn")

    cmds.text("light name")

    lightGenField = pm.textField(text = "Enter Light Name", width = 100)
    #print "lightGenField = ",lightGenField

    cmds.rowLayout("nameRowLayout00", numberOfColumns = 4, parent="mainColumn")

    #U:\\cwinters\\thumbnails\\oneRampVerThumb
    #//Users//alfredwinters//Desktop//thumbnails//oneRampVerThumb

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\oneRampVerThumb", label = "two ramps", c = intpVal_buildOneRampVerNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\oneRampHorThumb", label = "two ramps", c = intpVal_buildOneRampHorNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\oneRampDiagLThumb", label = "two ramps", c = intpVal_buildOneRampDiagLNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\oneRampDiagRThumb", label = "two ramps",c = intpVal_buildOneRampDiagRNode(intp,cutout,lightGenField))

    cmds.rowLayout("nameRowLayout01", numberOfColumns = 4, parent="mainColumn")

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\twoRampHorThumb", label = "two ramps", c = intpVal_buildTwoRampHorNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\twoRampVerThumb", label = "two ramps", c = intpVal_buildTwoRampVerNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\twoRampDiagLThumb", label = "two ramps", c = intpVal_buildTwoRampDiagLNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\twoRampDiagRThumb", label = "two ramps",c = intpVal_buildTwoRampDiagRNode(intp,cutout,lightGenField))

    cmds.rowLayout("nameRowLayout02", numberOfColumns = 4, parent="mainColumn")

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\fourRampHardTBthumb", label = "four ramps",c = intpVal_buildFourRampHardTBnode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\fourRampHardSidesThumb", label = "four ramps",c = intpVal_buildFourRampHardSnode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\fourRampThumb", label = "four ramps",c = intpVal_buildFourRampNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\fourRampDBrampALLthumb", label = "four ramps",c = intpVal_buildFourRampDoublesNode(intp,cutout,lightGenField))

    cmds.rowLayout("nameRowLayout03", numberOfColumns = 4, parent="mainColumn")

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\discHORBDRampThumb", label = "disc ramps",c = intpVal_buildDiscHORBDSrampNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\discVERDRampThumb", label = "disc ramps",c = intpVal_buildDiscVERBDSrampNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\discRampTightThumb", label = "disc ramps",c = intpVal_buildDiscTightRampNode(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\discRampThumb", label = "disc ramps",c = intpVal_buildDiscRampNode(intp,cutout,lightGenField))

    cmds.rowLayout("nameRowLayout03.5", numberOfColumns = 4, parent = "mainColumn")

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\softBoxThumbBNDhor", label = "jesse ramps",c = intpVal_buildSoftBOXrampNodeBarnHor(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\softBoxThumbBNDvert", label = "jesse ramps",c = intpVal_buildSoftBOXrampNodeBarnVert(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\softBoxThumbBNDdiag", label = "jesse ramps",c = intpVal_buildSoftBOXrampNodeBarnDiag(intp,cutout,lightGenField))

    cmds.iconTextButton(style='iconOnly', image1="U:\\cwinters\\thumbnails\\softBoxThumb", label = "jesse ramps",c = intpVal_buildSoftBOXrampNode(intp,cutout,lightGenField))


    cmds.rowLayout("nameRowLayout04", numberOfColumns = 4, parent = "mainColumn")

    oMenuName = cmds.optionMenu(label = "interppolation")
    cmds.menuItem(label = "none")
    cmds.menuItem(label = "linear")
    cmds.menuItem(label = "exp up")
    cmds.menuItem(label = "exp down")
    cmds.menuItem(label = "smooth")
    cmds.menuItem(label = "bump")
    cmds.menuItem(label = "spike")
    cmds.optionMenu(oMenuName, edit = True, v = "smooth")

    cutOutMenuName = cmds.optionMenu(label = "cutout")
    cmds.menuItem(label = "none")
    cmds.menuItem(label = "circle")
    cmds.menuItem(label = "box")
    cmds.menuItem(label = "noise_1")
    cmds.menuItem(label = "noise_2")
    cmds.menuItem(label = "grid_1")
    cmds.menuItem(label = "grid_2")
    cmds.menuItem(label = "grid_3")
    cmds.menuItem(label = "leaves")
    cmds.menuItem(label = "bulge_1")
    cmds.menuItem(label = "bulge_2")
    cmds.menuItem(label = "bulge_3")
    cmds.menuItem(label = "checker_1")
    cmds.menuItem(label = "checker_2")
    cmds.menuItem(label = "checker_3")
    cmds.optionMenu(cutOutMenuName, edit = True, v = "none")

    cmds.rowLayout("nameRowLayout05", numberOfColumns = 5, parent = "mainColumn")

    cmds.text(label = "blur ")

    blurField = cmds.floatField( minValue = -10, maxValue = 10, value = 0 )

    cmds.rowLayout("nameRowLayout06", numberOfColumns = 5, parent = "mainColumn")

    cmds.showWindow()

# --- 0

def buildOneRampHorNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    #print "cutout = ",cutout
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 0)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""


    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = ""

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)

    blurMult = blurAmount * .0095
    blurMultColor = blurAmount * .012

    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 90)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .5)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 90)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .9 + blurMult)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")

    if blurAmount != 0:

        blurMult = blurAmount * .01

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), blurMult, blurMult, blurMult, type="double3")


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)



def buildOneRampVerNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    #print "cutout = ",cutout
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)


    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 0)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = ""

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)

    blurMult = blurAmount * .0095
    blurMultColor = blurAmount * .012

    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .5)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .9 + blurMult)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")

    if blurAmount != 0:

        blurMult = blurAmount * .01

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), blurMult, blurMult, blurMult, type="double3")


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)


def buildOneRampDiagLNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    #print "cutout = ",cutout
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 0)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = ""

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    pm.setAttr((rampOneName + ".type"), 2)

    blurMult = blurAmount * .0095
    blurMultColor = blurAmount * .012

    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 90)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .5 + blurMult)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 90)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .9 + blurMult)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")

    if blurAmount != 0:

        blurMult = blurAmount * .01

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), blurMult, blurMult, blurMult, type="double3")


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)


    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)



def buildOneRampDiagRNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    #print "cutout = ",cutout
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 0)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = ""

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    pm.setAttr((rampOneName + ".type"), 2)

    blurMult = blurAmount * .0095
    blurMultColor = blurAmount * .012

    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 180)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"),.5)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 180)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .9 + blurMult)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultColor, 1 - blurMultColor, 1 - blurMultColor, type="double3")

    if blurAmount != 0:

        blurMult = blurAmount * .01

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), blurMult, blurMult, blurMult, type="double3")


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)


# --- 1


def buildTwoRampHorNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    ##print "cutout = ",cutout
    #print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    pm.setAttr((rampTwoName + ".interpolation"), intp)


    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")


        if blurAmount != 0:

            blurMult = blurAmount * .04

            pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampOneName + ".colorEntryList[0].position"), .25 + blurMult)

            pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25 + blurMult)


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)

# --- 2

def buildTwoRampVerNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)

    pm.setAttr((rampOneName + ".type"), 1)
    pm.setAttr((rampTwoName + ".type"), 1)
    pm.setAttr((rampTwoName + ".interpolation"), intp)
    pm.setAttr((rampOneName + ".interpolation"), intp)

    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")


        if blurAmount != 0:

            blurMult = blurAmount * .04

            pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampOneName + ".colorEntryList[0].position"), .25 + blurMult)

            pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25 + blurMult)


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)


# --- 3

def buildTwoRampDiagLNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)

    pm.setAttr((rampOneName + ".type"), 2)
    pm.setAttr((rampTwoName + ".type"), 2)
    pm.setAttr((rampTwoName + ".interpolation"), intp)
    pm.setAttr((rampOneName + ".interpolation"), intp)


    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")


        if blurAmount != 0:

            blurMult = blurAmount * .04

            pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampOneName + ".colorEntryList[0].position"), .25 + blurMult)

            pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25 + blurMult)


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)


        # --- 4


def buildTwoRampDiagRNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="twoRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", -1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", -1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)

    pm.setAttr((rampOneName + ".type"), 2)
    pm.setAttr((rampTwoName + ".type"), 2)
    pm.setAttr((rampTwoName + ".interpolation"), intp)
    pm.setAttr((rampOneName + ".interpolation"), intp)

    if intp == 0:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"),.25)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25)
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")


        if blurAmount != 0:

            blurMult = blurAmount * .04

            pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampOneName + ".colorEntryList[0].position"), .25 + blurMult)

            pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0 + blurMult, 0 + blurMult, 0 + blurMult, type="double3")
            pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .25 + blurMult)


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)

        # --- 5


def buildFourRampNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = cmds.shadingNode("ramp", name="rampeRIGHT", asTexture=True)
    rampFourName = cmds.shadingNode("ramp", name="rampeLEFT", asTexture=True)

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d4 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    cmds.connectAttr(p2d3 + ".outUV", rampThreeName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    pm.setAttr((rampTwoName + ".interpolation"), intp)
    pm.setAttr((rampThreeName + ".interpolation"), intp)
    pm.setAttr((rampFourName + ".interpolation"), intp)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)

    if intp == 0:

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

    else:

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")



        if blurAmount != 0:

            blurMult = blurAmount * .1

            print "new position = ",(.25 + blurMult)

            if blurAmount > 0 and blurAmount <= 1:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .725)

            if blurAmount > 1 and blurAmount <= 2:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .7)

            if blurAmount > 2 and blurAmount <= 3:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.94,.94,94, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .675)

            if blurAmount > 3 and blurAmount <= 4:

                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .65)

            if blurAmount > 4 and blurAmount <= 5:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .625)

            if blurAmount > 5 and blurAmount <= 6:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .6)

            if blurAmount > 6 and blurAmount <= 7:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .575)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .757)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .575)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .575)

            if blurAmount > 7 and blurAmount <= 8:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .55)

            if blurAmount > 8 and blurAmount <= 9:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .525)

            if blurAmount > 9 and blurAmount <= 10:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .5)

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)



# --- 6

def buildFourRampHardSnode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = cmds.shadingNode("ramp", name="rampeRIGHT", asTexture=True)
    rampFourName = cmds.shadingNode("ramp", name="rampeLEFT", asTexture=True)

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d4 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    cmds.connectAttr(p2d3 + ".outUV", rampThreeName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    pm.setAttr((rampTwoName + ".interpolation"), intp)
    pm.setAttr((rampThreeName + ".interpolation"), 0)
    pm.setAttr((rampFourName + ".interpolation"), 0)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)

    if intp == 0:

        pm.setAttr((rampThreeName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), .9)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), .9)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

    else:

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .8)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), .8)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")


        if blurAmount != 0:

            blurMult = blurAmount * .1

            print "new position = ",(.25 + blurMult)

            if blurAmount > 0 and blurAmount <= 1:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .725)

            if blurAmount > 1 and blurAmount <= 2:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .7)

            if blurAmount > 2 and blurAmount <= 3:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.94,.94,94, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .675)

            if blurAmount > 3 and blurAmount <= 4:

                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .65)

            if blurAmount > 4 and blurAmount <= 5:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .625)

            if blurAmount > 5 and blurAmount <= 6:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .6)

            if blurAmount > 6 and blurAmount <= 7:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .575)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .757)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .575)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .575)

            if blurAmount > 7 and blurAmount <= 8:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .55)

            if blurAmount > 8 and blurAmount <= 9:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .525)

            if blurAmount > 9 and blurAmount <= 10:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .5)

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)



# --- 7

def buildFourRampHardTBnode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = cmds.shadingNode("ramp", name="rampeRIGHT", asTexture=True)
    rampFourName = cmds.shadingNode("ramp", name="rampeLEFT", asTexture=True)

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d4 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    cmds.connectAttr(p2d3 + ".outUV", rampThreeName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), 0)
    pm.setAttr((rampTwoName + ".interpolation"), 0)
    pm.setAttr((rampThreeName + ".interpolation"), intp)
    pm.setAttr((rampFourName + ".interpolation"), intp)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)

    if intp == 0:

        pm.setAttr((rampThreeName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), .8)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), .8)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .9)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), .9)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), 0)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

    else:

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .6)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .6)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

        if blurAmount != 0:

            blurMult = blurAmount * .1

            print "new position = ",(.25 + blurMult)

            if blurAmount > 0 and blurAmount <= 1:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .725)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .725)

            if blurAmount > 1 and blurAmount <= 2:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .7)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .7)

            if blurAmount > 2 and blurAmount <= 3:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.94,.94,94, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .675)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .675)

            if blurAmount > 3 and blurAmount <= 4:

                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .65)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .65)

            if blurAmount > 4 and blurAmount <= 5:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.90,.90,.90, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .625)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .625)

            if blurAmount > 5 and blurAmount <= 6:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.88,.88,.88, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .6)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .6)

            if blurAmount > 6 and blurAmount <= 7:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.86,.86,.86, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .575)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .757)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .575)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .575)

            if blurAmount > 7 and blurAmount <= 8:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.84,.84,.84, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .55)

            if blurAmount > 8 and blurAmount <= 9:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.82,.82,.82, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .525)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .525)

            if blurAmount > 9 and blurAmount <= 10:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.8,.8,.8, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .5)

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)



def buildFourRampDoublesNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)


    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBOTTOM", asTexture=True)
    rampThreeName = cmds.shadingNode("ramp", name="rampeRIGHT", asTexture=True)
    rampFourName = cmds.shadingNode("ramp", name="rampeLEFT", asTexture=True)

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d4 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)

    placs2D = (p2d1, p2d2)
    ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    cmds.connectAttr(p2d3 + ".outUV", rampThreeName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[3].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    pm.setAttr((rampTwoName + ".interpolation"), intp)
    pm.setAttr((rampThreeName + ".interpolation"), intp)
    pm.setAttr((rampFourName + ".interpolation"), intp)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 6)

    if intp == 0:

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), .65)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .35)
        pm.setAttr((rampOneName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), .65)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .35)
        pm.setAttr((rampTwoName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 180)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .65)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .35)
        pm.setAttr((rampThreeName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), .64)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), .35)
        pm.setAttr((rampFourName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")

    else:

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[3].color"), 1, 1, 1, type="double3" )
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .4)
        pm.setAttr((rampOneName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[3].position"), .6)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[3].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[3].color"), 1, 1, 1, type="double3" )
        pm.setAttr((p2d2 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .4)
        pm.setAttr((rampTwoName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .6)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[3].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampThreeName + ".type"), 1)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[3].color"), 1, 1, 1, type="double3" )
        pm.setAttr((p2d3 + ".rotateUV"), 180)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .4)
        pm.setAttr((rampThreeName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .6)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[3].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampFourName + ".type"), 1)

        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[3].color"), 1, 1, 1, type="double3" )
        pm.setAttr((p2d4 + ".rotateUV"), 180)
        pm.setAttr((rampFourName + ".colorEntryList[0].position"), 1)
        pm.setAttr((rampFourName + ".colorEntryList[1].position"), .4)
        pm.setAttr((rampFourName + ".colorEntryList[2].position"), 0)
        pm.setAttr((rampFourName + ".colorEntryList[3].position"), .6)
        pm.setAttr((rampFourName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[2].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampFourName + ".colorEntryList[3].color"), 1, 1, 1, type="double3")

        if blurAmount != 0:

            blurMult = blurAmount * .1

            print "new position = ",(.25 + blurMult)

            if blurAmount > 0 and blurAmount <= 1:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.98,.98,.98, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .59)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .41)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .59)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .41)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .59)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .41)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .59)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .41)

            if blurAmount > 1 and blurAmount <= 2:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.97,.97,.97, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .58)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .42)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .58)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .42)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .58)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .42)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .58)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .42)

            if blurAmount > 2 and blurAmount <= 3:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.96,.96,.96, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .57)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .43)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .57)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .43)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .57)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .43)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .57)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .43)

            if blurAmount > 3 and blurAmount <= 4:

                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.95,.95,.95, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .56)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .44)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .56)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .44)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .56)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .44)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .56)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .44)

            if blurAmount > 4 and blurAmount <= 5:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .45)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .45)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .45)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .55)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .45)

            if blurAmount > 5 and blurAmount <= 6:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.94,.94,.94, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .54)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .45)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .54)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .45)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .54)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .45)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .54)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .45)

            if blurAmount > 6 and blurAmount <= 7:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.93,.93,.93, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .53)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .46)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .53)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .46)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .53)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .46)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .53)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .46)

            if blurAmount > 7 and blurAmount <= 8:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.92,.92,.92, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .52)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .47)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .52)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .47)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .52)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .47)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .52)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .47)

            if blurAmount > 8 and blurAmount <= 9:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.91,.91,.91, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .51)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .48)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .51)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .48)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .51)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .48)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .51)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .48)
            if blurAmount > 9 and blurAmount <= 10:
                pm.setAttr((rampOneName + ".colorEntryList[1].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[3].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[1].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampTwoName + ".colorEntryList[3].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[1].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampThreeName + ".colorEntryList[3].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[1].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampFourName + ".colorEntryList[3].color"),.9,.9,.9, type="double3")
                pm.setAttr((rampOneName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampOneName + ".colorEntryList[3].position"), .49)
                pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampTwoName + ".colorEntryList[3].position"), .49)
                pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampThreeName + ".colorEntryList[3].position"), .49)
                pm.setAttr((rampFourName + ".colorEntryList[1].position"), .5)
                pm.setAttr((rampFourName + ".colorEntryList[3].position"), .49)


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)


# --- 9

def buildDiscRampNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    #p2d2 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d2 + ".repeatU", 1)
    #p2d3 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d1 + ".repeatU", 1)
    #p2d4 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d2 + ".repeatU", 1)

    #placs2D = (p2d1, p2d2)
    #ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    #cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    #cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    #cmds.connectAttr(p2d3 + ".outUV", rampThreeName + ".uvCoord")
    #cmds.connectAttr(p2d3 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    #cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    #cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    #pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    #pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    #pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    #pm.setAttr((rampTwoName + ".interpolation"), intp)
    #pm.setAttr((rampThreeName + ".interpolation"), intp)
    #pm.setAttr((rampFourName + ".interpolation"), intp)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 0)

    blurMulty = blurAmount * .0125
    blurMultyColor = blurAmount * .07

    if intp == 0:

        pm.setAttr((rampOneName + ".type"), 4)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .4)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

    else:

        pm.setAttr((rampOneName + ".type"), 4)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultyColor, 1 - blurMultyColor, 1 - blurMultyColor, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .7 + blurMulty)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultyColor, 1 - blurMultyColor, 1 - blurMultyColor, type="double3")


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)

        # --- 8

def buildDiscTightRampNode(intp,cutout,blurAmount,lightGenFieldValue):

    layerTexHubName = ""
    rampOneName = ""
    rampTwoName = ""
    p2d1 = ""
    p2d2 = ""


    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTOP", asTexture=True)
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    #p2d2 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d2 + ".repeatU", 1)
    #p2d3 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d1 + ".repeatU", 1)
    #p2d4 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d2 + ".repeatU", 1)

    #placs2D = (p2d1, p2d2)
    #ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    #cmds.connectAttr(p2d2 + ".outUV", rampTwoName + ".uvCoord")
    #cmds.connectAttr(p2d2 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    #cmds.connectAttr(p2d3 + ".outUV", rampThreeName + ".uvCoord")
    #cmds.connectAttr(p2d3 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    #cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    #cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    #pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    #pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    #pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampOneName + ".interpolation"), intp)
    #pm.setAttr((rampTwoName + ".interpolation"), intp)
    #pm.setAttr((rampThreeName + ".interpolation"), intp)
    #pm.setAttr((rampFourName + ".interpolation"), intp)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 0)

    blurMulty = blurAmount * .03
    blurMultyColor = blurAmount * .02

    if intp == 0:

        pm.setAttr((rampOneName + ".type"), 4)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), .3)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .4)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")


    else:

        pm.setAttr((rampOneName + ".type"), 4)

        pm.setAttr((rampOneName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), .5 - blurMulty)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .6 + blurMulty)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1 - blurMultyColor, 1 - blurMultyColor, 1 - blurMultyColor, type="double3")

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)


def buildDiscHORBDSrampNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)


    layerTexHubName = ""
    rampOneName = ""
    rampTwoName = ""
    p2d1 = ""
    p2d2 = ""

    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampThreeName = cmds.shadingNode("ramp", name="rampeCircle", asTexture=True)
    rampOneName = cmds.shadingNode("ramp", name="rampeTop", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBottom", asTexture=True)
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    #p2d4 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d2 + ".repeatU", 1)

    #placs2D = (p2d1, p2d2)
    #ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampThreeName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d3 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    #cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    #cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    #pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampThreeName + ".interpolation"), intp)
    pm.setAttr((rampOneName + ".interpolation"), 0)
    pm.setAttr((rampTwoName + ".interpolation"), 0)
    #pm.setAttr((rampFourName + ".interpolation"), intp)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)

    blurMulty = blurAmount * .03
    blurMultyColor = blurAmount * .02

    if intp == 0:

        pm.setAttr((rampThreeName + ".type"), 4)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .2)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .7)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")


    else:

        pm.setAttr((rampThreeName + ".type"), 4)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .3 - blurMulty)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .5 + blurMulty)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1 - blurMultyColor, 1 - blurMultyColor, 1 - blurMultyColor, type="double3")

        pm.setAttr((rampOneName + ".type"), 0)

        pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".type"), 0)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)


#---9

def buildDiscVERBDSrampNode(intp,cutout,blurAmount,lightGenFieldValue):


    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)


    layerTexHubName = ""
    rampOneName = ""
    rampTwoName = ""
    p2d1 = ""
    p2d2 = ""

    layerTexHubName = cmds.shadingNode("layeredTexture", name="fourRampNode", asTexture=True)

    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampThreeName = cmds.shadingNode("ramp", name="rampeCircle", asTexture=True)
    rampOneName = cmds.shadingNode("ramp", name="rampeTop", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBottom", asTexture=True)
    rampFourName = ""

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    #p2d4 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d2 + ".repeatU", 1)

    #placs2D = (p2d1, p2d2)
    #ramps = (rampOneName, rampTwoName)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    cmds.connectAttr(p2d1 + ".outUV", rampThreeName + ".uvCoord")
    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")

    cmds.connectAttr(p2d2 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampOneName + ".uvFilterSize")

    cmds.connectAttr(p2d3 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")

    #cmds.connectAttr(p2d4 + ".outUV", rampFourName + ".uvCoord")
    #cmds.connectAttr(p2d4 + ".outUvFilterSize", rampFourName + ".uvFilterSize")

    pm.connectAttr((rampThreeName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    #pm.connectAttr((rampFourName + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    pm.setAttr((rampThreeName + ".interpolation"), intp)
    pm.setAttr((rampOneName + ".interpolation"), 0)
    pm.setAttr((rampTwoName + ".interpolation"), 0)
    #pm.setAttr((rampFourName + ".interpolation"), intp)

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)

    blurMulty = blurAmount * .03
    blurMultyColor = blurAmount * .02

    if intp == 0:

        pm.setAttr((rampThreeName + ".type"), 4)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .3)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .5)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampOneName + ".type"), 1)

        pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".type"), 1)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")


    else:

        pm.setAttr((rampThreeName + ".type"), 4)

        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d1 + ".rotateUV"), 0)
        pm.setAttr((rampThreeName + ".colorEntryList[0].position"), .5 - blurMulty)
        pm.setAttr((rampThreeName + ".colorEntryList[1].position"), .6 + blurMulty)
        pm.setAttr((rampThreeName + ".colorEntryList[1].color"), (0),(0), (0), type="double3")
        pm.setAttr((rampThreeName + ".colorEntryList[0].color"), 1 - blurMultyColor, 1 - blurMultyColor, 1 - blurMultyColor, type="double3")

        pm.setAttr((rampOneName + ".type"), 1)

        pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d2 + ".rotateUV"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampOneName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampOneName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")

        pm.setAttr((rampTwoName + ".type"), 1)

        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
        pm.setAttr((p2d3 + ".rotateUV"), 180)
        pm.setAttr((rampTwoName + ".colorEntryList[0].position"), 0)
        pm.setAttr((rampTwoName + ".colorEntryList[1].position"), .75)
        pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
        pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")


    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)




#---10

def buildSoftBOXrampNode(intp,cutout,blurAmount,lightGenFieldValue):

    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = ""
    rampOneName = ""
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""
    p2d1 = ""
    p2d2 = ""

    blurMulty = blurAmount * .06
    blurMultyColor = blurAmount * .02

    layerTexHubName = cmds.shadingNode("layeredTexture", name="softBox_1", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    outer = pm.shadingNode('ramp', name='softBox_outer', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %outer, (0 + blurMulty),(0 + blurMulty),(0 + blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %outer, 1)
    pm.setAttr('%s.colorEntryList[0].color' %outer, 1,1,1, type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %outer, (.766 - blurMulty))
    pm.setAttr('%s.type' %(outer), 5)
    pm.setAttr('%s.interpolation' %(outer), 1)

    inner = pm.shadingNode('ramp', name='softBox_inner', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %inner, 0,0,0, type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %inner, 1)
    pm.setAttr('%s.colorEntryList[0].color' %inner, (1 - blurMulty),(1 - blurMulty),(1 - blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %inner, (.2 + blurMulty))
    pm.setAttr('%s.type' %(inner), 4)
    pm.setAttr('%s.interpolation' %(inner), 2)

    place2d = pm.shadingNode('place2dTexture', name='softBox_p2d', asUtility=True)
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (outer) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (outer) )
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (inner) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (inner) )
    pm.connectAttr( '%s.outColor' % (inner), '%s.colorGain' % (outer))
    pm.connectAttr((outer + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    #layerTexHubName2 = cmds.shadingNode("layeredTexture", name="softBoxRampNode", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    #rampOneName = cmds.shadingNode("ramp", name="rampeTop", asTexture=True)
    #rampTwoName = cmds.shadingNode("ramp", name="rampeBottom", asTexture=True)

    #p2d1 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d1 + ".repeatU", 1)
    #p2d2 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d2 + ".repeatU", 1)
    #p2d3 = cmds.createNode("place2dTexture")
    #cmds.setAttr(p2d1 + ".repeatU", 1)
    #placAttrs2Dout = (".outUV", ".outUvFilterSize")
    #placAttrs2Din = (".uvCoord", ".uvFilterSize")

    #blurMulty = blurAmount * .03
    #blurMultyColor = blurAmount * .02

    #pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    #pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    #pm.setAttr((rampOneName + ".colorEntryList[1].position"), (.25))
    #pm.setAttr((rampOneName + ".colorEntryList[0].position"), (.24 - blurMulty))
    #pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    #pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    #pm.setAttr((p2d3 + ".repeatV"), -1)

    #pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    #pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    #pm.setAttr((rampTwoName + ".colorEntryList[1].position"), (.25))
    #pm.setAttr((rampTwoName + ".colorEntryList[0].position"), (.24 - blurMulty))
    #pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    #pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

    #cmds.connectAttr(p2d1 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")
    #cmds.connectAttr(p2d2 + ".outUV", rampOneName + ".uvCoord")
    #cmds.connectAttr(p2d2 + ".outUvFilterSize", rampOneName + ".uvFilterSize")
    #cmds.connectAttr(p2d3 + ".outUV", rampTwoName + ".uvCoord")
    #cmds.connectAttr(p2d3 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")
    #pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    #pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    #pm.setAttr((rampOneName + ".interpolation"), 1)
    #pm.setAttr((rampTwoName + ".interpolation"), 1)
    #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", )

    #pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    #pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    #pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)

def buildSoftBOXrampNodeHor(intp,cutout,blurAmount,lightGenFieldValue):


    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = ""
    rampOneName = ""
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""
    p2d1 = ""
    p2d2 = ""

    blurMulty = blurAmount * .06
    blurMultyColor = blurAmount * .02

    layerTexHubName = cmds.shadingNode("layeredTexture", name="softBox_1", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    outer = pm.shadingNode('ramp', name='softBox_outer', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %outer, (0 + blurMulty),(0 + blurMulty),(0 + blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %outer, 1)
    pm.setAttr('%s.colorEntryList[0].color' %outer, 1,1,1, type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %outer, (.766 - blurMulty))
    pm.setAttr('%s.type' %(outer), 5)
    pm.setAttr('%s.interpolation' %(outer), 1)

    inner = pm.shadingNode('ramp', name='softBox_inner', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %inner, 0,0,0, type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %inner, 1)
    pm.setAttr('%s.colorEntryList[0].color' %inner, (1 - blurMulty),(1 - blurMulty),(1 - blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %inner, (.2 + blurMulty))
    pm.setAttr('%s.type' %(inner), 4)
    pm.setAttr('%s.interpolation' %(inner), 2)

    place2d = pm.shadingNode('place2dTexture', name='softBox_p2d', asUtility=True)
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (outer) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (outer) )
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (inner) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (inner) )
    pm.connectAttr( '%s.outColor' % (inner), '%s.colorGain' % (outer))
    pm.connectAttr((outer + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    #layerTexHubName2 = cmds.shadingNode("layeredTexture", name="softBoxRampNode", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTop", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBottom", asTexture=True)

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[1].position"), (.25))
    pm.setAttr((rampOneName + ".colorEntryList[0].position"), (.24 - (blurMulty*.4)))
    pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((p2d3 + ".repeatV"), -1)

    pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[1].position"), (.25))
    pm.setAttr((rampTwoName + ".colorEntryList[0].position"), (.24 - (blurMulty*.4)))
    pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")

    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")
    cmds.connectAttr(p2d2 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampOneName + ".uvFilterSize")
    cmds.connectAttr(p2d3 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.setAttr((rampOneName + ".interpolation"), 1)
    pm.setAttr((rampTwoName + ".interpolation"), 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", )

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)

def buildSoftBOXrampNodeVert(intp,cutout,blurAmount,lightGenFieldValue):


    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = ""
    rampOneName = ""
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""
    p2d1 = ""
    p2d2 = ""

    blurMulty = blurAmount * .06
    blurMultyColor = blurAmount * .02

    layerTexHubName = cmds.shadingNode("layeredTexture", name="softBox_1", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    outer = pm.shadingNode('ramp', name='softBox_outer', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %outer, (0 + blurMulty),(0 + blurMulty),(0 + blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %outer, 1)
    pm.setAttr('%s.colorEntryList[0].color' %outer, 1,1,1, type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %outer, (.766 - blurMulty))
    pm.setAttr('%s.type' %(outer), 5)
    pm.setAttr('%s.interpolation' %(outer), 1)

    inner = pm.shadingNode('ramp', name='softBox_inner', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %inner, 0,0,0, type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %inner, 1)
    pm.setAttr('%s.colorEntryList[0].color' %inner, (1 - blurMulty),(1 - blurMulty),(1 - blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %inner, (.2 + blurMulty))
    pm.setAttr('%s.type' %(inner), 4)
    pm.setAttr('%s.interpolation' %(inner), 2)

    place2d = pm.shadingNode('place2dTexture', name='softBox_p2d', asUtility=True)
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (outer) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (outer) )
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (inner) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (inner) )
    pm.connectAttr( '%s.outColor' % (inner), '%s.colorGain' % (outer))
    pm.connectAttr((outer + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    #layerTexHubName2 = cmds.shadingNode("layeredTexture", name="softBoxRampNode", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTop", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBottom", asTexture=True)

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[1].position"), (.25))
    pm.setAttr((rampOneName + ".colorEntryList[0].position"), (.24 - (blurMulty*.4)))
    pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((p2d3 + ".repeatU"), -1)
    pm.setAttr((p2d3 + ".rotateUV"), 90)

    pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[1].position"), (.25))
    pm.setAttr((rampTwoName + ".colorEntryList[0].position"), (.24 - (blurMulty*.4)))
    pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((p2d2 + ".rotateUV"), 90)

    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")
    cmds.connectAttr(p2d2 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampOneName + ".uvFilterSize")
    cmds.connectAttr(p2d3 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.setAttr((rampOneName + ".interpolation"), 1)
    pm.setAttr((rampTwoName + ".interpolation"), 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", )

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)

def buildSoftBOXrampNodeDiag(intp,cutout,blurAmount,lightGenFieldValue):


    #print "intp = ", intp
    print "blur amount = ",blurAmount
    sel = cmds.ls(sl = True)

    layerTexHubName = ""
    rampOneName = ""
    rampTwoName = ""
    rampThreeName = ""
    rampFourName = ""
    p2d1 = ""
    p2d2 = ""

    blurMulty = blurAmount * .06
    blurMultyColor = blurAmount * .02

    layerTexHubName = cmds.shadingNode("layeredTexture", name="softBox_1", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    outer = pm.shadingNode('ramp', name='softBox_outer', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %outer, (0 + blurMulty),(0 + blurMulty),(0 + blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %outer, 1)
    pm.setAttr('%s.colorEntryList[0].color' %outer, 1,1,1, type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %outer, (.766 - blurMulty))
    pm.setAttr('%s.type' %(outer), 5)
    pm.setAttr('%s.interpolation' %(outer), 1)

    inner = pm.shadingNode('ramp', name='softBox_inner', asTexture=True)
    pm.setAttr('%s.colorEntryList[1].color' %inner, 0,0,0, type='double3')
    pm.setAttr('%s.colorEntryList[1].position' %inner, 1)
    pm.setAttr('%s.colorEntryList[0].color' %inner, (1 - blurMulty),(1 - blurMulty),(1 - blurMulty), type='double3')
    pm.setAttr('%s.colorEntryList[0].position' %inner, (.2 + blurMulty))
    pm.setAttr('%s.type' %(inner), 4)
    pm.setAttr('%s.interpolation' %(inner), 2)

    place2d = pm.shadingNode('place2dTexture', name='softBox_p2d', asUtility=True)
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (outer) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (outer) )
    pm.connectAttr( '%s.outUV' % (place2d), '%s.uvCoord' % (inner) )
    pm.connectAttr( '%s.outUvFilterSize' % (place2d), '%s.uvFilterSize' % (inner) )
    pm.connectAttr( '%s.outColor' % (inner), '%s.colorGain' % (outer))
    pm.connectAttr((outer + ".outColor"), (layerTexHubName + ".inputs[2].color"), force=True)

    #layerTexHubName2 = cmds.shadingNode("layeredTexture", name="softBoxRampNode", asTexture=True)
    pm.setAttr(layerTexHubName + ".alphaIsLuminance", 1)

    rampOneName = cmds.shadingNode("ramp", name="rampeTop", asTexture=True)
    rampTwoName = cmds.shadingNode("ramp", name="rampeBottom", asTexture=True)

    p2d1 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    p2d2 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d2 + ".repeatU", 1)
    p2d3 = cmds.createNode("place2dTexture")
    cmds.setAttr(p2d1 + ".repeatU", 1)
    placAttrs2Dout = (".outUV", ".outUvFilterSize")
    placAttrs2Din = (".uvCoord", ".uvFilterSize")

    pm.setAttr((rampOneName+ ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[1].position"), (.25))
    pm.setAttr((rampOneName + ".colorEntryList[0].position"), (.24 - (blurMulty*.4)))
    pm.setAttr((rampOneName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampOneName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((p2d2 + ".repeatV"), -1)
    pm.setAttr((p2d2 + ".rotateFrame"), -45)

    pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 0, 0, 0, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[1].position"), (.25))
    pm.setAttr((rampTwoName + ".colorEntryList[0].position"), (.24 - (blurMulty*.4)))
    pm.setAttr((rampTwoName + ".colorEntryList[1].color"), 1, 1, 1, type="double3")
    pm.setAttr((rampTwoName + ".colorEntryList[0].color"), 0, 0, 0, type="double3")
    pm.setAttr((p2d3 + ".rotateFrame"), -45)

    cmds.connectAttr(p2d1 + ".outUvFilterSize", rampThreeName + ".uvFilterSize")
    cmds.connectAttr(p2d2 + ".outUV", rampOneName + ".uvCoord")
    cmds.connectAttr(p2d2 + ".outUvFilterSize", rampOneName + ".uvFilterSize")
    cmds.connectAttr(p2d3 + ".outUV", rampTwoName + ".uvCoord")
    cmds.connectAttr(p2d3 + ".outUvFilterSize", rampTwoName + ".uvFilterSize")
    pm.connectAttr((rampOneName + ".outColor"), (layerTexHubName + ".inputs[1].color"), force=True)
    pm.connectAttr((rampTwoName + ".outColor"), (layerTexHubName + ".inputs[0].color"), force=True)
    pm.setAttr((rampOneName + ".interpolation"), 1)
    pm.setAttr((rampTwoName + ".interpolation"), 1)
    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", )

    pm.setAttr(layerTexHubName + ".inputs[0]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[1]blendMode", 6)
    pm.setAttr(layerTexHubName + ".inputs[2]blendMode", 0)

    if cutout == 1:

        cutout_circle(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 2:

        cutout_box(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 3:

        cutout_noise(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 4:

        cutout_fractal(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 5:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 6:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 7:

        cutout_grid(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 8:

        cutout_leaves(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 9:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 10:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 11:

        cutout_bulge(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 12:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 13:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    if cutout == 14:

        cutout_checker(layerTexHubName,rampTwoName,rampOneName,rampThreeName,rampFourName,p2d1,p2d2,cutout,blurAmount)

    lghtSel = 0

    print "lightGenFieldValue = ",lightGenFieldValue

    if lightGenFieldValue == "Enter Light Name" or lightGenFieldValue == "":
        print "no light name field detected"
        #print "sel = ",sel
        selType = pm.nodeType(sel)
        exi = len(sel)
        #print "exi = ",exi
        if exi > 0:
            if selType == "transform":
                shapes = cmds.listRelatives(sel, children=True)
                sel = shapes[0]
            else:
                sel = sel[0]
            attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)
            #print "attExists = ",attExists
            if attExists == 1:
                pm.setAttr(sel + ".useRectTex", 1)
                lghtSel = 1
                pm.setAttr(sel + ".useRectTex",1)
                pm.connectAttr((layerTexHubName + ".outColor"), (sel + ".rectTex"), force=True)
                pm.setAttr((sel + ".showTex"), 1)


    else:

        print "light name field detected"

        sel = pm.shadingNode('VRayLightRectShape', asLight=True)
        rectLightName = pm.rename(sel, lightGenFieldValue)
        sel = rectLightName
        lghtSel = 1
        attExists = pm.attributeQuery("useRectTex", node=sel, exists=True)

        pm.setAttr('%s.sz' %(rectLightName),lock=True)
        pm.setAttr('%s.invisible' %(rectLightName), 1)
        pm.setAttr('%s.intensityMult' %(rectLightName), 1 )
        pm.setAttr('%s.rectTexA' %(rectLightName), 0)
        pm.setAttr('%s.multiplyByTheLightColor' %(rectLightName), 1)

        pm.setAttr(sel + ".useRectTex",1)
        pm.connectAttr((layerTexHubName + ".outColor"), (rectLightName + ".rectTex"), force=True)
        pm.setAttr((rectLightName + ".showTex"), 1)

def main():
    rampGenWin()

#main()
