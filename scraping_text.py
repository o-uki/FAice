from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import MeCab
import pandas as pd
from rapidfuzz.process import cdist

# スクレイピング
# 顔文字と文章のデータのリスト
face_texts = []

face_data_range = 406

browser = webdriver.Chrome()
for i in range(face_data_range):
    browser.implicitly_wait(1)
    browser.get('https://www.kaomoji-ichiran.com/')
    print("Scraping...", str(round((i + 1) / face_data_range * 100, 2)) + "%", "/", "100%")
    try:
        browser.execute_script("arguments[0].click();", browser.find_element(by=By.XPATH, value="//*[@id='post-439']/div/table/tbody/tr[" + str(i + 2) + "]/td[1]/a"))
        face_text = browser.find_element(by=By.XPATH, value="//*[@id='post-" + str(i + 32) + "']/div/p[2]").text.removeprefix("■ ").split("\n■ ")
        face_texts += face_text
    except:
        continue

# MeCabの準備
mecab = MeCab.Tagger()

# 文字列が顔文字か判断する関数
def is_string_face(string):
    # 顔文字のデータファイル
    face_data_file = pd.read_csv("./face_data.csv")

    # 顔文字のリスト
    face_datas = [face_item for face_item in face_data_file]

    # 入力された文字列が顔文字かどうか判断する
    # 長さの平均をとる
    lengthDatas = [len(face) for face in face_datas]

    lengthMean = pd.Series(lengthDatas).mean() / 1.55

    # レーベンシュタイン距離のデータ
    distances = pd.DataFrame(cdist(pd.Series(face_datas), pd.Series([string])))[0]
    face_amount = distances.quantile([0, 0.25, 0.5, 0.75, 1]).mean() - abs(lengthMean - len(string)) - 20
    is_face = face_amount >= 0

    if is_face:
        return True
    else:
        return False

# 単語のリストに顔文字が含まれるか判断する関数
def is_in_face(check_words):
    words = check_words[:]
    words_length = len(words)

    faces = []
    in_face_flag = False

    for i in range(words_length):
        for j in range(words_length - i):
            detect_range_list = words[i : j + 1 + i][:]
            detect_string = "".join(detect_range_list)

            if is_string_face(detect_string):
                del words[i : j + 1 + i]
                faces.append("".join(detect_range_list))
                in_face_flag = True
    
    return {"words": words, "faces": faces, "in_face": in_face_flag}

# トークナイズする関数
def tokenize(string):
    nodes = mecab.parseToNode(string).next
    tokens = []

    while nodes:
        tokens.append(nodes.surface)
        nodes = nodes.next

    tokens.pop()
    return tokens

# 顔文字を一つずつチェック
with open("./text_data.csv", "w", encoding="UTF-8") as text_data_file:
    # ファイルに出力する文字列のリスト
    file_output_list = ["Texts", "Faces"]
    
    # 顔文字データの量
    face_texts_length = len(face_texts)

    for i, face_text in enumerate(face_texts):
        print("Printing...", str(round((i + 1) / face_texts_length * 100, 2)) + "%", "/", "100%", ">", face_text)

        face_data = is_in_face(tokenize(face_text))
        if face_data["in_face"] and face_data["words"]:
            file_output_list += ["¥¥¥".join(face_data["words"]), "¥¥¥".join(face_data["faces"])]

    print(*file_output_list, sep=",", file=text_data_file)