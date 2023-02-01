import sys
from plexapi.server import PlexServer
from pick import pick

baseurl = ''
token = ''
plex = PlexServer(baseurl, token)


libs = plex.library.sections()
tvshowlibs = [lib for lib in libs if lib.type == "show"]

selectedLib = ""
if len(tvshowlibs) == 0:
    print("no tv libs")
    exit(1)
if len(tvshowlibs) > 1:
    title = 'Please select Library'
    options = [lib.title for lib in tvshowlibs]
    selectedLib, index = pick(options, title, indicator='-')
else:
    selectedLib = tvshowlibs[0].title
shows = plex.library.section(selectedLib)

title = 'Please select Show'
options = [show.title for show in shows.search()]
selectedShow, index = pick(options, title, indicator='-')

print("please enter the filename for the m3u")
filename = input()

f = open(filename, "w")

f.write("#EXTM3U\n\n")

for show in shows.search():
    if str(selectedShow) in show.title:
        f.write("#PLAYLIST:" + str(show.title) + "\n\n")
        for episode in show.episodes():
            media = episode.media[0]
            f.write("#EXTINF:" + str(media.parts[0].duration//1000) + "," + show.title + " - " + episode.seasonEpisode + " " + episode.title + "\n")
            f.write(baseurl + media.parts[0].key + "?download=1&X-Plex-Token=" + token + "\n\n")
        break
f.close()
