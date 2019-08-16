print " "
print "lighting_tools_shelf loaded (python_git_hub_pub)"
print " "
import sys
import maya.mel as mel
import maya.cmds as cmds
from functools import partial

def lights_palette():
    print "lights_palette function"
    import lights_palette
    reload(lights_palette)
    lights_palette.main()

def batch_review():
    print "batch_review function"
    import batch_review
    reload(batch_review)
    batch_review.main()

def object_replace():
    print "object replace function"
    import object_replace
    reload(object_replace)
    object_replace.main()

def texture_swap():
    print "texture_swap function"
    import texture_swap
    reload(texture_swap)
    texture_swap.main()

def texture_swap_no_gui():
    print "texture_swap_no_gui function"
    import texture_swap_no_gui
    reload(texture_swap_no_gui)
    texture_swap_no_gui.main()

def attributes_swapper():
    print "attributes_swapper function"
    import xfer_attrs
    reload(xfer_attrs)
    xfer_attrs.main()

def cleaner():
    print "cleaner function"
    import cleaner
    reload(cleaner)
    cleaner.main()

def ramp_generator():
    print "ramp_generator function"
    import ramp_generator
    reload(ramp_generator)
    ramp_generator.main()

def rebuild_layers():
    print "rebuild_layers function"
    import rebuild_layers
    reload(rebuild_layers)
    rebuild_layers.main()

def uv_transforms():
    print "uv_transforms function"
    import uv_transforms
    reload(uv_transforms)
    uv_transforms.main()

def quick_links():
    print "quick_links function"
    import quick_links
    reload(quick_links)
    quick_links.main()

def rename_shading_groups():
    print "rename_shading_groups function"
    import rename_shading_groups
    reload(rename_shading_groups)
    rename_shading_groups.main()

def standard_lighting_tool_rotation_fix():
    print "standard_lighting_tool_rotation_fix"
    import standard_lighting_tool_rotation_fix
    reload(standard_lighting_tool_rotation_fix)
    standard_lighting_tool_rotation_fix.main()

def uv_set_chooser():
    print 'uv_set_chooser'
    import uv_set_chooser
    reload(uv_set_chooser)
    uv_set_chooser.main()

def asset_tracker():
    print "asset_tracker"
    import asset_tracker
    reload(asset_tracker)
    asset_tracker.main()

def object_replace_beta():
    print "object_replace_beta"
    import object_replace_beta
    reload(object_replace_beta)
    object_replace_beta.main()

def build_custom_shelf():
    main_shelf = mel.eval('$tempMelVar=$gShelfTopLevel')
    name = "Lighting_Tools"
    #name.labelBackground = (0, 0, 0, 0)
    #name.labelColour = (.9, .9, .9)
    if cmds.shelfLayout(name, ex=1):
        print "deleting ",name
        if cmds.shelfLayout(name, q=1, ca=1):
            for each in cmds.shelfLayout(name, q=1, ca=1):
               print "deleting ", each
               cmds.deleteUI(each)
    else:
        print "creating custom Lighting Tools shelf"
        cmds.shelfLayout(name, p=main_shelf)
    cmds.setParent(name)
    annotation = 'Lights Palette: Creates a palette to display and hide light textures, toggle the visibility of lights, and set and delete render layer overrides for light transforms and light intensity.'
    cmds.shelfButton(annotation = annotation,image = 'U:/cwinters/thumbnails/lights_palette_Logo_small.jpg',command = partial(lights_palette))
    annotation = 'Batch Review: Launches an interactive render for each render layer'
    cmds.shelfButton(annotation = annotation,image = 'U:/cwinters/thumbnails/batchReview_Logo_small.jpg',command = partial(batch_review))
    annotation = 'Object Replace: Replaces one object with another, transfering most attributes settings and shader assignments'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/objectReplacer_Logo_small.jpg', command = partial(object_replace))
    annotation = 'Texture Swap: Transfers the connections and settings from one set of textures to another. Double clicking the button swaps 2 selected textures without launching the GUI'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/texture_swapper_Logo_small.jpg', command = partial(texture_swap),doubleClickCommand = partial(texture_swap_no_gui))
    annotation = 'Rebuild layers Tool: Many useful tools for render layer management'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/layer_tool_Logo_small.jpg', command = partial(rebuild_layers))
    annotation = 'Hypershade Cleaner: Deletes unused shaders and textures from the hypershade'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/cleaner_Logo_small.jpg', command = partial(cleaner))
    annotation = 'Ramp Generator: generates a variety of ramp texures'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/ramp_generator_Logo_small.jpg', command = partial(ramp_generator))
    annotation = 'UV set editor: Allows the manipulation of selected UV shells with transform inputs'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/UV_editor_Logo_small.jpg', command = partial(uv_transforms))
    annotation = '18 quick link: Opens up the 2018 link in shotgun for the chosen brand'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/shotgun_links_tool_Logo_small.jpg', command = partial(quick_links))
    annotation = 'rename shading groups, add/delete a postfix to materials nodes'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/rename_shading_groups_Logo_small.jpg', command = partial(rename_shading_groups))
    annotation = 'rebuilds the standard lighting rig dome rotations'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/standard_lighting_tool_rotation_fix_thumb.jpg', command = partial(standard_lighting_tool_rotation_fix))
    annotation = 'UV set uv_set_chooser, not object selection based, runs faster'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/uv_set_editor_logo_small.jpg', command = partial(uv_set_chooser))
    annotation = 'shows the latest version of assets available and your current version'
    cmds.shelfButton(annotation  = annotation, image = 'U:/cwinters/thumbnails/asset_tracker_logo_small.jpg', command = partial(asset_tracker))
    annotation = 'Object Replace_beta: Replaces one object with another, transfering most attributes settings and shader assignments'
    cmds.shelfButton(annotation  = annotation, image = '', command = partial(object_replace_beta))
