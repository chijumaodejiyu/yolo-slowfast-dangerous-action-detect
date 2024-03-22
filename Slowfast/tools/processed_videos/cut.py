import cv2
import numpy as np
import re
import os


def check_out_dir(out_path):
    if os.path.exists(out_path):
        return
    check_out_dir(re.findall(r'.*(?=/)', out_path)[0])
    os.mkdir(out_path)
    return


def set_point(target_path, output_path=None, speed=2):
    cap = cv2.VideoCapture(target_path)

    if output_path is None:
        output_path = target_path + '_point'

    fps = cap.get(cv2.CAP_PROP_FPS)
    # fps = 30
    count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    step = int(1000 / fps / speed)
    filename = target_path.split('/')[-1]
    cut_points = []
    f_num = 0

    while f_num <= count:
        ret, frame = cap.read()
        if not ret:
            print("Can't read frame.")
            break
        f_num += 1
        cv2.imshow(filename, frame)
        key = cv2.waitKey(step)
        if key == ord(' '):
            point = f_num/fps
            cut_points.append(point)
            print(f'Set cut point {f_num/fps}')
        elif key == ord('q'):
            break

    f = open(output_path, 'w')
    for point in cut_points:
        f.write(str(point))
        f.write('\n')

    cap.release()
    f.close()
    return cut_points


def cut(target_path, points):
    filename = re.findall(r'.*?(?=\.)', target_path.split('/')[-1])[0]
    out_dir = re.findall(r'.*(?=\.)', target_path)[0]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    for index in range(1, len(points)):
        outfile_path = f'{out_dir}/{index:05d}.mp4'
        point0 = int(float(points[index-1]))
        point1 = int(float(points[index]))
        order = f'ffmpeg -ss {point0} -to {point1} -i "{target_path}" "{outfile_path}"'
        print(order)
        os.system(order)


def to_frames(target_path):
    if os.path.isfile(target_path):
        target_dir = re.findall(r'.*(?=/)', target_path)[0]
        filenames = re.findall(r'(?=/).*?')[-1]
    else:
        target_dir = target_path
        filenames = os.listdir(target_dir)
    for filename in filenames:
        filepath = f'{target_dir}/{filename}'
        check_out_dir(filepath)



target_file = "E:/datasets/ava_datasets/test.mp4"
point = range(0, 80, 3)

# points_path = target_file + '_point'
# f = open(points_path, 'r')
# point = f.read().strip().split('\n')
# point = ['0'] + point
print(point)
cut(target_file, point)
# target_dir = "E:\datasets\slowfast_ufc\videos"

