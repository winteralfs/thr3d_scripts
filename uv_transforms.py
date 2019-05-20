"""
lighting_shelf: uv_editor
********************************************
"""


import maya.cmds as cmds
from functools import partial
import random

sel = cmds.ls(sl = 1)
siz = len(sel)
if siz == 0:
	print "**NOTHING SELECTED**"
else:
	print sel

Pu = .5
Pv = .5

global countMyU_D
countMyU_D = {}

global changeMyU_D
changeMyU_D = {}

global countMyV_D
countMyV_D = {}

global changeMyV_D
changeMyV_D = {}

global countMySU_D
countMySU_D = {}
global changeMySU_D
changeMySU_D = {}

global countMySV_D
countMySV_D = {}
global changeMySV_D
changeMySV_D = {}

global countMyA_D
countMyA_D = {}
global changeMyA_D
changeMyA_D = {}

def F_MyU(mffuVal, locSelFunc, selo):

    print "     "
    print "-----"
    print "     "

    global countMyU_D
    print "countMyU_D = ", countMyU_D
    global changeMyU_D
    print "changeMyU = ", changeMyU_D

    cmds.select(clear = True)
    cmds.select(selo)

    MyU_countKey = (locSelFunc + "_MyU_count")

    print " MyU_countKey = ", MyU_countKey
    print " countMyU_D = ", countMyU_D

    if MyU_countKey in countMyU_D:
        print MyU_countKey, " exists"
    else:
        countMyU_D[MyU_countKey] = 0

    print "countMyU_D = ", countMyU_D

    countMyU = countMyU_D[MyU_countKey]
    countMyUadj = (countMyU - 1)

    MyU = mffuVal
    MyU = float(MyU)

    print locSelFunc
    print "F_MyU = ", mffuVal
    print "countMyUadj =", countMyUadj

    changeMyUdictkey = (locSelFunc + "_" + str(countMyU))
    changeMyUdictkeyAdj = (locSelFunc + "_" + str(countMyUadj))

    print  "changeMyUdictkey = ", changeMyUdictkey
    changeMyU_D[changeMyUdictkey] = (mffuVal * -1)
    print "changeMyU_D = ", changeMyU_D[changeMyUdictkey], ",key = ", changeMyUdictkey

    if(countMyU<1):
        changeMyU = changeMyU_D[changeMyUdictkey]
        print "if_changeMyU = ", changeMyU
        print "if_changeMyU_D = ", changeMyU_D
    else:
        changeMyU = changeMyU_D[changeMyUdictkeyAdj]
        print "else_changeMyU = ", changeMyU
        print "else_changeMyU_D = ", changeMyU_D

    if countMyU < 1:
        print "if_MyU", MyU
        cmds.polyEditUV (pu = Pu, pv = Pv, u = MyU, v = 0)
        print "if changeMyU", changeMyU

    else:
        print "else_MyU", MyU
        cmds.polyEditUV (pu = Pu, pv = Pv, u = changeMyU, v = 0)
        cmds.polyEditUV (pu = Pu, pv = Pv, u = MyU, v = 0)
        print "else changeMyU", changeMyU

    tempCount = countMyU_D[MyU_countKey]
    countMyU_D[MyU_countKey] = tempCount + 1

    print "countMyU = ", countMyU
    print "     "
    print "-----"
    print "     "
    return changeMyU;

