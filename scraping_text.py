from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import MeCab
import pandas as pd
from rapidfuzz.process import cdist

# # スクレイピング
# # 顔文字と文章のデータのリスト
# face_texts = []

# browser = webdriver.Chrome()
# for i in range(406):
#     browser.implicitly_wait(1)
#     browser.get('https://www.kaomoji-ichiran.com/')
#     try:
#         browser.execute_script("arguments[0].click();", browser.find_element(by=By.XPATH, value="//*[@id='post-439']/div/table/tbody/tr[" + str(i + 2) + "]/td[1]/a"))
#         face_texts += browser.find_element(by=By.XPATH, value="//*[@id='post-" + str(i + 32) + "']/div/p[2]").text.split("\n■ ")
#     except:
#         continue

# MeCabの準備
mecab = MeCab.Tagger()

# 文字列が顔文字か判断する関数
def isStringFace(string):
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
def isInFace(checkWords):
    words = checkWords.copy()
    wordsLength = len(words)

    faces = []
    inFaceFlag = False

    for i in range(wordsLength):
        for j in range(wordsLength - i):
            detectRangeList = words[i : j + 1 + i].copy()
            detectString = "".join(detectRangeList)

            if isStringFace(detectString):
                del words[i : j + 1 + i]
                faces.append("".join(detectRangeList))
                inFaceFlag = True
    
    return {"words": words, "faces": faces, "inFace": inFaceFlag}

print(isInFace(["どうも", "みなさん", "こんにちは"]))

# トークナイズする関数
def tokenize(string):
    nodes = mecab.parseToNode(string)
    tokens = []
    while nodes:
        tokens.append(nodes.surface)
        nodes = nodes.next

    return tokens

# # 顔文字を一つずつチェック
# for i, post in enumerate(japanese_bluesky_data.posts):
#     print("Index:", i, "Text:", post.record.text, "\n")
#     tokenFace = isInFace(tokenize(post.record.text))
    
#     if tokenFace["inFace"]:
#         # ファイルに書き込み
#         with open("./bluesky_data.csv", "a", encoding="UTF-8") as post_text_data_file:
#             print(print("," + " ".join(tokenFace["words"]) + "," + tokenFace["face"], file=post_text_data_file), file=post_text_data_file)

#         print("Face Printed!!")
    
#     print("======")

# with open("./text_data.csv", "w", encoding="UTF-8") as text_data_file:
#     # ファイルに出力する文字列
#     file_output = ""
    
#     # 顔文字データの量
#     face_texts_length = len(face_texts)

#     for face_text, i in enumerate(face_texts):
#         print("Printing...", i, "/", face_texts_length)

#         face_data = isInFace(tokenize(face_text))