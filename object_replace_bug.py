"""

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_gui_v02.JPG
   :align: center
   :scale: 75%

Object_replace is used for swapping one object in the scene with another. It is useful for updating a model to a newer published
version, or replacing an object with a similar one when setting up a new scene. The tool will do its best to transfer all the connections
and settings from the old object to the new one.  Object_replace is launched from the lighting_tools_shelf:

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_lighting_shelf.JPG
   :align: center
   :scale: 75%

First, choose the new object and then the asset to be replaced.  If the selected object is a valid object (not a light, camera, group node, or Shape node, etc...),
the field will turn green.  If the selected object is not valid, the field will be red.  No more than two objects should be selected, or both fields will be red.

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_gui_one_selection_v02.JPG
   :align: center
   :scale: 75%

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_gui_two_selections_v02.JPG
  :align: center
  :scale: 75%

The script editor will report what attributes were transfered and when the script has finished running.

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_script_editor.JPG
   :align: center
   :scale: 75%

Once finished, the tool hides the old object.  It can be deleted if you no longer need it.

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_outliner.JPG
   :align: center
   :scale: 75%

One common issue occures when the UV sets for the object are named differently.  The tool will not find and transfer those assignments, those
connections need to be updated by hand. If the UV set names do not change, the script will transfer the assignments.

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_UV_set_editor.JPG
   :align: center
   :scale: 75%

Another common issue are the objects not being in the same position in the scene.  The tool does its best to match the orientation and position
of the new object to the old one, but a manuel adjustment is sometimes required.

.. image:: U:/cwinters/docs/build/html/_images/object_replace/object_replace_gui_objects_not_in_position.JPG
   :align: center
   :scale: 75%

It is best practice to save your scene, and save a render of the original object in the scenein the frame buffer, before running the tool.  This way,
you have a backup of your scene if needed, and a visual comparison can be made to catch any attributes that need to be adjusted manually.
"""

import maya.cmds as cmds
import maya.mel as mel
from functools import partial
from string import digits
import os
from os import stat
import os.path
import maya.OpenMayaUI as mui
from functools import partial
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtCore import Qt
import shiboken2
#from pwd import getpwuid
from datetime import datetime

print 'tuesday'

def user_track():
    path = 'U:/cwinters/object_replace_temp_files/'
    #path = '/Users/alfredwinters/Desktop/'
    file_name_on_disk_temp = path + 'temp' + '.txt'
    file_name_on_disk_temp_open = open(file_name_on_disk_temp,'w')
    file_name_on_disk_temp_open.close()
    os.remove(file_name_on_disk_temp)
    filepath = cmds.file(q=True, sn=True)
    filename = os.path.basename(filepath)
    raw_name,extension = os.path.splitext(filename)
    #date = datetime.today().strftime('%m-%d-%Y')
    file_name_on_disk = path + raw_name
    print 'file_name_on_disk = ',file_name_on_disk
    if os.path.isfile(file_name_on_disk) and os.access(file_name_on_disk, os.R_OK):
        os.remove(file_name_on_disk)
    file_name_on_disk_open = open(file_name_on_disk,'w')
    file_name_on_disk_open.close()

def look_for_duplicate_nodes():
    duplicate_node_names = []
    all_nodes = cmds.ls(long = True)
    all_nodes_compare = all_nodes
    for node_1 in all_nodes_compare:
        node_1_split = node_1.split('|')
        node_1_short_name = node_1_split[-1]
        compare = 0
        for node_2 in all_nodes:
            node_2_split = node_2.split('|')
            node_2_short_name = node_2_split[-1]
            if node_1_short_name == node_2_short_name:
                compare = compare + 1
                if compare > 1:
                    if node_1 not in duplicate_node_names:
                        if 'Shape' not in duplicate_node_names:
                            duplicate_node_names.append(node_1)
    return(duplicate_node_names)

