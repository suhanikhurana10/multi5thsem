try:
    import spacy
except ImportError:
    spacy = None

import os
import re

from visuals.geometry import generate_triangle, generate_circle, generate_rectangle
from visuals.physics import (
    draw_force_diagram, 
    draw_motion_vector, 
    draw_projectile_motion, 
    draw_circuit
)
from visuals.graphs import (
    draw_linear_graph,
    draw_parabola,
    draw_hyperbola,
    draw_bar_graph,
    draw_pie_chart,
    draw_histogram,
    draw_generic_function,
    plot_points
)
from visuals.derivative import draw_derivative
from visuals.scenario_viz import draw_flowchart
from visuals.general import generate_concept_card




try:
    if spacy:
        nlp = spacy.load("en_core_web_sm")
    else:
        nlp = None
except Exception:
    nlp = None


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
    if "force" in text or "newton" in text: return "force"
    if "motion" in text or "velocity" in text: return "motion"
    if "projectile" in text or "trajectory" in text: return "projectile"
    if "circuit" in text or "battery" in text or "resistor" in text: return "circuit"

    # Calculus / Math Functions
    if "derivative" in text or "derive" in text or "differentiate" in text: return "derivative"

    if "plot" in text and "sin" in text or "cos" in text or "tan" in text or "x**" in text or "x^" in text: return "function"

    # Scenarios
    if "flowchart" in text or "process" in text or "steps" in text: return "flowchart"

    # Graphs
    if "pie" in text: return "pie"
    if "hist" in text: return "histogram"
    if "bar" in text: return "bar"
    if any(word in text for word in ["graph", "plot", "points", "parabola", "hyperbola", "line", "chart"]):
        return "graph"

    return None



# =====================================================
# Main Controller
# =====================================================

def text_to_image(text, output_folder="generated_images"):

    print(f"DEBUG: text_to_image called with '{text}'")
    
    os.makedirs(output_folder, exist_ok=True)
    shape = detect_shape(text)
    numbers = extract_numbers(text)
    
    print(f"DEBUG: Detected shape='{shape}', numbers={numbers}")

    if not shape:
        # UNIVERSAL FALLBACK: Generate a Concept Card
        print("DEBUG: No specific shape detected. Generating fallback Concept Card.")
        path = os.path.join(output_folder, "concept_card.png")
        return generate_concept_card(text, output_path=path)



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

    # =================== PHYSICS EXTENDED ===================
    if shape == "projectile":
        # extract velocity and angle?
        # defaults:
        vel, angle = 20, 45
        if len(numbers) >= 1: vel = numbers[0]
        if len(numbers) >= 2: angle = numbers[1]
        path = os.path.join(output_folder, "projectile.png")
        return draw_projectile_motion(angle=angle, velocity=vel, output_path=path)

    if shape == "circuit":
        path = os.path.join(output_folder, "circuit.png")
        return draw_circuit(output_path=path)

    # =================== SCENARIO ===================
    if shape == "flowchart":
        # Extract steps? e.g. "Step 1, Step 2, Step 3"
        steps = ["Start", "Process", "End"]
        # Basic heuristic splits by comma or 'to'
        if "," in text:
            raw_steps = text.split(",")
            steps = [s.strip() for s in raw_steps if s.strip()]
        elif "->" in text:
            raw_steps = text.split("->")
            steps = [s.strip() for s in raw_steps if s.strip()]
            
        path = os.path.join(output_folder, "flowchart.png")
        return draw_flowchart(steps=steps, output_path=path)

    # =================== MATH FUNCTIONS ===================
    if shape == "function":
        # Extract expression
        # usually "plot sin(x)" -> "sin(x)"
        expr = text.lower()
        if "plot" in expr:
            expr = expr.split("plot")[1].strip()
        
        path = os.path.join(output_folder, "function_plot.png")
        return draw_generic_function(expr, output_path=path)


    # =================== DERIVATIVE ===================

    if shape == "derivative":
        try:
            parts = text.lower().split("of")
            if len(parts) < 2:
                print("DEBUG: Could not split 'of' in derivative query")
                return None
            expr = parts[1].strip()
            print(f"DEBUG: Extracting derivative for expression '{expr}'")
            path = os.path.join(output_folder, "derivative.png")
            result = draw_derivative(expr, path)
            print(f"DEBUG: draw_derivative returned '{result}'")
            return result
        except Exception as e:
            print(f"DEBUG: Exception in derivative generation: {e}")
            return None


    # =================== GRAPHS ===================
    
    if shape == "pie":
        path = os.path.join(output_folder, "pie.png")
        return draw_pie_chart(data=numbers if numbers else [10, 20, 30], output_path=path)

    if shape == "histogram":
        path = os.path.join(output_folder, "histogram.png")
        return draw_histogram(data=numbers if numbers else [], output_path=path)
        
    if shape == "bar":
        path = os.path.join(output_folder, "bar_graph.png")
        data = numbers if numbers else [5, 3, 7, 2]
        return draw_bar_graph(data=data, output_path=path)

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

        if "line" in t:
            pts = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers)-1, 2)]
            path = os.path.join(output_folder, "linear_graph.png")
            return draw_linear_graph(points=pts, output_path=path)

        # Scatter points
        if "point" in t:
            path = os.path.join(output_folder, "points.png")
            return plot_points(output_path=path)

        # Bar graph
        if "bar" in t:
            path = os.path.join(output_folder, "bar_graph.png")
            data = numbers if numbers else [5, 3, 7, 2]
            return draw_bar_graph(data=data, output_path=path)
        
        # Default
        path = os.path.join(output_folder, "linear_graph.png")
        return draw_linear_graph(output_path=path)


    # UNIVERSAL FALLBACK (for anything else that falls through)
    print("DEBUG: Fell through specific handlers. Generating fallback Concept Card.")
    path = os.path.join(output_folder, "concept_card.png")
    return generate_concept_card(text, output_path=path)

