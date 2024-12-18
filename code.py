import os
import streamlit as st

# Get the port from the environment variable or default to 8501
port = int(os.environ.get('PORT', 8501))

# Run Streamlit on the dynamic port
st.write("Hello, World!")
