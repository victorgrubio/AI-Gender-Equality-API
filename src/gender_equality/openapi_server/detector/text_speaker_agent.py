# -*- coding: utf-8 -*-
import pandas as pd
import time

class TextSpeakerAgent:
    
    def __init__(self, speaker_file="texts/speakers_radio.txt"):
        self.speaker_file = speaker_file
        self.df = pd.read_csv(
                speaker_file, sep="\t|\s|,|;", header=None, names=["t_start", "t_end", "speaker"])
    

    def get_current_interval(self, current_time):
        condition1 = (self.df['t_start'].to_numpy() <= current_time) & (self.df['t_end'].to_numpy() >= current_time)
#         print("TIME define interval condition {}".format(time.time() - start_time))
        df_interval = self.df[condition1].reset_index(drop=True)
#         print("TIME find interval {}".format(time.time() - start_time))
        interval = {"t_start":df_interval.iloc[0].t_start, "t_end": df_interval.iloc[0].t_end}
        return interval
    

    def get_current_interval_speaker(self, interval):
        condition1 = self.df['t_start'].to_numpy() == interval["t_start"]
        speaker = self.df[condition1].reset_index(drop=True).iloc[0].speaker
        return speaker
    

    def get_current_time_speaker(self, current_time):
        interval = self.get_current_interval(current_time)
        speaker = self.get_current_interval_speaker(interval)
        return speaker
    