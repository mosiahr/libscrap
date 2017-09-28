#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import csv
import re
import sys
import urllib.request
from urllib.parse import urlparse
import requests
from requests.exceptions import MissingSchema
from bs4 import BeautifulSoup

from random import uniform
from time import sleep

BASE_URL = 'https://www.python.org/blogs'

# soup.prettify()


class HtmlPage:
    """
    Get HTML Page
    """
    def __init__(self, url=None, lib_get_html='requests', lib_bs='lxml'):
        """
        :param url: url
        :param lib_get_html: 'requests', 'urllib'
        :param lib_bs: "html.parser", "lxml", "lxml-xml", "xml", "html5lib"
        """
        self.url = url
        self.lib_get_html = lib_get_html
        self.lib_bs = lib_bs
        if self.url is not None:
            self.set_url(self.url)

    def set_url(self, url):
        self.url = url
        self.host, self.host_and_scheme = self.get_host(url)[0], self.get_host(url)[1]
        self.is_connected(write=True)

    def get_host(self, url):
        try:
            if url != None:
                parse = urlparse(url)
                host = parse.netloc
                host_and_scheme = '{}://{}'.format(parse.scheme, parse.netloc)
            else:
                host, host_and_scheme = None, None
        except:
            host, host_and_scheme = None, None
        return (host, host_and_scheme)

    def is_connected(self, write=False):
        try:
            ip = socket.gethostbyname(self.host)
            socket.create_connection((ip, 80), timeout=2)
            if write:
                print('Connecting to the server ! HOST: {} | IP: {}'.format(self.host, ip))
            return True
        except Exception as e:
            print(e)
        print('Not conected !')
        return False

    def get_html(self, url):
        if self.lib_get_html == 'requests':
            return requests.get(url).text
        if self.lib_get_html == 'urllib':
            return urllib.request.urlopen(url).read()

    def soup(self, url):
        """
        Returns the BeautifulSoup object
        Allows you to select the parser library.

        :return: BeautifulSoup object
        """
        try:
            if self.is_connected():
                html = self.get_html(url)
                soup = BeautifulSoup(html, self.lib_bs)
                return soup
        except MissingSchema as e:
            print(e)

    def save_row_fields(self, path, row_fields=()):
        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row_fields)

if __name__=='__main__':
    page = HtmlPage()
    page.set_url('https://marry.ua')
    print(page.url)
    # if page.is_connected(BASE_URL):
    #     print("Hey")

