from PIL import Image as PILImage
import os
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from pathlib import Path
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
 
class Image():
    def __init__(self, id, width, height, file_name) -> None:
         self.id = id
         self.width = width
         self.height = height
         self.flickr_url = '-'
         self.license = '-'
         self.coco_url = 1
         self.date_captured = "2017-01-01 00:00:00"
         self.file_name = file_name

class Annot():
     def __init__(self, id, image_id, category_id, bbox, blurness) -> None:
          self.id = id
          self.image_id = image_id
          self.category_id = category_id
          self.bbox = bbox
          self.segmentation = []
          self.area = 0
          self.blurness = blurness
          self.iscrowd = 0

def convert(wider_split_annotation_path, wider_folder, wider_label_folder):
    with open(wider_split_annotation_path) as f:
        image_id = 0
        annot_id = 0
        images = []
        annots = []
        while True:

            # Get next line from file
            file_name = f.readline().replace('\n', '')

            # if line is empty
            # end of file is reached
            if not file_name:
                break

            image_id += 1

            img = PILImage.open(os.path.join(wider_folder, file_name))

            base_name, _ = os.path.splitext(file_name)
            label_name = os.path.join(wider_label_folder, f'{base_name}.txt')

            path = Path(label_name)
            # Create the directories recursively
            path.parent.mkdir(parents=True, exist_ok=True)

            images.append(
                Image(image_id, img.width, img.height, file_name).__dict__
            )
            # fig, ax = plt.subplots()
            # ax.imshow(img)
            n = int(f.readline())
            with open(label_name, 'w') as labelfile:
                
                for i in range(n):
                    annot_id += 1
                    bbox = f.readline().split(' ')

                    x = int(bbox[0])
                    y = int(bbox[1])
                    w = int(bbox[2])
                    h = int(bbox[3])
                    blurness = int(bbox[4])

                    
                    # rect = patches.Rectangle((x, y), w, h, linewidth=2, edgecolor='r', facecolor='none')
                    # ax.add_patch(rect)
                    # annots.append(Annot(annot_id, image_id, 1, [x/img.width, y/img.height, w/img.width, h/img.height], blurness).__dict__)
                    annots.append(Annot(annot_id, image_id, 1, [x/img.width, y/img.height, w/img.width, h/img.height], blurness).__dict__)
                    labelfile.write(f'0 {(x + w/2)/img.width} {(y + h/2)/img.height} {w/img.width} {h/img.height}\n')
                
                labelfile.close()
            if n == 0:
                f.readline()


        # obj = {
        #     "info": info,
        #     "categories": categories,
        #     "images": images,
        #     "annotations": annots
        # }
        # import json
        # with open('data.json', 'w') as a:
        #     json.dump(obj, a)

if __name__ == '__main__':
    print("Converting")
    convert('D:\\Datasets\\WIDER\\wider_face_split\\wider_face_train_bbx_gt.txt', 'D:\\Datasets\\WIDER\\WIDER_train\\images', 'D:\\Datasets\\WIDER\\WIDER_train\\labels')
    convert('D:\\Datasets\\WIDER\\wider_face_split\\wider_face_val_bbx_gt.txt', 'D:\\Datasets\\WIDER\\WIDER_val\\images', 'D:\\Datasets\\WIDER\\WIDER_val\\labels')
    # convert('D:\\Datasets\\WIDER\\wider_face_split\\wider_face_test_bbx_gt.txt', 'D:\\Datasets\\WIDER\\WIDER_test\\images', 'D:\\Datasets\\WIDER\\WIDER_test\\labels')
    print("Done")