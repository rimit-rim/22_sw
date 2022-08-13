# 22_sw
### 코드 실행 전 깔아야 하는 모듈
- cv2(openCV) : pip install opencv-python
- datetime : pip install datetime
- schedule : pip install schedule
- pyautogui : pip install pyautogui
- numpy : pip install numpy
- pandas : pip install pandas
- csv : pip install csv

### 유의사항
- yolov3.weights의 경우 전에 공유했던 파일 사용하시면 됩니다! (첨부된 coco.names, yolov3.cfg 파일도 전과 동일한 파일)
- 코드 파일 경로 내에 이미지를 저장하는 폴더 경로<b>(/video_caputre)</b>가 반드시 있어야 합니다.
- csv 파일의 경우 코드를 실행하면 자동으로 생성 됩니다.
- <b>층별로 수용인원이 다르기 때문에, main.py code line 111~117의 코드 숫자를 층에 맞게 바꿔주면 됩니다. </b> 
  - 7층(72석) / 6, 5, 4층(56석) / 3층(65석) / 2층(약 12석) / 1층(58석)
- 코드에 대한 설명은 주석을 참고해주세요.

### 저장되는 csv파일
- time_data : 분 단위로 인원수, 사용률, 상태가 저장되는 csv파일
  - 여유: 40% 미만 / 보통: 40~75% / 혼잡 75%
![1](https://user-images.githubusercontent.com/86980164/183939597-8084fa22-a4ee-4c13-9cda-419ea430dbe8.png)

- day_data : 일주일(시간대별로) 데이터가 찍히는 csv
![2](https://user-images.githubusercontent.com/86980164/183939609-0b414aa8-6823-49b4-a0e6-642b93394e0b.png)

### 실행영상
https://user-images.githubusercontent.com/86980164/184469237-6a3f92a9-011a-46b6-8ded-7f7bffabda88.mp4
