"""
Lights_pallette is a tool to help speed up a few common tasks related to lighting a scene in Maya.

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI.png
   :align: center
   :scale: 50%

It is launched from the lighting tools shelf.

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_lighting_shelf.png
   :align: center
   :scale: 50%

You can hide, show, and toggle the textures for all the lights in the scene, or just the selected lights.

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_lights_ramps_on.png
   :align: center
   :scale: 50%

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_lights_ramps_off.png
   :align: center
   :scale: 50%

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_lights_ramps_toggle.png
   :align: center
   :scale: 50%

You can also set or remove render layer overrides for light transforms and light intensity for all the selected lights on
the active render layer. If there are currently render layer overrides set for any of the selected lights on the active render
layer, the button wil be orange, and clicking it will remove the overrides for those lights. Otherwise, the button will be grey,
and clicking it will set the overrides for all the selected lights on the active render layer.

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_lights_overrides.png
   :align: center
   :scale: 50%

You can hide and display all the lights in the scene.

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_hide_lights.png
   :align: center
   :scale: 50%

And you can set or remove a V-ray smoothing attribute node for the selected objects. If the button is grey it means no
vray smoothing attribute was detected for any selected objects, and if the button is green it means at least one of the
selected objects currently has a vray smoothing node attached. Pressing the button while it is green will remove the smoothing
nodes from all the selected objects.

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_smoothing.png
   :align: center
   :scale: 50%

Lastly, you can change render layers using the GUI.

.. image:: U:/cwinters/docs/build/html/_images/lights_pallette/lights_pallette_GUI_render_layers.png
   :align: center
   :scale: 50%

 """

import sys
sys.path.append("C:/Users/Chris.Winters/Desktop/PythonTesting/")
import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

# this is a script to speed up hiding and showing lights, hiding and showing rect light textures,and setting render layer overrides

# defines the lightsPalette class

class lightsPalette():
    def __init__(self):
        self.lights = []
        self.lights = cmds.ls(type = "VRayLightRectShape")

# a method that clears a layout of all data

    def clear_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())

# methods to turn all the rect light textures off and on

    def all_toggle_texture_off(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 0)

    def all_toggle_texture_on(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 1)

# methods to turn the selected rect light textures off and on

    def selected_toggle_texture_off(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 0)

    def selected_toggle_texture_on(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 1)

