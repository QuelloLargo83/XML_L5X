XML_FILE = 'F:\SCRIPTING\XML_L5X\INI\PLC\STERILCAP\P16378_PLC_00P.L5X'

import xml.etree.ElementTree as ET
mytree = ET.parse(XML_FILE)
myroot = mytree.getroot()

for x in myroot[2].findall(' '):
    print('ddd')