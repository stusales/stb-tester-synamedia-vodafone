"""
Author     : stusales at 04/02/2021 stusales@synamedia.com
File       : _init__.py
-*- coding : UTF-8 -*-
"""

from tests.core.videocapture import VideoCheck

__video_check = None


def init():
    global __video_check
    __video_check = VideoCheck()


def get_video_check():
    return __video_check
