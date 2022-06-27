
# def newton(func, symbol, initial, variables = [[],[]], tolerance = 10E-8, iterations = 100):
# 	"""
# 	Output is a list [final_value, iteration_count]

# 	Input function in python notation as a string
# 		Ex: 'x**2+9-5x'
# 	Denote symbol of differentiation as string
# 	Becareful when using complexe equations involving things such as trig funcitons, if the defined symbol is a letter in a trig function it will cause errors
# 		Ex: 'x'
# 	Denote initial "guess" as float
# 		Ex: 3.1415
# 	If needed input desired/custom tolerance for |x_i+1 - x_i|, default setting to 10E8
# 		Ex: 10E3
# 	Using trig, ALL INPUTS SHOULD BE IN RADIANS and trig functions written as follows
# 		sin(x), cos(x), tan(x), asin(x), acos(x), atan(x)... etc
# 		- I would suggest importing numpy as np and using the numpy pi value
# 			Ex: np.pi	

# 	IMPORTANT ARGUEMENT
# 	----------------------------------------
# 	Putting in float values for all other numbers is quite taxing and may lead to roundoff error.

# 	To eleviate this use the 	variables = 	arguement to input the values for the other variables. 

# 	This is accomplished using a list of 2 lists, the first being a comma seperate list of the variables as strings as they appear in the funciton arguement and the second being the float values of those variables in the same respective index.
# 		Ex: newtonRhapson(func = 'x**3 - M*v**2 - t', symbol = 'x', initial = '2', variables = [['M','v','t'],[100,3.15E-9,43]])
# 	----------------------------------------
	
# 	Default iteration count is set to 100 and is non changable

# 	All trig calculations are in radians so output of calculation is also in radians
# 	"""

# 	y = Symbol(symbol)
# 	if len(variables[0]) > 0:
# 		for var in range(len(variables[0])):
# 			func = func.replace(str(variables[0][var]),str(variables[1][var]))

# 	def f(function_,y_val):
# 		evaluated_f = eval(function_.replace(symbol,str(y_val)))
# 		return evaluated_f

# 	def df(function_,y_val):
# 		evaluated_df = eval(str(diff(function_,y)).replace(symbol,str(y_val)))
# 		return evaluated_df

# 	def plotting(values,function_):
# 		max_val = max(values)
# 		min_val = min(values)
# 		difference_of_vals = max_val-min_val
# 		plotting_tolerance = 0.1*difference_of_vals

# 		plotting_list = np.linspace(min_val-plotting_tolerance, max_val+plotting_tolerance,100)
# 		plotted_function = []
# 		plotted_guesses = []
# 		for i in plotting_list:
# 			plotted_function.append(eval(function_.replace(symbol,str(i))))
# 		for i in values:
# 			plotted_guesses.append(eval(function_.replace(symbol,str(i))))
# 		fig = plt.figure()
# 		graph = fig.add_subplot(1,1,1)
# 		graph.plot(plotting_list,plotted_function,label='Function')
# 		graph.scatter(values,plotted_guesses,marker='o',facecolor='none',linewidths=1,edgecolors='red',label='Iterations')
# 		graph.axhline(0,color='black',linewidth=1)
# 		graph.grid()
# 		graph.legend()
# 		plt.show() 
# 		return

# 	iteration = 0
# 	max_iterations = 100
# 	x_1 = 1E6
# 	check = 1E6
# 	xo = initial

# 	list_iteration_vals = [xo]

# 	while check > tolerance:
# 		x_1 = eval(str(xo - f(func,xo)/df(func,xo)))
# 		check = abs(x_1-xo)
# 		xo = x_1
# 		list_iteration_vals.append(x_1)
# 		iteration += 1
# 		if iteration == max_iterations: 
# 			print(x_1, 'was found after reaching max iterations, I suggest using a different initial condition')
# 			return
# 		elif iteration == iterations:
# 			plotting(list_iteration_vals,func)
# 			return [x_1, iteration]
# 	plotting(list_iteration_vals,func)
# 	return [x_1, iteration]
