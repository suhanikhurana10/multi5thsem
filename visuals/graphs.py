import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

# ---------------- Linear Graph ----------------
def draw_linear_graph(points=None, output_path="linear_graph.png"):
    plt.figure()
    if points and len(points) >= 2:
        # Fit a line through points
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        
        # Calculate slope (m) and intercept (c)
        coeffs = np.polyfit(x_coords, y_coords, 1)
        m, c = coeffs
        
        # Determine plot range
        x_min, x_max = min(x_coords) - 2, max(x_coords) + 2
        x = np.linspace(x_min, x_max, 100)
        y = m * x + c
        
        plt.plot(x, y, label=f"y = {m:.2f}x + {c:.2f}")
        plt.scatter(x_coords, y_coords, color='red', zorder=5) # Plot original points
        plt.title(f"Line through ({points[0][0]},{points[0][1]}) and ({points[1][0]},{points[1][1]})")
    else:
        # Default example
        x = np.linspace(-10, 10, 200)
        y = 2 * x + 1 
        plt.plot(x, y, label="y=2x+1")
        plt.title("Linear Graph")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    return output_path


# ---------------- Parabola ----------------
def draw_parabola(points=None, output_path="parabola.png"):
    plt.figure()
    if points is None or len(points) < 2:
        # default parabola
        x = np.linspace(-10, 10, 200)
        y = x**2
    else:
        # Fit a quadratic: y = ax^2 + bx + c
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]
        coeffs = np.polyfit(x_coords, y_coords, 2)  # returns [a,b,c]
        a, b, c = coeffs
        x = np.linspace(min(x_coords)-1, max(x_coords)+1, 200)
        y = a*x**2 + b*x + c

    plt.plot(x, y, label="Parabola")
    
    if points is not None:
        # Plot points for reference
        px = [p[0] for p in points]
        py = [p[1] for p in points]
        plt.scatter(px, py, color='red', label='Points')

    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Parabola")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    return output_path


# ---------------- Hyperbola ----------------
def draw_hyperbola(output_path="hyperbola.png"):
    plt.figure()
    x = np.linspace(0.1, 10, 200)
    y = 1 / x  # example hyperbola
    plt.plot(x, y, label="y=1/x")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Hyperbola")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------------- Bar Graph ----------------
def draw_bar_graph(data=[5,3,7,2], output_path="bar_graph.png"):
    plt.figure()
    x = np.arange(len(data))
    plt.bar(x, data, color='skyblue')
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.title("Bar Graph")
    plt.grid(True, axis='y')
    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------------- Pie Chart ----------------
def draw_pie_chart(data=[30, 20, 50], labels=None, output_path="pie_chart.png"):
    plt.figure()
    if not labels or len(labels) != len(data):
        labels = [f"Item {i+1}" for i in range(len(data))]
    
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title("Pie Chart")
    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------------- Histogram ----------------
def draw_histogram(data, output_path="histogram.png"):
    plt.figure()
    # Default to sample normal distribution if no data
    if not data:
        data = np.random.randn(1000)
        
    plt.hist(data, bins=10, color='skyblue', edgecolor='black')
    plt.title("Histogram")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------------- General Function Plotter ----------------
def draw_generic_function(expression_str, output_path="function_plot.png"):
    try:
        x = sp.symbols('x')
        expr = sp.sympify(expression_str)
        f = sp.lambdify(x, expr, "numpy")
        
        x_vals = np.linspace(-10, 10, 400)
        y_vals = f(x_vals)

        # Broadcast if scalar
        if np.isscalar(y_vals):
           y_vals = np.full_like(x_vals, y_vals)

        plt.figure()
        plt.plot(x_vals, y_vals, label=f"y = {expression_str}")
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.title(f"Plot of {expression_str}")
        plt.legend()
        plt.grid(True)
        plt.savefig(output_path)
        plt.close()
        return output_path
    except Exception as e:
        print(f"Function plot error: {e}")
        return None

# ---------------- Scatter Points ----------------
def plot_points(output_path="points.png"):
    plt.figure()
    x = np.random.randint(-10,10,10)
    y = np.random.randint(-10,10,10)
    plt.scatter(x, y, color='purple')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Scatter Points")
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    return output_path
