import sys
from os import system, listdir
from os.path import dirname, basename, exists, isdir, abspath, normpath
from settings import PYTHON_COMMAND
import re

def search(paths):
    for fp in paths:
        fp = abspath(fp)
        if isdir(fp):
            search([abspath(fp+"/"+e) for e in listdir(fp)])
            continue
        if fp.split(".")[-1] not in ["mp4", "avi", "mkv"]:
            continue
        parent = dirname(fp)
        filename = basename(fp)[0:-(len(fp.split(".")[-1])+1)]
        if exists(parent+"/"+filename+".smi") or exists(parent+"/"+filename+".srt"):
            continue
        command = '%s %s/core.py --keyword=\"%s\" --dst_dir=\"%s\"' % (PYTHON_COMMAND, sys.path[0], filename, parent)
        print(command)
        system(command)

def main():
    print(sys.argv[1:])
    line = " ".join(sys.argv[1:]).replace("\\", "/")

    file_paths = [re.sub('''["']''', "", e) for e in re.findall(r'''["'].*?["']''', line)]
    print(file_paths)
    search(file_paths)


if __name__ == "__main__":
    main()
