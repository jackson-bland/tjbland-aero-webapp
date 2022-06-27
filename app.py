from flask import Flask, Response, request, render_template, url_for, session
from datetime import timedelta
import numpy as np
from math import *
import io
from numpy import sin, cos, tan, cosh, tanh, sinh
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from sympy import *
from calculators import *


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

@app.route("/resume")
def resume():
    return render_template("resume.html")


@app.route("/newton",  methods =["POST", "GET"])
def newton():
    if request.method == "POST":
        session.permanent = True
        equ = request.form["newton_equation"]
        variable = request.form["newton_equation_variable"]
        initial = float(request.form["newton_equation_init"])
        if len(request.form["newton_equation_tol"]) < 1 and len(request.form["newton_equation_iter"]) < 1:
            output = newton_calculate(equ, variable, initial)
        elif len(request.form["newton_equation_tol"]) < 1:
            iteration = int(request.form["newton_equation_iter"])
            output = newton_calculate(equ, variable, initial, iterations=iteration)
        elif len(request.form["newton_equation_iter"]) < 1:
            tol = float(request.form["newton_equation_tol"])
            output = newton_calculate(equ, variable, initial, tolerance=tol)
        else:
            iteration = int(request.form["newton_equation_iter"])
            tol = float(request.form["newton_equation_tol"])
            output = newton_calculate(equ, variable, initial, tolerance=tol, iterations=iteration)
        
        return render_template('newton.html', objects = output)
    return render_template("newton.html")

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