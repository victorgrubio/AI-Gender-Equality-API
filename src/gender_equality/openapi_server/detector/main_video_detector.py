from openapi_server.detector.gender_video_detector import GenderVideoDetector


if __name__ == "__main__":
    video_informe_semanal = "/home/visiona2/Videos/videos_age_gender/gender_equality_demo/recoded_informe_semanal_07092019.mp4"
    video_desayunos = "/home/visiona2/Videos/videos_age_gender/gender_equality_demo/desayunos_sanchez_cut.mp4"
    video_noche15min = "/home/visiona2/Videos/videos_age_gender/gender_equality_demo/noche_en_24h_2019_10_31_cut15min.mp4"
    video_noche30min = "/home/visiona2/Videos/videos_age_gender/gender_equality_demo/noche_en_24h_2019_10_31_cut30min.mp4"
    video_informativo = "/home/visiona2/Videos/videos_age_gender/gender_equality_demo/informativo_2019_04_11.mp4"
    detector = GenderVideoDetector(sensor_id=1, video_filename=video_informativo)
    detector.run()