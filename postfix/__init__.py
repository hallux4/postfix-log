#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Container.OrderedDict2 as OrderedDict2
import PersonalTools.CommonTools as CommonTools
import sys
import PersonalTools.Colors as Colors
import operator
import re
import os
import datetime
from functools import partial
import elementShell
import elementFile
import getopt

# sys.stderr = open('toto.txt', 'w')


def check_param():

    LongOpts = None
    LongOpts = optionsDict.keys()

    try:
        opts, args = getopt.getopt(sys.argv[3:], '', LongOpts)
    except getopt.GetoptError, err:
        exit(Colors.change_color('\n     %s' % err, 'FAIL'))
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


def check_first_and_last_line_postfix():
    global anal
    global filetool

    filetool.check_first_and_last_line()

    anal.Set_Date_START_FILE(filetool.get_fd().readline())
    anal.Set_Date_END_FILE(filetool.get_fd().readlines()[-1])

    tmpSTART = "     Debut du fichier: %s" % anal.Get_Date_START_FILE()
    print Colors.change_color(tmpSTART, 'OKGREEN')
    tmpEND = "     Fin du fichier: %s" % anal.Get_Date_END_FILE()
    print Colors.change_color(tmpEND, 'OKGREEN')

    filetool.get_fd().seek(0)


# variable en input, fournies par l'utilisateur
# python -m memory_profiler check_mail.py 'param_type=postfix' ...>
# ...> 'param_path=/var/log/mail.log' 'param_command=6' mfast


def init_normal_mode():
    global uranus
    global anal

    while uranus.Set_From(
            raw_input(
                Colors.change_color(
                    '     Adresse Emettrice: ', 'HEADER'))) is not True:
        continue
    while uranus.Set_To(
            raw_input(
                Colors.change_color(
                    '     Adresse Destinataire: ', 'HEADER'))) is not True:
        continue
    while uranus.Set_Status(
            raw_input(
                Colors.change_color(
                    '     Statut: ', 'HEADER'))) is not True:
        continue
    while uranus.Set_Full_Date_Start(
            raw_input(
                Colors.change_color(
                    '     Date Debut: ', 'HEADER'))) is not True:
        continue
    while uranus.Set_Full_Date_End(
            raw_input(
                Colors.change_color(
                    '     Date Fin: ', 'HEADER'))) is not True:
        continue
    if (uranus.Get_Full_Date_Start() is None and
            uranus.Get_Full_Date_End() is not None):
        uranus.Full_Date_Start = anal.Get_Date_START_FILE()
    if (uranus.Get_Full_Date_Start() is not None and
            uranus.Get_Full_Date_End() is None):
        uranus.Full_Date_End = anal.Get_Date_END_FILE()
    if (uranus.Get_Full_Date_Start() is not None and
            uranus.Get_Full_Date_End() is not None):
        print Colors.change_color(
                '     Fourchette de temps choisie: ', 'HEADER')
        tmp1 = str(uranus.Get_Full_Date_Start())
        print Colors.change_color(
                '                          début: ', 'HEADER') + tmp1
        tmp1 = str(uranus.Get_Full_Date_End())
        print Colors.change_color(
                '                          fin  : ', 'HEADER') + tmp1
    while uranus.Set_Id(
            raw_input(
                Colors.change_color(
                    '     ID: ', 'HEADER'))) is not True:
        continue
    tmp1 = "     Filters (liste de filtre, exemple: "
    tmp1 = tmp1 + "blacklist google refused): "
    while uranus.Set_Filters(
            raw_input(Colors.change_color(tmp1, 'HEADER'))) is not True:
        continue


