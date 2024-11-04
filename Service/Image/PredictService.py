import os
import logging #TODO("필요없으면 지우십쇼")

import tensorflow as tf
import numpy as np

import cv2
from PIL import Image
from rembg import remove


class PredictService:
    root_path: str
    static_path:str
    
    def __init__(self):
        self.root_path = os.getcwd()
        self.static_path = os.path.join(self.root_path, "static")
    
    def predict_angle(self, image_path:str):
        image = cv2.imread(image_path)
        rb_img = remove(image)
        filled = np.array(rb_img)
        
        resize_image = self.__resize_with_padding(filled)
        
        if resize_image.shape[2] == 4:
            resize_image = cv2.cvtColor(resize_image, cv2.COLOR_RGBA2BGR)
            
        predicted_coords = self.__model_predict(resize_image)
        
        pred_red = (predicted_coords[0][0], predicted_coords[0][1])
        pred_green = (predicted_coords[0][2], predicted_coords[0][3])
        pred_blue = (predicted_coords[0][4], predicted_coords[0][5])

        base_height, base_width = image.shape[:2]
        pred_red_x = int(pred_red[0] * base_width / 224)
        pred_red_y = int(pred_red[1] * base_height / 224)
        pred_green_x = int(pred_green[0] * base_width / 224)
        pred_green_y = int(pred_green[1] * base_height / 224)
        pred_blue_x = int(pred_blue[0] * base_width / 224)
        pred_blue_y = int(pred_blue[1] * base_height / 224)

        pred_red = (pred_red_x, pred_red_y)
        pred_green = (pred_green_x, pred_green_y)
        pred_blue = (pred_blue_x, pred_blue_y)
        
        angle = self.__get_angle(pred_red, pred_green, pred_blue)
        return angle
        
    
### private ###
    def __resize_with_padding(self, image, target_size: tuple = (224,224)):
        h, w = image.shape[:2]
        target_h, target_w = target_size

        scale = min(target_w / w, target_h / h)
        new_w = int(w * scale)
        new_h = int(h * scale)

        resized_image = cv2.resize(image, (new_w, new_h))

        pad_w = (target_w - new_w) // 2
        pad_h = (target_h - new_h) // 2

        padded_image = cv2.copyMakeBorder(
            resized_image,
            pad_h,
            target_h - new_h - pad_h,
            pad_w,
            target_w - new_w - pad_w,
            borderType=cv2.BORDER_CONSTANT,
            value=[0, 0, 0],
        )
        
        return padded_image

    def __model_predict(self, resize_image):
        model_path = os.path.join(self.static_path, "keras_model", "cnn_model.keras")
        model = tf.keras.models.load_model(
            model_path,
            custom_objects={
                "euclidean_distance_loss": lambda y_true, y_pred: tf.sqrt(
                    tf.reduce_sum(tf.square(y_pred - y_true), axis=-1)
                )
            },
        )
        input_image = resize_image/255.0
        input_image = np.expand_dims(input_image, axis=0)
        
        result = model.predict(input_image)
        logging.info(result)
        return result
    
    def __get_angle(self, p1, p2, p3):
        a = np.linalg.norm(np.array(p2) - np.array(p1))
        b = np.linalg.norm(np.array(p2) - np.array(p3))
        c = np.linalg.norm(np.array(p1) - np.array(p3))
        
        angle = np.arccos((a**2 + b**2 - c**2) / (2*a*b))
        return np.degrees(angle)