# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 17:26:40 2024

@author: arjun
"""

import pandas as pd
from os import listdir
import matplotlib.pyplot as plt
import numpy as np




def calculate_grad(df):
    """function to calculate gradient du/dr"""
    """delta_r1 = df["r"].iloc[-1] - df["r"].iloc[-2]
    delta_r2 = df["r"].iloc[-2] - df["r"].iloc[-3]
    delta_r3 = delta_r1 + delta_r2
    gradient =  df["uz(r)"].iloc[-2]*(delta_r3**2) - df["uz(r)"].iloc[-3]*(delta_r1**2) + \
                (delta_r1**2 - delta_r3**2)*df["uz(r)"].iloc[-1]
    gradient /= (delta_r3**2)*delta_r1 - (delta_r1**2)*delta_r3
    return gradient"""
    grad = np.gradient(df["uz(r)"],df["r"])
    return np.abs(grad)
    
def laminar_velocity_profile(df):
    """https://web.itu.edu.tr/~bulu/fluid_mechanics_files/lecture_notes_07.pdf"""
    #max pipe radius is, R = 1
    df["u_laminar"] = (1 - (df["r"])**2) #u = u_max(1-(r**2)/(R**2))
    return df

def read_velocity_prof(element):
    req_file_path = file_path[element] +  "/vel_profile.dat"
    Re = int(element[2:])
    if element == "Re10000":
        """vel_profile.dat of Re10000 has a weird delimiter scheme at the beginning
        and end of data stream. Delimitater has been fixed manually and hence use 
        the vel_profile.dat provided in the repo. There are no change in values
        but only the delimiter."""
        vel_prof_df1 = pd.read_csv(req_file_path,nrows=9, delimiter= " ",float_precision=None)
        vel_prof_df1 = vel_prof_df1.reset_index()
        vel_prof_df1 = vel_prof_df1[["level_2","#"]]
        vel_prof_df1 = vel_prof_df1.rename(columns={vel_prof_df1.columns[0]:"r",vel_prof_df1.columns[1]:"uz(r)"})
        vel_prof_df2 = pd.read_csv(req_file_path,skiprows=9, delimiter= " ",float_precision=None)
        vel_prof_df2 = vel_prof_df2.reset_index()
        vel_prof_df2 = vel_prof_df2[["level_2",vel_prof_df2.columns[9]]]
        vel_prof_df2 = vel_prof_df2.rename(columns={vel_prof_df2.columns[0]:"r",vel_prof_df2.columns[1]:"uz(r)"})
        vel_prof_df = pd.concat([vel_prof_df1,vel_prof_df2])
        vel_prof_df = laminar_velocity_profile(vel_prof_df)
    else:
        vel_prof_df = pd.read_csv(req_file_path,skiprows=1, delimiter= "  ",float_precision=None)
        vel_prof_df = vel_prof_df.rename(columns={vel_prof_df.columns[0]:"r"})
    return vel_prof_df

def plot_raw_velocity_profiles(element):
    vel_prof_df = read_velocity_prof(element)
    grad_dict.update({element:calculate_grad(vel_prof_df)})
    plt.plot(vel_prof_df["r"],vel_prof_df["uz(r)"],label=f"{element}")
    if element == "Re10000":
        plt.plot(vel_prof_df["r"],vel_prof_df["u_laminar"],label="u laminar")
    plt.xlabel("r")
    plt.ylabel("uz(r)")
    plt.legend()
    return vel_prof_df

def plot_uplus_yplus(element,grad_dict):
    vel_prof_df = read_velocity_prof(element) 
    wall_velocity_gradient = grad_dict[element][-1]
    vel_prof_df = calculate_u_plus(vel_prof_df,wall_velocity_gradient,element)
    vel_prof_df = calculate_y_plus(vel_prof_df,element)
    plt.plot(vel_prof_df["y_plus"],vel_prof_df["u_plus"],label=f"{element}")
    plt.xscale("log")
    plt.xlabel("log y+")
    plt.ylabel("U+")
    plt.legend()
    
def calculate_u_plus(df,wall_velocity_gradient,element):
    req_u_wall = calculate_u_wall(wall_velocity_gradient, element)
    df["u_plus"] = df["uz(r)"]/req_u_wall
    return df

def calculate_y_plus(df,Re_str):
    Re = int(Re_str[2:])
    df["y_plus"] = (1 - df["r"])*df["u_plus"]*Re
    return df
    
def return_wall_parameters(grad_dict,req_files):
    for element in req_files:
        wall_velocity_gradient = grad_dict[element][-1]
        friction_Re = calculate_friction_reynolds(wall_velocity_gradient,element)
        u_wall = calculate_u_wall(wall_velocity_gradient,element)
        print(f"Wall velocity gradient for {element} is: {wall_velocity_gradient}")
        print(f"Wall velocity for {element} is: {u_wall}")
        print(f"Friction Reynolds for {element} is: {friction_Re}\n")
        
def calculate_friction_reynolds(wall_vel_grad,Re_str):
    Re = int(Re_str[2:])
    friction_Re = (np.sqrt(wall_vel_grad/Re)*1)*Re
    return friction_Re

def calculate_Re_tau(u_plus,Re,R):
    return u_plus*R*Re

def calculate_u_wall(wall_velocity_gradient,Re_str):
    Re = int(Re_str[2:])
    return np.sqrt(wall_velocity_gradient/Re)


if __name__ == "__main__":
    
    """the script needs to be in the same directory as DNS_pipe for the code to work"""
    file_path = {"Re2400":"DNS_pipe/Re2400",
                 "Re3000":"DNS_pipe/Re3000",
                 "Re10000":"DNS_pipe/Re10000"} 
    
    req_files = ["Re2400","Re3000","Re10000"]
    grad_dict = {}
    plt.figure()
    for element in req_files:
        vel_prof_df = plot_raw_velocity_profiles(element)
        grad_dict.update({element:calculate_grad(vel_prof_df)})
    plt.show()
    plt.figure()
    for element in req_files:
        plot_uplus_yplus(element, grad_dict)
    plt.show()
    return_wall_parameters(grad_dict, req_files)
    