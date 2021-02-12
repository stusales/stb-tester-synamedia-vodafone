import stbt


class ChannelOverlay(stbt.FrameObject):
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
        return bool(self.progress_bar_progress)

    @property
    def progress_bar_progress(self):
        """A percentage (a float between 0.0 and 1.0) of the progress bar
         position.
        """
        r = stbt.Region(x=120, y=615, right=1160, bottom=640)
        m = stbt.match("progress-bar-red.png", frame=self._frame, region=r)
        if m:
            x = m.region.right
        else:
            # If the program has just started, it won't have matched
            # "progress-bar-red.png". Let's try a reference image with the
            # circle (the position indicator) at the left edge:
            m = stbt.match("progress-bar-white.png", frame=self._frame,
                           region=r)
            if m:
                x = m.region.x
            else:
                # Progress bar not visible
                return None

        return (x - r.x) / r.width


    @property
    def channel_number(self):
        return int(stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=1075, y=540, right=1155, bottom=590),
            mode=stbt.OcrMode.SINGLE_LINE,
            char_whitelist="0123456789",
            text_color=(255, 255, 255)))


    @property
    def program_title(self):
        return stbt.ocr(
            frame=self._frame,
            region=stbt.Region(x=120, y=540, right=880, bottom=590),
            text_color=(255, 255, 255))
