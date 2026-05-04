
import matplotlib.pyplot as plt
import textwrap

def generate_concept_card(text, output_path="concept_card.png"):
    """
    Generates a generic 'Concept Card' image for inputs that don't match specific graph types.
    Displays the text nicely formatted.
    """
    plt.figure(figsize=(8, 4))
    
    # Background color
    plt.gca().set_facecolor('#f0f8ff') # AliceBlue
    
    # Add title "Assessment Visual"
    plt.text(0.5, 0.9, "Assessment Content", 
             ha='center', va='center', 
             fontsize=14, fontweight='bold', color='#333333')
             
    # Wrap text
    wrapper = textwrap.TextWrapper(width=60)
    word_list = wrapper.wrap(text=text)
    wrapped_text = "\n".join(word_list)
    
    # Add main text
    plt.text(0.5, 0.5, wrapped_text, 
             ha='center', va='center', 
             fontsize=12, color='#000000',
             bbox=dict(facecolor='white', edgecolor='#cccccc', boxstyle='round,pad=1'))
             
    plt.axis('off')
    
    plt.savefig(output_path, bbox_inches='tight', dpi=100)
    plt.close()
    return output_path
