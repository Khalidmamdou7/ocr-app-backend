import torch
import cv2
import numpy as np
import easyocr

import sys
import os
# model names are located in ocr-models folder
model_names = os.listdir('ocr-models')
print(model_names)

models = dict()
for model_name in model_names:
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=f'ocr-models/{model_name}', force_reload=False, trust_repo=True)
    models[model_name] = model

# for test purposes
model = models[model_names[0]]

reader = easyocr.Reader(['en'])

def add_model(model_file_name: str):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=f'ocr-models/{model_file_name}', force_reload=False, trust_repo=True)
    models[model_file_name] = model

def get_digits_from_image(image_path, model_name):
    img, labels, cord = model_predict(image_path, model_name)
    img, bounding_boxes = get_bounding_boxes(img, labels, cord)
    cropped_images = crop_image(img, bounding_boxes)
    results = dict()
    for label, image in cropped_images.items():
        result, preprocessed_image = ocr_predict(image)
        results[label] = result
    return results



def model_predict(image_path, model_name: str):
    model = get_model(model_name)
    img = cv2.imread(image_path)
    img = cv2.resize(img, (800, 800))
    results = model([img])
    results.print()
    labels, cord = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]
    return img, labels, cord

def get_model(model_name: str):

    if model_name not in models:
        raise ValueError(f"OCR: OCR model {model_name} not found, available models: {model_names}")
    return models[model_name]


    


def get_bounding_boxes(img, labels, cord):

    x_shape, y_shape = img.shape[1], img.shape[0]
    bounding_boxes = dict()
    for i in range(len(labels)):
        row = cord[i]
        x1, y1, x2, y2 = int(row[0]*x_shape), int(row[1]*y_shape), int(row[2]*x_shape), int(row[3]*y_shape)
        # bgr = (0, 255, 0)
        # cv2.rectangle(img, (x1, y1), (x2, y2), bgr, 2)
        # cv2.putText(img, model.names[int(labels[i])], (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, bgr, 2)

        bounding_boxes[model.names[int(labels[i])]] = [x1, y1, x2, y2]
    
    return img, bounding_boxes

def crop_image(image, bounding_boxes):
    cropped_images = dict()
    for label, cord in bounding_boxes.items():
        x1, y1, x2, y2 = cord
        crop_img = image[y1-10:y2, x1:x2]
        # cv2.imshow(label, crop_img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        cropped_images[label] = crop_img

    return cropped_images

def ocr_predict(img):
   
   preprocessed_image = preprocess_image(img)
   result = reader.readtext(preprocessed_image, detail=0, allowlist='0123456789')
   return result, preprocessed_image

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    black_hat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    dilated = cv2.dilate(black_hat, (1, 1), iterations=1)
    resized = cv2.resize(dilated, (400, 200))

    return resized