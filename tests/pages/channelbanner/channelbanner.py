"""
Author     : stusales at 04/02/2021 stusales@synamedia.com
File       : channel_banner.py
-*- coding : UTF-8 -*-
"""

import re

import stbt

import tests.core.bitmap
from utils import profile


class ChannelBanner(stbt.FrameObject):
    """The overlay that appears at the bottom of the screen when you go to
     live tv or when you change channel.

     This is a "Page Object" that represents a particular page of your
     app. Each instance of this class has a member (``self._frame``)
     which is a video-frame captured when the instance is created.
     Properties of this class describe the state of the device-under-test
     *when the instance was created*, so properties must pass
     ``frame=self._frame`` to any image-processing functions (such as
     `stbt.match` or `stbt.ocr`).

     For more information about Page Objects, see "Object Repository" in
     the Stb-tester manual:
     https://stb-tester.com/manual/object-repository

     You can debug your Page Objects in the Object Repository tab of
     your Stb-tester Portal:
     https://synamedia.stb-tester.com/app/#/objects
    """

    @property
    def is_visible(self):
        """Checks to see if the object is visible"""
        return bool(self.progress_bar_progress)

    @property
    def progress_bar_progress(self):
        """A percentage (a float between 0.0 and 1.0) of the progress bar
         position.
        """
        r = stbt.Region(x=120, y=615, right=1160, bottom=640)
        m = stbt.match(tests.core.bitmap.get_bitmap(self, "ProgressBarRed.png"), frame=self._frame, region=r)
        if m:
            x = m.region.right
        else:
            # If the program has just started, it won't have matched
            # "progress-bar-red.png". Let's try a reference image with the
            # circle (the position indicator) at the left edge:
            m = stbt.match(tests.core.bitmap.get_bitmap(self, "ProgressBarWhite.png"), frame=self._frame, region=r)
            #  m = stbt.match("ProgressBarWhite.png", frame=self._frame,
            #                 region=r)
            if m:
                x = m.region.x
            else:
                # Progress bar not visible
                return None

        return (x - r.x) / r.width

    @property
    def channel_number(self):
        """Gets the channel property"""

        return int(stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=1075, y=540, right=1155, bottom=590),
            mode=stbt.OcrMode.SINGLE_LINE,
            char_whitelist="0123456789",
            text_color=(255, 255, 255)))

    @property
    def program_title(self):
        """Gets the program title property"""

        text = stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=120, y=540, right=880, bottom=590),
            text_color=(255, 255, 255))

        # OCR is a little unreliable at reading " S01 E23" at the end of a
        # title.  It sometimes mistakes an "S" for a "5" and vice-versa.  We
        # fix this up here:
        def fix_series_episode(m):
            s, e = m.groups()
            return " S%s E%s" % (s.replace("S", "5"), e.replace("S", "5"))

        return re.sub(r"\s[S5]([0-9S]+)\sE([0-9S]+)$", fix_series_episode, text)

    @property
    def program_timing(self):
        """Gets the program timing property"""

        return stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=126, y=507, right=267, bottom=538),
            # mode=stbt.OcrMode.SINGLE_LINE,
            # char_whitelist="0123456789",
            text_color=(255, 255, 255))


def wait_until_channel_banner_dismissed():
    """This function will wait until the channel banneris dismissed.
         Assert if the channel banner is still visible after the <CHANNEL_BANNER_TIMEOUT> timeout value.
    """

    assert stbt.wait_until(lambda: not ChannelBanner().is_visible,
                           timeout=profile["CHANNEL_BANNER_TIMEOUT"]), stbt.draw_text(
        'Channel banner                  : Visible - NOK')


def bring_up_channel_banner():
    """Bring up the channel banner"""

    stbt.draw_text('Action                           : Bring up Channel Banner')
    if stbt.wait_until(lambda: not ChannelBanner().is_visible):
        stbt.press('KEY_SELECT')

    class GetBanner:
        count = 0

        @staticmethod
        def get_banner():
            """Wait unti banner is visible
             :return: banner object
            """

            b = ChannelBanner()
            if b.is_visible:
                stbt.draw_text('Channel banner                  : Visible - OK')
                return b

    return stbt.wait_until(GetBanner().get_banner, predicate=lambda x: x is not None)


def get_banner_channel_number():
    """This function returns the channel number on the channel banner"""

    stbt.draw_text('Action                           : Get the banner channel number')

    chan_num = int(ChannelBanner().channel_number)

    assert (chan_num is None), stbt.draw_text("Unable to capture the channel number")
    stbt.draw_text('Channel number                   :  {}'.format(chan_num))

    return chan_num


def get_banner_channel_title():
    """This function returns the channel title on the channel banner"""

    stbt.draw_text('Action                           : Get the banner channel title')

    channel_title = ChannelBanner().program_title

    assert (channel_title is None), stbt.draw_text("Unable to capture the channel title")
    stbt.draw_text('Channel title                    :  {}'.format(channel_title))

    return channel_title


def get_banner_channel_timings():
    """This function will check for the event timings"""

    stbt.draw_text('Action                           : Get the event timings')

    event_timings = ChannelBanner().program_timing

    assert (event_timings is None), stbt.draw_text("Unable to capture event time details")
    stbt.draw_text('Progress Bar                     :  {}'.format(event_timings))

    return event_timings


def get_banner_event_progress():
    """This function will check for the event progress"""

    stbt.draw_text('Action                           : Get the event progress')

    event_progress = ChannelBanner().progress_bar_progress

    assert (event_progress is None), stbt.draw_text("Unable to capture progress bar details")
    stbt.draw_text('Progress Bar                     :  {}'.format(event_progress))

    return event_progress


def verify_channel_number(chan_num):
    """This function will verify if the stb is tuned to expected channel number (channel_number)"""

    curr_channel = get_banner_channel_number
    assert curr_channel == chan_num, stbt.draw_text('Expected channel number %s, Actual channel number %s',
                                                    chan_num, curr_channel)


def verify_channel_title(channel_title):
    """This function will verify if the channel title is as expected (channel_title)"""

    curr_title = get_banner_channel_title
    assert curr_title == channel_title, stbt.draw_text('Expected channel title %s, Actual channel title %s',
                                                       channel_title, curr_title)
