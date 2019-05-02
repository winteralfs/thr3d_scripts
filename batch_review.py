"""
lighting_tools_shelf: batch_review
********************************************

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_gui.JPG
   :align: center
   :scale: 75%

batch_review is a tool that launches a sequence of renders to the V-ray frame buffer, one for each render layer,
as a convenient way to visually review each camera angle before publishing.

batch_review can be launched in two different ways, either from the lighting_tool_shelf:

.. image:: U:/cwinters/docs/build/html/_images/batch_review/lighting_tools_shelf_batch_review.JPG
   :align: center
   :scale: 75%

or from the Thr3d drop down menu in Maya:

.. image:: U:/cwinters/docs/build/html/_images/batch_review/drop_down_menu.JPG
   :align: center
   :scale: 75%

------

the sequence of renders are launched by pressing the button labeled 'render', and you can interupt the sequence by pressing the button labeled 'cancel renders.'
The frame that is currently rendering will complete, but you can stop that as well by pressing the 'esc' button on the keyboard.

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_gui_render_and_cancel_buttons.JPG
   :align: center
   :scale: 75%

there are three preset settings available for quickly setting the quality of the renders, and there are also inputs for manually setting the resolution and
threshold of the renders. The higher the resolution, the higher the quality of the image, and the lower the threshold, the higher the quality of the image.

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_gui_preset_quality.JPG
   :align: center
   :scale: 75%

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_gui_resolution.JPG
   :align: center
   :scale: 75%

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_threshold.JPG
  :align: center
  :scale: 75%

batch_review also has a checkbox to utilize the V-ray framebuffer render region function. If the checkbox is switched on, onlu the region defined by the
marquee will be rendered for each render layer.

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_use_render_region.JPG
  :align: center
  :scale: 75%

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_use_render_region_example.JPG
  :align: center
  :scale: 75%

lastly, batch_review has a checkbox option to turn on and off the render elements for the frames.  Switching them off will speed up processing time, but you
will not be able to evaluate the different render passes such as: reflection, refraction, and bump maps.

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_elements.JPG
  :align: center
  :scale: 75%

.. image:: U:/cwinters/docs/build/html/_images/batch_review/batch_review_elements_example_2.JPG
:align: center
:scale: 75%


"""

import maya
import maya.cmds as cmds
import re
from functools import partial
import sys
from datetime import datetime

global cancel
cancel = 0

print 'batch_review'

def no_cam_window_popup(no_cam_set_list):
    #print no_cam_set_list
    cmds.window(title = 'WARNING: NO CAMERAS LINKED TO LAYERS', width = 300, height = 75, sizeable = False)
    cmds.columnLayout("mainColumn", adjustableColumn = True)
    cmds.rowLayout("nameRowLayout01", numberOfColumns = 15, parent = "mainColumn")
    cmds.text(label = ("no cam set for layers:"))
    for layer in no_cam_set_list:
        cmds.text(label = ('' + layer + ', '),font = 'boldLabelFont')
    cmds.showWindow()

