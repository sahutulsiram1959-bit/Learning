import streamlit as st
import requests
from datetime import datetime
import time
from io import BytesIO
import zipfile
from PIL import Image, ImageDraw, ImageFont

# =========================
# Streamlit Page Config
# =========================
st.set_page_config(
    page_title="📸 Auto Screenshot Tool",
    page_icon="🌌",
    layout="centered"
)

# =========================
# Background
# =========================
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&w=1950&q=80");
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Title
# =========================
st.markdown("<h1 style='text-align:center;color:white;'>📸 Auto Screenshot Tool</h1>", unsafe_allow_html=True)
st.write("")

# =========================
# Inputs
# =========================
url = st.text_input("Enter URL (with https://)", placeholder="https://example.com")
interval = st.number_input("Interval (seconds)", min_value=1, value=5)
count = st.number_input("Number of screenshots", min_value=1, value=10)
width = st.number_input("Screenshot width (px)", min_value=200, value=1280)

# =========================
# Start Capture
# =========================
if st.button("Start Capture"):
    if not url:
        st.error("❌ Enter a valid URL")
    else:
        st.info(f"Capturing {count} full-page screenshots every {interval} seconds...")

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for i in range(count):
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"screenshot_{timestamp}.png"
                # Full-page capture: remove crop parameter
                api_url = f"https://image.thum.io/get/width/{width}/{url}"

                try:
                    response = requests.get(api_url)
                    if response.status_code == 200:
                        # Add watermark
                        img = Image.open(BytesIO(response.content)).convert("RGB")
                        draw = ImageDraw.Draw(img)
                        font = ImageFont.load_default()
                        text = f"{timestamp}"
                        draw.text((10, img.height - 20), text, fill="white", font=font)

                        # Save to in-memory ZIP
                        img_bytes = BytesIO()
                        img.save(img_bytes, format="PNG")
                        zip_file.writestr(filename, img_bytes.getvalue())

                        # Show in app
                        st.image(img, caption=filename)
                        st.write(f"Captured {i+1}/{count}")
                    else:
                        st.error(f"Failed to get screenshot {i+1}")
                except Exception as e:
                    st.error(f"Error: {e}")

                if i < count - 1:
                    time.sleep(interval)

        # Download ZIP
        zip_buffer.seek(0)
        st.download_button(
            "💾 Download All Screenshots as ZIP",
            data=zip_buffer,
            file_name="screenshots.zip",
            mime="application/zip"
        )

        st.success("✅ All screenshots captured and ready to download!")
