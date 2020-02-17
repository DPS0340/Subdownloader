import argparse
import requests
from bs4 import BeautifulSoup
import re
import mimetypes
import lxml

def requestSoup(url, parser="lxml"):
    html = requests.get(url)
    return BeautifulSoup(html.text, parser)

def saveBinaryFile(blob, dest, name, ext):
    with open("%s/%s.%s" % (dest, name, ext), 'wb') as w:
        w.write(blob)
    print("%s/%s.%s" % (dest, name, ext))


def searchSub(keyword):
    soup = requestSoup("https://www.gomlab.com/subtitle/?preface=kr&keyword=%s" % keyword)
    table = soup.find("tbody")
    subject = table.find("td", class_="subject")
    link = subject.find("a")["href"]
    return re.compile("\D*?\d*?&").match(link).group(0).replace("view.gom", "download.gom")


def saveasfile(directory, name, query):
    session = requests.get("https://www.gomlab.com/subtitle/%s" % query)
    content_type = session.headers['content-type']
    ext = mimetypes.guess_extension(content_type)
    if ext is None:
        ext = "smi"
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

    saveasfile(args.dst_dir, args.keyword, query)



if __name__ == "__main__":
    main()