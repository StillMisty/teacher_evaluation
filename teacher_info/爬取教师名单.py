import httpx
import os
os.chdir(os.path.dirname(__file__))
import json

url = "http://cta.jxufe.edu.cn/searchTeachers"
data = {"fid": 109051,
        "teaName": None,
        "researchFields": None, 
        "groupname": None,
        "page": 1,
        "pageSize": 10
}

res = httpx.post(url, data=data)
data.update({"pageSize": res.json()["totalResult"]})

res = httpx.post(url, data=data)
json_data = res.json()["teachersInfos"]
json.dump(json_data, open("total_info.json", "w", encoding="utf-8"), ensure_ascii=False, indent=4)