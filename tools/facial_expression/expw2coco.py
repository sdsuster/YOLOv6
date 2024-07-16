from PIL import Image as PILImage
import os
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from pathlib import Path
import pandas as pd
import shutil
from sklearn.model_selection import KFold


info = {
    "year": 0,
    "version": "1.0",
    "description": "WIDER",
    "contributor": "-",
    "url": "-",
    "date_created": "2017-09-01T00:00:00Z"
}

categories = [{
    "id": 1,
    "name": "face",
    "supercategory": "face"
}]

def convert(expw_split_annotation_path, expw_folder, expw_new_folder, expw_label_folder):
    df = pd.read_csv(expw_split_annotation_path)
    shutil.rmtree(expw_new_folder, ignore_errors=True)
    shutil.rmtree(expw_label_folder, ignore_errors=True)

    for (i, row) in df.iterrows():
        file_name = row['image_name']
        print(f'processing {i/len(df.index)}% {file_name}')
        file_path = os.path.join(expw_folder, file_name)
        target_file_path = os.path.join(expw_new_folder, file_name)
        path = Path(target_file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(file_path, target_file_path)

        img = PILImage.open(file_path)
        base_name, _ = os.path.splitext(file_name)
        label_name = os.path.join(expw_label_folder, f'{base_name}.txt')

        path = Path(label_name)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(label_name, 'a') as labelfile:
            x = int(row['face_box_left'])
            y = int(row['face_box_top'])
            w = int(row['face_box_right']) - x
            h = int(row['face_box_bottom']) - y
            label = int(row['label'])

            labelfile.write(f'{label} {(x + w/2)/img.width} {(y + h/2)/img.height} {w/img.width} {h/img.height}\n')
            labelfile.close()

def split_train_val(image_folder, label_folder, train_folder, val_folder):
    files = os.listdir(image_folder)
    files = [os.path.splitext(file_name)[0] for file_name in files]
    kf = KFold(n_splits=5, shuffle=True, random_state=42)

    
    os.makedirs(os.path.join(val_folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(val_folder, 'label'), exist_ok=True)

    os.makedirs(os.path.join(train_folder, 'images'), exist_ok=True)
    os.makedirs(os.path.join(train_folder, 'label'), exist_ok=True)

    for train, val in kf.split(files):
        for i in val:
            file = files[i]
            image_path = os.path.join(image_folder, f'{file}.jpg')
            label_path = os.path.join(label_folder, f'{file}.txt')
            target_image_path = os.path.join(val_folder, 'images', f'{file}.jpg')
            target_label_path = os.path.join(val_folder, 'label', f'{file}.txt')
            shutil.move(image_path, target_image_path)
            shutil.move(label_path, target_label_path)

        for i in train:
            file = files[i]
            image_path = os.path.join(image_folder, f'{file}.jpg')
            label_path = os.path.join(label_folder, f'{file}.txt')
            target_image_path = os.path.join(train_folder, 'images', f'{file}.jpg')
            target_label_path = os.path.join(train_folder, 'label', f'{file}.txt')
            shutil.move(image_path, target_image_path)
            shutil.move(label_path, target_label_path)
        break


if __name__ == '__main__':
    print("Converting")
    convert('D:\\Datasets\\Exp-W\\data\\label\\label.csv', 'D:\\Datasets\\Exp-W\\data\\image\\origin', 'D:\\Datasets\\Exp-W\\data\\origin\\images', 'D:\\Datasets\\Exp-W\\data\\origin\\labels')
    split_train_val('D:\\Datasets\\Exp-W\\data\\origin\\images', 'D:\\Datasets\\Exp-W\\data\\origin\\labels', 'D:\\Datasets\\Exp-W\\data\\train', 'D:\\Datasets\\Exp-W\\data\\val')
    print("Done")