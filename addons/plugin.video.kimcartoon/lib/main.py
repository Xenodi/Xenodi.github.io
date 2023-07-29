# -*- coding: utf-8 -*-
import requests
import six

import sys

from six.moves import urllib_parse
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import xbmc, xbmcaddon, xbmcgui, xbmcplugin

ADDON = xbmcaddon.Addon()

ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_ICON = ADDON.getAddonInfo("icon")

USERNAME = ADDON.getSetting("username")
PASSWORD = ADDON.getSetting("password")
BASE_URL = ADDON.getSetting("baseUrl")

session = requests.session()

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def xbmcDebug(message):
    xbmc.log(f"{ADDON_NAME} > {message}", xbmc.LOGWARNING)

def BuildURL(query):
    return sys.argv[0] + "?" + urllib_parse.urlencode({
        k: v.encode("utf-8") if isinstance(v, six.text_type) else str(v).encode("utf-8")
        for k, v in query.items()
    })

class Listing:
    def __init__(self):
        self.listItems = []
    
    def addItem(self, label, thumbnailImage, action, path, color="yellow"):
        list_item = xbmcgui.ListItem(f"[COLOR {color}]{label}[/COLOR]", label2=label)
        list_item.setArt(thumbnailImage)

        self.listItems.append((BuildURL({ "action": action, "path": path }), list_item, True))

    def show(self, handle=int(sys.argv[1])):
        xbmcplugin.addDirectoryItems(
            handle,
            tuple(self.listItems)
        )

        xbmcplugin.endOfDirectory(handle)

def Login():
    session.get(f"{BASE_URL}/Mobile/SwitchToDesktop")

    if USERNAME != "":
        session.post(f"{BASE_URL}/Login", data={"username": USERNAME, "password": PASSWORD})

def ActionMainMenu(params):
    listing = Listing()

    listing.addItem("Latest", ADDON_ICON, "ActionLatest", None)
    listing.addItem("Search", ADDON_ICON, "ActionSearch", None, "orange")

    listing.show()

def ActionLatest(params):
    Login()

    listing = Listing()

    container = BeautifulSoup(session.get("https://kimcartoon.li").text, features="html.parser").find(id="container")
    items = container.find("div", {"class": "items" }).find_all("a")
    for item in items:
        xbmcDebug(item.find("img"))
        listing.addItem(
            item.find("div", {"class": "item-title"}).contents[0],
            BASE_URL + item.find("img")["src" if "src" in item.find("img").attrs else "srctemp"],
            "ActionMainMenu",
            item["href"]
        )

    listing.show()

def ActionSearch(params):
    pass

def main():
    params = dict(urllib_parse.parse_qsl(sys.argv[2][1:], keep_blank_values=True))
    globals()[params.get("action", "ActionMainMenu")](params)