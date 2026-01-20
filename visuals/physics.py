import matplotlib.pyplot as plt

# ---------- Force Diagram ----------
def draw_force_diagram(force_value=10, direction="up", output_path="force.png"):
    """
    Draw a box with a force arrow applied in a given direction.
    direction: 'up', 'down', 'left', 'right'
    """
    plt.figure(figsize=(5,5))
    ax = plt.gca()

    # Draw box
    box_width = 1
    box_height = 1
    box = plt.Rectangle((0, 0), box_width, box_height, fill=True, color='lightgray')
    ax.add_patch(box)

    # Determine arrow based on direction
    if direction.lower() == "up":
        start_x, start_y, dx, dy = box_width/2, box_height, 0, force_value/5
        text_x, text_y = start_x + 0.1, start_y + dy/2
    elif direction.lower() == "down":
        start_x, start_y, dx, dy = box_width/2, 0, 0, -force_value/5
        text_x, text_y = start_x + 0.1, start_y + dy/2
    elif direction.lower() == "right":
        start_x, start_y, dx, dy = box_width, box_height/2, force_value/5, 0
        text_x, text_y = start_x + dx/2, start_y + 0.1
    elif direction.lower() == "left":
        start_x, start_y, dx, dy = 0, box_height/2, -force_value/5, 0
        text_x, text_y = start_x + dx/2, start_y + 0.1
    else:  # default up
        start_x, start_y, dx, dy = box_width/2, box_height, 0, force_value/5
        text_x, text_y = start_x + 0.1, start_y + dy/2

    # Draw arrow
    ax.arrow(start_x, start_y, dx, dy, head_width=0.1, head_length=0.2, fc='red', ec='red', length_includes_head=True)
    ax.text(text_x, text_y, f"{force_value} N", color='red', fontsize=12)

    # Plot settings
    ax.set_xlim(-2, 5)
    ax.set_ylim(-2, 5)
    ax.set_aspect('equal')
    plt.title(f"Force applied to a box ({direction})")
    plt.axis('off')

    plt.savefig(output_path)
    plt.close()
    return output_path

# ---------- Motion Vector ----------
def draw_motion_vector(direction="right", output_path="motion.png"):
    """
    Draw a motion arrow (left or right) with a box
    """
    plt.figure(figsize=(5,3))
    ax = plt.gca()

    # Draw box
    box_width = 1
    box_height = 1
    box = plt.Rectangle((0, 0), box_width, box_height, fill=True, color='lightblue')
    ax.add_patch(box)

    # Draw arrow based on direction
    if direction.lower() == "right":
        ax.arrow(box_width, box_height/2, 1, 0, head_width=0.2, head_length=0.3, fc='green', ec='green', length_includes_head=True)
        ax.text(box_width + 0.5, box_height/2 + 0.1, "Motion →", color='green', fontsize=12)
    elif direction.lower() == "left":
        ax.arrow(0, box_height/2, -1, 0, head_width=0.2, head_length=0.3, fc='green', ec='green', length_includes_head=True)
        ax.text(-1, box_height/2 + 0.1, "← Motion", color='green', fontsize=12)

    ax.set_xlim(-2, 3)
    ax.set_ylim(0, 2)
    ax.set_aspect('equal')
    plt.title("Motion Vector")
    plt.axis('off')

    plt.savefig(output_path)
    plt.close()
    return output_path
