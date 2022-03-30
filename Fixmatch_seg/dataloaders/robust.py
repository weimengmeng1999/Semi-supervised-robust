from base import BaseDataSet, BaseDataLoader
from utils import pallete
import numpy as np
import os
import scipy
import torch
from PIL import Image
import cv2
from torch.utils.data import Dataset
from torchvision import transforms
import json
from os.path import exists
from numpy import zeros_like, ones_like

class ROBDataset(BaseDataSet):
    def __init__(self, **kwargs):
        self.num_classes = 2

        self.palette = pallete.get_voc_pallete(self.num_classes)
        super(ROBDataset, self).__init__(**kwargs)

    def _set_files(self):
        self.root = os.path.join(self.root, 'robustmislite')
        if self.split == "val":
            file_list = os.path.join("dataloaders/robust_split", f"{self.split}" + ".txt")
        elif self.split in ["train_supervised", "train_unsupervised"]:
            file_list = os.path.join("dataloaders/robust_split", f"{self.n_labeled_examples}_{self.split}" + ".txt")
        else:
            raise ValueError(f"Invalid split name {self.split}")

        file_list = [line.rstrip().split(' ') for line in tuple(open(file_list, "r"))]
        self.files, self.labels = list(zip(*file_list))

    def _load_data(self, index):
        image_path = os.path.join(self.root, self.files[index][1:])
        image = np.asarray(Image.open(image_path), dtype=np.float32)
        image=np.resize(image,(500,334,3))
        #print(image.shape)
        image_id = self.files[index].split("/")[-1].split(".")[0]
        if self.use_weak_lables:
            label_path = os.path.join(self.weak_labels_output, image_id+".png")
        else:
            label_path = os.path.join(self.root, self.labels[index][1:]) 
        label = np.asarray(Image.open(label_path), dtype=np.int32) if exists(label_path) else zeros_like(image[..., 0])
        #print(label.shape)
        label=np.resize(label,(500,334))
        return image, label, image_id

class ROB(BaseDataLoader):
    def __init__(self, kwargs):
        
        self.MEAN = [0.485, 0.456, 0.406]
        self.STD = [0.229, 0.224, 0.225]
        self.batch_size = kwargs.pop('batch_size')
        kwargs['mean'] = self.MEAN
        kwargs['std'] = self.STD
        kwargs['ignore_index'] = 255
        try:
            shuffle = kwargs.pop('shuffle')
        except:
            shuffle = False
        num_workers = kwargs.pop('num_workers')

        self.dataset = ROBDataset(**kwargs)

        super(ROB, self).__init__(self.dataset, self.batch_size, shuffle, num_workers, val_split=None)
