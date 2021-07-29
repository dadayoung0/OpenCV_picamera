import board
import busio
import adafruit_vl53l0x

import time

from graphic import *
from calculate import *


# 동영상 해상도
FRAME_W = 2592
FRAME_H = 1944
FPS = 10

# 기본 높이
STAND_H = 57

# 잘라낼 수치
CUT_X1 = 500
CUT_X2 = 2150
CUT_Y1 = 400
CUT_Y2 = 1650


class Measure:
    # 초기화
    def __init__(self):
        # 카메라
        self.cap = cv2.VideoCapture(-1)
        self.cap.set(3, FRAME_W)
        self.cap.set(4, FRAME_H)
        self.prev_time = 0
        self.current_time = 0

        # 레이저
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vl53l0x.VL53L0X(i2c)

    # 센서로 거리 측정하여 정수 형태로 반환
    def get_distance(self):
        # 거리 측정
        d = self.sensor.range / 10

        # 보정 계수 적용
        if 30 < d < 50:
            d = (d + 11) * 0.77
        elif 50 < d < STAND_H:
            d = (d - 11) * 1.2

        return int(d)

    # 가로, 세로, 높이 구하기
    def get_xyz(self, cnt):
        # 높이 구하기
        d = self.get_distance()

        # 정렬하기
        sort_x = sorted(cnt, key=lambda x: x[0])
        sort_y = sorted(cnt, key=lambda x: x[1])

        # 가로, 세로, 높이 구하기
        x = int(distance(sort_x) * d / 2168)
        y = int(distance(sort_y) * d / 2168)
        z = int(STAND_H - d)

        return [x, y, z]

    # 결과 출력
    def get_result(self):
        # 상품 정보 저장
        # obj_result = [0, 0, 0]
        # result_count = 0

        while True:
            self.current_time = time.time() - self.prev_time

            if self.current_time > 1.0 / FPS:
                self.prev_time = time.time()

                # 영상을 이미지로 읽어오기
                _, img = self.cap.read()
                img = img[CUT_Y1:CUT_Y2, CUT_X1:CUT_X2]

                # img 에 contours 그리기
                img_contour = edit_for_contours(img)
                contours = draw_contours(img_contour, img, 50000)

                if len(contours) != 0:
                    # contours 1개씩 반복
                    for cnt in contours:
                        # img 에 x, y, z 정보 표시
                        xyz = self.get_xyz(cnt)
                        draw_xyz(img, xyz)

                        if np.all(cnt > 0):
                            # img 에 바코드 정보 표시
                            img_barcode = edit_for_barcode(img, cnt)
                            draw_barcode(img_barcode, img)

                # img 출력
                img_re = cv2.resize(img, (0, 0), None, 0.5, 0.5)
                cv2.imshow("Result", img_re)

            if cv2.waitKey(1) & 0xff == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
