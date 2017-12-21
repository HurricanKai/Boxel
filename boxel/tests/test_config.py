from boxel.config import Dimensions, Palette
from PIL import Image

def test_dimensions():
    dims = Dimensions(pixel_width=50, img_size=[896, 896])
    dims.pixels_per_box = 3
    dims2 = Dimensions(pixel_width=50, img_size=[896, 896])
    assert dims is dims2

def test_palette():
    colors = Palette(file="palettes/3bit.yml")
    assert colors.name == "3bit"
    assert colors.num_of_colors == 8
