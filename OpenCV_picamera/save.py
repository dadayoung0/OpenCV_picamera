import urllib.request
import json


def barcode_info(barcode):
    api_url = 'https://apis.tracker.delivery/carriers/kr.cjlogistics/tracks/'
    url = api_url + barcode

    # 바코드 정보 저장할 파일 불러오기
    f = open('barcode.txt', 'a')

    # url 통신하기
    response = urllib.request.urlopen(url)
    response_message = response.read().decode('utf8')

    if response_message:
        data = json.loads(response_message)

        # 보내는 사람
        get_data = data.get('from')
        f.write("보내는 사람 : " + get_data.get('name') + "(" + get_data.get('time') + ")\n")

        # 받는 사람
        get_data = data.get('to')
        f.write("받는 사람 : " + get_data.get('name') + "(" + get_data.get('time') + ")\n")

        # 상품 상태
        f.write("상품 상태 : " + data.get('state').get('text') + "\n")

        # 진행 상황
        # get_data = data.get('progresses')
        # f.write("진행 상황" + "\n")
        # print(get_data)

        # 배달사
        get_data = data.get('carrier')
        f.write("배달사 : " + get_data.get('name') + "(" + get_data.get('tel') + ")\n")

    f.close()
