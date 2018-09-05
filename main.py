#!/usr/bin/python
import sys
import detector
import osshim

if len(sys.argv) < 4:
    print("usage: main.py <torrent id> <torrent name> <path>\n"
          "Example: main.py 1 My.Cool.Home.Videos /download")
    exit(-1)
detector.detect(sys.argv[2], sys.argv[3], osshim)

