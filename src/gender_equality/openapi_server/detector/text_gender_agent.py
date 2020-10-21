# -*- coding: utf-8 -*-
import pandas as pd
import math
# import time

from openapi_server.detector.text_speaker_agent import TextSpeakerAgent


class TextGenderAgent:

    def __init__(self, gender_file="texts/gender_radio.txt", speaker_file="texts/speakers_radio.txt"):
        self.df = pd.read_csv(gender_file, sep="\t|\s|,|;", header=None,
                              names=["t_start", "t_end", "gender"])
        self.speaker_agent = TextSpeakerAgent(speaker_file)
        df_cols = ["t_start","t_end", "gender", "speaker_id"]
        self.df_gender_speaker_intervals = pd.DataFrame(columns=df_cols)
        self.generate_df_gender_intervals(df_cols)
    

    def generate_df_gender_intervals(self, df_cols):
        current_time = 0.00
        max_time = self.df['t_end'].to_numpy().max()
        while current_time < max_time:
            interval = self.speaker_agent.get_current_interval(current_time)
            speaker = self.speaker_agent.get_current_interval_speaker(interval)
            gender = self.get_current_interval_gender(interval)
            self.df_gender_speaker_intervals = self.df_gender_speaker_intervals.append(
                    pd.DataFrame([
                    [interval["t_start"], interval["t_end"], gender, speaker]],
                    columns=df_cols))
            current_time = math.ceil(interval["t_end"]) if math.ceil(interval["t_end"]) != int(current_time) else current_time +1 
        
    def get_current_interval_gender(self, interval):
        # For intervals smaller than the gender analysis time (3 secs)
        if interval["t_end"] - interval["t_start"] < 3:
            condition1 = (self.df["t_start"].to_numpy() >= round(interval["t_start"]))
            condition2 = (self.df["t_start"].to_numpy() <= round(interval["t_end"]))
            df_gender_current_interval = self.df[condition1 & condition2 ]
        else:
            condition1 = (self.df["t_start"].to_numpy() >= round(interval["t_start"]))
            condition2 = (self.df["t_start"].to_numpy() <= round(interval["t_end"]))
            df_gender_current_interval = self.df[ condition1 & condition2 ]
        # If gender empty, defines f
        if df_gender_current_interval.empty:
            gender = "f"
            accuracy = 1
        else:
            genders = df_gender_current_interval["gender"].value_counts()
            gender = genders.idxmax()
            accuracy = genders[gender] / genders.sum()
        return (gender, accuracy)
    

    def get_current_time_gender(self, current_time):
        interval = self.speaker_agent.get_current_interval(current_time)
        return self.get_current_interval_gender(interval)
    

    def get_speaker_gender_time(self, df_speaker, gender="f"):
            speaker_gender_t_start = df_speaker[(df_speaker["gender"].to_numpy() == gender)]["t_start"].to_numpy().sum()
            speaker_gender_t_end = df_speaker[(df_speaker["gender"].to_numpy() == gender)]["t_end"].to_numpy().sum()
            return speaker_gender_t_end - speaker_gender_t_start
    

    def get_current_time_gender_speaker(self, current_time):
#         start_time = time.time()
        interval = self.speaker_agent.get_current_interval(current_time)
#         print("TIME get_current_interval {}".format(time.time() - start_time))
        (gender, gender_accuracy) = self.get_current_interval_gender(interval)
#         print("TIME get_current_interval_gender {}".format(time.time() - start_time))
        speaker = self.speaker_agent.get_current_interval_speaker(interval)
#         print("TIME get_current_interval_speaker {}".format(time.time() - start_time))
        return (gender, gender_accuracy, speaker)
        