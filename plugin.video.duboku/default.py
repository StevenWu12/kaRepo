import sys
import urllib.request
import re
import xbmcplugin
import xbmcgui
import xbmcaddon
import urllib.parse

ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASE_URL = 'https://duboku.tv'

def build_url(query):
    return sys.argv[0] + '?' + urllib.parse.urlencode(query)

def list_videos():
    url = BASE_URL + '/vodtype/1.html'
    try:
        html = urllib.request.urlopen(url).read().decode('utf-8')
        matches = re.findall(r'<a href="(/voddetail/\d+\.html)".*?title="([^"]+)"', html)
        for link, title in matches:
            li = xbmcgui.ListItem(label=title)
            url = build_url({'action': 'play', 'video': link})
            xbmcplugin.addDirectoryItem(handle=HANDLE, url=url, listitem=li, isFolder=False)
        xbmcplugin.endOfDirectory(HANDLE)
    except Exception as e:
        xbmcgui.Dialog().ok("Duboku Error", f"Failed to load videos: {str(e)}")

def play_video(path):
    try:
        # Try multiple geo-subdomains
        subdomains = ['ea', 'us', 'www']
        for sub in subdomains:
            full_url = f"https://{sub}.duboku.fun{path}"
            try:
                html = urllib.request.urlopen(full_url).read().decode('utf-8')
                match = re.search(r'src="(https://[^"]+\.m3u8)"', html)
                if match:
                    play_item = xbmcgui.ListItem(path=match.group(1))
                    xbmcplugin.setResolvedUrl(HANDLE, True, listitem=play_item)
                    return
            except:
                continue
        raise Exception("Playable link not found.")
    except Exception as e:
        xbmcgui.Dialog().ok("Playback Error", f"Could not fetch video: {str(e)}")

def router(paramstring):
    params = dict(urllib.parse.parse_qsl(paramstring))
    if params:
        if params['action'] == 'play':
            play_video(params['video'])
    else:
        list_videos()

if __name__ == '__main__':
    router(sys.argv[2][1:])
