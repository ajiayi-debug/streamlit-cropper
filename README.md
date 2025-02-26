# Streamlit - Cropper

A Forked version of the original [streamlit-cropper](https://github.com/turner-anderson/streamlit-cropper), with added fixes 
# Fixes:
1) `should_resize_image=False` now works
2) Using manual box_function in box_algorithm will hence work as well
3) Remove stroke width from overall crop dimension

![](./demo.gif)

## Installation

```shell script
pip install streamlit-cropper-fix
```

## Example Usage

```python
import streamlit as st
from streamlit_cropper import st_cropper
from PIL import Image
st.set_option('deprecation.showfileUploaderEncoding', False)

# Upload an image and set some options for demo purposes
st.header("Cropper Demo")
img_file = st.sidebar.file_uploader(label='Upload a file', type=['png', 'jpg'])
realtime_update = st.sidebar.checkbox(label="Update in Real Time", value=True)
box_color = st.sidebar.color_picker(label="Box Color", value='#0000FF')
aspect_choice = st.sidebar.radio(label="Aspect Ratio", options=["1:1", "16:9", "4:3", "2:3", "Free"])
aspect_dict = {
    "1:1": (1, 1),
    "16:9": (16, 9),
    "4:3": (4, 3),
    "2:3": (2, 3),
    "Free": None
}
aspect_ratio = aspect_dict[aspect_choice]

if img_file:
    img = Image.open(img_file)
    if not realtime_update:
        st.write("Double click to save crop")
    # Get a cropped image from the frontend
    cropped_img = st_cropper(img, realtime_update=realtime_update, box_color=box_color,
                                aspect_ratio=aspect_ratio)
    
    # Manipulate cropped image at will
    st.write("Preview")
    _ = cropped_img.thumbnail((150,150))
    st.image(cropped_img)
```

## References
- [streamlit-cropper](https://github.com/turner-anderson/streamlit-cropper)
- [streamlit-drawable-canvas](https://github.com/andfanilo/streamlit-drawable-canvas)

## Acknowledgments

Big thanks to Turner Anderson, zoncrd and yanirs for their contributions