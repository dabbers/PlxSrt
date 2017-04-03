import os
import sys
import re
import tvparser

# List of extensions that count as a "zip" or compressed file
_zips = [".rar", ".zip", ".gz", ".tar"]
# All extensions that should be copied over (that don't contain sample)
_media = [".mkv", ".avi", ".mp4", ".webm"]
#Subtitle extensions
_sub = [".sub", ".idx", ".srt"]
# File types we expect to not have to handle. Other files will be processed.
_ignore = [".nfo", ".sfv", ".txt", ".doc", ".docx", ".rtf"]

def _isZip(fullpath): # {
    fn, ext = os.path.splitext(fullpath.lower())
    return (ext in _zips)
#}

def _isMedia(fullpath): #{
    fn, ext = os.path.splitext(fullpath.lower())
    return (ext in _media) and not ("sample" in fn)
#}

def _isSubtitle(fullpath): #{
    fn, ext = os.path.splitext(fullpath.lower())
    return (ext in _sub) and not ("sample" in fn)
#}

def _isKnownNoOp(fullpath): #{
    fn, ext = os.path.splitext(fullpath.lower())
    return (ext[1] == "r" or ext in _ignore)
#}

def _couldBeSubs(fullpath):
    return "subs" in fullpath.lower() or "subtitle" in fullpath.lower() or _isSubtitle(fullpath)


def getDestinationPathForFile(filename, path, osshim):
    fullpath = os.path.join(path, filename)
    tv = tvparser.getSeasonAndEpisode(fullpath)

    if (tv == None):
        # Movies go in Movies\MovieName\Movie.mkv
        return os.path.join( osshim.movieFolder(), tvparser.getCleanNameFromPath(fullpath))
    else:
        # TV goes in TV\Show Name\Season ##\Episode.##.mkv
        if (int(tv.season) < 1000):
            return os.path.join( osshim.tvFolder(), tv.show, "Season " + str(int(tv.season)))
        
        return os.path.join( osshim.tvFolder(), tv.show, str(int(tv.season)))


def detect(filename, path, osshim): #{
    source = os.path.join(path, filename)
    #print filename + ' ' + path
    #print("Checking: " + source)
    if (osshim.isdir(source)):
        dirs = osshim.listdir(source)

        # Quick check to see if folder has multi-part rar folder with all files ending in .rar
        # This script would attempt to extract each partial rar file, resulting in n-attempts of extracting
        # a file where n is the number of parts.
        rars = filter(_isZip, dirs)

        results = []

        if (len(rars) > 1 and ".part" in rars[0].lower()):
            # Take care of any subtitle files
            subs = filter(_couldBeSubs, dirs)

            for sub in subs:
                flee = os.path.basename(sub)
                results.extend(detect(flee, source, osshim))
            
            fle = os.path.basename(rars[0])
            results.extend(detect(fle, source, osshim))
        elif (len(rars) > 0):
            for subfile in dirs:
                fle = os.path.basename(subfile)
                results.extend(detect(fle, source, osshim))
        else:
            lm = (lambda shim, o, source: (lambda a: shim.isdir(o.path.join(source, a))))(osshim, os, source)
            folders = filter( lm, dirs )
            if (len(folders) > 0):
                for subfile in dirs:
                    fle = os.path.basename(subfile)
                    results.extend(detect(fle, source, osshim))
            else:

                destpath = os.path.normpath(getDestinationPathForFile(filename, path, osshim))

                # check if maybe we parsed this current path incorrectly and a look at a file might correct it.
                secondlook_destpath = os.path.normpath(getDestinationPathForFile(dirs[0], os.path.join(path, filename), osshim)) if len(dirs) > 0 else destpath

                # If we're merging this source into an existing source, don't symlink over it.
                # Ie: IF we already extracted a tv episode into this Season, and this source is the rest of a season,
                # Don't just symlink it since the Season folder will already exist.
                if (osshim.isdir(destpath) or destpath != secondlook_destpath):
                    for subfile in dirs:
                        fle = os.path.basename(subfile)
                        results.extend(detect(fle, source, osshim))
                #elif (osshim.allowFolderLink()):
                #    results.append({"Result":True, "Output": osshim.link( source, destpath, destpath )})
                else:
                    media = filter(_isMedia, dirs)
                    for subfile in media:
                        fle = os.path.basename(subfile)
                        results.extend(detect(fle, source, osshim))
        return results
    else:
        if (_isZip(source)):
            return [{ "Result":True, "Output":osshim.extract(source, os.path.normpath(getDestinationPathForFile(filename, path, osshim))) }]
        elif (_isMedia(source) or _isSubtitle(source)):
            return [{ "Result":True, "Output":osshim.link( source, os.path.normpath(os.path.join( getDestinationPathForFile(filename, path, osshim), filename) ), os.path.normpath(getDestinationPathForFile(filename, path, osshim))) }]
        elif (_isKnownNoOp(source)):
            return []
        else:
            return [{ "Result":False, "Output":"Unknown file type" }]
#}
