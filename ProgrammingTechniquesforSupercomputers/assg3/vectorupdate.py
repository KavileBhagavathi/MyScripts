# -*- coding: utf-8 -*-
"""
Created on Wed May 29 14:28:28 2024

@author: arjun
"""
import pandas as pd
import matplotlib.pyplot as plt
import os
import zipfile

def unzip_op(long=True):
    """Unzip raw data files"""
    if long == True:
        with zipfile.ZipFile("vectorupdatelong.zip","r") as zip_ref:
            zip_ref.extractall("")
    else:
        with zipfile.ZipFile("vectorupdate.zip","r") as zip_ref:
            zip_ref.extractall("")
        
def average_perfcolumn(vectordf,temp_df):
    """Taking average of data values"""
    col = "Performance(F/s)"
    vectordf[col] = (vectordf[col] + temp_df[col])/2
    return vectordf

def return_txtop_files():
    """return list of text data files"""
    dir_files = os.listdir()
    data_files = []

    for file in dir_files:
        name,ext = os.path.splitext(file)
        if ext == ".txt" and "schon" not in name:
            data_files.append(file)
    return data_files

long = True
unzip_op(long)
data_files = return_txtop_files()
vectordf = pd.read_csv(data_files[0]) #starter dataframe

for file in data_files[1:]:
    temp_df = pd.read_csv(file)    
    vectordf = average_perfcolumn(vectordf, temp_df)
vectordf[vectordf.columns[-1]] = vectordf[vectordf.columns[-1]]/1e6
vectordf.rename(columns = {vectordf.columns[-1]:"MF/s"},inplace=True)
plt.plot(vectordf["Stride"],vectordf["MF/s"],color='green', marker='.', linestyle='--',lw=0.75)
plt.xlabel("Strides (M)")
plt.ylabel("Performance (MF/s)")
plt.title("Performance v/s Stride length")
plt.xscale("log")