def init_mfast_mode():
    global optionsDict
    global anal
    global uranus

    if optionsDict['start='] is not None:
        uranus.Set_Full_Date_Start(optionsDict['start='])
    if optionsDict['end='] is not None:
        uranus.Set_Full_Date_End(optionsDict['end='])
    if optionsDict['status='] is not None:
        uranus.Set_Status(optionsDict['status='])
    if optionsDict['from='] is not None:
        uranus.Set_From(optionsDict['from='])
    if optionsDict['to='] is not None:
        uranus.Set_To(optionsDict['to='])
    if optionsDict['id='] is not None:
        uranus.Set_Id(optionsDict['id='])
    if optionsDict['filters='] is not None:
        uranus.Set_Filters(' '.join(optionsDict['filters='].split(',')))

    if optionsDict['start='] is None and optionsDict['end='] is not None:
        uranus.Full_Date_Start = anal.Get_Date_START_FILE()
    elif optionsDict['end='] is None and optionsDict['start='] is not None:
        uranus.Full_Date_End = anal.Get_Date_END_FILE()


def init_arguments_for_multi():
    global optionsDict
    global uranus

    if uranus.Get_Full_Date_Start() is not None:
        optionsDict['start='] = str(uranus.Get_Full_Date_Start())
    if uranus.Get_Full_Date_End() is not None:
        optionsDict['end='] = str(uranus.Get_Full_Date_End())
    if uranus.Get_Status() is not None:
        optionsDict['status='] = str(uranus.Get_Status())
    if uranus.Get_From() is not None:
        optionsDict['from='] = str(uranus.Get_From())
    if uranus.Get_To() is not None:
        optionsDict['to='] = str(uranus.Get_To())
    if uranus.Get_Id() is not None:
        optionsDict['id='] = str(uranus.Get_Id())
    if uranus.Get_Filters() is not None:
        optionsDict['filters='] = str(','.join(uranus.Get_Filters()))


