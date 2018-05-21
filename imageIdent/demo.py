# -*- coding: utf-8 -*-
"""
 * Created by PyCharm Community Edition.
 * User: nihuan
 * Date: 18-4-3
 * Time: 下午5:07
 """
__author__ = 'nihuan'


from PIL import Image
import pytesseract
text = pytesseract.image_to_string(Image.open('test.png'), lang='chi_sim')
print(text)
