"""
Author     : stusales at 04/02/2021 stusales@synamedia.com
-- FILE    : displayBannerLiveTV.py
-*- coding : UTF-8 -*-
"""

import stbt

from tests.pages.channelbanner.channelbanner import bring_up_channel_banner, verify_channel_number, \
    verify_channel_title, get_banner_channel_number, get_banner_channel_title, get_banner_channel_timings, \
    get_banner_event_progress, wait_until_channel_banner_dismissed
from tests.pages.lineartv.linear_tv import goto_fullscreen_tv, tune_clear_sd_service, check_for_video, \
    wait_till_black_screen_dismissed
from utils import wait


def test_displayBannerLiveTV():
    """
     Display the banner in live tv and check that the correct channel number and channel title is displayed
     Asserts if either the channel number or the channel title is not as expected
    """

    stbt.draw_text("Sanity - Display Banner in LiveTV test starts here..")

    goto_fullscreen_tv()
    tune_clear_sd_service()
   # wait_till_black_screen_dismissed()
    check_for_video()
    bring_up_channel_banner()
    verify_channel_number(get_banner_channel_number())
    verify_channel_title(get_banner_channel_title())
    get_banner_channel_timings()
    get_banner_event_progress()
    wait_until_channel_banner_dismissed()
    wait(3)

    stbt.draw_text("Sanity - Display Banner in LiveTV test is COMPLETED!")
