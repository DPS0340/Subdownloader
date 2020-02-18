import sys
from os import system, listdir
from os.path import dirname, basename, exists, isdir, abspath, normpath
from settings import PYTHON_COMMAND
import re

def search(paths):
    for fp in paths:
        fp = abspath(fp)
        print('found {0}'.format(basename(fp)))
        if isdir(fp):
            print("it's directory, doing recursive search")
            search([abspath(fp+"/"+e) for e in listdir(fp)])
            continue
        if fp.split(".")[-1] not in ["mp4", "avi", "mkv"]:
            print("it's not a video")
            continue
        parent = dirname(fp)
        filename = basename(fp)[0:-(len(fp.split(".")[-1])+1)]
        if exists(parent+"/"+filename+".smi") or exists(parent+"/"+filename+".srt"):
            print("subtitle already exists!")
            continue
        command = '%s %s/core.py --keyword=\"%s\" --dst_dir=\"%s\"' % (PYTHON_COMMAND, sys.path[0], filename, parent)
        # print(command)
        system(command)

def main():
    # print(sys.argv[1:])

    file_paths = sys.argv[1:]
    print(file_paths)
    search(file_paths)


if __name__ == "__main__":
    main()
