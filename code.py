import os
import yt_dlp
import streamlit as st
import subprocess

# Function to download and convert YouTube video to MP3
def download_and_convert_to_mp3(url):
    try:
        # Set up yt-dlp options
        download_dir = "/tmp"  # Streamlit Cloud uses /tmp for temporary files
        os.makedirs(download_dir, exist_ok=True)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, 'temp_audio.%(ext)s'),  # Set download path
            'quiet': True,  # Suppress unnecessary output
            'extractaudio': True,  # Only extract audio
            'audioquality': 0,  # Best audio quality
            'noplaylist': True,  # Ensure only one video is downloaded (not a playlist)
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info, including the title
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')
            st.write(f"Downloading: {video_title}")  # Display video title instead of URL
            ydl.download([url])

        # After downloading, check if the file exists
        audio_file = os.path.join(download_dir, 'temp_audio.webm')  # Expected download format
        if not os.path.exists(audio_file):
            st.error(f"Error: The downloaded file {audio_file} was not found.")
            return

        # Use video title for the output filename
        output_mp3 = os.path.join(download_dir, f'{video_title}.mp3')

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
        subprocess.run(command, check=True)  # This ensures ffmpeg is run with the correct path

        # Display success message and audio player
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
