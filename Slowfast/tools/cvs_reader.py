import numpy as np
import os


def read_csv(path, separator=',') -> list:
    f = open(path, 'r')
    content = f.read()
    content = content.strip()
    lines = content.split('\n')
    out = []
    for line in lines:
        out.append(line.split(separator))
        l = len(out)
        if l % 100000 == 0:
            print(f'Read {l} lines.')

    f.close()
    return out


def write_csv(path, data: np.ndarray, separator=',') -> bool:
    f = open(path, 'w')
    for items in data:
        for item in items[:-1]:
            f.write(str(item) + separator)
        f.write(str(items[-1]) + '\n')
    f.close()
    return True


def _sift_video_ids(data, action_ids):
    out_video_ids = {}

    for line in data:
        if line[6] in action_ids:
            if line[0] in out_video_ids.keys():
                out_video_ids[line[0]] += 1
            else:
                out_video_ids[line[0]] = 1

    return out_video_ids


def get_out_video_ids(inpath, out_action_ids):
    train_inpath = inpath + '/ava_train_v2.2.csv'
    val_inpath = inpath + '/ava_val_v2.2.csv'

    train_data = read_csv(train_inpath)
    val_data = read_csv(val_inpath)

    train_out_video_ids = _sift_video_ids(train_data, out_action_ids)
    val_out_video_ids = _sift_video_ids(val_data, out_action_ids)

    out_video_ids = train_out_video_ids | val_out_video_ids

    print(f'Have found {len(out_video_ids)} videos.')

    return out_video_ids


def _processed_ava_train(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath)
    for line in data:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv)

    return out_csv


def _processed_ava_val(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath)
    for line in data:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv)

    return out_csv


def _processed_train(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath, separator=' ')
    out_csv.append(data[0])
    for line in data[1:]:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv, separator=' ')

    return out_csv


def _processed_val(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath, separator=' ')
    out_csv.append(data[0])
    for line in data[1:]:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv, separator=' ')

    return out_csv


def _processed_ava_train_predicted(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath)
    for line in data:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv)

    return out_csv


def _processed_ava_val_predicted(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath)
    for line in data:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv)

    return out_csv


def _processed_ava_train_excluded_timestamps(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath)
    for line in data:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv)

    return out_csv


def _processed_ava_val_excluded_timestamps(filepath, out_path, out_video_ids):
    out_csv = []
    data = read_csv(filepath)
    for line in data:
        if line[0] in out_video_ids:
            out_csv.append(line)
    out_csv = np.array(out_csv)

    write_csv(out_path, out_csv)

    return out_csv


def _processed_move(filepath, out_path, out_video_ids):
    s = f"move \"{filepath}\" \"{out_path}\""
    print(s)
    os.system(s)

    return None


def generate_data(base_dir, output_dir, video_ids=None, processed_defs=None):
    """

    Args:
        base_dir: path of base data
        output_dir: path of out data
        video_ids: names of needed videos
        data_struct: structure of data

    Returns:

    """
    annotations_path = base_dir + '/' + 'annotations'
    out_annotations_path = output_dir + '/' + 'annotations'
    frame_list_path = base_dir + '/' + 'frame_list'
    out_frame_list_path = output_dir + '/' + 'frame_list'
    frames_path = base_dir + '/' + 'frames'
    out_frames_path = output_dir + '/' + 'frames'

    if video_ids is None:
        video_ids = frames2video_ids(frames_path)

    if processed_defs is None:
        processed_defs = {'train.csv': _processed_train,
                          'val.csv': _processed_val,
                          'ava_train_v2.2.csv': _processed_ava_train,
                          'ava_val_v2.2.csv': _processed_ava_val,
                          'ava_train_predicted_boxes.csv': _processed_ava_train_predicted,
                          'ava_val_predicted_boxes.csv': _processed_ava_val_predicted,
                          'ava_train_excluded_timestamps_v2.2.csv': _processed_ava_train_excluded_timestamps,
                          'ava_val_excluded_timestamps_v2.2.csv': _processed_ava_val_excluded_timestamps,
                          'ava_action_list_v2.2.pbtxt': _processed_copy,
                          'ava_action_list_v2.2_for_activitynet_2019.pbtxt': _processed_copy}
    if not os.path.exists(out_annotations_path):
        os.mkdir(out_annotations_path)
    # processed annotations
    for filename in os.listdir(annotations_path):
        filepath = annotations_path + '/' + filename
        out_path = out_annotations_path + '/' + filename
        processed_def = processed_defs[filename]
        print(f'Processed {filepath} and write it to {out_path}.')
        processed_def(filepath, out_path, video_ids)
        print(f'Finished.')
    if not os.path.exists(out_frame_list_path):
        os.mkdir(out_frame_list_path)
    # processed frame_list
    for filename in os.listdir(frame_list_path):
        filepath = frame_list_path + '/' + filename
        out_path = out_frame_list_path + '/' + filename
        processed_def = processed_defs[filename]
        print(f'Processed {filepath} and write it to {out_path}.')
        processed_def(filepath, out_path, video_ids)
        print(f'Finished.')
    if not os.path.exists(out_frames_path):
        os.mkdir(out_frames_path)
    # processed frames
    for filename in os.listdir(frames_path):
        filepath = frames_path + '/' + filename
        out_path = out_frames_path + '/' + filename
        processed_def = _processed_copy
        print(f'Processed {filepath} and write it to {out_path}.')
        if filename in video_ids:
            processed_def(filepath, out_path)
        print(f'Finished.')


