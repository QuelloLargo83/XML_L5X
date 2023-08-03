import cfg
import utils

XML_FILE = cfg.PLCStcFolder + cfg.bars + 'P16378_PLC_00P.L5X'


from xml.dom import minidom

dom = minidom.parse(XML_FILE)
elements = dom.getElementsByTagName('Routine')


for element in elements:
    print(element.attributes['Name'].value)
