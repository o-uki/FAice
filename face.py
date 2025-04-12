import requests
from bs4 import BeautifulSoup

# HTML取得
html_data = requests.get("https://snskeyboard.com/emoticon/?lang=ja")
html_data.encoding = html_data.apparent_encoding

html_object = BeautifulSoup(html_data.text, "html.parser")

# 顔文字のリスト
face_datas = []

# HTMLを解析して顔文字を取得
face_containers = html_object.find_all("div", attrs={"class": "data"})

for container in face_containers:
    face_element_datas = container.find_all("pre")
    for face_element_data in face_element_datas:
        face_datas.append(face_element_data.string)

# デバッグ用、顔文字のリストを順番に出力


for item in face_datas:
    print(item)

print("ｺﾐｯﾄｫ")
print("ｺﾐｯﾄｫｱﾝｻｰ!!!")