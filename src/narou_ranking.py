# %%
import datetime
import gzip
import os

import requests

from helper_functions import save_json, date_to_rtype, now_jst

# %%


def request_ranking_async(rtype, out="json"):
    base_url = "https://api.syosetu.com/rank/rankget/"
    parameter = "?" + "&".join(
        [f"rtype={rtype}", f"out={out}", "gzip=5"],
    )
    url = base_url + parameter
    res = requests.get(url)
    return gzip.decompress(res.content).decode("unicode-escape")


# %%
def request_all_rankings_async(date):
    tuesday = date - datetime.timedelta(date.weekday() - 1)
    tuesday = tuesday if date > tuesday else tuesday - datetime.timedelta(7)
    month_start = date.replace(day=1)

    rtypes = (
        date_to_rtype(date, "d"),
        date_to_rtype(tuesday, "w"),
        date_to_rtype(month_start, "m"),
        date_to_rtype(month_start, "q"),
    )

    return {rtype: request_ranking_async(rtype) for rtype in rtypes}


# %%
def request_rankings_async(date):
    tuesday = date - datetime.timedelta(date.weekday() - 1)
    tuesday = tuesday if date > tuesday else tuesday - datetime.timedelta(7)
    month_start = date.replace(day=1)

    rtypes = (
        date_to_rtype(date, "d"),
        date_to_rtype(tuesday, "w") if date.date() == tuesday.date() else None,
        date_to_rtype(month_start, "m") if date.date() == month_start.date() else None,
        date_to_rtype(month_start, "q") if date.date() == month_start.date() else None,
    )

    return {r: request_ranking_async(r) for r in rtypes if r is not None}


# %%
def get_ranking_json_(f, date=None):
    date = date if date is not None else now_jst()
    date_formatted = date_to_rtype(date)
    ranking_dict = f(date)
    base_path = os.path.join(
        os.path.dirname(__file__), "..", "data", date_formatted, "ranking"
    )
    for rtype, json in ranking_dict.items():
        save_json(base_path, rtype, json)


# %%
def get_all_rankings_json(date=None):
    get_ranking_json_(request_all_rankings_async, date)


# %%
def get_rankings_json(date=None):
    get_ranking_json_(request_rankings_async, date)


# %%
if __name__ == "__main__":
    get_rankings_json()
