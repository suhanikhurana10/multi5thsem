import matplotlib.pyplot as plt
import os
import numpy as np

def generate_triangle(output_path="triangle.png"):
    fig, ax = plt.subplots()
    triangle = plt.Polygon([[0, 0], [1, 0], [0.5, 1]], fill=False, linewidth=2)
    ax.add_patch(triangle)
    ax.set_aspect('equal')
    plt.title("Triangle")
    plt.savefig(output_path)
    plt.close()
    return output_path

def generate_circle(radius=5, output_path="circle.png"):
    fig, ax = plt.subplots()
    circle = plt.Circle((0, 0), radius, fill=False, linewidth=2)
    ax.add_patch(circle)
    
    ax.set_xlim(-radius - 1, radius + 1)
    ax.set_ylim(-radius - 1, radius + 1)
    ax.set_aspect('equal')

    plt.title(f"Circle (r={radius})")
    plt.savefig(output_path)
    plt.close()
    return output_path

def generate_rectangle(length=6, width=4, output_path="rectangle.png"):
    fig, ax = plt.subplots()
    rectangle = plt.Rectangle((0, 0), length, width, fill=False, linewidth=2)
    ax.add_patch(rectangle)
    
    ax.set_xlim(0, length + 1)
    ax.set_ylim(0, width + 1)
    ax.set_aspect('equal')

    plt.title(f"Rectangle ({length} x {width})")
    plt.savefig(output_path)
    plt.close()
    return output_path
