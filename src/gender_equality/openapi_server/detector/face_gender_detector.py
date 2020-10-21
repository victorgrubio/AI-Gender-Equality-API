import time
import cv2
import numpy as  np
from itertools import takewhile
from os.path import dirname, abspath

from openapi_server.detector.my_model import MyModel
from openapi_server.detector.wide_resnet import WideResNet


class FaceGenderDetector():

    def __init__(self):
        self.gender_detector_input_size = 64
        self.face_detector = self.load_facenet()
        self.model = self.load_gender_model()
    
    def load_facenet(self):
        prototxt = dirname(abspath(__file__)) + '/weights/deploy.prototxt'
        model_path = dirname(abspath(__file__)) + '/weights/face_detection.caffemodel'
        net = cv2.dnn.readNetFromCaffe(prototxt, model_path)
        return net

    def load_gender_model(self):
        """
        Load model and weights
        """
        depth = 16
        k = 8
        weight_file = dirname(abspath(__file__)) + '/weights/weights.28-3.73.hdf5'
        # load model and weights
        model_arch = WideResNet(self.gender_detector_input_size, depth=depth, k=k)()
        model = MyModel(path_weights=weight_file, path_arch=None, model=model_arch)
        return model

    def detect_faces(self, img):
        threshold_confidence = 0.4
        # load the input image and construct an input blob for the image
        # by resizing to a fixed 300x300 pixels and then normalizing it
        (h, w) = img.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0,
            (300, 300), (104.0, 177.0, 123.0))
        self.face_detector.setInput(blob)
        detections = self.face_detector.forward()
        valid_detections = list(takewhile(
            lambda detection: detection > threshold_confidence, detections[0,0,:,2]))
        faces = np.empty(
            (len(valid_detections),
             self.gender_detector_input_size, self.gender_detector_input_size, 3))
        boxes_coordinates = np.empty((len(valid_detections), 4), dtype=np.int32)
        for index in range(0, len(valid_detections)):
            confidence = detections[0, 0, index, 2]
            if confidence > threshold_confidence:
                box = detections[0, 0, index, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                if any(coord > max(w, h) for coord in box.astype("int")) or any(coord < 0 for coord in box.astype("int")):
                    continue
                else:
                    cv2.rectangle(
                        img, (startX, startY), (endX, endY), (255, 0, 0), 1)
                    boxes_coordinates[index] = [startX, startY, endX, endY]
                    faces[index, :, :, :] =\
                        cv2.resize(img[startY:endY + 1, startX:endX + 1, :],
                                   (self.gender_detector_input_size, self.gender_detector_input_size))
            else:
                break
        return (faces, boxes_coordinates)
    
    def detect_genders_from_faces(self, faces, boxes_coordinates, filter_faces = True):
        if filter_faces:
            biggest_face_index = self.get_index_biggest_face(boxes_coordinates)
            faces = np.expand_dims(faces[biggest_face_index], axis = 0)
        genders = []
        start_time = time.time()
        predicted_genders = self.model.predict(faces)[0]
        for index in range(0, faces.shape[0]):
            if any(str(x) == 'nan' for x in predicted_genders[index]):
                continue
            gender_label = "f" if predicted_genders[index][0] > 0.5 else "m"
            accuracy = max(predicted_genders[index])
            genders.append({"gender": gender_label, "accuracy": accuracy})
        return genders
    
    def detect_genders_from_img(self, img):
        (faces, boxes_coordinates) = self.detect_faces(img)
        if len(faces) == 0:
            return {}
        else:
            gender_dict = self.detect_genders_from_faces(faces, boxes_coordinates)
        return gender_dict

    def get_index_biggest_face(self, face_boxes):
        max_index = 0
        max_area = 0
        for index_box, box in enumerate(face_boxes):
            area = self.get_area_of_box(box)
            if area > max_area:
                max_index = index_box
                max_area = area
        return max_index
    
    def get_area_of_box(self, box):
        return (int(box[2])-int(box[1]))*(int(box[3])-int(box[1]))
    
