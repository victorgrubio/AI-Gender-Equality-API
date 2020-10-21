import numpy as np
import time
import traceback
from threading import Lock, Thread
import cv2
from collections import OrderedDict
from datetime import timedelta

from openapi_server.detector.base_detector import BaseDetector
from openapi_server.detector.face_gender_detector import FaceGenderDetector

from web_client.gender_equality_client.utils import save_results


class GenderVideoDetector(BaseDetector):

    def __init__(self, sensor_id, video_filename):
        super(GenderVideoDetector, self).__init__(
                id=sensor_id, video_filename=video_filename)
        self.results_lock = Lock()
        self.results = ''
        self.progress_lock = Lock()
        self.progress = 0
        self.actual_frame_number_lock = Lock()
        self.actual_frame_number = 0
        self.status_lock = Lock()
        self.status = "Initialized"
        self.thread = None
        self.face_gender_detector = FaceGenderDetector()

    @property
    def results(self):
        self.results_lock.acquire(True)
        val = self.__results
        self.results_lock.release()
        return val

    @results.setter
    def results(self, value):
        self.results_lock.acquire(True)
        self.__results = value
        self.results_lock.release()

    @property
    def progress(self):
        self.progress_lock.acquire(True)
        val = self.__progress
        self.progress_lock.release()
        return val

    @progress.setter
    def progress(self, value):
        self.progress_lock.acquire(True)
        self.__progress = value
        self.progress_lock.release()

    @property
    def status(self):
        self.status_lock.acquire(True)
        val = self.__status
        self.status_lock.release()
        return val

    @status.setter
    def status(self, value):
        self.status_lock.acquire(True)
        self.__status = value
        self.status_lock.release()

    @property
    def actual_frame_number(self):
        self.actual_frame_number_lock.acquire(True)
        val = self.__actual_frame_number
        self.actual_frame_number_lock.release()
        return val

    @actual_frame_number.setter
    def actual_frame_number(self, value):
        self.actual_frame_number_lock.acquire(True)
        self.__actual_frame_number = value
        self.actual_frame_number_lock.release()
        
    def start_thread(self, daemon=False):
        """
        Start detection thread
        """
        thread = Thread(target=self.run, args=())
        thread.daemon = daemon
        thread.start()
        self.thread = thread
        return self

    def run(self):
        """
        Method for predicting video
        """
        self.status = "Processing"
        start_total_time = time.time()
        while self.is_running:
            if self.video_queue.is_running:
                if self.video_queue.empty():
                    if self.video_queue.thread.is_running:
                        time.sleep(0.005)
                        self.logger.log(0, 'VIDEO QUEUE EMPTY')
                    else:
                        self.finalize()
                else:
                    try:
                        if self.video_queue:
                            img = self.video_queue.get()
                            if type(img) is np.ndarray:
                                start_time = time.time()
                                self.logger.log(0, "TIME AFTER CURRENT_TIME {}".format( time.time()-start_time ))
                                gender_video_predict = self.face_gender_detector.detect_genders_from_img(img)
                                if gender_video_predict:
                                    self.logger.log(0, "FACES DETECTED. TIME {}".format( time.time()-start_time ))
                                    final_gender = gender_video_predict[0]["gender"]
                                    dict_detection = OrderedDict(
                                        [('frame', self.actual_frame_number),
                                         ('gender', final_gender)])
                                    self.results.append(dict_detection)
                                self.actual_frame_number += 1
                                self.logger.log(0, "TIME AFTER dict_detection {}".format( time.time()-start_time ))
                                self.logger.log(0, "TIME AFTER write_results {}".format( time.time()-start_time ))
                                self.progress = self.update_progress()
                                self.logger.log(0, "TIME AFTER update_progress {}".format( time.time()-start_time ))
                                total_time = time.time() - start_total_time
                                self.logger.log(
                                        10, "PROGRESS: {}; TIME ELAPSED: {}; E.T.A: {}".format(
                                            self.progress, 
                                            timedelta(seconds=int(total_time)),
                                            timedelta(
                                                seconds=int(total_time*100/self.progress) - int(total_time))))
                    except:
                        self.status = "Failed"
                        self.logger.error(
                            'Unexpected error : {}'.format(
                                    traceback.format_exc()))
                        self.finalize()
                        break
            else:
                self.logger.info('Queue has stopped')
                self.finalize()
                break
        self.status = "Completed"
        self.logger.info(f"Analysis of video {self.video_queue.path} has been completed")
        save_results(self.results, "/home/visiona2/code/gender_equality_api/src/gender_equality/")

    def update_progress(self):
        return (self.actual_frame_number /
                self.video_queue.get_total_frames()) * 100
                
    def get_current_time(self):
        return self.actual_frame_number / self.video_queue.cap.get(cv2.CAP_PROP_FPS)
        