def optionnal_param_file():

    global anal    # input
    global uranus  # output
    global filetool
    global optionsDict

    list_dict = OrderedDict2.OrderedDict()
    blacklist_dict = OrderedDict2.OrderedDict()

    # 1) check si les elements de la ligne correspondent au elements en input
    # 2) si la ligne est valide, chercher l'ID dans list_dict.
    # 3) Si l'id n'est pas la, ajouter une entree. list_dict[ID] = valid_list()
    # 4) Si l'id est present, Set.From() ou add_To() sur l'element concerne.

    if (optionsDict['mfast'] == 1):
        init_mfast_mode()
    else:
        init_normal_mode()
    init_arguments_for_multi()

    nb_line = 0
    i = 0

    old = datetime.datetime.now()
    for line in filetool.get_fd():
        if i == 1000:
            filetool.cli_progress_test(nb_line)
            i = 0
        nb_line = nb_line + 1
        i = i + 1

        if ('from=<' not in line and 'to=<' not in line):
            continue

        anal.clean()
        anal.Line_func(line)

        # SCOPE CHECK BETWEEN ELEMENTIN AND ELEMENTOUT
        if (uranus.Get_Full_Date_Start() is not None and
                anal.Get_Date() < uranus.Get_Full_Date_Start()):
            continue
        if (uranus.Get_Full_Date_Start() is not None and
                anal.Get_Date() > uranus.Get_Full_Date_End()):
            continue
        if (uranus.Get_Id() is not None and
                uranus.Get_Id() not in anal.Get_Id()):
            continue
        if (anal.Get_To() is not None and
                (uranus.Get_Status() is not None and
                    uranus.Get_Status() not in str(anal.Get_Status()))):
            continue
        if anal.Get_To() is not None:
            if (uranus.Get_Filters()):
                check = False
                for elem in uranus.Get_Filters():
                    if (elem in str(anal.Get_Desc())):
                        check = True
                        break
                if check is not True:
                    continue

        if uranus.Get_From() is not None and uranus.Get_To() is not None:
            if anal.Get_From() is not None:
                if uranus.Get_From() not in anal.Get_From():
                    if anal.Get_Id() not in list_dict:
                        blacklist_dict[anal.Get_Id()] = True
                    continue
            elif anal.Get_To() is not None:
                if uranus.Get_To() not in anal.Get_To():
                    continue
                else:
                    if (anal.Get_Id() not in list_dict and
                            anal.Get_Id() not in blacklist_dict):
                        list_dict[anal.Get_Id()] = elementFile.valid_list()
                    else:
                        continue

        elif uranus.Get_From() is not None and anal.Get_To() is None:
            if uranus.Get_From() not in str(anal.Get_From()):
                continue
            else:
                if anal.Get_Id() not in list_dict:
                    list_dict[anal.Get_Id()] = elementFile.valid_list()
        elif uranus.Get_To() is not None and anal.Get_From() is None:
            if uranus.Get_To() not in str(anal.Get_To()):
                continue
            else:
                if anal.Get_Id() not in list_dict:
                    list_dict[anal.Get_Id()] = elementFile.valid_list()

        elif uranus.Get_From() is None and uranus.Get_To() is None:
            if anal.Get_To() is not None:
                if anal.Get_Id() not in list_dict:
                    list_dict[anal.Get_Id()] = elementFile.valid_list()

        # SCOPE THAT ADD THE VALID ELEMENTS IN THE LIST ##

        if anal.Get_Id() in list_dict:
            if (anal.Get_To() is not None):
                if anal.Prepare_To_Valid() is not None:
                    list_dict[anal.Get_Id()].add_To(anal.Prepare_To_Valid())

    filetool.get_fd().seek(0)

    print ''
    nb_line = 0
    i = 0
    for line in filetool.get_fd():
        if i == 1000:
            filetool.cli_progress_test(nb_line)
            i = 0
        nb_line = nb_line + 1
        i = i + 1

        if ('from=<' in line):
            anal.clean()
            anal.Line_func(line)

            if anal.Get_Id() in list_dict and anal.Get_From() is not None:
                if (anal.Prepare_From_Valid() is not None and
                        list_dict[anal.Get_Id()].From is None):
                    tmp1 = anal.Prepare_From_Valid()
                    list_dict[anal.Get_Id()].set_From(tmp1)

    print ''
    new = datetime.datetime.now()

    # SCOPE THAT DISPLAY THE INFORMATION STORED IN THE LIST

    tmp_pop_list = []
    for key, value in list_dict.iteritems():
        if value.From is not None:
            if len(value.To) > 0:
                print '_________________________________\n'
                print value.From.Get_output()
            else:
                tmp_pop_list.append(key)
        if value.From is not None and value.To is not None:
            for elem in value.To:
                if (elem is not None):
                    print '    ' + elem.Get_output()
    print '     ' + Colors.change_color(
                        '\n     Temps passe total= ', 'FAIL') + str(new - old)

    if tmp_pop_list:
        for item in tmp_pop_list:
            list_dict.popitem(item)

    print 'La taille de la liste est : ' + str(len(list_dict))

    list_dict.clear()
    uranus = elementShell.elementShell()
    go_trhough_multi()


