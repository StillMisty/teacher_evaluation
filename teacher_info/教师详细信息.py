import httpx
import json
import asyncio
import os

os.chdir(os.path.dirname(__file__))


async def main():
    
    if not os.path.exists("teacher"):
        os.mkdir("teacher")
        
    total_info : list[dict] = json.load(open("total_info.json", "r", encoding="utf-8"))
    url = r"http://cta.jxufe.edu.cn/home/teachInfo"
    
    async with httpx.AsyncClient() as client:
        for i in total_info:
            uid = i.get("uid")
            fid = i.get("fid")
            data = {
                "fid": fid,
                "uid": uid,
                "isPreview": None
            }
            res = await client.post(url,data=data)
            data = res.json().get("data")
            if data:
                with open(f"./teacher/{uid}.json", "w", encoding="utf-8") as f:
                    f.write(data)
            else:
                continue
                
                
asyncio.run(main())