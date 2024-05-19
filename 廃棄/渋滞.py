# -*- coding: utf-8 -*-

# 一次元セルオートマトンによる渋滞の状態変化
import random
import copy

MAX = 45
SIM_TIME = 5
P = 0.6

# 状態0は車なしの空きスペース
# 状態1は車両を表す
trafic = [0 for i in range(MAX)]


def list2string(l):
    string = ""
    for state in l:
        if state == 0:
            s = "□ "
        elif state == 1:
            s = "■ "
        string += s
    return string


def setRandom(l, p):
    for i, state in enumerate(l):
        if p < random.random():
            l[i] = 0
        else:
            l[i] = 1


def nextTime(l):
    temp = copy.deepcopy(l)
    for i, state in enumerate(l):
        if state == 0:
            # 左端なら
            if i == 0:
                temp[i] = 0
            # それ以外のとき後方チェック
            elif l[i-1] == 0:
                temp[i] = 0
            else:
                temp[i] = 1

        elif state == 1:
            # 右端なら
            if i == len(l)-1:
                temp[i] = 0
            # それ以外のとき前方チェック
            elif l[i+1] == 0:
                temp[i] = 0
            else:
                temp[i] = 1
    return temp

if __name__ == "__main__":
    # 実行部分
    setRandom(trafic, P)
    print(list2string(trafic))

    for i in range(SIM_TIME):
        # 情報を更新
        trafic = nextTime(trafic)
        # 情報を文字にして描画
        print(list2string(trafic))
