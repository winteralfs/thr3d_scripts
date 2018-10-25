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

class lights_palette():
    def __init__(self):
        #print " "
        #print "*init*"
        self.wdth_compare = 0
        self.showTex_label_button_pressed = 0
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

    def render_layers_scan(self):
        self.render_layers = cmds.ls(type = "renderLayer")
        self.current_render_layer = cmds.editRenderLayerGlobals(query=True, currentRenderLayer=True)
        self.render_layer_overrides = cmds.editRenderLayerAdjustment(self.current_render_layer, query = 1) or []

    def render_layer_state(self):
        chosen_layer = self.renderLayers_combobox.currentText()
        cmds.editRenderLayerGlobals(currentRenderLayer = chosen_layer)

    def default_light_attrs(self):
        #print " "
        self.default_light_link_values = {}
        self.lights = cmds.ls(type = "VRayLightRectShape")
        for transform in self.transforms_list:
            translateX_val = cmds.getAttr(transform + ".translateX")
            key = transform + "_translateX"
            self.default_light_attr_values[key] = translateX_val
            translateY_val = cmds.getAttr(transform + ".translateY")
            key = transform + "_translateY"
            self.default_light_attr_values[key] = translateY_val
            translateZ_val = cmds.getAttr(transform + ".translateZ")
            key = transform + "_translateZ"
            self.default_light_attr_values[key] = translateZ_val
            rotateX_val = cmds.getAttr(transform + ".rotateX")
            key = transform + "_rotateX"
            self.default_light_attr_values[key] = rotateX_val
            rotateY_val = cmds.getAttr(transform + ".rotateY")
            key = transform + "_rotateY"
            self.default_light_attr_values[key] = rotateY_val
            rotateZ_val = cmds.getAttr(transform + ".rotateZ")
            key = transform + "_rotateZ"
            self.default_light_attr_values[key] = rotateZ_val
        for light in self.lights:
            self.enabled_val = self.default_light_attr_values[(light + "_enabled")]
            if self.solo_list_on_size == 0:
                if self.solo_active_iter > 7:
                    self.enabled_val = cmds.getAttr(light + ".enabled")
                key = light + "_enabled"
                self.default_light_attr_values[key] = self.enabled_val

            light_color_val = cmds.getAttr(light + ".lightColor")
            key = light + "_lightColor"
            self.default_light_attr_values[key] = light_color_val

            intensityMult_val = cmds.getAttr(light + ".intensityMult")
            key = light + "_intensityMult"
            self.default_light_attr_values[key] = intensityMult_val
            uSize_val = cmds.getAttr(light + ".uSize")
            key = light + "_uSize"
            self.default_light_attr_values[key] = uSize_val
            vSize_val = cmds.getAttr(light + ".vSize")
            key = light + "_vSize"
            self.default_light_attr_values[key] = vSize_val
            directional_val = cmds.getAttr(light + ".directional")
            key = light + "_directional"
            self.default_light_attr_values[key] = directional_val
            useRectTex_val = cmds.getAttr(light + ".useRectTex")
            key = light + "_useRectText"
            self.default_light_attr_values[key] = useRectTex_val

            rectTex_val = cmds.getAttr(light + ".rectTex")
            key = light + "_rectTex"
            self.default_light_attr_values[key] = rectTex_val

            showTex_val = cmds.getAttr(light + ".showTex")
            key = light + "_showTex"
            self.default_light_attr_values[key] = showTex_val
            affect_diffuse_val = cmds.getAttr(light + ".affectDiffuse")
            key = light + "_affectDiffuse"
            self.default_light_attr_values[key] = affect_diffuse_val
            contribute_diffuse_val = cmds.getAttr(light + ".diffuseContrib")
            key = light + "_diffuseContrib"
            self.default_light_attr_values[key] = contribute_diffuse_val
            affect_specular_val = cmds.getAttr(light + ".affectSpecular")
            key = light + "_affectSpecular"
            self.default_light_attr_values[key] = affect_specular_val
            contribute_specular_val = cmds.getAttr(light + ".specularContrib")
            key = light + "_specularContrib"
            self.default_light_attr_values[key] = contribute_specular_val
            affect_reflections_val = cmds.getAttr(light + ".affectReflections")
            key = light + "_affectReflections"
            self.default_light_attr_values[key] = affect_reflections_val
            self.light_linking_line_edit_list_val = cmds.lightlink(query = True, light = light)
            key = light + "&light_linking"
            self.default_light_link_values[key] = self.light_linking_line_edit_list_val
        self.solo_active_iter = self.solo_active_iter + 1
        #print " "

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())

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

    def populate_lights(self):
        #print " "
        #print "*populate lights*"
        self.render_layers_scan()
        self.light_labels_list = []
        self.light_labels_dict = {}
        self.solo_checkbox_list = []
        self.light_link_dict = {}
        self.translateX_spinbox_list = []
        self.translateY_spinbox_list = []
        self.translateZ_spinbox_list = []
        self.rotateX_spinbox_list = []
        self.rotateY_spinbox_list = []
        self.rotateZ_spinbox_list = []
        self.enabled_checkbox_list = []
        self.light_color_pushbutton_list = []
        self.intensity_multiplier_spinbox_list = []
        self.uSize_spinbox_list = []
        self.vSize_spinbox_list = []
        self.directional_spinbox_list = []
        self.useRectText_checkbox_list = []
        self.rect_tex_push_button_list = []
        self.showTex_combo_box_list = []
        self.affect_diffuse_checkbox_list = []
        self.diffuse_contribution_spinbox_list = []
        self.affect_specular_checkbox_list = []
        self.specular_contribution_spinbox_list = []
        self.affect_reflections_checkbox_list = []
        self.light_linking_line_edit_list = []
        iter = 0
        self.clearLayout(self.vertical_layout_lights)
        for light in self.lights:
            horizontal_layout_light = QtWidgets.QHBoxLayout(self.mainWidget)
            horizontal_layout_light.setAlignment(QtCore.Qt.AlignRight)
            horizontal_layout_light.setSpacing(17)
            self.vertical_layout_lights.addLayout(horizontal_layout_light)
            self.light_label = QtWidgets.QPushButton(light)
            self.light_label.setFixedHeight(20)
            self.light_labels_dict[light] = self.light_label
            self.light_labels_list.append(self.light_label)
            self.light_label.setStyleSheet("QPushButton {background:rgb(65,66,66);} QPushButton::checked{background-color: rgb(100, 100, 100);""border:3px solid rgb(80, 170, 20)};")
            self.light_label.setFont(QtGui.QFont("SansSerif", 8))
            self.light_label.setCheckable(True)
            self.light_label.toggled.connect(partial(self.light_label_event,light))
            horizontal_layout_light.addWidget(self.light_label)
            horizontal_layout_light.addStretch(1)
            self.solo_checkbox = QtWidgets.QCheckBox()
            self.solo_checkbox_list.append(self.solo_checkbox)
            horizontal_layout_light.addWidget(self.solo_checkbox)
            self.enabled_checkbox = QtWidgets.QCheckBox()
