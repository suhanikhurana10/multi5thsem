import spacy
import os
import re

from visuals.geometry import generate_triangle, generate_circle, generate_rectangle
from visuals.physics import draw_force_diagram, draw_motion_vector
from visuals.graphs import (
    draw_linear_graph,
    draw_parabola,
    draw_hyperbola,
    draw_bar_graph,
    plot_points
)
from visuals.derivative import draw_derivative


nlp = spacy.load("en_core_web_sm")

# =====================================================
# Utility Functions
# =====================================================

def extract_numbers(text):
    """
    Extract numbers safely (supports integers & decimals)
    """
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    return [float(n) for n in nums]


def detect_shape(text):
    """
    Detect intent type from input
    """
    text = text.lower()

    # Geometry
    if "triangle" in text:
        return "triangle"
    if "circle" in text or "radius" in text:
        return "circle"
    if "rectangle" in text:
        return "rectangle"

    # Physics
    if "force" in text or "newton" in text:
        return "force"
    if "motion" in text or "velocity" in text:
        return "motion"

    # Calculus
    if "derivative" in text:
        return "derivative"

    # Graphs
    if any(word in text for word in ["graph", "plot", "bar", "points", "parabola", "hyperbola"]):
        return "graph"

    return None


# =====================================================
# Main Controller
# =====================================================

def text_to_image(text, output_folder="generated_images"):

    os.makedirs(output_folder, exist_ok=True)
    shape = detect_shape(text)
    numbers = extract_numbers(text)

    if not shape:
        return None

    # =================== GEOMETRY ===================

    if shape == "triangle":
        path = os.path.join(output_folder, "triangle.png")
        return generate_triangle(output_path=path)

    if shape == "circle":
        radius = numbers[0] if numbers else 5
        path = os.path.join(output_folder, "circle.png")
        return generate_circle(radius=radius, output_path=path)

    if shape == "rectangle":
        l = numbers[0] if len(numbers) > 0 else 6
        w = numbers[1] if len(numbers) > 1 else 4
        path = os.path.join(output_folder, "rectangle.png")
        return generate_rectangle(length=l, width=w, output_path=path)

    # =================== PHYSICS ===================

    if shape == "force":
        value = numbers[0] if numbers else 10
        direction = "up"

        if "left" in text:
            direction = "left"
        elif "right" in text:
            direction = "right"
        elif "down" in text:
            direction = "down"

        path = os.path.join(output_folder, "force.png")
        return draw_force_diagram(force_value=value, direction=direction, output_path=path)

    if shape == "motion":
        direction = "left" if "left" in text else "right"
        path = os.path.join(output_folder, "motion.png")
        return draw_motion_vector(direction=direction, output_path=path)

    # =================== DERIVATIVE ===================

    if shape == "derivative":
        try:
            expr = text.lower().split("of")[1].strip()
            path = os.path.join(output_folder, "derivative.png")
            return draw_derivative(expr, path)
        except:
            return None

    # =================== GRAPHS ===================

    if shape == "graph":
        t = text.lower()

        # Parabola
        if "parabola" in t:
            pts = [(numbers[i], numbers[i+1])
                   for i in range(0, len(numbers)-1, 2)]
            path = os.path.join(output_folder, "parabola.png")
            return draw_parabola(points=pts, output_path=path)

        # Hyperbola
        if "hyperbola" in t:
            pts = [(numbers[i], numbers[i+1])
                   for i in range(0, len(numbers)-1, 2)]
            path = os.path.join(output_folder, "hyperbola.png")
            return draw_hyperbola(points=pts, output_path=path)

        # Scatter points
        if "point" in t:
            path = os.path.join(output_folder, "points.png")
            return plot_points(output_path=path)

        # Bar graph
        if "bar" in t:
            path = os.path.join(output_folder, "bar_graph.png")
            data = numbers if numbers else [5, 3, 7, 2]
            return draw_bar_graph(data=data, output_path=path)

        # Linear graph (default)
        path = os.path.join(output_folder, "linear_graph.png")
        return draw_linear_graph(output_path=path)

    return None
