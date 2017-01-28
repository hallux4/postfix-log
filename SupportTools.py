#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sys import argv
from PersonalTools.CommonTools import Message


class Controller(object):

    def __init__(self):
        self._module = None
        self._module_list = ['postfix', 'apache']
        self._check_module()

    def _check_module(self):
        if (len(argv) > 2 and
                argv[1] in self._module_list):
            self._module = __import__(argv[1])

    def get_module(self):
        return self._module


def main():
    tools = Controller()

    if tools.get_module() is None:
        exit(Message.printNormalUsage())
    else:
        execute = tools.get_module()
        execute.get_shell()

        # le module est charge dynamiquemet en fonction du parametre CMD, reste
        # a appeler le shell du correspondant.

main()
