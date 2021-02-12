"""
Author     : stusales at 04/02/2021 stusales@synamedia.com
File       : bitmap.py
-*- coding : UTF-8 -*-
Bitmap sub-module contains all image file defines
"""

import inspect
import os

import stbt


def get_bitmap(frame_object, filename):
    """Get the image from obect for comparison

    :param frame_object: Object for comparison
    :param filename: image for comparison
    :return:
    """
    module_dir = os.path.dirname(inspect.getfile(frame_object.__class__))
    folder = stbt.get_config('device_under_test', 'device_type')

    # return os.path.join(module_dir, "images", folder, filename)
    if os.path.exists(os.path.join(module_dir, "images")):
        if os.path.exists(os.path.join(module_dir, "images", filename)):
            return os.path.join(module_dir, "images", filename)
        elif os.path.exists(os.path.join(module_dir, "images", folder, filename)):
            return os.path.join(module_dir, "images", folder, filename)
        assert False, "File {} does not exist".format(filename)
    else:
        assert False, "The <images> folder does not exist"
