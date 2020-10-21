from wtforms import Form
from wtforms.fields import SelectField

class SelectVideoForm(Form):
    video = SelectField('Video to process:', choices=[
        (u"/home/visiona2/Videos/videos_age_gender/gender_equality_demo/recoded_informe_semanal_07092019.mp4", "informe_semanal_07092019"),
        (u"/home/visiona2/Videos/videos_age_gender/gender_equality_demo/desayunos_sanchez_cut.mp4", "desayunos_sanchez_cut"),
        (u"/home/visiona2/Videos/videos_age_gender/gender_equality_demo/noche_en_24h_2019_10_31_cut15min.mp4", "La Noche 24h (15 min)"),
        (u"/home/visiona2/Videos/videos_age_gender/gender_equality_demo/noche_en_24h_2019_10_31_cut30min.mp4", "La Noche 24h (30 min)"),
        (u"/home/visiona2/Videos/videos_age_gender/gender_equality_demo/informativo_2019_04_11.mp4", "Informativo 04-09-2019")
        ])
    system = SelectField('Video to process:', choices=[
        (u"uam", "UAM"),
        (u"limecraft", "Limecraft")
        ])