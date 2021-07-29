import math


# 점과 점 사이의 거리 구하는 함수
def distance(cnt):
    center1 = center_point(cnt[0], cnt[1])
    center2 = center_point(cnt[2], cnt[3])
    result = math.sqrt(math.pow(center1[0] - center2[0], 2) +
                       math.pow(center1[1] - center2[1], 2))
    return result


# 가운데 점을 구해주는 함수
def center_point(point1, point2):
    center_x = (point1[0] + point2[0]) / 2.0
    center_y = (point1[1] + point2[1]) / 2.0
    return [center_x, center_y]
