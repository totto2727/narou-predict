# %%
import os
import requests
import asyncio
import gzip
import datetime

# %%


async def request_ranking_async(rtype, out="json"):
    loop = asyncio.get_event_loop()
    base_url = "https://api.syosetu.com/rank/rankget/"
    parameter = "?" + "&".join(
        [f"rtype={rtype}", f"out={out}", "gzip=5"],
    )
    url = base_url + parameter
    res = await loop.run_in_executor(None, requests.get, url)
    return gzip.decompress(res.content).decode("utf-8")


# %%
async def request_rankings_async():
    now = now_jst()
    tuesday = now - datetime.timedelta(now.weekday() - 1)
    tuesday = tuesday if now > tuesday else tuesday - datetime.timedelta(7)
    month_start = now.replace(day=1)

    def rtype(date: datetime.date, target):
        return f"{date.year}{date.month:02}{date.day:02}-{target}"

    rtypes = (
        rtype(now, "d"),
        rtype(tuesday, "w"),
        rtype(month_start, "m"),
        rtype(month_start, "q"),
    )

    return {rtype: await request_ranking_async(rtype) for rtype in rtypes}, now


# %%
def saveJson(name, json, create_at=None):
    create_at = now_jst() if create_at is None else create_at
    directory = f"{create_at.year}{create_at.month:02}{create_at.day:02}"
    base_path = os.path.join(os.path.dirname(__file__), "..", "data")
    path = os.path.join(base_path, directory, "ranking")
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, name), mode="w") as f:
        f.write(json)


# %%
async def get_ranking_json(time=None):
    ranking_dict, now = await request_rankings_async()
    now = now if time is None else time
    for rtype, json in ranking_dict.items():
        saveJson(rtype, json, now)


# %%
def now_jst():
    jst = datetime.timezone(datetime.timedelta(hours=+9), "JST")
    return datetime.datetime.now(jst)


# %%
if __name__ == "__main__":
    asyncio.run(get_ranking_json())
