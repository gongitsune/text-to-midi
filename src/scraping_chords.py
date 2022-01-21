import requests  # type: ignore
from bs4 import BeautifulSoup
from requests.models import Response  # type: ignore
import json


class Scraping:
    def get_chords(self) -> None:
        chords_list: list[list[str]] = []
        page_url = "https://gakufu.gakki.me/search/?mode=list&wo??rd=AT:BiSH"
        href_list = self.get_href_list(page_url)
        for count, href in enumerate(href_list):
            print(f"{count} / {len(href_list)}", end="\r", flush=True)
            if count == 5:
                break
            chords = self.extract_chords(requests.get(f"https://gakufu.gakki.me{href}"))
            chords_list.append(chords)

        with open("dist/chords_data.json", "w", encoding="utf-8") as f:
            json.dump(chords_list, f)

    def extract_chords(self, response: Response) -> list[str]:
        soup = BeautifulSoup(response.content, "html.parser")

        res = [
            tag.text.replace("\uff03", "#").replace("\u266d", "b")
            for tag in soup.find_all("span", attrs={"class": "cd_fontpos"})
        ]
        res.append("[EOF]")
        return res

    def get_href_list(self, url: str) -> list[str]:
        return [
            elem.find("a").get("href")
            for elem in BeautifulSoup(
                (requests.get(url)).content, "html.parser"
            ).find_all("p", attrs={"class": "mname"})
            if "on" not in elem
        ]


if __name__ == "__main__":
    Scraping().get_chords()
