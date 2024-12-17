import streamlit as st
import subprocess
import os
from yt_dlp import YoutubeDL

# Initialize session state for the URL input
if 'url' not in st.session_state:
    st.session_state.url = ''

# Use the correct path for FFmpeg in Streamlit Cloud
FFMPEG_PATH = '/usr/bin/ffmpeg'  # This is where FFmpeg is installed in Streamlit Cloud

def download_audio(url, output_path="."):
    try:
        # Set yt-dlp options to extract the video title and best audio format
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, 'temp_audio.%(ext)s'),
            'noplaylist': True,  # Ensure it's only downloading the single video, not a playlist
            'quiet': True  # Don't show extra output in Streamlit
        }

        # Download the video and get the video info (including title)
        with YoutubeDL(ydl_opts) as ydl:
            st.write(f"Downloading: {url}")
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', 'downloaded_audio')  # Use video title or a fallback name

        # Convert to MP3 using ffmpeg
        input_file = os.path.join(output_path, 'temp_audio.webm')  # WebM is typical for audio downloads
        output_file = os.path.join(output_path, f"{video_title}.mp3")  # Use video title for the MP3 name
        
        # Command to convert using ffmpeg (320 kbps)
        command = [FFMPEG_PATH, "-i", input_file, "-vn", "-b:a", "320k", output_file]
        print(f"Running command: {command}")  # Debugging line
        subprocess.run(command, check=True)

        os.remove(input_file)  # Clean up the temporary WebM file
        st.success(f"Conversion complete! File saved as: {output_file}")
        return output_file
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit app layout
st.title("YouTube to MP3 Converter")

# Input for YouTube URL
url = st.text_input("Enter YouTube URL:", value=st.session_state.url)

# "Download and Convert" button
if st.button("Download and Convert"):
    if url:
        download_audio(url)
    else:
        st.error("Please enter a valid YouTube URL.")

# "Convert Another" button (below the download button)
if st.button("Convert Another"):
    st.session_state.url = ''  # Reset the URL in session state
    st.experimental_rerun()  # Refresh the app to reset the URL input field
