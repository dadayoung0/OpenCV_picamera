import cv2
import pyzbar.pyzbar as pyzbar
import numpy as np

import save


# 폰트 정보
FONT_THICK = 2
FONT_SIZE = 1
FONT_COLOR = (200, 0, 200)


# contours 그리기 위한 이미지 보정
def edit_for_contours(img):
    img_blur = cv2.GaussianBlur(img, (11, 11), 1)
    img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
    img_canny = cv2.Canny(img_gray, 20, 30)
    kernel = np.ones((5, 5))
    img_dil = cv2.dilate(img_canny, kernel, iterations=1)
    return img_dil


# 바코드 번호 알아내기 위한 이미지 보정
def edit_for_barcode(img, cnt):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    x1, y1 = np.min(cnt, axis=0)
    x2, y2 = np.max(cnt, axis=0)
    img_cut = img_gray[y1:y2, x1:x2]
    return img_cut


# img 에서 contour 구한 뒤 img_contour 에 contour 그리기
def draw_contours(img_contour, img, area_min):
    # img 에서 contour 찾기
    contours, _ = cv2.findContours(img_contour, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # contour box 좌표 정보
    result = []

    for cnt in contours:
        # contour 영역 구하기
        area = cv2.contourArea(cnt)

        # 최소 영역 이상일 때만 반복문 실행
        if area < area_min:
            continue

        # contour box 좌표 구하기
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # contour box 그리기
        cv2.drawContours(img, [box], -1, (0, 0, 255), 2)

        # contour box 좌표 정보 추가
        result.append(box)

    # contour box 좌표 정보 반환
    return result


# img_contour 에 x, y, z 정보 표시
def draw_xyz(img, xyz):
    cv2.putText(img, "X: "+str(xyz[0])+"cm", (5, 30), cv2.FONT_HERSHEY_COMPLEX, FONT_SIZE, FONT_COLOR, FONT_THICK)
    cv2.putText(img, "Y: "+str(xyz[1])+"cm", (5, 60), cv2.FONT_HERSHEY_COMPLEX, FONT_SIZE, FONT_COLOR, FONT_THICK)
    cv2.putText(img, "Z: "+str(xyz[2])+"cm", (5, 90), cv2.FONT_HERSHEY_COMPLEX, FONT_SIZE, FONT_COLOR, FONT_THICK)


# img 에서 비코드 번호 구한 뒤 img_contour 에 바코드 정보 표시
def draw_barcode(img_barcode, img):
    barcodes = pyzbar.decode(img_barcode)

    cnt = 2
    # 결과 출력(탐지된 코드 타입, 데이터)
    for obj in barcodes:
        if (obj.type == "CODE128") and (len(obj.data.decode('utf-8')) > 9):
            cv2.putText(img, "Type : "+obj.type, (5, (60*cnt)), cv2.FONT_HERSHEY_COMPLEX, FONT_SIZE, FONT_COLOR, FONT_THICK)
            cv2.putText(img, "Data : "+obj.data.decode('utf-8'), (5, (60*cnt)+30), cv2.FONT_HERSHEY_COMPLEX, FONT_SIZE, FONT_COLOR, FONT_THICK)
            print('Type : ', obj.type)
            print('Data : ', obj.data.decode('utf-8'))

            save.barcode_info(obj.data.decode('utf-8'))
            cnt += 1