def F_MyV(mffvVal, locSelFunc, selo):

    print "     "
    print "-----"
    print "     "

    global countMyV_D
    print "countMyV = ", countMyV_D
    global changeMyV_D
    print "changeMyV = ", changeMyV_D

    cmds.select(clear = True)
    cmds.select(selo)

    MyV_countKey = (locSelFunc + "_MyV_count")

    print " MyV_countKey = ", MyV_countKey
    print " countMyV_D = ", countMyV_D

    if MyV_countKey in countMyV_D:
        print MyV_countKey, " exists"
    else:
        countMyV_D[MyV_countKey] = 0

    print "countMyV_D = ", countMyV_D

    countMyV = countMyV_D[MyV_countKey]
    countMyVadj = (countMyV - 1)

    MyV = mffvVal
    MyV = float(MyV)

    print locSelFunc
    print "F_MyV = ", mffvVal
    print "countMyVadj =", countMyVadj

    changeMyVdictkey = (locSelFunc + "_" + str(countMyV))
    changeMyVdictkeyAdj = (locSelFunc + "_" + str(countMyVadj))

    print  "changeMyVdictkey = ", changeMyVdictkey
    changeMyV_D[changeMyVdictkey] = (mffvVal * -1)
    print "changeMyV_D = ", changeMyV_D[changeMyVdictkey], ",key = ", changeMyVdictkey


    if(countMyV<1):
        changeMyV = changeMyV_D[changeMyVdictkey]
        print "if_changeMyV = ", changeMyV
        print "if_changeMyV_D = ", changeMyV_D
    else:
        changeMyV = changeMyV_D[changeMyVdictkeyAdj]
        print "else_changeMyV = ", changeMyV
        print "else_changeMyV_D = ", changeMyV_D

    if countMyV < 1:
        print "if_MVV", MyV
        cmds.polyEditUV (pu = Pu, pv = Pv, u = 0, v = MyV)
        print "if changeMyV", changeMyV

    else:
        print "else_MyV", MyV
        cmds.polyEditUV (pu = Pu, pv = Pv, u = 0, v = changeMyV)
        cmds.polyEditUV (pu = Pu, pv = Pv, u = 0, v = MyV)
        print "else changeMyV", changeMyV

    tempCount = countMyV_D[MyV_countKey]
    countMyV_D[MyV_countKey] = tempCount + 1

    print "countMyV = ", countMyV
    print "     "
    print "-----"
    print "     "
    return countMyV;

def F_MySU(mffsuVal, mffuVal, mffvVal, mffaVal, locSelFunc, selo):

    print "     "
    print "-----"
    print "     "

    global countMySU_D
    print "countMySU_D = ", countMySU_D
    global changeMySU_D
    print "changeMySU = ", changeMySU_D

    cmds.select(clear = True)
    cmds.select(selo)

    MySU_countKey = (locSelFunc + "_MySU_count")

    print locSelFunc
    print "F_MySU = ", mffsuVal

    if MySU_countKey in countMySU_D:
        print MySU_countKey, " exists"
    else:
        countMySU_D[MySU_countKey] = 0

    print "countMySU_D = ", countMySU_D

    countMySU = countMySU_D[MySU_countKey]
    countMySUadj = (countMySU - 1)

    MyU = mffuVal
    MyV = mffvVal

    MySU = mffsuVal
    MySU = float(MySU)

    if MySU == 0:
        MySU = .001

    MyA = mffaVal

    print locSelFunc
    print "F_MySU = ", mffsuVal
    print "countMySUadj =", countMySUadj

    changeMySUdictkey = (locSelFunc + "_" + str(countMySU))
    changeMySUdictkeyAdj = (locSelFunc + "_" + str(countMySUadj))

    print  "changeMySUdictkey = ", changeMySUdictkey
    changeMySU_D[changeMySUdictkey] = (float(MySU)/(MySU*MySU))
    print "changeMySU_D = ", changeMySU_D[changeMySUdictkey], ",key = ", changeMySUdictkey

    if(countMySU<1):
        changeMySU = changeMySU_D[changeMySUdictkey]
        print "if_changeMySU = ", changeMySU
        print "if_changeMySU_D = ", changeMySU_D
    else:
        changeMySU = changeMySU_D[changeMySUdictkeyAdj]
        print "else_changeMySU = ", changeMySU
        print "else_changeMySU_D = ", changeMySU_D


    if countMySU < 1:
        print "if_MySU", MySU

        if MySU !=0:
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), su = MySU, sv = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySU", changeMySU

        else:
            MySU = .0001
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), su = MySU, sv = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySU", changeMySU

    else:
        print "else_MySU", MySU

        if MySU != 0:
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), su = changeMySU, sv = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), su = MySU, sv = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySU", changeMySU

        else:
            MySU = .0001
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), su = changeMySU, sv = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), su = MySU, sv = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySU", changeMySU

    tempCount = countMySU_D[MySU_countKey]
    countMySU_D[MySU_countKey] = tempCount + 1

    print "countMySU = ", countMySU
    print "     "
    print "-----"
    print "     "
    return countMySU;

