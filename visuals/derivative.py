import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

def draw_derivative(function_str, output_path="derivative.png"):
    """
    Draws a function and its derivative.
    Example input: "2*x**2 + 5"
    """

    x = sp.symbols('x')

    try:
        # Convert string → symbolic expression
        expr = sp.sympify(function_str)

        # Derivative
        derivative = sp.diff(expr, x)

        # Convert to numerical functions
        f = sp.lambdify(x, expr, "numpy")
        df = sp.lambdify(x, derivative, "numpy")

        # Generate values
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)
        dy_vals = df(x_vals)

        # Plot
        plt.figure(figsize=(7,5))
        plt.plot(x_vals, y_vals, label=f"f(x) = {expr}")
        plt.plot(x_vals, dy_vals, '--', label=f"f'(x) = {derivative}")
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
        plt.legend()
        plt.grid(True)
        plt.title("Function and its Derivative")

        plt.savefig(output_path)
        plt.close()

        return output_path

    except Exception as e:
        print("Derivative error:", e)
        return None
