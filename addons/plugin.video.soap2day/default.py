# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

from lib import utils

from six.moves import urllib_parse

import xbmcgui

BASE_URL = utils.ADDON.getSetting("baseUrl")
IMG_BASE_URL = utils.ADDON.getSetting("imgBaseUrl")

def ActionMainMenu(params):
    searchQuery = utils.KeyboardInput("Search movie")
    if searchQuery == None:
        return
    
    listing = utils.Listing()

    soup = BeautifulSoup(utils.session.post(BASE_URL + "app/http/public/search", data={ "searchQuery": searchQuery, "typeFilter": "movie" }).json()["searchResult"], features="html.parser")
    items = soup.find_all("div", {"class": "col"})
    for item in items:
        path = item.find("a")["href"][1:]
        if path.startswith("movie/"):
            listing.addItem(
                "Movie: " + item.find("p", {"class": "title-video"}).text,
                item.find("img")["data-src"],
                { "action": "ActionWatchMovie", "path": path },
                isFolder=False,
                IsPlayable="true"
            )
        else:
            listing.addItem(
                "Series: "+ item.find("p", {"class": "title-video"}).text,
                item.find("img")["data-src"],
                { "action": "ActionWatchSeries", "path": path }
            )

    listing.show()

def ActionWatchMovie(params):
    soup = BeautifulSoup(utils.session.get("https://wwvv.ssoap2day.to/" + params["path"]).content, features="html.parser")
    video_id, player = soup.find("div", { "class": "click-play" })["onclick"].split("(")[1].split(")")[0].split(", ")
    player = player.replace("'", "")

    url = utils.session.get(
        f"https://wwvv.ssoap2day.to/app/http/public/retrieveMovieEmbed.php?movie_id={video_id}&server={player}"
    ).json()["embed"]
    
    soup2 = BeautifulSoup(utils.session.get(url).content, features="html.parser")

    source = utils.session.get("https://" + url.split("/")[2] + "/app/http/movie/getData.php?" + urllib_parse.urlencode(
        {
            "id": soup2.find(id="video-id")["value"],
            "id_type": soup2.find(id="video-type")["value"],
            "season": soup2.find(id="video-season")["value"],
            "episode": soup2.find(id="video-episode")["value"]
        }
    )).json()["source"]

    utils.PlayVideo(source)

def ActionWatchSeries(params):
    xbmcgui.Dialog().ok("ActionWatchSeries", params["path"])

def ActionListEpisodes(params):
    listing = utils.Listing()

    items = BeautifulSoup(utils.session.get(BASE_URL + "film/" + params["path"] + "/"), features="html.parser").find(id="eps-list").find_all("button")
    for item in items:
        listing.addItem(
            items["title"],
            params["image"],
            { "action": "ActionWatchEpisode", "path": "" },
            isFolder=False,
            IsPlayable="true"
        )
    
    listing.show()

if __name__ == "__main__":
    utils.Main(globals())