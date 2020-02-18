import argparse
import requests
from bs4 import BeautifulSoup
import re
import mimetypes
from os.path import exists
from settings import PARSER
from difflib import SequenceMatcher

def requestSoup(url, parser=PARSER):
    html = requests.get(url)
    return BeautifulSoup(html.text, parser)

def saveBinaryFile(blob, dest, name, ext):
    with open('"%s/%s.%s"' % (dest, name, ext), 'wb+') as w:
        w.write(blob)
    print('downloading file...\n"%s/%s.%s"' % (dest, name, ext))


def searchSub(keyword):
    soup = requestSoup("https://www.gomlab.com/subtitle/?preface=kr&keyword=%s" % keyword)
    try:
        table = soup.find("tbody")
        subject = table.find("td", class_="subject")
        a = subject.find("a")
        link = a["href"]
        name = a.text.strip()
        print("found subtitle!\n\n{0}\n\nis that correct?\n".format(name))
        similarity = SequenceMatcher(a=keyword, b=name).ratio()
        print("\nsimilarity: %d\n" % int(similarity*100))
        if similarity >= 0.7:
            print("i thinks that's correct!")
            return re.compile(r"\D*?\d*?&").match(link).group(0).replace("view.gom", "download.gom")
        else:
            print("no, it's incorrect.")
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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--keyword", help="the name of keyword")
    parser.add_argument("--dst_dir", help="destination directory")
    args = parser.parse_args()

    if not (args.keyword and args.dst_dir):
        print("invalid arguments")
        return
    
    query = searchSub(args.keyword)

    if query:
        saveasfile(args.dst_dir, args.keyword, query)



if __name__ == "__main__":
    main()
