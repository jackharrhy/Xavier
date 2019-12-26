import requests
import shelve
from bs4 import BeautifulSoup
from urllib.parse import urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36"
}


def make_soup(url):
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")


class NTVCams(dict):
    ntv_cams_url = "http://ntv.ca/web-cams/"

    def cold_grab(self):
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

    def __init__(self, *args, **kwargs):
        super(NTVCams, self).__init__(*args, **kwargs)

        with shelve.open("persist") as db:
            if not "ntvcams" in db:
                ntvcams = self.cold_grab()
                db["ntvcams"] = ntvcams
                self.update(ntvcams)
            else:
                self.update(db["ntvcams"])


class NLRoadCams(dict):
    govnl_roads_url = "https://www.roads.gov.nl.ca/cameras/"

    def cold_grab(self):
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

    def __init__(self, *args, **kwargs):
        super(NLRoadCams, self).__init__(*args, **kwargs)

        with shelve.open("persist") as db:
            if not "nlroadcams" in db:
                nlroadcams = self.cold_grab()
                db["nlroadcams"] = nlroadcams
                self.update(nlroadcams)
            else:
                self.update(db["nlroadcams"])


if __name__ == "__main__":
    nlroadcams = NLRoadCams()
    print(nlroadcams)

    ntvcams = NTVCams()
    print(ntvcams)