#--
            self.tx_float_spinbox = custom_spin_box()
            self.translateX_spinbox_list.append(self.tx_float_spinbox)
            self.tx_float_spinbox.setMinimum(-100)
            self.tx_float_spinbox.setMaximum(10000)
            self.tx_float_spinbox.setDecimals(3)
            self.tx_float_spinbox.setSingleStep(.1)
            self.tx_float_spinbox.setFixedWidth(65)
            self.translateX_spinbox_list[iter].setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.tx_float_spinbox)
            self.ty_float_spinbox = custom_spin_box()
            self.translateY_spinbox_list.append(self.ty_float_spinbox)
            self.ty_float_spinbox.setMinimum(-100)
            self.ty_float_spinbox.setMaximum(10000)
            self.ty_float_spinbox.setDecimals(3)
            self.ty_float_spinbox.setSingleStep(.1)
            self.ty_float_spinbox.setFixedWidth(65)
            self.translateY_spinbox_list[iter].setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.ty_float_spinbox)
            self.tz_float_spinbox = custom_spin_box()
            self.translateZ_spinbox_list.append(self.tz_float_spinbox)
            self.tz_float_spinbox.setMinimum(-100)
            self.tz_float_spinbox.setMaximum(10000)
            self.tz_float_spinbox.setDecimals(3)
            self.tz_float_spinbox.setSingleStep(.1)
            self.tz_float_spinbox.setFixedWidth(65)
            self.translateZ_spinbox_list[iter].setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.tz_float_spinbox)
            self.rx_float_spinbox = custom_spin_box()
            self.rotateX_spinbox_list.append(self.rx_float_spinbox)
            self.rx_float_spinbox.setMinimum(-100)
            self.rx_float_spinbox.setMaximum(10000)
            self.rx_float_spinbox.setDecimals(3)
            self.rx_float_spinbox.setSingleStep(.1)
            self.rx_float_spinbox.setFixedWidth(65)
            self.rotateX_spinbox_list[iter].setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.rx_float_spinbox)
            self.ry_float_spinbox = custom_spin_box()
            self.rotateY_spinbox_list.append(self.ry_float_spinbox)
            self.ry_float_spinbox.setMinimum(-100)
            self.ry_float_spinbox.setMaximum(10000)
            self.ry_float_spinbox.setDecimals(3)
            self.ry_float_spinbox.setSingleStep(.1)
            self.ry_float_spinbox.setFixedWidth(65)
            self.rotateY_spinbox_list[iter].setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.ry_float_spinbox)
            self.rz_float_spinbox = custom_spin_box()
            self.rotateZ_spinbox_list.append(self.rz_float_spinbox)
            self.rz_float_spinbox.setMinimum(-100)
            self.rz_float_spinbox.setMaximum(10000)
            self.rz_float_spinbox.setDecimals(3)
            self.rz_float_spinbox.setSingleStep(.1)
            self.rz_float_spinbox.setFixedWidth(65)
            self.rotateZ_spinbox_list[iter].setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.rz_float_spinbox)
