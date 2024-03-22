import os
import numpy as np
os.system('chcp 65001')  # 将cmd的显示字符编码从默认的GBK改为UTF-8


input_path = 'E:/datasets/ava/videos/need.txt'
output_dir = 'E:/datasets/ava/videos'

if not os.path.exists(output_dir):
    os.mkdir(output_dir)


f = open(input_path, 'r')
content = f.read()
video_ids = content.strip().split('\n')
for video_id in video_ids:
    url = f'https://s3.amazonaws.com/ava-dataset/trainval/{video_id}'
    print(f'Get video from {url}')
    os.system(f'wget {url} -P {output_dir}')
