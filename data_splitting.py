"""
Data pre-processing part. Splits the entire train/val datasets by different image scenes:
    Scene_1 (train.txt / val.txt)
    Scene_2 (train.txt / val.txt)
    ...

Scene names are defined by CLS_SCENE in opt.py

Usage:
    python data_splitting.py --data_root <path/to/data/root>
                             --scene_lbls <path/to/file/with/scene/labels>
                             --tsk <str>
                             --res_dir <path/to/folder/where/to/save/results>

"""

import argparse
import pandas as pd
from pathlib import Path
import numpy as np

import opt


def make_dir(dir):
    if not dir.exists():
        dir.mkdir(parents=True)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_root', action='store', default='data', help='Path to data root')
    parser.add_argument('--scene_lbls', action='store', default='data/scene_labels.csv',
                        help='Path to image scene labels')
    parser.add_argument('--tsk', action='store', default='airport',
                        help='The column name with labels in scene_lbls file')
    parser.add_argument('--res_dir', action='store', default='data/splits',
                        help='Path to save split results')

    args = parser.parse_args()
    return args


def make_split_dirs(res_root, classes):
    for cls in classes:
        make_dir(res_root / cls)


def make_split(data, phase, cls, scene_lbls, tsk):
    cls_hashes = scene_lbls.loc[scene_lbls[tsk] == cls, 'hash'].values
    cls_files = []
    for f in data.values:
        fhash = Path(f[0]).stem.split('_')[0]
        fname = Path(f[0]).name
        if fhash in cls_hashes:
            cls_files.append(fname)

    return cls_files


if __name__ == '__main__':
    args = parse_args()
    data_root = Path(args.data_root)
    res_root = Path(args.res_dir)
    scene_lbl_file = args.scene_lbls

    train_txt = data_root/'train.txt'
    val_txt = data_root/'val.txt'

    train_split = pd.read_csv(train_txt, header=None)
    val_split = pd.read_csv(val_txt, header=None)

    scene_lbls = pd.read_csv(scene_lbl_file, sep=';')

    make_split_dirs(res_root, opt.CLS_SCENE)

    for phase, data in zip(['train', 'val'], [train_split, val_split]):
        num_images_per_cls = np.zeros(len(opt.CLS_SCENE))
        for i, cls in enumerate(opt.CLS_SCENE):
            cls_files = make_split(data, phase, cls, scene_lbls, args.tsk)
            num_images_per_cls[i] = len(cls_files)
            with open(res_root / cls / f'{phase}.txt', 'w') as f:
                f.write('\n'.join(cls_files))

        # Statistics
        with open(res_root/f'statistics_{phase}.txt', 'w') as f:
            for i, cls in enumerate(opt.CLS_SCENE):
                f.write(f'{cls}: {num_images_per_cls[i]} ({(num_images_per_cls[i] / num_images_per_cls.sum())*100:.2f}%)\n')
            f.write('----------------------\n')
            f.write(f'total: {num_images_per_cls.sum()}\n')




