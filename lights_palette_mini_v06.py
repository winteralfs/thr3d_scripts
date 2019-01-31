import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class lightsPalette():
    def __init__(self):
        self.lights = []
        self.lights = cmds.ls(type = "VRayLightRectShape")

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())    

    def render_layers_scan(self):
        self.render_layers = cmds.ls(type = "renderLayer")
        self.current_render_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        self.render_layer_overrides = cmds.editRenderLayerAdjustment(self.current_render_layer, query = 1) or []

    def render_layer_state(self):
        chosen_layer = self.renderLayers_combobox.currentText()
        cmds.editRenderLayerGlobals(currentRenderLayer = chosen_layer)          
    
    def allToggleTexture_off(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 0)
     
    def selectedToggleTexture_off(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 0)
     
    def allToggleTexture_on(self):
        all_nodes = cmds.ls(transforms = True)
        for all_node in all_nodes:
            type = cmds.nodeType(all_node)
            if type == "transform":
                all_node_kids = cmds.listRelatives(all_node,children = True,fullPath = True) or []
                for kid in all_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 1)
     
    def selectedToggleTexture_on(self):
        selected_nodes = cmds.ls(sl = True)
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "transform":
                selected_node_kids = cmds.listRelatives(selected_node,children = True,fullPath = True) or []
                for kid in selected_node_kids:
                    type = cmds.nodeType(kid)
                    if type == "VRayLightRectShape":
                        cmds.setAttr(kid + ".showTex", 1)
     
    def allToggleTexture(self):
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
     
    def selectedToggleTexture(self):
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

    def hideLights(self,checked):
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

    def sel_toggleOverrides(self,checked):
        tmp_sel = cmds.ls(sl = True)
        self.renderLayers_combobox.clear()
        for render_layer in self.render_layers:
            self.renderLayers_combobox.addItem(render_layer)
        l = 0
        for layer in self.render_layers:
            if layer == self.current_render_layer:
                self.renderLayers_combobox.setCurrentIndex(l)
            l = l + 1
        self.renderLayers_combobox.activated[str].connect(lambda:self.render_layer_state())
        if self.current_render_layer == "defaultRenderLayer":
            self.sel_button_toggle_override.setEnabled(False)
        else:   
            override_attrs = [".intensityMult",".translate",".rotate",".scale"]
            for attr in override_attrs:
                for selected_node in self.selected_nodes:
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
                                self.sel_button_toggle_override.setFixedHeight(20)                  
                            self.render_layers_scan()
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
                            self.render_layers_scan()
                    if type == "transform" and light_shape_found == 1:
                        if attr == ".intensityMult":
                            selection_attr = selection_name + attr           
                            print selection_attr
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
                            self.render_layers_scan()
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
                            self.render_layers_scan()                        
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
                            self.render_layers_scan()
        for sel in tmp_sel:
            cmds.select(sel,add = True)     
            
    def all_toggleOverrides(self):       
        self.all_checked = 1
        tmp_sel = cmds.ls(sl = True)
        self.renderLayers_combobox.clear()
        for render_layer in self.render_layers:
            self.renderLayers_combobox.addItem(render_layer)
        l = 0
        for layer in self.render_layers:
            if layer == self.current_render_layer:
                self.renderLayers_combobox.setCurrentIndex(l)
            l = l + 1
        self.renderLayers_combobox.activated[str].connect(lambda:self.render_layer_state())
        if self.current_render_layer == "defaultRenderLayer":
            self.all_button_toggle_override.setEnabled(False)
        else:   
            override_attrs = [".intensityMult",".translate",".rotate",".scale"]
            for attr in override_attrs:
                for selected_node in self.lights:
                    type = cmds.nodeType(selected_node)
                    valid_selection = 1
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
                                if selection_name in self.render_layer_overrides:
                                    self.all_checked = 0
                    if type == "VRayLightRectShape":
                        selecton_name = selected_node     
                        valid_selection = 1
                        selected_node_parent = cmds.listRelatives(selected_node,parent = True,fullPath = True) or []
                        selected_node_parent_list = []
                        override_split_list = [] 
                        override_list = []                        
                        selected_node_parent_split = selected_node_parent[0].split("|")
                        for item in selected_node_parent_split:
                            if item not in selected_node_parent_list:
                                selected_node_parent_list.append(item)
                        for override in self.render_layer_overrides:
                            override_split_list = override.split(".")
                            for item in override_split_list:                                
                                if item not in override_list:
                                    if item != "translate" or item != "rotate" or item != "scale" or item != "intensityMult": 
                                        override_list.append(item)                                                                                
                        for selected_parent in selected_node_parent_list:                            
                            if selected_parent in override_list:
                                self.all_checked = 0
            for attr in override_attrs:
                for selected_node in self.lights:
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
                    if type == "VRayLightRectShape":
                        selecton_name = selected_node     
                        valid_selection = 1
                        selected_node_parent = cmds.listRelatives(selected_node,parent = True,fullPath = True) or []
                    if attr == ".intensityMult":
                        selection_attr = selected_node_parent[0] + attr           
                        if self.all_checked == 1 and valid_selection == 1:
                            cmds.editRenderLayerAdjustment(selection_attr)
                            self.all_button_toggle_override.setFixedHeight(20)                          
                        if self.all_checked == 0 and valid_selection == 1:
                            cmds.editRenderLayerAdjustment(selection_attr,remove = True)
                            self.all_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(200, 200, 200);""border:0px solid rgb(80, 170, 20)};")
                            self.all_button_toggle_override.setFixedHeight(20)                  
                        self.render_layers_scan()
                    if attr == ".translate" or attr == ".rotate" or attr == ".scale":
                        selection_attr = selected_node_parent[0] + attr      
                        if self.all_checked == 1 and valid_selection == 1:
                            cmds.editRenderLayerAdjustment(selection_attr)
                            self.all_button_toggle_override.setFixedHeight(20)
                        if self.all_checked == 0 and valid_selection == 1:
                            cmds.editRenderLayerAdjustment(selection_attr,remove = True)
                            self.all_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(200, 200, 200);""border:0px solid rgb(80, 170, 20)};")
                            self.all_button_toggle_override.setFixedHeight(20)                  
                        self.render_layers_scan()
        for sel in tmp_sel:
            cmds.select(sel,add = True)            
     
    def populateLights(self):
        self.render_layers_scan()
        self.selected_nodes = cmds.ls(sl = True)
        self.clearLayout(self.grid_layout)
        self.lights = cmds.ls(type = "VRayLightRectShape")
        label_all = QtWidgets.QLabel("all")
        label_all.setAlignment(QtCore.Qt.AlignCenter)    
        self.grid_layout.addWidget(label_all,0,0)
        label_selected = QtWidgets.QLabel("selected")
        label_selected.setAlignment(QtCore.Qt.AlignCenter)  
        self.grid_layout.addWidget(label_selected,0,1)
        button_all_off = QtWidgets.QPushButton("off")
        button_all_off.pressed.connect(partial(self.allToggleTexture_off))
        self.grid_layout.addWidget(button_all_off,1,0)
        button_all_on = QtWidgets.QPushButton("on")
        button_all_on.pressed.connect(partial(self.allToggleTexture_on))
        self.grid_layout.addWidget(button_all_on,2,0)
        button_all_toggle = QtWidgets.QPushButton("toggle")
        self.grid_layout.addWidget(button_all_toggle,3,0)
        button_all_toggle.pressed.connect(partial(self.allToggleTexture))
        button_sel_off = QtWidgets.QPushButton("off")
        button_sel_off.pressed.connect(partial(self.selectedToggleTexture_off))         
        self.grid_layout.addWidget(button_sel_off,1,1)
        button_sel_on = QtWidgets.QPushButton("on")
        button_sel_on.pressed.connect(partial(self.selectedToggleTexture_on))       
        self.grid_layout.addWidget(button_sel_on,2,1)
        button_sel_toggle = QtWidgets.QPushButton("toggle")
        button_sel_toggle.pressed.connect(partial(self.selectedToggleTexture))     
        self.grid_layout.addWidget(button_sel_toggle,3,1)
        self.all_button_toggle_override = QtWidgets.QPushButton("toggle overrides")
        self.all_button_toggle_override.setFixedHeight(20)
        self.all_button_toggle_override.setCheckable(True)
        self.all_button_toggle_override.pressed.connect(partial(self.all_toggleOverrides))
        self.grid_layout.addWidget(self.all_button_toggle_override,4,0)  
        self.sel_button_toggle_override = QtWidgets.QPushButton("no overrides")
        self.sel_button_toggle_override.setCheckable(True)
        self.sel_button_toggle_override.toggled.connect(partial(self.sel_toggleOverrides))
        self.sel_button_toggle_override.setEnabled(False)
        self.grid_layout.addWidget(self.sel_button_toggle_override,4,1)  
        self.button_show_lights = QtWidgets.QPushButton("hide_lights")
        self.button_show_lights.setFixedHeight(20)
        self.button_show_lights.setCheckable(True)
        self.button_show_lights.toggled.connect(partial(self.hideLights))
        self.button_show_lights.setStyleSheet("QPushButton::checked{color: rgb(249, 0, 0);""border:1px solid rgb(249, 0, 0)};")
        self.grid_layout.addWidget(self.button_show_lights,5,0,1,2)      
        self.renderLayers_combobox = QtWidgets.QComboBox()
        self.renderLayers_combobox.setMaximumWidth(150)
        self.renderLayers_combobox.setMinimumHeight(20)
        self.grid_layout.addWidget(self.renderLayers_combobox,6,0,1,2)         
        self.populate_attrs()
        for sel in self.selected_nodes:
            cmds.select(sel,add = True) 

    def populate_attrs(self):
        self.renderLayers_combobox.clear()
        for render_layer in self.render_layers:
            self.renderLayers_combobox.addItem(render_layer)
        l = 0
        for layer in self.render_layers:
            if layer == self.current_render_layer:
                self.renderLayers_combobox.setCurrentIndex(l)
            l = l + 1
        self.renderLayers_combobox.activated[str].connect(lambda:self.render_layer_state())
        selected_nodes = cmds.ls(sl = True)
        self.render_layers_scan()
        for selected_node in selected_nodes:
            type = cmds.nodeType(selected_node)
            if type == "VRayLightRectShape":     
                overide_found = 0
                self.all_button_toggle_override.setEnabled(True) 
                self.sel_button_toggle_override.setEnabled(True)                                                 
                if self.current_render_layer != "defaultRenderLayer":
                    for override in self.render_layer_overrides:
                        if selected_node in override:
                            if "intensityMult" in override or "translate" in override or "rotate" in override or "scale" in override:
                                overide_found = 1
                                self.sel_button_toggle_override.setStyleSheet("QPushButton{background-color: rgb(200, 100, 0);""border:2px solid rgb(200, 100, 0)};")    
                                self.sel_button_toggle_override.setText("overrides set")        
                                self.sel_button_toggle_override.setFixedHeight(20)                      
                                self.sel_button_toggle_override.setChecked(True)                                       
                    if overide_found == 0:
                        self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(200, 200, 200);""border:0px solid rgb(80, 170, 20)};")
                        self.sel_button_toggle_override.setText("no overrides")   
                        self.sel_button_toggle_override.setFixedHeight(20)
                        self.sel_button_toggle_override.setChecked(False) 
                        self.all_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(200, 200, 200);""border:0px solid rgb(80, 170, 20)};")
                        self.all_button_toggle_override.setFixedHeight(20)
                        self.all_button_toggle_override.setChecked(False)                                                                         
                if self.current_render_layer == "defaultRenderLayer":
                    self.sel_button_toggle_override.setEnabled(False)
            if type == "transform":     
                overide_found = 0
                self.all_button_toggle_override.setEnabled(True) 
                self.sel_button_toggle_override.setEnabled(True)                                                 
                if self.current_render_layer != "defaultRenderLayer":
                    for override in self.render_layer_overrides:
                        if selected_node in override:
                            if "translate" in override or "rotate" in override or "scale" in override:
                                overide_found = 1
                                self.sel_button_toggle_override.setStyleSheet("QPushButton{background-color: rgb(200, 100, 0);""border:2px solid rgb(200, 100, 0)};")    
                                self.sel_button_toggle_override.setText("overrides set")        
                                self.sel_button_toggle_override.setFixedHeight(20)                      
                                self.sel_button_toggle_override.setChecked(True)                                       
                    if overide_found == 0:
                        self.sel_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(200, 200, 200);""border:0px solid rgb(80, 170, 20)};")
                        self.sel_button_toggle_override.setText("no overrides")   
                        self.sel_button_toggle_override.setFixedHeight(20)
                        self.sel_button_toggle_override.setChecked(False) 
                        self.all_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(200, 200, 200);""border:0px solid rgb(80, 170, 20)};")
                        self.all_button_toggle_override.setFixedHeight(20)
                        self.all_button_toggle_override.setChecked(False)                                                                         
                if self.current_render_layer == "defaultRenderLayer":
                    self.sel_button_toggle_override.setEnabled(False)
        num_of_lights = len(self.lights)
        overrides_split_list = []
        for override in self.render_layer_overrides:
            override_split = override.split(".")
            overrides_split_list.append(override_split[0])
        count = 0
        for light in self.lights:
            if light in overrides_split_list:
                count = count + 1 
        if count == num_of_lights:
            self.all_button_toggle_override.setStyleSheet("QPushButton {background:rgb(100,100,100);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:0px solid rgb(80, 170, 20)};")
            self.all_button_toggle_override.setFixedHeight(20)
            self.all_button_toggle_override.setChecked(True)  
        if self.current_render_layer == "defaultRenderLayer":
            self.all_button_toggle_override.setEnabled(False)            

    def lightsTextureView(self):
        windowName = "OLP"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        window.setFixedSize(250,200)
        self.grid_layout = QtWidgets.QGridLayout(mainWidget)
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["renderLayerManagerChange", self.populateLights])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["renderLayerChange", self.populateLights])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SelectionChanged", self.populateLights])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SceneOpened", self.populateLights])
        self.populateLights()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()
        
ltv = lightsPalette()
ltv.lightsTextureView()