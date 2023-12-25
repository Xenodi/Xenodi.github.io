from lib import Xenodi
import random

def ActionMainMenu(params):
    Xenodi.Debug(params)

    video_ids = [
        "L_LUpnjgPso",
        "g6Ye4xwXyAw",
        "HF6LSbMKvrw",
        "RrPP6NaF4gk"
    ]

    Xenodi.Execute("RunPlugin(plugin://plugin.video.youtube/play/?video_id=" + random.choice(video_ids) + "&incognito=true)")

if __name__ == "__main__":
    Xenodi.Main(globals())