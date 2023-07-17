# 教师评价

## 1. 项目简介

江西财经大学的教师评价，包含教职工信息爬取以及处理，后端以及前端展示

## 2. 项目启动

先启用爬取教师名单，再使用教师详细信息爬取以及教师头像的爬取，将所得文件移到`/backend/static`目录下。
进入`/frontend`目录下，运行`npm install`安装依赖，再运行`npm run build`打包前端文件，将所得`dist`文件夹内的文件移到`/backend/static`目录下。
进入`/backend`目录下，运行`poetry install`安装依赖，再运行`poetry run python main.py`启动后端。

## 3. 已完成

- 教职工信息爬取
- 后端接口
- 评论以及打分的提交
- IP验证是否为校内网
- 使用百度ai进行评论过滤
- 前端展示
