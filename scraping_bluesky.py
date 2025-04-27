from atproto import Client
import json
import MeCab
import pandas as pd
from rapidfuzz.process import cdist
import copy

# 書き込み用のリスト
write_file_data = []

# Bluesky取得
client = Client()
with open("./local.json", "r") as data_json:
    bluesky_data = json.load(data_json)["bluesky"]
    client.login(bluesky_data["handle_name"], bluesky_data["password"])

japanese_bluesky_data = client.app.bsky.feed.search_posts({"q": "lang:ja", "sort": "latest", "limit": 30})

# MeCabの準備
mecab = MeCab.Tagger()

# 文字列が顔文字か判断する関数
def isStringFace(string):
    # 顔文字のリスト
    face_datas = []

    # 顔文字のデータファイル
    face_data_file = pd.read_csv("./face_data.csv")
    for face_item in face_data_file:
        face_datas.append(face_item)

    # 入力された文字列が顔文字かどうか判断する
    # 長さの平均をとる
    lengthDatas = []
    for face in face_datas:
        lengthDatas.append(len(face))

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
    detectRangeList = []
    
    for i in range(len(words)):
        for j in range(len(words) - i):
            detectRangeList = words[i : j + 1 + i].copy()
            detectString = "".join(detectRangeList)

            if isStringFace(detectString):
                del words[i : j + 1 + i]
                return {"words": words, "face": "".join(detectRangeList), "inFace": True}
            
    return {"words": words, "face": "", "inFace": False}

# トークナイズする関数
def tokenize(string):
    nodes = mecab.parseToNode(string)
    tokens = []
    while nodes:
        tokens.append(nodes.surface)
        nodes = nodes.next

    return tokens

# Blueskyの投稿を一つずつチェック
for i, post in enumerate(japanese_bluesky_data.posts):
    tokenFace = isInFace(tokenize(post.record.text))
    if tokenFace["inFace"]:
        print("Face:", tokenFace["face"])
    print("Loding...", i, post.record.text)

# # 顔文字の書き込み用データファイル
# with open("./bluesky_data.csv", "w", encoding="UTF-8") as post_text_data_file:
#     print(*write_file_data, sep=",", file=post_text_data_file)