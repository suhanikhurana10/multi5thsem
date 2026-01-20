import matplotlib.pyplot as plt
import numpy as np

# ---------------- Linear Graph ----------------
def draw_linear_graph(output_path="linear_graph.png"):
    x = np.linspace(-10, 10, 200)
    y = 2 * x + 1  # example linear
    plt.plot(x, y, label="y=2x+1")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Linear Graph")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------------- Parabola ----------------
import matplotlib.pyplot as plt
import numpy as np

def draw_parabola(points=None, output_path="parabola.png"):
    """
    Draw a parabola passing through given points.
    points: list of tuples [(x1,y1), (x2,y2), ...]
    If None, plots default y = x^2
    """
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
    x = np.arange(len(data))
    plt.bar(x, data, color='skyblue')
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.title("Bar Graph")
    plt.grid(True, axis='y')
    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------------- Scatter Points ----------------
def plot_points(output_path="points.png"):
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
