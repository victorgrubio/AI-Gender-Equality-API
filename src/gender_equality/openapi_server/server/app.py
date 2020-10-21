import sys
import os
from pathlib import Path
import logging.config
import yaml
from openapi_server.server.detector_list import FaceDetectorList


log_dir = 'log'


def setupLogging(path=log_dir, default_level=logging.DEBUG, env_key='LOG_CFG'):
    """
    Setup logging configuration
    """
    value = os.getenv(env_key, None)
    if value:
        path = Path(value)
    if not Path(path).exists():
        backup_path = Path(__file__)
        if backup_path.exists():
            with backup_path.open('rt') as f:
                print(backup_path)
                config = yaml.safe_load(f.read())
            with path.open('w') as f:
                f.write(yaml.dump(config, default_flow_style=False))

    # Check logging directory
    log_dir = Path(sys.path[0]).joinpath(path)
    if not log_dir.exists():
        log_dir.mkdir()

    if path.exists():
        with path.open('rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


class BaseApp(object):
    '''
    classdocs
    HERE WE DEFINE DETECTORS AND SO ON
    '''

    def __init__(self):
        '''
        Constructor
        '''
#         setupLogging(path=log_dir)
#         self.logger = logging.getLogger(__name__)
        self.detector_list = FaceDetectorList()

    def list_detectors(self):
        pass

    def add_detector(self, detector):
        self.detector_list.add(detector)

    def delete_detector(self, detector):
        self.detector_list.delete(detector)

    def has_detector(self, detector_id):
        return self.detector_list.detectorExists(detector_id)

    def kill(self):
        self.detector_list.kill()

    @property
    def detector_list(self):
        return self.__detector_list

    @detector_list.setter
    def detector_list(self, value):
        if value is None:
            raise TypeError("Cannot assign without a valid detector List.")
        self.__detector_list = value
