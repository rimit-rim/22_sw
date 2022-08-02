import cv2
import datetime
import schedule
import pyautogui
import numpy as np
import pandas as pd
from csv import writer

# time_data.csv (실시간 데이터) 파일 생성 및 초기화
time_df = pd.DataFrame(data={'date': [],
                             'number of people': []})
time_df.to_csv('time_data.csv')

# day_data.csv (일주일 데이터를 시간대별로 저장하는 csv) 초기화 (생성은 하단에)
day_df = pd.DataFrame(data={'weekday': ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'],
                            '00': [0, 0, 0, 0, 0, 0, 0], '01': [0, 0, 0, 0, 0, 0, 0], '02': [0, 0, 0, 0, 0, 0, 0],
                            '03': [0, 0, 0, 0, 0, 0, 0], '04': [0, 0, 0, 0, 0, 0, 0], '05': [0, 0, 0, 0, 0, 0, 0],
                            '06': [0, 0, 0, 0, 0, 0, 0], '07': [0, 0, 0, 0, 0, 0, 0], '08': [0, 0, 0, 0, 0, 0, 0],
                            '09': [0, 0, 0, 0, 0, 0, 0], '10': [0, 0, 0, 0, 0, 0, 0], '11': [0, 0, 0, 0, 0, 0, 0],
                            '12': [0, 0, 0, 0, 0, 0, 0], '13': [0, 0, 0, 0, 0, 0, 0], '14': [0, 0, 0, 0, 0, 0, 0],
                            '15': [0, 0, 0, 0, 0, 0, 0], '16': [0, 0, 0, 0, 0, 0, 0], '17': [0, 0, 0, 0, 0, 0, 0],
                            '18': [0, 0, 0, 0, 0, 0, 0], '19': [0, 0, 0, 0, 0, 0, 0], '20': [0, 0, 0, 0, 0, 0, 0],
                            '21': [0, 0, 0, 0, 0, 0, 0], '22': [0, 0, 0, 0, 0, 0, 0], '23': [0, 0, 0, 0, 0, 0, 0]})

def now_camera():
    # 웹캠에 찍힌 이미지 캡쳐 (C: 캡쳐, Q:강제종료)
    cap = cv2.VideoCapture(0)
    now = datetime.datetime.now().strftime("%m-%d_%H-%M")    # 파일 저장 형식

    # day_data.csv 에 사용될 변수
    weekday = datetime.datetime.today().weekday()
    week_now = datetime.datetime.now().strftime("%H")

    if not cap.isOpened():
        print("camera open failed")
        exit()
    while True:
        ret, img = cap.read()
        if not ret:
            print("Can't read camera")
            break
        cv2.imshow('PC_camera', img)
        # C(캡쳐) 자동 입력 코드 (카메라 딜레이 시간을 고려해 다른 알파벳을 입력해 시간을 벌게 끔 설정함)
        pyautogui.write('esc', interval=1)
        if cv2.waitKey(1) == ord('c'):
            cv2.imwrite("video_capture/" + str(now) + ".jpg", img)
            break
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

    # 이미지를 바탕으로 분류
    # Yolo 로드
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))
    # 이미지 가져오기
    # 이미지 경로) 현재 코드 폴더 > video_capture
    img = cv2.imread("video_capture/" + str(now) + ".jpg")
    img = cv2.resize(img, None, fx=0.4, fy=0.4)
    height, width, channels = img.shape
    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)
    # 정보를 화면에 표시
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if class_id == 0 and confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # 좌표
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    font = cv2.FONT_HERSHEY_PLAIN
    label_count = 0     # label_count = 인원수 카운트
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            label_count += 1
            color = colors[i]
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, label, (x, y + 30), font, 3, color, 3)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # time_data.csv에 데이터 추가
    tmp_data = ['', str(now), label_count]
    with open('time_data.csv', 'a', newline='') as f:
        writer_object = writer(f)
        writer_object.writerow(tmp_data)
        f.close()

    # day_df 데이터 값 변경 후 day_data.csv로 생성
    day_df.at[weekday, week_now] = day_df.at[weekday, week_now] + label_count
    day_df.to_csv('day_data.csv')
    
# schedule.every(N).seconds.do(now_camera) : now_camera 함수를 n초 후 자동 반복
# 컴퓨터 사양에 따라 달라질 수 있으나 여러 딜레이 시간을 고려해 50초로 설정(결론적으론 1분 간격으로 반복)
schedule.every(50).seconds.do(now_camera)

while True:
    schedule.run_pending()