def renderThumbs(checkBoxLow,checkBoxMid,checkBoxHigh,checkBoxRenderRegion,intField_res,floatField_thrhld,*args):
    global cancel
    cams = cmds.ls(type = "camera")
    cancel = 0
    popup_win = 0
    no_cam_set_list = []
    cmds.loadPlugin('vrayformaya', quiet=True)
    cmds.pluginInfo('vrayformaya', edit=True, autoload=True)
    cmds.setAttr("defaultRenderGlobals.ren", "vray", type = "string")

    curLay = cmds.editRenderLayerGlobals( currentRenderLayer = True, query = True )
    changeLay = curLay

    rls = cmds.ls(type = "renderLayer")
    renCams = cmds.ls(type = "camera")
    renCam = "persp"

    lowBut = cmds.checkBox(checkBoxLow,value = True, query = True)
    midBut = cmds.checkBox(checkBoxMid,value = True, query = True)
    highBut = cmds.checkBox(checkBoxHigh,value = True, query = True)
    globopt_cache_geom_plugins = cmds.getAttr('vraySettings.globopt_cache_geom_plugins')
    #print 'globopt_cache_geom_plugins = ',globopt_cache_geom_plugins

    print " "
    print "-- batch_review --"

    res = cmds.intField(intField_res, v = True, query = True)
    thr = cmds.floatField(floatField_thrhld, v = True,query = True)

    if lowBut == 1:
        cmds.setAttr("vraySettings.dmcThreshold",thr)
        cmds.setAttr("vraySettings.width", res)
        cmds.setAttr("vraySettings.height", res)
        cmds.setAttr("vraySettings.globopt_cache_geom_plugins",1)
        cmds.setAttr("vraySettings.globopt_ray_maxIntens_on",1)
        #cmds.setAttr('vraySettings.globopt_cache_geom_plugins',globopt_cache_geom_plugins)
        print " "
        print "---"
        print "quality = %s, dmcThreshold = %s"%(res,thr)
    if midBut == 1:
        cmds.setAttr("vraySettings.dmcThreshold",thr)
        cmds.setAttr("vraySettings.width", res)
        cmds.setAttr("vraySettings.height", res)
        cmds.setAttr("vraySettings.globopt_cache_geom_plugins",1)
        cmds.setAttr("vraySettings.globopt_ray_maxIntens_on",1)
        #cmds.setAttr('vraySettings.globopt_cache_geom_plugins',globopt_cache_geom_plugins)
        print " "
        print "---"
        print "quality = %s, dmcThreshold = %s"%(res,thr)
    if highBut == 1:
        cmds.setAttr("vraySettings.dmcThreshold",thr)
        cmds.setAttr("vraySettings.width", res)
        cmds.setAttr("vraySettings.height", res)
        cmds.setAttr("vraySettings.globopt_cache_geom_plugins",1)
        cmds.setAttr("vraySettings.globopt_ray_maxIntens_on",1)
        #cmds.setAttr('vraySettings.globopt_cache_geom_plugins',globopt_cache_geom_plugins)
        print " "
        print "---"
        print "quality = %s, dmcThreshold = %s"%(res,thr)

    print "--- "
    print " "

    for rl in rls:
        found_cam = 0
        if rl != "defaultRenderLayer" and cancel == 0:
            rlState = cmds.getAttr(rl + ".renderable")
            if rlState == 1:
                print ' '
                print "rende layer = ",rl
                cmds.editRenderLayerGlobals( currentRenderLayer = rl )
                for cam in cams:
                    camState = cmds.getAttr(cam + ".renderable")
                    if camState == 1:
                        rrState = cmds.checkBox(checkBoxRenderRegion,value = True,query = True)
                        reg = cmds.vray("vfbControl","-getregion")
                        if  rrState == 0:
                            cmds.vray("vfbControl","-setregion","reset")
                        if  rrState == 1:
                            cmds.vray("vfbControl","-setregionenabled",1)
                            cmds.vray("vfbControl","-setregion",reg[0],reg[1],reg[2],reg[3])
                        mayaString = "renderWindowRenderCamera render renderView " + cam
                        print 'using ' + cam + ' for ' + rl
                        maya.mel.eval(mayaString)
                        cmds.vray("vfbControl", "-historysave")
                        cmds.vray("vfbControl", "-historyselect",0)
                        dte = datetime.now().strftime('%H:%M:%S')
                        editStr = dte + " ,render layer: " + rl + " , " + "cam: " + cam
                        cmds.vray("vfbControl", "-historycomment", editStr)
                        print " "
                        found_cam = 1
                if found_cam == 0:
                    print 'no camera link found, using persp cam for ',rl
                    cam = 'persp'
                    rrState = cmds.checkBox(checkBoxRenderRegion,value = True,query = True)
                    reg = cmds.vray("vfbControl","-getregion")
                    if  rrState == 0:
                        cmds.vray("vfbControl","-setregion","reset")
                    if  rrState == 1:
                        cmds.vray("vfbControl","-setregionenabled",1)
                        cmds.vray("vfbControl","-setregion",reg[0],reg[1],reg[2],reg[3])
                    mayaString = "renderWindowRenderCamera render renderView " + cam
                    maya.mel.eval(mayaString)
                    cmds.vray("vfbControl", "-historysave")
                    cmds.vray("vfbControl", "-historyselect",0)
                    dte = datetime.now().strftime('%H:%M:%S')
                    editStr = dte + " ,render layer: " + rl + " , " + "cam: " + cam
                    cmds.vray("vfbControl", "-historycomment", editStr)
                    popup_win = 1
                    no_cam_set_list.append(rl)
    #if popup_win == 1:
        #no_cam_window_popup(no_cam_set_list)


