import sys
import maya.cmds as cmds
#sys.path.append('/Users/alfredwinters/Desktop/')
sys.path.append('C:/Users/Chris.Winters/Desktop/python_git_hub/')

def _null(*args):
    pass

def batch_review():
    print "object_replacer"
    import batch_review
    reload(batch_review)
    batch_review.main()

def object_replacer():
    print "object_replacer"
    import objectReplacer_v02
    reload(objectReplacer_v02)
    objectReplacer_v02.main()
    
def texture_swapper():
    print "texture_swapper"
    import textures_swapper
    reload(textures_swapper)
    textures_swapper.main()
    
def cleaner():
    print "cleaner_v02"
    import cleaner_v02
    reload(cleaner_v02)
    cleaner_v02.main()

def lights_palette():
    print "lights_palette_v07"
    import lights_palette_v07
    reload(lights_palette_v07)
    lights_palette_v07.main()        
    
def ramp_generator():
    print "ramp_generator"
    import ramp_generator
    reload(ramp_generator)
    ramp_generator.main()
    
def uv_editor():
    print "uv_editor"
    import uv_editor
    reload(uv_editor)
    uv_editor.main()
    
def layers_tool():
    print "layers_tool"
    import layers_tool
    reload(layers_tool)
    layers_tool.main()
    
def xfer_attrs():
    print "xfer_attrs"
    import xfer_attrs
    reload(xfer_attrs)
    xfer_attrs.main()           
    
class custom_shelf():
    def __init__(self, name="lighting_shelf"):
        self.name = name
        self.labelBackground = (0, 0, 0, 0)
        self.labelColour = (.9, .9, .9)        
        self._cleanOldShelf()
        cmds.setParent(self.name)
        self.build()

    def _cleanOldShelf(self):
        if cmds.shelfLayout(self.name, ex=1):
            print "deleting ",self.name
            if cmds.shelfLayout(self.name, q=1, ca=1):
                for each in cmds.shelfLayout(self.name, q=1, ca=1):
                   print "deleting ", each
                   cmds.deleteUI(each)
        else:
            cmds.shelfLayout(self.name, p="ShelfLayout")

    def build(self):
        self.addButon('batch_review','U:/cwinters/thumbnails/pubTHUMBthumb.jpg','batch_review()','-null')
        self.addButon('object_replacer','U:/cwinters/thumbnails/objectReplacerTHUMB.jpg','object_replacer()','-null')
        self.addButon('texture_swapper','U:/cwinters/thumbnails/textureConnectorTHUMB.jpg','texture_swapper()','-null')
        self.addButon('cleaner','U:/cwinters/thumbnails/textureConnectorTHUMB.jpg','cleaner()','-null')
        self.addButon('lights_palette','U:/cwinters/thumbnails/rampGeneratorTHUMB.jpg','lights_palette()','-null')        
        self.addButon('ramp_generator','U:/cwinters/thumbnails/rampGeneratorTHUMB.jpg','ramp_generator()','-null')        
        self.addButon('uv_editor','U:/cwinters/thumbnails/UVadjTHUMB.jpg','uv_editor()','-null')  
        self.addButon('layers_tool','U:/cwinters/thumbnails/UVadjTHUMB.jpg','layers_tool()','-null')  
        self.addButon('xfer_attrs','U:/cwinters/thumbnails/UVadjTHUMB.jpg','xfer_attrs()','-null')  

    def addButon(self, label, icon, command, doubleCommand):
        cmds.setParent(self.name)
        cmds.shelfButton(width=37, height=37, image=icon, l=label, command=command, dcc=doubleCommand, imageOverlayLabel=label, olb=self.labelBackground, olc=self.labelColour)

lighting_tools_shelf = custom_shelf
def main():
    print "!!! SCRIPT IS LOADING !!!"
    lighting_tools_shelf() 
main()