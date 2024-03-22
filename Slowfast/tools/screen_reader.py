import numpy as np
import pyautogui
import cv2
import time


out_dir = 'D:/git/temp/videos'
out_path = f"{out_dir}/{int(time.time())}.mp4"
print(out_path)
h, w, c = np.array(pyautogui.screenshot()).shape
video_writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*'mp4v'), 20, (w, h))
print('Start!')
while True:
    frame = pyautogui.screenshot()
    frame = np.array(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video_writer.write(frame)
    # cv2.imshow('screen', frame)
    key = cv2.waitKey(1)
    # time.sleep(0.03)
    if key == ord('q'):
        break
video_writer.release()
