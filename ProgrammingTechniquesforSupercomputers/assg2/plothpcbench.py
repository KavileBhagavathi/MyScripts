#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 15 11:38:12 2024

@author: fo55pahy
"""

import pandas as pd
import matplotlib.pyplot as plt

vectortridf = pd.read_csv(r"vectortriad_benchmark.txt")
daxpy_df = pd.read_csv(r"daxpy_benchmarkop.txt")
vectortridf[vectortridf.columns[-1]] = vectortridf[vectortridf.columns[-1]]/1e6
vectortridf.rename(columns = {vectortridf.columns[-1]:"MF/s"},inplace=True)
daxpy_df[daxpy_df.columns[-1]] = daxpy_df[daxpy_df.columns[-1]]/1e6
daxpy_df.rename(columns = {daxpy_df.columns[-1]:"MF/s"},inplace=True)

plt.figure()
plt.plot(vectortridf["Array_Length"],vectortridf["MF/s"],label="Vector Triad benchmarking",color='green', marker='.', linestyle='--',lw=0.75)
plt.plot(daxpy_df["Array_Length"],daxpy_df["MF/s"],label="DAXPY benchmarking",color="steelblue", marker=".",linestyle="--",lw=0.75)
plt.legend()
plt.xlabel("Array length")
plt.ylabel("Performance (MF/s)")
plt.xscale("log")
plt.show()