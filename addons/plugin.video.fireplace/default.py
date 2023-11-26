from lib import Xenodi

def ActionMainMenu(params):
    Xenodi.Debug(params)

    Xenodi.Execute("RunPlugin(plugin://plugin.video.youtube/play/?video_id=L_LUpnjgPso)")

if __name__ == "__main__":
    Xenodi.Main(globals())