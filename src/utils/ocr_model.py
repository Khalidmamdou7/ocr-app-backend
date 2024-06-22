# import torch
import cv2
import numpy as np
import easyocr
import json
from roboflow import Roboflow

roboflow_config = json.load(open("./src/utils/roboflow-config.json"))["counters_models"]

reader = easyocr.Reader(['en'])


def get_digits_from_image(image_path, counter_id = None):
    img, labels, bounding_boxes = model_predict_roboflow(image_path, counter_id)

    cropped_images = crop_image(img, bounding_boxes)
    results = dict()
    for model_name in labels:
        results[model_name] = "0"
    for label, image in cropped_images.items():
        result, preprocessed_image = ocr_predict(image)
        if len(result) == 0:
            print(f"OCR: No text detected in {label}, setting to 0 by default")
            continue
        results[label] = result[0]
    print(f"OCR: Predicted results: {results}")
    return results




def model_predict_roboflow(image_path, counter_id: str):
    img = cv2.imread(image_path)
    model_config = roboflow_config[counter_id]
    # url = "https://detect.roboflow.com/"+model_config['project_id']+"/" + model_config['version'] + "?api_key=" + model_config['api_key'] + "&confidence=" + str(model_config['confidence']) + "&overlap=" + str(model_config['overlap'])
    rf = Roboflow(api_key=model_config["api_key"])

    rf_project = rf.workspace().project(model_config["project_id"])
    rf_model = rf_project.version(model_config["version"]).model
    rf_result = rf_model.predict(image_path, confidence=model_config["confidence"], overlap=model_config["overlap"]).json()
    
    predictions = rf_result['predictions']
    image_width = int(rf_result['image']['width'])
    image_height = int(rf_result['image']['height'])

    bounding_boxes = dict()
    labels = []
    for prediction in predictions:
        labels.append(prediction['class'])
        width = int(prediction['width'])
        height = int(prediction['height'])
        x = int(prediction['x'])
        y = int(prediction['y'])

        x1 = int(x - (width/2))
        y1 = int(y - (height/2))
        x2 = int(x + (width/2))
        y2 = int(y + (height/2))
        bounding_boxes[prediction['class']] = [x1, y1, x2, y2]

    labels = np.array(labels)
    
    print(f"Roboflow: Predicted {len(predictions)} objects")
    print(f"Roboflow: Predicted labels: {labels}")

    return img, labels, bounding_boxes

def crop_image(image, bounding_boxes: dict):

    cropped_images = dict()
    for label, cord in bounding_boxes.items():
        x1, y1, x2, y2 = cord
        crop_img = image[y1-10:y2, x1:x2]
        
        cropped_images[label] = crop_img


    return cropped_images

def ocr_predict(img):
   result = reader.readtext(img, detail=0, allowlist='0123456789')
   return result, img