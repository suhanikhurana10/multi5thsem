from nlp_engine import text_to_image
import os

def generate_visuals_from_user():
    print("=== Text to Visual Generator ===")
    print("Type any question or instruction to convert into a visual format.")
    print("Enter 'exit' to stop.\n")

    output_folder = "generated_images"
    os.makedirs(output_folder, exist_ok=True)

    while True:
        user_input = input("Enter question: ")
        if user_input.lower() == "exit":
            print("Exiting...")
            break

        print(f"\nProcessing: {user_input}")
        img_path = text_to_image(user_input, output_folder)
        if img_path:
            print(f"✔ Visual generated: {img_path}\n")
        else:
            print("⚠ This question cannot be visualized yet.\n")

if __name__ == "__main__":
    generate_visuals_from_user()
