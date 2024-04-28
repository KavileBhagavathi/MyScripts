# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:26:40 2024

@author: arjun
"""

import pandas as pd
from os import listdir
import seaborn as sb
if __name__ == "__main__":
    
    file_path = {"Re2400":"DNS_pipe/Re2400",
                 "Re3000":"DNS_pipe/Re3000",
                 "Re10000":"DNS_pipe/Re10000"}
    
    #req_file = input("Choose Re value (Re2400 / Re3000 / Re10000)")
    req_file = "Re2400"
    req_file_path = file_path[req_file] +  "/vel_profile.dat"
    
    vel_prof_df = pd.read_csv(req_file_path,skiprows=1, delimiter= "  ",float_precision=None)
    vel_prof_df = vel_prof_df.rename(columns={vel_prof_df.columns[0]:"r"})
    
    sb.lineplot(x=vel_prof_df["r"],y=vel_prof_df["uz(r)"])