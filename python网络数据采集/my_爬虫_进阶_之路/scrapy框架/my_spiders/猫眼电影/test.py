# coding:utf-8

'''
@author = super_fazai
@File    : test.py
@connect : superonesfazai@gmail.com
'''

from fzutils.common_utils import save_base64_img_2_local
from fontTools.ttLib import TTFont
from pprint import pprint
from xmltodict import parse

'''字体保存到本地'''
a = 'base64,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'
save_path = '/Users/afa/Desktop/x.woff'
font_xml_save_path = '/Users/afa/Desktop/x.xml'
res = save_base64_img_2_local(save_path=save_path, base64_img_str=a)
print(res)

font = TTFont(save_path)
font.saveXML(font_xml_save_path)
pprint(font.getGlyphOrder())

with open(font_xml_save_path, 'r') as f:
    xml_content = f.read()

xml_dict = dict(parse(xml_input=xml_content))
# pprint(xml_dict)
_ = xml_dict['ttFont']['hmtx']['mtx'][1:-1]
a = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
_ = [dict(item).get('@name') for item in _]
_ = list(zip(_, a))
pprint(_)