# a method to toggle all the rect light textutes off and on

    def all_toggle_texture(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        get_toggle = cmds.getAttr(kid + ".showTex")
                        if get_toggle == 0:
                            cmds.setAttr(kid + ".showTex", 1)
                        if get_toggle == 1:
                            cmds.setAttr(kid + ".showTex", 0)

# a method to toggle selected rect lights textures off and on

    def selected_toggle_texture(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        get_toggle = cmds.getAttr(kid + ".showTex")
                        if get_toggle == 0:
                            cmds.setAttr(kid + ".showTex", 1)
                        if get_toggle == 1:
                            cmds.setAttr(kid + ".showTex", 0)

#  a method to create or delete render layer overrides for selected lights and objects

    def sel_toggle_overrides(self,checked):
        if self.current_render_layer == "defaultRenderLayer":
            self.sel_button_toggle_override.setEnabled(False)
        else:
            override_attrs = [".intensityMult",".translate",".rotate",".scale"]
            for selected_node in self.selected_nodes:
                for attr in override_attrs:
                    light_shape_found = 0
                    type = cmds.nodeType(selected_node)
                    valid_selection = 0
                    selection_name = ""
                    selection_attr = ""
                    if type == "transform":
                        selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                        for kid in selected_node_kids:
                            kid_type = cmds.nodeType(kid)
                            if kid_type == "VRayLightRectShape":
                                kid_split = kid.split("|")
                                kid_split_size = len(kid_split)
                                selection_name = kid_split[kid_split_size - 1]
                                valid_selection = 1
                                light_shape_found = 1
                    if type == "VRayLightRectShape" or type == "transform":
                        selecton_name = selected_node
                        valid_selection = 1
                    if type == "VRayLightRectShape":
                        if attr == ".intensityMult":
                            selection_attr = selection_name + attr
                            if checked == True and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr)
                                self.sel_button_toggle_override.setText("overrides set")
                                self.sel_button_toggle_override.setFixedHeight(20)
                                self.sel_button_toggle_override.setStyleSheet("QPushButton::checked{background-color: rgb(200, 100, 0);""border:2px solid rgb(200, 100, 0)};")
                            if checked == False and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr,remove = True)
                                self.sel_button_toggle_override.setText("no overrides")
                                self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:0px solid rgb(80, 170, 20)};")
                        if attr == ".translate" or attr == ".rotate" or attr == ".scale":
                            selection_attr = selected_node + attr
                            if checked == True and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr)
                                self.sel_button_toggle_override.setText("overrides set")
                                self.sel_button_toggle_override.setFixedHeight(20)
                                self.sel_button_toggle_override.setStyleSheet("QPushButton::checked{background-color: rgb(200, 100, 0);""border:2px solid rgb(200, 100, 0)};")
                            if checked == False and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr,remove = True)
                                self.sel_button_toggle_override.setText("no overrides")
                                self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:0px solid rgb(80, 170, 20)};")
                                self.sel_button_toggle_override.setFixedHeight(20)
                    if type == "transform" and light_shape_found == 1:
                        if attr == ".intensityMult":
                            selection_attr = selection_name + attr
                            if checked == True and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr)
                                self.sel_button_toggle_override.setText("overrides set")
                                self.sel_button_toggle_override.setFixedHeight(20)
                                self.sel_button_toggle_override.setStyleSheet("QPushButton::checked{background-color: rgb(200, 100, 0);""border:2px solid rgb(200, 100, 0)};")
                            if checked == False and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr,remove = True)
                                self.sel_button_toggle_override.setText("no overrides")
                                self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:0px solid rgb(80, 170, 20)};")
                                self.sel_button_toggle_override.setFixedHeight(20)
                        if attr == ".translate" or attr == ".rotate" or attr == ".scale":
                            selection_attr = selected_node + attr
                            if checked == True and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr)
                                self.sel_button_toggle_override.setText("overrides set")
                                self.sel_button_toggle_override.setFixedHeight(20)
                                self.sel_button_toggle_override.setStyleSheet("QPushButton::checked{background-color: rgb(200, 100, 0);""border:2px solid rgb(200, 100, 0)};")
                            if checked == False and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr,remove = True)
                                self.sel_button_toggle_override.setText("no overrides")
                                self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:0px solid rgb(80, 170, 20)};")
                                self.sel_button_toggle_override.setFixedHeight(20)
                    if type == "transform" and light_shape_found == 0:
                        if attr == ".translate" or attr == ".rotate" or attr == ".scale":
                            selection_attr = selected_node + attr
                            if checked == True and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr)
                                self.sel_button_toggle_override.setText("overrides set")
                                self.sel_button_toggle_override.setFixedHeight(20)
                                self.sel_button_toggle_override.setStyleSheet("QPushButton::checked{background-color: rgb(200, 100, 0);""border:2px solid rgb(200, 100, 0)};")
                            if checked == False and valid_selection == 1:
                                cmds.editRenderLayerAdjustment(selection_attr,remove = True)
                                self.sel_button_toggle_override.setText("no overrides")
                                self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:0px solid rgb(80, 170, 20)};")
                                self.sel_button_toggle_override.setFixedHeight(20)

# a method to to hide all the lights in the scene

    def hide_lights(self,checked):
        panels = cmds.getPanel( type = "modelPanel" )
        if checked == True:
            self.button_show_lights.setText("LIGHTS HIDDEN")
            self.button_show_lights.setFixedHeight(20)
            for mPanel in panels:
                cmds.modelEditor(mPanel, edit = True, lt = 0, lc = 0)
        if checked == False:
            self.button_show_lights.setText("hide lights")
            self.button_show_lights.setFixedHeight(20)
            for mPanel in panels:
                cmds.modelEditor(mPanel, edit = True, lt = 1, lc = 1)

    def Vray_smooth(self,checked):
        selected_objects = cmds.ls(sl = True)
        objects_to_run = []
        for object in selected_objects:
            if 'Shape' in object:
                if object not in objects_to_run:
                    objects_to_run.append(object)
            else:
                object_children = cmds.listRelatives(children = True) or []
                for child in object_children:
                    if 'Shape' in child:
                        if child not in objects_to_run:
                            objects_to_run.append(child)
        for object in objects_to_run:
            node_type = cmds.nodeType(object)
            if node_type == 'mesh':
                if checked == 1:
                    cmds.vray("addAttributesFromGroup", object, "vray_subdivision", 1)
                if checked == 0:
                    cmds.vray("addAttributesFromGroup", object, "vray_subdivision", 0)
        smoothing_exists = 0
        for object in objects_to_run:
            node_type = cmds.nodeType(object)
            if node_type == 'mesh':
                smoothing_exists = cmds.objExists(object + '.vraySubdivUVs')
        if smoothing_exists == 1:
            self.button_Vray_smooth.setChecked(True)
        if smoothing_exists == 0:
            self.button_Vray_smooth.setChecked(False)
                    #self.button_Vray_smooth.setChecked(False)