def F_MySV(mffsvVal, mffuVal, mffvVal, mffaVal, locSelFunc, selo):

    print "     "
    print "-----"
    print "     "

    global countMySV_D
    print "countMySV_D = ", countMySV_D
    global changeMySV_D
    print "chang1eMySV = ", changeMySV_D

    cmds.select(clear = True)
    cmds.select(selo)

    MySV_countKey = (locSelFunc + "_MySV_count")

    print locSelFunc
    print "F_MySV = ", mffsvVal

    if MySV_countKey in countMySV_D:
        print MySV_countKey, " exists"
    else:
        countMySV_D[MySV_countKey] = 0

    print "countMySV_D = ", countMySV_D

    countMySV = countMySV_D[MySV_countKey]
    countMySVadj = (countMySV - 1)

    MyU = mffuVal
    MyV = mffvVal

    MySV = mffsvVal
    MySV = float(MySV)

    if MySV == 0:
        MySV = .001

    MyA = mffaVal

    print locSelFunc
    print "F_MySV = ", mffsvVal
    print "countMySVadj =", countMySVadj

    changeMySVdictkey = (locSelFunc + "_" + str(countMySV))
    changeMySVdictkeyAdj = (locSelFunc + "_" + str(countMySVadj))

    print  "changeMySVdictkey = ", changeMySVdictkey
    changeMySV_D[changeMySVdictkey] = (float(MySV)/(MySV*MySV))
    print "changeMySV_D = ", changeMySV_D[changeMySVdictkey], ",key = ", changeMySVdictkey

    if(countMySV<1):
        changeMySV = changeMySV_D[changeMySVdictkey]
        print "if_changeMySV = ", changeMySV
        print "if_changeMySV_D = ", changeMySV_D
    else:
        changeMySV = changeMySV_D[changeMySVdictkeyAdj]
        print "else_changeMySU = ", changeMySV
        print "else_changeMySU_D = ", changeMySV_D


    if (countMySV<1):
        print "if_MySV", MySV

        if MySV !=0:
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), sv = MySV, su = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySV", changeMySV

        else:
            MySV = .0001
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), sv = MySV, su = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySV", changeMySV

    else:
        print "else_MySV", MySV

        if MySV != 0:
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), sv = changeMySV, su = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), sv = MySV, su = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySV", changeMySV

        else:
            MySV = .0001
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*1))
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), sv = changeMySV, su = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), sv = MySV, su = 1)
            cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA*-1))
            print "if changeMySV", changeMySV

    tempCount = countMySV_D[MySV_countKey]
    countMySV_D[MySV_countKey] = tempCount + 1

    print "countMySV = ", countMySV
    print "     "
    print "-----"
    print "     "
    return countMySV;

def F_MyA(mffaVal, mffuVal, mffvVal, locSelFunc, selo):

    print "     "
    print "-----"
    print "     "

    global countMyA_D

    cmds.select(clear = True)
    cmds.select(selo)

    MyA_countKey = (locSelFunc + "_MyA_count")

    print locSelFunc
    print "F_MyA = ", mffaVal

    if MyA_countKey in countMyA_D:
        print MyA_countKey, " exists"
    else:
        countMyA_D[MyA_countKey] = 0

    print "countMyA_D = ", countMyA_D

    countMyA = countMyA_D[MyA_countKey]
    countMyAadj = (countMyA - 1)

    MyU = mffuVal
    MyV = mffvVal
    MyA = (mffaVal * -1)

    print locSelFunc
    print "F_MyA = ", mffaVal

    print locSelFunc
    print "F_MyA = ", mffaVal
    print "countMyAadj =", countMyAadj

    changeMyAdictkey = (locSelFunc + "_" + str(countMyA))
    changeMyAdictkeyAdj = (locSelFunc + "_" + str(countMyAadj))

    print  "changeMyAdictkey = ", changeMyAdictkey
    changeMyA_D[changeMyAdictkey] = (float(MyA*-1))
    print "changeMyA_D = ", changeMyA_D[changeMyAdictkey], ",key = ", changeMyAdictkey

    if(countMyA<1):
        changeMyA = changeMyA_D[changeMyAdictkey]
        print "if_changeMyA_D = ", changeMyA_D
        print "if_changeMyA_D = ", changeMyA_D
    else:
        changeMyA = changeMyA_D[changeMyAdictkeyAdj]
        print "else_changeMyA_D = ", changeMyA_D
        print "else_changeMyA_D = ", changeMyA_D
    if(countMyA<1):
        changeMyA = changeMyA_D[changeMyAdictkey]
        print "if_changeMyA_D = ", changeMyA_D
        print "if_changeMyA_D = ", changeMyA_D
    else:
        changeMyA = changeMyA_D[changeMyAdictkeyAdj]
        print "else_changeMyA_D = ", changeMyA_D
        print "else_changeMyA_D = ", changeMyA_D

    if countMyA < 1:
        MyA = MyA
        print "if_A", MyA
        cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA))
        print "if changeMyA", changeMyA

    else:
        MyA = MyA
        print "else changeMyA", changeMyA
        print "else_A", MyA
        cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = changeMyA)
        cmds.polyEditUV (pu = (MyU + Pu), pv = (MyV + Pv), a = (MyA))

    tempCount = countMyA_D[MyA_countKey]
    countMyA_D[MyA_countKey] = tempCount + 1

    print "countMyA = ", countMyA
    print "     "
    print "-----"
    print "     "
    return countMyA;


