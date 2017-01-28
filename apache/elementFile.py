#!/usr/bin/env python
# coding=utf-8


class apache_line(object):

    status = None
    request_url = None
    request_header_user_agent = None
    request_method = None
    time_received_datetimeobj = None
    remote_host = None

    def __init__(self):
        print 'Init Apache Line'

    def clean(self):
        self.status = None
        self.request_url = None
        self.request_header_user_agent = None
        self.request_method = None
        self.time_received_datetimeobj = None
        self.remote_host = None

    def set_status(self, input):
        self.status = input

    def get_status(self):
        return self.status

    def set_request_url(self, input):
        self.request_url = input

    def get_request_url(self):
        return self.request_url

    def set_request_header_user_agent(self, input):
        self.request_header_user_agent = input

    def get_request_header_user_agent(self):
        return self.request_header_user_agent

    def set_request_method(self, input):
        self.request_method = input

    def get_request_method(self):
        return self.request_method

    def set_time_received_datetimeobj(self, input):
        tmp = str(input).split(' ')[0]
        self.time_received_datetimeobj = tmp+"]"

    def get_time_received_datetimeobj(self):
        return self.time_received_datetimeobj

    def set_remote_host(self, input):
        self.remote_host = input

    def get_remote_host(self):
        return self.remote_host

    def get_string(self):
        #return self.status + self.request_url + self.request_header_user_agent + self.request_method + self.time_received_datetimeobj + self.remote_host
        return "%s %s %s %s %s" % (self.time_received_datetimeobj, self.remote_host, self.request_method, self.status, self.request_url)
