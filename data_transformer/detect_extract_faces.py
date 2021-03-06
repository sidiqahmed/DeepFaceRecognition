from __future__ import division, print_function, absolute_import

import os
import cv2
import numpy as np
import logging
from scipy import  misc

from config import path_dict, myNet

FACE_CASCADE=cv2.CascadeClassifier(path_dict['haar_cascade'])

def resize_image(image, resize_shape):
    if image.shape[0] < resize_shape[0] or image.shape[1] < resize_shape[1]:
        return []
    else:
        imageResized = misc.imresize(image, myNet['image_shape'])
        imageResized = np.array(imageResized)

        return imageResized
    

def detect_extract_faces(image_path, face_extracted_path=None,
                         face_detection_path=None, store=True):
    image=cv2.imread(image_path)
    # print (image)
    image_grey=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    
    faces = FACE_CASCADE.detectMultiScale(image_grey,scaleFactor=1.16,
                                          minNeighbors=5,minSize=(25,25),flags=0)
    faces_arr = []
    rect_arr = []
    if len(faces) > 0:
        for num, (x,y,w,h) in enumerate(faces):
            sub_img = image[y-10:y+h+10,x-10:x+w+10]
            logging.info('Yes! We could detect faces')
            sub_img = resize_image(sub_img, resize_shape=myNet['image_shape'])
            
            if len(sub_img) > 0:
                faces_arr.append(sub_img)
                rect_arr.append([x, y, w, h])
                if store:
                    outpath = os.path.basename(face_extracted_path).split('.')[0]
                    outpath = os.path.join(path_dict['face_extracted_test_path'],
                                           str(outpath)+'_%s.jpg'%str(num))
                    cv2.imwrite(outpath, sub_img)
            else:
                if store:
                    rimg = resize_image(image, resize_shape=myNet['image_shape'])
                    outpath = os.path.basename(face_extracted_path).split('.')[0]
                    outpath = os.path.join(path_dict['face_extracted_test_path'],
                                           str(outpath) + '_%s.jpg' % str(num))
                    cv2.imwrite(outpath, rimg)
                
            # Place rectangles for the regions
            cv2.rectangle(image,(x,y),(x+w,y+h),(255, 255,0),2)
    else:
        logging.info('Oops! We could not detect faces')
        if store:
            rimg = resize_image(image, resize_shape=myNet['image_shape'])
            cv2.imwrite(face_extracted_path, rimg)

    if store:
        # image = resize_image(image, (400,300))
        cv2.imwrite(face_detection_path, image)
    return np.array(faces_arr), np.array(rect_arr)


debugg = False
if debugg:
    full_image_path = '/Users/sam/All-Program/App-DataSet/DeepFaceRecognition/output_data_faces/face_snapshot/img4.jpg'
    test_faces = detect_extract_faces(full_image_path, store=False)
    print (test_faces.shape)
# detect_extract_faces(path_dict['image_path'])