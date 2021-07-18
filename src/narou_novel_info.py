# %%
import datetime
import glob
import gzip
import json
import os
from time import sleep

import requests

from helper_functions import date_to_rtype, now_jst, save_json
from narou_ranking import get_rankings_json


# %%
def request_novel_info(ncodes=None, genres=None, out="json"):
    base_url = "https://api.syosetu.com/novelapi/api/"
    parameter = "?" + "&".join(
        p
        for p in (
            "gzip=5",
            "lim=400",
            "order=dailypoint",
            "of=t-n-u-w-s-g-k",
            f"out={out}",
            f"ncode={'-'.join(n.lower() for n in ncodes)}"
            if ncodes is not None
            else None,
            f"genre={'-'.join(genres)}" if genres is not None else None,
        )
        if p is not None
    )
    url = base_url + parameter
    res = requests.get(url)
    return gzip.decompress(res.content).decode("unicode-escape")


# %%
def get_novel_info_json_in_ranking(date):
    date_formatted = date_to_rtype(date)
    base_path = os.path.join(os.path.dirname(__file__), "..", "data", date_formatted)
    ranking_path = os.path.join(base_path, "ranking")
    ranking_jsons_paths = glob.glob(os.path.join(ranking_path, "*"))
    if ranking_jsons_paths == []:
        get_rankings_json(date)
        ranking_jsons_paths = glob.glob(os.path.join(ranking_path, "*"))
    path_novel_info = os.path.join(base_path, "ranking_novel_info")
    ranking_jsons_paths_filtered = [
        p
        for p in ranking_jsons_paths
        if not os.path.isfile(os.path.join(path_novel_info, os.path.basename(p)))
    ]
    infos = get_novel_info_json_in_ranking_(ranking_jsons_paths_filtered)
    for r, info in infos.items():
        print(r)
        save_json(path_novel_info, r, info)


# %%
def get_novel_info_json_in_ranking_(ranking_jsons_paths):
    rankings = dict()
    for path in ranking_jsons_paths:
        rtype = os.path.splitext(os.path.basename(path))[0]
        with open(path, mode="r") as f:
            rankings[rtype] = json.load(f)
    ncodes = {r: [j["ncode"] for j in js] for r, js in rankings.items()}
    infos = {r: request_novel_info(ncodes=np) for r, np in ncodes.items()}
    return infos


# %%
if __name__ == "__main__":
    now = now_jst()
    for before in range(1, 32):
        date = now - datetime.timedelta(before)
        get_novel_info_json_in_ranking(date)
        sleep(1)

# %%
