import requests
from bs4 import BeautifulSoup
import emoji

# 書き込み用のリスト
write_file_data = []

# HTML取得
html_data = requests.get("https://snskeyboard.com/emoticon/?lang=ja")
html_data.encoding = html_data.apparent_encoding

html_object = BeautifulSoup(html_data.text, "html.parser")

# HTMLを解析して顔文字を取得
face_containers = html_object.find_all("div", attrs={"class": "data"})

for container in face_containers:
    face_element_datas = container.find_all("pre")
    for face_element_data in face_element_datas:
        face_data_string = face_element_data.string
        # 絵文字ないか判定
        if emoji.emoji_count(face_data_string) == 0:
            write_file_data.append(face_data_string)

# 顔文字の書き込み用データファイル
with open("./face_data.csv", "w", encoding="UTF-8") as face_data_file:
    print(*write_file_data, sep=",", file=face_data_file)