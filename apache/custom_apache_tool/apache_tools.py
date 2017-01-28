#!/usr/bin/env python

from subprocess import Popen, PIPE
from os import listdir
from os import path as SysPath
from Container.OrderedDict2 import OrderedDict
from pprint import pprint

# /usr/sbin/apache2 -V pour get le HTTPD_ROOT, au cas ou...
HTTPD_ROOT = '/etc/apache2/'
env_cmd = "source %senvvars; env" % HTTPD_ROOT
default_dir = "%ssites-enabled/" % HTTPD_ROOT


class vhost_dummy(object):

    def __init__(self):
        self.VHStart = False
        self.VHEnd = False
        self.Alias = []
        self.Name = False
        self.CustomLog = False


class apache_tools(object):

    __env_list = []
    __env_cmd = None
    __custom_log_dic = {}
    __dummys = []

    def __exec_cmd(self):

        p = Popen(
                env_cmd,
                shell=True,
                executable='/bin/bash',
                stdout=PIPE,
                stderr=PIPE)
        out, err = p.communicate()
        return out.strip()

    def __set_apache_env(self):
        self.__env_list = self.__exec_cmd().split('\n')

    def get_log_directory_from_env(self):
        if not self.__env_list:
            self.__set_apache_env()
        if self.__env_list:
            for line in self.__env_list:
                if "APACHE_LOG_DIR" in line:
                    return line.split('=')[1]

    def __open_vhost_from_url(self, path, pattern, fd):

        vhost_dic = OrderedDict()

        nb_line = 0

        for line in fd:
            line = line.strip()
            line = line.lower()
            nb_line = nb_line + 1
            if line.startswith('#') is True or len(line) < 1:
                continue
            if ('servername' not in line and
                'serveralias' not in line and
                'customlog' not in line and
                    'virtualhost' not in line):
                continue

            vhost_dic['%s:%d: ' % (
                path.replace(default_dir, ''), nb_line)] = line

        for key in vhost_dic.iterkeys():
            if '<virtualhost' in vhost_dic[key]:
                dummy = vhost_dummy()
                dummy.Alias = []
                dummy.VHStart = vhost_dic[key].split(' ')[1][:-1]
            elif 'servername' in vhost_dic[key]:
                if pattern in vhost_dic[key]:
                    dummy.Name = vhost_dic[key].split(' ')[1]
            elif 'serveralias' in vhost_dic[key]:
                for alias in vhost_dic[key].split(' '):
                    if pattern in alias:
                        dummy.Alias.append(alias)
            elif 'customlog' in vhost_dic[key]:
                if len(vhost_dic[key].split(' ')) >= 3:
                    tmp_log_path = vhost_dic[key].split(' ')[1]
                    tmp_log_format = vhost_dic[key].split(' ')[2]
                    dummy.CustomLog = '%s:%s' % (tmp_log_path, tmp_log_format)
                    if '${APACHE_LOG_DIR}'.lower() in dummy.CustomLog:
                        tmp_env = self.get_log_directory_from_env()
                        var_dir = '${APACHE_LOG_DIR}'.lower()
                        dummy.CustomLog = dummy.CustomLog.replace(
                                                            var_dir, tmp_env)
            elif '</virtualhost' in vhost_dic[key]:
                dummy.VHEnd = True
                if self.check_dummy_complet(dummy) is True:
                    self.__dummys.append([key, dummy])
                else:
                    continue

    def __open_vhost_from_logfile(self, path, pattern, fd):

        for line in fd:
            line = line.strip()
            line = line.lower()
            if line.startswith('#') is True or len(line) < 1:
                continue
            if 'customlog' not in line:
                continue
            else:
                if len(line.split(' ')) >= 3:
                    tmp_log_path = line.split(' ')[1]
                    tmp_log_format = line.split(' ')[2]
                    CustomLog = '%s:%s' % (tmp_log_path, tmp_log_format)
                    if '${APACHE_LOG_DIR}'.lower() in CustomLog:
                        tmp_env = self.get_log_directory_from_env()
                        var_dir = '${APACHE_LOG_DIR}'.lower()
                        CustomLog = CustomLog.replace(var_dir, tmp_env)
                    if CustomLog.split(':')[0] not in pattern:
                        continue
                    else:
                        logformat = CustomLog.split(':')[1]
                        CustomLog = '%s:%s' % (pattern, logformat)
                        return CustomLog
                    return None

    def check_dummy_complet(self, dummy):
        if dummy.VHStart is False and dummy.VHEnd is False:
            return False
        if not dummy.Alias and dummy.Name is False:
            return False
        if dummy.CustomLog is False:
            return False
        return True

    def get_log_file_from_vhost(self, url, path=default_dir):

        if not SysPath.exists(path):
            return None
        for vhost in listdir(path):
            fd = open(path+vhost, 'r')
            self.__open_vhost_from_url(path+vhost, url, fd)
            fd.close()
        return self.__dummys

    def get_vhost_from_log_file(self, logpath, path=default_dir):
        # utiliser le nom du fichier pour recuperer la vhost
        # necessaire pour get le LogFormat
        logpath = SysPath.abspath(logpath)

        for vhost in listdir(path):
            fd = open(path+vhost, 'r')
            tmp = self.__open_vhost_from_logfile(path+vhost, logpath, fd)
            fd.close()
            if tmp is not None:
                return tmp
        return None

    def get_LogFormat_from_vhost(self):
        # si un log format est defini.
        # on fait une 1ere passe, ex: ${APACHE_LOG_DIR} devient -->
        # /var/log/apache2
        pass

    def get_LogFormat_from_apache_conf(self, logformat_style):

        fd = open('%sapache2.conf' % HTTPD_ROOT, 'r')

        for line in fd:
            if line.startswith('#') is True or len(line) < 1:
                continue
            tmp_line = line.split(' ')[len(line.split(' ')) - 1]
            tmp_line = tmp_line.replace('\n', '')
            if tmp_line in logformat_style:
                if len(tmp_line) == len(logformat_style):
                    # print logformat_style + ' ' + tmp_line
                    # CHECK RINDEX STRING
                    first_index = line.find('"') + 1
                    last_index = line.rfind('"')
                    logformats = line[first_index:last_index]
                    # print logformats
                    return logformats

    def find_logID_from_log_path(self, logpath):

        parent_directory, filename = SysPath.split(logpath)
        file_list = []
        if not SysPath.exists(parent_directory):
            print "\n     TMP ERROR: PATH LOG UNKNOWN"
            return (None, None)
        for logfile in listdir(parent_directory):
            if filename in logfile and logfile.startswith(filename):
                file_list.append(logfile)
        # for item in sorted(file_list):
        #    print item
        if file_list:
            return (parent_directory, sorted(file_list))
        else:
            return (None, None)
