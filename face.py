import pandas as pd
import re
from rapidfuzz.process import cdist
from string import Template

# 顔文字のリスト
face_datas = []

# 顔文字のデータファイル
face_data_file = pd.read_csv("./face_data.csv")
for face_item in face_data_file:
    face_datas.append(face_item)

# 文字列の入力を求める
input_string = input("Enter here! > ")

# 入力された文字列が顔文字かどうか判断する
# レーベンシュタイン距離のデータ
distances = pd.DataFrame(cdist(pd.Series(face_datas), pd.Series([input_string])))[0]
distances_median = distances.quantile([0, 0.25, 0.5, 0.75, 1]).mean() - 20

print("====")

if distances_median >= 0:
    print("Is face: True")
else:
    print("Is face: False")

print(Template("Face amount: ${amount}\n====").substitute(amount=distances_median))