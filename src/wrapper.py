import sys
from os import listdir
from os.path import dirname, basename, exists, isdir, abspath, normpath
from settings import PYTHON_COMMAND
import re
import core

notFoundSubs = []

def search(paths):
    global notFoundSubs
    for fp in paths:
        fp = abspath(fp)
        print('found {0}'.format(basename(fp)))
        if isdir(fp):
            print("it's directory, doing recursive search\n\n")
            search([abspath(fp+"/"+e) for e in listdir(fp)])
            continue
        if fp.split(".")[-1] not in ["mp4", "avi", "mkv"]:
            print("it's not a video.\n\n")
            continue
        parent = dirname(fp)
        filename = basename(fp)[0:-(len(fp.split(".")[-1])+1)]
        if exists(parent+"/"+filename+".smi") or exists(parent+"/"+filename+".srt"):
            print("subtitle already exists!\n\n")
            continue
        print("\n\n", end="")
        res = core.run(filename, parent)
        if res is False:
            notFoundSubs.append(filename)

def main():
    global notFoundSubs

    file_paths = sys.argv[1:]
    print(file_paths)
    search(file_paths)

    if notFoundSubs:
        print("not found subtitles to notfound.txt")
        with open(dirname(dirname(abspath(__file__))) + "/notfound.txt", "w+") as w:
            w.write("\n".join(notFoundSubs))


if __name__ == "__main__":
    main()
