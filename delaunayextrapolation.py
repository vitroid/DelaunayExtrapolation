from scipy.spatial import Delaunay
import numpy as np

def plane(p):
    # ax+by+cz+e=1を満足するabceを求める。
    # (x,y,z,1) @ (a,b,c,e) = 1
    # pseudo-inverse matrix?
    q = np.zeros([p.shape[0], p.shape[1]+1])
    q[:,:-1] = p
    q[:, -1] = 1
    qplus = q.T @ np.linalg.inv(q @ q.T)
    abce = qplus @ np.ones(q.shape[0])
    # ax+by+cz = 1-e = d
    abcd = abce.copy()
    abcd[-1] = 1 - abce[-1]
    return abcd


class DelaunayE(Delaunay):
    def __init__(self, *args, **kwarg):
        super().__init__(*args, **kwarg)
        # 次元を上げる。2次元なら3次元にする。
        pulledup = np.zeros([self._points.shape[0], self._points.shape[1]+1])
        # 2次元まではそのままコピー
        pulledup[:,:-1] = self._points
        # 3次元目には、二乗和を入れる。
        pulledup[:, -1] = np.sum(pulledup[:]**2, axis=1)

        self.planes = np.zeros([self.nsimplex, self.ndim+2])
        for i, simplex in enumerate(self.simplices):
            # simplexの3点を通る方程式を定める。
            # ax+by+cz=d を3つの点のいずれでも満たすようなa,b,c,dを求めたい。
            abcd = plane(pulledup[simplex])
            self.planes[i] = abcd

    def extrapolate_simplex(self, p):
        z = (self.planes[:, -1] - self.planes[:, :-2] @ p) / self.planes[:,-2]
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
        # choose the first vertex of the simplex as the origin
        origin = self._points[self.simplices[which][0]]
        # position of p relative to origin
        pp = p - origin
        # relative positions of the vextices of the simplex
        ps = self._points[self.simplices[which][1:]] - origin
        ratio = np.zeros(self.ndim+1)
        ratio[1:] = pp @ np.linalg.inv(ps)
        ratio[0]  = 1 - np.sum(ratio[1:])
        return self.simplices[which], ratio


if __name__ == "__main__":
    # 代表点。4つだけ。
    points = np.array([[0, -0.1], [0, 1.1], [1.2, 0], [1, 1]])

    # いきなりDelaunay三角形分割
    tri = DelaunayE(points)
    p = np.array([0.5, 0.7])
    # 点pを含む三角形(点が3次元以上の場合は単体)と、それらの混合比
    v, ratio = tri.mixratio(p)
    print(v, ratio)
