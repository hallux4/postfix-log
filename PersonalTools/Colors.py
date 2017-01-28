#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functools import partial


class bcolors:
    HEADER = '\033[36m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_header():
    global value_string
    return bcolors.HEADER + value_string + bcolors.ENDC


def color_okblue():
    global value_string
    return bcolors.OKBLUE + value_string + bcolors.ENDC


def color_okgreen():
    global value_string
    return bcolors.OKGREEN + value_string + bcolors.ENDC


def color_warning():
    global value_string
    return bcolors.WARNING + value_string + bcolors.ENDC


def color_fail():
    global value_string
    return bcolors.FAIL + value_string + bcolors.ENDC


def color_endc():
    global value_string
    return bcolors.ENDC + value_string + bcolors.ENDC


def color_bold():
    global value_string
    return bcolors.BOLD + value_string + bcolors.ENDC


def color_underline():
    global value_string
    return bcolors.UNDERLINE + value_string + bcolors.ENDC


def change_color(string_to_change, color_to_choose):
    global value_string
    if color_to_choose in color_list:
        value_string = string_to_change
        return color_list[color_to_choose]()
    else:
        print "     je n ai pas cette couleur !"

value_string = None

color_list = {
        'HEADER': partial(color_header),
        'OKBLUE': partial(color_okblue),
        'OKGREEN': partial(color_okgreen),
        'WARNING': partial(color_warning),
        'FAIL': partial(color_fail),
        'ENDC': partial(color_endc),
        'BOLD': partial(color_bold),
        'UNDERLINE': partial(color_underline)}
