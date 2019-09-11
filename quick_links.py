"""

.. image:: U:/cwinters/docs/build/html/_images/quick_links/quick_links_lighting_shelf.JPG
   :align: center
   :scale: 75%

.. image:: U:/cwinters/docs/build/html/_images/quick_links/quick_links.JPG
   :align: center
   :scale: 75%

Quick_links is a simple GUI to navigate to the 2018 version of brand's Shotgun pages.
"""


import maya.cmds as cmds
import maya.mel as mel
import os
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2
import webbrowser

def website_picker(website_shortcut_combobox):
    chosen_link = website_shortcut_combobox.currentText()

    if chosen_link == 'CAVENDISHFARMS':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=273")
    if chosen_link == 'CLIFBAR':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=274")
    if chosen_link == 'DANNON':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=195")
    if chosen_link == 'DANNONWAVE':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=185")
    if chosen_link == 'DANONE':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=183")
    if chosen_link == 'GSK':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=190")
    if chosen_link == 'KRAFTHEINZCO':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=189")
    if chosen_link == 'KROGER':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=186")
    if chosen_link == 'LEGO':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=307")
    if chosen_link == 'NESTLE':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=159")
    if chosen_link == 'PG':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=187")
    if chosen_link == 'PHILLIPS':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=238")
    if chosen_link == 'POST':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=239")
    if chosen_link == 'PURINA':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=203")
    if chosen_link == 'STONYFIELD':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=204")
    if chosen_link == 'UNILEVER':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=188")
    if chosen_link == 'WRIGLEY':
        webbrowser.open("https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=197")

def browser_link_gui():
    links = ['CAVENDISHFARMS','CLIFBAR','DANONE','DANNON','DANNONWAVE','GSK','KRAFTHEINZCO','KROGER','LEGO','NESTLE','PG','PHILLIPS','POST','PURINA','STONYFIELD','UNILEVER','WRIGLEY']
    windowName = "link_shortcuts"
    if cmds.window(windowName,exists = True):
        cmds.deleteUI(windowName, wnd = True)
    pointer = mui.MQtUtil.mainWindow()
    parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
    window = QtWidgets.QMainWindow(parent)
    window.setObjectName(windowName)
    window.setWindowTitle(windowName)
    window.setFixedSize(250,50)
    mainWidget = QtWidgets.QWidget()
    window.setCentralWidget(mainWidget)
    vertical_layout_main = QtWidgets.QVBoxLayout(mainWidget)
    website_shortcut_combobox = QtWidgets.QComboBox()
    website_shortcut_combobox.setMaximumHeight(30)
    vertical_layout_main.addWidget(website_shortcut_combobox)
    for link in links:
        website_shortcut_combobox.addItem(link)
    website_shortcut_combobox.activated[str].connect(lambda:website_picker(website_shortcut_combobox))
    window.show()

def main():
    browser_link_gui()

#main()
