import requests
from bs4 import BeautifulSoup
import urllib.request
import sys


class Download(object):
    def __init__(self, start="2005-12", end="2018-02"):
        self.start = start
        self.end = end
        self.data_url = "https://files.pushshift.io/reddit/comments/"
        self.full_link = []

    def parse_links(self):
        response = requests.get(self.data_url)
        text = BeautifulSoup(response.text, "lxml")
        link = list(text.find_all("a"))
        link = list(map(lambda x: x.get("href"), link))
        link = list(filter(lambda x: "RC" in x, link) )
        link = list(set(link))

        full_link = list(map(lambda x: "https://files.pushshift.io/reddit/comments/" + x, link))
        full_link = sorted(full_link)
        self.full_link = full_link[:]

    def save_links(self):
        try:
            self.parse_links()
        except:
            print("Error when acquiring all links...")

        start = list(map(int, self.start.split("-") ) )
        end = list(map(int, self.end.split("-") ) )

        if start[0] < 2005 or start[0] > 2018 or start[1] > 12 or start[1] < 1:
            print("Wrong start date...")
            exit()
        if end[0] < 2005 or end[0] > 2018 or end[1] > 12 or end[1] < 1:
            print("Wrong end date...")
            exit()

        if start[0] > end[0]:
            print("Wrong date...")
            exit()

        if start[0] == end[0] and start[1] > end[1]:
            print("Wrong date...")
            exit()

        start_idx = 0
        end_idx = 0
        if start[0] > 2005:
            start_idx += start[1] + (start[0] - 2005 - 1) * 12
        else:
            start_idx = 0

        if end[0] > 2005:
            end_idx += end[1] + (end[0] - 2005 - 1) * 12 + 1
        else:
            end_idx = 0

        output = self.full_link[start_idx:end_idx]

        f = open("download_links.txt", "w+")
        for i in output:
            f.write(i+"\n")
        f.close()



if __name__ == "__main__":
    args = sys.argv[1:]
    start, end = args
    if "-" not in start or "-" not in end:
        print("Please enter start date and end date in this format: 2005-12 2018-02  ")
        exit()
    print(start, end)
    d = Download(start, end)
    d.save_links()