#--
            self.enabled_checkbox_list.append(self.enabled_checkbox)
            horizontal_layout_light.addWidget(self.enabled_checkbox)
            self.enabled_checkbox.setEnabled(False)
            enabled_checkbox_value = self.default_light_attr_values[(light + "_enabled")]
            if enabled_checkbox_value == 1 and self.solo_list_on_size == 0:
                self.enabled_checkbox_list[iter].setChecked(1)
            self.light_color_pushbutton = QtWidgets.QPushButton()
            self.light_color_pushbutton_list.append(self.light_color_pushbutton)
            self.light_color_pushbutton.setMinimumWidth(30)
            self.light_color_pushbutton.setMaximumWidth(30)
            self.light_color_pushbutton.setMinimumHeight(30)
            self.light_color_pushbutton.setMaximumHeight(30)
            self.light_color_pushbutton.clicked.connect(partial(self.light_color_state,light))
            horizontal_layout_light.addWidget(self.light_color_pushbutton)
            self.intensity_multiplier_float_spinbox = custom_spin_box()
            self.intensity_multiplier_spinbox_list.append(self.intensity_multiplier_float_spinbox)
            self.intensity_multiplier_float_spinbox.setMinimum(-100)
            self.intensity_multiplier_float_spinbox.setMaximum(10000)
            self.intensity_multiplier_float_spinbox.setDecimals(3)
            self.intensity_multiplier_float_spinbox.setSingleStep(.1)
            self.intensity_multiplier_float_spinbox.setFixedWidth(65)
            self.intensity_multiplier_spinbox_list[iter].setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.intensity_multiplier_float_spinbox)
            self.uSize_float_spinbox = custom_spin_box()
            self.uSize_spinbox_list.append(self.uSize_float_spinbox)
            self.uSize_float_spinbox.setMinimum(0)
            self.uSize_float_spinbox.setMaximum(10000)
            self.uSize_float_spinbox.setDecimals(3)
            self.uSize_float_spinbox.setSingleStep(.1)
            self.uSize_float_spinbox.setFixedWidth(65)
            self.uSize_float_spinbox.setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.uSize_float_spinbox)
            self.vSize_float_spinbox = custom_spin_box()
            self.vSize_spinbox_list.append(self.vSize_float_spinbox)
            self.vSize_float_spinbox.setMinimum(0)
            self.vSize_float_spinbox.setMaximum(10000)
            self.vSize_float_spinbox.setDecimals(3)
            self.vSize_float_spinbox.setSingleStep(.1)
            self.vSize_float_spinbox.setFixedWidth(65)
            self.vSize_float_spinbox.setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.vSize_float_spinbox)
            self.directional_float_spinbox = custom_spin_box()
            self.directional_spinbox_list.append(self.directional_float_spinbox)
            self.directional_float_spinbox.setMinimum(0)
            self.directional_float_spinbox.setMaximum(1)
            self.directional_float_spinbox.setDecimals(3)
            self.directional_float_spinbox.setSingleStep(.1)
            self.directional_float_spinbox.setFixedWidth(65)
            self.directional_float_spinbox.setKeyboardTracking(False)
            horizontal_layout_light.addWidget(self.directional_float_spinbox)
            self.useRectText_checkbox = QtWidgets.QCheckBox()
            horizontal_layout_light.addWidget(self.useRectText_checkbox)
            self.useRectText_checkbox_list.append(self.useRectText_checkbox)
            self.rect_tex_push_button = QtWidgets.QPushButton()
            self.rect_tex_push_button.setMinimumWidth(30)
            self.rect_tex_push_button.setMaximumWidth(30)
            self.rect_tex_push_button.setMinimumHeight(30)
            self.rect_tex_push_button.setMaximumHeight(30)
            self.rect_tex_push_button_list.append(self.rect_tex_push_button)
            self.rect_tex_push_button.clicked.connect(partial(self.rect_tex_state,light))
            horizontal_layout_light.addWidget(self.rect_tex_push_button)
            self.showTex_comboBox = QtWidgets.QComboBox()
            self.showTex_combo_box_list.append(self.showTex_comboBox)
            self.showTex_comboBox.addItem("Disabled")
            self.showTex_comboBox.addItem("Texture_Only")
            self.showTex_comboBox.addItem("Texture_Intensity")
            horizontal_layout_light.addWidget(self.showTex_comboBox)
            self.affect_diffuse_checkbox = QtWidgets.QCheckBox()
            self.affect_diffuse_checkbox_list.append(self.affect_diffuse_checkbox)
            horizontal_layout_light.addWidget(self.affect_diffuse_checkbox)
            self.diffuse_contributions_spinbox = custom_spin_box()
            self.diffuse_contributions_spinbox.setMinimum(0)
            self.diffuse_contributions_spinbox.setMaximum(10000)
            self.diffuse_contributions_spinbox.setDecimals(3)
            self.diffuse_contributions_spinbox.setSingleStep(.1)
            self.diffuse_contributions_spinbox.setFixedWidth(65)
            self.diffuse_contributions_spinbox.setKeyboardTracking(False)
            self.diffuse_contribution_spinbox_list.append(self.diffuse_contributions_spinbox)
            horizontal_layout_light.addWidget(self.diffuse_contributions_spinbox)
            self.affect_specular_checkbox = QtWidgets.QCheckBox()
            self.affect_specular_checkbox_list.append(self.affect_specular_checkbox)
            horizontal_layout_light.addWidget(self.affect_specular_checkbox)
            self.affect_specular_spinbox = custom_spin_box()
            self.affect_specular_spinbox.setMinimum(0)
            self.affect_specular_spinbox.setMaximum(10000)
            self.affect_specular_spinbox.setDecimals(3)
            self.affect_specular_spinbox.setSingleStep(.1)
            self.affect_specular_spinbox.setFixedWidth(65)
            self.affect_specular_spinbox.setKeyboardTracking(False)
            self.specular_contribution_spinbox_list.append(self.affect_specular_spinbox)
            horizontal_layout_light.addWidget(self.affect_specular_spinbox)
            self.affect_reflections_checkbox = QtWidgets.QCheckBox()
            self.affect_reflections_checkbox_list.append(self.affect_reflections_checkbox)
            horizontal_layout_light.addWidget(self.affect_reflections_checkbox)
            self.light_linking_line_edit = QtWidgets.QLineEdit()
            self.light_linking_line_edit.setFont(QtGui.QFont("SansSerif", 7))
            self.light_linking_line_edit.setFixedWidth(200)
            self.light_linking_line_edit_list.append(self.light_linking_line_edit)
            self.light_link_dict[light] = self.light_linking_line_edit
            horizontal_layout_light.addWidget(self.light_linking_line_edit)
            iter = iter + 1
        self.populate_attrs()
        self.maya_selection()
        #print "*END populate lights*"
        #print " "

    def populate_attrs(self):
        #print " "
        #print "populate attrs*"
        self.default_light_attrs()
        light_color_pointer_dict = {}
        override_environment_status = cmds.getAttr("vraySettings.cam_overrideEnvtex")
        if override_environment_status == 0:
            self.override_environment_checkbox.setChecked(0)
        if override_environment_status == 1:
            self.override_environment_checkbox.setChecked(1)
        self.renderLayers_combobox.clear()
        for render_layer in self.render_layers:
            self.renderLayers_combobox.addItem(render_layer)
        l = 0
        for layer in self.render_layers:
            if layer == self.current_render_layer:
                self.renderLayers_combobox.setCurrentIndex(l)
            l = l + 1
        self.renderLayers_combobox.activated[str].connect(lambda:self.render_layer_state())
#--
        iter = 0
        selected_objects = cmds.ls(sl = True)
        for transform in self.transforms_list:
            translateX_float_spinbox_value = self.default_light_attr_values[(transform + "_translateX")]
            self.translateX_spinbox_list[iter].setValue(translateX_float_spinbox_value)
            self.translateX_spinbox_list[iter].valueChanged.connect(lambda:self.translateX_float_spinbox_state())
            for override in self.render_layer_overrides:
                if transform in override:
                    if "translate" in override:
                        translateX_spinbox_list_pal = self.translateX_spinbox_list[iter].palette()
                        translateX_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.translateX_spinbox_list[iter].setPalette(translateX_spinbox_list_pal)
                        self.translateX_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if transform not in override:
                    self.translateX_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            translateY_float_spinbox_value = self.default_light_attr_values[(transform + "_translateY")]
            self.translateY_spinbox_list[iter].setValue(translateY_float_spinbox_value)
            self.translateY_spinbox_list[iter].valueChanged.connect(lambda:self.translateY_float_spinbox_state())
            for override in self.render_layer_overrides:
                if transform in override:
                    if "translate" in override:
                        translateY_spinbox_list_pal = self.translateY_spinbox_list[iter].palette()
                        translateY_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.translateY_spinbox_list[iter].setPalette(translateY_spinbox_list_pal)
                        self.translateY_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if transform not in override:
                    self.translateY_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            translateZ_float_spinbox_value = self.default_light_attr_values[(transform + "_translateZ")]
            self.translateZ_spinbox_list[iter].setValue(translateZ_float_spinbox_value)
            self.translateZ_spinbox_list[iter].valueChanged.connect(lambda:self.translateZ_float_spinbox_state())
            for override in self.render_layer_overrides:
                if transform in override:
                    if "translate" in override:
                        translateZ_spinbox_list_pal = self.translateZ_spinbox_list[iter].palette()
                        translateZ_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.translateZ_spinbox_list[iter].setPalette(translateZ_spinbox_list_pal)
                        self.translateZ_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if transform not in override:
                    self.translateZ_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            rotateX_float_spinbox_value = self.default_light_attr_values[(transform + "_rotateX")]
            self.rotateX_spinbox_list[iter].setValue(rotateX_float_spinbox_value)
            self.rotateX_spinbox_list[iter].valueChanged.connect(lambda:self.rotateX_float_spinbox_state())
            for override in self.render_layer_overrides:
                if transform in override:
                    if "rotate" in override:
                        rotateX_spinbox_list_pal = self.rotateX_spinbox_list[iter].palette()
                        rotateX_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.rotateX_spinbox_list[iter].setPalette(rotateX_spinbox_list_pal)
                        self.rotateX_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if transform not in override:
                    self.rotateX_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            rotateY_float_spinbox_value = self.default_light_attr_values[(transform + "_rotateY")]
            self.rotateY_spinbox_list[iter].setValue(rotateY_float_spinbox_value)
            self.rotateY_spinbox_list[iter].valueChanged.connect(lambda:self.rotateY_float_spinbox_state())
            for override in self.render_layer_overrides:
                if transform in override:
                    if "rotate" in override:
                        rotateY_spinbox_list_pal = self.rotateY_spinbox_list[iter].palette()
                        rotateY_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.rotateY_spinbox_list[iter].setPalette(rotateY_spinbox_list_pal)
                        self.rotateY_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if transform not in override:
                    self.rotateY_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            rotateZ_float_spinbox_value = self.default_light_attr_values[(transform + "_rotateZ")]
            self.rotateZ_spinbox_list[iter].setValue(rotateZ_float_spinbox_value)
            self.rotateZ_spinbox_list[iter].valueChanged.connect(lambda:self.rotateZ_float_spinbox_state())
            for override in self.render_layer_overrides:
                if transform in override:
                    if "rotate" in override:
                        rotateZ_spinbox_list_pal = self.rotateZ_spinbox_list[iter].palette()
                        rotateZ_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.rotateZ_spinbox_list[iter].setPalette(rotateZ_spinbox_list_pal)
                        self.rotateZ_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if transform not in override:
                    self.rotateZ_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            iter = iter + 1
