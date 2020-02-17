import sys
from os import system, listdir
from os.path import dirname, basename, exists, isdir, abspath, normpath
import re

def search(paths):
    for fp in paths:
        fp = abspath(fp)
        if isdir(fp):
            search([abspath(fp+"\\"+e) for e in listdir(fp)])
            continue
        if fp.split(".")[-1] not in ["mp4", "avi", "mkv"]:
                continue
        parent = dirname(fp)
        filename = basename(fp)[0:-(len(fp.split(".")[-1])+1)]
        command = 'python %s\\core.py --keyword=\"%s\" --dst_dir=\"%s\"' % (sys.path[0], filename, parent)
        system(command)

def main():

    line = "".join(sys.argv[1:])

    file_paths = re.findall(".:\\\\.*", line)
    print(file_paths)
    search(file_paths)


if __name__ == "__main__":
    main()