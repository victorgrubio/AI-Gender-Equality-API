from threading import Lock
import os
import yaml
import logging
from openapi_server.detector.setup_logging import setup_logging
from openapi_server.detector.video_queue import VideoQueue


class BaseDetector():

    def __init__(self, id, video_filename):
        self.id = id
        self.logger = logging.getLogger(__name__)
        self.video_queue = None
        self.video_filename = video_filename
        self.is_running_lock = Lock()
        self.is_running = True
        self.results_lock = Lock()
        self.results = ''
        self.setup_video_detector(video_filename)

    @property
    def is_running(self):
        self.is_running_lock.acquire(True)
        val = self.__is_running
        self.is_running_lock.release()
        return val

    @is_running.setter
    def is_running(self, value):
        self.is_running_lock.acquire(True)
        self.__is_running = value
        self.is_running_lock.release()
    
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

    def load_config(self, config_file):
        """
        Load config file
        TODO: AUTO PATH
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config = ""
        if os.path.exists(dir_path+'/'+config_file):
            with open(dir_path+'/'+config_file, 'rt') as f:
                config = yaml.safe_load(f.read())
        return config

    def setup_video_detector(self, video_filename):
        """Method documentation"""
        setup_logging()
        self.config = self.load_config('cfg/detector.yaml')
        self.create_results()
        self.video_queue = VideoQueue(
            self.logger, queue_size=1000, fps=1000, path=video_filename)
        self.video_queue.start()

    def create_results(self):
        self.results = []

    def start(self):
        """Method documentation"""
        pass

    def stop(self):
        """Method documentation"""
        pass

    def kill(self):
        """Method documentation"""
        pass

    def finalize(self):
        """
        Method docs
        """
        self.status = "Completed"
        self.progress = 100.0
        self.finalize_video_queue()

    def finalize_video_queue(self):
        """
        Method docs
        """
        if self.video_queue is not None:
            self.video_queue.is_running = False
            self.video_queue.finalize()
        self.is_running = False
