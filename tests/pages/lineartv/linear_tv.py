"""
Author     : stusales at 08/02/2021 stusales@synamedia.com
File       : livetv.py
-*- coding : UTF-8 -*-
"""

import stbt

import tests.core.bitmap
from tests.pages.channelbanner import ChannelBanner
from utils import get_randomized_item, profile, wait


class LinearTV(stbt.FrameObject):
    """Linear TV frameObject"""

    def __init__(self):
        self._frame = None

    @property
    def is_visible(self):
        """Checks to see if the object is visible"""
        # is fullscreen tv displayed
        return

    @property
    def fullscreen(self):
        """This is the fullscreen frame

        :return:
        """
        #    stbt.draw_text('Action                           : Go to fullscreen TV')

        import tests.core.bitmap
        return bool(stbt.press_until_match(stbt.press('KEY_BACK'),
                                           tests.core.bitmap.get_bitmap(self, "BlackScreenMaskCropped.png"),
                                           interval_secs=2, max_presses=5))

    @property
    def check_motion(self):
        """
        Detects if there is any motion in full screen
        Asserts if blackscreen is still seen after <timeout>
        :return:
        """

        #  import tests.core.bitmap
        #  for motionresult in stbt.detect_motion(timeout_secs=float(profile['MOTION_IMAGE_TIMEOUT']),
        #                                         mask=tests.core.bitmap.get_bitmap(self, "VideoMovementMaskCropped.png"),
        #                                         region=stbt.Region(x=127, y=71, width=1024, height=576)):
        #      if motionresult.motion:
        #          stbt.draw_text('Action                          : Fullscreen TV motion detected')
        #          break

        #  assert False, stbt.draw_text('Action                          : Motion TIMEOUT reached, %s seconds',
        #                               timeout=profile["MOTION_IMAGE_TIMEOUT"])

        return bool(stbt.detect_motion(timeout_secs=float(profile['MOTION_IMAGE_TIMEOUT']),
                                       mask=tests.core.bitmap.get_bitmap(self, "VideoMovementMaskCropped.png"),
                                       region=stbt.Region(x=127, y=71, width=1024, height=576)))


def check_for_video():
    """This function will check for motion on fullscreen TV"""

    stbt.draw_text('Action                           : Check for motion on fullscreen TV')

    if not LinearTV().check_motion:
        assert False, stbt.draw_text('Action                          : Motion not detected in %s seconds',
                                     timeout=profile["MOTION_IMAGE_TIMEOUT"])

#  get_video_check().check_motion()


def wait_till_black_screen_dismissed():
    """This function will wait umtil fullscreen shows motion"""

#  get_video_check().check_black_screen()


def goto_fullscreen_tv():
    """This function moves to fullscreen TV. It does not check for video"""

    stbt.draw_text('Action                           : Go to fullscreen TV')

    if not LinearTV().fullscreen:
        assert False, stbt.draw_text('The STB has not reached fullscreen TV')


def tune_to_channel(channel_number):
    """This function tunes to channel number (channel_number)"""

    stbt.draw_text('Tune to channel                  : Channel %s', channel_number)

    for digit in str(channel_number):
        stbt.press('KEY_' + digit)
        wait(0.5)

    stbt.wait_until(lambda: ChannelBanner().is_visible, timeout_secs=5)


def tune_clear_sd_service():
    """This function will return a random clear SD service defined in the <CLEAR_SD_SERVICES> list"""

    clear_sd_service_list = profile["CLEAR_SD_SERVICES"]
    clear_sd_service = get_randomized_item(clear_sd_service_list)
    tune_to_channel(clear_sd_service)

    return clear_sd_service


def tune_clear_hd_service():
    """This function will return a random clear HD service defined in the <CLEAR_HD_SERVICES> list"""

    clear_hd_service_list = profile["CLEAR_HD_SERVICES"]
    clear_hd_service = get_randomized_item(clear_hd_service_list)
    tune_to_channel(clear_hd_service)

    return clear_hd_service


def tune_scrambled_sd_service():
    """This function will return a random scrambled SD service defined in the <SCRAMBLED_SD_SERVICES> list"""

    scrambled_sd_service_list = profile["SCRAMBLED_SD_SERVICES"]
    scrambled_sd_service = get_randomized_item(scrambled_sd_service_list)
    tune_to_channel(scrambled_sd_service)

    return scrambled_sd_service


def tune_scrambled_hd_service():
    """This function will return a random scrambled HD service defined in the <SCRAMBLED_HD_SERVICES> list"""

    scrambled_hd_service_list = profile["SCRAMBLED_HD_SERVICES"]
    scrambled_hd_service = get_randomized_item(scrambled_hd_service_list)
    tune_to_channel(scrambled_hd_service)

    return scrambled_hd_service


def tune_to_default_service():
    """This function will return a random default service defined in the <DEFAULT_SERVICE> list"""

    default_service_list = profile["DEFAULT_SERVICE"]
    default_service = get_randomized_item(default_service_list)
    tune_to_channel(default_service)

    return default_service


def tune_to_favourite_service():
    """This function will return a random favourite service defined in the <FAVOURITE_SERVICE> list"""

    favourite_service_list = profile["FAVOURITE_SERVICE"]
    favourite_service = get_randomized_item(favourite_service_list)
    tune_to_channel(favourite_service)

    return favourite_service
