# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from lib import utils

import xbmcgui

USERNAME = utils.ADDON.getSetting("username")
PASSWORD = utils.ADDON.getSetting("password")
BASE_URL = utils.ADDON.getSetting("baseUrl")

def ActionMainMenu(params):
    listing = utils.Listing()

    resp = utils.session.get(BASE_URL).text
    soup = BeautifulSoup(resp, features="html.parser").find(id="main")

    contentBox = soup.find(id="mv-latest")

    items = contentBox.find_all("div", {"class": "ml-item"})
    for item in items:
        listing.addItem(
            item.find("span", {"class": "mli-info"}).text.strip(),
            item.find("img", {"class": "thumb"})["src"],
            { "action": "ActionWatchEpisode", "path": item.find("a", {"class": "ml-mask"})["href"] },
            isFolder=False,
            IsPlayable="true"
        )

    listing.show()

def ActionWatchEpisode(params):
    resp = utils.session.get(params["path"]).text
    soup = BeautifulSoup(resp, features="html.parser").find(id="main")

    listEpisodes = soup.find("div", {"class": "list-episodes"})
    episodeId = listEpisodes.find("option", {"selected": "selected"})["episodeid"]

    resp2 = utils.session.get(f"{BASE_URL}/ajax-get-link-stream/?server=youtu&filmId={episodeId}").text
    resp3 = utils.session.post("https://" + resp2.split("/")[2] + "/player/index.php?data=" + resp2.split("/")[-1] + "&do=getVideo", data={ "hash": resp2.split("/")[-1] }, headers={ "X-Requested-With": "XMLHttpRequest" }).json()

    resp4 = utils.session.get(resp3["securedLink"]).text

    utils.PlayVideo(resp4.split("\n")[-1])

    # utils.PlayVideo(None)

if __name__ == "__main__":
    utils.Main(globals())