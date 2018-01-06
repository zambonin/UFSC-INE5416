#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""tracking.py

A simple parser for Correios' tracking website, the brazilian postal system.
Valid tracking codes are thirteen characters long with some details [1].

[1] http://www.correios.com.br/para-voce/precisa-de-ajuda/como-rastrear-um-objeto
"""

from pprint import pprint
from re import findall, search, sub
from sys import argv

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen


def fetch_source(tracking_code):
    """Requests the raw tracking information through Correios' site."""
    url = "http://www.websro.com.br/detalhes.php?P_COD_UNI={}"
    return urlopen(url.format(tracking_code)).read().decode('utf-8')


def parse_info(tracking_code):
    """Transforms the raw page source so it is human-readable."""
    content = findall(r'<td.+?</td>', fetch_source(tracking_code))
    info = [sub(r'<[^>]*>', '', line) for line in content]
    ind = [info.index(line) for line in info if search(r'(\d+/\d+/\d+)', line)]

    return [info[ind[i]:ind[i + 1]] for i in range(len(ind) - 1)][::-1] \
            or "Invalid tracking number."


if __name__ == '__main__':
    try:
        pprint(parse_info(argv[1]))
    except IndexError:
        print("Invalid tracking number.")
