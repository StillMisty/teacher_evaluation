
import httpx
import IPy
from config import settings


def get_academicTitle(degress: str) -> str:
    '''获取职称'''
    try:
        degress = int(degress)
    except Exception:
        return ""
    
    if degress == 1:
        return "教授"
    elif degress == 2:
        return "副教授"
    elif degress == 3:
        return "讲师"
    elif degress == 4:
        return "研究员"
    elif degress == 5:
        return "副研究员"
    elif degress == 6:
        return "助理研究员"
    elif degress == 7:
        return "研究实习员"
    elif degress == 30:
        return "助教"
    else:
        return ""
    
async def content_review(content: str) -> bool:
    if settings.ACCESS_TOKEN is None:
        return True
    
    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"
    
    params = {
        "text": content
    }
    
    access_token = settings.ACCESS_TOKEN
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    
    # 异步请求，防止阻塞
    async with httpx.AsyncClient() as client:
        response = await client.post(request_url, data=params, headers=headers)

        res = response.json()
        if res.get("conclusionType") != 2:
            return True
        else:
            return False
        
def ip_review(ip: str) -> bool:
    # ip验证是否开启
    if settings.SEGMENTATION is False:
        return True
    
    for i in settings.SEGMENTATION_IP:
        if ip in IPy.IP(i):
            return True
    
    return False