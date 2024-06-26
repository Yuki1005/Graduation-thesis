import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import networkx as nx
import numpy as np


# エッジデータを生成
edge_list = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 0),
    (0, 5), (1, 6), (2, 7), (3, 8), (4, 9),
    (5, 10), (10, 11), (11, 6), (6, 12), (12, 13),
    (13, 7), (7, 14), (14, 15), (15, 8), (8, 16),
    (16, 17), (17, 9), (9, 18), (18, 19), (19, 5),
    (11, 20), (20, 21), (21, 12), (13, 22), (22, 23),
    (23, 14), (15, 24), (24, 25), (25, 16), (17, 26),
    (26, 27), (27, 18), (19, 28), (28, 29), (29, 10),
    (21, 30), (30, 31), (31, 22), (23, 32), (32, 33),
    (33, 24), (25, 34), (34, 35), (35, 26), (27, 36),
    (36, 37), (37, 28), (29, 38), (38, 39), (39, 20),
    (31, 40), (40, 41), (41, 32), (33, 42), (42, 43),
    (43, 34), (35, 44), (44, 45), (45, 36), (37, 46),
    (46, 47), (47, 38), (39, 48), (48, 49), (49, 30),
    (41, 50), (50, 42), (43, 51), (51, 44), (45, 52),
    (52, 46), (47, 53), (53, 48), (49, 54), (54, 40),
    (50, 55), (51, 56), (52, 57), (53, 58), (54, 59),
    (55, 56), (56, 57), (57, 58), (58, 59), (59, 55),
]

# 生成したエッジデータからグラフ作成
G = nx.Graph()
G.add_edges_from(edge_list)
# spring_layout アルゴリズムで、3次元の座標を生成する
pos = nx.spring_layout(G, dim=3)
# 辞書型から配列型に変換
pos_ary = np.array([pos[n] for n in G])

# ここから可視化
fig = plt.figure(figsize=(20, 10), facecolor="w")
ax = fig.add_subplot(projection="3d")

# 各ノードの位置に点を打つ
ax.scatter(
    pos_ary[:, 0],
    pos_ary[:, 1],
    pos_ary[:, 2],
    s=200,
)

# ノードにラベルを表示する
for n in G.nodes:
    ax.text(*pos[n], n)

# エッジの表示
for e in G.edges:
    node0_pos = pos[e[0]]
    node1_pos = pos[e[1]]
    xx = [node0_pos[0], node1_pos[0]]
    yy = [node0_pos[1], node1_pos[1]]
    zz = [node0_pos[2], node1_pos[2]]
    ax.plot(xx, yy, zz, c="#aaaaaa")

# 出来上がった図を表示
plt.show()