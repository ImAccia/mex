#!/usr/bin/env python3

import sys
import os

class Mex:
    def __init__(self):
        self.check_args()

    def check_args(self):
        if len(sys.argv) < 2:
            print("Error: no file specified")
            sys.exit(1)

        if not os.path.exists(sys.argv[1]):
            print("Error: file not found")
            sys.exit(1)

        if not os.path.isfile(sys.argv[1]):
            print("Error: not a file")
            sys.exit(1)

    def startFileHandling(self, file, video, photo):
        if photo:
            from PhotoHandler.PhotoHandler import PhotoHandler
            pH = PhotoHandler(sys.argv[2] if len(sys.argv) == 3 else False)
            pH.handlePhoto(file, False)
        elif video:
            from VideoHandler.VideoHandler import VideoHandler
            pH = VideoHandler(sys.argv[2] if len(sys.argv) == 3 else False)
            pH.handleVideo(file)

if __name__ == '__main__':
    mexHandler = Mex()

    videoTypes = ['mp4', 'avi', 'mov', 'mkv']
    photoTypes = ['jpg', 'jpeg', 'png']

    file = sys.argv[1]
    ext = file.split('.')[-1]

    isVid = ext in videoTypes
    isPhoto = ext in photoTypes

    if isVid or isPhoto:
        mexHandler.startFileHandling(file, isVid, isPhoto)
    else:
        print("Unknown file type")
        exit(1)
    
