#!/usr/bin/env python
# coding=utf-8
import Colors
import gzip
from subprocess import Popen, PIPE
from os import popen
from sys import stdout, exit, argv
import atexit
from os import path as SysPath


class check_file(object):

    end_val = 0
    fd = None
    execute = None
    bar_length = None

    def __init__(self):
        self.execute = Command()
        atexit.register(self.quit_gracefully)

    def checkfile_shell(self, path):

        check_zip = \
            "file %s | sed 's/^.*gzip.*/gzip/'" % path
        check_ascii = \
            "file %s | sed 's/^.*ASCII.*/ASCII/'" % path
        check_sas = \
            "file %s | sed 's/^.*SAS.*/SAS/'" % path
        check_empty = \
            "file %s | sed 's/^.*empty.*/EMPTY/'" % path

        if self.check_path(path) is False:
            return False

        if self.execute.cmd(check_zip) == 'gzip':
            print Colors.change_color('     File Type: gzip', 'OKGREEN')
            self.fd = gzip.open(path, 'rb')
        elif (self.execute.cmd(check_ascii) == "ASCII" or
                self.execute.cmd(check_sas) == "SAS"):
            print Colors.change_color('     File Type: ASCII', 'OKGREEN')
            self.fd = open(path, 'r')
        elif (self.execute.cmd(check_empty) == 'EMPTY'):
            print Colors.change_color('\n     This File is Empty.', 'FAIL')
            return False
        else:
            print Colors.change_color('\n     Unrecognized file type ', 'FAIL')
            return False
        return True

    def check_first_and_last_line(self):

        num_lines = sum(1 for line in self.fd)
        self.fd.seek(0)

        self.end_val = num_lines
        rows, self.bar_length = popen('stty size', 'r').read().split()
        self.bar_length = int(self.bar_length) - len('  00\rPercent: 100 {1}%')

        print Colors.change_color(
                '     Nombre de lignes au total: %s' % num_lines, 'OKGREEN')

    def cli_progress_test(self, cur_val):

        percent = float(cur_val) / self.end_val
        hashes = '#' * int(round(percent * self.bar_length))
        spaces = ' ' * (self.bar_length - len(hashes))
        stdout.write(
                "\r     Percent: [%s] %d%%" % (
                    hashes + spaces, int(round(percent * 100))))
        stdout.flush()

    def quit_gracefully(self):
        if self.get_fd() is not None:
            self.get_fd().close()
        print ''
        exit()

    def get_fd(self):
        return self.fd

    def question_safe(self, question):
        while True:
            try:
                try_input = raw_input(question)
                if (len(try_input) > 0):
                    return try_input
                else:
                    Message = "\n     No Input Detected"
                    exit(Colors.change_color(Message, 'FAIL'))
            except EOFError:
                self.quit_gracefully()
            except KeyboardInterrupt:
                self.quit_gracefully()

    def check_path(self, path):
        if SysPath.exists(path) and SysPath.isfile(path):
            return True
        else:
            return False
            # tmp = "\n     Le chemin semble incorrect."
            # print Colors.change_color(tmp, 'FAIL')


class Message(object):

    @classmethod
    def printNormalUsage(self):
        print Colors.change_color(NormalUsage, 'OKGREEN')


class Command(object):

    def cmd(self, cmd):
        p = Popen(cmd,
                  shell=True,
                  executable='/bin/bash',
                  stdout=PIPE,
                  stderr=PIPE)
        out, err = p.communicate()
        return out.rstrip()


NormalUsage = """
        USAGE:
                %s "TYPE" "CHEMIN"/"URL"
        TYPE:
                postfix; sendmail; nginx; apache
        CHEMIN:
                Exemple : /var/log/mail.log
        URL:
                www.exemple.fr
""" % argv[0]
