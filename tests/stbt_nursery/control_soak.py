# Copyright 2019 Stb-tester.com Ltd.

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from builtins import *  # pylint:disable=redefined-builtin,unused-wildcard-import,wildcard-import,wrong-import-order

import cv2
import numpy
import stbt


def soak_remote_control(
        key_next="KEY_RIGHT", key_prev="KEY_LEFT",
        region=stbt.Region.ALL, mask=None, count=100):
    """
    Soaks a remote control by pressing KEY_LEFT and KEY_RIGHT keys and making
    sure they have an effect each time.  We check that every time we press
    KEY_LEFT and KEY_RIGHT we get back to where we started.  This should be
    sufficient to detect missed keypresses and intermittent double presses.

    Use ``region`` and/or ``mask`` to exclude parts of the page that might
    change from press to press, such as picture-in-picture video or clocks.
    """
    if mask is None:
        m = stbt.crop(
            numpy.ones(stbt.get_frame().shape[:2], dtype=numpy.uint8) * 255,
            region)
    else:
        m = stbt.load_image(mask, cv2.IMREAD_GRAYSCALE)

    # Get in a position where we'll be able to press left later. Note: no
    # assertion - it's ok if we can't move right right now
    stbt.press(key_next)
    print(region, m.shape)
    stbt.press_and_wait(key_next, region=region, mask=m)  # pylint:disable=stbt-unused-return-value

    # Grab reference images of the left and right position. We need these to
    # check that we've actually moved, and haven't moved too far. We add an
    # alpha channel (transparency) using the user-supplied mask.
    right_template = numpy.append(stbt.crop(stbt.get_frame(), region),
                                  m[:, :, numpy.newaxis],
                                  axis=2)
    cv2.imwrite("right_template.png", right_template)

    if stbt.press_and_wait(key_prev, region=region, mask=m).status == \
            stbt.TransitionStatus.START_TIMEOUT:
        raise RuntimeError(
            "No movement after pressing %r during setup" % (key_prev,))
    if stbt.match(right_template, region=region):
        raise RuntimeError(
            "Setup error: No detectable differences after pressing %r"
            % (key_prev,))
    left_template = numpy.append(stbt.crop(stbt.get_frame(), region),
                                 m[:, :, numpy.newaxis],
                                 axis=2)
    cv2.imwrite("left_template.png", left_template)

    # Error messages:
    missed_press = "Missed keypress: No change after pressing %s"
    double_press = \
        "Didn't find expected screen after pressing %s (double keypress?)"

    # Now we perform the actual test:
    for _ in range(count // 2):
        assert stbt.press_and_wait(key_next, region=region, mask=m), \
            missed_press % (key_next,)
        assert stbt.match(right_template, region=region), \
            double_press % (key_next,)
        assert stbt.press_and_wait(key_prev, region=region, mask=m), \
            missed_press % (key_prev,)
        assert stbt.match(left_template, region=region), \
            double_press % (key_prev,)