def checkBoxCheckLow(checkBoxLow,checkBoxMid,checkBoxHigh,intField_res,floatField_thrhld,*args):
    global cancel
    lowButVal = cmds.checkBox(checkBoxLow,value = True, query = True)
    midButVal = cmds.checkBox(checkBoxMid,value = True, query = True)
    highButVal = cmds.checkBox(checkBoxHigh,value = True, query = True)

    cmds.checkBox(checkBoxMid,value = False, edit = True)
    cmds.checkBox(checkBoxHigh,value = False, edit = True)
    cmds.intField(intField_res, v = 800,edit = True)
    cmds.floatField(floatField_thrhld, v = .1,edit = True )
    cancel = 0

def checkBoxCheckMid(checkBoxLow,checkBoxMid,checkBoxHigh,intField_res,floatField_thrhld,*args):
    global cancel
    lowButVal = cmds.checkBox(checkBoxLow,value = True, query = True)
    midButVal = cmds.checkBox(checkBoxMid,value = True, query = True)
    highButVal = cmds.checkBox(checkBoxHigh,value = True, query = True)

    cmds.checkBox(checkBoxLow,value = False, edit = True)
    cmds.checkBox(checkBoxHigh,value = False, edit = True)
    cmds.intField(intField_res, v = 1000,edit = True)
    cmds.floatField(floatField_thrhld, v = .5,edit = True )
    cancel = 0

def checkBoxCheckHigh(checkBoxLow,checkBoxMid,checkBoxHigh,intField_res,floatField_thrhld,*args):
    global cancel
    lowButVal = cmds.checkBox(checkBoxLow,value = True, query = True)
    midButVal = cmds.checkBox(checkBoxMid,value = True, query = True)
    highButVal = cmds.checkBox(checkBoxHigh,value = True, query = True)

    cmds.checkBox(checkBoxLow,value = False, edit = True)
    cmds.checkBox(checkBoxMid,value = False, edit = True)
    cmds.intField(intField_res, v = 2000,edit = True)
    cmds.floatField(floatField_thrhld, v = .008,edit = True )
    cancel = 0

def checkBoxAOVchange(checkBoxAOV,*args):
    checkBoxAOVval = cmds.checkBox(checkBoxAOV,value = True,query = True)
    if checkBoxAOVval == 1:
        cmds.setAttr("vraySettings.relements_enableall", 1)
    if checkBoxAOVval == 0:
        cmds.setAttr("vraySettings.relements_enableall", 0)

def rrCheckbox(checkBoxRenderRegion,reg,*args):
    global gReg
    zeroes = ['0','0','0','0']
    tRes = cmds.vray("vfbControl","-getregion")
    if tRes != zeroes:
        gReg = tRes
    rrstate = cmds.checkBox(checkBoxRenderRegion,value = True,query = True)
    if rrstate == 0:
        if gReg != zeroes:
            cmds.vray("vfbControl","-setregion",gReg[0],gReg[1],gReg[2],gReg[3])
        else:
            cmds.vray("vfbControl","-setregion",reg[0],reg[1],reg[2],reg[3])
        cmds.vray("vfbControl","-setregion","reset")
    if rrstate == 1:
        cmds.vray("vfbControl","-setregionenabled",1)
        if gReg != zeroes:
            cmds.vray("vfbControl","-setregion",gReg[0],gReg[1],gReg[2],gReg[3])
        else:
            cmds.vray("vfbControl","-setregion",reg[0],reg[1],reg[2],reg[3])
    return(reg)

