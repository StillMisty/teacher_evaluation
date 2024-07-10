import httpx
import ujson as json
import asyncio
import os

os.chdir(os.path.dirname(__file__))

async def get_total():
    """获取总的教师信息"""
    url = "http://cta.jxufe.edu.cn/searchTeachers"
    data = {
        "fid": 109051,
        "teaName": None,
        "researchFields": None,
        "groupname": None,
        "page": 1,
        "pageSize": 10,
    }

    res = httpx.post(url, data=data)
    data.update({"pageSize": res.json()["totalResult"]})

    res = httpx.post(url, data=data)
    json_data = res.json()["teachersInfos"]
    json.dump(
        json_data,
        open("total_info.json", "w", encoding="utf-8"),
        ensure_ascii=False,
        indent=4,
    )


async def get_detail(info):
    """获取教师详细信息"""
    url = r"http://cta.jxufe.edu.cn/home/teachInfo"

    uid = info.get("uid")
    fid = info.get("fid")
    data = {"fid": fid, "uid": uid, "isPreview": None}
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, data=data)
        except Exception:
            print(f"{uid}信息请求失败")
            return

        data = res.json().get("data")
        if data:
            with open(f"./teacher/{uid}.json", "w", encoding="utf-8") as f:
                f.write(data)
            print(f"{uid}信息写入成功")
        else:
            return


async def get_photo(info):
    """获取教师头像"""
    temp = info.get("photo")
    if temp is None or temp == "":
        return

    url = r"http://p.ananas.chaoxing.com/star3/origin/"
    # 因为有反爬 伪造请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        "Host": "p.ananas.chaoxing.com",
    }

    uid = info.get("uid")
    photo = url + temp + ".png"

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(photo, headers=headers)
        except Exception:
            print(f"{uid}头像下载失败")
            return

        new_data = res.content
        with open(f"./headimgs/{uid}.png", "wb") as f:
            f.write(new_data)
            print(f"{uid}头像下载成功")


async def main():
    await get_total()

    if not os.path.exists("teacher"):
        os.mkdir("teacher")
    if not os.path.exists("headimgs"):
        os.mkdir("headimgs")

    total_info: list[dict] = json.load(open("total_info.json", "r", encoding="utf-8"))
    print("开始获取详细信息，稍等片刻")

    tasks = []
    for info in total_info:
        tasks.append(get_detail(info))
        tasks.append(get_photo(info))
        # 限制并发数
        if tasks.__len__() >= 120:
            await asyncio.gather(*tasks)
            tasks.clear()


asyncio.run(main())