# a method to detect render layer names and query for render layer overrides

    def render_layers_scan(self):
        self.render_layers = cmds.ls(type = "renderLayer")
        self.current_render_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        render_layer_order_dict = {}
        self.render_layers_in_order = []
        for layer in self.render_layers:
            render_layer_order_number = cmds.getAttr(layer + ".displayOrder")
            render_layer_order_dict[layer] = render_layer_order_number
        number_of_render_layers = 30
        i = 0
        while i <= number_of_render_layers:
            for layer in render_layer_order_dict:
                layer_number = render_layer_order_dict[layer]
                if layer_number == i:
                    self.render_layers_in_order.append(layer)
            i = i + 1
        self.render_layers_in_order.reverse()
        self.render_layers = self.render_layers_in_order
        self.render_layer_overrides = cmds.editRenderLayerAdjustment(self.current_render_layer, query = 1) or []

# a method that detects the current render layer

    def layer_change(self):
        new_current_layer = self.render_layer_QListWidget.currentItem().text()
        if new_current_layer == "masterLayer":
            new_current_layer = "defaultRenderLayer"
        cmds.editRenderLayerGlobals(currentRenderLayer = new_current_layer)

# a method to allow the palette to change render layers and sync the palettes render layer list to the scene's render layer list

    def render_layer_state(self):
        render_layer_mod = "masterLayer"
        self.render_layer_QListWidget.clear()
        render_layer_QListWidget = self.render_layer_QListWidget
        for render_layer in self.render_layers:
            if render_layer == "defaultRenderLayer":
                self.render_layer_QListWidget.addItem(render_layer_mod)
            if render_layer != "defaultRenderLayer":
                self.render_layer_QListWidget.addItem(render_layer)
        i = 0
        render_layer_QListWidget_count = render_layer_QListWidget.count()
        while i < render_layer_QListWidget_count:
            item = render_layer_QListWidget.item(i)
            item_text = item.text()
            if item_text == "masterLayer":
                item_text = "defaultRenderLayer"
            if item_text == self.current_render_layer:
                self.current_render_layer_pointer = item
            i += 1
        render_layer_QListWidget.setCurrentItem(self.current_render_layer_pointer)
        self.render_layer_QListWidget = render_layer_QListWidget
        render_layer_QListWidget.itemClicked.connect(self.layer_change)

# a method that populates the palette window with the tool's buttons

    def populate_window(self):
        self.render_layers_scan()
        self.selected_nodes = cmds.ls(sl = True)
        self.clear_layout(self.grid_layout_top)
        self.lights = cmds.ls(type = "VRayLightRectShape")
        label_all = QtWidgets.QLabel("all")
        label_all.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout_top.addWidget(label_all,0,0)
        label_selected = QtWidgets.QLabel("selected")
        label_selected.setAlignment(QtCore.Qt.AlignCenter)
        self.grid_layout_top.addWidget(label_selected,0,1)
        button_all_off = QtWidgets.QPushButton("off")
        button_all_off.pressed.connect(partial(self.all_toggle_texture_off))
        self.grid_layout_top.addWidget(button_all_off,1,0)
        button_all_on = QtWidgets.QPushButton("on")
        button_all_on.pressed.connect(partial(self.all_toggle_texture_on))
        self.grid_layout_top.addWidget(button_all_on,2,0)
        button_all_toggle = QtWidgets.QPushButton("toggle")
        self.grid_layout_top.addWidget(button_all_toggle,3,0)
        button_all_toggle.pressed.connect(partial(self.all_toggle_texture))
        button_sel_off = QtWidgets.QPushButton("off")
        button_sel_off.pressed.connect(partial(self.selected_toggle_texture_off))
        self.grid_layout_top.addWidget(button_sel_off,1,1)
        button_sel_on = QtWidgets.QPushButton("on")
        button_sel_on.pressed.connect(partial(self.selected_toggle_texture_on))
        self.grid_layout_top.addWidget(button_sel_on,2,1)
        button_sel_toggle = QtWidgets.QPushButton("toggle")
        button_sel_toggle.pressed.connect(partial(self.selected_toggle_texture))
        self.grid_layout_top.addWidget(button_sel_toggle,3,1)
        self.sel_button_toggle_override = QtWidgets.QPushButton("no overrides")
        self.sel_button_toggle_override.setCheckable(True)
        self.sel_button_toggle_override.setEnabled(False)
        self.grid_layout_top.addWidget(self.sel_button_toggle_override,4,0,1,2)
        self.button_show_lights = QtWidgets.QPushButton("hide_lights")
        self.button_show_lights.setFixedHeight(20)
        self.button_show_lights.setCheckable(True)
        self.button_show_lights.toggled.connect(partial(self.hide_lights))
        self.grid_layout_top.addWidget(self.button_show_lights,5,0,1,2)
        self.button_Vray_smooth = QtWidgets.QPushButton("v-ray_smooth")
        self.button_Vray_smooth.setFixedHeight(20)
        self.button_Vray_smooth.setCheckable(True)
        self.button_Vray_smooth.toggled.connect(partial(self.Vray_smooth))
        self.button_Vray_smooth.setStyleSheet("QPushButton::checked{color: rgb(0, 200, 50);""border:1px solid rgb(0, 200, 50)};")
        self.grid_layout_top.addWidget(self.button_Vray_smooth,6,0,1,2)
        render_layers_label = QtWidgets.QLabel("render layers")
        self.grid_layout_top.addWidget(render_layers_label,7,0)
        self.render_layer_QListWidget = QtWidgets.QListWidget()
        self.render_layer_QListWidget.setMinimumHeight(170)
        self.grid_layout_bottom.addWidget(self.render_layer_QListWidget,1,0)
        self.render_layer_state()
        self.populate_attrs()

