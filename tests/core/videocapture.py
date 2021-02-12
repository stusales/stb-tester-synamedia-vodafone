"""
Author     : stusales at 04/02/2021 stusales@synamedia.com
File       : videocapture.py
-*- coding : UTF-8 -*-

Bitmap sub-module contains all video defines
"""

import stbt

import tests.core.bitmap
from utils import profile


class VideoCheck:
    """
    Video Capture class
    It contains the methods to get and check motion and black screen
    """

    def check_black_screen(self):
        """
         Checks for a black screen.
         Asserts if blackscreen is still seen after <timeout>
        """
        stbt.draw_text('Action                           : Wait until black screen is dismissed')

        if not stbt.wait_until(lambda: stbt.is_screen_black(
                mask=tests.core.bitmap.get_bitmap(self, "BlackScreenMaskCropped.png")),
                               timeout_secs=float(profile["MOTION_IMAGE_TIMEOUT"])):
            assert True, stbt.draw_text('Black Screen                    : Visible after timeout %s seconds',
                                        timeout=float(profile["MOTION_IMAGE_TIMEOUT"]))

    def check_motion(self):
        """
         Detects if there is any motion on full screen
         Asserts if blackscreen is still seen after <timeout>
         :return:
        """
        stbt.draw_text('Action                           : Check for motion on fullscreen TV')

        for m in stbt.detect_motion(timeout_secs=float(profile['MOTION_IMAGE_TIMEOUT']),
                                    mask=tests.core.bitmap.get_bitmap(self, "VideoMovementMaskCropped.png"),
                                    region=stbt.Region(x=127, y=71, width=1024, height=576)):
            if m.motion:
                stbt.draw_text('Action                          : Fullscreen TV motion detected')
                break

        assert False, stbt.draw_text('Action                          : Motion TIMEOUT reached, %s seconds',
                                     timeout=profile["MOTION_IMAGE_TIMEOUT"])
