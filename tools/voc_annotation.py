import os
import random
import xml.etree.ElementTree as ET

from utils.utils import get_classes

# --------------------------------------------------------------------------------------------------------------------------------#
#   annotation_mode用于指定该文件运行时计算的内容
#   annotation_mode为0代表整个标签处理过程，包括获得VOCdevkit/VOC2007/ImageSets里面的txt以及训练用的2007_train.txt、2007_val.txt
#   annotation_mode为1代表获得VOCdevkit/VOC2007/ImageSets里面的txt
#   annotation_mode为2代表获得训练用的2007_train.txt、2007_val.txt
# --------------------------------------------------------------------------------------------------------------------------------#
annotation_mode = 0
# -------------------------------------------------------------------#
#   必须要修改，用于生成2007_train.txt、2007_val.txt的目标信息
#   与训练和预测所用的classes_path一致即可
#   如果生成的2007_train.txt里面没有目标信息
#   那么就是因为classes没有设定正确
#   仅在annotation_mode为0和2的时候有效
# -------------------------------------------------------------------#
classes_path = '/data/waterscenes/Achelous_format/classes.txt'
# --------------------------------------------------------------------------------------------------------------------------------#
#   trainval_percent用于指定(训练集+验证集)与测试集的比例，默认情况下 (训练集+验证集):测试集 = 9:1
#   train_percent用于指定(训练集+验证集)中训练集与验证集的比例，默认情况下 训练集:验证集 = 9:1
#   仅在annotation_mode为0和1的时候有效
# --------------------------------------------------------------------------------------------------------------------------------#
trainval_percent = 0.8
train_percent = 0.8
# -------------------------------------------------------#
#   指向VOC数据集所在的文件夹
#   默认指向根目录下的VOC数据集
# -------------------------------------------------------#
Annotation_path = "/data/waterscenes/detection/all/Annotations"
out_path = "/data/waterscenes/Achelous_format"

classes, _ = get_classes(classes_path)


def convert_annotation(image_id, list_file):
    # print(year)
    # print(image_id)
    in_file = open(os.path.join(Annotation_path, '%s.xml' % (image_id)), encoding='utf-8')
    tree = ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = 0
        if obj.find('difficult') != None:
            difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(float(xmlbox.find('xmin').text)), int(float(xmlbox.find('ymin').text)),
             int(float(xmlbox.find('xmax').text)), int(float(xmlbox.find('ymax').text)))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))


if __name__ == "__main__":

    # train_list = open(os.path.join(out_path, 'train.txt'), encoding='utf-8')
    list_file = open(os.path.join(out_path, 'test_list.txt'), 'w', encoding='utf-8')
    with open(os.path.join(out_path, 'test.txt'), "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            print(line)
            timestamp = line[-20:-4]
            print(timestamp)

            list_file.write('/data/waterscenes/all/image/%s.jpg' % (timestamp))
            convert_annotation(timestamp, list_file)
            list_file.write('\n')





