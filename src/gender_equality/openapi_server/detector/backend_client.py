import requests
import time
import pandas as pd


def calculate_percentage(row, total):
    return row/total*100
    
def get_percentages(df, parameter="gender"):
    total = df["h"].sum(axis = 0, skipna = True)
    return df["h"].apply(calculate_percentage, args=[total])

if __name__ == "__main__":

    headers = {"Content-Type": "application/json"}
    detector_response = requests.post(
            "http://localhost:5000/v1/gender_equality/face_detection",
            headers=headers,
            json={"video": "/home/visiona2/Videos/videos_age_gender/recoded_informe_semanal_07092019.mp4"}
    ).json()
    detector_id = detector_response["data"]["id"]
    time.sleep(30)
    report = requests.get(
        "http://localhost:5000/v1/gender_equality/results",
        headers= headers,
        json={"id": detector_id}
    ).json()
    results = report["data"]["results"]
    df = pd.DataFrame(results)
    gender_group = df.groupby("gender").count()
    speaker_group = df.groupby("speaker_id").count()
    time_group = df.loc[ df['speaker_id'].ne(df['speaker_id'].shift()).astype(int) == 1 ]
    print("{} \n {} \n {} \n".format(
        gender_group, speaker_group, time_group))
    
    
    
    