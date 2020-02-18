import argparse
import requests
from bs4 import BeautifulSoup
import re
import mimetypes
from os.path import exists, normpath
from settings import PARSER
from difflib import SequenceMatcher

def requestSoup(url, parser=PARSER):
    html = requests.get(url)
    return BeautifulSoup(html.text, parser)

def saveBinaryFile(blob, dest, name, ext):
    with open(normpath('%s/%s.%s') % (dest, name, ext), 'wb+') as w:
        w.write(blob)
    print('downloading file...\n"%s/%s.%s"' % (dest, name, ext))


def searchSub(keyword, recursive=False):
    soup = requestSoup("https://www.gomlab.com/subtitle/?preface=kr&keyword=%s" % keyword)
    try:
        table = soup.find("tbody")
        subject = table.find("td", class_="subject")
        a = subject.find("a")
        link = a["href"]
        name = a.text.strip()
        huddle = 0.5
        keyword = re.match(r"(.+?)[. ]*?(\d+p)", keyword).group(1)
        print("using parsed keyword: {0}".format(keyword))
        # if recursive:
        #     huddle = 0.5
        print("found subtitle!\n\n{0}\n\nis that correct?\n".format(name))
        similarity = SequenceMatcher(a=keyword, b=name).ratio()
        print("\nsimilarity: %d\n" % int(similarity*100))
        if similarity >= huddle:
            print("i thinks that's correct!")
            return re.compile(r"\D*?\d*?&").match(link).group(0).replace("view.gom", "download.gom")
        else:
            print("no, it's incorrect.")
            # if recursive is False:
            #     sliced = re.match(r".*?S\d.*?E\d.*?[^\D]", keyword).group(0)
            #     print("try another search method...")
            #     return searchSub(sliced, recursive=True)
            raise NameError
    except:
        print("subtitle not found!\n")
        return None


def saveasfile(directory, name, query):
    session = requests.get("https://www.gomlab.com/subtitle/%s" % query)
    content_type = session.headers['content-type']
    ext = mimetypes.guess_extension(content_type)
    if ext is None:
        ext = "smi"
    if not exists("%s/%s.%s" % (directory, name, ext)):
        saveBinaryFile(session.content, directory, name, ext)


def run(keyword, dst_dir):
    if not (keyword and dst_dir):
        print("invalid arguments")
        return
    
    query = searchSub(keyword)

    if query:
        saveasfile(dst_dir, keyword, query)
        return True
    else:
        return False
