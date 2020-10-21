import requests
import logging
from collections import OrderedDict
from csv import DictWriter
from time import time

PRODUCTION_ID=1950
API_URL_BASE='https://platform.limecraft.com/api/'
API_URL_DOWNLOAD= f'https://platform.limecraft.com/api/production/{PRODUCTION_ID}/'
USER="vgarcia"
PASSWORD="$5n22A!Z7P^o#E"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

data_login= {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'j_username': USER,
'j_password': PASSWORD,
'_spring_security_remember_me': 'on'}

#apply .json to obtain data as a python dict
login_dict = requests.post(API_URL_BASE+'j_spring_security_check',data=data_login).json()
token = login_dict['token']
#token header
headers_token = {'Authorization': 'BasicToken '+token}

#check if token work
token_status = requests.get(API_URL_BASE+'authentication/user',headers=headers_token)

production_list = requests.get(API_URL_BASE+'production.js',headers=headers_token).json()

#get media files
list_media_files = requests.get(API_URL_DOWNLOAD+'mo',headers=headers_token).json()
array_filenames = [
    # "informe_semanal_07092019.mp4", "desayunos_sanchez_cut.mp4",
    "informativo_2019_04_11.mp4", "noche_en_24h_2019_10_31_cut15min.mp4",
    "noche_en_24h_2019_10_31_cut30min.mp4", "por_tres_razones_millenials_ahorradores.aac"]

data_trans = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
'j_username': USER,
'j_password': PASSWORD
}


for media_file in list_media_files:
    if media_file['name'] in array_filenames:
        results = []
        media_file_dict = {'id' : media_file['id'], 'name' : media_file['name']}
        file_id = media_file.get('id')
        transcription = requests.get(API_URL_DOWNLOAD+'an/search.js?fq=mediaObjectId%3A'+str(file_id)+'&q=*:*&rows=10000000',headers=headers_token).json()
        filename = media_file.get('name').split('.')[0]
        #Obtain results
        last_start = 0
        result = transcription.get('results')
        #Each transcription's result is splitted in sections (Limecraft do not transcribed all at once)
        #tsa_content contains the raw text as a result of the transcription
        for transcribed_section in result:
            section_type=transcribed_section.get('type')
            if section_type == 'TRANSCRIBER':
                dict_results = OrderedDict()
                dict_results["speaker"] = transcribed_section.get('tsa_speaker')
                dict_results["frame_start"] = transcribed_section.get('start')
                dict_results["frame_end"] = transcribed_section.get('end')
                results.append(dict_results)
                # Limecraft transcript return all the analysis but 
                # the latest rows are the final result shown at the website.
        keys = results[0].keys()
        timestamp = int(time())
        with open(f'texts/results/limecraft_{filename}_{timestamp}.csv', 'w') as output_file:
            dict_writer = DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(results)
        
