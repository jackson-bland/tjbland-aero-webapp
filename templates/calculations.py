from flask import Flask, request, render_template, url_for, session
from datetime import timedelta
import numpy as np

def standard_atmos_calculations(height, units):
    if units.lower() == 'eng':
        e_radius, phase_1, phase_2, phase_3, phase_4 = 20925648.48, 0, 36089.2, 82021., 154199. 
        temp_s, den_s, pres_s, gas_c, grav, gamma, temp_tp = 518.69, .002377, 2116.2, 1716, 32.2, 1.4, 389.9
        unitList = ["[ft]", "[ft/lb^2]", "[R]", "[slug/ft^3]", "[ft/s]"]
    elif units.lower() == 'metric':
        e_radius, phase_1, phase_2, phase_3, phase_4 = 6.3781E6, 0, 11000, 25000, 47000. 
        temp_s, den_s, pres_s, gas_c, grav, gamma, temp_tp = 288.16, 1.2250, 1.01325E5, 287, 9.81, 1.4, 216.66
        unitList = ["[m]", "[Pa]", "[K]", "[kg/m^2]", "[m/s]"]
    h_geom = float(height)
    lap_rt_1 = (temp_tp - temp_s) / (phase_2)
    lap_rt_2 = (temp_s - temp_tp) / (phase_4 - phase_3)
    pres_1 = pres_s * (temp_tp / temp_s) ** -(grav / (lap_rt_1 * gas_c))
    den_1 = den_s * ((temp_tp / temp_s) ** -(grav / (lap_rt_1 * gas_c) + 1))
    pres_2 = pres_1 * np.exp((-grav / (gas_c * temp_tp)) * (phase_3 - phase_2))
    den_2 = den_1 * np.exp((-grav / (gas_c * temp_tp)) * (phase_3 - phase_2))
    h_geop = round((e_radius / (e_radius + h_geom)) * h_geom, 4)
    if h_geop <= phase_2:
        region = phase_1
    elif h_geop > phase_2 and h_geop <= phase_3:
        region = phase_2
    else:
        region = phase_3
    if region == phase_2:
        temp = temp_tp
        pres = pres_1 * np.exp((-grav / (gas_c * temp_tp)) * (h_geop - phase_2))
        den = den_1 * np.exp((-grav / (gas_c * temp_tp)) * (h_geop - phase_2))
    elif region == phase_1:
        temp = temp_s + lap_rt_1 * (h_geop)
        pres = pres_s * (temp / temp_s) ** -(grav / (lap_rt_1 * gas_c))
        den = den_s * (temp / temp_s) ** -(grav / (lap_rt_1 * gas_c) + 1)
    else:
        temp = temp_tp + lap_rt_2 * (h_geop - phase_3)
        pres = pres_2 * (temp / temp_tp) ** -(grav / (lap_rt_2 * gas_c))
        den = den_2 * (temp / temp_tp) ** -(grav / (lap_rt_2 * gas_c) + 1)
    speed_o_sound = np.sqrt(gamma * gas_c * temp)
    temp = round(temp,4)
    pres = "{:5e}".format(pres)
    den = "{:5e}".format(den)
    
    return h_geop, pres, temp, den, speed_o_sound, unitList
