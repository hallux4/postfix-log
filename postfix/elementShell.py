#!/usr/bin/env python
# coding=utf-8

import re
import datetime


class elementShell(object):

        From = None
        To = None
        Id = None
        Full_Date_Start = None
        Full_Date_End = None
        Status = None
        Filters = None

        def __init__(self):
            self.list_limiter = [' ', '/', '-', '.', ',', ':', 'h', '\\', ';']
            self.Status_List = ['sent', 'deferred', 'bounced']

        def Set_From(self, _From):
            if _From in '':
                return True
            self.From = _From
            return True

        def Get_From(self):
            return self.From

        def Set_To(self, _To):
            if _To in '':
                return True
            self.To = _To
            return True

        def Get_To(self):
            return self.To

        def Set_Id(self, _Id):
            if _Id in '':
                return True
            self.Id = _Id
            return True

        def Get_Id(self):
            return self.Id

        def Set_Full_Date_Start(self, _Full_Date_Start):
            if _Full_Date_Start in '':
                return True
            for i in self.list_limiter:
                if i in _Full_Date_Start:
                    _Full_Date_Start = _Full_Date_Start.replace(i, " ")
                    _Full_Date_Start = re.sub(
                                            "\s\s+", " ",
                                            _Full_Date_Start.strip()
                                            )
            try:
                self.Full_Date_Start = datetime.datetime.strptime(
                                            _Full_Date_Start,
                                            '%Y %m %d %H %M %S'
                                            )
                return True
            except ValueError:
                print _Full_Date_Start + """
                                : Cette date semble incorrecte.
                                \nExemple: 2015 5 6 5 2 3
                                 donne 2015-05-06 05:02:03"""
                return False

        def Get_Full_Date_Start(self):
            return self.Full_Date_Start

        def Set_Full_Date_End(self, _Full_Date_End):
            if _Full_Date_End in '':
                return True
            for i in self.list_limiter:
                if i in _Full_Date_End:
                    _Full_Date_End = _Full_Date_End.replace(i, " ")
                    _Full_Date_End = re.sub(
                                            "\s\s+", " ",
                                            _Full_Date_End.strip()
                                            )

            try:
                self.Full_Date_End = datetime.datetime.strptime(
                                            _Full_Date_End,
                                            '%Y %m %d %H %M %S'
                                            )
                return True
            except ValueError:
                print _Full_Date_End + """
                                : Cette date semble incorrecte.
                                \nExemple: 2015 5 6 5 2 3
                                 donne 2015-05-06 05:02:03"""
                return False

        def Get_Full_Date_End(self):
            return self.Full_Date_End

        def Set_Status(self, _Status):
            if _Status in '':
                return True
            if (_Status in self.Status_List):
                self.Status = _Status
                return True
            else:
                print 'Le statut semble incorrect'
                print self.Status_List
                return False

        def Get_Status(self):
            return self.Status

        def Set_Filters(self, _Filters):
            if _Filters in '':
                return True
            if len(_Filters) > 0:
                _Filters = " ".join(_Filters.split())
                if _Filters not in ' ':
                    self.Filters = _Filters.split(' ')
                else:
                    print """Vous n'avez renseigne aucun filtre.
                                Pas besoin du mot clef filter="""
                    return False
                # for elem in self.Filters:
                #    print '     %s' % elem
            else:
                print """Vous n'avez renseigne aucun filtre.
                            Pas besoin du mot clef filter="""
                return False
            return True

        def Get_Filters(self):
            return self.Filters