def processed(base_dir, output_dir, video_ids=None):
    annotations_inpath = base_dir + '/annotations'
    frame_list_inpath = base_dir + '/frame_list'
    annotations_outpath = output_dir + '/annotations'
    frame_list_outpath = output_dir + '/frame_list'

    if not os.path.exists(annotations_outpath):
        os.mkdir(annotations_outpath)
    if not os.path.exists(frame_list_outpath):
        os.mkdir(frame_list_outpath)

    if video_ids is None:
        video_ids = np.array(['XF87VL5T0aA'])
    print(video_ids)
    processed_defs = {'train.csv': _processed_train,
                      'val.csv': _processed_val,
                      'ava_train_v2.2.csv': _processed_ava_train,
                      'ava_val_v2.2.csv': _processed_ava_val,
                      'ava_train_predicted_boxes.csv': _processed_ava_train_predicted,
                      'ava_val_predicted_boxes.csv': _processed_ava_val_predicted,
                      'ava_train_excluded_timestamps_v2.2.csv': _processed_ava_train_excluded_timestamps,
                      'ava_val_excluded_timestamps_v2.2.csv': _processed_ava_val_excluded_timestamps,}
    processed_filenames = np.array(list(processed_defs.keys()))
    for filename in os.listdir(frame_list_inpath):
        if filename in processed_filenames:
            filepath = frame_list_inpath + "/" + filename
            outpath = frame_list_outpath + "/" + filename
            processed_defs[filename](filepath, outpath, video_ids)
    for filename in os.listdir(annotations_inpath):
        if filename in processed_filenames:
            filepath = annotations_inpath + "/" + filename
            outpath = annotations_outpath + "/" + filename
            processed_defs[filename](filepath, outpath, video_ids)


def make_test_dir(input_dir, output_dir):
    input_dir = '../AVA'
    output_dir = '../ava_test'
    filenames = ['train.csv', 'val.csv',
                 'ava_train_v2.2.csv', 'ava_val_v2.2.csv',
                 'ava_train_predicted_boxes.csv', 'ava_val_predicted_boxes.csv',
                 'ava_train_excluded_timestamps_v2.2.csv', 'ava_val_excluded_timestamps_v2.2.csv']
    for filename in filenames[: 2]:
        filepath = input_dir + '/' + filename
        out_path = output_dir + '/' + filename

        data = read_csv(filepath, separator=' ')[: 3]
        write_csv(out_path, data, separator=' ')

    for filename in filenames[2:]:
        filepath = input_dir + '/' + filename
        out_path = output_dir + '/' + filename

        data = read_csv(filepath)[: 3]
        write_csv(out_path, data)


def frames2video_ids(target_dir):
    filenames = os.listdir(target_dir)
    return filenames


if __name__ == '__main__':
    os.system('chcp 65001')  # 将cmd的显示字符编码从默认的GBK改为UTF-8
    input_dir = 'D:/git/temp/ava'
    output_dir = 'D:/git/temp/ava_l'
    # action_ids = ['64']
    # video_number = 7
    #
    # data = read_csv(input_dir + '/annotations/ava_train_v2.2.csv')
    # video_dicts = _sift_video_ids(data, action_ids)
    # video_ids = np.array(list(video_dicts.keys()))
    # video_nums = np.array(list(video_dicts.values()))
    # args = np.argsort(video_nums)
    # video_ids = np.array([video_ids[index] for index in args[-video_number:]])
    # print(video_ids)
    # write_csv('./temp.csv', video_ids[:, np.newaxis])
    # target_dir = ''
    # out_dir = ''
    # if not os.path.exists(out_dir):
    #     os.mkdir(out_dir)
    # video_ids = np.array(read_csv('./temp.csv')).flatten()
    # for filename in os.listdir(target_dir):
    #     if filename in video_ids:
    #         target_path = target_dir + f'/{filename}'
    #         out_path = out_dir + f'/{filename}'
    #         print(f'Move {target_path} to {out_path}.')
    #         _processed_move(target_path, out_path)
    processed(input_dir, output_dir)
