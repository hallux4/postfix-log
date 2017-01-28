#!/usr/bin/env python
# -*- coding: utf-8 -*-

from functools import partial
from custom_apache_tool.apache_tools import apache_tools
import Container.OrderedDict2 as OrderedDict
import PersonalTools.CommonTools as CommonTools
import PersonalTools.Colors as Colors
import getopt
import elementFile
# import operator
from apache import apache_log_parser
import os
# import datetime
from sys import argv, exit
# from pprint import pprint


def check_param():

    LongOpts = None
    LongOpts = optionsDict.keys()

    try:
        opts, args = getopt.getopt(argv[3:], '', LongOpts)
    except getopt.GetoptError, err:
        exit(err)
    for option in opts:
        for key in optionsDict.iterkeys():
            if key[:-1] in option[0][1:]:
                optionsDict[key] = option[1]
        if 'mfast' in option[0]:
            optionsDict['mfast'] = 1
    if optionsDict['command='] is not None and optionsDict['command='] in '1':
        for key in optionsDict.iterkeys():
            if key in 'command=':
                pass
            else:
                optionsDict[key] = None


def check_first_and_last_line_apache():
    global anal
    global filetool

    filetool.check_first_and_last_line()

    filetool.get_fd().seek(0)


def GetStatsFromString():
    print '     GetStatsFromString'


def optionnal_param_file():
    print '     optionnal_param_file'


def go_trhough_multi():
    global param_multi

    command_line = create_subprocess_arguments()

    print Colors.change_color(
        '\n     Commande rapide sans shell:::', 'HEADER')
    # subprocess.call(["/root/main.sh", command_line])
    # print Colors('--- Fin du traitement multiple ---','OKGREEN')
    exit(Colors.change_color(command_line, 'OKGREEN'))


def create_subprocess_arguments():
    cmd = None
    if "./" not in argv[0]:
        cmd = 'python %s' % argv[0]
    else:
        cmd = argv[0]
    path = '%s ' % str(os.path.abspath(argv[2]))
    cmd = '  '.join([cmd, argv[1], path])
    for key, value in optionsDict.iteritems():
        if value is not None and key not in 'mfast':
            cmd = cmd + ("--" + key + "'" + str(value) + "'" + ' ')
    return cmd + ' --mfast'


def apache_shell():

    global filetool
    global optionsDict

    if optionsDict['mfast'] == 0:
        print Colors.change_color(
            commandDial(), 'HEADER')
        optionsDict['command='] = filetool.question_safe('     ')
        while optionsDict['command='] not in function:
            print Colors.change_color("     je n ai pas compris", 'FAIL')
            print Colors.change_color(
                commandDial(), 'HEADER')
            optionsDict['command='] = filetool.question_safe('     ')

        tmp1 = "     Vous avez choisi la commande : "
        print Colors.change_color(tmp1+optionsDict['command='], 'OKGREEN')
    if (optionsDict['command='] is not None):
        function[optionsDict['command=']]()
        filetool.get_fd().seek(0)


def find_vhost_from_url(url):
    vhost_list = apache_tool.get_log_file_from_vhost(argv[2])

    if vhost_list is None:
        tmp = "\n     Le dossier /etc/apache2 n'existe pas."
        tmp = Colors.change_color(tmp, 'FAIL')
        exit(tmp)
    i = 0
    list_tmp = []
    for key in vhost_list:
        keytmp = key[0].split(':')[0]
        tmp = "\n     %s %s" % (keytmp, key[1].VHStart)
        list_tmp.append(tmp)
        if key[1].Name:
            tmp = "\n           ServerName:: %s" % key[1].Name
            list_tmp.append(Colors.change_color(tmp, 'FAIL'))
        if key[1].Alias:
            tmp = ("\n           ServerAlias:: %s" % key[1].Alias)
            list_tmp.append(Colors.change_color(tmp, 'OKGREEN'))
        tmp = "\n           CustomLog:: %s" % key[1].CustomLog
        list_tmp.append(tmp)
        vhost_choice_dic[str(i)] = ' '.join(list_tmp)
        list_tmp = []
        i = i + 1

    len_choice_dic = len(vhost_choice_dic)
    choice = None
    if len_choice_dic > 1:
        for elem in vhost_choice_dic:
                choice_key = Colors.change_color(str(elem), 'HEADER')
                print '\n     ' + choice_key + ' ' + vhost_choice_dic[elem]
        while choice not in vhost_choice_dic:
            question = "\n     Quelle Vhost souhaitez vous consulter ?"
            print Colors.change_color(question, 'HEADER')
            choice = filetool.question_safe('     ')
            if (choice not in vhost_choice_dic):
                tmp = "     Ce choix n'existe pas."
                print Colors.change_color(tmp, 'FAIL')
            else:
                tmp_choice = vhost_choice_dic[choice]
                tmp_pattern = 'CustomLog:: '
                tmp_index = tmp_choice.find(tmp_pattern)
                tmp_index = tmp_index + len(tmp_pattern)
                optionsDict['logformat'] = tmp_choice[tmp_index:]
    elif len_choice_dic > 0:
        tmp_choice = vhost_choice_dic['0']
        tmp_pattern = 'CustomLog:: '
        tmp_index = tmp_choice.find(tmp_pattern)
        tmp_index = tmp_index + len(tmp_pattern)
        optionsDict['logformat'] = tmp_choice[tmp_index:]
    else:
        tmp = "\n     Aucune Vhost ne correspond à votre url"
        exit(Colors.change_color(tmp, 'FAIL'))


