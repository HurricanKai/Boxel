# -*- coding: utf-8 -*-
"""
    boxel.service
    ~~~~~~~~~~~~~

    This module provides functions for various media services that can be
    boxelized.
"""

from .config import Dimensions
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urlparse import urlparse
from PIL import Image
import os
import numpy as np
import cStringIO
import base64
import urllib
import math
import requests


def picture(num_of_pixels, img_file, media='picture', palette=None):
    """Returns a Boxelized Image and Pixel Indices
    :param num_of_pixels: The number of boxels wide for an Image
    :param img_file: The filepath of the Image to be used for boxelization
    :param palette: (optional) a :class:`Palette` that is a color palette to
        use for specific colors
    """
    pixels, dims = _prep(num_of_pixels, img_file, media=media)
    return _boxelize(pixels, dims, palette)


def stream(num_of_pixels, msg, updateDims, palette=None):
    """Returns a Boxelized Image and Pixel Indices
    :param num_of_pixels: The number of boxels wide for an Image
    :param msg: A base64 encoded string that is JPEG after decoding
    :param updateDims: Whether or not to update singleton dimensions file.
    :param palette: (optional) a :class:`Palette`
    """
    img_base64 = base64.b64decode(msg.split(',')[1])
    img_file = cStringIO.StringIO(img_base64)
    pixels, dims = _prep(num_of_pixels, img_file, updateDims, media='stream')
    return _boxelize(pixels, dims, palette)


def website(num_of_pixels, url, palette=None):
    """Returns a Boxelized Image and Pixel Indices
    :param num_of_pixels: The number of boxels wide for an Image
    :param url: URL of the website to boxelize
    :param palette: (optional) a :class:`Palette` that is a color palette to
        use for specific colors
    """
    parse = urlparse(url)
    assert parse.scheme == 'https' or parse.scheme == 'http'
    phantom_url = os.getenv('PHANTOMJS_PORT_8910_TCP_ADDR')
    driver = webdriver.Remote(
                command_executor='http://' + phantom_url + ':8910',
                desired_capabilities=DesiredCapabilities.PHANTOMJS)
    driver.set_window_size(560, 275)
    driver.get(url)
    data = driver.get_screenshot_as_png()
    driver.quit()
    img_file = cStringIO.StringIO(data)
    pixels, dims = _prep(num_of_pixels, img_file, media='web')
    out, idxs =  _boxelize(pixels, dims, palette)
    return out, idxs


def _prep(num_of_pixels, filepath, updateDims=False, media='picture'):
    """Returns a numpy array of RGB values and a :class:`Dimensions`
    :param num_of_pixels: The number of boxels wide for an Image
    :param filepath: The filepath of the Image to be turned into a numpy aray
    :param media: (optional) The specified media going to be used
    """
    if media == 'web':
        im = Image.open(filepath).convert('RGB')
        dims = Dimensions(pixel_width=num_of_pixels, img_size=im.size)
        # update dims every website
        dims.__init__(pixel_width=num_of_pixels, img_size=im.size)
    elif media == 'mms':
        file = cStringIO.StringIO(requests.get(filepath).content)
        im = Image.open(file)
        dims = Dimensions(pixel_width=num_of_pixels, img_size=im.size)
        # update dims every image
        dims.__init__(pixel_width=num_of_pixels, img_size=im.size)
    else:
        im = Image.open(filepath)
        dims = Dimensions(pixel_width=num_of_pixels, img_size=im.size)
        if updateDims:
            dims.__init__(pixel_width=num_of_pixels, img_size=im.size)
    pixels = np.asarray(im, dtype=np.uint8)
    return pixels, dims


def _palettize(pixels, palette):
    """Returns a numpy array of RGB values all within the palette's color
        ranges and it's respective pixel indices
    :param pixels: A numpy array of RGB values
    :param palette: A :class:`Palette`
    """
    image = Image.fromarray(pixels, 'RGB')
    colorized_image = image._makeself(
            image.im.convert('P', 1, palette.palette_img.im))
    pixels = np.asarray(colorized_image.convert('RGB'))
    pixel_indices = np.asarray(colorized_image, dtype=np.uint8)
    return pixels, pixel_indices


def _boxelize(pixels, dims, palette=None):
    """Returns a numpy array of RGB values and it's respective pixel indices
    :param pixels: A numpy array of RGB values
    :param dims: A :class:`Dimensions` for size constraints
    :param palette: (optional) a :class:`Palette` that is a color palette to
        use for specific colors
    """
    pixel_unit = dims.pixels_per_box
    if palette:
        pixels, pixel_indices = _palettize(pixels, palette)
    else:
        pixel_indices = np.asarray([], dtype=np.uint8)

    pixels.setflags(write=1)
    for i in xrange(dims.output_dims[0]):
        cols = pixels[:, i * pixel_unit:(i + 1) * pixel_unit]
        if (cols.shape[1] != 0):
            sections = np.resize(
                    cols, (math.ceil(cols.shape[0]/pixel_unit),
                           pixel_unit * pixel_unit, 3))
            avg = np.percentile(sections, 50, axis=1, interpolation='lower')
            out = np.repeat(avg, pixel_unit * pixel_unit, axis=0)
            out_expand = np.resize(out, cols.shape)
            pixels[:, i * pixel_unit:(i + 1) * pixel_unit] = out_expand
    out = Image.fromarray(pixels, 'RGB')

    if palette:
        idxs = pixel_indices[0::dims.pixels_per_box, 0::dims.pixels_per_box]
        idxs.setflags(write=1)
        idxs[np.where(idxs >= palette.num_of_colors)] = palette.num_of_colors - 1
    else:
        idxs = np.asarray([])
    return out, idxs
