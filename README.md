# Jackson Bland - TAMU Aero based Webapp and Resume
My aim with this webapp was to expand on pieces of code that I have written while enrolled in Texas A&M in a visual aspect. In this way they might become more usable and maybe even be used by others students to aid in their studies. 

I also wanted to be able to write down an overview of my college career and what I experienced in each class, while providing a broader dive into my resume bullet points.
# Running the Webapp
I plan to eventually turn this into an actual webpage though I am unsure what I want the domain name to be. You can clone the repository using github and run 
```bash
app.py 
```
Or, having atleast python 3.7 installed
```bash
git clone <repository url>
```
then run
```bash
app.py 
```
# Viewing the Webapp
Go to `http://127.0.0.1:5000`

## Calculators
### Newton Method Calculator
For those unfamiliar, below is the equation for the simple root finding algorithm known as Newtons Method
$$ x_{i+1} = x_i - \frac{f(x_i)}{f'(x_i)}$$
This basic root finding algorthim may not be the fanciest or the fastest but atleast in my undergraduate studies, it has been the most used. I have personally used it in many assignments, quizzes, exams and for each of those that code was needed I always seemed to misplace my previous version and when I did find it, it was written pourly and not universal. Though there are libraries that have newton method as functions, we were never allowed to use such so I decided to show off the universal one I greated.

To use this feature, the user must input the equation in the correct form, $f(x)=0$, then give the variable that will be iterated over, $x$, as well as the initial guess, $x_0$. Other options are to change the tolerance and/or the max number of iterations. This can be used to either test how quickly the initial guess converges or limit the iterations to see how the values change from one to another. All of this culminates into a universal newton method calculator that gives the final itertion count and the final value of the root. These are then illustrated on a graph that shows the general area of the graph near the root and highlights the iterations as they converge to a final solution. 


### NACA 1135 Calculator
I am not sure if many aerospace programs use the NACA 1135 as we have, but these tables are used extensivly here to learn about shock waves and supersonic flight. For those who are unfamiliar, these tables provide great insights into the flow you are dealing with through many differnet variable values per row. Though these tables are a lifesaver, they are very tendious to use, especially when using paper versions. 

This feature allows the user to look up any value of any variable through a variety to dropdown selections and outputs all other values associated with that row. 

### Standard Atmosphere Calculator

Anybody who has ever needed to use a standard atmosphere table will know that they are slightly infuriating. Hundreds if not thousands of heights in metric and engineering units can create quite to pain in the rear when using paper tables, and most online tables are old pdf's that are either hard to read, have cutoff measuremetnts or have to large of margins between measurements. 

I beleive this feature provides an easy to use solution for all of these problems. Instead of a table system this simple search system allows the user to find all values relating to any geopotential height in either metric or engineering units.

Results
- Geopotential Height
- Pressure
- Temperature
- Density
- Speed of Sound
