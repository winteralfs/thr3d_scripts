# Select the shader you want to add innerLabel material and run.

import pymel.core as pm

selShader = pm.ls(sl=True)

# Selected Shader material override ON and settings
for sel in selShader:
    pm.vray('addAttributesFromGroup', sel, 'vray_specific_mtl', 1)
    sel.vrayEnableSpecificSurfaceShader.set(0)
    sel.vrayEnableGIMaterial.set(0)
    sel.vrayEnableReflectMaterial.set(0)
    sel.vrayEnableRefractMaterial.set(1)
    sel.vrayEnableShadowMaterial.set(0)
    sel.vrayEnableEnvironmentOverride.set(0)
    sel.vrayEnableGIMaterial.set(0)

# innerLabel MTL creation
innerShader = pm.shadingNode('VRayMtl', asShader=True, n='innerLabel_MTL')
innerSG = pm.sets(renderable=True, empty=True, n='innerLabel_SG')
innerShader.outColor >> innerSG.surfaceShader

# innerLabel settings
innerShader.color.set([1, 1, 1])
innerShader.doubleSided.set(0)

# connect innerLabel_MTL to Selected
innerShader.outColor >> selShader[0].vrayRefractMaterial






