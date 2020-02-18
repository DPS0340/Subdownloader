import requests
from bs4 import BeautifulSoup
import re
import mimetypes
from os.path import exists, normpath
from settings import PARSER
from difflib import SequenceMatcher
from googlesearch import search as google
import time

def requestSoup(url, parser=PARSER):
    html = requests.get(url)
    return BeautifulSoup(html.text, parser)

def saveBinaryFile(blob, dest, name, ext):
    with open(normpath('%s/%s.%s') % (dest, name, ext), 'wb+') as w:
        w.write(blob)
    print('downloading file...\n"%s/%s.%s"' % (dest, name, ext))

def perfomGoogleSearch(keyword):
    print(keyword)
    try:
        answer = list(google("{0} site:cineaste.co.kr".format(keyword), lang="ko", stop=1))[0]
    except:
        return None
    print(answer)
    if "cineaste.co.kr" not in answer:
        return None
    return answer


def searchSub(keyword):
    url = perfomGoogleSearch(keyword)
    if url is None:
        print("subtitle not found!\n")
        return None, None
    try:
        soup = requestSoup(url)
        a = soup.find("a", class_="list-group-item break-word view_file_download at-tip")
        regex = re.compile(r"([^ ]+?)([.]smi|[.]srt)", re.IGNORECASE | re.DOTALL)
        regexed = re.search(regex, str(a.text).strip())
        link = a["href"]
        name = regexed.group(1)
        ext = regexed.group(2)[1:]
        huddle = 0.50
        print("using parsed keyword: {0}".format(keyword))
        print("found subtitle!\n{0}\n\nis that correct?\n".format(name))
        similarity = SequenceMatcher(a=keyword.replace(" ", "."), b=name).ratio()
        temp = SequenceMatcher(a=keyword.replace(".", " "), b=name).ratio()
        if similarity < temp:
            temp = similarity
        print("\nsimilarity: %d\n" % int(similarity*100))
        if similarity >= huddle:
            print("i think that's correct!")
            return link, ext
        else:
            print("no, it's incorrect.")
            raise NameError
    except Exception as err:
        print(err)
        print("subtitle not found!\n")
        return None, None


def saveasfile(directory, name, ext, query):
    session = requests.get(query)
    if not exists(normpath("%s/%s.%s") % (directory, name, ext)):
        saveBinaryFile(session.content, directory, name, ext)


def run(keyword, dst_dir):
    if not (keyword and dst_dir):
        print("invalid arguments")
        return
    
    query, ext = searchSub(keyword)

    if query and ext:
        saveasfile(dst_dir, keyword, ext, query)
        return True
    else:
        return False
