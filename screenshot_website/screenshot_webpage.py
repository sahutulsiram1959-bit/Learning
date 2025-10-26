import streamlit as st
import requests
from datetime import datetime
import time

st.title("📸 Auto Screenshot Tool")

url = st.text_input("Enter URL (with https://)")
interval = st.number_input("Interval (seconds)", min_value=1, value=5)
count = st.number_input("Number of screenshots", min_value=1, value=10)

if st.button("Start Capture"):
    if not url:
        st.error("❌ Enter a valid URL")
    else:
        st.info(f"Capturing {count} screenshots every {interval} seconds...")
        for i in range(count):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            api_url = f"https://image.thum.io/get/width/1280/crop/800/{url}"
            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    st.image(response.content, caption=filename)
                    st.download_button(
                        f"💾 Download {filename}",
                        data=response.content,
                        file_name=filename,
                        mime="image/png"
                    )
                    st.write(f"Captured {i+1}/{count}")
                else:
                    st.error(f"Failed to get screenshot {i+1}")
            except Exception as e:
                st.error(f"Error: {e}")
            if i < count - 1:
                time.sleep(interval)
        st.success("✅ All screenshots captured!")
