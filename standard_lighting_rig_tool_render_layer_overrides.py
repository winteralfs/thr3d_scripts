import maya.cmds as cmds
import maya.mel as mel

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

#-- Rt

cmds.editRenderLayerGlobals(currentRenderLayer = "Rt")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 270)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

#-- Lt

cmds.editRenderLayerGlobals(currentRenderLayer = "Lt")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 90)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

#-- Ft

cmds.editRenderLayerGlobals(currentRenderLayer = "Ft")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 0)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

#-- FtTp

cmds.editRenderLayerGlobals(currentRenderLayer = "FtTp")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 0)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

#--Tp

cmds.editRenderLayerGlobals(currentRenderLayer = "Tp")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 0)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 90)

#--Bt

cmds.editRenderLayerGlobals(currentRenderLayer = "Bt")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 0)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 270)

#--FtLtTp

cmds.editRenderLayerGlobals(currentRenderLayer = "FtLtTp")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 15)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

#--Bk

cmds.editRenderLayerGlobals(currentRenderLayer = "Bk")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", 180)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)

#--FtRtTp

cmds.editRenderLayerGlobals(currentRenderLayer = "FtRtTp")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation",remove = True)
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.horRotation")
cmds.editRenderLayerAdjustment("place_env_rot_sdt_lgt.verRotation")
cmds.setAttr("place_env_rot_sdt_lgt.horRotation", -15)
cmds.setAttr("place_env_rot_sdt_lgt.verRotation", 0)
