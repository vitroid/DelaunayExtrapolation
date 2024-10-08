from scipy.spatial import Delaunay
import numpy as np


def plane(p):
    # ax+by+cz=1を満足するabcを求める。
    abc = np.linalg.inv(p) @ np.ones_like(p[0])
    return abc


class DelaunayE(Delaunay):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        # 次元を上げる。2次元なら3次元にする。
        pulledup = np.zeros([len(self._points), self.ndim + 1])
        # 2次元まではそのままコピー
        pulledup[:, :-1] = self._points
        # 3次元目には、二乗和を入れる。
        pulledup[:, -1] = np.sum(self._points**2, axis=1)
        self.pulledup = pulledup

        self.planes = np.zeros([self.nsimplex, self.ndim + 1])
        for i, simplex in enumerate(self.simplices):
            # simplexの3点を通る方程式を定める。
            # ax+by+cz=d を3つの点のいずれでも満たすようなa,b,c,dを求めたい。
            abc = plane(pulledup[simplex])
            self.planes[i] = abc

    def extrapolate_simplex(self, point):
        # ax+by+cz = 1
        # z = (1 - (a,b)@(x,y)) / c
        ab, c = self.planes[:, :-1], self.planes[:, -1]
        z = (1 - ab @ point) / c
        which = np.argmax(z)
        return which

    def mixratio(self, p):
        """
        Determine the simplex containing the given point and calculate the mixing ratio.

        Parameter:
            p           the point to be interpolated.
        Returns:
            v           list of vertices of the simplex that contains p
            ratio       mixing ratio for the vertices
        """
        which = self.extrapolate_simplex(p)
        simplex = self.simplices[which]
        # choose the first vertex of the simplex as the origin
        origin = self._points[simplex[0]]
        # position of p relative to origin
        rel_p = p - origin
        # relative positions of the vextices of the simplex
        other_vertices = self._points[simplex[1:]] - origin
        ratio = np.zeros(self.ndim + 1)
        ratio[1:] = rel_p @ np.linalg.inv(other_vertices)
        ratio[0] = 1 - np.sum(ratio[1:])

        return simplex, ratio

    def extrapolate_simplices(self, p):
        """
        A collective version of extrapolate_simplex
        """
        A = self.planes[:, :-2] @ p.T
        B = self.planes[:, -1] - A.T
        z = B / self.planes[:, -2]
        which = np.argmax(z, axis=1)
        return which

    def mixratios(self, p):
        """
        A collective version of mixratio.

        Parameter:
            p           the pointS to be interpolated.
        Returns:
            v           a list of list of vertices of the simplex that contains p
            ratio       mixing ratioS for the vertices
        """
        which = self.extrapolate_simplices(p)
        # それぞれのsimplexでoriginを定める。
        origins = self._points[self.simplices[:, 0]]
        ps = np.zeros([self.nsimplex, self.ndim, self.ndim])
        for i in range(self.ndim):
            ps[:, i, :] = self._points[self.simplices[:, i + 1]] - origins
        psi = np.zeros_like(ps)
        for i in range(self.nsimplex):
            psi[i] = np.linalg.inv(ps[i])
        # position of p relative to origin
        pp = p - origins[which]
        # relative positions of the vextices of the simplex
        ratio = np.zeros([p.shape[0], self.ndim + 1])
        for i in range(p.shape[0]):
            ratio[i, 1:] = pp[i] @ psi[which[i]]
        ratio[:, 0] = 1 - np.sum(ratio[:, 1:], axis=1)
        return self.simplices[which], ratio


if __name__ == "__main__":
    # 代表点。4つだけ。
    points = np.array([[0, -0.1], [0, 1.1], [1.2, 0], [1, 1]])

    # いきなりDelaunay三角形分割
    tri = DelaunayE(points)
    p = np.array([0.5, -0.3])
    # 点pを含む三角形(点が3次元以上の場合は単体)と、それらの混合比
    v, ratio = tri.mixratio(p)
    print(v, ratio)
