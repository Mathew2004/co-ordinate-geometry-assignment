import os
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, redirect, url_for
import io

app = Flask(__name__)

# Ensure the 'static' directory exists to save the plot images
if not os.path.exists('static'):
    os.mkdir('static')

# Function to check if the equation represents pair of straight lines
def check_pair_of_lines(A, H, B):
    if (H ** 2 - A * B) == 0:
        return True
    return False

# Function to find the equations of two lines
def find_lines(A, H, B, G, F, C):
    line1 = lambda x: (-A * x - G) / H if H != 0 else None
    line2 = lambda x: (-H * x - F) / B if B != 0 else None
    
    # Find the equation of the two lines as strings
    line1_eq = f"y = (-{A}*x - {G}) / {H}" if H != 0 else None
    line2_eq = f"y = (-{H}*x - {F}) / {B}" if B != 0 else None

    return line1, line2, line1_eq, line2_eq

# Visualize the lines and save the plot as an image
def visualize_lines(line1, line2, filename):
    plt.figure(figsize=(8, 8))
    x = np.linspace(-10, 10, 400)
    
    if line1:
        plt.plot(x, line1(x), label='Line 1')
    if line2:
        plt.plot(x, line2(x), label='Line 2')

    plt.legend()
    plt.grid(True)

    # Save the plot to a file in the 'static' directory
    filepath = os.path.join('static', filename)
    plt.savefig(filepath)
    plt.close()
    return filepath

# Home route - displays the form for input
@app.route('/')
def home():
    return render_template('index.html')

# Route to process the form data and display result in result.html
@app.route('/solve', methods=['POST'])
def solve():
    try:
        # Get coefficients from form
        A = float(request.form['A'])
        B = float(request.form['B'])
        C = float(request.form['C'])
        H = float(request.form['H'])
        G = float(request.form['G'])
        F = float(request.form['F'])

        # Check if it's a pair of straight lines
        if check_pair_of_lines(A, H, B):
            # Find the lines and their equations
            line1, line2, line1_eq, line2_eq = find_lines(A, H, B, G, F, C)
            
            # Generate plot and save it as an image file
            filename = 'plot.png'  # Save as a static file
            img_path = visualize_lines(line1, line2, filename)

            return render_template('result.html', 
                                   img_path=img_path, 
                                   equation=f"{A}x^2 + 2*{H}xy + {B}y^2 + 2*{G}x + 2*{F}y + {C} = 0", 
                                   line1_eq=line1_eq, 
                                   line2_eq=line2_eq, 
                                   success=True)
        else:
            return render_template('result.html', img_path=None, equation=None, success=False)
    
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    app.run(debug=True)