def GetStatsFromString():

    global filetool

    db_stats_list = {}
    idListTo = {}
    idListFrom = {}

    old = datetime.datetime.now()

    i = 0
    nb_line = 0
    for line in filetool.get_fd():
        if i == 1000:
            filetool.cli_progress_test(nb_line)
            i = 0
        nb_line = nb_line + 1
        i = i + 1
        if 'uid=' not in line:
            if ('from=<' in line):
                Id = re.sub("\s\s+", " ", line).split(' ')[5].split(':')[0]
                if Id in idListFrom:
                    continue
                else:
                    idListFrom[Id] = True
                tmp_mail = line[line.find("from=<") + 6:line.find(">")]
                tmp1 = Colors.change_color('from=<', 'OKGREEN') + tmp_mail
                if (tmp1 not in db_stats_list):
                    tmp1 = Colors.change_color('from=<', 'OKGREEN') + tmp_mail
                    db_stats_list[tmp1] = 1
                else:
                    tmp1 = Colors.change_color('from=<', 'OKGREEN') + tmp_mail
                    db_stats_list[tmp1] = db_stats_list[tmp1] + 1
            if ('to=<' in line):
                Id = re.sub("\s\s+", " ", line).split(' ')[5].split(':')[0]
                if Id in idListTo:
                    continue
                else:
                    idListTo[Id] = True
                tmp_mail = line[line.find("to=<") + 4:line.find(">")]
                tmp1 = Colors.change_color('to=<', 'WARNING') + tmp_mail
                if (tmp1 not in db_stats_list):
                    db_stats_list[tmp1] = 1
                else:
                    db_stats_list[tmp1] = db_stats_list[tmp1] + 1

    new = datetime.datetime.now()
    print ''
    print '     ' + Colors.change_color(
                            'Temps passe total= ', 'FAIL') + str(new - old)

    sorted_x = sorted(db_stats_list.items(), key=operator.itemgetter(1))
    for key, value in sorted_x:
        print '     ' + key + '> ' + Colors.change_color(str(value), 'FAIL')

    new = datetime.datetime.now()
    db_stats_list.clear()
    print '     ' + Colors.change_color(
                            'Temps passe total= ', 'FAIL') + str(new - old)
    go_trhough_multi()


def go_trhough_multi():
    command_line = create_subprocess_arguments()

    print Colors.change_color(
        '\n     Commande rapide sans shell:::', 'HEADER')
    exit('\n     %s' % Colors.change_color(command_line, 'OKGREEN'))
    # subprocess.call(["/root/main.sh", command_line])
    # print Colors('--- Fin du traitement multiple ---','OKGREEN')


def create_subprocess_arguments():
    cmd = None
    if "./" not in sys.argv[0]:
        cmd = 'python %s' % sys.argv[0]
    else:
        cmd = sys.argv[0]
    path = '%s ' % str(os.path.abspath(sys.argv[2]))
    cmd = '  '.join([cmd, sys.argv[1], path])
    for key, value in optionsDict.iteritems():
        if value is not None and key not in 'mfast':
            cmd = cmd + ("--" + key + "'" + str(value) + "'" + ' ')
    return cmd + ' --mfast'


def postfix_shell():

    global filetool
    global optionsDict

    if optionsDict['mfast'] == 0:
        print Colors.change_color(
            commandDial(), 'HEADER')
        optionsDict['command='] = filetool.question_safe('     ')
        while optionsDict['command='] not in function:
            print Colors.change_color("     je n ai pas compris", 'FAIL')
            print Colors.change_color(commandDial(), 'HEADER')
            optionsDict['command='] = filetool.question_safe('     ')
        tmp1 = "     Vous avez choisi la commande : "
        print Colors.change_color(tmp1+optionsDict['command='], 'OKGREEN')
    if (optionsDict['command='] is not None):
        function[optionsDict['command=']]()
        filetool.get_fd().seek(0)


def get_shell():

    global filetool

    filetool = CommonTools.check_file()
    if (filetool.checkfile_shell(sys.argv[2]) is False):
        Message = "Le module Postfix prend un fichier en paramètre"
        exit('\n     %s' % Colors.change_color(Message, 'FAIL'))

    check_first_and_last_line_postfix()
    check_param()

    try:
        postfix_shell()
    except KeyboardInterrupt:
        Message = '\n     KeyboardInterrupt'
        exit(Colors.change_color(Message, 'FAIL'))

anal = elementFile.elementFile()
uranus = elementShell.elementShell()
filetool = None

function = {
        '1': partial(GetStatsFromString),
        '2': partial(optionnal_param_file)
        }

optionsDict = {
    'start=': None,
    'end=': None,
    'command=': None,
    'status=': None,
    'from=': None,
    'to=': None,
    'id=': None,
    'filters=': None,
    'mfast': 0
}


def commandDial():

    return """
    Quelle commande souhaitez-vous utiliser ?
    1 : Liste
        Procure une liste des adresses mail classée par ordre d'occurrence
    2 : Recherche Custom
        Recherche avec Filtres Optionnels
    """
