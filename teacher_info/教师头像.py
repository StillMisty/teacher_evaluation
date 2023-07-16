import httpx
import json
import asyncio
import os
from typing import List
os.chdir(os.path.dirname(__file__))

async def main():
    total_info : List[dict] = json.load(open("total_info.json", "r", encoding="utf-8"))
    url = r"http://p.ananas.chaoxing.com/star3/origin/"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Host": "p.ananas.chaoxing.com"
    }
    async with httpx.AsyncClient() as client:
        for i in total_info:
            temp = i.get("photo")
            uid = i.get("uid")
            if temp == None or temp == "":
                break
            photo = url + temp + ".png"
            print(photo)
            res = await client.get(photo, headers=headers)
            new_data = res.content
            with open(f"./教师头像/{uid}.png", "wb") as f:
                f.write(new_data)
                
                
asyncio.run(main())