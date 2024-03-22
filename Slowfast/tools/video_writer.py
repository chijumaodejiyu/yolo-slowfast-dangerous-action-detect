# -*-coding:utf-8-*-
import datetime
import time
import cv2
import os

cap = cv2.VideoCapture(0)
time_now = time.time()
os.makedirs('capture', exist_ok=True)

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
time_str = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
video_path = 'capture/' + time_str + '.mp4'
video_out = cv2.VideoWriter(video_path, fourcc, 30.0, (640, 480))
print(f"Save to {video_path}.")

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1)
    if video_out:
        video_out.write(frame)
    cv2.imshow("Video", frame)

    if cv2.waitKey(1) == ord('q'):
        cap.release()
        video_out.release()
        break
