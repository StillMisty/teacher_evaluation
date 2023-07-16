
def get_academicTitle(degress: int) -> str:
    '''获取职称'''

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