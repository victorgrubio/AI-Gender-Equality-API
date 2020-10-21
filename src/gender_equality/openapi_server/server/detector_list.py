import uuid
from openapi_server.detector.gender_equality_detector import GenderEqualityDetector


class FaceDetectorList(object):

    def __init__(self):
        self.detector_list = {}

    @property
    def detector_list(self):
        return self.__detector_list

    @detector_list.setter
    def detector_list(self, value):
        if value is None:
            raise TypeError("Cannot assign without a valid detector_list.")
        self.__detector_list = value

    def add_detector(self, video):
        detector_id = uuid.uuid1().hex
        detector = GenderEqualityDetector(detector_id, video)
        self.detector_list[detector_id] = detector
        print("Created new detector with ID {}".format(detector_id))
        return detector_id

    def get_detector(self, detector_id):
            if self.has_detector(detector_id):
                return self.detector_list[detector_id]
            else:
                raise AttributeError(
                        "Detector {} not found in app".format(detector_id))

    def delete_detector(self, detector_id):
        if detector_id in self.detector_list.keys():
            self.detector_list[detector_id].kill()
            self.detector_list[detector_id].pop()

    def start_detector(self, detector_id):
        detector = self.get_detector(detector_id)
        detector.start_thread()

    def has_detector(self, detector_id):
        if detector_id in self.detector_list.keys():
            return True
        else:
            print('List does not have detector {}'.format(detector_id))
            return False

    def kill(self):
        for name, detector in self.detector_list.items():
            detector.kill()
            self.detector_list[name].pop()
