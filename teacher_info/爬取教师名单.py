import httpx

import os
os.chdir(os.path.dirname(__file__))

import json

url = "http://cta.jxufe.edu.cn/searchTeachers"

pageSize = 10

data = {"fid": 109051,
        "teaName": None,
        "researchFields": None, 
        "groupname": None,
        "page": 1,
        "pageSize": pageSize
}

res = httpx.post(url, data=data)


pageSize = res.json()["totalResult"] if pageSize < res.json()["totalResult"] else pageSize

res = httpx.post(url, data=data)

json_data = res.json()["teachersInfos"]

json.dump(json_data, open("total_info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)