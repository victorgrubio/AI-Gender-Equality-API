from os import environ
from os.path import dirname, realpath, join, sep

class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY') or 'you-will-never-guess'
    dir_path = dirname(realpath(__file__))
    UPLOAD_FOLDER = join(
        sep, dir_path, "gender_equality_client/uploads"
        )
    MAX_CONTENT_LENGTH = 1024 * 1024 * 1024 * 1024
#     PROCESSED_VIDEOS = [
#          "/home/visiona2/Videos/videos_age_gender/gender_equality_demo/recoded_informe_semanal_07092019.mp4",
#          "/home/visiona2/Videos/videos_age_gender/gender_equality_demo/recoded_informe_semanal_07092019.mp4"]
#     CSV_FILES = ["report_informe_semanal_audio", "report_desayunos_audio"]
    PROCESSED_VIDEOS = []
    CSV_FILES = []