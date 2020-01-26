import maya
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2

print 'tues 2'

class custom_spin_box(QtWidgets.QDoubleSpinBox):
    def wheelEvent(self, event):
        event.ignore()

class render_overrides_prop(object):
    def __init__(self):
        self.current_chosen_light = 'empty'
        self.default_layer_values_dic = {}

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.clearLayout(item.layout())

    def light_color_state(self):
        pass

    def rect_tex_color_state(self):
        pass

    def light_name_eval(self):
        print 'light_name_eval'
        self.light_names = []
        self.light_names = cmds.ls(type = 'VRayLightRectShape')

    def render_layers_eval(self):
        print 'render_layers_eval'
        self.render_layers_in_order = []
        self.render_layers = cmds.ls(type = 'renderLayer')
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
        #print 'render_layers_in_order = ',self.render_layers_in_order

    def default_Layer_values(self):
        print 'default_Layer_values'
        self.default_layer_values_dic = {}
        cmds.editRenderLayerGlobals(currentRenderLayer = 'defaultRenderLayer')
        for attr in self.scriptJob_attrs:
            if attr in self.xforms:
                light_parent = cmds.listRelatives(self.current_chosen_light,parent = True)
                light_parent = light_parent[0]
                light_name_attr = light_parent + '.' + attr
            else:
                light_name_attr = self.current_chosen_light + '.' + attr
            value = cmds.getAttr(light_name_attr)
            if (self.current_chosen_light + '_XXX_' + attr) not in self.default_layer_values_dic:
                self.default_layer_values_dic[attr] = value
        #print 'default_layer_values_dic = ',self.default_layer_values_dic
        cmds.editRenderLayerGlobals(currentRenderLayer = self.current_render_layer)

    def detect_overrides(self):
        print 'detect_overrides '
        self.layer_overrides_dic = {}
        for layer in self.render_layers_in_order:
            #print ' '
            #print 'layer = ',layer
            cmds.editRenderLayerGlobals( currentRenderLayer = layer)
            for attr in self.scriptJob_attrs:
                if attr in self.xforms:
                    light_parent = cmds.listRelatives(self.current_chosen_light,parent = True)
                    light_parent = light_parent[0]
                    light_name_attr = light_parent + '.' + attr
                else:
                    light_name_attr = self.current_chosen_light + '.' + attr
                value = cmds.getAttr(light_name_attr)
                for default_attr in self.default_layer_values_dic:
                    if default_attr == attr:
                        #print 'default_attr = ',default_attr
                        #print cmds.editRenderLayerGlobals( query = True, currentRenderLayer = True)
                        #print 'attr = ',attr
                        attr_value = cmds.getAttr(light_name_attr)
                        default_attr = self.default_layer_values_dic[attr]
                        #print 'attr_value = ',attr_value
                        #print 'default_attr = ',default_attr
                        if attr_value != default_attr:
                            #print 'attr_value = ',attr_value
                            #print 'default_attr = ',default_attr
                            self.layer_overrides_dic[attr] = layer
        #print 'self.layer_overrides_dic = ',self.layer_overrides_dic
        self.override_color_mod()

    def override_color_mod(self):
        print ' '
        print 'override_color_mod'
        #print 'self.attribute_name_pointer_dic = ',self.attribute_name_pointer_dic
        #print 'self.layer_overrides_dic = ',self.layer_overrides_dic
        for attr in self.attribute_name_pointer_dic:
            pointer = self.attribute_name_pointer_dic[attr]
            #print 'setting ' + attr + ' to black'
            pointer.setStyleSheet("QLabel { background:rgb(65,66,66); color : rgb(180,180,180); }");
            for override in self.layer_overrides_dic:
                #print 'attr = ',attr
                #print 'override = ',override
                if attr in override:
                    #print 'match, turning ' + attr + ' orange'
                    pointer.setStyleSheet("QLabel { background:rgb(65,66,66); color : rgb(225,120,0); }");
        cmds.editRenderLayerGlobals(currentRenderLayer = self.current_render_layer)

    def override_color_mod_single(self,attr):
        print ' '
        print 'override_color_mod'
        #print 'self.attribute_name_pointer_dic = ',self.attribute_name_pointer_dic
        #print 'self.layer_overrides_dic = ',self.layer_overrides_dic
        pointer = self.attribute_name_pointer_dic[attr]
        #print 'setting ' + attr + ' to black'
        pointer.setStyleSheet("QLabel { background:rgb(65,66,66); color : rgb(180,180,180); }");
        for override in self.layer_overrides_dic:
            #print 'attr = ',attr
            #print 'override = ',override
            if attr in override:
                #print 'match, turning ' + attr + ' orange'
                pointer.setStyleSheet("QLabel { background:rgb(65,66,66); color : rgb(225,120,0); }");
        cmds.editRenderLayerGlobals(currentRenderLayer = self.current_render_layer)

    def value_set(self,attribute_label,widget,args):
        print 'value_set'
        #print 'widget = ',widget
        #print 'self.default_layer_values_dic = ',self.default_layer_values_dic
        attribute_label_text = attribute_label.text()
        #print 'attribute_label_text = ',attribute_label_text
        empty_default_layer_values_dic = len(self.default_layer_values_dic)
        transforms = ['translate','rotate','scale']
        if empty_default_layer_values_dic != 0:
            attribute_label_text = attribute_label_text.replace(' ','')
            if attribute_label_text not in transforms:
                print 'attribute_label_text not in transforms'
                print attribute_label_text
                #print 'transforms = ',transforms
                if attribute_label_text == 'intensity':
                    attribute_label_text = 'intensityMult'
                if attribute_label_text == 'Usize':
                    attribute_label_text = 'uSize'
                if attribute_label_text == 'Vsize':
                    attribute_label_text = 'vSize'
                if attribute_label_text == 'lightcolor':
                    attribute_label_text = 'lightColor'
                if attribute_label_text == 'userecttex':
                    attribute_label_text = 'useRectTex'
                if attribute_label_text == 'recttex':
                    attribute_label_text = 'rectTex'
                if attribute_label_text == 'affectdiffuse':
                    attribute_label_text = 'affectDiffuse'
                if attribute_label_text == 'affectspecular':
                    attribute_label_text = 'affectSpecular'
                if attribute_label_text == 'affectreflections':
                    attribute_label_text = 'affectReflections'
                if attribute_label_text == 'diffusecontribution':
                    attribute_label_text = 'diffuseContrib'
                if attribute_label_text == 'specularcontribution':
                    attribute_label_text = 'specularContrib'
                default_value = self.default_layer_values_dic[attribute_label_text]
                #print 'default_value = ',default_value
                if attribute_label_text == 'enabled' or attribute_label_text == 'useRectTex' or attribute_label_text == 'affectDiffuse' or attribute_label_text == 'affectSpecular' or attribute_label_text == 'affectReflections':
                    set_value = widget.isChecked()
                else:
                    set_value = widget.value()
                #print 'set_value = ',set_value
                if set_value != default_value:
                    attribute_label.setStyleSheet("QLabel { background:rgb(65,66,66); color : rgb(250,0,0); }");
                else:
                    self.override_color_mod_single(attribute_label_text)
            else:
                #print 'setting ' + str(widget) + ' to red'
                attribute_label.setStyleSheet("QLabel { background:rgb(65,66,66); color : rgb(250,0,0); }");


    def populate_gui(self):
        print 'populate_gui'
        self.current_render_layer = cmds.editRenderLayerGlobals( query = True, currentRenderLayer = True)
        cmds.editRenderLayerGlobals( currentRenderLayer = 'defaultRenderLayer')
        self.light_name_eval()
        self.render_layers_eval()
        #self.clearLayout(self.main_horizontal_layout)
        #self.clearLayout(self.button_horizontal_layout)
        #print ' 0 self.current_chosen_light = ',self.current_chosen_light
        self.light_name_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_horizontal_layout.addLayout(self.light_name_layout)
        self.light_name_layout.setAlignment(Qt.AlignTop)
        self.light_combo_box = QtWidgets.QComboBox()
        self.light_combo_box.setMaximumWidth(280)
        self.light_combo_box.setMinimumHeight(18)
        self.light_name_layout.addWidget(self.light_combo_box)
        for light in self.light_names:
            self.light_combo_box.addItem(light)
        self.light_combo_box.activated[str].connect(lambda:self.attribute_analysis())
        i = 0
        #print ' 1 self.current_chosen_light = ',self.current_chosen_light
        for light in self.light_names:
            #print 'light = ',light
            #print '2 self.current_chosen_light = ',self.current_chosen_light
            if light == self.current_chosen_light:
                #print 'i = i'
                self.light_combo_box.setCurrentIndex(i)
            i = i + 1
        self.attribute_name_pointer_dic = {}
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidgetResizable(False)
        self.main_horizontal_layout.addWidget(self.scroll)
        self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_widget = QtWidgets.QWidget()
        self.scroll.setWidget(self.scroll_widget)
        self.attribute_layout = QtWidgets.QVBoxLayout(self.scroll)
        #self.clearLayout(self.attribute_layout)
        self.attribute_layout.setAlignment(Qt.AlignTop)
        self.main_horizontal_layout.addLayout(self.attribute_layout)
        self.translate_layout = QtWidgets.QHBoxLayout(self.scroll)                #---
        self.translate_layout.setAlignment(Qt.AlignTop)
        self.attribute_layout.addLayout(self.translate_layout)
        attribute_label = QtWidgets.QLabel('translate    ')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.translate_layout.addWidget(attribute_label)
        self.attribute_translateX_float_spinbox = custom_spin_box()
        #self.attribute_name_pointer_dic['translate'] = self.attribute_translateX_float_spinbox
        self.attribute_translateX_float_spinbox.setMinimum(-100)
        self.attribute_translateX_float_spinbox.setMaximum(10000)
        self.attribute_translateX_float_spinbox.setDecimals(3)
        self.attribute_translateX_float_spinbox.setSingleStep(.1)
        self.attribute_translateX_float_spinbox.setFixedWidth(65)
        self.attribute_translateX_float_spinbox.setKeyboardTracking(False)
        self.translate_layout.addWidget(self.attribute_translateX_float_spinbox)
        self.attribute_name_pointer_dic['translateX'] = attribute_label
        self.attribute_translateX_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_translateX_float_spinbox))
        self.attribute_translateY_float_spinbox = custom_spin_box()
        self.attribute_translateY_float_spinbox.setMinimum(-100)
        self.attribute_translateY_float_spinbox.setMaximum(10000)
        self.attribute_translateY_float_spinbox.setDecimals(3)
        self.attribute_translateY_float_spinbox.setSingleStep(.1)
        self.attribute_translateY_float_spinbox.setFixedWidth(65)
        self.attribute_translateY_float_spinbox.setKeyboardTracking(False)
        self.translate_layout.addWidget(self.attribute_translateY_float_spinbox)
        self.attribute_name_pointer_dic['translateY'] = self.attribute_translateY_float_spinbox
        self.attribute_translateY_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_translateY_float_spinbox))
        self.attribute_translateZ_float_spinbox = custom_spin_box()
        self.attribute_translateZ_float_spinbox.setMinimum(-100)
        self.attribute_translateZ_float_spinbox.setMaximum(10000)
        self.attribute_translateZ_float_spinbox.setDecimals(3)
        self.attribute_translateZ_float_spinbox.setSingleStep(.1)
        self.attribute_translateZ_float_spinbox.setFixedWidth(65)
        self.attribute_translateZ_float_spinbox.setKeyboardTracking(False)
        self.translate_layout.addWidget(self.attribute_translateZ_float_spinbox)
        self.attribute_name_pointer_dic['translateZ'] = self.attribute_translateZ_float_spinbox
        self.attribute_translateZ_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_translateZ_float_spinbox))
        self.translate_layout_spacer_label = QtWidgets.QLabel(' ')
        self.translate_layout.addWidget(self.translate_layout_spacer_label)
        self.rotate_layout = QtWidgets.QHBoxLayout(self.scroll)                #---
        self.rotate_layout.setAlignment(Qt.AlignTop)
        self.attribute_layout.addLayout(self.rotate_layout)
        attribute_label = QtWidgets.QLabel('rotate        ')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.rotate_layout.addWidget(attribute_label)
        self.attribute_rotateX_float_spinbox = custom_spin_box()
        self.attribute_rotateX_float_spinbox.setMinimum(-100)
        self.attribute_rotateX_float_spinbox.setMaximum(10000)
        self.attribute_rotateX_float_spinbox.setDecimals(3)
        self.attribute_rotateX_float_spinbox.setSingleStep(.1)
        self.attribute_rotateX_float_spinbox.setFixedWidth(65)
        self.attribute_rotateX_float_spinbox.setKeyboardTracking(False)
        self.rotate_layout.addWidget(self.attribute_rotateX_float_spinbox)
        self.attribute_name_pointer_dic['rotateX'] = attribute_label
        self.attribute_rotateX_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_rotateX_float_spinbox))
        self.attribute_rotateY_float_spinbox = custom_spin_box()
        self.attribute_rotateY_float_spinbox.setMinimum(-100)
        self.attribute_rotateY_float_spinbox.setMaximum(10000)
        self.attribute_rotateY_float_spinbox.setDecimals(3)
        self.attribute_rotateY_float_spinbox.setSingleStep(.1)
        self.attribute_rotateY_float_spinbox.setFixedWidth(65)
        self.attribute_rotateY_float_spinbox.setKeyboardTracking(False)
        self.rotate_layout.addWidget(self.attribute_rotateY_float_spinbox)
        self.attribute_name_pointer_dic['rotateY'] = attribute_label
        self.attribute_rotateY_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_rotateY_float_spinbox))
        self.attribute_rotateZ_float_spinbox = custom_spin_box()
        self.attribute_rotateZ_float_spinbox.setMinimum(-100)
        self.attribute_rotateZ_float_spinbox.setMaximum(10000)
        self.attribute_rotateZ_float_spinbox.setDecimals(3)
        self.attribute_rotateZ_float_spinbox.setSingleStep(.1)
        self.attribute_rotateZ_float_spinbox.setFixedWidth(65)
        self.attribute_rotateZ_float_spinbox.setKeyboardTracking(False)
        self.rotate_layout.addWidget(self.attribute_rotateZ_float_spinbox)
        self.attribute_name_pointer_dic['rotateZ'] = attribute_label
        self.attribute_rotateZ_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_rotateZ_float_spinbox))
        self.rotate_layout_spacer_label = QtWidgets.QLabel('')
        self.rotate_layout.addWidget(self.rotate_layout_spacer_label)
        self.scale_layout = QtWidgets.QHBoxLayout(self.scroll)
        self.scale_layout.setAlignment(Qt.AlignTop)
        self.attribute_layout.addLayout(self.scale_layout)
        attribute_label = QtWidgets.QLabel('scale         ')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.scale_layout.addWidget(attribute_label)
        self.attribute_scaleX_float_spinbox = custom_spin_box()
        self.attribute_scaleX_float_spinbox.setMinimum(-100)
        self.attribute_scaleX_float_spinbox.setMaximum(10000)
        self.attribute_scaleX_float_spinbox.setDecimals(3)
        self.attribute_scaleX_float_spinbox.setSingleStep(.1)
        self.attribute_scaleX_float_spinbox.setFixedWidth(65)
        self.attribute_scaleX_float_spinbox.setKeyboardTracking(False)
        self.scale_layout.addWidget(self.attribute_scaleX_float_spinbox)
        self.attribute_name_pointer_dic['scaleX'] = attribute_label
        self.attribute_scaleX_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_scaleX_float_spinbox))
        self.attribute_scaleY_float_spinbox = custom_spin_box()
        self.attribute_scaleY_float_spinbox.setMinimum(-100)
        self.attribute_scaleY_float_spinbox.setMaximum(10000)
        self.attribute_scaleY_float_spinbox.setDecimals(3)
        self.attribute_scaleY_float_spinbox.setSingleStep(.1)
        self.attribute_scaleY_float_spinbox.setFixedWidth(65)
        self.attribute_scaleY_float_spinbox.setKeyboardTracking(False)
        self.scale_layout.addWidget(self.attribute_scaleY_float_spinbox)
        self.attribute_name_pointer_dic['scaleY'] = attribute_label
        self.attribute_scaleY_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_scaleY_float_spinbox))
        self.attribute_scaleZ_float_spinbox = custom_spin_box()
        self.attribute_scaleZ_float_spinbox.setMinimum(-100)
        self.attribute_scaleZ_float_spinbox.setMaximum(10000)
        self.attribute_scaleZ_float_spinbox.setDecimals(3)
        self.attribute_scaleZ_float_spinbox.setSingleStep(.1)
        self.attribute_scaleZ_float_spinbox.setFixedWidth(65)
        self.attribute_scaleZ_float_spinbox.setKeyboardTracking(False)
        self.scale_layout.addWidget(self.attribute_scaleZ_float_spinbox)
        self.attribute_name_pointer_dic['scaleZ'] = attribute_label
        self.attribute_scaleZ_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_scaleZ_float_spinbox))
        self.scale_layout_spacer_label = QtWidgets.QLabel('')
        self.scale_layout.addWidget(self.scale_layout_spacer_label)
        attribute_label = QtWidgets.QLabel('enabled')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.enabled_checkbox = QtWidgets.QCheckBox()
        self.attribute_layout.addWidget(self.enabled_checkbox)
        self.attribute_name_pointer_dic['enabled'] = attribute_label
        self.enabled_checkbox.stateChanged.connect(partial(self.value_set,attribute_label,self.enabled_checkbox))
        attribute_label = QtWidgets.QLabel('light color  ')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.light_color_pushbutton = QtWidgets.QPushButton()
        self.light_color_pushbutton.setMinimumWidth(30)
        self.light_color_pushbutton.setMaximumWidth(30)
        self.light_color_pushbutton.setMinimumHeight(30)
        self.light_color_pushbutton.setMaximumHeight(30)
        self.light_color_pushbutton.clicked.connect(partial(self.light_color_state))
        self.attribute_layout.addWidget(self.light_color_pushbutton)
        self.attribute_name_pointer_dic['lightColor'] = attribute_label
        self.light_color_pushbutton.clicked.connect(partial(self.value_set,attribute_label,self.light_color_pushbutton))
        attribute_label = QtWidgets.QLabel('intensity')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.attribute_intensityMult_float_spinbox = custom_spin_box()
        self.attribute_intensityMult_float_spinbox.setMinimum(-100)
        self.attribute_intensityMult_float_spinbox.setMaximum(10000)
        self.attribute_intensityMult_float_spinbox.setDecimals(3)
        self.attribute_intensityMult_float_spinbox.setSingleStep(.1)
        self.attribute_intensityMult_float_spinbox.setFixedWidth(65)
        self.attribute_intensityMult_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_intensityMult_float_spinbox)
        self.attribute_name_pointer_dic['intensityMult'] = attribute_label
        self.attribute_intensityMult_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_intensityMult_float_spinbox))
        attribute_label = QtWidgets.QLabel('U size')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.attribute_u_size_float_spinbox = custom_spin_box()
        self.attribute_u_size_float_spinbox.setMinimum(-100)
        self.attribute_u_size_float_spinbox.setMaximum(10000)
        self.attribute_u_size_float_spinbox.setDecimals(3)
        self.attribute_u_size_float_spinbox.setSingleStep(.1)
        self.attribute_u_size_float_spinbox.setFixedWidth(65)
        self.attribute_u_size_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_u_size_float_spinbox)
        self.attribute_name_pointer_dic['uSize'] = attribute_label
        self.attribute_u_size_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_u_size_float_spinbox))
        attribute_label = QtWidgets.QLabel('V size')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.attribute_v_size_float_spinbox = custom_spin_box()
        self.attribute_v_size_float_spinbox.setMinimum(-100)
        self.attribute_v_size_float_spinbox.setMaximum(10000)
        self.attribute_v_size_float_spinbox.setDecimals(3)
        self.attribute_v_size_float_spinbox.setSingleStep(.1)
        self.attribute_v_size_float_spinbox.setFixedWidth(65)
        self.attribute_v_size_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_v_size_float_spinbox)
        self.attribute_name_pointer_dic['vSize'] = attribute_label
        self.attribute_v_size_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_v_size_float_spinbox))
        attribute_label = QtWidgets.QLabel('directional')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.attribute_directional_float_spinbox = custom_spin_box()
        self.attribute_directional_float_spinbox.setMinimum(-100)
        self.attribute_directional_float_spinbox.setMaximum(10000)
        self.attribute_directional_float_spinbox.setDecimals(3)
        self.attribute_directional_float_spinbox.setSingleStep(.1)
        self.attribute_directional_float_spinbox.setFixedWidth(65)
        self.attribute_directional_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_directional_float_spinbox)
        self.attribute_name_pointer_dic['directional'] = attribute_label
        self.attribute_directional_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_directional_float_spinbox))
        attribute_label = QtWidgets.QLabel('use rect tex')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.use_rect_tex_checkbox = QtWidgets.QCheckBox()
        self.attribute_layout.addWidget(self.use_rect_tex_checkbox)
        self.attribute_name_pointer_dic['useRectTex'] = attribute_label
        self.use_rect_tex_checkbox.stateChanged.connect(partial(self.value_set,attribute_label,self.use_rect_tex_checkbox))
        attribute_label = QtWidgets.QLabel('rect tex     ')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.rect_text_color_pushbutton = QtWidgets.QPushButton()
        self.rect_text_color_pushbutton.setMinimumWidth(30)
        self.rect_text_color_pushbutton.setMaximumWidth(30)
        self.rect_text_color_pushbutton.setMinimumHeight(30)
        self.rect_text_color_pushbutton.setMaximumHeight(30)
        self.rect_text_color_pushbutton.clicked.connect(partial(self.rect_tex_color_state))
        self.attribute_layout.addWidget(self.rect_text_color_pushbutton)
        self.attribute_name_pointer_dic['rectTex'] = attribute_label
        self.rect_text_color_pushbutton.clicked.connect(partial(self.value_set,attribute_label,self.rect_text_color_pushbutton))
        self.light_rect_color_r = 10
        self.light_rect_color_g = 100
        self.light_rect_color_b = 1
        color_string = "rgb(" + str(self.light_rect_color_r) + "," + str(self.light_rect_color_g) + "," + str(self.light_rect_color_b) + ")"
        self.rect_text_color_pushbutton.setStyleSheet("QPushButton { background-color: %s}" %color_string)
        attribute_label = QtWidgets.QLabel('affect diffuse')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.affect_diffuse_checkbox = QtWidgets.QCheckBox()
        self.attribute_layout.addWidget(self.affect_diffuse_checkbox)
        self.attribute_name_pointer_dic['affectDiffuse'] = attribute_label
        self.affect_diffuse_checkbox.stateChanged.connect(partial(self.value_set,attribute_label,self.affect_diffuse_checkbox))
        attribute_label = QtWidgets.QLabel('affect specular')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.affect_specular_checkbox = QtWidgets.QCheckBox()
        self.attribute_layout.addWidget(self.affect_specular_checkbox)
        self.attribute_name_pointer_dic['affectSpecular'] = attribute_label
        self.affect_specular_checkbox.stateChanged.connect(partial(self.value_set,attribute_label,self.affect_specular_checkbox))
        attribute_label = QtWidgets.QLabel('affect reflections')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.affect_reflection_checkbox = QtWidgets.QCheckBox()
        self.attribute_layout.addWidget(self.affect_reflection_checkbox)
        self.attribute_name_pointer_dic['affectReflections'] = attribute_label
        self.affect_reflection_checkbox.stateChanged.connect(partial(self.value_set,attribute_label,self.affect_reflection_checkbox))
        attribute_label = QtWidgets.QLabel('diffuse contribution')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.attribute_diffuse_contribution_float_spinbox = custom_spin_box()
        self.attribute_diffuse_contribution_float_spinbox.setMinimum(-100)
        self.attribute_diffuse_contribution_float_spinbox.setMaximum(10000)
        self.attribute_diffuse_contribution_float_spinbox.setDecimals(3)
        self.attribute_diffuse_contribution_float_spinbox.setSingleStep(.1)
        self.attribute_diffuse_contribution_float_spinbox.setFixedWidth(65)
        self.attribute_diffuse_contribution_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_diffuse_contribution_float_spinbox)
        self.attribute_name_pointer_dic['diffuseContrib'] = attribute_label
        self.attribute_diffuse_contribution_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_diffuse_contribution_float_spinbox))
        attribute_label = QtWidgets.QLabel('specular contribution')
        attribute_label.setFont(QtGui.QFont('SansSerif', 10))
        self.attribute_layout.addWidget(attribute_label)
        self.attribute_specular_contribution_float_spinbox = custom_spin_box()
        self.attribute_specular_contribution_float_spinbox.setMinimum(-100)
        self.attribute_specular_contribution_float_spinbox.setMaximum(10000)
        self.attribute_specular_contribution_float_spinbox.setDecimals(3)
        self.attribute_specular_contribution_float_spinbox.setSingleStep(.1)
        self.attribute_specular_contribution_float_spinbox.setFixedWidth(65)
        self.attribute_specular_contribution_float_spinbox.setKeyboardTracking(False)
        self.attribute_layout.addWidget(self.attribute_specular_contribution_float_spinbox)
        self.attribute_name_pointer_dic['specularContrib'] = attribute_label
        self.attribute_specular_contribution_float_spinbox.valueChanged.connect(partial(self.value_set,attribute_label,self.attribute_specular_contribution_float_spinbox))
        #print self.render_layers_in_order
        self.render_layer_layout = QtWidgets.QVBoxLayout(self.main_widget)
        #self.clearLayout(self.render_layer_layout)
        self.main_horizontal_layout.addLayout(self.render_layer_layout)
        self.render_layer_layout.setAlignment(Qt.AlignTop)
        self.render_layer_checkbox_layout = QtWidgets.QVBoxLayout(self.main_widget)
        #self.clearLayout(self.render_layer_checkbox_layout)
        self.main_horizontal_layout.addLayout(self.render_layer_checkbox_layout)
        self.render_layer_checkbox_layout.setAlignment(Qt.AlignTop)
        #self.spacer_label = QtWidgets.QLabel('')
        #self.render_layer_checkbox_layout.addWidget(self.spacer_label)
        for render_layer in self.render_layers_in_order:
            if render_layer != 'defaultRenderLayer':
                self.render_layer_label = QtWidgets.QLabel(render_layer)
                self.render_layer_label.setFont(QtGui.QFont('SansSerif', 7))
                self.render_layer_layout.addWidget(self.render_layer_label)
                layer_checkbox = QtWidgets.QCheckBox()
                self.render_layer_checkbox_layout.addWidget(layer_checkbox)
        button_clear_selected_layer_overrides = QtWidgets.QPushButton("clear overrides in selected layers")
        button_clear_all_overrides = QtWidgets.QPushButton("clear overrides in all layers")
        button_set_selected_layer_overrides = QtWidgets.QPushButton("set overrides in selected layers")
        button_set_all_layer_overrides = QtWidgets.QPushButton("set overrides in all layers")
        #button_set_overrides.setFixedWidth(button_width)
        #button_set_overrides.setFixedHeight(button_height)
        #button_set_overrides.pressed.connect(partial(self.allToggleTexture_off))
        self.button_horizontal_layout.addWidget(button_clear_selected_layer_overrides)
        self.button_horizontal_layout.addWidget(button_clear_all_overrides)
        self.button_horizontal_layout.addWidget(button_set_selected_layer_overrides)
        self.button_horizontal_layout.addWidget(button_set_all_layer_overrides)
        self.attribute_analysis()

    def attribute_analysis(self):
        print 'attribute_analysis'
        self.current_chosen_light = self.light_combo_box.currentText()
        #print ' self.current_chosen_light = ',self.current_chosen_light
        parent = cmds.listRelatives(self.current_chosen_light, parent = True)
        transform_x = cmds.getAttr(parent[0] + '.translateX')
        transform_y = cmds.getAttr(parent[0] + '.translateY')
        transform_z = cmds.getAttr(parent[0] + '.translateZ')
        rotate_x = cmds.getAttr(parent[0] + '.rotateX')
        rotate_y = cmds.getAttr(parent[0] + '.rotateY')
        rotate_z = cmds.getAttr(parent[0] + '.rotateZ')
        scale_x = cmds.getAttr(parent[0] + '.scaleX')
        scale_y = cmds.getAttr(parent[0] + '.scaleY')
        scale_z = cmds.getAttr(parent[0] + '.scaleZ')
        self.attribute_translateX_float_spinbox.setValue(transform_x)
        self.attribute_translateY_float_spinbox.setValue(transform_y)
        self.attribute_translateZ_float_spinbox.setValue(transform_z)
        self.attribute_rotateX_float_spinbox.setValue(rotate_x)
        self.attribute_rotateY_float_spinbox.setValue(rotate_y)
        self.attribute_rotateZ_float_spinbox.setValue(rotate_z)
        self.attribute_scaleX_float_spinbox.setValue(scale_x)
        self.attribute_scaleY_float_spinbox.setValue(scale_y)
        self.attribute_scaleZ_float_spinbox.setValue(scale_z)
        enabled_value = cmds.getAttr(self.current_chosen_light + '.enabled')
        #print 'enabled_value = ',enabled_value
        #print 'setting ' + str(self.enabled_checkbox) + ' to ' + str(enabled_value)
        self.enabled_checkbox.setChecked(enabled_value)
        light_color = cmds.getAttr(self.current_chosen_light + '.lightColor')
        light_color = light_color[0]
        #print 'light_color = ',light_color
        light_color_r = light_color[0]
        light_color_r = (light_color_r*255)
        #print 'light_color_r = ',light_color_r
        light_color_g = light_color[1]
        light_color_g = (light_color_g*255)
        #print 'light_color_g = ',light_color_g
        light_color_b = light_color[2]
        light_color_b = (light_color_b*255)
        #print 'light_color_b = ',light_color_b
        color_string = "rgb(" + str(light_color_r) + "," + str(light_color_g) + "," + str(light_color_b) + ")"
        self.light_color_pushbutton.setStyleSheet("QPushButton { background-color: %s}" %color_string)
        intensityMult_value = cmds.getAttr(self.current_chosen_light + '.intensityMult')
        #print 'intensityMult_value = ',intensityMult_value
        #print 'setting ' + str(self.attribute_intensityMult_float_spinbox) + ' to ' + str(intensityMult_value)
        self.attribute_intensityMult_float_spinbox.setValue(intensityMult_value)
        u_size_value = cmds.getAttr(self.current_chosen_light + '.uSize')
        #print 'u_size_value = ',u_size_value
        #print 'setting ' + str(self.attribute_u_size_float_spinbox) + ' to ' + str(u_size_value)
        self.attribute_u_size_float_spinbox.setValue(u_size_value)
        v_size_value = cmds.getAttr(self.current_chosen_light + '.vSize')
        #print 'v_size_value = ',v_size_value
        #print 'setting ' + str(self.attribute_v_size_float_spinbox) + ' to ' + str(v_size_value)
        self.attribute_v_size_float_spinbox.setValue(v_size_value)
        directional_value = cmds.getAttr(self.current_chosen_light + '.directional')
        #print 'directional_value = ',directional_value
        #print 'setting ' + str(self.attribute_directional_float_spinbox) + ' to ' + str(directional_value)
        self.attribute_directional_float_spinbox.setValue(directional_value)
        use_rect_tex_value = cmds.getAttr(self.current_chosen_light + '.useRectTex')
        #print 'use_rect_tex_value = ',use_rect_tex_value
        #print 'setting ' + str(self.use_rect_tex_checkbox ) + ' to ' + str(use_rect_tex_value)
        self.use_rect_tex_checkbox.setChecked(use_rect_tex_value)
        rect_tex_color = cmds.getAttr(self.current_chosen_light + '.rectTex')
        rect_tex_color = rect_tex_color[0]
        #print 'rect_tex_color = ',rect_tex_color
        rect_tex_color_r = rect_tex_color[0]
        rect_tex_color_r = (rect_tex_color_r*255)
        #print 'rect_tex_color_r = ',rect_tex_color_r
        rect_tex_color_g = rect_tex_color[1]
        rect_tex_color_g = (rect_tex_color_g*255)
        #print 'rect_tex_color_g = ',rect_tex_color_g
        rect_tex_color_b = rect_tex_color[2]
        rect_tex_color_b = (rect_tex_color_b*255)
        #print 'rect_tex_color_b = ',rect_tex_color_b
        color_string = "rgb(" + str(rect_tex_color_r) + "," + str(rect_tex_color_g) + "," + str(rect_tex_color_b) + ")"
        self.rect_text_color_pushbutton.setStyleSheet("QPushButton { background-color: %s}" %color_string)
        affect_diffuse_value = cmds.getAttr(self.current_chosen_light + '.affectDiffuse')
        #print 'affect_diffuse_value = ',affect_diffuse_value
        #print 'setting ' + str(self.affect_diffuse_checkbox) + ' to ' + str(affect_diffuse_value)
        self.affect_diffuse_checkbox.setChecked(affect_diffuse_value)
        affect_specular_value = cmds.getAttr(self.current_chosen_light + '.affectSpecular')
        #print 'affect_specular_value = ',affect_specular_value
        #print 'setting ' + str(self.affect_specular_checkbox) + ' to ' + str(affect_specular_value)
        self.affect_specular_checkbox.setChecked(affect_specular_value)
        affect_reflection_value = cmds.getAttr(self.current_chosen_light + '.affectReflections')
        #print 'affect_reflection_value = ',affect_reflection_value
        #print 'setting ' + str(self.affect_reflection_checkbox) + ' to ' + str(affect_reflection_value)
        self.affect_reflection_checkbox.setChecked(affect_reflection_value)
        diffuse_contribution_value = cmds.getAttr(self.current_chosen_light + '.diffuseContrib')
        #print 'diffuse_contribution_value = ',diffuse_contribution_value
        #print 'setting ' + str(self.attribute_diffuse_contribution_float_spinbox) + ' to ' + str(diffuse_contribution_value)
        self.attribute_diffuse_contribution_float_spinbox.setValue(diffuse_contribution_value)
        specular_contribution_value = cmds.getAttr(self.current_chosen_light + '.specularContrib')
        #print 'specular_contribution_value = ',specular_contribution_value
        #print 'setting ' + str(self.attribute_specular_contribution_float_spinbox) + ' to ' + str(specular_contribution_value)
        self.attribute_specular_contribution_float_spinbox.setValue(specular_contribution_value)
        self.default_Layer_values()
        self.detect_overrides()
        cmds.editRenderLayerGlobals(currentRenderLayer = self.current_render_layer)

    def render_overrides_prop_UI(self):
        print 'render_overrides_prop_UI'
        self.window_name = "render_overrides_prop"
        if cmds.window(self.window_name,exists = True):
            cmds.deleteUI(self.window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        self.window = QtWidgets.QMainWindow(parent)
        self.window.setObjectName(self.window_name)
        self.window.setWindowTitle(self.window_name)
        #self.window.setFixedSize(1015,300)
        self.window.setFixedWidth(550)
        self.window.setFixedHeight(850)
        self.main_widget = QtWidgets.QWidget()
        self.window.setCentralWidget(self.main_widget)
        self.base_vertical_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_horizontal_layout = QtWidgets.QHBoxLayout(self.main_widget)
        self.base_vertical_layout.addLayout(self.main_horizontal_layout)
        self.button_horizontal_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.base_vertical_layout.addLayout(self.button_horizontal_layout)
        #self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerManagerChange", self.populate_gui])
        #self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["renderLayerChange", self.populate_gui])
        #self.myScriptJobID = cmds.scriptJob(p = self.window_name, event=["NameChanged", self.populate_gui])
        self.light_name_eval()
        self.xforms = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ']
        self.scriptJob_attrs = ['translateX','translateY','translateZ','rotateX','rotateY','rotateZ','scaleX','scaleY','scaleZ','enabled','lightColor','intensityMult','uSize','vSize','directional','useRectTex','rectTex','affectDiffuse','affectSpecular','affectReflections','diffuseContrib','specularContrib']
        for light in self.light_names:
            for attr in self.scriptJob_attrs:
                light_name_attr = light + '.' + attr
                if attr in self.xforms:
                    light_parent = cmds.listRelatives(light,parent = True)
                    light_parent = light_parent[0]
                    light_name_attr = light_parent + '.' + attr
                else:
                    light_name_attr = light + '.' + attr
                #print 'light_name_attr = ',light_name_attr
                #self.myScriptJobID = cmds.scriptJob(attributeChange = [light_name_attr, self.populate_gui])
        self.populate_gui()
        self.window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.window.show()

def main():
    render_overrides_prop_inst = render_overrides_prop()
    render_overrides_prop_inst.render_overrides_prop_UI()

#main()