# a method that enables and deactives, and changes the color and label of the toggle render layer override button

    def populate_attrs(self):
        selected_nodes = cmds.ls(sl = True)
        self.render_layers_scan()
        master_override_found = 0
        master_smoothing_attribute_found = 0
        self.sel_button_toggle_override.setEnabled(False)
        self.sel_button_toggle_override.setFixedHeight(20)
        if self.current_render_layer != "defaultRenderLayer":
            for selected_node in selected_nodes:
                self.selected_node = selected_node
                type = cmds.nodeType(selected_node)
                if type == "VRayLightRectShape":
                    self.sel_button_toggle_override.setEnabled(True)
                    self.sel_button_toggle_override.setFixedHeight(20)
                    for override in self.render_layer_overrides:
                        if selected_node in override:
                            if "intensityMult" in override or "translate" in override or "rotate" in override or "scale" in override:
                                master_override_found = 1
                if type == "transform":
                    self.sel_button_toggle_override.setEnabled(True)
                    self.sel_button_toggle_override.setFixedHeight(20)
                    for override in self.render_layer_overrides:
                        if selected_node in override:
                            if "translate" in override or "rotate" in override or "scale" in override:
                                master_override_found = 1
        if master_override_found == 0:
            self.sel_button_toggle_override.setChecked(False)
            self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(200, 200, 200);""border:0px solid rgb(80, 170, 20)};")
            self.sel_button_toggle_override.setText("no overrides")
            self.sel_button_toggle_override.setFixedHeight(20)
        if master_override_found == 1:
            self.sel_button_toggle_override.setStyleSheet("QPushButton{background-color: rgb(200, 0, 0);""border:2px solid rgb(200,0,0)};")
            self.sel_button_toggle_override.setText("overrides set")
            self.sel_button_toggle_override.setChecked(True)
        self.sel_button_toggle_override.toggled.connect(partial(self.sel_toggle_overrides))
        selected_objects = cmds.ls(sl = True)
        objects_to_run = []
        for object in selected_objects:
            if 'Shape' in object:
                if object not in objects_to_run:
                    objects_to_run.append(object)
            else:
                object_children = cmds.listRelatives(children = True) or []
                for child in object_children:
                    if 'Shape' in child:
                        if child not in objects_to_run:
                            objects_to_run.append(child)
        smoothing_exists = 0
        for object in objects_to_run:
            node_type = cmds.nodeType(object)
            if node_type == 'mesh':
                smoothing_exists = cmds.objExists(object + '.vraySubdivUVs')
        if smoothing_exists == 1:
            self.button_Vray_smooth.setText("vray smoothing on at least one selected node")
            self.button_Vray_smooth.setFont(QtGui.QFont('SansSerif', 8))
            self.button_Vray_smooth.setChecked(True)
            cmds.setAttr("vraySettings.ddisplac_maxSubdivs",6)
        if smoothing_exists == 0:
            self.button_Vray_smooth.setText("no vray smoothing")
            self.button_Vray_smooth.setChecked(False)
# a method that builds the light pallete window and creates the layouts

    def lights_palette_window(self):
        windowName = "lights palatte"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        window.setFixedSize(250,390)
        self.vertical_layout = QtWidgets.QVBoxLayout(mainWidget)
        self.grid_layout_top = QtWidgets.QGridLayout()
        self.vertical_layout.addLayout(self.grid_layout_top)
        self.grid_layout_bottom = QtWidgets.QGridLayout()
        self.vertical_layout.addLayout(self.grid_layout_bottom)
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["NameChanged", self.populate_window])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["renderLayerManagerChange", self.populate_window])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["renderLayerChange", self.populate_window])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SelectionChanged", self.populate_window])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SceneOpened", self.populate_window])
        self.populate_window()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def main():
    ltv = lightsPalette()
    ltv.lights_palette_window()

#main()
