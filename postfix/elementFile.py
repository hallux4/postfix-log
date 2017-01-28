#!/usr/bin/env python
# coding=utf-8

import re
import datetime


class elementFile(object):

        From = None
        To = None
        Id = None
        Date = None
        Status = None
        Desc = None
        Line = None

        def __init__(self):
            self.tmpnow = datetime.datetime.now()
            self.year = int(str(self.tmpnow).split('-')[0])
            self.month = None
            self.day = None

        def clean(self):
            self.From = None
            self.To = None
            self.Id = None
            self.Date = None
            self.Status = None
            self.Desc = None
            self.Line = None

        def Prepare_From_Valid(self):
            if (self.Get_Date() is not None and
                    self.Get_From() is not None and
                    self.Get_Id() is not None):
                tmp = from_valid()
                tmp.Date = self.Get_Date()
                tmp.From = self.Get_From()
                tmp.ID = self.Get_Id()
                return tmp
            else:
                print """un element n'a pas pu etre traite sur cette ligne,
                         les elements 'NULL' ne sont pas encore gere par
                         le script"""
                return None

        def Prepare_To_Valid(self):
            if (self.Get_Date() is not None and
                    self.Get_To() is not None and
                    self.Get_Id() is not None and
                    self.Get_Status() is not None and
                    self.Get_Desc() is not None):
                tmp = to_valid()
                tmp.Date = self.Get_Date()
                tmp.ID = self.Get_Id()
                tmp.To = self.Get_To()
                tmp.Status = self.Get_Status()
                tmp.Desc = self.Get_Desc()
                return tmp
            else:
                print """un element n'a pas pu etre traite sur cette ligne,
                         les elements 'NULL' ne sont pas encore gere par
                         le script"""
                return None

        def Line_func(self, _Line):
            self.Line = _Line
            self.Set_From()
            self.Set_To()
            self.Set_Date()
            self.Set_Status()
            self.Set_Desc()
            self.Set_Id()

        def Set_From(self):
            if ("from=<" in self.Line):
                self.From = self.Line[self.Line.find("from=<"):
                                      self.Line.find(">") + 1]

        def Get_From(self):
            return self.From

        def Set_To(self):
            if ("to=<" in self.Line):
                self.To = self.Line[self.Line.find("to=<"):
                                    self.Line.find(">") + 1]

        def Get_To(self):
            return self.To

        def Set_Date_START_FILE(self, _Line_tmp):
            self.month = re.sub("\s\s+", " ", _Line_tmp).split(' ')[0]
            self.day = re.sub("\s\s+", " ", _Line_tmp).split(' ')[1]
            self.time = re.sub("\s\s+", " ", _Line_tmp).split(' ')[2]
            self.check_year()
            tmpyear = '%s %s %s %s' % (self.year,
                                       self.month,
                                       self.day,
                                       self.time)
            self.Date_START_FILE = datetime.datetime.strptime(
                tmpyear, '%Y %b %d %H:%M:%S')

        def Get_Date_START_FILE(self):
            return self.Date_START_FILE

        def Set_Date_END_FILE(self, _Line_tmp):
            self.month = re.sub("\s\s+", " ", _Line_tmp).split(' ')[0]
            self.day = re.sub("\s\s+", " ", _Line_tmp).split(' ')[1]
            self.time = re.sub("\s\s+", " ", _Line_tmp).split(' ')[2]
            self.check_year()
            tmpyear = '%s %s %s %s' % (self.year,
                                       self.month,
                                       self.day,
                                       self.time)
            self.Date_END_FILE = datetime.datetime.strptime(
                tmpyear, '%Y %b %d %H:%M:%S')

        def Get_Date_END_FILE(self):
            return self.Date_END_FILE

        def Set_Date(self):
            self.month = re.sub("\s\s+", " ", self.Line).split(' ')[0]
            self.day = re.sub("\s\s+", " ", self.Line).split(' ')[1]
            self.time = re.sub("\s\s+", " ", self.Line).split(' ')[2]
            self.check_year()
            tmpyear = '%s %s %s %s' % (self.year,
                                       self.month,
                                       self.day,
                                       self.time)

            if self.From is not None or self.To is not None:
                self.Date = datetime.datetime.strptime(
                    tmpyear, '%Y %b %d %H:%M:%S')
                return

        def Get_Date(self):
            return self.Date

        def Set_Status(self):
            if self.To is not None:
                lenstat = len('status=')
                lendef = len('deferred')
                tmpfind1 = self.Line.find('status=') + len('status=')
                tmpfind2 = lendef + self.Line.find('status=') + lenstat
                self.Status = self.Line[tmpfind1:tmpfind2].split(' ')[0]

        def Get_Status(self):
            return self.Status

        def Set_Desc(self):
            if self.Status is not None:
                lenstat = len('status=')
                tmp1 = self.Line.find('status=') + lenstat + len(self.Status)
                self.Desc = self.Line[tmp1:-1]

        def Get_Desc(self):
            return self.Desc

        def Set_Id(self):
            if self.From is not None or self.To is not None:
                tmp1 = "\s\s+"
                self.Id = re.sub(
                            tmp1, " ",
                            self.Line).split(' ')[5].split(':')[0]

        def check_year(self):
            tmp = '%s %s %s' % (self.year, self.month, self.day)
            tmpdate = datetime.datetime.strptime(tmp, '%Y %b %d')
            if tmpdate > self.tmpnow:
                self.year = self.year - 1
                # print tmpdate, tmpnow

        def Get_Id(self):
            return self.Id


class from_valid(object):
    Date = None
    ID = None
    From = None

    def Get_output(self):
        return str(self.Date) + ' ' + str(self.ID) + ' ' + str(self.From)


class to_valid(object):
    Date = None
    ID = None
    To = None
    Status = None
    Desc = None

    def Get_output(self):
        return str(self.Date) + ' ' + \
                str(self.ID) + ' ' + \
                str(self.To) + ' ' + \
                str(self.Status) + ' ' + \
                str(self.Desc)


class valid_list(object):
    From = None  # (type : from_valid)
    To = None  # (list type : to_valid)

    def __init__(self):
        self.To = []

    def set_From(self, _From):
        self.From = _From

    def add_To(self, _To):
        self.To.append(_To)
