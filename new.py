import os
import cv2
import string
import tkinter as tk
from tkinter import simpledialog

# Load the image
def load_image(image_path):
    return cv2.imread(image_path)

# Embed the message in the image
def embed_message(image, message, char_to_int):
    n, m, z = 0, 0, 0

    for char in message:
        image[n, m, z] = char_to_int.get(char, 0)
        n, m, z = n + 1, m + 1, (z + 1) % 3  # Rotate through RGB channels

    return image

# Save the image with the embedded message
def save_embedded_image(image, output_path):
    cv2.imwrite(output_path, image)
    print("Message embedded successfully!")

# Extract the hidden message from the image
def extract_message(image, int_to_char, message_length):
    extracted_message = ""
    n, m, z = 0, 0, 0

    for _ in range(message_length):
        extracted_message += int_to_char.get(image[n, m, z], ' ')
        n, m, z = n + 1, m + 1, (z + 1) % 3  # Rotate through RGB channels

    return extracted_message

# Function to handle embedding and extraction
def handle_embed_extract():
    root = tk.Tk()
    root.withdraw()

    image_path = simpledialog.askstring("Input", "Enter the path of the image:")
    image = load_image(image_path)

    secret_message = simpledialog.askstring("Input", "Enter the secret message:")

    char_to_int = {char: i for i, char in enumerate(string.printable)}
    int_to_char = {i: char for char, i in char_to_int.items()}

    image_with_message = embed_message(image.copy(), secret_message, char_to_int)
    
    encryption_password = simpledialog.askstring("Input", "Enter encryption password:")

    output_path = simpledialog.askstring("Input", "Enter the output image path:")
    
    save_embedded_image(image_with_message, output_path)

    os.system( f"Start {output_path}" )#shows encrypted image

    decryption_password = simpledialog.askstring("Input", "Enter the decryption password:")

    message_length = len(secret_message)
    extracted_message = extract_message(image_with_message, int_to_char, message_length)

    if decryption_password == encryption_password:
        print("Decrypted Message:", extracted_message)
    else:
        print("Invalid password")

if __name__ == "__main__":
    handle_embed_extract()
