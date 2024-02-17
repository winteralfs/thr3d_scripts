import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2
from functools import partial

print('')
print('node name cleaner')
print('')

def changeText(text_input):
   currentText = text_input.text()

def replace_text(text_input):
   
    current_text = text_input.text()

    print("removing '" + current_text + "' from node names" )
    print('')

    name_list = []
    
    types = ['ramp','place2dTexture','multiplyDivide','surfaceShader','layeredTexture','transform','VRayLightRectShape','VRayLightRectShape','VRayLightDome', 
             'VRayLightDomeShape','blinn','lambert','phong','VRayMtl','VRayLightMesh','renderLayer','VRayLightMtl','gammaCorrect','VRaySoftbox']

    nodes = cmds.ls()  
    
    for node in nodes:
        if current_text in node:
            name_list.append(node)

    for _ in name_list:
        
        nodes = cmds.ls(long = True)
        
        for node in nodes:
            type = cmds.nodeType(node)
            if type in types:
                if current_text in node:
                    new_name = node.replace(current_text, '')
                    new_name_split = new_name.split('_')
                    new_name = ''
                    for split in new_name_split:
                        if split.isalpha():
                            new_name = new_name + '_' + split
                            if new_name[0] == '_':
                                new_name = new_name[1:]
                            if new_name[-1] == '_':
                                new_name = new_name[:-1]
                    cmds.rename(node, new_name)            
                    break          

def prefix_suffix_replace_gui():
        window_name = "node name cleaner"
        if cmds.window(window_name,exists = True):
                cmds.deleteUI(window_name, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(int(pointer),QtWidgets.QWidget)    
        window = QtWidgets.QMainWindow(parent)    
        window.setObjectName(window_name)
        window.setWindowTitle(window_name)
        main_widget = QtWidgets.QWidget()
        window.setCentralWidget(main_widget)
        window.setFixedWidth(310)
        window.setFixedHeight(90)
        window.main_box_layout = QtWidgets.QVBoxLayout(main_widget)
        window.main_box_layout.setAlignment(QtCore.Qt.AlignTop)
        window.text_input_layout = QtWidgets.QVBoxLayout(main_widget)
        window.button_grid_layout = QtWidgets.QGridLayout(main_widget)
        window.lower_button_grid_layout = QtWidgets.QGridLayout(main_widget)
        window.main_box_layout.addLayout(window.text_input_layout)
        window.main_box_layout.addLayout(window.button_grid_layout)
        window.main_box_layout.addLayout(window.lower_button_grid_layout)
        spacing = 1
        text_input = QtWidgets.QLineEdit()
        text_input.setFixedSize(295,30)
        
        text_input.setText('pasted')
        window.text_input_layout.addWidget(text_input)
        currentText = text_input.editingFinished.connect(lambda:changeText(text_input))

        button_replace_text = QtWidgets.QPushButton("remove")
        window.button_grid_layout.addWidget(button_replace_text,0,0)
        button_replace_text.pressed.connect(lambda:replace_text(text_input)) 

        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

def prefix_suffix_replace():
        prefix_suffix_replace_gui()

prefix_suffix_replace()
