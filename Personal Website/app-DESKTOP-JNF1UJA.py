from flask import Flask, request, render_template, url_for, session
from datetime import timedelta
import numpy as np
from math import *

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


def nacaCalculate(value, column):
    M1subsonic = np.linspace(0,1,101)
    M1subsonic = np.delete(M1subsonic, 0)
    M1sonic = np.linspace(1,15,1401)
    g = 1.4
    def sigfig(a_number, sigs):
        if a_number == 0:
            return 0.0
        else:
            return round(a_number, sigs - int(floor(log10(abs(a_number))))-1)

    def closest(c_list, a_number):
        def abs_difference(list_value):
            if list_value == "-" or list_value == "N/A":
                return 10E6
            else:
                return abs(list_value - a_number)
        closest_value = min(c_list, key=abs_difference)
        return closest_value

    p_pt=[sigfig((1+M**2/5)**(-7/2), 4) for M in M1subsonic]
    rho_rhot=[sigfig((1+M**2/5)**(-5/2), 4) for M in M1subsonic]
    T_Tt = [sigfig((1+M**2/5)**(-1), 4) for M in M1subsonic]
    beta = [sigfig(sqrt(abs(M**2-1)), 4) for M in M1subsonic]
    q_pt = [sigfig((7/10*M**2*(1+(g-1)/2*M**2)**(-7/2)), 4) for M in M1subsonic]
    A_As = [sigfig(1 / (216/125 * M * (1+M**2/5)**(-3)), 4) for M in M1subsonic]
    V_as = [sigfig(np.sqrt((6*M**2/5*(1+M**2/5)**(-1))), 4) for M in M1subsonic]

    nu = ['N/A' for M in M1subsonic]
    mu = ['N/A' for M in M1subsonic]
    M2 = ['N/A' for M in M1subsonic]
    p2_p1 = ['N/A' for M in M1subsonic]
    rho2_rho1 = ['N/A' for M in M1subsonic]
    T2_T1 = ['N/A' for M in M1subsonic]
    pt2_pt1 = ['N/A' for M in M1subsonic]
    p1_pt2 = ['N/A' for M in M1subsonic]
    for M in M1sonic:
        p_pt.append( sigfig((1+M**2/5)**(-7/2),4) )
        rho_rhot.append( sigfig((1+M**2/5)**(-5/2),4))
        T_Tt.append( sigfig((1+M**2/5)**(-1),4))
        beta.append( sigfig(np.sqrt(M**2-1),4))
        q_pt.append( sigfig((7/10*M**2*(1+(g-1)/2*M**2)**(-7/2)),4))
        A_As.append( sigfig(1 / (216/125 * M * (1+M**2/5)**(-3)),4))
        V_as.append( sigfig(np.sqrt((6*M**2/5*(1+M**2/5)**(-1))),4))
        
        nu.append('-')
        mu.append('-')

        M2.append( sigfig(np.sqrt((M**2+5)/(7*M**2-1)),4))
        p2_p1.append( sigfig((7*M**2-1)/6,4))
        rho2_rho1.append( sigfig(6*M**2/(M**2+5),4))
        T2_T1.append( sigfig(((7*M**2-1)*(M**2+5))/(36*M**2),4))
        pt2_pt1.append( sigfig(((6*M**2)/(M**2+5))**(7/2) * (6/(7*M**2-1))**(5/2),4))
        p1_pt2.append( sigfig(1 / ( (6*M**2/5)**(7/2) * (6/(7*M**2-1))**(5/2)),4))

    MTotal = []
    for i in M1subsonic:
        MTotal.append(sigfig(i,4))
    for i in M1sonic:
        MTotal.append(sigfig(i,4))
    if column == "c7a":
        A_As[100:] = ["-" for i in M1sonic]
    elif column == "c7b":
        A_As[0:100] = ["-" for i in M1subsonic]

    columnDict = {"c1":MTotal, "c2":p_pt, "c3":rho_rhot, "c4":T_Tt, "c5":beta, "c6":q_pt, "c7a":A_As,"c7b":A_As, "c8":V_as, "c9":nu, "c10":mu, "c11":M2, "c12":p2_p1, "c13":rho2_rho1, "c14":T2_T1, "c15":pt2_pt1, "c16":p1_pt2}
    index_val = columnDict[column].index(closest(columnDict[column], value))

    return MTotal[index_val], p_pt[index_val], rho_rhot[index_val], T_Tt[index_val], beta[index_val], q_pt[index_val], A_As[index_val], V_as[index_val], nu[index_val], mu[index_val], M2[index_val], p2_p1[index_val], rho2_rho1[index_val], T2_T1[index_val], pt2_pt1[index_val], p1_pt2[index_val]


# Flask constructor
app = Flask(__name__) 
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classes")
def classes():
    return render_template("classes.html")

@app.route("/stanAtmos", methods =["POST", "GET"])
def standard_atmos():
    if request.method == "POST":
        session.permanent = True
        height = float(request.form["heightValue"])
        unit = request.form["units"]
        output = standard_atmos_calculations(height, unit)
        
        return render_template("stanAtmos.html", objects=output)
    return render_template("stanAtmos.html")

@app.route("/naca1135",methods=["GET", "POST"])
def naca():
    if request.method == "POST":
        session.permanent = True
        col = request.form["column"]
        col_val = float(request.form["columnValue"])
        output = nacaCalculate(col_val, col)
        return render_template("naca1135.html", objects=output)
    return render_template("naca1135.html")

if __name__=='__main__':
    app.run()