def UVeditWin():
    if siz > 0:
        name = sel[0]
        windowName = "UVeditor"
        locSel = name
        selo = cmds.ls(sl = True)
        windowSize = (300,100)
        if (cmds.window(windowName, exists = True)):
            cmds.deleteUI(windowName)
        window = cmds.window(windowName, title = sel[0], widthHeight=(windowSize[0],windowSize[1]),sizeable = False)
        nameB = name.replace("[","a")
        nameB = nameB.replace("]","a")
        nameB = nameB.replace(".","a")
        cmds.columnLayout("mainColumn", adjustableColumn = True)
        cmds.rowLayout("nameRowLayout01", numberOfColumns = 3, parent = "mainColumn")
        cmds.text("translate ")
        myFloatField_U_path = cmds.floatField((nameB + "mFFu"), value = 0,ec = lambda x:mFFu_func(x), parent = "nameRowLayout01")
        myFloatField_V_path = cmds.floatField((nameB + "mFFv"), value = 0,ec = lambda x:mFFv_func(x), parent = "nameRowLayout01")
        myFloatField_V_path
        cmds.rowLayout("nameRowLayout02", numberOfColumns = 3, parent = "mainColumn")
        cmds.text("scale       ")
        myFloatField_SU_path = cmds.floatField((nameB + "mFFsu"), value = 1,ec = lambda x:mFFsu_func(x), parent = "nameRowLayout02")
        myFloatField_SV_path = cmds.floatField((nameB + "mFFsv"), value = 1,ec = lambda x:mFFsv_func(x), parent = "nameRowLayout02")
        cmds.rowLayout("nameRowLayout03", numberOfColumns = 2, parent = "mainColumn")
        cmds.text("rotate     ")
        myFloatField_A_path = cmds.floatField((nameB + "mFFa"), value = 0,ec = lambda x:mFFa_func(x), parent = "nameRowLayout03")
        cmds.rowLayout("nameRowLayout04", numberOfColumns = 5, parent = "mainColumn")
	cmds.showWindow()

    def mFFu_func(myFloatField_U_path):
        locSelFunc = locSel
        mffuVal = cmds.floatField((nameB + "mFFu"), q = 1, v = 1)
        print "mffu = ", mffuVal
        F_MyU(mffuVal, locSelFunc, selo)

    def mFFv_func(myFloatField_v_path):
        locSelFunc = locSel
        mffvVal = cmds.floatField((nameB + "mFFv"), q = 1, v = 1)
        print "mffv = ", mffvVal
        F_MyV(mffvVal, locSelFunc, selo)

    def mFFsu_func(myFloatField_su_path):
        locSelFunc = locSel
        mffsuVal = cmds.floatField((nameB + "mFFsu"), q = 1, v = 1)
        mffuVal = cmds.floatField((nameB + "mFFu"), q = 1, v = 1)
        mffvVal = cmds.floatField((nameB + "mFFv"), q = 1, v = 1)
        mffaVal = cmds.floatField((nameB + "mFFa"), q = 1, v = 1)
        print "mffsu = ", mffsuVal
        F_MySU(mffsuVal, mffuVal, mffvVal, mffaVal, locSelFunc, selo)

    def mFFsv_func(myFloatField_sv_path):
        locSelFunc = locSel
        mffsvVal = cmds.floatField((nameB + "mFFsv"), q = 1, v = 1)
        mffuVal = cmds.floatField((nameB + "mFFu"), q = 1, v = 1)
        mffvVal = cmds.floatField((nameB + "mFFv"), q = 1, v = 1)
        mffaVal = cmds.floatField((nameB + "mFFa"), q = 1, v = 1)
        print "mffsv = ", mffsvVal
        F_MySV(mffsvVal, mffuVal, mffvVal, mffaVal, locSelFunc, selo)

    def mFFa_func(myFloatField_a_path):
        locSelFunc = locSel
        mffaVal = cmds.floatField((nameB + "mFFa"), q = 1, v = 1)
        mffuVal = cmds.floatField((nameB + "mFFu"), q = 1, v = 1)
        mffvVal = cmds.floatField((nameB + "mFFv"), q = 1, v = 1)
        print "mffa = ", mffaVal
        F_MyA(mffaVal, mffuVal, mffvVal, locSelFunc, selo)

def main():
    UVeditWin()