#--
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
            for override in self.render_layer_overrides:
                if light in override:
                    if "enabled" in  override:
                        self.enabled_checkbox_list[iter].setStyleSheet("QCheckBox {background-color: orange;color: black};")
                if light not in override:
                    self.enabled_checkbox_list[iter].setStyleSheet("QCheckBox {background:rgb(65,66,66);")
            intensity_multiplier_float_spinbox_value = self.default_light_attr_values[(light + "_intensityMult")]
            self.intensity_multiplier_spinbox_list[iter].setValue(intensity_multiplier_float_spinbox_value)
            self.intensity_multiplier_spinbox_list[iter].valueChanged.connect(lambda:self.intensity_mult_float_spinbox_state())

            #for override in self.render_layer_overrides:
                #if light in override:
                    #if "light_color" in  override:
                        #light_color_pushbutton_list_pal = self.light_color_pushbutton_list[iter].palette()
                        #light_color_pushbutton_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        #self.light_color_pushbutton_list[iter].setPalette(vSize_spinbox_list_pal)
                        #self.light_color_pushbutton_list[iter].setStyleSheet("QPushButton {color: black};")
                #if light not in override:
                    #self.light_color_pushbutton_list[iter].setStyleSheet("QPushButton {background:rgb(65,66,66);")
            light_color_pushbutton_value = self.default_light_attr_values[(light + "_lightColor")]
            light_color_pushbutton_value = light_color_pushbutton_value[0]
            self.light_color_r = light_color_pushbutton_value[0]
            self.light_color_g = light_color_pushbutton_value[1]
            self.light_color_b = light_color_pushbutton_value[2]
            self.light_color_r = (self.light_color_r*255)
            self.light_color_r = int(self.light_color_r)
            self.light_color_g = (self.light_color_g*255)
            self.light_color_g = int(self.light_color_g)
            self.light_color_b = (self.light_color_b*255)
            self.light_color_b = int(self.light_color_b)
            color_string = "rgb(" + str(self.light_color_r) + "," + str(self.light_color_g) + "," + str(self.light_color_b) + ")"
            self.light_color_pushbutton_list[iter].setStyleSheet("QPushButton { background-color: %s}" %color_string)

            for override in self.render_layer_overrides:
                if light in override:
                    if "intensityMult" in override:
                        intensity_multiplier_spinbox_list_pal = self.intensity_multiplier_spinbox_list[iter].palette()
                        intensity_multiplier_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.intensity_multiplier_spinbox_list[iter].setPalette(intensity_multiplier_spinbox_list_pal)
                        self.intensity_multiplier_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if light not in override:
                    self.intensity_multiplier_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            uSize_float_spinbox_value = self.default_light_attr_values[(light + "_uSize")]
            self.uSize_spinbox_list[iter].setValue(uSize_float_spinbox_value)
            uSize_pointer = self.uSize_spinbox_list[iter]
            uSize_pointer.valueChanged.connect(lambda:self.uSize_spinbox_state(uSize_pointer))
            for override in self.render_layer_overrides:
                if light in override:
                    if "uSize" in  override:
                        uSize_spinbox_list_pal = self.uSize_spinbox_list[iter].palette()
                        uSize_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.uSize_spinbox_list[iter].setPalette(uSize_spinbox_list_pal)
                        self.uSize_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if light not in override:
                    self.uSize_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            vSize_float_spinbox_value = self.default_light_attr_values[(light + "_vSize")]
            self.vSize_spinbox_list[iter].setValue(vSize_float_spinbox_value)
            self.vSize_spinbox_list[iter].valueChanged.connect(lambda:self.vSize_spinbox_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "vSize" in  override:
                        vSize_spinbox_list_pal = self.vSize_spinbox_list[iter].palette()
                        vSize_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.vSize_spinbox_list[iter].setPalette(vSize_spinbox_list_pal)
                        self.vSize_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if light not in override:
                    self.vSize_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            directional_float_spinbox_value = self.default_light_attr_values[(light + "_directional")]
            self.directional_spinbox_list[iter].setValue(directional_float_spinbox_value)
            self.directional_spinbox_list[iter].valueChanged.connect(lambda:self.directional_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "directional" in  override:
                        directional_spinbox_list_pal = self.directional_spinbox_list[iter].palette()
                        directional_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.directional_spinbox_list[iter].setPalette(directional_spinbox_list_pal)
                        self.directional_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if light not in override:
                    self.directional_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            useRectText_checkbox_value = self.default_light_attr_values[(light + "_useRectText")]
            if useRectText_checkbox_value == 1:
                self.useRectText_checkbox_list[iter].setChecked(1)
            self.useRectText_checkbox_list[iter].stateChanged.connect(lambda:self.useRectTex_checkbox_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "useRectTex" in  override:
                        self.useRectText_checkbox_list[iter].setStyleSheet("QCheckBox {background-color: orange;color: black};")
                if light not in override:
                    self.useRectText_checkbox_list[iter].setStyleSheet("QCheckBox {background:rgb(65,66,66);")
            showTex_comboBox_value = self.default_light_attr_values[(light + "_showTex")]
            self.showTex_combo_box_list[iter].setCurrentIndex(showTex_comboBox_value)
            self.showTex_combo_box_list[iter].currentIndexChanged.connect(lambda:self.showTex_state())
            affectDiffuse_checkbox_value = self.default_light_attr_values[(light + "_affectDiffuse")]
            if affectDiffuse_checkbox_value == 1:
                self.affect_diffuse_checkbox_list[iter].setChecked(1)
            self.affect_diffuse_checkbox_list[iter].stateChanged.connect(lambda:self.affectDiffuse_checkbox_state())

            #for override in self.render_layer_overrides:
                #if light in override:
                    #if "rect_tex" in  override:
                        #rect_tex_push_button_list_pal = self.rect_tex_push_button_list[iter].palette()
                        #rect_tex_push_button_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        #self.rect_tex_push_button_list[iter].setPalette(vSize_spinbox_list_pal)
                        #self.rect_tex_push_button_list[iter].setStyleSheet("QPushButton {color: black};")
                #if light not in override:
                    #self.rect_tex_push_button_list[iter].setStyleSheet("QPushButton {background:rgb(65,66,66);")
            light_rect_pushbutton_value = self.default_light_attr_values[(light + "_rectTex")]
            light_rect_pushbutton_value = light_rect_pushbutton_value[0]
            self.light_rect_color_r = light_rect_pushbutton_value[0]
            self.light_rect_color_g = light_rect_pushbutton_value[1]
            self.light_rect_color_b = light_rect_pushbutton_value[2]
            self.light_rect_color_r = (self.light_rect_color_r*255)
            self.light_rect_color_r = int(self.light_rect_color_r)
            self.light_rect_color_g = (self.light_rect_color_g*255)
            self.light_rect_color_g = int(self.light_rect_color_g)
            self.light_rect_color_b = (self.light_rect_color_b*255)
            self.light_rect_color_b = int(self.light_rect_color_b)
            color_string = "rgb(" + str(self.light_rect_color_r) + "," + str(self.light_rect_color_g) + "," + str(self.light_rect_color_b) + ")"
            self.rect_tex_push_button_list[iter].setStyleSheet("QPushButton { background-color: %s}" %color_string)

            for override in self.render_layer_overrides:
                if light in override:
                    if "affectDiffuse" in  override:
                        self.affect_diffuse_checkbox_list[iter].setStyleSheet("QCheckBox {background-color: orange;color: black};")
                if light not in override:
                    self.affect_diffuse_checkbox_list[iter].setStyleSheet("QCheckBox {background:rgb(65,66,66);")
            diffuse_contribution_float_spinbox_value = self.default_light_attr_values[(light + "_diffuseContrib")]
            self.diffuse_contribution_spinbox_list[iter].setValue(diffuse_contribution_float_spinbox_value)
            self.diffuse_contribution_spinbox_list[iter].valueChanged.connect(lambda:self.diffuse_contribution_float_spinbox_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "diffuseContrib" in override:
                        diffuse_contribution_spinbox_list_pal = self.diffuse_contribution_spinbox_list[iter].palette()
                        diffuse_contribution_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.diffuse_contribution_spinbox_list[iter].setPalette(diffuse_contribution_spinbox_list_pal)
                        self.diffuse_contribution_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if light not in override:
                    self.diffuse_contribution_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            affectSpecular_checkbox_value = self.default_light_attr_values[(light + "_affectSpecular")]
            if affectSpecular_checkbox_value == 1:
                self.affect_specular_checkbox_list[iter].setChecked(1)
            self.affect_specular_checkbox_list[iter].stateChanged.connect(lambda:self.affectSpecular_checkbox_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "affectSpecular" in  override:
                        self.affect_specular_checkbox_list[iter].setStyleSheet("QCheckBox {background-color: orange;color: black};")
                if light not in override:
                    self.affect_specular_checkbox_list[iter].setStyleSheet("QCheckBox {background:rgb(65,66,66);")
            specular_contribution_float_spinbox_value = self.default_light_attr_values[(light + "_specularContrib")]
            self.specular_contribution_spinbox_list[iter].setValue(specular_contribution_float_spinbox_value)
            self.specular_contribution_spinbox_list[iter].valueChanged.connect(lambda:self.specular_contribution_float_spinbox_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "specularContrib" in override:
                        specular_contribution_spinbox_list_pal = self.specular_contribution_spinbox_list[iter].palette()
                        specular_contribution_spinbox_list_pal.setColor(QtGui.QPalette.Base, QtGui.QColor("orange"))
                        self.specular_contribution_spinbox_list[iter].setPalette(specular_contribution_spinbox_list_pal)
                        self.specular_contribution_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {color: black};")
                if light not in override:
                    self.specular_contribution_spinbox_list[iter].setStyleSheet("QDoubleSpinBox {background:rgb(65,66,66);")
            affectReflections_checkbox_value = self.default_light_attr_values[(light + "_affectReflections")]
            if affectReflections_checkbox_value == 1:
                self.affect_reflections_checkbox_list[iter].setChecked(1)
            self.affect_reflections_checkbox_list[iter].stateChanged.connect(lambda:self.affectReflections_checkbox_state())
            for override in self.render_layer_overrides:
                if light in override:
                    if "affectReflections" in  override:
                        self.affect_reflection_checkbox_list[iter].setStyleSheet("QCheckBox {background-color: orange;color: black};")
                if light not in override:
                    self.affect_reflections_checkbox_list[iter].setStyleSheet("QCheckBox {background:rgb(65,66,66);")
            iter = iter + 1
        iter = 0
        for light in self.lights:
            line_edit_light_linking_value = self.default_light_link_values[(light + "&light_linking")]
            for light_link in self.default_light_link_values:
                light_link_split = light_link.split("&")
                if light_link_split[0] == light:
                    link_values = self.default_light_link_values[light_link]
                    light_link_string = ""
                    for link in link_values:
                        link_string_size = len(light_link_string)
                        if link_string_size == 0:
                            light_link_string = link
                        if link_string_size > 0:
                            light_link_string = light_link_string + " , " + link
                    self.light_linking_line_edit_list[iter].setText(light_link_string)
                    self.light_link_pointer = self.light_linking_line_edit_list[iter]
                    for lit in self.light_labels_dict:
                        if lit == light:
                            self.light_pressed = lit
                    self.light_linking_line_edit_list[iter].returnPressed.connect(self.light_linking_line_edit_state)
            iter = iter + 1
            #print "*END populate attrs*"
            #print " "

    def override_environment_checkbox_state(self):
        state = self.override_environment_checkbox.isChecked()
        if state == 1:
            cmds.setAttr("vraySettings.cam_overrideEnvtex",1)
        if state == 0:
            cmds.setAttr("vraySettings.cam_overrideEnvtex",0)

    def solo_checkbox_state(self):
        #print " "
        #print "*solo checkbox*"
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
        #print "*END solo checkbox*"
        #print " "

    def enabled_checkbox_state(self):
        #print " "
        #print "*enabled checkbox*"
        iter = 0
        self.enabled_light_list_on_list = []
        self.solo_list_on_size = len(self.solo_list_on)
        for checkbox in self.enabled_checkbox_list:
            state = checkbox.isChecked()
            light = self.lights[iter]
            cmds.setAttr((light + ".enabled"),state)
            iter = iter + 1
        self.default_light_attrs()
        #print "*END enabled checkbox*"
        #print " "

    def light_color_state(self,light):
        cmds.colorEditor()
        if cmds.colorEditor(query=True, result=True):
            RGB_values = cmds.colorEditor(query=True, rgb=True)
            #print "RGB = " + str(RGB_values)
            r = RGB_values[0]
            g = RGB_values[1]
            b = RGB_values[2]
        cmds.setAttr((light + ".lightColor"),r,g,b, type = "double3")

#---

    def translateX_float_spinbox_state(self):
        iter = 0
        for spinbox in self.translateX_spinbox_list:
            value = spinbox.value()
            transform = self.transforms_list[iter]
            cmds.setAttr((transform + ".translateX"),value)
            iter = iter + 1

    def translateY_float_spinbox_state(self):
        iter = 0
        for spinbox in self.translateY_spinbox_list:
            value = spinbox.value()
            transform = self.transforms_list[iter]
            cmds.setAttr((transform + ".translateY"),value)
            iter = iter + 1

    def translateZ_float_spinbox_state(self):
        iter = 0
        for spinbox in self.translateZ_spinbox_list:
            value = spinbox.value()
            transform = self.transforms_list[iter]
            cmds.setAttr((transform + ".translateZ"),value)
            iter = iter + 1

    def rotateX_float_spinbox_state(self):
        iter = 0
        for spinbox in self.rotateX_spinbox_list:
            value = spinbox.value()
            transform = self.transforms_list[iter]
            cmds.setAttr((transform + ".rotateX"),value)
            iter = iter + 1

    def rotateY_float_spinbox_state(self):
        iter = 0
        for spinbox in self.rotateY_spinbox_list:
            value = spinbox.value()
            transform = self.transforms_list[iter]
            cmds.setAttr((transform + ".rotateY"),value)
            iter = iter + 1

    def rotateZ_float_spinbox_state(self):
        iter = 0
        for spinbox in self.rotateZ_spinbox_list:
            value = spinbox.value()
            transform = self.transforms_list[iter]
            cmds.setAttr((transform + ".rotateZ"),value)
            iter = iter + 1
#---
    def intensity_mult_float_spinbox_state(self):
        iter = 0
        for spinbox in self.intensity_multiplier_spinbox_list:
            value = spinbox.value()
            light = self.lights[iter]
            cmds.setAttr((light + ".intensityMult"),value)
            iter = iter + 1

    def uSize_spinbox_state(self,uSize_pointer):
        iter = 0
        for spinbox in self.uSize_spinbox_list:
            value = spinbox.value()
            light = self.lights[iter]
            cmds.setAttr((light + ".uSize"),value)
            iter = iter + 1

    def vSize_spinbox_state(self):
        iter = 0
        for spinbox in self.vSize_spinbox_list:
            value = spinbox.value()
            light = self.lights[iter]
            cmds.setAttr((light + ".vSize"),value)
            iter = iter + 1

    def directional_state(self):
        iter = 0
        for spinbox in self.directional_spinbox_list:
            value = spinbox.value()
            light = self.lights[iter]
            cmds.setAttr((light + ".directional"),value)
            iter = iter + 1

    def useRectTex_checkbox_state(self):
        iter = 0
        for checkbox in self.useRectText_checkbox_list:
            state = checkbox.isChecked()
            light = self.lights[iter]
            cmds.setAttr((light + ".useRectTex"),state)
            iter = iter + 1

    def rect_tex_state(self,light):
        ramp_detect = 0
        rect_texture_cons = cmds.listConnections(light + ".rectTex") or []
        for con in rect_texture_cons:
            con_type = cmds.nodeType(con)
            if con_type == "ramp" or con_type == "layeredTexture":
                ramp_detect = 1
        print "ramp_detect = ",ramp_detect
        if ramp_detect == 0:
            cmds.colorEditor()
            if cmds.colorEditor(query=True, result=True):
                RGB_values = cmds.colorEditor(query=True, rgb=True)
                r = RGB_values[0]
                g = RGB_values[1]
                b = RGB_values[2]
                cmds.setAttr((light + ".rectTex"),r,g,b, type = "double3")
        if ramp_detect == 1:
            attr_vis_state = cmds.workspaceControl('AttributeEditor', q=1, visible=1)
            ramp_node = rect_texture_cons[0]
            cmds.select(ramp_node)
            if attr_vis_state == 0:
                melAttrEdString = "AttributeEditor;"
                state = mel.eval(melAttrEdString)
            if attr_vis_state == 1:
                melAttrEdString = "copyAEWindow;"
                state = mel.eval(melAttrEdString)

    def showTex_state(self):
        iter = 0
        for spinbox in self.showTex_combo_box_list:
            value = spinbox.currentIndex()
            light = self.lights[iter]
            cmds.setAttr((light + ".showTex"),value)
            iter = iter + 1

    def showTex_label_event(self):
        for light in self.lights:
            if self.showTex_label_button_pressed == 0:
                cmds.setAttr(light + ".showTex",0)
            if self.showTex_label_button_pressed == 1:
                cmds.setAttr(light + ".showTex",1)
        if self.showTex_label_button_pressed == 0:
            self.showTex_label_button_pressed = 1
        else:
            self.showTex_label_button_pressed = 0
        self.populate_lights()

    def light_label_event(self,light,checked):
        for lght in self.lights:
            if lght == light:
                light_parent = cmds.listRelatives(lght,parent = True)
                if checked == True:
                    cmds.select(light_parent,add = True)
                if checked == False:
                    cmds.select(lght,deselect = True)
                    cmds.select(light_parent,deselect = True)

    def affectDiffuse_checkbox_state(self):
        iter = 0
        for checkbox in self.affect_diffuse_checkbox_list:
            state = checkbox.isChecked()
            light = self.lights[iter]
            cmds.setAttr((light + ".affectDiffuse"),state)
            iter = iter + 1

    def diffuse_contribution_float_spinbox_state(self):
        iter = 0
        for spinbox in self.diffuse_contribution_spinbox_list:
            value = spinbox.value()
            light = self.lights[iter]
            cmds.setAttr((light + ".diffuseContrib"),value)
            iter = iter + 1

    def affectSpecular_checkbox_state(self):
        iter = 0
        for checkbox in self.affect_specular_checkbox_list:
            state = checkbox.isChecked()
            light = self.lights[iter]
            cmds.setAttr((light + ".affectSpecular"),state)
            iter = iter + 1

    def specular_contribution_float_spinbox_state(self):
        iter = 0
        for spinbox in self.specular_contribution_spinbox_list:
            value = spinbox.value()
            light = self.lights[iter]
            cmds.setAttr((light + ".specularContrib"),value)
            iter = iter + 1

    def affectReflections_checkbox_state(self):
        iter = 0
        for checkbox in self.affect_reflections_checkbox_list:
            state = checkbox.isChecked()
            light = self.lights[iter]
            cmds.setAttr((light + ".affectReflections"),state)
            iter = iter + 1

    def light_linking_line_edit_state(self):
        iter = 0
        for light_linking_line_edit in self.light_linking_line_edit_list:
            print " "
            field_link_list = []
            light_linking_line_edit_values = light_linking_line_edit.displayText() or []
            size_light_linking_line_edit_values = len(light_linking_line_edit_values)
            if size_light_linking_line_edit_values > 0:
                light_linking_line_edit_values_split = light_linking_line_edit_values.split(" , ")
                for lllevs in light_linking_line_edit_values_split:
                    if  lllevs not in field_link_list:
                        field_link_list.append(lllevs)
                light = self.lights[iter]
                for new_link in field_link_list:
                    new_link_len = len(new_link)
                    if new_link_len > 0:
                        valid_link = 0
                        valid_link = cmds.objExists(new_link)
                    if new_link_len == 0:
                        print "empty light link field"
                    if valid_link == 1:
                        temp_links = cmds.lightlink(query = True,light = light)
                        for temp_link in temp_links:
                            cmds.lightlink(b = True, light = light, object = temp_link)
                        if size_light_linking_line_edit_values > 0:
                            for new_link in field_link_list:
                                valid_link = cmds.objExists(new_link)
                                if valid_link == 1:
                                    cmds.lightlink(make = True, light = light, object = new_link)
                    if valid_link == 0:
                        print "bad link detected"
            if size_light_linking_line_edit_values == 0:
                light = self.lights[iter]
                temp_links = cmds.lightlink(query = True,light = light)
                for temp_link in temp_links:
                    cmds.lightlink(b = True, light = light, object = temp_link)
            iter = iter + 1
        self.populate_attrs()

    def light_palette_ui(self):
        iter = 0
        self.render_layers_scan()
        self.windowName = "lights_palette"
        if cmds.window(self.windowName,exists = True):
            cmds.deleteUI(self.windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        self.window = QtWidgets.QMainWindow(parent)
        self.window.setObjectName(self.windowName)
        self.window.setWindowTitle(self.windowName)
        self.mainWidget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.mainWidget)
        self.vertical_layout_main = QtWidgets.QVBoxLayout(self.mainWidget)
        self.vertical_layout_main.setAlignment(QtCore.Qt.AlignTop)
        self.horizontal_layout_attrs = QtWidgets.QGridLayout(self.mainWidget)
        self.horizontal_layout_attrs.setAlignment(QtCore.Qt.AlignTop)
        self.horizontal_layout_attrs.setSpacing(0)
        self.vertical_layout_main.addLayout(self.horizontal_layout_attrs)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.vertical_layout_main.addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll.setWidget(self.scroll_widget)
        self.vertical_layout_lights = QtWidgets.QVBoxLayout(self.scroll_widget)
        self.vertical_layout_lights.setAlignment(QtCore.Qt.AlignTop)
        self.vertical_layout_main.addLayout(self.vertical_layout_lights)
        self.horizontal_layout_attrs.setColumnMinimumWidth(0,1)
        self.horizontal_layout_attrs.setAlignment(QtCore.Qt.AlignLeft)
        self.renderLayers_combobox = QtWidgets.QComboBox()
        self.renderLayers_combobox.setMaximumWidth(150)
        self.renderLayers_combobox.setMinimumHeight(18)
        self.horizontal_layout_attrs.addWidget(self.renderLayers_combobox,0,0)
        font = "SansSerif"
        type_size = 7
        spacer_1 = QtWidgets.QLabel("   ")
        self.horizontal_layout_attrs.addWidget(spacer_1,0,1)
        self.override_environment_checkbox = QtWidgets.QCheckBox("override_environment")
        self.override_environment_checkbox.setFont(QtGui.QFont(font, type_size))
        self.override_environment_checkbox.stateChanged.connect(lambda:self.override_environment_checkbox_state)
        self.horizontal_layout_attrs.addWidget(self.override_environment_checkbox,0,2)
        spacer_2 = QtWidgets.QLabel("                                                                              ")
        self.horizontal_layout_attrs.addWidget(spacer_2,0,3)
        solo_label = QtWidgets.QLabel("solo")
        solo_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(solo_label,0,4)
        spacer_3 = QtWidgets.QLabel("             ")
        self.horizontal_layout_attrs.addWidget(spacer_3,0,5)
        tx_label = QtWidgets.QLabel("tx")
        tx_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(tx_label,0,6)
        spacer_4 = QtWidgets.QLabel("                      ")
        self.horizontal_layout_attrs.addWidget(spacer_4,0,7)
        ty_label = QtWidgets.QLabel("ty")
        ty_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(ty_label,0,8)
        spacer_5 = QtWidgets.QLabel("                           ")
        self.horizontal_layout_attrs.addWidget(spacer_5,0,9)
        tz_label = QtWidgets.QLabel("tz")
        tz_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(tz_label,0,10)
        spacer_6 = QtWidgets.QLabel("                         ")
        self.horizontal_layout_attrs.addWidget(spacer_6,0,11)
        rx_label = QtWidgets.QLabel("rx")
        rx_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(rx_label,0,12)
        spacer_7 = QtWidgets.QLabel("                       ")
        self.horizontal_layout_attrs.addWidget(spacer_7,0,13)
        ry_label = QtWidgets.QLabel("ry")
        ry_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(ry_label,0,14)
        spacer_8 = QtWidgets.QLabel("                       ")
        self.horizontal_layout_attrs.addWidget(spacer_8,0,15)
        rz_label = QtWidgets.QLabel("rz")
        rz_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(rz_label,0,16)
        spacer_9 = QtWidgets.QLabel("              ")
        self.horizontal_layout_attrs.addWidget(spacer_9,0,17)
        enabled_label = QtWidgets.QLabel("enabled")
        enabled_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(enabled_label,0,18)
        spacer_10 = QtWidgets.QLabel("    ")
        self.horizontal_layout_attrs.addWidget(spacer_10,0,19)
        light_color_label = QtWidgets.QLabel("light_color")
        light_color_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(light_color_label,0,20)
        spacer_11 = QtWidgets.QLabel("     ")
        self.horizontal_layout_attrs.addWidget(spacer_11,0,21)
        intensityMult_label = QtWidgets.QLabel("intensityMult")
        intensityMult_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(intensityMult_label,0,22)
        spacer_12 = QtWidgets.QLabel("             ")
        self.horizontal_layout_attrs.addWidget(spacer_12,0,23)
        uSize_label = QtWidgets.QLabel("uSize")
        uSize_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(uSize_label,0,24)
        spacer_13 = QtWidgets.QLabel("                 ")
        self.horizontal_layout_attrs.addWidget(spacer_13,0,25)
        vSize_label = QtWidgets.QLabel("vSize")
        vSize_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(vSize_label,0,26)
        spacer_14 = QtWidgets.QLabel("                ")
        self.horizontal_layout_attrs.addWidget(spacer_14,0,27)
        directional_label = QtWidgets.QLabel("directional")
        directional_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(directional_label,0,28)
        spacer_15 = QtWidgets.QLabel("      ")
        self.horizontal_layout_attrs.addWidget(spacer_15,0,29)
        useRectText_label = QtWidgets.QLabel("useRectText")
        useRectText_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(useRectText_label,0,30)
        spacer_16 = QtWidgets.QLabel("   ")
        self.horizontal_layout_attrs.addWidget(spacer_16,0,31)
        rect_tex_label = QtWidgets.QLabel("rect_tex")
        rect_tex_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(rect_tex_label,0,32)
        spacer_17 = QtWidgets.QLabel("                 ")
        self.horizontal_layout_attrs.addWidget(spacer_17,0,33)
        self.showTex_label = QtWidgets.QPushButton("showTex")
        self.showTex_label.setFont(QtGui.QFont(font, type_size))
        self.showTex_label.setStyleSheet('QPushButton {background:rgb(65,66,66); color: white;}')
        self.showTex_label.clicked.connect(lambda:self.showTex_label_event())
        self.horizontal_layout_attrs.addWidget(self.showTex_label,0,34)
        spacer_18 = QtWidgets.QLabel("                    ")
        self.horizontal_layout_attrs.addWidget(spacer_18,0,35)
        affect_diffuse_label = QtWidgets.QLabel("diffuse")
        affect_diffuse_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(affect_diffuse_label,0,36)
        spacer_19 = QtWidgets.QLabel("     ")
        self.horizontal_layout_attrs.addWidget(spacer_19,0,37)
        diffuse_contribution_label = QtWidgets.QLabel("diffuse_contr")
        diffuse_contribution_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(diffuse_contribution_label,0,38)
        spacer_20 = QtWidgets.QLabel("     ")
        self.horizontal_layout_attrs.addWidget(spacer_20,0,39)
        affect_specular_label = QtWidgets.QLabel("specular")
        affect_specular_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(affect_specular_label,0,40)
        spacer_21 = QtWidgets.QLabel("    ")
        self.horizontal_layout_attrs.addWidget(spacer_21,0,41)
        specular_contribution_label = QtWidgets.QLabel("specular_contr")
        specular_contribution_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(specular_contribution_label,0,42)
        spacer_22 = QtWidgets.QLabel("   ")
        self.horizontal_layout_attrs.addWidget(spacer_22,0,43)
        affect_reflections_label = QtWidgets.QLabel("reflections")
        affect_reflections_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(affect_reflections_label,0,44)
        spacer_23 = QtWidgets.QLabel("                        ")
        self.horizontal_layout_attrs.addWidget(spacer_23,0,45)
        light_links_label = QtWidgets.QLabel("light_linking")
        light_links_label.setFont(QtGui.QFont(font, type_size))
        self.horizontal_layout_attrs.addWidget(light_links_label,0,46)
        self.lights = []
        self.lights = cmds.ls(type = "VRayLightRectShape")
        self.num_of_lights = len(self.lights)
        self.transforms_list = []
        self.transform_attrs = ["translateX","translateY","translateZ","rotateX","rotateY","rotateZ"]
        exp_transform_list = []
        self.light_attrs = ["enabled","lightColor","intensityMult","uSize","vSize","directional","useRectTex","rectTex","showTex","affectDiffuse","diffuseContrib","affectSpecular","specularContrib","affectReflections","lightColor"]
        exp_list = []
        for light in self.lights:
            for attr in self.light_attrs:
                string = light + "." + attr
                exp_list.append(string)
        exp_list.append("vraySettings.cam_overrideEnvtex")
        for light in self.lights:
            for attr in self.transform_attrs:
                transform = cmds.listRelatives(light,parent = True)
                if transform[0] not in self.transforms_list:
                    self.transforms_list.append(transform[0])
                string = transform[0] + "." + attr
                exp_transform_list.append(string)
        self.myScriptJobID = cmds.scriptJob(p = self.windowName, event=["renderLayerManagerChange", self.populate_lights])
        self.myScriptJobID = cmds.scriptJob(p = self.windowName, event=["SelectionChanged", self.populate_lights])
        for exp in exp_list:
            self.myScriptJobID = cmds.scriptJob(p = self.windowName, attributeChange=[exp, self.populate_lights])
        for exp in exp_transform_list:
            self.myScriptJobID = cmds.scriptJob(p = self.windowName, attributeChange=[exp, self.populate_lights])
        #for light in self.lights:
            #self.myScriptJobID = cmds.scriptJob(p = self.windowName, nodeNameChanged=[light, self.populate_lights])
        self.window.setFixedWidth(2150)
        self.default_light_attrs()
        self.populate_lights()
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.show()

lg = lights_palette()
lg.light_palette_ui()