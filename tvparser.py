import re
import os


nameRgx = re.compile("(.*).(720p|720|1080p|1080|BluRay|BRRip|BRRp|BDRip|bdrip|BDRp|bdrp|DVDRip|HDTV|HD|UHD|dvdrip|bluray|brrip|dvdscr|DVDScr|Web|WebRip|webrip|Webrip|WEBRip).*")

class TvShowResult:
    def __init__(self, name, s, e):
        self.show = name
        self.season = s
        self.episode = e

__regexes = [
    # Most common pattern. Usually show.name.s01e01.format.ext
    { "rgx": re.compile("([\w\.,\- ']+?).[Ss](\d+)[Ee](\d+)[^\d]"), "show":0, "season":1, "episode":2 },
    # Sometimes common pattern. Usually show.name.01x01.format.ext
    { "rgx": re.compile("([\w\.,\- ']+?).(\d+)[Xx](\d+)[^\d]"), "show":0, "season":1, "episode":2 },
    # Uncommon format, usually show.name.S01ep01.format.ext
    { "rgx": re.compile("([\w\.,\- ']+?).S(\d+)ep(\d+)[^\d]"), "show":0, "season":1, "episode":2 },
    # Episode with year as season. show.name.2017.03.17.format.ext
    { "rgx": re.compile("([\w\.,\- ']+?).(\d{4}).(\d{2}.\d{2})[^\d]"), "show":0, "season":1, "episode":2 },
    # Common format for only seasons. show.name.S01
    { "rgx": re.compile("([\w\.,\- ']+?).[Ss](\d{2,})[^\d]"), "show":0, "season":1, "episode":-1 },
    # Might start at beginning of regex. No starting . intentional
    { "rgx": re.compile("[Ss](\d+)[Ee](\d+)[^\d]{0,}"), "show":0, "season":0, "episode":1 },
    # Might start at beginning of regex. No starting . intentional
    { "rgx": re.compile("[Ss]eason\s+(\d+)[^\d]{0,}"), "show":-1, "season":0, "episode":-1 }
]

def getCleanNameFromPath(fullpath):
    tv = isTvShow(fullpath)

    name = ""
    if (tv != None):
        name = tv.show

    if (tv == None or len(name.strip()) == 0):
        name = cleanWithRegex(os.path.splitext(os.path.basename(fullpath))[0])

    return name

def cleanWithRegex(name):
    match = nameRgx.findall(name)

    return (match[0][0] if len(match) > 0 else name).replace(".", " ").strip()

def findTvShowName(fullPath):
    tv = getSeasonAndEpisode(fullPath)
    return tv

def isTvShow(fullpath):
    # Try finding the show name by filename, then by the rest of the path.
    # Pathname usually gets less vague close to the file name.
    parts = os.path.normpath(fullpath).split(os.path.sep)
    tv = None

    for part in reversed(parts):
        tv = findTvShowName(part)

        if (tv != None):
            break

    # Not every file/path might return an episode
    return tv

def getSeasonAndEpisode(name):
    # Check for .[Ss]\d+[Ee]\d+.
    #res = __show_reg1.findall(name)
    tvres = None
    res = False
    print name
    for r in __regexes:
        res = r["rgx"].findall(name)
        if (len(res) >= 1):
            tvres = TvShowResult( (res[0][r["show"]] if r["show"] != -1 else ""), (res[0][r["season"]] if r["season"] != -1 else ""), (res[0][r["episode"]] if r["episode"] != -1 else "")  )
            break

    if (tvres != None):
        tvres.show = cleanWithRegex(tvres.show)

    return tvres

# def __getTitleIfShow(name, api):

#     return api.findShow(name)
