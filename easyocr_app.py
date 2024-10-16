# -*- coding: utf-8 -*-
"""EasyOCR_app

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1leipeBrfEpbBYKIKnBMFzRxdONiIWxXe
"""

import streamlit as st
import easyocr
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

# Preprocessing function to apply contrast stretching
def contrast_stretching(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    # Stretch contrast of the grayscale image
    xp = [0, 64, 128, 192, 255]
    fp = [0, 16, 128, 240, 255]
    stretched_image = np.interp(gray, xp, fp).astype(np.uint8)

    return stretched_image

# Function to print the whole detected text in a single line
def print_full_text(results):
    full_text = " ".join([text for (_, text, _) in results])
    return full_text

# Streamlit app
st.title("OCR with Contrast Stretching")

# Upload an image
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Apply contrast stretching
    enhanced_image = contrast_stretching(image)

    # Show the contrast-stretched image using Matplotlib
    st.write("Contrast-Stretched Image")
    fig, ax = plt.subplots()
    ax.imshow(enhanced_image, cmap='gray')
    ax.axis('off')
    st.pyplot(fig)  # Use st.pyplot to display the grayscale image with Matplotlib

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'], gpu=False)

    # Perform OCR on the enhanced image
    results = reader.readtext(enhanced_image)

    # Display individual results with bounding boxes
    st.write("Detected Text with Confidence:")
    for (bbox, text, prob) in results:
        st.write(f"Detected Text: {text} (Confidence: {prob:.4f})")

    # Print the full detected text in a single line
    full_text = print_full_text(results)
    st.write("Full Detected Text in Single Line:")
    st.write(full_text)

    # Draw bounding boxes on the original image
    image_np = np.array(image)
    for (bbox, text, prob) in results:
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        cv2.rectangle(image_np, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image_np, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the image with bounding boxes
    st.write("Image with Detected Text and Bounding Boxes:")
    st.image(image_np, use_column_width=True)