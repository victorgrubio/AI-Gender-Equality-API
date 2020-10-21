import cv2
import time
from threading import Lock
from openapi_server.detector.utils.my_queue import MyQueue


class VideoQueue(MyQueue):
    # class to read streams using threads

    def __init__(self, logger, queue_size=1, path=0, fps=None, has_buffer=False):
        MyQueue.__init__(self, logger, queue_size)
        self.cap = self.get_video_cap(path)
        self.fps = fps
        self.path = path
        self.has_buffer = has_buffer
        self.is_finished_lock = Lock()
        self.is_finished = False


    @property
    def is_finished(self):
        self.is_finished_lock.acquire(True)
        val = self.__is_finished
        self.is_finished_lock.release()
        return val

    @is_finished.setter
    def is_finished(self, val):
        self.is_finished_lock.acquire(True)
        self.__is_finished = val
        self.is_finished_lock.release()

    def get_video_cap(self, path):
        # check if video capture works
        cap = cv2.VideoCapture(path)
        if cap.isOpened() is False:
            raise FileNotFoundError(
                'Video stream or file not found at {}'.format(path))
        else:
            return cap

    def get_actual_frame(self):
        return int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))

    def get_total_frames(self):
        return int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def run(self):
        self.fps = int(self.cap.get(5)) if self.fps is None else self.fps
        last_added_frame_time = 0
        while self.thread.is_running:
            if not self.full():
                # read current frame from capture
                ret, frame = self.cap.read()
                if not ret:
                    self.logger.debug("No more images in video")
                    if self.empty():
                        self.logger.warn('Thread has stopped due to not ret')
                        self.thread.is_running = False
                else:
                    # self.logger.debug('Added frame to queue')
                    self.logger.log(
                        0, 'Last frame was added {} s ago'.format(
                            time.time() - last_added_frame_time))
                    last_added_frame_time = time.time()
                    self.put(frame)
                    self.logger.log(0, 'Current size of queue: {}'.format(
                        self.qsize()))
            # If the queue is full, clear it and reset. Only for streams
            else:
                if self.has_buffer:
                    self.clear()
                    self.logger.debug(
                        'Queue reached maximum capacity '
                        '({}). Cleared'.format(self.maxsize))
                else:
                    # self.logger.debug('SLEEPING for {:.3f}'.format(
                    #   timespace_frames))
                    time.sleep(1/self.fps)
            if self.is_stopped:
                break
        self.logger.info('videoThread not running')
        self.thread.is_running = False
