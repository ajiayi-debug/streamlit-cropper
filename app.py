import streamlit as st
import numpy as np
from streamlit_cropper import st_cropper
from PIL import Image

st.header("Cropper Demo with Custom Crop Dimensions and Actual Crop Size")

# --- Sidebar Widgets ---
img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
stroke_width = st.sidebar.number_input(label="Box Thickness", value=3, step=1)

aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}
aspect_ratio = aspect_dict[aspect_choice]

return_type_choice = st.sidebar.radio(label="Return type", options=["Cropped image", "Rect coords"])
return_type_dict = {
    "Cropped image": "image",
    "Rect coords": "box"
}
return_type = return_type_dict[return_type_choice]

# --- Main Area ---
if img_file:
    img = Image.open(img_file)
    
    # Display original image dimensions for reference
    st.write(f"Original Image Dimensions: {img.width}px x {img.height}px")
    
    # ---------- Insert Crop Dimension Inputs ----------
    st.subheader("Insert Crop Dimensions")
    
    # Set default dimensions in session state if not already set.
    if "desired_width" not in st.session_state:
        st.session_state["desired_width"] = img.width // 2
    if "desired_height" not in st.session_state:
        st.session_state["desired_height"] = img.height // 2

    # Inline layout for crop dimensions
    col1, col2, col3 = st.columns([1, 0.1, 1])
    with col1:
        crop_width = st.number_input("Crop Width (px)", value=st.session_state["desired_width"],
                                     min_value=1, max_value=img.width, step=1)
    with col2:
        st.markdown("<h4 style='text-align: center;'> x </h4>", unsafe_allow_html=True)
    with col3:
        crop_height = st.number_input("Crop Height (px)", value=st.session_state["desired_height"],
                                      min_value=1, max_value=img.height, step=1)
    
    if st.button("Apply Crop Dimensions"):
        st.session_state["desired_width"] = crop_width
        st.session_state["desired_height"] = crop_height
        st.success("Crop dimensions updated!")
        st.rerun()  # Re-run to update the cropper with new dimensions

    # ---------- Define Custom Box Algorithm ----------
    # This function tells st_cropper the initial crop box dimensions using your values.
    def my_box_algorithm(img, aspect_ratio=None):
        return {
            "left": 0, 
            "top": 0, 
            "width": st.session_state["desired_width"], 
            "height": st.session_state["desired_height"]
        }
    
    # ---------- Cropper Widget ----------
    st.subheader("Crop the Image")
    if return_type == 'box':
        # If returning box coordinates, the cropper returns a dict.
        rect = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type,
            stroke_width=stroke_width,
            should_resize_image=False
        )
        st.write("Crop Coordinates:", rect)
        # Display actual crop dimensions from the coordinates.
        crop_width_actual = rect.get("width", 0)
        crop_height_actual = rect.get("height", 0)
        st.write(f"Actual Crop Dimensions: {crop_width_actual}px x {crop_height_actual}px")
    else:
        # If returning the cropped image, apply our custom box algorithm.
        cropped_img = st_cropper(
            img,
            realtime_update=realtime_update,
            box_color=box_color,
            aspect_ratio=aspect_ratio,
            return_type=return_type,
            stroke_width=stroke_width,
            box_algorithm=my_box_algorithm,
            should_resize_image=False
        )
        
        st.write("Cropped Image Preview")
        # Calculate and display the crop dimensions from the cropped image.
        crop_width_actual, crop_height_actual = cropped_img.size
        st.write(f"Actual Crop Dimensions: {crop_width_actual}px x {crop_height_actual}px")
        
        # Resize preview for display (optional)
        preview_img = cropped_img.copy()
        preview_img.thumbnail((150, 150))
        st.image(preview_img)
else:
    st.info("Please upload an image to begin.")


