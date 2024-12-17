import streamlit as st
from yt_dlp import YoutubeDL
from moviepy import AudioFileClip
import os

# Function to download audio and convert to MP3
def download_and_convert_to_mp3(url, output_path="."):
    try:
        # Set options for yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, 'temp_audio.%(ext)s'),
        }

        with YoutubeDL(ydl_opts) as ydl:
            st.write(f"Downloading audio from: {url}")
            ydl.download([url])

        # Check for downloaded file
        audio_file = os.path.join(output_path, 'temp_audio.webm')  # Default extension
        if not os.path.exists(audio_file):
            st.error("Failed to download audio file.")
            return None

        # Convert to MP3 using moviepy
        st.write("Converting audio to MP3...")
        output_mp3 = os.path.join(output_path, 'output.mp3')
        audio_clip = AudioFileClip(audio_file)
        audio_clip.write_audiofile(output_mp3, codec="libmp3lame", bitrate="320k")
        audio_clip.close()

        # Cleanup temporary file
        os.remove(audio_file)
        st.success(f"Conversion complete! File saved at: {output_mp3}")
        return output_mp3
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Streamlit interface
st.title("YouTube to MP3 Converter")
url = st.text_input("Enter YouTube URL:")
if st.button("Download and Convert"):
    if url:
        output_file = download_and_convert_to_mp3(url)
        if output_file:
            st.success("File conversion successful!")
    else:
        st.error("Please enter a valid YouTube URL.")
