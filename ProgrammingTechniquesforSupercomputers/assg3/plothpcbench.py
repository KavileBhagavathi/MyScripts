#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:38:12 2024

@author: fo55pahy
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import zipfile

def unzip_op():
    """Unzip raw data files"""
    with zipfile.ZipFile("benchopSSE.zip","r") as zip_ref:
        zip_ref.extractall("")

def return_txtop_files():
    """return list of text data files"""
    dir_files = os.listdir()
    data_files = []

    for file in dir_files:
        name,ext = os.path.splitext(file)
        if ext == ".txt" and "vector" not in name:
            data_files.append(file)
    return data_files

def average_perfcolumn(schonauertridf,temp_df):
    """Taking average of data values"""
    col = "Performance(F/s)"
    schonauertridf[col] = (schonauertridf[col] + schonauertridf[col])/2
    return schonauertridf


def return_theoretical_peak_perf(AVX,precision):
    n_cores = 1
    n_fma = 2
    f = 2.1e9
    if precision == "dp":
        p = 64
    else:
        p = 32
    peak_perf = n_cores*2*n_fma*f*(AVX/p)
    return peak_perf/1e9

    
def print_theoretical_peak_perf():
    AVX = int(input("Input AVX width(512 or 256): "))
    precision = input("Input precision(dp or sp): ")
    peak_perf = return_theoretical_peak_perf(AVX, precision)
    print(f"Theoretical peak performance for the processor is: {peak_perf} GF/s")

def print_measured_theoretical_peal_perf_frac():
    pass
    
if __name__ == "__main__":
    unzip_op()
    print_theoretical_peak_perf()
    data_files = return_txtop_files()
    schonauertridf = pd.read_csv(data_files[0]) #starter dataframe
    
    for file in data_files[1:]:
        temp_df = pd.read_csv(file)    
        schonauertridf = average_perfcolumn(schonauertridf, temp_df)
        
    schonauertridf[schonauertridf.columns[-1]] = schonauertridf[schonauertridf.columns[-1]]/1e6
    schonauertridf.rename(columns = {schonauertridf.columns[-1]:"MF/s"},inplace=True)
    peak_performance = max(schonauertridf["MF/s"])
    peak_perf_array = schonauertridf.loc[schonauertridf["MF/s"]==peak_performance,"Array_Length"]
    plt.figure()
    plt.plot(schonauertridf["Array_Length"],schonauertridf["MF/s"],label="Vector Triad benchmarking",color='green', marker='.', linestyle='--',lw=0.75)
    plt.scatter(peak_perf_array, peak_performance,marker="D", color="red",label= f"Peak Performance = {peak_performance:.0f}MF/s")
    #plt.annotate(f"Peak performance = {peak_performance} MF/s", xy=(peak_perf_array, peak_performance),xytext=(int(peak_perf_array.iloc[0])+100, peak_performance))
    plt.legend()
    plt.xlabel("Array length")
    plt.ylabel("Performance (MF/s)")
    plt.xscale("log")
    plt.title("Double-Precision SSE Schönauer triad performance")
    plt.show()