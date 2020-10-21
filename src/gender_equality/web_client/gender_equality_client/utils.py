from csv import DictWriter
from os.path import join, sep
import time
from pandas import DataFrame, read_csv


def calculate_percentage(row, total):
    return row/total*100
    
def get_percentages_groupby(df):
    total = df["h"].sum(axis = 0, skipna = True)
    return df["h"].apply(calculate_percentage, args=[total])

def get_percentages_series(serie):
    total = serie.sum()
    return serie.apply(calculate_percentage, args=[total])

def save_results(results, upload_folder):
    timestamp = int(time.time())
    with open(join(sep, upload_folder, f"report_{timestamp}.csv"), "w", newline="") as csvfile:
        writer = DictWriter(csvfile, fieldnames=results[0].keys())
        writer.writeheader()
        for result in results:
            writer.writerow(result)
            
def process_results(results):
    df = None
    if isinstance(results, DataFrame):
        df = results
    else:
        df = DataFrame(results)
    gender_group = df.groupby("gender").count()
    df["COUNTER"] = 1
    speaker_serie = df.groupby(["gender","speaker_id"])['COUNTER'].sum() #sum function
    df = df.drop(columns="COUNTER")
    time_group = df.loc[ df['speaker_id'].ne(df['speaker_id'].shift()).astype(int) == 1 ]
    gender_percentage_df = get_percentages_groupby(gender_group)
    speakers_percentage_df = get_percentages_series(speaker_serie)
    gender_percentage_dict = gender_percentage_df.sort_values(ascending=False).to_dict()
    speakers_percentage_dict = speakers_percentage_df.sort_values(ascending=False).to_dict()
    return {"time_group": time_group, "gender_percentage": gender_percentage_dict, 
            "speakers_percentage": speakers_percentage_dict}
    
def load_dataframe_from_server(upload_folder, csv_filename):
    return read_csv(join(sep, upload_folder, csv_filename+".csv")) 
    