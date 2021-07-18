# %%
import datetime
import os


# %%
def save_json(base_path, file_name, json):
    os.makedirs(base_path, exist_ok=True)
    with open(os.path.join(base_path, file_name+".json"), mode="w") as f:
        f.write(json)


# %%
# def save_json(rtype, json, kind="novel_info"):
#     date = rtype[:-2]
#     base_path = os.path.join(os.path.dirname(__file__), "..", "data")
#     path = os.path.join(base_path, date, kind)
#     os.makedirs(path, exist_ok=True)
#     with open(os.path.join(path, rtype), mode="w") as f:
#         f.write(json)


# %%
def now_jst():
    jst = datetime.timezone(datetime.timedelta(hours=+9), "JST")
    return datetime.datetime.now(jst)


# %%
def date_to_rtype(date, target=""):
    return f"{date.year}{date.month:02}{date.day:02}{'-'+target if target!='' else ''}"

# %%
