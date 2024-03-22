import re


f = open('E:/datasets/slowfast_ufc/0.mp4_point', 'r')
data = f.read()
data = re.findall(r'(?<=Set cut point )\w+', data)
print(data)
f.close()
f = open('E:/datasets/slowfast_ufc/0.mp4_point', 'w')
for point in data:
    f.write(point)
    f.write('\n')
f.close()
