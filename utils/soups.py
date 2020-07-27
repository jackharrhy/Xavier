import shelve
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

fake_user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
headers = {"User-Agent": fake_user_agent}


def make_soup(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")


class DynaDict(dict):
    def grab():
        raise NotImplementedError

    def refresh(self):
        self.update(self.grab())

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.refresh()

class NTVCams(DynaDict):
    ntv_cams_url = "http://ntv.ca/web-cams/"

    def grab(self):
        fresh_data = {}
        for tag in make_soup(NTVCams.ntv_cams_url).find_all(
            "div", class_="wpb_single_image"
        ):
            cam_link = tag.a["href"]
            location = tag.h2.text

            real_cam_link = make_soup(cam_link).iframe["src"]
            parsed_url = urlparse(real_cam_link)
            url_parts = parsed_url.path.split("/")

            real_real_cam_link = f"https://www.mangocam.com/c/{url_parts[2]}/frame.php"
            mucky_url = urlparse(make_soup(real_real_cam_link).img["src"])
            img = f"https://{mucky_url.netloc}{mucky_url.path}"
            fresh_data[location] = img
        return fresh_data

class NLRoadCams(DynaDict):
    govnl_roads_url = "https://www.roads.gov.nl.ca/cameras/"

    def grab(self):
        fresh_data = {}
        for tag in make_soup(NLRoadCams.govnl_roads_url).find_all(
            "a", href=True, target=False
        ):
            parsed_url = urlparse(tag["href"])
            url_parts = parsed_url.path.split("/")
            if dict(enumerate(url_parts)).get(1) == "cameras":
                road_page_url = f"{NLRoadCams.govnl_roads_url}{url_parts[2]}"
                img = make_soup(road_page_url).find_all("img", border=1)[0]
                fresh_data[tag.text] = img["src"]
        return fresh_data

if __name__ == "__main__":
    nlroadcams = NLRoadCams()
    print(nlroadcams)

    ntvcams = NTVCams()
    print(ntvcams)
