import pandas as pd
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
# 長さの平均をとる
lengthDatas = []
for face in face_datas:
    lengthDatas.append(len(face))

lengthMean = pd.Series(lengthDatas).mean() / 1.55

# レーベンシュタイン距離のデータ
distances = pd.DataFrame(cdist(pd.Series(face_datas), pd.Series([input_string])))[0]
face_amount = distances.quantile([0, 0.25, 0.5, 0.75, 1]).mean() - (lengthMean - len(input_string)) - 20

is_face = face_amount >= 0

print("====")

if is_face:
    print("Is face: True")
else:
    print("Is face: False")

print(Template("Face amount: ${amount}\n====").substitute(amount=face_amount))