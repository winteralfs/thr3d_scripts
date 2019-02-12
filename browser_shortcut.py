import maya.cmds as cmds
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

def website_picker(website_shortcut_combobox):
    chosen_link = website_shortcut_combobox.currentText()

    if chosen_link == 'CAVENDISHFARMS':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=273")
    if chosen_link == 'CLIFBAR':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=274")
    if chosen_link == 'DANNON':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=195")
    if chosen_link == 'DANNONWAVE':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=185")
    if chosen_link == 'DANONE':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=183")
    if chosen_link == 'GSK':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=190")
    if chosen_link == 'KRAFTHEINZCO':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=189")
    if chosen_link == 'Kroger':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=186")
    if chosen_link == 'LEGO':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=307")
    if chosen_link == 'NESTLE':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=159")
    if chosen_link == 'PG':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=187")
    if chosen_link == 'PHILLIPS':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=238")
    if chosen_link == 'POST':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=239")
    if chosen_link == 'PURINA':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=203")
    if chosen_link == 'STONYFIELD':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=204")
    if chosen_link == 'UNILEVER':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=188")
    if chosen_link == 'Wrigley':
        cmds.launch(web="https://thr3dcgi.shotgunstudio.com/page/project_overview?project_id=197")

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
    window.setFixedSize(150,50)
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

browser_link_gui()
