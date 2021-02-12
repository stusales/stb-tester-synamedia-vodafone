"""
Author     : stusales at 07/02/2021 stusales@synamedia.com
File       : utils.py
-*- coding : UTF-8 -*-
Un-categorized functions.
"""

import logging
import os
import time
from random import random

import stbt
import yaml


class FileLoader:
    """File loader class"""

    def __init__(self, path):
        self.path = path
        self.file = None

    def __enter__(self):
        base_dir = os.path.dirname(__file__)
        self.file = open(os.path.join(base_dir, self.path), encoding='utf8')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()


def load_project_config(project):
    """
    :param project: device type defined in the <*.conf file>
    :return: profile specific configurations
   """
    with FileLoader(os.path.join("config", 'config.yaml')) as yaml_file:
        data = yaml.safe_load(yaml_file.read())
        return data[project]


device = stbt.get_config('device_under_test', 'device_type')
profile = load_project_config(device)


def wait(duration=2, unit='seconds'):
    """Sleep for a duration

    :param duration: Integer/float value
    :param unit: sleep unit
   """
    stbt.draw_text('Action                           : Wait for %s %s', duration, unit)
    time.sleep(durationToSeconds(duration, unit))


def get_randomized_item(target_list):
    """Select a random item from the <target list>.

     :param target_list: list of items
     :return: single item from target list
    """
    stbt.draw_text('Action                           : Get a random item from the target list')

    items = []
    for x in target_list.values():
        items.append(x)

    variables = int(random.randint(0, len(items) - 1))
    var = (items[variables])
    stbt.draw_text('Action                           : Return value %s', var)

    return var


def durationToSeconds(duration, inputUnit):
    """ Convert input unit to duration in seconds

     :param duration: integer/float unit
     :param inputUnit: unit measurement type for duration
     :return:
    """
    assert inputUnit in ['millis', 'ms', 'milliseconds', 'millisecond',
                         'second', 'seconds',
                         'minute', 'minutes',
                         'hour', 'hours'], \
        'Invalid type: <%s> used for the unit parameter.\n ' \
        'Check the utils file for valid options' % inputUnit
    return durationToMillis(duration, inputUnit) / 1000


def durationToMillis(duration, inputUnit):
    """ Convert input unit to duration in milliseconds

     :param duration: integer/float unit
     :param inputUnit: unit measurement type for duration
     :return:
    """
    if inputUnit == "millis" or inputUnit == "ms" or inputUnit == "milliseconds" or inputUnit == "millisecond":
        return float(duration)
    elif inputUnit == "seconds" or inputUnit == "second":
        return float(duration) * 1000
    elif inputUnit == "minutes" or inputUnit == "minute":
        return float(duration) * 60000
    elif inputUnit == "hours" or inputUnit == "hour":
        return float(duration) * 3600000
    else:
        logging.error("inputUnit: '{}' is not supported".format(inputUnit))
        assert False, "inputUnit: '{}' is not supported".format(inputUnit)
