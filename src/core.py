import requests
from hyper.contrib import HTTP20Adapter
from bs4 import BeautifulSoup
import re
import mimetypes
from os.path import exists, normpath
from settings import PARSER
from difflib import SequenceMatcher
import hyper
import traceback
import time
import urllib.parse

gomlab = requests.Session()
gomlab.mount("https://www.gomlab.com/", HTTP20Adapter())

reflat = requests.Session()
reflat.mount("https://reflat.net/", HTTP20Adapter())

gomlabSearchFormat = "https://www.gomlab.com/subtitle/?preface=kr&keyword=%s"
reflatSearchFormat = "https://reflat.net/sear/%s?"

timeout = 10

movieparse = r"(?:(?:^(?:[\[\(][\da-zA-Z\-]*?[\]\)])?[ .]?(.*?(?:\d{4}?))[ .]?(?:(?:\d{3,4}p)|(?:[\[\(].*?\d*?x\d*?.*?[\]\)])|[ .]))|(?:\((.*?) ?,? ?(\d{4})?\))|(.*S\d+E\d+))"


def gomlabUrlParse(url):
    return '/subtitle/download.gom?seq={0}'.format(re.compile(r"\D*?(\d+)&").search(url).group(1))


def reflatUrlParse(url):
    return '/loadFILES?p_seq={0}'.format(re.compile(r"seq=(\d+)").search(url).group(1))


def requestSoup(conn=gomlab, query="/", parser=PARSER):
    try:
        print("{0}".format(query))
        html = conn.request("GET", query, timeout=timeout).text
        return BeautifulSoup(html, parser)
    except Exception as err:
        print(err)
        traceback.print_tb(err.__traceback__)
        return None


def saveBinaryFile(blob, dest, name, ext):
    with open(normpath('%s/%s.%s') % (dest, name, ext), 'wb+') as w:
        w.write(blob)
    print('downloading file...\n"%s/%s.%s"' % (dest, name, ext))


def searchSub(keyword, conn, format):
    print("keyword: %s" % keyword)
    keyword = urllib.parse.quote_plus(keyword)
    soup = requestSoup(conn, format % keyword)
    if soup is None:
        return
    try:
        a = ""
        link = ""
        name = ""
        if conn == gomlab:
            table = soup.find("tbody")
            subject = table.find("td", class_="subject")
            a = subject.find("a")
            link = a["href"]
            regex = re.search(movieparse, a.text.strip())
            if regex.group(1) is not None:
                name = regex.group(1)
            elif regex.group(2) is not None and regex.group(3) is not None:
                name = regex.group(2) + " " + regex.group(3)
            elif regex.group(4) is not None:
                name = regex.group(4)
            else:
                name = a.text.strip()
        elif conn == reflat:
            a = soup.find("h4").find("a")
            link = a["href"]
        res = ""
        if conn == gomlab:
            res = "https://www.gomlab.com{0}".format(gomlabUrlParse(link))
        elif conn == reflat:
            res = reflatUrlParse(link)
            soup = requestSoup(conn, "https://reflat.net{0}".format(res))
            print("https://reflat.net{0}".format(res))
            a = soup.find("a")
            print(a["title"])
            print(a["data-floc"])
            regex = re.search(movieparse, a["title"])
            res = "https://sail.reflat.net/api/dwFunc/?l=blog%2Frocketman%2F{0}&f={1}".format(
                a["data-floc"], a["title"])
            if regex.group(1) is not None:
                name = regex.group(1)
            elif regex.group(2) is not None and regex.group(3) is not None:
                name = regex.group(2) + " " + regex.group(3)
            elif regex.group(4) is not None:
                name = regex.group(4)
            else:
                name = a.text.strip()
        huddle = 0.62
        print("using parsed keyword: {0}".format(keyword))
        print("found subtitle!\n\n{0}\n\nis that correct?\n".format(name))
        similarity = SequenceMatcher(a=keyword, b=name).ratio()
        print("\nsimilarity: %d\n" % int(similarity*100))
        if similarity >= huddle:
            print("i think that's correct!")
            return res
        else:
            print("no, it's incorrect.")
            raise NameError
    except Exception as err:
        print(err)
        traceback.print_tb(err.__traceback__)
        print("subtitle not found!\n")
        return None


def searchReflat(keyword):
    print(keyword)
    regex = re.search(movieparse, keyword)
    if regex is not None:
        if regex.group(1) is not None:
            keyword = regex.group(1)
        elif regex.group(2) is not None and regex.group(3) is not None:
            keyword = regex.group(2) + " " + regex.group(3)
        elif regex.group(4) is not None:
            keyword = regex.group(4)
        else:
            pass
    print(keyword)
    return searchSub(keyword, reflat, reflatSearchFormat)


def searchGom(keyword):
    return searchSub(keyword, gomlab, gomlabSearchFormat)


def saveasfile(directory, name, session):
    ext = ""
    try:
        content_type = session.headers['content-type']
        ext = mimetypes.guess_extension(content_type)
        if ext != "srt":
            ext = "smi"
    except KeyError:
        ext = "smi"
    if not exists("%s/%s.%s" % (directory, name, ext)):
        saveBinaryFile(session.content, directory, name, ext)


def run(keyword, dst_dir):
    if not (keyword and dst_dir):
        print("invalid arguments")
        return

    isReflat = True

    query = searchReflat(keyword)

    if not query:
        isReflat = False
        query = searchGom(keyword)

    if query:
        print(query)
        if isReflat:
            saveasfile(dst_dir, keyword, reflat.request(
                "GET", query, timeout=timeout))
        else:
            saveasfile(dst_dir, keyword, gomlab.request(
                "GET", query, timeout=timeout))
        return True
    else:
        return False