def cancelOPs(*args):
    global cancel
    cancel = 1
    raise Exception("quitting renders")

def renthumbsWin():
    name = "Batch_Review"
    global gReg
    gReg = ('0','0','0','0')
    zeroes = ('0','0','0','0')
    windowSize = (200,100)
    if (cmds.window(name, exists = True)):
        cmds.deleteUI(name)
    window = cmds.window(name, title = name, width = 350, height = 50,bgc = (.2,.2,.2), s = False)
    cmds.columnLayout("mainColumn", adjustableColumn = True)
    cmds.rowLayout("nameRowLayout01", numberOfColumns = 15, parent = "mainColumn")
    cmds.text(label = "preset quality:  ")
    checkBoxLow = cmds.checkBox(label = "low", value = False)
    checkBoxMid = cmds.checkBox(label = "mid", value = True,)
    checkBoxHigh = cmds.checkBox(label = "high", value = False)
    cmds.text(label = "                             ")
    cmds.text(label = "resolution:  ")
    intField_res = cmds.intField(v = 1000,width = 45)
    cmds.text(label = "  ")
    cmds.text(label = "threshold:  ")
    floatField_thrhld = cmds.floatField(v = .5,width = 45)
    cmds.checkBox(checkBoxLow, changeCommand = partial(checkBoxCheckLow,checkBoxLow,checkBoxMid,checkBoxHigh,intField_res,floatField_thrhld), edit = True)
    cmds.checkBox(checkBoxMid, changeCommand = partial(checkBoxCheckMid,checkBoxLow,checkBoxMid,checkBoxHigh,intField_res,floatField_thrhld),edit = True)
    cmds.checkBox(checkBoxHigh, changeCommand = partial(checkBoxCheckHigh,checkBoxLow,checkBoxMid,checkBoxHigh,intField_res,floatField_thrhld),edit = True)
    cmds.rowLayout("nameRowLayout02", numberOfColumns = 10, parent = "mainColumn")
    cmds.text(label = "  ")
    cmds.rowLayout("nameRowLayout03", numberOfColumns = 5, parent = "mainColumn")
    renderButton = cmds.button(label = "render",width = 100, bgc = (.6,.8,1) )
    cmds.text(label = "  ")
    cmds.button(label = "cancel renders", command = partial(cancelOPs),bgc = (1,.3,.3) )
    cmds.rowLayout("nameRowLayout04", numberOfColumns = 10, parent = "mainColumn")
    cmds.text(label = "  ")
    cmds.rowLayout("nameRowLayout05", numberOfColumns = 10, parent = "mainColumn")
    checkBoxRenderRegion = cmds.checkBox(label = "use render region", value = False)
    cmds.text(label = "  ")
    cmds.text(label = "  ")
    reg = cmds.vray("vfbControl","-getregion")
    if reg != gReg and reg != zeroes:
        gReg = reg
    cmds.vray("vfbControl","-setregion","reset")
    cmds.checkBox(checkBoxRenderRegion,changeCommand = partial(rrCheckbox,checkBoxRenderRegion,reg),edit = True)
    cmds.rowLayout("nameRowLayout06", numberOfColumns = 10, parent = "mainColumn")
    AOVstate = cmds.getAttr("vraySettings.relements_enableall")
    checkBoxAOV = cmds.checkBox(label = "elements", value = AOVstate)
    cmds.checkBox(checkBoxAOV,changeCommand = partial(checkBoxAOVchange,checkBoxAOV),edit = True)
    cmds.button(renderButton,command = partial(renderThumbs,checkBoxLow,checkBoxMid,checkBoxHigh,checkBoxRenderRegion,intField_res,floatField_thrhld),edit = True)
    cmds.showWindow()

def main():
    renthumbsWin()

#main()
