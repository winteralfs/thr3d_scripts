import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class custom_spin_box(QtWidgets.QDoubleSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class lightsPalette():
    def __init__(self):
        self.solo_list_on = []
        self.enabled_light_list_on_list = []
        self.solo_list_on_size = 0
        self.lights = []
        self.transforms_list = []
        self.lights = cmds.ls(type = "VRayLightRectShape")
        self.default_light_attr_values = {}
        self.solo_active_iter = 8
        for light in self.lights:
            self.enabled_val = cmds.getAttr(light + ".enabled")
            key = light + "_enabled"
            self.default_light_attr_values[key] = self.enabled_val        
        
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

    def maya_selection(self):
        self.selected_light_objects = []
        self.selected_light_transform_objects = []
        selected_objects = cmds.ls(sl = True)
        for sel_obj in selected_objects:
            obj_type = cmds.objectType(sel_obj)
            if obj_type == "VRayLightRectShape":
                self.selected_light_objects.append(sel_obj)
            if obj_type == "transform":
                child_objs = cmds.listRelatives(children = True) or []
                for child_obj in child_objs:
                    child_obj_type = cmds.nodeType(child_obj)
                    if child_obj_type == "VRayLightRectShape":
                        if sel_obj not in self.selected_light_transform_objects:
                            self.selected_light_transform_objects.append(sel_obj)
        for light_object in self.selected_light_objects:
            light_label_pointer = self.light_labels_dict[light_object]
            light_label_pointer.setChecked(True)
        for t_object in self.selected_light_transform_objects:
            children = cmds.listRelatives(t_object)
            for child in children:
                child_node_type = cmds.nodeType(child)
                if child_node_type == "VRayLightRectShape":
                    light_label_pointer = self.light_labels_dict[child]
                    light_label_pointer.setChecked(True)

    def default_light_attrs(self):
        self.default_light_link_values = {}
        for light in self.lights:
            self.enabled_val = self.default_light_attr_values[(light + "_enabled")]
            if self.solo_list_on_size == 0:
                if self.solo_active_iter > 7:
                    self.enabled_val = cmds.getAttr(light + ".enabled")
                key = light + "_enabled"
                self.default_light_attr_values[key] = self.enabled_val
            intensityMult_val = cmds.getAttr(light + ".intensityMult")
            key = light + "_intensityMult"
            self.default_light_attr_values[key] = intensityMult_val 

    def populateLights(self):
        self.render_layers_scan()
        self.light_labels_list = []
        self.light_labels_dict = {}
        self.solo_checkbox_list = []
        self.enabled_checkbox_list = []
        self.intensity_multiplier_spinbox_list = []        
        self.clearLayout(self.vertical_layout_lights)
        self.lights = cmds.ls(type = "VRayLightRectShape")
        iter = 0
        for light in self.lights:
            self.horizontal_layout_light = QtWidgets.QHBoxLayout(self.mainWidget)
            self.horizontal_layout_light.setAlignment(QtCore.Qt.AlignRight)
            self.vertical_layout_lights.addLayout(self.horizontal_layout_light)
            light_label = QtWidgets.QPushButton(light)
            light_label.setCheckable(True)        
            light_label.setStyleSheet("QPushButton {background:rgb(69,69,69);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:3px solid rgb(80, 170, 20)};")
            light_label.setFixedWidth(270)
            light_label.setFixedHeight(20)
            light_label.toggled.connect(partial(self.light_label_event,light))
            self.light_labels_dict[light] = light_label
            self.light_labels_list.append(light_label)             
            self.horizontal_layout_light.addWidget(light_label)
            spacer1 = QtWidgets.QLabel("    ")
            self.horizontal_layout_light.addWidget(spacer1)
            self.solo_checkbox = QtWidgets.QCheckBox() 
            self.solo_checkbox_list.append(self.solo_checkbox)            
            self.horizontal_layout_light.addWidget(self.solo_checkbox)
            self.enabled_checkbox = QtWidgets.QCheckBox()            
            self.enabled_checkbox_list.append(self.enabled_checkbox)
            #horizontal_layout_light.addWidget(self.enabled_checkbox)
            self.enabled_checkbox.setEnabled(False)
            enabled_checkbox_value = self.default_light_attr_values[(light + "_enabled")]
            if enabled_checkbox_value == 1 and self.solo_list_on_size == 0:
                self.enabled_checkbox_list[iter].setChecked(1)                        
            spacer2 = QtWidgets.QLabel("    ")
            self.horizontal_layout_light.addWidget(spacer2)
            self.intensity_multiplier_float_spinbox = custom_spin_box()
            self.intensity_multiplier_float_spinbox.setMinimum(-100)
            self.intensity_multiplier_float_spinbox.setMaximum(10000)
            self.intensity_multiplier_float_spinbox.setDecimals(3)
            self.intensity_multiplier_float_spinbox.setSingleStep(.1)
            self.intensity_multiplier_float_spinbox.setFixedWidth(65)
            self.intensity_multiplier_float_spinbox.setKeyboardTracking(False)            
            self.intensity_multiplier_spinbox_list.append(self.intensity_multiplier_float_spinbox)            
            self.horizontal_layout_light.addWidget(self.intensity_multiplier_float_spinbox)
            iter = iter + 1                       
        self.populate_attrs()        
        self.maya_selection()

    def populate_attrs(self):
        self.default_light_attrs()
        self.renderLayers_combobox.clear()
        for render_layer in self.render_layers:
            self.renderLayers_combobox.addItem(render_layer)
        l = 0
        for layer in self.render_layers:
            if layer == self.current_render_layer:
                self.renderLayers_combobox.setCurrentIndex(l)
            l = l + 1
        self.renderLayers_combobox.activated[str].connect(lambda:self.render_layer_state())
        iter = 0
        for light in self.lights:
            if light in self.solo_list_on:
                self.solo_checkbox_list[iter].setChecked(1)
            self.solo_checkbox_list[iter].stateChanged.connect(lambda:self.solo_checkbox_state())
            enabled_checkbox_value = self.default_light_attr_values[(light + "_enabled")]
            if enabled_checkbox_value == 1 and self.solo_list_on_size == 0:
                self.enabled_checkbox_list[iter].setChecked(1)
            self.enabled_checkbox_list[iter].stateChanged.connect(lambda:self.enabled_checkbox_state())
            if self.solo_list_on_size == 0:
                self.enabled_checkbox_list[iter].setEnabled(True)
                cmds.setAttr((light + ".enabled"), lock = False)
            intensity_multiplier_float_spinbox_value = self.default_light_attr_values[(light + "_intensityMult")]
            self.intensity_multiplier_spinbox_list[iter].setValue(intensity_multiplier_float_spinbox_value)
            self.intensity_multiplier_spinbox_list[iter].valueChanged.connect(lambda:self.intensity_mult_float_spinbox_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "intensityMult" in override:
                        intensity_multiplier_spinbox_list_pal = self.intensity_multiplier_spinbox_list[iter].palette()
                        intensity_multiplier_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.intensity_multiplier_spinbox_list[iter].setPalette(intensity_multiplier_spinbox_list_pal)
                        self.intensity_multiplier_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if light not in override:
                    self.intensity_multiplier_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            iter = iter + 1
        selected_objects = cmds.ls(sl = True)

    def solo_checkbox_state(self):
        self.solo_active_iter = 0
        light_solo_dict = {}
        self.solo_list_on = []
        iter = 0
        for lgt in self.lights:
            cmds.setAttr((lgt + ".enabled"), lock = False)
        for solo in self.solo_checkbox_list:
            state = solo.isChecked()
            light = self.lights[iter]
            light_solo_dict[light] = state
            iter = iter + 1
        for lgt in self.lights:
            val = light_solo_dict[lgt]
            if val == 0:
                cmds.setAttr((lgt + ".enabled"),val)
                cmds.setAttr(lgt + ".visibility",0)
            if val == 1:
                cmds.setAttr((lgt + ".enabled"),val)
                cmds.setAttr(lgt + ".visibility",1)
                self.solo_list_on.append(lgt)
        self.solo_list_on_size = len(self.solo_list_on)
        for cb in self.enabled_checkbox_list:
            cb.setEnabled(False)
        for lgt in self.lights:
            cmds.setAttr((lgt + ".enabled"), lock = True)
        if self.solo_list_on_size == 0:
            for light in self.lights:
                cmds.setAttr(light + ".visibility",1)
                cmds.setAttr((light + ".enabled"),lock = False)
                val = self.default_light_attr_values[light + "_enabled"]
                cmds.setAttr((light + ".enabled"),val)

    def enabled_checkbox_state(self):
        iter = 0
        self.enabled_light_list_on_list = []
        self.solo_list_on_size = len(self.solo_list_on)
        for checkbox in self.enabled_checkbox_list:
            state = checkbox.isChecked()
            light = self.lights[iter]
            cmds.setAttr((light + ".enabled"),state)
            iter = iter + 1
        self.default_light_attrs()

    def intensity_mult_float_spinbox_state(self):
        iter = 0
        for spinbox in self.intensity_multiplier_spinbox_list:
            value = spinbox.value()
            light = self.lights[iter]
            cmds.setAttr((light + ".intensityMult"),value)
            iter = iter + 1

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

    def light_label_event(self,light,checked):
        for lght in self.lights:
            if lght == light:
                light_parent = cmds.listRelatives(lght,parent = True)
                if checked == True:
                    cmds.select(light_parent,add = True)
                if checked == False:
                    cmds.select(lght,deselect = True)
                    cmds.select(light_parent,deselect = True)
     
    def lightsTextureView(self):
        windowName = "LTV"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        self.mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(self.mainWidget)
        window.setFixedSize(450,550)
        self.vertical_layout_main = QtWidgets.QVBoxLayout(self.mainWidget)
        self.grid_layout = QtWidgets.QGridLayout(self.mainWidget)
        self.vertical_layout_main.addLayout(self.grid_layout)
        button_width = 210
        button_height = 20
        label_all = QtWidgets.QLabel("all")
        label_all.setAlignment(QtCore.Qt.AlignCenter)    
        self.grid_layout.addWidget(label_all,0,0)
        label_selected = QtWidgets.QLabel("selected")
        label_selected.setAlignment(QtCore.Qt.AlignCenter)  
        self.grid_layout.addWidget(label_selected,0,1)
        button_all_off = QtWidgets.QPushButton("light ramp texture off")
        button_all_off.setFixedWidth(button_width)
        button_all_off.setFixedHeight(button_height)
        button_all_off.pressed.connect(partial(self.allToggleTexture_off))
        self.grid_layout.addWidget(button_all_off,1,0) 
        button_all_on = QtWidgets.QPushButton("light ramp texture on")
        button_all_on.setFixedWidth(button_width)
        button_all_on.setFixedHeight(button_height)
        button_all_on.pressed.connect(partial(self.allToggleTexture_on))
        self.grid_layout.addWidget(button_all_on,2,0)
        button_all_toggle = QtWidgets.QPushButton("light ramp texture toggle")
        self.grid_layout.addWidget(button_all_toggle,3,0)
        button_all_toggle.setFixedWidth(button_width)
        button_all_toggle.setFixedHeight(button_height)
        button_all_toggle.pressed.connect(partial(self.allToggleTexture))
        button_sel_off = QtWidgets.QPushButton("light ramp texture off")
        button_sel_off.setFixedWidth(button_width)
        button_sel_off.setFixedHeight(button_height)
        button_sel_off.pressed.connect(partial(self.selectedToggleTexture_off))         
        self.grid_layout.addWidget(button_sel_off,1,1)
        button_sel_on = QtWidgets.QPushButton("light ramp texture on")
        button_sel_on.setFixedWidth(button_width)
        button_sel_on.setFixedHeight(button_height)
        button_sel_on.pressed.connect(partial(self.selectedToggleTexture_on))       
        self.grid_layout.addWidget(button_sel_on,2,1)
        button_sel_toggle = QtWidgets.QPushButton("light ramp texture toggle")
        button_sel_toggle.setFixedWidth(button_width)
        button_sel_toggle.setFixedHeight(button_height)
        button_sel_toggle.pressed.connect(partial(self.selectedToggleTexture))     
        self.grid_layout.addWidget(button_sel_toggle,3,1)
        self.button_show_lights = QtWidgets.QPushButton("hide_lights")
        self.button_show_lights.setFixedHeight(20)
        self.button_show_lights.setCheckable(True)
        self.button_show_lights.toggled.connect(partial(self.hideLights))
        self.button_show_lights.setStyleSheet("QPushButton::checked{color: rgb(249, 0, 0);""border:1px solid rgb(249, 0, 0)};")
        self.grid_layout.addWidget(self.button_show_lights,4,0,1,2)
        light_title = QtWidgets.QLabel("                                           lights    ")
        self.grid_layout.addWidget(light_title) 
        solo_title = QtWidgets.QLabel("                            solo            int")
        self.grid_layout.addWidget(solo_title)
        self.horizontal_light_layout = QtWidgets.QHBoxLayout(self.mainWidget)
        self.horizontal_light_layout.setAlignment(QtCore.Qt.AlignLeft) 
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.vertical_layout_main.addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll.setWidget(self.scroll_widget)
        self.vertical_layout_lights = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.vertical_layout_main.addLayout(self.vertical_layout_lights)
        self.vertical_layout_lights.setAlignment(QtCore.Qt.AlignTop)
        self.horizontal_layout_bottom = QtWidgets.QHBoxLayout(self.mainWidget)   
        self.vertical_layout_main.addLayout(self.horizontal_layout_bottom)
        self.renderLayers_combobox = QtWidgets.QComboBox()
        self.renderLayers_combobox.setMaximumWidth(250)
        self.renderLayers_combobox.setMinimumHeight(20)
        self.horizontal_layout_bottom.setAlignment(QtCore.Qt.AlignLeft)
        self.horizontal_layout_bottom.addWidget(self.renderLayers_combobox)  
        exp_list = []
        self.light_attrs = ["enabled","intensityMult"]
        for light in self.lights:
            for attr in self.light_attrs:
                string = light + "." + attr
                exp_list.append(string)                
        for exp in exp_list:
            self.myScriptJobID = cmds.scriptJob(p = windowName, attributeChange=[exp, self.populateLights])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["renderLayerManagerChange", self.populateLights])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["renderLayerChange", self.populateLights])
        #self.myScriptJobID = cmds.scriptJob(p = windowName, event=["idleVeryLow", self.populateLights])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SelectionChanged", self.populateLights])
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SceneOpened", self.populateLights])                  
        self.default_light_attrs()
        self.populateLights()
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()
 
ltv = lightsPalette()
ltv.lightsTextureView()