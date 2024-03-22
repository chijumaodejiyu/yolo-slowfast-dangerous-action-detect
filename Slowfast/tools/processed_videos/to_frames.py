import os
import re


target_dir = 'E:/datasets/ava_datasets/test'
out_dir = 'E:/datasets/ava_datasets/frames'

filenames = os.listdir(target_dir)
# out_dir = re.findall(r'.*?/', target_dir)[0] + 'frames'
print(out_dir)
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

for filename in filenames:
    filepath = f'{target_dir}/{filename}'
    temp = filename.split('.')[0]
    frames_dir = f'{out_dir}/{temp}'
    if not os.path.exists(frames_dir):
        os.mkdir(frames_dir)
    order = f'ffmpeg -i {filepath} -r 30 "{frames_dir}/{temp}_%06d.jpg"'
    print(order)
    os.system(order)
