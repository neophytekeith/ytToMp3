import os
import yt_dlp
import streamlit as st
from moviepy.editor import AudioFileClip

# Function to download and convert YouTube video to MP3
def download_and_convert_to_mp3(url):
    try:
        # Set up yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': './temp_audio.%(ext)s',
        }

        # Create download directory if it doesn't exist
        download_dir = "/tmp"  # Streamlit Cloud uses `/tmp` as the working directory
        os.makedirs(download_dir, exist_ok=True)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.write(f"Downloading: {url}")
            ydl.download([url])

        # Get the downloaded file path
        audio_file = os.path.join(download_dir, 'temp_audio.webm')  # Update this path

        # Check if the file exists
        if not os.path.exists(audio_file):
            st.error(f"Error: The downloaded file {audio_file} was not found.")
            return

        output_mp3 = os.path.join(download_dir, 'output.mp3')
        st.write(f"Converting to MP3: {audio_file} -> {output_mp3}")

        # Use ffmpeg directly to convert the audio to MP3
        command = [
            'ffmpeg',
            '-i', audio_file,
            '-vn',  # Don't process video, just the audio
            '-b:a', '320k',  # Set bitrate to 320 kbps
            output_mp3
        ]
        
        # Run the command using subprocess
        os.system(" ".join(command))  # This ensures ffmpeg is run with the correct path
        
        st.success(f"Conversion successful! Download your file: {output_mp3}")
        st.audio(output_mp3, format='audio/mp3')

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3 Converter")
url = st.text_input("Enter YouTube URL:")

if st.button("Download and Convert"):
    if url:
        download_and_convert_to_mp3(url)
    else:
        st.warning("Please enter a valid YouTube URL.")

# "Convert Another" button to refresh
if st.button("Convert Another"):
    st.experimental_rerun()  # Refresh the app to reset the URL input