def objectChooseWin():
    #user_track()
    name = "object_replace_bug"
    windowSize = (300,100)
    if (cmds.window(name, exists = True)):
        cmds.deleteUI(name)
    bad_node_types = ['VRayObjectProperties']
    window = cmds.window(name, title = name, width = 30, height = 10, sizeable = True)
    cmds.columnLayout("mainColumn", adjustableColumn = True)
    cmds.rowLayout("nameRowLayout01", numberOfColumns = 2, parent = "mainColumn")
    cmds.text(label = "new_object  ")
    object_new_textfield = cmds.textField(tx = 'select_new_object', width = 250,editable = False)
    cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
    cmds.rowLayout("nameRowLayout02", numberOfColumns = 2, parent = "mainColumn")
    cmds.text(label = " old_object   ")
    object_old_textfield= cmds.textField(tx = 'select_old_object', width = 250,editable = False)
    cmds.textField(object_old_textfield,backgroundColor = [.3,.1,.1], edit = True, )
    selected_objects = cmds.ls(sl = True,long = True)
    number_of_selected_objects = len(selected_objects)
    object_New_full_name = ''
    object_Old_full_name = ''
    if number_of_selected_objects == 1:
        select_one_node_type = cmds.nodeType(selected_objects[0])
        if select_one_node_type not in bad_node_types:
            selections_children = cmds.listRelatives(selected_objects[0], shapes = True, fullPath = True) or []
            number_children_shapes = len(selections_children)
            if number_children_shapes > 0:
                for child in selections_children:
                    child_type = cmds.nodeType(child)
                    if child_type == 'mesh':
                        object_New_full_name = selected_objects[0]
                        object_New_short_name_split = selected_objects[0].split('|')
                        object_New_short_name = object_New_short_name_split[-1]
                        cmds.textField(object_new_textfield,text = object_New_short_name, edit = True)
                        cmds.textField(object_new_textfield,backgroundColor = [.3,.45,.3], edit = True, )
        else:
            cmds.textField(object_new_textfield,text = 'select_new_object', edit = True)
            cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
        cmds.textField(object_old_textfield,backgroundColor = [.3,.1,.1], edit = True, )
        cmds.textField(object_old_textfield,text = 'select_old_object', edit = True)
    if number_of_selected_objects == 2:
        select_one_node_type = cmds.nodeType(selected_objects[0])
        if select_one_node_type not in bad_node_types:
            selections_children = cmds.listRelatives(selected_objects[0], shapes = True, fullPath = True) or []
            number_children_shapes = len(selections_children)
            if number_children_shapes > 0:
                for child in selections_children:
                    child_type = cmds.nodeType(child)
                    if child_type == 'mesh':
                        object_New_full_name = selected_objects[0]
                        object_New_short_name_split = selected_objects[0].split('|')
                        object_New_short_name = object_New_short_name_split[-1]
                        cmds.textField(object_new_textfield,text = object_New_short_name, edit = True)
                        cmds.textField(object_new_textfield,backgroundColor = [.3,.45,.3], edit = True, )
        else:
            cmds.textField(object_new_textfield,text = 'select_new_object', edit = True)
            cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
        select_two_node_type = cmds.nodeType(selected_objects[1])
        if select_two_node_type not in bad_node_types:
            selections_children = cmds.listRelatives(selected_objects[1], shapes = True, fullPath = True) or []
            number_children_shapes = len(selections_children)
            if number_children_shapes > 0:
                for child in selections_children:
                    child_type = cmds.nodeType(child)
                    if child_type == 'mesh':
                        object_Old_full_name = selected_objects[1]
                        object_Old_short_name_split = selected_objects[1].split('|')
                        object_Old_short_name = object_Old_short_name_split[-1]
                        cmds.textField(object_old_textfield,text = object_Old_short_name, edit = True)
                        cmds.textField(object_old_textfield,backgroundColor = [.3,.45,.3], edit = True, )
        else:
            cmds.textField(object_old_textfield,text = 'select_old_object', edit = True)
            cmds.textField(object_old_textfield,backgroundColor = [.3,.1,.1], edit = True, )

    def text_fields_selected_objects():
        print 'text_fields_selected_objects'
        mesh_found = 0
        bad_node_types = ['VRayObjectProperties']
        selected_objects = cmds.ls(sl = True,long = True)
        number_of_selected_objects = len(selected_objects)
        print 'number_of_selected_objects = ',number_of_selected_objects
        if number_of_selected_objects == 0:
            cmds.textField(object_new_textfield,text = 'select_new_object', edit = True)
            cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
            cmds.textField(object_old_textfield,text = 'select_old_object', edit = True)
            cmds.textField(object_old_textfield,backgroundColor = [.3,.1,.1], edit = True, )
        if number_of_selected_objects == 1:
            print 'mesh_found = ',mesh_found
            select_one_node_type = cmds.nodeType(selected_objects[0])
            if select_one_node_type not in bad_node_types:
                selections_children = cmds.listRelatives(selected_objects[0], shapes = True, fullPath = True) or []
                print 'selections_children = ', selections_children
                number_children_shapes = len(selections_children)
                if number_children_shapes > 0:
                    for child in selections_children:
                        child_type = cmds.nodeType(child)
                        if child_type == 'mesh':
                            mesh_found = 1
                            object_New_full_name = selected_objects[0]
                            object_New_short_name_split = selected_objects[0].split('|')
                            object_New_short_name = object_New_short_name_split[-1]
                            cmds.textField(object_new_textfield,text = object_New_short_name, edit = True)
                            cmds.textField(object_new_textfield,backgroundColor = [.3,.45,.3], edit = True, )
                if mesh_found == 0:
                    cmds.textField(object_new_textfield,text = 'select_new_object', edit = True)
                    cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
            else:
                cmds.textField(object_new_textfield,text = 'select_new_object', edit = True)
                cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
            cmds.textField(object_old_textfield,text = 'select_old_object', edit = True)
            cmds.textField(object_old_textfield,backgroundColor = [.3,.1,.1], edit = True, )
        if number_of_selected_objects == 2:
            select_one_node_type = cmds.nodeType(selected_objects[0])
            if select_one_node_type not in bad_node_types:
                selections_children = cmds.listRelatives(selected_objects[0], shapes = True, fullPath = True) or []
                print 'selections_children = ', selections_children
                number_children_shapes = len(selections_children)
                if number_children_shapes > 0:
                    for child in selections_children:
                        child_type = cmds.nodeType(child)
                        if child_type == 'mesh':
                            object_New_full_name = selected_objects[0]
                            object_New_short_name_split = selected_objects[0].split('|')
                            object_New_short_name = object_New_short_name_split[-1]
                            cmds.textField(object_new_textfield,text = object_New_short_name, edit = True)
                            cmds.textField(object_new_textfield,backgroundColor = [.3,.45,.3], edit = True, )
            else:
                cmds.textField(object_new_textfield,text = 'select_new_object', edit = True)
                cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
            select_two_node_type = cmds.nodeType(selected_objects[1])
            if select_two_node_type not in bad_node_types:
                selections_children = cmds.listRelatives(selected_objects[1], shapes = True, fullPath = True) or []
                print 'selections_children = ', selections_children
                number_children_shapes = len(selections_children)
                if number_children_shapes > 0:
                    for child in selections_children:
                        child_type = cmds.nodeType(child)
                        if child_type == 'mesh':
                            object_Old_full_name = selected_objects[1]
                            object_Old_short_name_split = selected_objects[1].split('|')
                            object_Old_short_name = object_Old_short_name_split[-1]
                            cmds.textField(object_old_textfield,text = object_Old_short_name, edit = True)
                            cmds.textField(object_old_textfield,backgroundColor = [.3,.45,.3], edit = True, )
            else:
                cmds.textField(object_old_textfield,text = 'select_old_object', edit = True)
                cmds.textField(object_old_textfield,backgroundColor = [.3,.1,.1], edit = True, )
        if number_of_selected_objects > 2:
            print 'num of sel object more than 3 =  ',number_of_selected_objects
            cmds.textField(object_new_textfield,text = 'select_new_object', edit = True)
            cmds.textField(object_new_textfield,backgroundColor = [.3,.1,.1], edit = True, )
            cmds.textField(object_old_textfield,text = 'select_old_object', edit = True)
            cmds.textField(object_old_textfield,backgroundColor = [.3,.1,.1], edit = True, )
    myScriptJobID = cmds.scriptJob(p = window, event=["SelectionChanged", text_fields_selected_objects])

    def objects_CB(*args):
        print ' '
        print '*** starting object replace ***'
        print ' '
        selected_objects = cmds.ls(sl = True,long = True)
        panels = cmds.getPanel( type = "modelPanel" )
        for mPanel in panels:
            cmds.modelEditor(mPanel, edit = True, allObjects = 0)
        number_of_selected_objects = len(selected_objects)
        if number_of_selected_objects != 2:
            cmds.select(clear = True)
            object_new_text = cmds.textField(object_new_textfield, text = True, query = True)
            cmds.select(object_new_text)
            object_old_text = cmds.textField(object_old_textfield, text = True, query = True)
            cmds.select(object_old_text,add = True)
            selected_objects = cmds.ls(sl = True,long = True)
        object_New = selected_objects[0]
        object_Old = selected_objects[1]
        objects(object_Old,object_New)

    cmds.rowLayout("nameRowLayout2.5", numberOfColumns = 10, parent = "mainColumn")
    cmds.rowLayout("nameRowLayout4.5", numberOfColumns = 10, parent = "mainColumn")
    cmds.rowLayout("nameRowLayout05", numberOfColumns = 2, parent = "mainColumn")
    cmds.text(label = "                      ")
    cmds.button(label = "replace", width = 150,command =  partial(objects_CB, object_New_full_name,object_Old_full_name))
    cmds.showWindow()

    def objects(object_Old,object_New):
        print 'new_object = ',object_New
        print 'old_object = ',object_Old
        cmds.xform(object_Old,centerPivots = True)
        cmds.xform(object_New,centerPivots = True)
        old_Xforms =  cmds.objectCenter(object_Old)
        all_shape_nodes = []
        transform_nodes = cmds.ls(type = 'transform')
        for transform_node in transform_nodes:
            transform_node_shapes = cmds.listRelatives(transform_node,shapes = True,fullPath = True) or []
            for transform_node_shape in transform_node_shapes:
                if transform_node_shape not in all_shape_nodes:
                    all_shape_nodes.append(transform_node_shape)
                    all_shape_nodes.append(transform_node_shape[1:])
                    all_shape_nodes.append('|' + transform_node_shape)
        if object_Old in all_shape_nodes:
            object_Old_parents = cmds.listRelatives(object_Old,parent = True,fullPath = True)
            object_Old = object_Old_parents[0]
        if object_New in all_shape_nodes:
            object_New_parents = cmds.listRelatives(object_New,parent = True,fullPath = True)
            object_New = object_New_parents[0]
        duplicate_node_names = look_for_duplicate_nodes()
        duplicate_node_shape_list = []
        duplicate_node_names.reverse()
        number_of_dup_nodes = len(duplicate_node_names)
        duplicate_node_names_renamed = []
        duplicate_name_dic = {}
        object_old_rename_check = 0
        object_new_rename_check = 0
        if number_of_dup_nodes > 0:
            duplicate_node_names.sort(key=len,reverse = True)
            for duplicate_node_name in duplicate_node_names:
                shapes = cmds.listRelatives(duplicate_node_name,shapes = True,fullPath = True) or []
                for shape in shapes:
                    if shape not in duplicate_node_shape_list:
                        if shape[0] == '|':
                            shape = shape[1:]
                        shape_name = shape
                        shape_name_bar = '|' + shape_name
                        duplicate_node_shape_list.append(shape_name)
                        duplicate_node_shape_list.append(shape_name_bar)
            i = 0
            for duplicate_node_name in duplicate_node_names:
                if duplicate_node_name not in duplicate_node_shape_list:
                    duplicate_node_name_split = duplicate_node_name.split('|')
                    object_name = duplicate_node_name_split[-1]
                    rename_string = object_name + '_XXXXXX__duplicate_name' + str(i)
                    cmds.lockNode(duplicate_node_name,lock = False)
                    cmds.rename(duplicate_node_name,rename_string)
                    duplicate_node_names_renamed.append(rename_string)
                    if duplicate_node_name == object_Old:
                        duplicate_name_dic[rename_string] = object_Old
                        object_Old = rename_string
                        object_old_rename_check = 1
                    if duplicate_node_name == ('|' + object_Old):
                        duplicate_name_dic[rename_string] = object_Old
                        object_Old = rename_string
                        object_old_rename_check = 1
                    if duplicate_node_name == object_Old[1:]:
                        duplicate_name_dic[rename_string] = object_Old
                        object_Old = rename_string
                        object_old_rename_check = 1
                    if duplicate_node_name == object_New:
                        duplicate_name_dic[rename_string] = object_New
                        object_New = rename_string
                        object_new_rename_check = 1
                    if duplicate_node_name == ('|' + object_New):
                        duplicate_name_dic[rename_string] = object_New
                        object_New = rename_string
                        object_new_rename_check = 1
                    if duplicate_node_name == object_New[1:]:
                        duplicate_name_dic[rename_string] = object_New
                        object_New = rename_string
                        object_new_rename_check = 1
                    object_Old_name_split = object_Old.split('|')
                    object_Old_name_raw = object_Old_name_split[-1]
                    duplicate_node_name_split = duplicate_node_name.split('|')
                    i = i + 1
        object_Old_split = object_Old.split('|')
        object_Old_raw = object_Old_split[-1]
        object_New_split = object_New.split('|')
        object_New_raw = object_New_split[-1]
        object_Old_full_paths = cmds.ls(object_Old_raw,long = True)
        object_New_full_paths = cmds.ls(object_New_raw,long = True)
        for object_Old_full_path in object_Old_full_paths:
            object_Old_full_path_node_type = cmds.nodeType(object_Old_full_path)
            if object_Old_full_path_node_type != 'mesh':
                object_Old = object_Old_full_path
        for object_New_full_path in object_New_full_paths:
            object_New_full_path_node_type = cmds.nodeType(object_New_full_path)
            if object_New_full_path_node_type != 'mesh':
                object_New = object_New_full_path
        transform_nodes = cmds.ls(type = 'transform')
        looking_for_duplicate_shape_node_names = look_for_duplicate_nodes()
        print 'looking_for_duplicate_shape_node_names = ',looking_for_duplicate_shape_node_names
        scene_shapes = []
        for transform_node in transform_nodes:
            transform_node_shapes = cmds.listRelatives(transform_node,shapes = True,fullPath = True) or []
            for transform_node_shape in transform_node_shapes:
                if 'Shape' not in transform_node_shape:
                    cmds.lockNode(transform_node_shape,lock = False)
                    cmds.rename(transform_node_shape,transform_node_shape + 'Shape')
                    if transform_node_shape in duplicate_node_names_renamed:
                        duplicate_node_names_renamed.remove(transform_node_shape)
        obj_kids_old = cmds.listRelatives(object_Old, children = True) or []
        obj_kids_new = cmds.listRelatives(object_New, children = True) or []
        obj_kids_old_len = len(obj_kids_old)
        obj_kids_new_len = len(obj_kids_new)
        if obj_kids_old_len == 0:
            object_old_split = object_Old.split("_")
            object_old_split_size = len(object_old_split)
            if "Shape" in object_old_split[object_old_split_size - 1]:
                old_kid_parent = cmds.listRelatives(object_Old, parent = True) or [[]]
                object_Old = old_kid_parent[0]
        if obj_kids_new_len == 0:
            object_new_split = object_New.split("_")
            object_new_split_size = len(object_new_split)
            if "Shape" in object_new_split[object_new_split_size - 1]:
                new_kid_parent = cmds.listRelatives(object_New, parent = True) or [[]]
                object_New = new_kid_parent[0]
        renderLayers = cmds.ls(type = 'renderLayer')
        currentRenderLayer = cmds.editRenderLayerGlobals( query = True, currentRenderLayer = True)
        object_old_print_temp = ''
        object_new_print_temp = ''
        if object_old_rename_check == 1:
            if object_Old in duplicate_name_dic:
                object_old_print_temp = duplicate_name_dic[object_Old]
        else:
            object_old_print_temp = object_Old
        if object_new_rename_check ==  1:
            if object_New in duplicate_name_dic:
                object_new_print_temp = duplicate_name_dic[object_New]
        else:
            object_new_print_temp = object_New

        def master_path(object_Old,object_New,renderLayers):
            print "old object path check:"
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            pathOBJ = cmds.listRelatives(object_Old, fullPath = True) or []
            pathmasterObj = pathOBJ[0]
            si = len(pathOBJ)
            pathmasterObj_print_temp = pathmasterObj
            pathmasterObj_print_temp_split = pathmasterObj_print_temp.split('|')
            number_of_splits = len(pathmasterObj_print_temp_split)
            pathmasterObj_print_temp = ''
            i = 0
            while i < (number_of_splits - 3):
                pathmasterObj_print_temp = pathmasterObj_print_temp + pathmasterObj_print_temp_split[i] + '|'
                i = i + 1
            pathmasterObj_print_temp = pathmasterObj_print_temp + object_old_print_temp
            if si > 0:
                print pathmasterObj_print_temp
            else:
                print "parent object selected"
            return pathmasterObj,object_Old,object_New,pathOBJ

        def renderLayerCheck(object_Old,object_New,renderLayers):
            #print ' '
            #print "old object render layers check:"
            object_Old = (str(object_Old))
            #print ' XXX '
            #print 'object_Old = ',object_Old
            objects_render_layer_compare = []
            objects_render_layer_compare.append(object_Old)
            #print 'objects_render_layer_compare = ',objects_render_layer_compare
            object_Old_kids = cmds.listRelatives(object_Old,fullPath = True,children = True) or []
            #print 'object_Old_kids = ',object_Old_kids
            for object in object_Old_kids:
                #print 'object = ',object
                object_type = cmds.nodeType(object)
                #print 'object_type = ',object_type
                if object_type == 'mesh':
                    #print 'object type = mesh'
                    if object not in objects_render_layer_compare:
                        #print object + ' not in objects_render_layer_compare'
                        object_split = object.split('|')
                        size_of_list = len(object_split)
                        object = object_split[(size_of_list - 1)]
                        #print 'object = ',object
                        if object not in objects_render_layer_compare:
                            #print 'object not in objects_render_layer_compare'
                            objects_render_layer_compare.append(object)
                            #print 'objects_render_layer_compare = ',objects_render_layer_compare
            object_Old_parents = cmds.listRelatives(object_Old,fullPath = True,parent = True) or []
            #print 'object_Old_parents = ',object_Old_parents
            for object in object_Old_parents:
                #print 'object = ',object
                object_type = cmds.nodeType(object)
                #print 'object_type = ',object_type
                if object_type == 'mesh':
                    #print 'object_type == mesh'
                    if object not in objects_render_layer_compare:
                        #print 'object not in objects_render_layer_compare'
                        object_split = object.split('|')
                        size_of_list = len(object_split)
                        object = object_split[(size_of_list - 1)]
                        #print 'object = ',object
                        if object not in objects_render_layer_compare:
                            #print 'object not in objects_render_layer_compare'
                            objects_render_layer_compare.append(object)
            #print '1 objects_render_layer_compare = ',objects_render_layer_compare
            for object in objects_render_layer_compare:
                #print 'object = ',object
                object_split = object.split('|')
                #print 'object_split = ',object_split
                if len(object_split) > 0:
                    object_name_isolated = object_split[-1]
                    if object_name_isolated not in  objects_render_layer_compare:
                        #print 'adding isolated object name to objects_render_layer_compare'
                        objects_render_layer_compare.append(object_name_isolated)
            #print '2 objects_render_layer_compare = ',objects_render_layer_compare
            object_New = (str(object_New))
            #print ' XXX '
            #print 'object_New = ',object_New
            #print ' XXX '
            object_in_render_layer_list = []
            size_layers = len(renderLayers)
            for render_layer in renderLayers:
                #print '******'
                #print 'render_layer = ',render_layer
                members_in_render_layer = cmds.editRenderLayerMembers(render_layer, query = True ) or []
                #print 'members_in_render_layer = ',members_in_render_layer
                number_of_objects_in_render_layer = len(members_in_render_layer)
                #print 'number_of_objects_in_render_layer = ',number_of_objects_in_render_layer
                if number_of_objects_in_render_layer > 0:
                    #print 'number_of_objects_in_render_layer > 0'
                    for member_in_render_layer in members_in_render_layer:
                        #print 'member_in_render_layer = ',member_in_render_layer
                        #print 'objects_render_layer_compare = ',objects_render_layer_compare
                        if member_in_render_layer in objects_render_layer_compare:
                            #print 'member_in_render_layer in objects_render_layer_compare'
                            if render_layer not in object_in_render_layer_list:
                                object_in_render_layer_list.append(render_layer)
                                #print 'render_layer not in object_in_render_layer_list'
                                #print 'appending ' + render_layer
                                #print 'object_in_render_layer_list = ',object_in_render_layer_list
            print 'old_object in render layers, ',object_in_render_layer_list
            print ' '
            return object_in_render_layer_list,object_Old,object_New

        def translations(object_Old,object_New,renderLayers,old_Xforms):
            print "old object transforms check:"
            transValuesDict = {}
            transX_val = 0
            transY_val = 0
            transZ_val = 0
            rotX_val = 0
            rotY_val = 0
            rotZ_val = 0
            scaleX_val = 1
            scaleY_val = 1
            scaleZ_val = 1
            objInLayers = []
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            object_Old = object_Old
            if "Shape" in object_Old:
                par = cmds.listRelatives(object_Old, parent = True)
                object_Old = par[0]
            RL = renderLayers
            for L in RL:
                objList = cmds.editRenderLayerMembers( L, query=True ) or []
                for obj in objList:
                    object_Old = object_Old
                    if obj in object_Old:
                        objInLayers.append(L)
            for lay in objInLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = lay )
                strTransX = object_Old + ".translateX"
                transX = cmds.getAttr(strTransX)
                var = object_Old + "_" + '&'+lay+'&' + "_transX"
                transValuesDict[var] = transX
                strTransY = object_Old + ".translateY"
                transY = cmds.getAttr(strTransY)
                var = object_Old + "_" + '&'+lay+'&' + "_transY"
                transValuesDict[var] = transY
                strTransZ = object_Old + ".translateZ"
                transZ = cmds.getAttr(strTransZ)
                var = object_Old + "_" + '&'+lay+'&' + "_transZ"
                transValuesDict[var] = transZ
                strRotX = object_Old + ".rotateX"
                rotX = cmds.getAttr(strRotX)
                var = object_Old + "_" + '&'+lay+'&' + "_rotX"
                transValuesDict[var] = rotX
                strRotY = object_Old + ".rotateY"
                rotY = cmds.getAttr(strRotY)
                var = object_Old + "_" + '&'+lay+'&' + "_rotY"
                transValuesDict[var] = rotY
                strRotZ = object_Old + ".rotateZ"
                rotZ = cmds.getAttr(strRotZ)
                var = object_Old + "_" + '&'+lay+'&' + "_rotZ"
                transValuesDict[var] = rotZ
                strScaleX = object_Old + ".scaleX"
                scaleX = cmds.getAttr(strScaleX)
                var = object_Old + "_" + '&'+lay+'&' + "_scaleX"
                transValuesDict[var] = scaleX
                strScaleY = object_Old + ".scaleY"
                scaleY = cmds.getAttr(strScaleY)
                var = object_Old + "_" + '&'+lay+'&' + "_scaleY"
                transValuesDict[var] = scaleY
                strScaleZ = object_Old + ".scaleZ"
                scaleZ = cmds.getAttr(strScaleZ)
                var = object_Old + "_" + '&'+lay+'&' + "_scaleZ"
                transValuesDict[var] = scaleZ
            defVals = []
            for tv in transValuesDict:
                if "defaultRenderLayer" in tv:
                    defVals.append(tv)
            for A in defVals:
                if "transX" in A:
                    transX_val = transValuesDict[A]
            for A in defVals:
                if "transY" in A:
                    transY_val = transValuesDict[A]
            for A in defVals:
                if "transZ" in A:
                    transZ_val = transValuesDict[A]
            for A in defVals:
                if "rotX" in A:
                    rotX_val = transValuesDict[A]
            for A in defVals:
                if "rotY" in A:
                    rotY_val = transValuesDict[A]
            for A in defVals:
                if "rotZ" in A:
                    rotZ_val = transValuesDict[A]
            for A in defVals:
                if "scaleX" in A:
                    scaleX_val = transValuesDict[A]
            for A in defVals:
                if "scaleY" in A:
                    scaleY_val = transValuesDict[A]
            for A in defVals:
                if "scaleZ" in A:
                    scaleZ_val = transValuesDict[A]
            transLayerOveride = []
            for dic in transValuesDict:
                if "transX" in dic:
                    val = transValuesDict[dic]
                    if val != transX_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "transY" in dic:
                    val = transValuesDict[dic]
                    if val != transY_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "transZ" in dic:
                    val = transValuesDict[dic]
                    if val != transZ_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "rotX" in dic:
                    val = transValuesDict[dic]
                    if val != rotX_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "rotY" in dic:
                    val = transValuesDict[dic]
                    if val != rotY_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "rotZ" in dic:
                    val = transValuesDict[dic]
                    if val != rotZ_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "scaleX" in dic:
                    val = transValuesDict[dic]
                    if val != scaleX_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "scaleY" in dic:
                    val = transValuesDict[dic]
                    if val != scaleY_val:
                        transLayerOveride.append(dic)
            for dic in transValuesDict:
                if "scaleZ" in dic:
                    val = transValuesDict[dic]
                    if val != scaleZ_val:
                        transLayerOveride.append(dic)
            defValList = [transX_val,transY_val,transZ_val,rotX_val,rotY_val,rotZ_val,scaleX_val,scaleY_val,scaleZ_val]
            sizL = len(transLayerOveride)
            transValuesDict_string = str(transValuesDict)
            transLayerOveride_string = str(transLayerOveride)
            transValuesDict_string = transValuesDict_string.replace(object_Old,object_old_print_temp)
            transLayerOveride_string = transLayerOveride_string.replace(object_Old,object_old_print_temp)
            print 'old_object transforms = ',transValuesDict_string
            print 'old_object transform layer overrides = ',transLayerOveride_string
            return transValuesDict,object_Old,object_New,defVals,defValList,objInLayers,transLayerOveride

        def excludeListSets(object_Old,object_New,renderLayers):
            print "old object exclude sets check:"
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            tmpOBJ = object_Old
            if "Shape" in tmpOBJ:
                object_Old_Parent = cmds.listRelatives(object_Old, parent = True) or []
                object_Old_Child = object_Old
                object_Old = object_Old_Parent
            if "Shape" not in tmpOBJ:
                objectChild = cmds.listRelatives(object_Old, children = True) or []
                object_Old_Child = objectChild
                object_Old_Parent = object_Old
            setsINC = []
            exTextures = []
            allNodes = cmds.ls(long = True, type = "VRayRenderElement")
            for node in allNodes:
                if "Extra_Tex" in node:
                    exTextures.append(node)
            for exTex in exTextures:
                listItems = cmds.listConnections(exTex) or []
                listSiz = len(listItems)
                for LI in listItems:
                    if "extratex" in LI:
                        setMembers = cmds.listConnections(LI) or []
                        for A in setMembers:
                            if A in object_Old:
                                setsINC.append(LI)
                        for A in setMembers:
                            if A in object_Old_Child:
                                setsINC.append(LI)
            sizeL = len(setsINC)
            if sizeL > 0:
                if object_old_rename_check != 0:
                    print "sets used by a v-ray Extra_Tex that contain " + object_old_print_temp + " = ", setsINC
                else:
                    print "sets used by a v-ray Extra_Tex that contain " + object_Old + " = ", setsINC
            else:
                if object_old_rename_check == 1:
                    print object_old_print_temp + "detected in no exlude sets"
                else:
                    print object_Old + " detected in no exlude sets"
            return setsINC,object_Old,object_New

        def lightLinking(object_Old,object_New,renderLayers):
            print 'light linking check:'
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            tmpOBJ = object_Old
            lightLinkingDict = []
            if "Shape" in tmpOBJ:
                object_Old_Parent = cmds.listRelatives(object_Old, parent = True) or []
                object_Old_Child = object_Old
                object_Old = object_Old_Parent
            if "Shape" not in tmpOBJ:
                objectChild = cmds.listRelatives(object_Old, children = True) or []
                object_Old_Child = objectChild
                object_Old_Parent = object_Old
                cmds.select(object_Old)
                ltsL = cmds.lightlink( query=True, object = object_Old)
            ltsLL = []
            ltsLL = ltsL
            print "lights linked to " + object_old_print_temp + " are:", ltsLL
            return ltsLL,object_Old,object_New

        def renderStats(object_Old,object_New,renderLayers):
            print "old object render stats check:"
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            objParent = cmds.listRelatives(object_Old, parent = True) or []
            objChild = cmds.listRelatives(object_Old, children = True) or []
            renderStatsDic = {}
            if "Shape" in object_Old:
                objParent = objParent
                objChild = object_Old
                object_Old = objChild
            else:
                objParent = object_Old
                objChild = objChild
                object_Old = objChild
            RLOs = cmds.ls(type = "renderLayer")
            for RL in RLOs:
                cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                castsShadowsV = object_Old[0] + ".castsShadows"
                castsShadowsVAR = cmds.getAttr(castsShadowsV)
                castsShadowsKEY = object_Old[0] + "_" + RL + "_castsShadows"
                renderStatsDic[castsShadowsKEY] = castsShadowsVAR
                receiveShadowsV = object_Old[0] + ".receiveShadows"
                receiveShadowsVAR = cmds.getAttr(receiveShadowsV)
                receiveShadowsKEY = object_Old[0] + "_" + RL + "_receiveShadows"
                renderStatsDic[receiveShadowsKEY] = receiveShadowsVAR
                motionBlurV = object_Old[0] + ".motionBlur"
                motionBlurVAR = cmds.getAttr(motionBlurV)
                motionBlurKEY = object_Old[0] + "_" + RL + "_motionBlur"
                renderStatsDic[motionBlurKEY] = motionBlurVAR
                primaryVisibilityV = object_Old[0] + ".primaryVisibility"
                primaryVisibilityVAR = cmds.getAttr(primaryVisibilityV)
                primaryVisibilityKEY = object_Old[0] + "_" + RL + "_primaryVisibility"
                renderStatsDic[primaryVisibilityKEY] = primaryVisibilityVAR
                smoothShadingV = object_Old[0] + ".smoothShading"
                smoothShadingVAR = cmds.getAttr(smoothShadingV)
                smoothShadingKEY = object_Old[0] + "_" + RL + "_smoothShading"
                renderStatsDic[smoothShadingKEY] = smoothShadingVAR
                visibleInReflectionsV = object_Old[0] + ".visibleInReflections"
                visibleInReflectionsVAR = cmds.getAttr(visibleInReflectionsV)
                visibleInReflectionsKEY = object_Old[0] + "_" + RL + "_visibleInReflections"
                renderStatsDic[visibleInReflectionsKEY] = visibleInReflectionsVAR
                visibleInRefractionsV = object_Old[0] + ".visibleInRefractions"
                visibleInRefractionssVAR = cmds.getAttr(visibleInRefractionsV)
                visibleInRefractionsKEY = object_Old[0] + "_" + RL + "_visibleInRefractions"
                renderStatsDic[visibleInRefractionsKEY] = visibleInRefractionssVAR
                doubleSidedV = object_Old[0] + ".doubleSided"
                doubleSidedVAR = cmds.getAttr(doubleSidedV)
                doubleSidedKEY = object_Old[0] + "_" + RL + "_doubleSided"
                renderStatsDic[doubleSidedKEY] = doubleSidedVAR
            defRSlist = []
            NONdefRSlist = []
            for defi in renderStatsDic:
                if "default" in defi:
                    defRSlist.append(defi)
                else:
                    NONdefRSlist.append(defi)
            for defiVar in defRSlist:
                if "castsShadows" in defiVar:
                    defaultVal_castsShadows = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "receiveShadows" in defiVar:
                    defaultVal_receiveShadows = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "motionBlur" in defiVar:
                    defaultVal_motionBlur = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "primaryVisibility" in defiVar:
                    defaultVal_primaryVisibility = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "smoothShading" in defiVar:
                    defaultVal_smoothShading = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "visibleInReflections" in defiVar:
                    defaultVal_visibleInReflections = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "visibleInRefractions" in defiVar:
                    defaultVal_refractionVisibility = renderStatsDic[defiVar]
            for defiVar in defRSlist:
                if "doubleSided" in defiVar:
                    defaultVal_doubleSided = renderStatsDic[defiVar]
            RS_overRideList = []
            for NDL in NONdefRSlist:
                if "castsShadows" in NDL:
                    Val_ND_castsShadows = renderStatsDic[NDL]
                    if Val_ND_castsShadows != defaultVal_castsShadows:
                        RS_overRideList.append(NDL)
                if "receiveShadows" in NDL:
                    Val_ND_receiveShadows = renderStatsDic[NDL]
                    if Val_ND_receiveShadows != defaultVal_receiveShadows:
                        RS_overRideList.append(NDL)
                if "motionBlur" in NDL:
                    Val_ND_motionBlur = renderStatsDic[NDL]
                    if Val_ND_motionBlur != defaultVal_motionBlur:
                        RS_overRideList.append(NDL)
                if "primaryVisibility" in NDL:
                    Val_ND_primaryVisibility = renderStatsDic[NDL]
                    if Val_ND_primaryVisibility != defaultVal_primaryVisibility:
                        RS_overRideList.append(NDL)
                if "smoothShading" in NDL:
                    Val_ND_smoothShading = renderStatsDic[NDL]
                    if Val_ND_smoothShading != defaultVal_smoothShading:
                        RS_overRideList.append(NDL)
                if "visibleInReflections" in NDL:
                    Val_ND_visibleInReflections = renderStatsDic[NDL]
                    if Val_ND_visibleInReflections != defaultVal_visibleInReflections:
                        RS_overRideList.append(NDL)
                if "visibleInRefractions" in NDL:
                    Val_ND_refractionVisibility = renderStatsDic[NDL]
                    if Val_ND_refractionVisibility != defaultVal_refractionVisibility:
                        RS_overRideList.append(NDL)
                if "doubleSided" in NDL:
                    Val_ND_doubleSided = renderStatsDic[NDL]
                    if Val_ND_doubleSided != defaultVal_doubleSided:
                        RS_overRideList.append(NDL)
            rss = len(RS_overRideList)
            renderStatsDic_string = str(renderStatsDic)
            renderStatsDic_string = renderStatsDic_string.replace(object_Old[0],object_old_print_temp)
            RS_overRideList_string = str(RS_overRideList)
            RS_overRideList_string = RS_overRideList_string.replace(object_Old[0],object_old_print_temp)
            print 'old_object render state settings = ',renderStatsDic_string
            if rss > 0:
                print "suspected renderState layer overides in, ", RS_overRideList_string
            if rss == 0:
                print "no renderState layer overides detected"
            return RS_overRideList,object_Old,object_New,defRSlist,RS_overRideList,renderStatsDic,RLOs

        def objectProptertyOverides(object_Old,object_New,renderLayers):
            print "old object v-ray object properties check:"
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            objParent = cmds.listRelatives(object_Old, parent = True) or []
            objChild = cmds.listRelatives(object_Old, children = True) or []
            VoBpropertyDic = {}
            defVPlist = []
            NONdefVPlist = []
            objectIDo = "False"
            vpOPid = 0
            if "Shape" in object_Old:
                objParent = objParent
                objChild = object_Old
                object_Old = objParent
            else:
                objParent = object_Old
            OPlist = []
            OPlist_all = cmds.ls(type = "VRayObjectProperties") or []
            #print 'OPlist_all = ',OPlist_all
            object_Old_split = object_Old.split('|')
            object_Old_base_name = object_Old_split[-1]
            for op in OPlist_all:
                #print 'op = ',op
                chilRels = cmds.listRelatives(op) or []
                chilCons = cmds.listConnections(op) or []
                for chiRel in chilRels:
                    #print 'object_Old = ',object_Old
                    #print 'chiRel = ',chiRel
                    if object_Old in chiRel or object_Old_base_name in chiRel:
                        if op not in OPlist:
                            OPlist.append(op)
                for chiCon in chilCons:
                    #print 'object_Old = ',object_Old
                    #print 'chiCon = ',chiCon
                    if object_Old in chiCon or object_Old_base_name in chiCon:
                        if op not in OPlist:
                            OPlist.append(op)
            size_OPlist = len(OPlist)
            if size_OPlist > 0:
                print 'old_object v-ray object property groups = ',OPlist
            else:
                print 'no v-ray object property group detected for ',object_old_print_temp
            return object_Old,object_New,OPlist

        def objectIDnode(object_Old,object_New,renderLayers):
            print "old object, object ID check:"
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            objID = "None"
            objectID_dic = {}
            if "Shape" in object_Old:
                objectIDnode = object_Old + ".vrayObjectID"
            else:
                chil = cmds.listRelatives(object_Old, children = True)
                object_Old = chil
                objectIDnode = object_Old[0] + ".vrayObjectID"
            ext = cmds.objExists(objectIDnode)
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            RLOs = cmds.ls(type = "renderLayer")
            if ext == 1:
                objID = cmds.getAttr(objectIDnode)
                print "default render layer objectID exists and is",objID
                for RL in RLOs:
                    cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                    objIDl = cmds.getAttr(objectIDnode)
                    if objIDl != objID:
                        objectID_dic[RL] = objIDl
                        print "ObjectID render layer overide detected in layers: " + RL + ":" + str(objIDl)
            else:
                print "no v-ray object ID attribute detected"
            return objID,object_Old,object_New,objectID_dic,RLOs


        def materials(object_Old,object_New,renderLayers):
            print "old object materials check:"
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            materials_assigned_object_old = {}
            materials_assigned_object_old_OVR = []
            LayerMats_dic = {}
            mats_dict = {}
            mats_faceDict = {}
            mats_objectList = {}
            mats_objectList_clean = []
            mats_objectList_clean_BASE = []
            spltMatList = []
            spltMatList2 = []
            layerOverM2  = {}
            matAssignsExist = 0
            render_layers_in_scene = cmds.ls(type = "renderLayer")
            for render_layer in render_layers_in_scene:
                cmds.editRenderLayerGlobals( currentRenderLayer = render_layer )
                cmds.select(clear = True)
                cmds.select(object_Old)
                cmds.hyperShade(smn = True)
                materials_assigned_object_old = cmds.ls(sl = True)
                for material_assigned_object_old in materials_assigned_object_old:
                    NT = cmds.nodeType(material_assigned_object_old)
                    if NT != "renderLayer":
                        materials_assigned_object_old_OVR.append(material_assigned_object_old)
                number_of_assigned_materials = len(materials_assigned_object_old_OVR)
                if number_of_assigned_materials > 0:
                    for matsInc in materials_assigned_object_old_OVR:
                        cmds.select(matsInc)
                        LayerMats_dic[render_layer] = matsInc
                        cmds.hyperShade(o = matsInc)
                        mats_objectList = cmds.ls(sl = True)
                        for mo in mats_objectList:
                            object_old_split = object_Old.split('_XXXXXX')
                            if mo in object_Old:
                                mats_objectList_clean.append(mo)
                            mo_no_shape = mo.replace('Shape','')
                            if mo_no_shape in object_Old:
                                mats_objectList_clean.append(mo)
                            if object_old_split[0] in object_Old:
                                mats_objectList_clean.append(mo)
                        matAssignsExist = len(mats_objectList_clean)
                        for moc in mats_objectList_clean:
                            baseO = cmds.listRelatives(moc, parent = True)
                            if baseO not in mats_objectList_clean_BASE:
                                mats_objectList_clean_BASE.append(baseO)
                        layer_Mats_Inc = render_layer + "_" + matsInc + "_"
                        for moc in mats_objectList_clean:
                            baseO = cmds.listRelatives(moc, parent = True)
                            if baseO not in mats_objectList_clean_BASE:
                                mats_objectList_clean_BASE.append(baseO)
                        emptyListTest = len(mats_objectList)
                        emptyListTest2 = len(mats_objectList_clean_BASE)
                        if emptyListTest > 0:
                            if emptyListTest2 > 0:
                                mats_dict[layer_Mats_Inc] = mats_objectList_clean_BASE[0]
                    spltMatList.append(matsInc)
            sz = len(spltMatList)
            szz = sz - 1
            aa = 0
            layerOverM = []
            FDRL = 0
            for findDRL in render_layers_in_scene:
                if "defaultRenderLayer" in findDRL:
                    defaultRenderLayerPosition = FDRL
                FDRL += 1
            FDRL = int(FDRL)
            for L in render_layers_in_scene:
                a = 0
                for m in mats_dict:
                    if L in m:
                        key = L + "*" + str(a)
                        layerOverM2[key] = m
                        a=a+1
            RlayerOlist = []
            for LO in layerOverM2:
                if "defaultRenderLayer" in LO:
                    defVal = layerOverM2[LO]
            for LO in layerOverM2:
                valu = layerOverM2[LO]
                if defVal != valu:
                    RlayerOlist.append(LO)
            cmds.select(clear = True)
            mats_dict_string = str(mats_dict)
            mats_dict_string = mats_dict_string.replace(object_Old,object_old_print_temp)
            RlayerOlist_string = str(RlayerOlist)
            RlayerOlist_string = RlayerOlist_string.replace(object_Old,object_old_print_temp)
            if matAssignsExist == 0:
                print "WARNING: no material assignments found for object: ",object_old_print_temp
            print 'old_object material assignments = ',mats_dict_string
            print "potential material layer overide detected in layers:",RlayerOlist_string
            cmds.select(clear = True)
            return mats_dict,LayerMats_dic,layerOverM2,object_Old,object_New,render_layers_in_scene,matAssignsExist

        def UVsetLinking(object_Old,object_New,renderLayers):
            print "old object UV sets check:"
            UvSetTexturesDict = {}
            uvAddress = []
            setAddressOLD = ""
            uvAddDic = {}
            uvNameDic = {}
            texADDdic = {}
            object_Old = (str(object_Old))
            object_New = (str(object_New))
            renderLayers = cmds.ls(type = "renderLayer")
            tmpOBJ = object_Old
            lightLinkingDict = []
            if "Shape" in tmpOBJ:
                object_Old_Parent = cmds.listRelatives(object_Old, parent = True) or []
                object_Old_Child = object_Old
                object_Old = object_Old_Parent
                object_Old = tmpOBJ
            if "Shape" not in tmpOBJ:
                objectChild = cmds.listRelatives(object_Old, children = True) or []
                object_Old_Child = objectChild
                object_Old_Parent = object_Old
                object_Old = object_Old_Child
            object_Old = object_Old[0]
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            cmds.select(clear = True)
            cmds.select(object_Old)
            obj_UVsets = cmds.polyUVSet( query=True, allUVSets=True )
            cmds.select(clear = True)
            textures = cmds.ls(type = "file")
            for tex in textures:
                setAddress = cmds.uvLink(query = True, texture = tex) or []
                for set in setAddress:
                    if object_Old in set:
                        setAddressOLD = set
                        setName = cmds.getAttr(setAddressOLD)
                        uvAddress.append(setAddressOLD)
                        uvAddDic[str(setAddressOLD)] = tex
                        uvNameDic[setName] = setAddressOLD
                        texADDdic[tex] = setAddressOLD
            print "object UV_sets = ",obj_UVsets
            return uvNameDic,texADDdic,uvAddDic,uvAddress,obj_UVsets,object_Old,object_New,renderLayers

        def polySmoothOBJ(object_Old,object_New,renderLayers):
            print "old object polySmooth detection check:"
            object_Old_smooth_node_found = 0
            object_New_smooth_node_found = 0
            object_Old_smooth_division_level = 0
            object_New_smooth_division_level = 0
            old_object_polysmooth_node = []
            new_object_smooth_node = 'none'
            smoothNodes = cmds.ls(type = "polySmoothFace") or []
            #print 'smoothNodes = ',smoothNodes
            for smoothNode in smoothNodes:
                #print ' '
                #print 'smoothNode = ',smoothNode
                smooth_node_connections = cmds.listConnections(smoothNode, destination = True)
                #print 'smooth_node_connections = ',smooth_node_connections
                for connection in smooth_node_connections:
                    #print 'connection = ',connection
                    #print 'object_Old = ',object_Old
                    #print 'object_New = ',object_New
                    if connection in object_Old:
                        #print 'connection found in object_Old'
                        old_object_polysmooth_node.append(smoothNode)
                        object_Old_smooth_node_found = 1
                        object_Old_smooth_division_level = cmds.polySmooth(smoothNode, query = True, divisions = True)
                    if connection in object_New:
                        #print 'connection found in object_New'
                        new_object_smooth_node = smoothNode
                        object_New_smooth_division_level = cmds.polySmooth(smoothNode, query = True, divisions = True)
                        object_New_smooth_node_found = 1
            #print 'xxx'
            #print 'object_Old_smooth_node_found = ',object_Old_smooth_node_found
            #print 'object_New_smooth_node_found = ',object_New_smooth_node_found
            print 'old_object polysmooth nodes = ',old_object_polysmooth_node
            print 'new_object polysmooth nodes = ',new_object_smooth_node
            return object_Old,object_New,object_Old_smooth_node_found,object_New_smooth_node_found,object_Old_smooth_division_level,object_New_smooth_division_level,new_object_smooth_node

        def visibilty(object_Old,object_New,renderLayers):
            print "old object visibility check:"
            visDic = {}
            vizPath = object_Old + ".visibility"
            for R in renderLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = R)
                vis = cmds.getAttr(vizPath)
                visDic[R] = vis
            print 'old object visibility = ',visDic
            return visDic,object_Old, object_New

        def displacementNodes(object_Old,object_New,renderLayers):
            print "old object displacement node check:"
            if "Shape" in object_Old:
                pass
            else:
                chil = cmds.listRelatives(object_Old, children = True)
                object_Old = chil[0]
            displacement_extra_attr_dic = {}
            displacement_extra_attributes = ['displayMapBorders','vraySeparator_vray_subquality','vrayOverrideGlobalSubQual','vrayViewDep','vrayEdgeLength','vrayMaxSubdivs','vraySeparator_vray_displacement','vrayDisplacementNone','vrayDisplacementStatic','vrayDisplacementType','vrayDisplacementAmount','vrayDisplacementShift','vrayDisplacementKeepContinuity','vrayEnableWaterLevel','vrayWaterLevel','vrayDisplacementCacheNormals','vray2dDisplacementResolution','vray2dDisplacementPrecision','vray2dDisplacementTightBounds','vray2dDisplacementMultiTile','vray2dDisplacementFilterTexture','vray2dDisplacementFilterBlur','vrayDisplacementUseBounds','vrayDisplacementMinValue','vrayDisplacementMaxValue','vrayOverrideGlobalSubQual','vrayViewDep','vrayEdgeLength','vrayMaxSubdivs','vrayDisplacementNone','vrayDisplacementStatic','vrayDisplacementType','vrayDisplacementAmount','vrayDisplacementShift','vrayDisplacementKeepContinuity','vrayEnableWaterLevel','vrayWaterLevel','vrayDisplacementCacheNormals','vray2dDisplacementResolution','vray2dDisplacementPrecision','vray2dDisplacementTightBounds','vray2dDisplacementMultiTile','vray2dDisplacementFilterTexture','vrayDisplacementUseBounds','vrayDisplacementMinValue','vrayDisplacementMaxValue']
            for displacement_extra_attribute in displacement_extra_attributes:
                disp_attr_full = object_Old + '.' + displacement_extra_attribute
                disp_attr_exists = cmds.attributeQuery(displacement_extra_attribute,node = object_Old,exists = True)
                if disp_attr_exists == 1:
                    disp_attr_value = cmds.getAttr(disp_attr_full)
                    displacement_extra_attr_dic[displacement_extra_attribute] = disp_attr_value
            vrayDisplacement_filePath = ""
            object_Old_DispNodeList = []
            vrayDispNode = []
            object_Old_DispNode = "None"
            dispNodeConnections = []
            fileConnections = []
            displacement_map_con = []
            disp_fileConnection = []
            displacement_map_connection = []
            disp_fileConnect = ""
            dispValDic = {}
            overide_dispValDic = {}
            dispLayerOR = []
            UVdic = {}
            UVdic_texSet = {}
            UVdic_label = {}
            conNodeDic = {}
            layerTexFiles = []
            layerTexDispTextures = []
            ramplayerConnects = []
            UvchooseRampC = []
            fileTextureName = ""
            def_fileTextureName = ""
            def_vrayDisplacementAmount = 0
            def_dispShift = 0
            def_vrayEdgeLength = 0
            def_dispMaxSubdivs = 0
            displacementBlackBox = 0
            overrideGlobalDisplacement = 0
            displacement_keepContinuity = 0
            layerTexDetect = 0
            rampDetect = 0
            object_Old = object_Old
            object_New = object_New
            cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
            if "Shape" in object_Old:
                parents = cmds.listRelatives(object_Old, parent = True) or []
                object_OldParent = parents
                object_Old = object_OldParent[0]
                object_OldChild = object_Old
            else:
                children = cmds.listRelatives(object_Old, children = True) or []
                object_OldParent = object_Old
                object_Old = object_Old
                object_OldChild = children
            dispNodes = cmds.ls(type = "VRayDisplacement") or []
            for DN in dispNodes:
                dispChildren = cmds.listConnections(DN) or []
                if object_Old in dispChildren:
                    object_Old_DispNodeList.append(DN)
            lsSize = len(object_Old_DispNodeList)
            if lsSize > 0:
                object_Old_DispNode = object_Old_DispNodeList[0]
            if object_Old_DispNode != "None":
                object_Old_DispNode = object_Old_DispNodeList[0]
                object_Old_DispNode = object_Old_DispNodeList[0]
                for RL in renderLayers:
                    cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                    dispNodeConnections = cmds.listConnections(object_Old_DispNode, s = True, d = True) or []
                    for dnc in dispNodeConnections:
                        NT = cmds.nodeType(dnc)
                        if NT == "file":
                            if dnc not in displacement_map_connection:
                                displacement_map_connection = dnc
                                dcon = dnc
                                key_dcon = object_Old + "_" + RL + "_" + "dcon"
                                dispValDic[key_dcon] = dcon
                        if NT == "VRayMtl":
                            if dnc not in displacement_map_connection:
                                displacement_map_connection = dnc
                                dcon = dnc
                                key_dcon = object_Old + "_" + RL + "_" + "dcon"
                                dispValDic[key_dcon] = dcon
                        if NT == "layeredTexture":
                            layerTexDetect = 1
                            layerConnects = cmds.listConnections(dnc, destination = False)
                            for l in layerConnects:
                                if l != "defaultTextureList1":
                                    if l not in layerTexFiles:
                                        layerTexFiles.append(l)
                            for ltf in layerTexFiles:
                                gts = ltf + ".fileTextureName"
                                atExist = cmds.attributeQuery("fileTextureName", node = ltf, ex = True)
                                if atExist == 1:
                                    layerDispTex = cmds.getAttr(gts)
                                    if layerDispTex not in layerTexDispTextures:
                                        layerTexDispTextures.append(layerDispTex)
                        if NT == "ramp":
                            rampDetect = 1
                            rampNode = dnc
                            vrayDisplacement_filePath = "none"
                            disp_fileConnect = "none"
                            displacement_map_connection = rampNode
                            ramplayerConnects = cmds.listConnections(dnc, destination = False)
                            ramplayerC_2DplaceTex = ramplayerConnects[0]
                            UvchooseRampC = cmds.listConnections(ramplayerC_2DplaceTex, destination = False)
                            UvchooseRamp = UvchooseRampC[0]
                            rampCnoPlugs = cmds.listConnections(UvchooseRamp, destination = False)
                            for rcnp in rampCnoPlugs:
                                if object_Old in rcnp:
                                    rampCs = cmds.listConnections(UvchooseRamp, destination = False, plugs = True)
                                    for rcs in rampCs:
                                        if object_Old in rcs:
                                            rampUVset = rcs
                    displacement_map_connection_size = len(displacement_map_connection)
                    DNT = cmds.nodeType(displacement_map_connection)
                    if DNT == "file":
                        fileName = dnc
                        fileConnectionString = dnc + ".fileTextureName"
                        disp_fileConnect = DNT
                        key_dfc = object_Old + "_" + RL + "_" + "disp_fileConnect"
                        dispValDic[key_dfc] = disp_fileConnect
                        vrayDisplacement_filePath = cmds.getAttr(fileConnectionString)
                        texSet = cmds.uvLink( query = True, texture = dnc )
                        e = len(texSet)
                        if e > 0 :
                            label = cmds.getAttr(texSet)
                            UVdic_texSet[dnc] = texSet
                            UVdic_label[dnc] = label
                        fileConnectionString = dnc + ".fileTextureName"
                        vrayDisplacement_filePath = cmds.getAttr(fileConnectionString)
                    if DNT == "VRayMtl":
                        lc = cmds.listConnections(displacement_map_connection + ".diffuseColor", d = False, s = True)
                        disp_fileConnect = lc[0]
                        key_dfc = object_Old + "_" + RL + "_" + "disp_fileConnect"
                        dispValDic[key_dfc] = disp_fileConnect
                        texSet = cmds.uvLink( query = True, texture = lc[0] )
                        fileName = lc[0]
                        e = len(texSet)
                        if e > 0 :
                            label = cmds.getAttr(texSet)
                            UVdic_texSet[lc[0]] = texSet
                            UVdic_label[lc[0]] = label
                        fileConnectionString = lc[0] + ".fileTextureName"
                        vrayDisplacement_filePath = cmds.getAttr(fileConnectionString)
                    key_fileTextureName = object_Old + "_" + RL + "_" + "displacement_map_connection"
                    z = len(displacement_map_connection)
                    key_fileTextureName = object_Old + "_" + RL + "_" + "vrayDisplacement_filePath"
                    dispValDic[key_fileTextureName] = vrayDisplacement_filePath
                    dispAmount =  object_Old_DispNode + ".vrayDisplacementAmount"
                    dispAmountExists = cmds.attributeQuery("vrayDisplacementAmount",node = object_Old_DispNode,exists = True)
                    if dispAmountExists == 1:
                        dispAmountVal = cmds.getAttr(dispAmount)
                    else:
                        dispAmountVal = 0
                    key_dispAmount = object_Old + "_" + RL + "_" + "dispAmount"
                    dispValDic[key_dispAmount] = dispAmountVal
                    dispShift =  object_Old_DispNode + ".vrayDisplacementShift"
                    dispShiftExists = cmds.attributeQuery("vrayDisplacementShift",node = object_Old_DispNode,exists = True)
                    if dispAmountExists == 1:
                        dispShiftVal = cmds.getAttr(dispShift) or 0
                    else:
                        dispShiftVal = 0
                    key_dispShift = object_Old + "_" + RL + "_" + "dispShift"
                    dispValDic[key_dispShift] = dispShiftVal
                    dispEdgeLength =  object_Old_DispNode + ".vrayEdgeLength"
                    dispEdgeLengthExists = cmds.attributeQuery("vrayEdgeLength",node = object_Old_DispNode,exists = True)
                    if dispEdgeLengthExists == 1:
                        dispEdgeLengthVal = cmds.getAttr(dispEdgeLength) or 0
                    else:
                        dispEdgeLengthVal = 0
                    key_vrayEdgeLength = object_Old + "_" + RL + "_" + "vrayEdgeLength"
                    dispValDic[key_vrayEdgeLength] = dispEdgeLengthVal
                    dispMaxSubdivs =  object_Old_DispNode + ".vrayMaxSubdivs"
                    dispMaxSubdivsExists = cmds.attributeQuery("vrayMaxSubdivs",node = object_Old_DispNode,exists = True)
                    if dispMaxSubdivsExists == 1:
                        dispMaxSubdivsVal = cmds.getAttr(dispMaxSubdivs) or 0
                    else:
                        dispMaxSubdivsVal = 0
                    key_dispMaxSubdivs = object_Old + "_" + RL + "_" + "dispMaxSubdivs"
                    dispValDic[key_dispMaxSubdivs] = dispMaxSubdivsVal
                    overrideGlobalDisplacement = cmds.getAttr( object_Old_DispNode + ".overrideGlobalDisplacement")
                    overrideGlobalDisplacementKey = object_Old + "_" + RL + "_" + "overrideGlobalDisplacement"
                    dispValDic[overrideGlobalDisplacementKey] = overrideGlobalDisplacement
                    displacementBlackBox = cmds.getAttr( object_Old_DispNode + ".blackBox")
                    displacementBlackBoxKey = object_Old + "_" + RL + "_" + "displacementBlackBox"
                    dispValDic[displacementBlackBoxKey] = displacementBlackBox
                    vdkpcExists = cmds.attributeQuery("vrayDisplacementKeepContinuity",node = object_Old_DispNode,exists = True)
                    if vdkpcExists == 1:
                        displacement_keepContinuity = cmds.getAttr(object_Old_DispNode + ".vrayDisplacementKeepContinuity" )
                        displacement_keepContinuityKey = object_Old + "_" + RL + "_" + "displacement_keepContinuity"
                        dispValDic[displacement_keepContinuityKey] = displacement_keepContinuity
                deflayerVals = []
                for valDics in dispValDic:
                    if "defaultRenderLayer" in valDics:
                        deflayerVals.append(valDics)
                        for defLvals in deflayerVals:
                            if "dcon" in defLvals:
                                def_displacement_map_con = dispValDic[defLvals]
                            if "displacement_keepContinuity" in defLvals:
                                def_displacement_keepContinuity = dispValDic[defLvals]
                            if "displacementBlackBox" in defLvals:
                                def_displacementBlackBox = dispValDic[defLvals]
                            if "overrideGlobalDisplacement" in defLvals:
                                def_overrideGlobalDisplacement = dispValDic[defLvals]
                            if "dispAmount" in defLvals:
                                def_vrayDisplacementAmount = dispValDic[defLvals]
                            if "dispShift" in defLvals:
                                def_dispShift = dispValDic[defLvals]
                            if "vrayEdgeLength" in defLvals:
                                def_vrayEdgeLength = dispValDic[defLvals]
                            if "dispMaxSubdivs" in defLvals:
                                def_dispMaxSubdivs = dispValDic[defLvals]
                dispLayerOR = []
                for vals in dispValDic:
                    if "vrayDisplacement_filePath" in vals:
                        tempVal = dispValDic[vals]
                for r in renderLayers:
                    cmds.editRenderLayerGlobals( currentRenderLayer = r )
                    st = object_Old_DispNode + ".displacement"
                    dc = cmds.listConnections(st)
                    for d in dc:
                        t = cmds.nodeType(d)
                        if t == "VRayMtl":
                            conNodeDic[r] = d
                        if t == "file":
                            conNodeDic[r] = d
                        if t == "layeredTexture":
                            conNodeDic[r] = d
                        if t == "ramp":
                            conNodeDic[r] = d
                for c in conNodeDic:
                    if "defaultRenderLayer" in c:
                        defConnectVal = conNodeDic[c]
                for r in renderLayers:
                    if "defaultRenderLayer" not in r:
                        tval = conNodeDic[r]
                        if tval != defConnectVal:
                            v = object_Old + "_" + r + "_disp_con"
                            dispLayerOR.append(v)
                            overide_dispValDic[v] = tval
                for vals in dispValDic:
                    if "displacement_keepContinuity" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_displacement_keepContinuity:
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "overrideGlobalDisplacement" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_overrideGlobalDisplacement:
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "displacementBlackBox" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_displacementBlackBox:
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "dispAmount" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_vrayDisplacementAmount:
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "dispShift" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_dispShift:
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "vrayEdgeLength" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_vrayEdgeLength:
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
                for vals in dispValDic:
                    if "dispMaxSubdivs" in vals:
                        tempVal = dispValDic[vals]
                        if tempVal != def_dispMaxSubdivs:
                            dispLayerOR.append(vals)
                            overide_dispValDic[vals] = tempVal
            if object_Old_DispNode != "None":
                if layerTexDetect != 1 and rampDetect != 1:
                    cmds.select(clear = True)
                    shadEx = cmds.objExists("tempShader")
                    if shadEx == 1:
                        cmds.delete("tempShader")
                    tempNodeName = cmds.createNode("surfaceShader")
                    cmds.lockNode(tempNodeName,lock = False)
                    cmds.rename(tempNodeName, "tempShader")
                    cmds.select(clear = True)
                    cmds.select(object_New)
                    cmds.hyperShade(assign = "tempShader")
                    tempFileMod = fileName + ".outColor"
                    cmds.connectAttr(tempFileMod,"tempShader.outColor", force = True)
                    object_Old_children = cmds.listRelatives(object_Old, children = True)
                    object_Old_child = object_Old_children[0]
                    object_New_children = cmds.listRelatives(object_New, children = True)
                    object_New_child = object_New_children[0]
                    firstConList = []
                    secConList = []
                    thirdConList = []
                    fourthConList = []
                    firstCon = cmds.listConnections(fileName, destination = False)
                    for f in firstCon:
                        if f not in firstConList:
                            if f not in firstConList:
                                firstConList.append(f)
                    for first_connection in firstConList:
                        first = first_connection
                        fType = cmds.nodeType(first)
                        if fType == "uvChooser":
                            firstConList = cmds.listConnections(first, destination = False, plugs = True) or []
                        if fType != "uvChooser":
                            firstConList = cmds.listConnections(first, destination = False) or []
                    siz = len(firstConList)
                    if siz > 0:
                        second = firstConList[0]
                        fType = cmds.nodeType(second)

                        if fType == "uvChooser":
                            secondConList = cmds.listConnections(second, destination = False, plugs = True) or []
                            UVmapAddressOLD = secondConList[0]
                            object_New_shape = cmds.listRelatives(object_New,children = True) or []
                            #print 'object_New_shape = ',object_New_shape
                            #print 'UVmapAddressOLD = ',UVmapAddressOLD
                            UVmapAddressOLD_split = UVmapAddressOLD.split('.')
                            #print 'UVmapAddressOLD_split = ',UVmapAddressOLD_split
                            #print 'UVmapAddressOLD_split 0 = ',UVmapAddressOLD_split[0]
                            #print 'UVmapAddressOLD_split 1 = ',UVmapAddressOLD_split[1]
                            #print 'UVmapAddressOLD_split 2 = ',UVmapAddressOLD_split[2]
                            UVmapAddressNEW = object_New_shape[0] + '.' + UVmapAddressOLD_split[1] + '.' + UVmapAddressOLD_split[2]
                            #print 'UVmapAddressNEW = ',UVmapAddressNEW
                            #print 'object_Old = ',object_Old
                            #print 'object_New = ',object_New
                            print '  '
                            cmds.uvLink( uvSet = UVmapAddressNEW, texture = fileName)
                        else:
                            secondConList = cmds.listConnections(second, destination = False) or []
                        shadEx2 = cmds.objExists("tempShader")
                        if shadEx2 == 1:
                            cmds.delete("tempShader")
                if  rampDetect == 1:
                    cmds.select(clear = True)
                    shadEx = cmds.objExists("tempShader")
                    if shadEx == 1:
                        cmds.delete("tempShader")
                    tempNodeName = cmds.createNode("surfaceShader")
                    cmds.lockNode(tempNodeName,lock = False)
                    cmds.rename(tempNodeName, "tempShader")
                    cmds.select(clear = True)
                    cmds.select(object_New)
                    cmds.hyperShade(assign = "tempShader")
                    tempFileMod = rampNode + ".outColor"
                    cmds.connectAttr(tempFileMod,"tempShader.outColor", force = True)
                    object_Old_children = cmds.listRelatives(object_Old, children = True)
                    object_Old_child = object_Old_children[0]
                    object_New_children = cmds.listRelatives(object_New, children = True)
                    object_New_child = object_New_children[0]
                    cmds.uvLink( uvSet = rampUVset, texture = rampNode)
                    shadEx2 = cmds.objExists("tempShader")
                    if shadEx2 == 1:
                        cmds.delete("tempShader")
                if layerTexDetect == 1:
                    for dft in layerTexFiles:
                        cmds.select(clear = True)
                        shadEx = cmds.objExists("tempShader")
                        if shadEx == 1:
                            cmds.delete("tempShader")
                        tempNodeName = cmds.createNode("surfaceShader")
                        cmds.lockNode(tempNodeName,lock = False)
                        cmds.rename(tempNodeName, "tempShader")
                        fileName = dft
                        cmds.select(clear = True)
                        cmds.select(object_New)
                        cmds.hyperShade(assign = "tempShader")
                        tempFileMod = fileName + ".outColor"
                        cmds.connectAttr(tempFileMod,"tempShader.outColor", force = True)
                        object_Old_children = cmds.listRelatives(object_Old, children = True)
                        object_Old_child = object_Old_children[0]
                        object_New_children = cmds.listRelatives(object_New, children = True)
                        object_New_child = object_New_children[0]
                        firstConList = []
                        secConList = []
                        thirdConList = []
                        fourthConList = []
                        firstCon = cmds.listConnections(fileName, destination = False) or []
                        for f in firstCon:
                            if f not in firstConList:
                                firstConList.append(f)
                        first = firstConList[0]
                        fType = cmds.nodeType(first)
                        second = ''
                        if fType == "uvChooser":
                            firstConList = cmds.listConnections(first, destination = False, plugs = True) or []
                        else:
                            firstConList = cmds.listConnections(first, destination = False) or []
                        siz = len(firstConList)
                        if siz > 0:
                            second = firstConList[0]
                            fType = cmds.nodeType(second)
                        if fType == "uvChooser":
                            secondConList = cmds.listConnections(second, destination = False, plugs = True) or []
                            UVmapAddressOLD = secondConList[0]
                            #UVmapAddressNEW = UVmapAddressOLD.replace(object_Old, object_New)
                            UVmapAddressOLD_split = UVmapAddressOLD.split('.')
                            object_New_shape = cmds.listRelatives(parent = False, children = True)
                            UVmapAddressNEW = object_New_shape[0] + '.' + UVmapAddressOLD_split[1] + '.' + UVmapAddressOLD_split[2]
                            #print 'UVmapAddressNEW = ',UVmapAddressNEW
                            cmds.uvLink( uvSet = UVmapAddressNEW, texture = fileName)
                        else:
                            siz = len(second)
                            if siz != 0:
                                secondConList = cmds.listConnections(second, destination = False) or []
            print 'old_object displacement node = ',object_Old_DispNode
            return vrayDisplacement_filePath,def_vrayDisplacementAmount,def_dispShift,def_vrayEdgeLength,def_dispMaxSubdivs,dispValDic,object_Old,object_New,object_Old_DispNode,displacement_map_con,disp_fileConnection,displacementBlackBox,displacement_keepContinuity,overrideGlobalDisplacement,dispLayerOR,overide_dispValDic,renderLayers,conNodeDic,UVdic_texSet,UVdic_label,displacement_map_connection,disp_fileConnect,displacement_extra_attributes,displacement_extra_attr_dic

        def oldObjectCenter(object_Old,object_New,renderLayers):
            chris = "me"
            return(object_Old,object_New,renderLayers)

        def old_object_v_ray_subdivisions_check(object_Old,object_New,renderLayers):
            print object_old_print_temp + "v-ray subdivision attribute check:"
            v_ray_subdivisions_check = 0
            object_to_check = object_Old[0]
            if 'Shape' in object_Old:
                    object_to_check = object_old_print_temp
            else:
                object_children = cmds.listRelatives(object_Old,children = True) or []
                for child in object_children:
                    if 'Shape' in child:
                        object_to_check = child
            v_ray_subdivisions_check = cmds.objExists(object_to_check + '.vraySubdivUVs')
            if v_ray_subdivisions_check == 1:
                print "v-ray subdivision attribute detected for ", object_old_print_temp
            else:
                print "no v-ray subdivision attribute detected for ",object_old_print_temp
            return(object_Old,object_New,renderLayers,v_ray_subdivisions_check)

        checkAll = 1
        checkTrans = 1
        checkMats = 1
        checkUVsets = 1
        checkLL = 1
        checkObjectProps = 1
        checkRenderStats = 1
        checkSets = 1
        if checkAll == 1:
            OBJ_1_newObjectCenter = oldObjectCenter(object_Old,object_New,renderLayers)
            OBJ_1_visibility = visibilty(object_Old,object_New,renderLayers)
            OBJ_1_polySmooth = polySmoothOBJ(object_Old,object_New,renderLayers)
            OBJ_1_objectIDnode = objectIDnode(object_Old,object_New,renderLayers)
        OBJ_1_renderLayer = renderLayerCheck(object_Old,object_New,renderLayers)
        OBJ_1_ELS = excludeListSets(object_Old,object_New,renderLayers)
        OBJ_1_LL = lightLinking(object_Old,object_New,renderLayers)
        OBJ_1_renderStats = renderStats(object_Old,object_New,renderLayers)
        OBJ_1_vrayObjProps = objectProptertyOverides(object_Old,object_New,renderLayers)
        OBJ_1_objectIDnode = objectIDnode(object_Old,object_New,renderLayers)
        OBJ_1_objectMaterials = materials(object_Old,object_New,renderLayers)
        OBJ_1_UVsets = UVsetLinking(object_Old,object_New,renderLayers)
        OBJ_1_polySmooth = polySmoothOBJ(object_Old,object_New,renderLayers)
        OBJ_1_visibility = visibilty(object_Old,object_New,renderLayers)
        OBJ_1_displacementNodes = displacementNodes(object_Old,object_New,renderLayers)
        OBJ_1_newObjectCenter = oldObjectCenter(object_Old,object_New,renderLayers)
        OBJ_1_v_ray_subdivisions_check = old_object_v_ray_subdivisions_check(object_Old,object_New,renderLayers)
        OBJ_1_translations = translations(object_Old,object_New,renderLayers,old_Xforms)
        OBJ_1_Path = master_path(object_Old,object_New,renderLayers)

        cmds.select(clear = True)
        if checkAll == 1:
            for L in renderLayers:
                cmds.editRenderLayerGlobals( currentRenderLayer = L )
                cmds.hide(OBJ_1_Path[1])
                if "defaultRenderLayer" in L:
                    cmds.editRenderLayerGlobals( currentRenderLayer = L )
        print ' '
        print '-- setting new object attributes --'
        print ' '
        def object_New_Center(object_Old,object_New,renderLayers):
            print "new object centered in frame"
            obj1 = object_Old
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            obj1_WorldSpace = cmds.xform(obj1,q = True, os = True,rotatePivot = True)
            cmds.xform(obj1,cp = True)
            obj1_WorldSpaceCentered = cmds.xform(obj1,q = True, ws = True,rotatePivot = True)
            old_transX = float(obj1_WorldSpaceCentered[0])
            old_transY = float(obj1_WorldSpaceCentered[1])
            old_transZ = float(obj1_WorldSpaceCentered[2])
            cmds.xform(obj1,rotatePivot = obj1_WorldSpace)
            obj1_WorldSpaceFixed = cmds.xform(obj1,q = True, os = True,rotatePivot = True)
            obj2 = object_New
            obj2_WorldSpace = cmds.xform(obj2,q = True, os = True,rotatePivot = True)
            cmds.xform(obj2,cp = True)
            obj2_WorldSpaceCentered = cmds.xform(obj2,q = True, ws = True,rotatePivot = True)
            new_transX = float(obj2_WorldSpaceCentered[0])
            new_transY = float(obj2_WorldSpaceCentered[1])
            new_transZ = float(obj2_WorldSpaceCentered[2])
            transXdiff = (old_transX - new_transX)
            transYdiff = (old_transY - new_transY)
            transZdiff = (old_transZ - new_transZ)
            cmds.xform(obj2,r = True, t = (transXdiff,transYdiff,transZdiff))
            cmds.xform(obj2,rotatePivot = obj2_WorldSpace)
            obj2_WorldSpaceFixed = cmds.xform(obj2,q = True, os = True,rotatePivot = True)

        def object_New_Path(OBJ_1_Path,duplicate_node_names_renamed):
            print "setting new object's path:"
            s = 0
            newObjPath = cmds.listRelatives(object_New, parent = True) or []
            splitPath = OBJ_1_Path[0].split("|")
            pathOBJ = OBJ_1_Path[3]
            sz = len(splitPath)
            curParent = cmds.listRelatives(OBJ_1_Path[2], parent = True) or []
            sizC = len(curParent)
            s = len(newObjPath)
            if sizC < 1:
                curParent = OBJ_1_Path[1]
            if splitPath[sz-3] != curParent[0]:
                if sz > 3:
                    cmds.parent(OBJ_1_Path[2],splitPath[sz-3],relative = True)
                    print "parenting " + object_new_print_temp + "to " + splitPath[sz-3]
                else:
                    print "object at the root level, no hierarchy detected"
                    if s > 0:
                        cmds.parent(OBJ_1_Path[2],splitPath[sz-2],relative = True)
            else:
                print OBJ_1_Path[2] + " already parented to the correct node."
            newPathChil = cmds.listRelatives(newObjPath,children = True) or []
            newPathChilSize = len(newPathChil)
            if s == 0 and newPathChilSize == 0:
                print "no empty parent group to delete"
            if s != 0 and newPathChilSize == 0:
                print "deleting empty parent group ",newObjPath
                if newObjPath[0] in duplicate_node_names_renamed:
                    print 'removing ' + newObjPath[0] + ' from duplicate_node_names_renamed'
                    duplicate_node_names_renamed.remove(newObjPath[0])
                cmds.delete(newObjPath)
            object_New_split = object_New.split('|')
            object_New_raw = object_New_split[-1]
            object_New_full_path = cmds.ls(object_New_raw,long = True)
            print 'object_New_full_path = ',object_New_full_path
            object_Old_split = object_Old.split('|')
            object_Old_raw = object_Old_split[-1]
            object_Old_full_path = cmds.ls(object_Old_raw,long = True)
            print 'object_Old_full_path = ',object_Old_full_path
            cmds.editRenderLayerGlobals( currentRenderLayer = 'defaultRenderLayer')
            cmds.matchTransform(object_New_full_path,object_Old_full_path)
            return(duplicate_node_names_renamed)

        def object_New_renderLayers(OBJ_1_renderLayer):
            print "setting new object render layer add:"
            s = len(OBJ_1_renderLayer[0])
            #print 'OBJ_1_renderLayer[0] = ',OBJ_1_renderLayer[0]
            if s > 1:
                for L in OBJ_1_renderLayer[0]:
                    if L != "defaultRenderLayer":
                        cmds.editRenderLayerMembers( L, OBJ_1_renderLayer[2])
                        print "adding " + object_old_print_temp + " to " + L
            else:
                print object_new_print_temp + " is being added to the default render layer only, " + object_new_print_temp + " not detected in the other layers."

        def object_New_translations(OBJ_1_TX,object_Old,object_New,old_Xforms):
            print "setting new object transforms:"
            transX_attr = OBJ_1_TX[2] + ".translateX"
            transY_attr = OBJ_1_TX[2] + ".translateY"
            transZ_attr = OBJ_1_TX[2] + ".translateZ"
            rotX_attr = OBJ_1_TX[2] + ".rotateX"
            rotY_attr = OBJ_1_TX[2] + ".rotateY"
            rotZ_attr = OBJ_1_TX[2] + ".rotateZ"
            scaleX_attr = OBJ_1_TX[2] + ".scaleX"
            scaleY_attr = OBJ_1_TX[2] + ".scaleY"
            scaleZ_attr = OBJ_1_TX[2] + ".scaleZ"
            defValList = OBJ_1_TX[4]
            object_in_render_layer_list = OBJ_1_TX[5]
            transLayerOveride = OBJ_1_TX[6]
            siiz = len(transLayerOveride)
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            cmds.setAttr(transX_attr,defValList[0])
            print 'setting X transform to ',defValList[0]
            cmds.setAttr(transY_attr,defValList[1])
            print 'setting Y transform to ',defValList[1]
            cmds.setAttr(transZ_attr,defValList[2])
            print 'setting Z transform to ',defValList[2]
            cmds.setAttr(rotX_attr,defValList[3])
            print 'setting X rotation to ',defValList[3]
            cmds.setAttr(rotY_attr,defValList[4])
            print 'setting Y rotation to ',defValList[4]
            cmds.setAttr(rotZ_attr,defValList[5])
            print 'setting Z rotation to ',defValList[5]
            cmds.setAttr(scaleX_attr,defValList[6])
            print 'setting X scale to ',defValList[6]
            cmds.setAttr(scaleY_attr,defValList[7])
            print 'setting Y scale to ',defValList[7]
            cmds.setAttr(scaleZ_attr,defValList[8])
            print 'setting Z scale to ',defValList[8]
            transValuesDict = OBJ_1_TX[0]
            for L in object_in_render_layer_list:
                for tlo in transLayerOveride:
                    override_layer_check_split = tlo.split('&')
                    override_layer_check = override_layer_check_split[1]
                    if L == override_layer_check:
                        cmds.select(object_New)
                        cmds.xform( r=True, cp = True )
                        cmds.select(clear = True)
                        if "transX" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "transX"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".translate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".translateX"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a TX overide value of " + str(va) + " in layer " + L
                            cmds.matchTransform(object_New,object_Old,pivots = True,position = True, rotation = True, scale = True)
                        if "transY" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "transY"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".translate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".translateY"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a TY overide value of " + str(va) + " in layer " + L
                            cmds.matchTransform(object_New,object_Old,pivots = True,position = True, rotation = True, scale = True)
                        if "transZ" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "transZ"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".translate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".translateZ"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a TZ overide value of " + str(va) + " in layer " + L
                            cmds.matchTransform(object_New,object_Old,pivots = True,position = True, rotation = True, scale = True)
                        if "rotX" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "rotX"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".rotate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".rotateX"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a RotX overide value of " + str(va) + " in layer " + L
                        if "rotY" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "rotY"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".rotate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".rotateY"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a RotY overide value of " + str(va) + " in layer " + L
                        if "rotZ" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "rotZ"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".rotate"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".rotateZ"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a RotZ overide value of " + str(va) + " in layer " + L
                        if "scaleX" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "scaleX"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".scale"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".scaleX"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a scaleX overide value of " + str(va) + " in layer " + L
                        if "scaleY" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "scaleY"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".scale"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".scaleY"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a scaleY overide value of " + str(va) + " in layer " + L
                        if "scaleZ" in tlo:
                            v = OBJ_1_TX[1] + "_" + '&'+L+'&' + "_" + "scaleZ"
                            va = transValuesDict[v]
                            cmds.editRenderLayerGlobals( currentRenderLayer = L )
                            ERLAnameT = OBJ_1_TX[2] + ".scale"
                            cmds.editRenderLayerAdjustment(ERLAnameT)
                            ERLAnameTX = OBJ_1_TX[2] + ".scaleZ"
                            cmds.setAttr(ERLAnameTX, va)
                            print "setting a scaleZ overide value of " + str(va) + " in layer " + L
            print 'defValList = ',defValList
            if siiz < 1:
                print "no transform render layer overides detected"
            print 'moving ' + object_Old + ' to position of ' + object_New
            cmds.matchTransform(object_New,object_Old,pivots = True,position = True, rotation = True, scale = True)
            worldSpace_position_pivots_object_New = cmds.xform(object_New,pivots = True, worldSpace = True,query = True)
            cmds.editRenderLayerGlobals( currentRenderLayer = 'defaultRenderLayer')

        def object_New_excludeListSets(OBJ_1_ELS):
            print "setting new object exclude list:"
            object_New = OBJ_1_ELS[2]
            VEsets = OBJ_1_ELS[0]
            si = len(VEsets)
            if si > 0:
                for v in VEsets:
                    cmds.sets(object_New,forceElement = v, edit = True)
                    print "adding " + object_new_print_temp + " to sets: " + v
            else:
                print "no exlude sets detected"

        def object_New_Light_Linking(OBJ_1_LL):
            print "setting new object light linking:"
            LL = OBJ_1_LL[0]
            object_Old = OBJ_1_LL[1]
            object_New = OBJ_1_LL[2]
            lightGroups = []
            lights = []
            childNumDict = {}
            childNumGroup_0 = []
            childNumGroup_1 = []
            childNumGroup_2 = []
            childNumGroup_3 = []
            childNumGroup_4 = []
            childNumGroup_5 = []
            childNumGroup_6 = []
            childNumGroup_7 = []
            childNumGroup_8 = []
            childNumGroup_9 = []
            childNumGroup_10 = []
            if LL != "None":
                for l in LL:
                    kind = cmds.nodeType(l)
                    childNum = cmds.listRelatives(l, children = True) or []
                    if childNum != "":
                        childNumber = len(childNum)
                        childNumDict[l] = childNumber
                        if childNumber == 1:
                            childNumGroup_1.append(l)
                            if kind == "transform":
                                if l not in lightGroups:
                                    lightGroups.append(l)
                for l in LL:
                    kind2 = cmds.nodeType(l)
                    if kind2 != "transform":
                        lights.append(l)
            cmds.lightlink(b = True, light = "defaultLightSet", object = object_New)
            size_childNumGroup_1 = len(childNumGroup_1)
            if size_childNumGroup_1 > 0:
                for child in childNumGroup_1:
                    print "linking " + child + " to " + object_New
                    cmds.lightlink(light = child, object = object_New)
            else:
                print "no light linking detected, using defaultLightSet"
                cmds.lightlink(light = "defaultLightSet", object = object_New)

        def object_New_renderStats(OBJ_1_renderStats):
            print "setting new object render stats:"
            si = len(OBJ_1_renderStats)
            object_Old = OBJ_1_renderStats[1]
            object_New = OBJ_1_renderStats[2]
            defRSlist = OBJ_1_renderStats[3]
            RS_overRideList = OBJ_1_renderStats[4]
            renderStatsDic = OBJ_1_renderStats[5]
            RLOs = OBJ_1_renderStats[6]
            if "Shape" not in object_New:
                chil = cmds.listRelatives(object_New)
                object_New = chil[0]
            old_castsShadows = 0
            old_recieveShadows = 0
            old_motionBlur = 0
            old_primaryVisibility = 0
            old_smoothShading = 0
            old_visibleInReflections = 0
            old_visibleInRefractions = 0
            old_doubleSided = 0
            print 'render state default values = ',renderStatsDic
            for DL in defRSlist:
                if "castsShadows" in DL:
                    old_castsShadows = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".castsShadows"),old_castsShadows)
                if "recieveShadows" in DL:
                    old_recieveShadows = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".receiveShadows"),old_recieveShadows )
                if "motionBlur" in DL:
                    old_motionBlur = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".motionBlur"),old_motionBlur)
                if "primaryVisibility" in DL:
                    old_primaryVisibility = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".primaryVisibility"),old_primaryVisibility)
                if "smoothShading" in DL:
                    old_smoothShading = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".smoothShading"),old_smoothShading)
                if "visibleInReflections" in DL:
                    old_visibleInReflections = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".visibleInReflections"),old_visibleInReflections)
                if "visibleInRefractions" in DL:
                    old_visibleInRefractions = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".visibleInRefractions"),old_visibleInRefractions )
                if "doubleSided" in DL:
                    old_doubleSided = renderStatsDic[DL]
                    cmds.editRenderLayerGlobals( currentRenderLayer='defaultRenderLayer' )
                    cmds.setAttr((object_New + ".doubleSided"),old_doubleSided)
            print 'setting the render state overrides ',RS_overRideList
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_1 = RL + "_" + "castsShadows"
                    if chunk_1 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "castsShadows"
                        old_castsShadows_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".castsShadows"))
                        cmds.setAttr((object_New + ".castsShadows"),old_castsShadows_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_2 = RL + "_" + "receiveShadows"
                    if chunk_2 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "receiveShadows"
                        old_receiveShadows_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".receiveShadows"))
                        cmds.setAttr((object_New + ".receiveShadows"),old_receiveShadows_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_3 = RL + "_" + "motionBlur"
                    if chunk_3 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "motionBlur"
                        old_motionBlur_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".motionBlur"))
                        cmds.setAttr((object_New + ".motionBlur"),old_motionBlur_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_5 = RL + "_" + "smoothShading"
                    if chunk_5 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "smoothShading"
                        old_smoothShading_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".smoothShading"))
                        cmds.setAttr((object_New + ".smoothShading"),old_smoothShading_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_6 = RL + "_" + "visibleInReflections"
                    if chunk_6 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "visibleInReflections"
                        old_visibleInReflections_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".visibleInReflections"))
                        cmds.setAttr((object_New + ".visibleInReflections"),old_visibleInReflections_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_4 = RL + "_" + "primaryVisibility"
                    if chunk_4 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "primaryVisibility"
                        old_primaryVisibility_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".primaryVisibility"))
                        cmds.setAttr((object_New + ".primaryVisibility"),old_primaryVisibility_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_5 = RL + "_" + "visibleInRefractions"
                    if chunk_5 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "visibleInRefractions"
                        old_visibleInRefractions_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".visibleInRefractions"))
                        cmds.setAttr((object_New + ".visibleInRefractions"),old_visibleInRefractions_lovr)
            for RL in RLOs:
                for R in RS_overRideList:
                    chunk_6 = RL + "_" + "doubleSided"
                    if chunk_6 in R:
                        cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                        ovrKey = object_Old[0] + "_" + RL + "_" + "doubleSided"
                        old_doubleSided_lovr = renderStatsDic[ovrKey]
                        cmds.editRenderLayerAdjustment((object_New + ".doubleSided"))
                        cmds.setAttr((object_New + ".doubleSided"),old_doubleSided_lovr)

        def object_New_VRAY_objectPropOverides(OBJ_1_vrayObjProps):
            print 'setting new object v-ray object properties:'
            size_OBJ_1_vrayObjProps = len(OBJ_1_vrayObjProps)
            if size_OBJ_1_vrayObjProps > 0:
                vray_object_props = OBJ_1_vrayObjProps[2]
                size_vray_object_props = len(vray_object_props)
                if size_vray_object_props != 0:
                    for vray_object_prop in vray_object_props:
                        print 'adding ' + object_new_print_temp + ' to ' + vray_object_prop
                        cmds.sets(object_New,addElement = vray_object_prop)
            else:
                print 'no v-ray object properties detected for ', object_Old

        def object_New_objectID(OBJ_1_objectIDnode):
            print "setting new object v-ray object ID:"
            objectID = OBJ_1_objectIDnode[0]
            objectID_dic = OBJ_1_objectIDnode[3]
            RLOs = OBJ_1_objectIDnode[4]
            object_Old = OBJ_1_objectIDnode[1]
            object_New = OBJ_1_objectIDnode[2]
            objParent = cmds.listRelatives(object_New, parent = True) or []
            objChild = cmds.listRelatives(object_New, children = True) or []
            VoBpropertyDic = {}
            if "Shape" in object_New:
                objParent = objParent
                objChild = object_Old
                obj = objParent
            else:
                objParent = object_Old
            string = "vray addAttributesFromGroup " + objChild[0] + " vray_objectID 1"
            melCmd = string
            if objectID != "None":
                mel.eval(melCmd)
                cmds.setAttr((objChild[0] + ".vrayObjectID"),objectID)
                print "Default render layer v-ray object ID attribute created and set to:",objectID
                for RL in RLOs:
                    if "DefaultRenderLayer" not in RL:
                        if RL in objectID_dic:
                            val = objectID_dic[RL]
                            cmds.editRenderLayerGlobals( currentRenderLayer = RL )
                            cmds.editRenderLayerAdjustment((objChild[0] + ".vrayObjectID"))
                            cmds.setAttr((objChild[0] + ".vrayObjectID"),val)
                            print "Setting an object ID attribute render layer overide of " + str(val) + " for layer, " + RL
            else:
                print "no v-ray object ID attribute detected"

        def object_New_materials(OBJ_1_objectMaterials):
            print "setting new object material assignments:"
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            mats_dict = OBJ_1_objectMaterials[0]
            LayerMats_dic = OBJ_1_objectMaterials[1]
            layerOverM = OBJ_1_objectMaterials[2]
            object_Old = OBJ_1_objectMaterials[3]
            object_New = OBJ_1_objectMaterials[4]
            render_layers_in_scene = OBJ_1_objectMaterials[5]
            matAssignsExist = OBJ_1_objectMaterials[6]
            defMatList = []
            valOLD = []
            valNEW = []
            if matAssignsExist != 0:
                for defMats in mats_dict:
                    if "defaultRenderLayer" in defMats:
                        defMatList.append(defMats)
                for dMat in defMatList:
                    valOLD.append(mats_dict[dMat])
                valOLD = valOLD[0]
                for VO in valOLD:
                    oldVO = object_Old
                    newVO = oldVO.replace(object_Old, object_New)
                    if newVO not in valNEW:
                        valNEW.append(newVO)
                #print ' '
                #print 'valNEW = ',valNEW
                #print ' '
                for va in valNEW:
                    #print ' '
                    #print 'va = ',va
                    #print ' '
                    tmp = va.replace(object_New, object_Old)
                    cmds.select(tmp)
                    cmds.hyperShade(smn = True)
                    tmpMat = cmds.ls(sl = True)
                    tmpMat_clean = []
                    for tm in tmpMat:
                        tmnt = cmds.nodeType(tm)
                        if tmnt != "renderLayer":
                            tmpMat_clean.append(tm)
                    for t in tmpMat_clean:
                        if "Layer" not in t:
                            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
                            cmds.select(clear = True)
                            cmds.select(va)
                            cmds.select(clear = True)
                            cmds.select(va)
                            cmds.hyperShade(assign='lambert1')
                            if '_XXXXXX_' in va:
                                va_split = va.split('_XXXXXX_')
                                va_base_name = va_split[0]
                                print "assigning " + t + " to " + va_base_name
                            else:
                                print "assigning " + t + " to " + va
                            cmds.hyperShade(assign=t)
                            cmds.hyperShade(assign='lambert1')
                            cmds.hyperShade(assign=t)
                            cmds.hyperShade(assign='lambert1')
                            cmds.hyperShade(assign=t)
                            cmds.select(clear = True)
                for L in LayerMats_dic:
                    if "defaultRenderLayer" not in L:
                        lay = L.split("*")
                        oKey = LayerMats_dic[L]
                        compVal = LayerMats_dic[L]
                        listCompare = defMatList[0]
                        if compVal not in listCompare:
                            print "setting a material overide in layer:",L
                            cmds.editRenderLayerGlobals( currentRenderLayer = L)
                            mat = LayerMats_dic[L]
                            cmds.select(object_New)
                            cmds.hyperShade(assign = mat)
                            cmds.select(clear = True)
            if matAssignsExist == 0:
                print "* WARNING: no materials assigned to ",object_new_print_temp

        def object_New_UVsetLinking(OBJ_1_UVsets):
            print "setting new object UV sets:"
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer" )
            object_Old = OBJ_1_UVsets[5]
            object_New = OBJ_1_UVsets[6]
            uvNameDic = OBJ_1_UVsets[0]
            texADDdic = OBJ_1_UVsets[1]
            uvAddDic = OBJ_1_UVsets[2]
            uvAddress = OBJ_1_UVsets[3]
            obj_UVsets = OBJ_1_UVsets[4]
            renderLayers = OBJ_1_UVsets[7]
            UV_sets_object_New = []
            uvAddress_NEW = []
            uvNameDic_NEW = {}
            uvAddDic_NEW = {}
            texADDdic_NEW = {}
            textures = cmds.ls(type = "file")
            for tex in textures:
                setAddress = cmds.uvLink(query = True, texture = tex) or []
                for set in setAddress:
                    if object_Old in set:
                        setAddressNEW = set
                        setName = cmds.getAttr(setAddressNEW)
                        uvAddress_NEW.append(setAddressNEW)
                        uvAddDic_NEW[str(setAddressNEW)] = tex
                        uvNameDic_NEW[setName] = setAddressNEW
                        texADDdic_NEW[tex] = setAddressNEW
            UV_sets_NAME_object_New = cmds.polyUVSet( object_New, query = True, allUVSets = True ) or []
            print "UV sets found for " + object_new_print_temp + " : ",UV_sets_NAME_object_New
            setList = []
            NO_setIND_dic = {}
            NO_indices = cmds.polyUVSet(object_New, query = True, allUVSetsIndices = True ) or []
            a = 0
            number_of_uv_sets = UV_sets_NAME_object_New
            if number_of_uv_sets > 0:
                for uv in UV_sets_NAME_object_New:
                    NO_setIND_dic[uv] = NO_indices[a]
                    a = (a + 1)
            for texDicNEW in texADDdic_NEW:
                for texDicOLD in texADDdic:
                    if texDicNEW == texDicOLD:
                        OLDuvlink = texADDdic[texDicOLD]
                        name_OLDuvlink = cmds.getAttr(OLDuvlink)
                        for name in UV_sets_NAME_object_New:
                            if name == name_OLDuvlink:
                                for NO in NO_setIND_dic:
                                    if name == NO:
                                        ind = NO_setIND_dic[name]
                                        set_string = object_New + ".uvSet[" + str(ind) + "]" + ".uvSetName"
                                        n = cmds.getAttr(set_string)
                                        print "setting a UVset link for texture map " + texDicNEW + " to the UV set " + n
                                        g = cmds.getAttr(set_string)
                                        cmds.uvLink(uvSet = set_string, texture = texDicNEW)

        def object_New_polySmoothOBJ(OBJ_1_polySmooth):
            print "setting new object polySmooth attribute:"
            object_Old = OBJ_1_polySmooth[0]
            object_New = OBJ_1_polySmooth[1]
            object_Old_smooth_node_found = OBJ_1_polySmooth[2]
            object_New_smooth_node_found = OBJ_1_polySmooth[3]
            object_Old_smooth_division_level = OBJ_1_polySmooth[4]
            object_New_smooth_division_level = OBJ_1_polySmooth[5]
            new_object_smooth_node = OBJ_1_polySmooth[6]
            if object_Old_smooth_node_found == 1:
                if object_New_smooth_node_found == 0:
                    #print 'object_New_smooth_node_found = ',object_New_smooth_node_found
                    cmds.polySmooth(object_New ,mth = 0, sdt = 2, ovb = 1, ofb = 1, ofc = 1, ost = 0, ocr = 0, dv = object_Old_smooth_division_level, bnr = 1, c = 1, kb = 1, ksb = 1, khe = 0, kt = 1, kmb = 1, suv = 1, peh = 0, sl = 1, dpe = 1, ps = .1, ro = 1, ch = 1)
                    print "applying a smoothing node to " + object_new_print_temp + " at division level ", object_Old_smooth_division_level
                else:
                    #print 'object_New_smooth_node_found = ',object_New_smooth_node_found
                    print 'found an existing smoothing node on new object, deleting ',new_object_smooth_node
                    print 'adding a smoothing node at smoothing level ',object_Old_smooth_division_level
                    cmds.delete(new_object_smooth_node)
                    cmds.polySmooth(object_New ,mth = 0, sdt = 2, ovb = 1, ofb = 1, ofc = 1, ost = 0, ocr = 0, dv = object_Old_smooth_division_level, bnr = 1, c = 1, kb = 1, ksb = 1, khe = 0, kt = 1, kmb = 1, suv = 1, peh = 0, sl = 1, dpe = 1, ps = .1, ro = 1, ch = 1)
                    #print "smoothing node detected for " + object_new_print_temp + ", NO additional smoothing applied"
            else:
                print "no smoothing detected for " + object_old_print_temp + ", applying no smoothing to " + object_new_print_temp


        def object_New_visibility(OBJ_1_visibility):
            print "setting new object visibility:"
            visDic = OBJ_1_visibility[0]
            object_Old = OBJ_1_visibility[1]
            object_New = OBJ_1_visibility[2]
            RLs = cmds.ls(type = "renderLayer")
            visPathNew = object_New + ".visibility"
            defVisVal = visDic["defaultRenderLayer"]
            cmds.editRenderLayerGlobals( currentRenderLayer = "defaultRenderLayer")
            print "setting the default renderLayer visibility to " + str(defVisVal)
            cmds.setAttr(visPathNew,defVisVal)
            for r in RLs:
                cmds.editRenderLayerGlobals( currentRenderLayer = r)
                if r != "defaultRenderLayer":
                    if r in visDic:
                        visVal = visDic[r]
                        if visVal != defVisVal:
                            cmds.editRenderLayerAdjustment((object_New + ".visibility"))
                            print "setting the visibility for " + object_new_print_temp + " to " + str(visVal) + " in render layer " + r
                            cmds.setAttr(visPathNew,visVal)

        def object_New_displacementNode(OBJ_1_displacementNodes):
            print "setting new object displacement node: ",OBJ_1_displacementNodes[8]
            object_Old = OBJ_1_displacementNodes[6]
            object_New = OBJ_1_displacementNodes[7]
            object_Old_DispNode = OBJ_1_displacementNodes[8]
            displacement_extra_attributes = OBJ_1_displacementNodes[22]
            displacement_extra_attr_dic = OBJ_1_displacementNodes[23]
            extra_disp_attr_exists = len(displacement_extra_attr_dic)
            if "Shape" in object_New:
                object_New_parent = cmds.listRelatives(object_New, parent = True)
                object_New_shape = object_New
            else:
                object_New_shape = cmds.listRelatives(object_New, children = True)
                object_New_parent = object_New
            if extra_disp_attr_exists > 1:
                cmds.vray("addAttributesFromGroup", object_New_shape, "vray_subquality", 1)
                cmds.vray("addAttributesFromGroup", object_New_shape, "vray_displacement", 1)
                for displacement_extra_attribute in displacement_extra_attributes:
                    if displacement_extra_attribute == 'vraySeparator_vray_subquality' or displacement_extra_attribute == 'vraySeparator_vray_displacement':
                        cmds.setAttr((object_New_parent + "." + displacement_extra_attribute),displacement_extra_attr_dic[displacement_extra_attribute], type = 'string')
                    else:
                        if displacement_extra_attribute != 'vrayDisplacementMinValue' and displacement_extra_attribute != 'vrayDisplacementMaxValue' and displacement_extra_attribute != 'vrayDisplacementMinValue' and displacement_extra_attribute != 'vrayDisplacementMaxValue':
                            cmds.setAttr((object_New_parent + "." + displacement_extra_attribute),displacement_extra_attr_dic[displacement_extra_attribute])
                    if displacement_extra_attribute == 'vrayDisplacementMinValue' or displacement_extra_attribute == 'vrayDisplacementMaxValue' or displacement_extra_attribute == 'vrayDisplacementMinValue' or displacement_extra_attribute == 'vrayDisplacementMaxValue':
                        val = displacement_extra_attr_dic[displacement_extra_attribute]
                        val = val[0]
                        cmds.setAttr((object_New_parent + "." + displacement_extra_attribute),val[0],val[1],val[2])
            if object_Old_DispNode != "None":
                vrayDisplacement_filePath = OBJ_1_displacementNodes[0]
                def_vrayDisplacementAmount = OBJ_1_displacementNodes[1]
                def_dispShift = OBJ_1_displacementNodes[2]
                def_vrayEdgeLength = OBJ_1_displacementNodes[3]
                def_dispMaxSubdivs = OBJ_1_displacementNodes[4]
                dispValDic = OBJ_1_displacementNodes[5]
                object_Old = OBJ_1_displacementNodes[6]
                object_New = OBJ_1_displacementNodes[7]
                disp_fileConnection = OBJ_1_displacementNodes[10]
                displacementBlackBox = OBJ_1_displacementNodes[11]
                displacement_keepContinuity = OBJ_1_displacementNodes[12]
                overrideGlobalDisplacement = OBJ_1_displacementNodes[13]
                dispLayerOR = OBJ_1_displacementNodes[14]
                overide_dispValDic = OBJ_1_displacementNodes[15]
                renderLayers = OBJ_1_displacementNodes[16]
                conNodeDic = OBJ_1_displacementNodes[17]
                UVdic_texSet = OBJ_1_displacementNodes[18]
                UVdic_label = OBJ_1_displacementNodes[19]
                displacement_map_connection = OBJ_1_displacementNodes[20]
                disp_fileConnect = OBJ_1_displacementNodes[21]
                displacement_map_con = conNodeDic["defaultRenderLayer"]
                cmds.select(object_New)
                newDispNode = cmds.vray("objectProperties", "add_single","VRayDisplacement")
                cmds.select(clear = True)
                cmds.vray("addAttributesFromGroup", newDispNode[0], "vray_displacement", 1)
                cmds.vray("addAttributesFromGroup", newDispNode[0], "vray_subquality", 1)
                ze = len(displacement_map_con)
                if ze > 0:
                    texString = (displacement_map_con + ".outColor" + " " + newDispNode[0] + ".displacement" )
                    texString2 = "connectAttr -force " + texString
                    mel.eval(texString2)
                cmds.setAttr((newDispNode[0] + ".overrideGlobalDisplacement"),overrideGlobalDisplacement)
                cmds.setAttr((newDispNode[0] + ".blackBox"),displacementBlackBox)
                cmds.setAttr((newDispNode[0] + ".vrayDisplacementKeepContinuity"),displacement_keepContinuity)
                cmds.setAttr((newDispNode[0] + ".vrayDisplacementAmount"),def_vrayDisplacementAmount)
                cmds.setAttr((newDispNode[0] + ".vrayDisplacementShift"),def_dispShift)
                cmds.setAttr((newDispNode[0] + ".vrayEdgeLength"),def_vrayEdgeLength)
                cmds.setAttr((newDispNode[0] + ".vrayMaxSubdivs"),def_dispMaxSubdivs)
                for L in renderLayers:
                    if "defaultRenderLayer" not in L:
                        if L in str(overide_dispValDic) and "dispAmount" in str(overide_dispValDic):
                            for over in overide_dispValDic:
                                if L in over and "disp_con" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".displacement"))
                                    displacement_map_conO = conNodeDic[L]
                                    texString = (displacement_map_conO + ".outColor" + " " + newDispNode[0] + ".displacement" )
                                    texString2 = "connectAttr -force " + texString
                                    mel.eval(texString2)
                            for over in overide_dispValDic:
                                if L in over and "dispAmount" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayDisplacementAmount"))
                                    cmds.setAttr((newDispNode[0] + ".vrayDisplacementAmount"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "dispMaxSubdivs" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayMaxSubdivs"))
                                    cmds.setAttr((newDispNode[0] + ".vrayMaxSubdivs"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "dispShift" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayDisplacementShift"))
                                    cmds.setAttr((newDispNode[0] + ".vrayDisplacementShift"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "vrayEdgeLength" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayEdgeLength"))
                                    cmds.setAttr((newDispNode[0] + ".vrayEdgeLength"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "overrideGlobalDisplacement" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".overrideGlobalDisplacement"))
                                    cmds.setAttr((newDispNode[0] + ".overrideGlobalDisplacement"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "displacement_keepContinuity" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".vrayDisplacementKeepContinuity"))
                                    cmds.setAttr((newDispNode[0] + ".vrayDisplacementKeepContinuity"),overide_dispValDic[over])
                            for over in overide_dispValDic:
                                if L in over and "displacementBlackBox" in over:
                                    cmds.editRenderLayerGlobals( currentRenderLayer = L)
                                    cmds.editRenderLayerAdjustment((newDispNode[0] + ".blackBox"))
                                    cmds.setAttr((newDispNode[0] + ".blackBox"),overide_dispValDic[over])
            else:
                print "no displacement detected"
            cmds.editRenderLayerGlobals( currentRenderLayer = currentRenderLayer )
        if checkAll == 1:
            object_New_renderLayers(OBJ_1_renderLayer)
            object_New_objectID(OBJ_1_objectIDnode)
            object_New_polySmoothOBJ(OBJ_1_polySmooth)
            object_New_visibility(OBJ_1_visibility)
            object_New_displacementNode(OBJ_1_displacementNodes)
        if checkTrans == 1:
            object_New_translations(OBJ_1_translations,object_Old,object_New,old_Xforms)
        if checkMats == 1:
            object_New_materials(OBJ_1_objectMaterials)
        if checkUVsets == 1:
            object_New_UVsetLinking(OBJ_1_UVsets)
        if checkLL == 1:
            object_New_Light_Linking(OBJ_1_LL)
        if checkObjectProps == 1:
            object_New_VRAY_objectPropOverides(OBJ_1_vrayObjProps)
        if checkRenderStats == 1:
            object_New_renderStats(OBJ_1_renderStats)
        if checkSets == 1:
            object_New_excludeListSets(OBJ_1_ELS)
        OBJ_1_v_ray_subdivisions_check = OBJ_1_v_ray_subdivisions_check[3]
        if OBJ_1_v_ray_subdivisions_check == 1:
            print "setting new object v-ray subdivision attribute:"
            if 'Shape' in object_New:
                    object_to_add = object_New
            else:
                object_children = cmds.listRelatives(object_New,children = True) or []
                for child in object_children:
                    if 'Shape' in child:
                        object_to_add = child
            print 'adding v-ray subdivision attribute to',object_to_add
            cmds.vray("addAttributesFromGroup", object_to_add, "vray_subdivision", 1)
        else:
            print 'no v-ray subdivision attribute detected for ' + object_old_print_temp + ', not adding a v-ray subdivision attribute to ' + object_new_print_temp
        OBJ_1_Path = master_path(object_Old,object_New,renderLayers)
        duplicate_node_names_renamed = object_New_Path(OBJ_1_Path,duplicate_node_names_renamed)
        for duplicate_node_name_renamed in duplicate_node_names_renamed:
            if 'Shape' not in duplicate_node_name_renamed:
                chosen_object = 0
                duplicate_node_name_renamed_split = duplicate_node_name_renamed.split('_XXXXXX')
                duplicate_node_name_mod = duplicate_node_name_renamed_split[0]
                object_Old_split = object_Old.split('|')
                object_old_name_raw = object_Old_split[-1]
                if duplicate_node_name_renamed == object_old_name_raw:
                    chosen_object = 1
                    duplicate_node_name_mod = duplicate_node_name_mod + '_old'
                object_New_split = object_New.split('|')
                object_New_name_raw = object_New_split[-1]
                if duplicate_node_name_renamed == object_New_name_raw:
                    chosen_object = 1
                    duplicate_node_name_mod = duplicate_node_name_mod + '_new'
                cmds.select(clear = True)
                cmds.select(duplicate_node_name_renamed)
                renamed_long_name = cmds.ls(selection = True,long = True)
                shape_node_originals = cmds.listRelatives(renamed_long_name,children = True,fullPath = True) or []
                shape_node_originals[::-1]
                for shape_node_original in shape_node_originals:
                    kids_for_shape_node_original = cmds.listRelatives(shape_node_original,children = True) or []
                    number_of_kids_node_original = len(kids_for_shape_node_original)
                    if number_of_kids_node_original == 0:
                        shape_node_mod =  duplicate_node_name_mod + 'Shape'
                        cmds.lockNode(shape_node_original,lock = False)
                        cmds.rename(shape_node_original,shape_node_mod)
                print 'renaming ' + duplicate_node_name_renamed + ' to ' + duplicate_node_name_mod
                cmds.lockNode(duplicate_node_name_renamed,lock = False)
                cmds.rename(duplicate_node_name_renamed,duplicate_node_name_mod)
        panels = cmds.getPanel( type = "modelPanel" )
        for mPanel in panels:
            cmds.modelEditor(mPanel, edit = True, allObjects = 1)

        print ' '
        print "*** finished matching object_new to object_old ***"
        print ' '
def main():
    objectChooseWin()
