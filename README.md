# DelaunayExtrapolation

## Explanation

Delaunay三角形分割を利用した内挿法です。

1. 点群をまず準備します。
2. それをDelaunay三角形分割します。
3. 点群に含まれない任意の点が、点群の構成する三角形のどれに含まれているかを割り出します。
4. さらに、三角形の中での相対位置(混合比)を算出します。

`scipy.spatial.Delaunay`を利用すれば内挿は容易にできますが、三角形に含まれない点にまで外挿することができないので、Delaunayクラスを拡張しました。

「三角形分割」と書いていますが、3次元以上でも問題なく動くはずです。

## Installation

```shell
$ pip install delaunayextrapolation
```

## Example

`test.py`に使用例があります。

## Known Issues

* 一点ずつしか内挿できません。多数の点を同時に内挿できると良いですよね。
