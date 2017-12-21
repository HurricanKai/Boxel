from PIL import Image
import boxel.service
import numpy as np
import cStringIO
import base64

FILE = "artwork/andycat.jpg"

def test_picture_jpg():
    im, boxels = boxel.service.picture(50, FILE)
    im2 = Image.open(FILE)
    assert im.size == im2.size

#TODO
def test_picture_png():
    assert True == True

def test_website():
    im, boxels = boxel.service.website(50, 'https://www.yahoo.com')
    assert True == True