def find_vhost_from_log_name(url):
    optionsDict['logformat'] = apache_tool.get_vhost_from_log_file(argv[2])
    # exit('EXIT TMP')


def find_logformat():
    tmp = optionsDict['logformat'].split(':')[1]
    tmp = apache_tool.get_LogFormat_from_apache_conf(tmp)
    optionsDict['apache_regex'] = tmp.replace('\\', '')


def try_parse():

    # logfile_path = optionsDict['logformat'].split(':')[0]
    global optionsDict
    global apache_cunt

    logfile_path = optionsDict['log=']

    print '\n     %s\n' % logfile_path

    if filetool.checkfile_shell(logfile_path) is False:
        exit()
    else:
        check_first_and_last_line_apache()
        tmp = optionsDict['apache_regex']
        line_parser = apache_log_parser.make_parser(tmp)

        #apache_cunt = apache_line()

        for line in filetool.get_fd():
            line = line.rstrip()

            log_line_data = line_parser(line)

            print ''
            # pprint(log_line_data)
            for key in log_line_data.iterkeys():
                if key in "remote_host":
                    apache_cunt.set_remote_host(log_line_data[key])
                if key in "status":
                    apache_cunt.set_status(log_line_data[key])
                if key in "request_url":
                    apache_cunt.set_request_url(log_line_data[key])
                if key in "time_received_datetimeobj":
                    apache_cunt.set_time_received_datetimeobj(log_line_data[key])
                if key in "request_method":
                    apache_cunt.set_request_method(log_line_data[key])
                if key in "request_header_user_agent":
                    apache_cunt.set_request_header_user_agent(log_line_data[key])

                #tmp_key = Colors.change_color(key, 'OKGREEN')
                #print "%s %s" % (tmp_key, log_line_data[key])

            print apache_cunt.get_string()

def make_log_choice():

    global optionsDict

    tmp = optionsDict['logformat'].split(':')[0]
    logpath, log_file_list = apache_tool.find_logID_from_log_path(tmp)

    if not log_file_list:
        tmp = "\n     Aucun fichier de log n'a été trouvés."
        tmp = Colors.change_color(tmp, 'FAIL')
        exit(tmp)

    i = 0
    for item in log_file_list:
        log_choice_dic[str(i)] = item
        i = i + 1

    len_choice_dic = len(log_choice_dic)
    choice = None
    if len_choice_dic > 1:
        for elem in log_choice_dic.iterkeys():
                choice_key = Colors.change_color(elem, 'HEADER')
                print '\n     ' + choice_key + ' ' + log_choice_dic[elem]
        while choice not in log_choice_dic:
            question = "\n     Quel Log souhaitez vous consulter ?"
            print Colors.change_color(question, 'HEADER')
            choice = filetool.question_safe('     ')
            if (choice not in log_choice_dic):
                tmp = "     Ce choix n'existe pas."
                print Colors.change_color(tmp, 'FAIL')
            else:
                log_path = '/'.join([logpath, log_choice_dic[choice]])
                optionsDict['log='] = log_path
    elif len_choice_dic == 1:
        choice = '0'
        optionsDict['log='] = '/'.join([logpath, log_choice_dic[choice]])

    else:
        print 'no ...'


def get_shell():

    global filetool

    filetool = CommonTools.check_file()

    # apache_tool.get_log_directory_from_env()

    if (filetool.checkfile_shell(argv[2]) is False):
        find_vhost_from_url(argv[2])
    else:
        find_vhost_from_log_name(argv[2])

    find_logformat()
    make_log_choice()

    # try_parse()

    # check_first_and_last_line_apache()
    # check_param()

    try:
        apache_shell()
    except KeyboardInterrupt:
        exit('Keyboard Interrupt')

filetool = None
apache_tool = apache_tools()
apache_cunt = elementFile.apache_line()

function = {
        '1': partial(try_parse),
        '2': partial(optionnal_param_file)
        }

optionsDict = {
    'start=': None,
    'end=': None,
    'logformat=': None,
    'log=': None,
    'apache_regex=': None,
    'mfast': 0
}

vhost_choice_dic = OrderedDict.OrderedDict()
log_choice_dic = OrderedDict.OrderedDict()


def commandDial():
    return """
    Quelle commande souhaitez-vous utiliser ?
    1 : try_parse
        fonction de test qui affiche chaque ligne sous forme de tableau.
    2 : Recherche Custom
        Recherche avec Filtres Optionnels
    """

# Procure une liste des adresses IP classée par ordre d'occurrence
