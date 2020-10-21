import numpy as np
import time
import traceback
from threading import Lock, Thread
import cv2
from os.path import dirname, join, realpath, sep
from collections import OrderedDict
from datetime import timedelta

from openapi_server.detector.base_detector import BaseDetector
from openapi_server.detector.text_gender_agent import TextGenderAgent
from openapi_server.detector.face_gender_detector import FaceGenderDetector

from openapi_server.utils.create_response_msg import CreateResponseMsg
from openapi_server.utils.message_tags import message_tags
from openapi_server import encoder


class GenderEqualityDetector(BaseDetector):

    def __init__(self, sensor_id, video_filename):
        super(GenderEqualityDetector, self).__init__(
                id=sensor_id, video_filename=video_filename)
        self.progress_lock = Lock()
        self.progress = 0
        self.actual_frame_number_lock = Lock()
        self.actual_frame_number = 0
        self.status_lock = Lock()
        self.status = "Initialized"
        self.thread = None
        self.text_gender_speaker_agent = None
        self.get_audio_text_agents(video_filename)
        self.face_gender_detector = FaceGenderDetector()

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
    
    def get_program_by_video_filename(self, video_filename):
        for program in self.config["programs"]:
            if video_filename == self.config[program]["video_path"]:
                return program
        raise AttributeError("Program not found")

    def get_audio_text_agents(self, video_filename):
        text_gender = self.get_processed_gender(video_filename)
        text_speakers = self.get_processed_speakers(video_filename)
        self.text_gender_speaker_agent = TextGenderAgent(gender_file=text_gender, speaker_file=text_speakers)
        
    def get_processed_gender(self, video_filename):
        dir_path =  dirname(realpath(__file__))
        program = self.get_program_by_video_filename(video_filename)
        gender_file = join(sep, dir_path, self.config[program]["gender_path"])
        return gender_file
    
    def get_processed_speakers(self, video_filename):
        dir_path =  dirname(realpath(__file__))
        program = self.get_program_by_video_filename(video_filename)
        speakers_file = join(sep, dir_path, self.config[program]["speakers_path"])
        return speakers_file

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
                                current_time = self.get_current_time()
                                self.logger.log(0, "TIME AFTER CURRENT_TIME {}".format( time.time()-start_time ))
                                time_code_dict = self.get_timecode_dict(current_time)
                                (gender_audio, gender_audio_accuracy, speaker) = self.text_gender_speaker_agent.get_current_time_gender_speaker(current_time)
                                self.logger.log(0, "TIME AFTER GETTING DATA FROM AUDIO FILES {}".format( time.time()-start_time ))
                                self.logger.log(10, "GENDER AUDIO: {} || ACCURACY {}".format(gender_audio, gender_audio_accuracy))
                                gender_video_predict = self.face_gender_detector.detect_genders_from_img(img)
                                if gender_video_predict:
                                    self.logger.log(10, "FACES DETECTED. TIME {}".format( time.time()-start_time ))
                                    final_gender = self.get_final_gender(gender_audio, gender_audio_accuracy, gender_video_predict[0])
                                    self.logger.log(10, "VIDEO RESULTS: {}".format(gender_video_predict))
                                else:
                                    final_gender = gender_audio
                                dict_detection = OrderedDict(
                                    [('h', time_code_dict["h"]),
                                     ('m', time_code_dict["m"]),
                                     ('s', time_code_dict["s"]),
                                     ('frame', time_code_dict["frame"]),
                                     ('gender', final_gender),
                                     ('speaker_id', speaker)])
                                self.actual_frame_number += 1
                                self.logger.log(0, "TIME AFTER dict_detection {}".format( time.time()-start_time ))
                                self.results.append(dict_detection)
                                self.logger.log(0, "TIME AFTER write_results {}".format( time.time()-start_time ))
                                self.progress = self.update_progress()
                                self.logger.log(0, "TIME AFTER update_progress {}".format( time.time()-start_time ))
                                total_time = time.time() - start_total_time
                                self.logger.log(10, "Actual frame: {} || Total frames: {}".format( self.actual_frame_number, self.video_queue.get_total_frames() ))
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
            else:
                self.logger.info('Queue has stopped')
                self.finalize()
                break
        self.status = "Completed"

    def update_progress(self):
        return (self.actual_frame_number /
                self.video_queue.get_total_frames()) * 100
                
    def get_current_time(self):
        return self.actual_frame_number / self.video_queue.cap.get(cv2.CAP_PROP_FPS)
    
    def get_timecode_dict(self, current_time):
        timecode_dict = {"h": 0, "m": 0, "s":0, "frame":0}
        timecode_dict["frame"] = int(self.actual_frame_number % self.video_queue.cap.get(cv2.CAP_PROP_FPS))
        timecode_dict["s"] = int(current_time % 60)
        timecode_dict["m"] = int(current_time / 60) if current_time > 60 else 0
        timecode_dict["h"] = int(current_time / 3600) if current_time > 3600 else 0
        return timecode_dict

    def get_final_gender(self, gender_audio, gender_audio_accuracy, gender_video_predict):
        if gender_audio_accuracy > gender_video_predict["accuracy"]:
            self.logger.log(10, "predicted using AUDIO")
            return gender_audio
        else:
            self.logger.log(10, "predicted using VIDEO")
            return gender_video_predict["gender"]

    def get_results_msg(self):
#         results_dict = self.results.to_dict('records', into=OrderedDict)
        tag = message_tags['RESULTS']['tag']
        msg = CreateResponseMsg.create_msg(tag)
        msg.set_timestamp()
        msg.data = {'results': self.results}
        msg_encoded = encoder.JSONEncoder().encode(msg)
        return msg_encoded
