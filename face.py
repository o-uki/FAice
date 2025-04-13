import pandas as pd
import re
from rapidfuzz.process import cdist
from string import Template

# 顔文字のリスト
face_datas = []

# 文字の出現量のリスト
character_datas = pd.DataFrame({"character_data": [], "count": []})

# 顔文字のデータファイル
face_data_file = pd.read_csv("./face_data.csv")
for face_item in face_data_file:
    # アルファベットが含まれていないか
    if not re.match("[a-zA-Z]+", face_item):
        # 文字を一つずつチェック
        for character in face_item:
            contain_data = character_datas[character_datas["character_data"] == character]
            if len(contain_data) > 0:
                get_index = contain_data.index.values.tolist()[0]
                add_amount = character_datas.loc[get_index, "count"]
                character_datas.loc[get_index, "count"] = add_amount + 1
            else:
                character_datas = pd.concat([character_datas, pd.DataFrame({"character_data": [character], "count": [0]}, index=[len(character_datas)])])

        face_datas.append(face_item)

# 文字列の入力を求める
input_string = input("Enter here! > ")

# 入力された文字列が顔文字かどうか判断する
# レーベンシュタイン距離のデータ
distances = pd.DataFrame(cdist(pd.Series(face_datas), pd.Series([input_string])))[0]
distances_median = distances.median()

print("====")

if distances_median > 7:
    print("Is face: True")
else:
    print("Is face: False")

print(Template("Face amount: ${amount}\n====").substitute(amount=distances_median))