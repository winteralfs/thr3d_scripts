"""
.. image:: U:/cwinters/docs/build/html/_images/standard_lighting_rig_dome_fix/standard_lighting_rig_dome_repair.JPG
   :align: center
   :scale: 75%

Standard_lighting_tool_rotation_fix cleans out all the expressions and render layer overrides for the standard lighting rig, and rebuilds
them with the default values.  You run the tool by pressing the icon on the lighting shelf.

.. image:: U:/cwinters/docs/build/html/_images/standard_lighting_rig_dome_fix/standard_lighting_rig_dome_repair_window.JPG
   :align: center
   :scale: 75%

"""

import maya.cmds as cmds
import maya.mel as mel

def main ():
    curRenLay = cmds.editRenderLayerGlobals(currentRenderLayer = True, query = True)
    exp1e = cmds.objExists("expression1")
    exp2e = cmds.objExists("expression2")
    exp3e = cmds.objExists("expression3")
    exp4e = cmds.objExists("expression4")
    exp5e = cmds.objExists("expression5")
    exp6e = cmds.objExists("expression6")
    exp7e = cmds.objExists("expression7")
    if exp1e == 1:
        print "deleting expression1"
        cmds.delete("expression1")
    if exp2e == 1:
        print "deleting expression2"
        cmds.delete("expression2")
    if exp3e == 1:
        print "deleting expression3"
        cmds.delete("expression3")
    if exp4e == 1:
        print "deleting expression4"
        cmds.delete("expression4")
    if exp5e == 1:
        print "deleting expression5"
        cmds.delete("expression5")
    if exp6e == 1:
        print "deleting expression6"
        cmds.delete("expression6")
    if exp7e == 1:
        print "deleting expression7"
        cmds.delete("expression7")

    #-- Ft

    cmds.editRenderLayerGlobals(currentRenderLayer = "Ft")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 0)
    cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

    #-- FtTp

    cmds.editRenderLayerGlobals(currentRenderLayer = "FtTp")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 0)
    cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

    #--Tp

    cmds.editRenderLayerGlobals(currentRenderLayer = "Tp")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt" + ".verRotation")
    mel.eval('expressionEditor EE "place_env_rot_sdt_lgt" "verRotation";')
    mel.eval('expression -s "place_env_rot_sdt_lgt.verRotation = std_lgt_core.rotation + 90"  -o place_env_rot_sdt_lgt -ae 1 -uc all ;')

    #--FtLtTp

    cmds.editRenderLayerGlobals(currentRenderLayer = "FtLtTp")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt" + ".horRotation")
    mel.eval('expressionEditor EE "place_env_rot_sdt_lgt" "horRotation";')
    mel.eval('expression -s "place_env_rot_sdt_lgt.horRotation = (90 - camera_rig.hangle) * -1"  -o place_env_rot_sdt_lgt -ae 1 -uc all ;')

    #--Bk

    cmds.editRenderLayerGlobals(currentRenderLayer = "Bk")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt" + ".horRotation")
    mel.eval('expressionEditor EE "place_env_rot_sdt_lgt" "horRotation";')
    mel.eval('expression -s "place_env_rot_sdt_lgt.horRotation = std_lgt_core.rotation + 180"  -o place_env_rot_sdt_lgt -ae 1 -uc all ;')

    #--FtRtTp

    cmds.editRenderLayerGlobals(currentRenderLayer = "FtRtTp")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt" + ".horRotation")
    mel.eval('expressionEditor EE "place_env_rot_sdt_lgt" "horRotation";')
    mel.eval('expression -s "place_env_rot_sdt_lgt.horRotation = 90 - camera_rig.hangle"  -o place_env_rot_sdt_lgt -ae 1 -uc all ;')

    #--Lt

    cmds.editRenderLayerGlobals(currentRenderLayer = "Lt")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt" + ".horRotation")
    mel.eval('expressionEditor EE "place_env_rot_sdt_lgt" "horRotation";')
    mel.eval('expression -s "place_env_rot_sdt_lgt.horRotation = std_lgt_core.rotation + 90"  -o place_env_rot_sdt_lgt -ae 1 -uc all ;')

    #--Bt

    cmds.editRenderLayerGlobals(currentRenderLayer = "Bt")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt" + ".verRotation")
    mel.eval('expressionEditor EE "place_env_rot_sdt_lgt" "verRotation";')
    mel.eval('expression -s "place_env_rot_sdt_lgt.verRotation = std_lgt_core.rotation + 270"  -o place_env_rot_sdt_lgt -ae 1 -uc all ;')

    #--Rt

    cmds.editRenderLayerGlobals(currentRenderLayer = "Rt")
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
    cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt" + ".horRotation")
    mel.eval('expressionEditor EE "place_env_rot_sdt_lgt" "horRotation";')
    mel.eval('expression -s "place_env_rot_sdt_lgt.horRotation = std_lgt_core.rotation + 270"  -o place_env_rot_sdt_lgt -ae 1 -uc all ;')

    curRenLay = cmds.editRenderLayerGlobals(currentRenderLayer = curRenLay)
