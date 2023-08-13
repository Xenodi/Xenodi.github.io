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

def XbmcDebug(message):
    xbmc.log(f"{ADDON_NAME} > {message}", xbmc.LOGWARNING)

def BuildURL(query):
    return sys.argv[0] + "?" + urllib_parse.urlencode({
        k: v.encode("utf-8") if isinstance(v, six.text_type) else str(v).encode("utf-8")
        for k, v in query.items()
    })

class Listing:
    def __init__(self):
        self.listItems = []
    
    def addItem(self, label, image=ADDON_ICON, data={}, color="yellow", infoType=None, infoLabels=None, isFolder=True, **properties):
        list_item = xbmcgui.ListItem(f"[COLOR {color}]{label}[/COLOR]", label2=label)
        list_item.setArt({ "thumb": image })
        
        if infoType and infoLabels:
            list_item.setInfo(infoType, infoLabels)
        
        for item in properties.items():
            list_item.setProperty(item[0], item[1])

        vinfo = list_item.getVideoInfoTag()
        vinfo.setTitle(label)
        vinfo.setMediaType("video")

        self.listItems.append((BuildURL(data), list_item, isFolder))

    def show(self, handle=int(sys.argv[1])):
        xbmcplugin.addDirectoryItems(
            handle,
            tuple(self.listItems)
        )

        xbmcplugin.endOfDirectory(handle)

def PlayVideo(url, handle=int(sys.argv[1])):
    play_item = xbmcgui.ListItem(offscreen=True)
    play_item.setPath(url)
    xbmcplugin.setResolvedUrl(handle, succeeded=True, listitem=play_item)

def Main(globals, defaultAction="ActionMainMenu"):
    params = dict(urllib_parse.parse_qsl(sys.argv[2][1:], keep_blank_values=True))
    globals[params.get("action", defaultAction)](params)