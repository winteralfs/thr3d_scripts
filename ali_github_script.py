import sys
import os
sys.path.insert(0, r'C:\Python27\Lib\site-packages')
import requests
import imp

url = 'https://raw.githubusercontent.com/winteralfs/thr3d_scripts/master/lights_palette_mini_v03.py'

page = requests.get(url)
code = page.text
module_name = os.path.split(url)[-1].split('.')[0]
module = imp.new_module(module_name)

exec code in module.__dict__

module.main()
