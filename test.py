import numpy as np
from delaunayextrapolation import DelaunayE

if __name__ == "__main__":
    # 代表点。4つだけ。
    points = np.array([[0, -0.1], [0, 1.1], [1.2, 0], [1, 1]])

    # Delaunay三角形分割
    tri = DelaunayE(points)

    # 内挿(外挿)したい点
    p = np.array([0.5, 0.7])

    # 内挿結果を得る。
    v, ratio = tri.mixratio(p)
    # v: 点pを含む三角形(点が3次元以上の場合は単体)の頂点番号
    # ratio: それらの混合比

    print(v, ratio)
