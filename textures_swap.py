import maya.mel as mel
import maya.cmds as cmds
import os
import maya.OpenMayaUI as mui
from PySide2 import QtWidgets,QtCore,QtGui
import shiboken2

class texture_replacer():

    def __init__(self):
        self.triSelect = []

    def refreshHyper(self):
        winds = cmds.lsUI(ed = True,p = True)
        for w in winds:
            if "hyperShadePanel" in w:
                cmds.deleteUI(w, pnl = True)
        mel.eval("HypershadeWindow;")

    def clear(self,listWidget):
        for i in range(listWidget.count()):
            item = listWidget.item(i)
            listWidget.setItemSelected(item, False)

    def oldTexEnable(self):
        textureIconChartSize = self.textureIconChart.count()
        oldSize = self.oldTexBox.count()
        if textureIconChartSize % 2 != 0:
            i = 0
            while i < oldSize:
                it =  self.oldTexBox.item(i)
                it.setFlags(it.flags() | QtCore.Qt.ItemIsSelectable)
                it.setFlags(it.flags() | QtCore.Qt.ItemIsEnabled)
                it.setFlags(it.flags() | QtCore.Qt.ItemIsEditable)
                i = i + 1
        self.oldTexBox.setCurrentIndex(QtCore.QModelIndex())

    def textures_populate(self):
        self.arrowPath = QtGui.QPixmap("U:/cwinters/thumbnails/_arrow.jpg")
        #self.arrowPath = QtGui.QPixmap("/Users/alfredwinters/Desktop/rArrow.png")
        self.textureConversionList = []
        self.texturePointerDic = {}
        self.selFileNodes = []
        self.fileNodeTextureNameDic = {}
        self.texturePathDic = {}
        self.textureNameDic = {}
        self.textureNamePathDic = {}
        self.textureDeleted = ["none"]
        self.textureDeletedP = []
        remNodes = []
        self.lwt = []
        self.new_textureCurrSTR = ""
        self.lowerWinSize = 1
        selNodes = cmds.ls(sl = True)
        for node in selNodes:
            nType = cmds.objectType(node)
            if nType == "file":
                self.selFileNodes.append(node)
        self.fileNodes = cmds.ls(type = "file")
        removeNodes = ["gi_std_lgt","reflection_sdt_lgt","refraction_sdt_lgt"] + self.selFileNodes
        for rNode in removeNodes:
            for node in self.fileNodes:
                if rNode == node:
                    if rNode not in removeNodes:
                        remNodes.append(node)
        for node in self.fileNodes:
            fileTextureName = cmds.getAttr(node + ".fileTextureName")
            ln = len(fileTextureName)
            if ln < 2:
                remNodes.append(node)
        for rn in remNodes:
            rnExists = cmds.objExists(rn)
            if rnExists == 1:
                self.fileNodes.remove(rn)
        for file in self.fileNodes:
            texturePath = cmds.getAttr(file + ".fileTextureName")
            self.texturePathDic[file] = texturePath
            textureName = texturePath.split("/")
            textureName = textureName[-1]
            self.textureNameDic[file] = textureName
            self.fileNodeTextureNameDic[textureName] = file
            self.textureNamePathDic[textureName] = texturePath
        for sfile in self.selFileNodes:
            texturePath = cmds.getAttr(sfile + ".fileTextureName")
            self.texturePathDic[sfile] = texturePath
            textureName = texturePath.split("/")
            textureName = textureName[-1]
            self.textureNameDic[sfile] = textureName
            self.fileNodeTextureNameDic[textureName] = sfile

    def populateBoxes(self):
        self.textures_populate()
        self.newTexBox.clear()
        self.oldTexBox.clear()
        self.selFileNodesRaw = self.selFileNodes
        for selFileNode in self.selFileNodesRaw:
            for  lt in self.lwt:
                node = self.fileNodeTextureNameDic[lt]
                if node == selFileNode:
                    self.selFileNodes.remove(selFileNode)
        for selFileNode in self.selFileNodes:
            imagePath = self.texturePathDic[selFileNode]
            imageName = self.textureNameDic[selFileNode]
            imagePathItem_New = QtWidgets.QListWidgetItem(imageName)
            pixmap_New = QtGui.QPixmap(imagePath)
            pixmap_scaled_New = pixmap_New.scaled(200,200)
            icon_New = QtGui.QIcon()
            icon_New.addPixmap(pixmap_New)
            imagePathItem_New.setIcon(icon_New)
            self.newTexBox.addItem(imagePathItem_New)
        for selFileNode in self.selFileNodes:
            imagePath = self.texturePathDic[selFileNode]
            imageName = self.textureNameDic[selFileNode]
            imagePathItem_old = QtWidgets.QListWidgetItem(imageName)
            pixmap_old = QtGui.QPixmap(imagePath)
            pixmap_scaled_old = pixmap_old.scaled(200,200)
            icon_old = QtGui.QIcon()
            icon_old.addPixmap(pixmap_old)
            imagePathItem_old.setIcon(icon_old)
            self.oldTexBox.addItem(imagePathItem_old)
        lowerWindowTexturesSize = self.textureIconChart.count()
        i = 0
        while i < lowerWindowTexturesSize:
            it =  self.textureIconChart.item(i)
            texture = it.text()
            self.lwt.append(texture)
            i = i + 1
        textureIconChartSize = len(self.lwt)
        newTextBoxSize = self.newTexBox.count()
        lwtSize = len(self.lwt)
        lowerTextTemp = self.lwt
        tmpNewList = []
        i = 0
        while i < newTextBoxSize:
            it =  self.newTexBox.item(i)
            textureNew = it.text()
            tmpNewList.append(textureNew)
            i = i + 1
        LenPrevT = 1
        lenPostT = 1
        lwtSizeTemp = len(lowerTextTemp)
        for lwt in lowerTextTemp:
            lnLwt = len(lwt)
            if lnLwt == 0:
                lowerTextTemp.remove(lwt)
        for tnl in tmpNewList:
            lwtSizeTemp = len(lowerTextTemp)
            a = 0
            while a < lwtSizeTemp:
                tex = lowerTextTemp[a]
                previousT = ""
                postT = ""
                if tex == tnl:
                    if a != 0 and a != 2 and a != 4 and a != 6 and a != 8 and a != 10 and a != 12 and a != 14 and a != 16 and a != 18:
                        prevT = lowerTextTemp[a - 1]
                        lowerTextTemp.remove(prevT)
                    if a != 1 and a != 3 and a != 5 and a != 7 and a != 9 and a != 11 and a != 13 and a != 15 and a != 17 and a != 19:
                        if a != (lwtSizeTemp - 1):
                            postT = lowerTextTemp[a + 1]
                            lowerTextTemp.remove(postT)
                    lowerTextTemp.remove(tnl)
                    lwtSizeTemp = len(lowerTextTemp)
                a = a + 1
        self.lwt = lowerTextTemp
        for t in self.lwt:
            ln = len(t)
            if ln == 0:
                self.lwt.remove(t)
        self.textureIconChart.clear()
        lwtSize = len(self.lwt)
        i = 0
        while i < (lwtSize):
            for l in self.lwt:
                self.textureIconChart.setCurrentRow(i)
                if l != "":
                   for tnpd in self.textureNamePathDic:
                    if l == tnpd:
                        if i == 1 or i == 3 or i == 5 or i == 7 or i == 9 or i == 11:
                            scaleAmountWidth = 30
                            scaleAmountHeight = 134
                            arrowItem = QtWidgets.QListWidgetItem("")
                            arrowPixmap = QtGui.QPixmap(self.arrowPath)
                            arrowPixmap = arrowPixmap.scaled(scaleAmountWidth,scaleAmountHeight)
                            arrowIcon = QtGui.QIcon()
                            arrowIcon.addPixmap(arrowPixmap)
                            arrowItem.setIcon(arrowIcon)
                            self.textureIconChart.addItem(arrowItem)
                            self.textureIconChart.setCurrentRow(i)
                            pth = self.textureNamePathDic[tnpd]
                            scaleAmount = 134
                            pmap = QtGui.QPixmap(pth)
                            pmap_scaled = pmap.scaled(scaleAmount,scaleAmount)
                            Itm = QtWidgets.QListWidgetItem(l)
                            icn = QtGui.QIcon()
                            icn.addPixmap(pmap_scaled)
                            Itm.setIcon(icn)
                            Itm.setFont(QtGui.QFont('SansSerif', 4))
                            self.textureIconChart.addItem(Itm)
                        if i == 0 or i == 2 or i == 4 or i == 6 or i == 8 or i == 10:
                            self.textureIconChart.setCurrentRow(i)
                            pth = self.textureNamePathDic[tnpd]
                            scaleAmount = 134
                            pmap = QtGui.QPixmap(pth)
                            pmap_scaled = pmap.scaled(scaleAmount,scaleAmount)
                            Itm = QtWidgets.QListWidgetItem(l)
                            icn = QtGui.QIcon()
                            icn.addPixmap(pmap_scaled)
                            Itm.setIcon(icn)
                            Itm.setFont(QtGui.QFont('SansSerif', 4))
                            self.textureIconChart.addItem(Itm)
                        i = i + 1
        self.lowerWindowTextures = self.lwt
        textureIconChart_size = self.textureIconChart.count()
        self.textureIconChart.setCurrentIndex(QtCore.QModelIndex())

    def newTextureListChange(self,curr):
        self.lowerWinSize = self.textureIconChart.count()
        if self.lowerWinSize < 30:
            rowPlace = 30
        if self.lowerWinSize < 27:
            rowPlace = 27
        if self.lowerWinSize < 24:
            rowPlace = 24
        if self.lowerWinSize < 21:
            rowPlace = 21
        if self.lowerWinSize < 18:
            rowPlace = 18
        if self.lowerWinSize < 15:
            rowPlace = 15
        if self.lowerWinSize < 12:
            rowPlace = 12
        if self.lowerWinSize < 9:
            rowPlace = 6
        if self.lowerWinSize < 6:
            rowPlace = 3
        if self.lowerWinSize < 3:
            rowPlace = 0
        self.textureIconChart.setCurrentRow(rowPlace)
        curRow = self.textureIconChart.currentRow()
        curItem = self.textureIconChart.currentItem()
        if curItem is not None:
            curItemText = curItem.text()
            self.textureIconChart.takeItem(rowPlace)
            curItemTextLen = len(curItemText)
            if curItemTextLen != 0:
                self.lowerWindowTextures.remove(curItemText)
                oldTextSize = self.oldTexBox.count()
                i = 0
                while i < oldTextSize:
                    it =  self.oldTexBox.item(i)
                    itemText = it.text()
                    if itemText == curItemText:
                        it.setHidden(0)
                        for hid in self.stayHidden:
                            if hid == curItemText:
                                self.stayHidden.remove(curItemText)
                    i = i + 1
        oldTextSize = self.oldTexBox.count()
        i = 0
        while i < oldTextSize:
            it =  self.oldTexBox.item(i)
            it.setFlags(it.flags() | QtCore.Qt.ItemIsSelectable)
            it.setFlags(it.flags() | QtCore.Qt.ItemIsEnabled)
            it.setFlags(it.flags() | QtCore.Qt.ItemIsEditable)
            i = i + 1
        popLowerWindow = len(self.lowerWindowTextures)
        currPointer = curr
        self.currNewTextPointer = curr
        if self.currNewTextPointer is not None:
            self.new_textureCurrSTR = curr.text()
            self.texturePointerDic[self.new_textureCurrSTR] = curr
            self.fileNode_new = self.fileNodeTextureNameDic[self.new_textureCurrSTR]
            self.currItem = QtWidgets.QListWidgetItem(self.new_textureCurrSTR)
            oldTextSize = self.oldTexBox.count()
            i = 0
            while i < oldTextSize:
                it =  self.oldTexBox.item(i)
                itemText = it.text()
                if itemText == self.new_textureCurrSTR:
                    it.setHidden(1)
                    self.currOldTextPointer = it
                    if itemText not in self.stayHidden:
                        self.stayHidden.append(itemText)
                if itemText != self.new_textureCurrSTR:
                   for hid in self.stayHidden:
                        if itemText != hid:
                            for lwt in self.lowerWindowTextures:
                                if itemText != lwt:
                                    it.setHidden(0)
                            for lwt in self.lowerWindowTextures:
                                if itemText == lwt:
                                    print ""
                                    it.setHidden(1)
                it.setSelected(0)
                i = i + 1
        self.oldTexEnable()
        self.populateLowerWindowIcons_New()

    def oldTextureListChange(self,curr):
        self.lowerWinSize = self.textureIconChart.count()
        if self.lowerWinSize == 0:
            oldTexBoxSize = self.oldTexBox .count()
            i = 0
            while i < oldTexBoxSize:
                it =  self.oldTexBox.item(i)
                it.setFlags(it.flags() & ~QtCore.Qt.ItemIsSelectable)
                it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEnabled)
                it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)
                i = i + 1
        if self.new_textureCurrSTR != "":
            self.oldTextureListCurr = curr
            if self.oldTextureListCurr is not None:
                if self.oldTextureListCurr is not None:
                    self.old_textureCurrSTR = curr.text()
                    self.texturePointerDic[self.old_textureCurrSTR] = curr
                    self.fileNode_old = self.fileNodeTextureNameDic[self.old_textureCurrSTR]
                    self.thumbnailNames = [self.new_textureCurrSTR,self.old_textureCurrSTR]
                    self.populateLowerWindowIcons()
                    self.stayHidden.append(self.old_textureCurrSTR)

    def populateLowerWindowIcons_New(self):
        self.lowerWindowTextures.append(self.new_textureCurrSTR)
        scaleAmount = 134
        self.new_pixmap_new = QtGui.QPixmap(self.texturePathDic[self.fileNode_new])
        self.new_pixmap_new_scaled = self.new_pixmap_new .scaled(scaleAmount,scaleAmount)
        self.new_thumbPathItem_1 = QtWidgets.QListWidgetItem(self.new_textureCurrSTR)
        self.new_icon = QtGui.QIcon()
        self.new_icon.addPixmap(self.new_pixmap_new_scaled)
        self.new_thumbPathItem_1.setIcon(self.new_icon)
        self.textureIconChart.addItem(self.new_thumbPathItem_1)
        self.lowerWinSize = self.textureIconChart.count()
        self.new_thumbPathItem_1.setFont(QtGui.QFont('SansSerif', 4))
        self.new_thumbPathItem_1.sizeHint()
        self.oldTexEnable()

    def populateLowerWindowIcons(self):
        if self.lowerWinSize > 0:
            self.lowerWindowTextures.append(self.old_textureCurrSTR)
            TextureToAddBack = "none"
            self.textureDeleted.append(self.old_textureCurrSTR)
            self.textureDeletedP.append(self.oldTextureListCurr)
            oldTextSize = self.oldTexBox.count()
            if self.lowerWinSize == 3 or self.lowerWinSize == 6 or self.lowerWinSize == 9:
                self.textureIconChart.takeItem(self.lowerWinSize - 2)
                self.textureIconChart.takeItem(self.lowerWinSize - 2)
                i = 0
                textureDeleted_size = len(self.textureDeleted)
                if textureDeleted_size > 2:
                    TextureToAddBack = self.textureDeleted[-2]
                    pointerToAddBack = self.textureDeletedP[-2]
                    self.lowerWindowTextures.remove(TextureToAddBack)
                oldTextSize = self.oldTexBox.count()
                i = 0
                while i < oldTextSize:
                    it =  self.oldTexBox.item(i)
                    itemText = it.text()
                    if itemText == TextureToAddBack:
                        it.setHidden(0)
                    i = i + 1
            scaleAmountWidth = 30
            scaleAmountHeight = 134
            arrowItem = QtWidgets.QListWidgetItem("")
            arrowPixmap = QtGui.QPixmap(self.arrowPath)
            arrowPixmap = arrowPixmap.scaled(scaleAmountWidth,scaleAmountHeight)
            arrowIcon = QtGui.QIcon()
            arrowIcon.addPixmap(arrowPixmap)
            arrowItem.setIcon(arrowIcon)
            self.textureIconChart.addItem(arrowItem)

            self.oldPointerList_hide = []
            scaleAmount = 134
            self.textureConversionList.append(self.fileNode_new + "%" +  self.fileNode_old)
            thumbPathItem_2 = QtWidgets.QListWidgetItem(self.old_textureCurrSTR)
            pixmap_old = QtGui.QPixmap(self.texturePathDic[self.fileNode_old])
            pixmap_old_scaled = pixmap_old.scaled(scaleAmount,scaleAmount)
            icon = QtGui.QIcon()
            icon.addPixmap(pixmap_old_scaled)
            thumbPathItem_2.setIcon(icon)
            self.textureIconChart.addItem(thumbPathItem_2)
            thumbPathItem_2.setFont(QtGui.QFont('SansSerif', 4))
            thumbPathItem_2.sizeHint()
            newTextSize = self.newTexBox.count()
            i = 0
            while i < newTextSize:
                it =  self.newTexBox.item(i)
                itemText = it.text()
                if itemText == self.new_textureCurrSTR:
                    it.setHidden(1)
                    self.currNewTextPointer = it
                if itemText == TextureToAddBack:
                    it.setHidden(1)
                    self.currNewTextPointer = it
                i = i + 1
            newTextSize = self.newTexBox.count()
            i = 0
            while i < newTextSize:
                it =  self.newTexBox.item(i)
                itemText = it.text()
                if itemText == self.old_textureCurrSTR:
                    it.setHidden(1)
                    self.currNewTextPointer = it
                if itemText == TextureToAddBack:
                    it.setHidden(0)
                    self.currNewTextPointer = it
                i = i + 1
            oldTextSize = self.oldTexBox.count()
            i = 0
            while i < oldTextSize:
                it =  self.oldTexBox.item(i)
                itemText = it.text()
                if itemText == self.new_textureCurrSTR:
                    it.setHidden(1)
                    self.currOldTextPointer = it
                    self.oldPointerList_hide.append(it)
                i = i + 1
            oldTextSize = self.oldTexBox.count()
            i = 0
            while i < oldTextSize:
                it =  self.oldTexBox.item(i)
                itemText = it.text()
                if itemText == self.old_textureCurrSTR:
                    it.setHidden(1)
                    self.currOldTextPointer = it
                    self.oldPointerList_hide.append(it)
                i = i + 1
        self.lowerWinSize = self.textureIconChart.count()
        self.newTexBox.setCurrentIndex(QtCore.QModelIndex())
        self.textureIconChart.setCurrentIndex(QtCore.QModelIndex())

    def highlightedTexture(self,curr):
        self.lowerWinSize = self.textureIconChart.count()
        self.highlightedTexturePNT = curr
        self.curRow = self.textureIconChart.currentRow()
        self.textureIconChart.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        curSelection = self.textureIconChart.currentRow()
        if curSelection >= 0 and curSelection < 3 and self.lowerWinSize > 1:
            self.textureIconChart.item(0).setSelected(True)
            self.textureIconChart.item(1).setSelected(True)
            self.textureIconChart.item(2).setSelected(True)
        if curSelection == 3 and self.lowerWinSize == 4:
            self.textureIconChart.item(0).setSelected(False)
            self.textureIconChart.item(1).setSelected(False)
            self.textureIconChart.item(2).setSelected(False)
            self.textureIconChart.item(3).setSelected(True)
        if curSelection > 2 and curSelection < 6 and self.lowerWinSize > 4:
            self.textureIconChart.item(3).setSelected(True)
            self.textureIconChart.item(4).setSelected(True)
            self.textureIconChart.item(5).setSelected(True)
        if curSelection == 6 and self.lowerWinSize == 7:
            self.textureIconChart.item(0).setSelected(False)
            self.textureIconChart.item(1).setSelected(False)
            self.textureIconChart.item(2).setSelected(False)
            self.textureIconChart.item(3).setSelected(False)
            self.textureIconChart.item(4).setSelected(False)
            self.textureIconChart.item(5).setSelected(False)
            self.textureIconChart.item(6).setSelected(True)
        if curSelection > 5 and curSelection < 9 and self.lowerWinSize > 7:
            self.textureIconChart.item(6).setSelected(True)
            self.textureIconChart.item(7).setSelected(True)
            self.textureIconChart.item(8).setSelected(True)
        if curSelection == 9 and self.lowerWinSize == 10:
            self.textureIconChart.item(0).setSelected(False)
            self.textureIconChart.item(1).setSelected(False)
            self.textureIconChart.item(2).setSelected(False)
            self.textureIconChart.item(3).setSelected(False)
            self.textureIconChart.item(4).setSelected(False)
            self.textureIconChart.item(5).setSelected(False)
            self.textureIconChart.item(6).setSelected(False)
            self.textureIconChart.item(7).setSelected(False)
            self.textureIconChart.item(8).setSelected(False)
            self.textureIconChart.item(9).setSelected(True)
        if curSelection > 8 and curSelection < 12 and self.lowerWinSize > 10:
            self.textureIconChart.item(6).setSelected(True)
            self.textureIconChart.item(7).setSelected(True)
            self.textureIconChart.item(8).setSelected(True)
        if curSelection == 12 and self.lowerWinSize == 13:
            self.textureIconChart.item(0).setSelected(False)
            self.textureIconChart.item(1).setSelected(False)
            self.textureIconChart.item(2).setSelected(False)
            self.textureIconChart.item(3).setSelected(False)
            self.textureIconChart.item(4).setSelected(False)
            self.textureIconChart.item(5).setSelected(False)
            self.textureIconChart.item(6).setSelected(False)
            self.textureIconChart.item(7).setSelected(False)
            self.textureIconChart.item(8).setSelected(False)
            self.textureIconChart.item(9).setSelected(False)
            self.textureIconChart.item(10).setSelected(False)
            self.textureIconChart.item(11).setSelected(False)
            self.textureIconChart.item(12).setSelected(True)

    def removeItemFromBox(self):
        deletePointers = []
        selList = []
        sizeTextureIconChart = self.textureIconChart.count()
        if self.curRow == 0 and sizeTextureIconChart == 1:
            selList = [0]
        if self.curRow == 0 and sizeTextureIconChart > 1:
            selList = [0,1,2]
        if self.curRow > 0 and self.curRow < 4:
            selList = [0,1,2]
        if self.curRow > 2 and self.curRow < 4:
            selList = [3]
        if self.curRow > 2 and self.curRow < 6:
            selList = [3,4,5]
        if self.curRow > 5 and self.curRow < 7:
            selList = [6]
        if self.curRow > 5 and self.curRow < 9:
            selList = [6,7,8]
        if self.curRow > 8 and self.curRow < 10:
            selList = [9]
        if self.curRow > 8 and self.curRow < 12:
            selList = [9,10,11]
        if self.curRow > 11 and self.curRow < 13:
            selList = [12]
        if self.curRow > 11 and self.curRow < 15:
            selList = [12,13,14]
        if self.curRow > 14 and self.curRow < 16:
            selList = [15]
        if self.curRow > 14 and self.curRow < 18:
            selList = [15,16,17]
        if self.curRow > 17 and self.curRow < 19:
            selList = [18]
        if self.curRow > 17 and self.curRow < 21:
            selList = [18,19,20]
        if self.curRow > 20 and self.curRow < 22:
            selList = [21]
        if self.curRow > 20 and self.curRow < 24:
            selList = [21,22,23]
        if self.curRow > 23 and self.curRow < 25:
            selList = [24]
        if self.curRow > 23 and self.curRow < 27:
            selList = [24,25,26]
        if self.curRow > 26 and self.curRow < 28:
            selList = [27]
        if self.curRow > 26 and self.curRow < 30:
            selList = [27,28,29]
        selList.reverse()
        for sel in selList:
            self.textureIconChart.setCurrentRow(sel)
            curItem = self.textureIconChart.currentItem()
            if curItem is not None:
                curItemText = curItem.text()
                newTextSize = self.newTexBox.count()
                i = 0
                while i < newTextSize:
                    it =  self.newTexBox.item(i)
                    itemText = it.text()
                    if itemText == curItemText:
                        it.setHidden(0)
                        it.setSelected(0)
                    i = i + 1
                oldTextSize = self.oldTexBox.count()
                i = 0
                while i < oldTextSize:
                    it =  self.oldTexBox.item(i)
                    itemText = it.text()
                    if itemText == curItemText:
                        it.setHidden(0)
                        it.setSelected(0)
                    i = i + 1
                deletePointers.append(curItem)
                textureBeingDeleted = curItem.text()
                for lowWinTex in self.lowerWindowTextures:
                    if lowWinTex == textureBeingDeleted:
                        self.lowerWindowTextures.remove(textureBeingDeleted)
            for pointer in deletePointers:
                TI = self.textureIconChart.takeItem(self.textureIconChart.row(pointer))
        self.lowerWindowTextures = []
        lowerWindowTexturesSize = self.textureIconChart.count()
        i = 0
        while i < lowerWindowTexturesSize:
            it =  self.textureIconChart.item(i)
            texture = it.text()
            self.lowerWindowTextures.append(texture)
            i = i + 1
        self.lowerWindowTextures
        self.oldTexEnable()
        self.newTexBox.setCurrentIndex(QtCore.QModelIndex())
        self.textureIconChart.setCurrentIndex(QtCore.QModelIndex())

    def fCheckLaunch(self,curr):
        fCheckText = curr.text()
        if fCheckText != "":
            nodeName = self.fileNodeTextureNameDic[fCheckText]
            fCheckTexPath = self.texturePathDic[nodeName]
            cmds.fcheck(fCheckTexPath)

    def texture_linker_UI(self):
        self.stayHidden = []
        self.lowerWindowTextures = []
        windowName = "texture_swap"
        if cmds.window(windowName,exists = True):
            cmds.deleteUI(windowName, wnd = True)
        pointer = mui.MQtUtil.mainWindow()
        parent = shiboken2.wrapInstance(long(pointer),QtWidgets.QWidget)
        window = QtWidgets.QMainWindow(parent)
        window.setObjectName(windowName)
        window.setWindowTitle(windowName)
        self.myScriptJobID = cmds.scriptJob(p = windowName, event=["SelectionChanged", self.populateBoxes])
        window.setMinimumSize(450,650)
        window.setMaximumSize(600,400)
        mainWidget = QtWidgets.QWidget()
        window.setCentralWidget(mainWidget)
        verticalLayout = QtWidgets.QVBoxLayout(mainWidget)
        TextureLabelLayout = QtWidgets.QHBoxLayout()
        verticalLayout.addLayout(TextureLabelLayout)
        newTextureLabel = QtWidgets.QLabel("new texture")
        newTextureLabel.setAlignment(QtCore.Qt.AlignCenter)
        oldTextureLabel = QtWidgets.QLabel("old texture")
        oldTextureLabel.setAlignment(QtCore.Qt.AlignCenter)
        TextureLabelLayout.addWidget(newTextureLabel)
        TextureLabelLayout.addWidget(oldTextureLabel)
        textureBoxLayout = QtWidgets.QHBoxLayout()
        verticalLayout.addLayout(textureBoxLayout)
        self.textures = self.textures_populate()
        self.newTexBox = QtWidgets.QListWidget()
        textureBoxLayout.addWidget(self.newTexBox)
        self.newTexBox.setObjectName("newTexBox")
        self.oldTexBox = QtWidgets.QListWidget()
        textureBoxLayout.addWidget(self.oldTexBox)
        self.oldTexBox.setObjectName("oldTexBox")
        self.newTexBox.setIconSize(QtCore.QSize(35,35))
        self.oldTexBox.setIconSize(QtCore.QSize(35,35))
        self.newTexBox.setStyleSheet('QListWidget {background-color: #000000; color: #B0E0E6;}')
        self.oldTexBox.setStyleSheet('QListWidget {background-color: #000000; color: #B0E0E6;}')
        selItems = self.newTexBox.selectedItems()
        self.textureIconChartLayout = QtWidgets.QVBoxLayout()
        textureIconsLayout = QtWidgets.QHBoxLayout()
        self.textureIconChartLayout.addLayout(textureIconsLayout)
        verticalLayout.addLayout(self.textureIconChartLayout)
        self.textureIconChart = QtWidgets.QListWidget()
        self.textureIconChart.setStyleSheet('QListWidget {background-color: #000000; color: #B0E0E6;}')
        self.textureIconChart.setViewMode(QtWidgets.QListWidget.IconMode)
        self.textureIconChart.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.size = 600
        self.textureIconChart.setIconSize(QtCore.QSize(self.size, self.size))
        self.textureIconChart.setIconSize(QtCore.QSize(self.size, self.size))
        self.textureIconChart.setDragEnabled(0)
        self.textureIconChart.setMaximumWidth(321)
        textureIconsLayout.addWidget(self.textureIconChart)
        curItem = self.newTexBox.currentItem()
        self.oldTexBox.itemClicked.connect(self.oldTextureListChange)
        self.newTexBox.itemClicked.connect(self.newTextureListChange)
        self.textureIconChart.itemPressed.connect(self.highlightedTexture)
        self.textureIconChart.itemDoubleClicked.connect(self.fCheckLaunch)
        remButtonLayout = QtWidgets.QHBoxLayout()
        verticalLayout.addLayout(remButtonLayout)
        removeBtn = QtWidgets.QPushButton('remove textures')
        remButtonLayout.addWidget(removeBtn)
        removeBtn.clicked.connect(self.removeItemFromBox)
        removeBtn.setShortcut("Backspace")
        removeBtn.setFixedSize(0,0)
        buttonLayout = QtWidgets.QVBoxLayout()
        verticalLayout.addLayout(buttonLayout)
        replaceBtn = QtWidgets.QPushButton('swap textures')
        replaceBtn.setStyleSheet("background-color:rgb(0,100,255)")
        replaceBtn.setFixedHeight(50)
        buttonLayout.addWidget(replaceBtn)
        replaceBtn.clicked.connect(self.textureReplace)
        self.populateBoxes()
        fg = window.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        window.move(fg.topLeft())
        window.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        window.show()

        self.newTexBox.setCurrentIndex(QtCore.QModelIndex())
        oldTexBoxSize = self.oldTexBox .count()
        i = 0
        while i < oldTexBoxSize:
            it =  self.oldTexBox.item(i)
            it.setFlags(it.flags() & ~QtCore.Qt.ItemIsSelectable)
            it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEnabled)
            it.setFlags(it.flags() & ~QtCore.Qt.ItemIsEditable)
            i = i + 1


    def textureReplace(self):
        for texturePair in self.textureConversionList:
            #splitting out the old and new texture names
            texturePair = texturePair.split("%")
            new_fileTex = texturePair[0]
            old_fileTex = texturePair[1]
            print " "
            print "---"
            print "self.textureConversionList = ",self.textureConversionList
            print new_fileTex + " swapping " + old_fileTex
            print "---"
            #starting the replace
            source_connections_modified = []
            destination_connections_modified = []
            #grab the old texure incoming connections
            connections_source_old = cmds.listConnections(old_fileTex, plugs = True, connections = True, destination = False)or []
            #grab the old texure outgoing connections
            connections_destination_old = cmds.listConnections(old_fileTex, connections = True, plugs = True, source = False) or []
            #how many incoming connections and outgoing connections are there
            connection_source_size = len(connections_source_old)
            connection_destination_size = len(connections_destination_old)
            #if the incoming connections source size is more than 0, replace the old texture in the incoming connections list
            if connection_source_size != 0:
                for connection in connections_source_old:
                    connection_modified = connection.replace(old_fileTex,new_fileTex)
                    source_connections_modified.append(connection_modified)
            #if the outgoing connections size is more than 0, replace the old texture in the outgoing connections list
            if connection_destination_size != 0:
                for connection in connections_destination_old:
                    connection_modified = connection.replace(old_fileTex,new_fileTex)
                    destination_connections_modified.append(connection_modified)
            source_connections_modified_size = len(source_connections_modified)
            #connect the old source node to the new texture
            inIter = 0
            outIter = 1
            while outIter < source_connections_modified_size:
                if connections_source_old[outIter] != "defaultColorMgtGlobals.cmEnabled" and connections_source_old[outIter] != "defaultColorMgtGlobals.configFileEnabled" and connections_source_old[outIter] != "defaultColorMgtGlobals.configFilePath" and connections_source_old[outIter] != "defaultColorMgtGlobals.workingSpaceName":
                    print "connecting " + connections_source_old[outIter] + " to "  + source_connections_modified[inIter]
                    cmds.connectAttr(connections_source_old[outIter],source_connections_modified[inIter],force = True)
                outIter = outIter + 2
                inIter = inIter + 2
            destination_connections_modified_size = len(destination_connections_modified)
            #connect the new texture to the old destination node
            inIter = 0
            outIter = 1
            while outIter < destination_connections_modified_size:
                if ".message" not in destination_connections_modified[inIter]:
                    print "connecting " + destination_connections_modified[inIter] + " to " + connections_destination_old[outIter]
                    cmds.connectAttr(destination_connections_modified[inIter],connections_destination_old[outIter], force = True)
                outIter = outIter + 2
                inIter = inIter + 2
            #transferAttr settings for new texture
            old_file_texture_attr_dic = {}
            new_file_texture_attr_dic = {}
            old_file_texture_attrs = cmds.listAttr(old_fileTex,k = True)
            attrAppend = ["filter","filterOffset","filterType"]
            attrRemove = ["aiUserOptions","defaultColorMgtGlobals.cmEnabled","defaultColorMgtGlobals.configFileEnabled","defaultColorMgtGlobals.configFilePath","workingSpaceName"]
            for attr in attrAppend:
                old_file_texture_attrs.append(attr)
            for attr in attrRemove:
                if attr in old_file_texture_attrs:
                    old_file_texture_attrs.remove(attr)
            new_file_texture_attrs = cmds.listAttr(new_fileTex,k = True)
            for attr in attrAppend:
                new_file_texture_attrs.append(attr)
            for attr in attrRemove:
                if attr in new_file_texture_attrs:
                    new_file_texture_attrs.remove(attr)
            for oldFileAttr in old_file_texture_attrs:
                oldFileAttrValue = cmds.getAttr(old_fileTex + "." + oldFileAttr)
                old_file_texture_attr_dic[oldFileAttr] = oldFileAttrValue
            for new_fileTexAttr in new_file_texture_attrs:
                new_fileTexAttr_Value = cmds.getAttr(new_fileTex + "." + new_fileTexAttr)
                new_file_texture_attr_dic[new_fileTexAttr] = new_fileTexAttr_Value
            for new_fileTexAttr in new_file_texture_attrs:
                if new_fileTexAttr in new_file_texture_attr_dic:
                    attrExists = cmds.attributeQuery(new_fileTexAttr,node = new_fileTex,exists = True)
                    if attrExists == 1:
                        print "setting " + str(new_fileTex) + "." + str(new_fileTexAttr) + " to " + str(old_file_texture_attr_dic[new_fileTexAttr])
                        cmds.setAttr(new_fileTex + "." + new_fileTexAttr,old_file_texture_attr_dic[new_fileTexAttr])
        self.textureIconChart.clear()
        self.newTexBox.clear()
        self.textures_populate()
        cmds.select(clear = True)
        #self.refreshHyper()

tr = texture_replacer()

def main():
    tr.texture_linker_UI()

main()
