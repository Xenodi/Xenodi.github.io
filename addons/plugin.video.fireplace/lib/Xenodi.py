# -*- coding: utf-8 -*-
import sys
import six

from six.moves import urllib_parse

import xbmc, xbmcgui, xbmcplugin, xbmcaddon

try:
    import requests

    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    
    session = requests.session()
except ImportError:
    session = None

ADDON = xbmcaddon.Addon()

ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ICON = ADDON.getAddonInfo("icon")

def Debug(message):
    xbmc.log(f"{ADDON_NAME} > {message}", xbmc.LOGWARNING)

def Execute(command):
    xbmc.executebuiltin(command)

def BuildURL(query):
    return sys.argv[0] + "?" + urllib_parse.urlencode({
        k: v.encode("utf-8") if isinstance(v, six.text_type) else str(v).encode("utf-8")
        for k, v in query.items()
    })

def Main(globals, defaultAction="ActionMainMenu"):
    params = dict(urllib_parse.parse_qsl(sys.argv[2][1:], keep_blank_values=True))
    globals[params.get("action", defaultAction)](params)