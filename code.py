import os
import yt_dlp
import streamlit as st
import subprocess

# Function to download and convert YouTube video to MP3
def download_and_convert_to_mp3(url):
    try:
        # Set up the download directory
        download_dir = "/tmp"  # Streamlit Cloud uses /tmp for temporary files
        os.makedirs(download_dir, exist_ok=True)

        # Clear any existing temporary files before starting a new conversion
        temp_audio_file = os.path.join(download_dir, 'temp_audio.webm')
        temp_mp3_file = os.path.join(download_dir, 'temp_audio.mp3')
        
        # Remove any existing temporary files
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)
        if os.path.exists(temp_mp3_file):
            os.remove(temp_mp3_file)

        # Add User-Agent header to avoid restrictions
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(download_dir, 'temp_audio.%(ext)s'),  # Set download path
            'quiet': True,  # Suppress unnecessary output
            'extractaudio': True,  # Only extract audio
            'audioquality': 0,  # Best audio quality
            'noplaylist': True,  # Ensure only one video is downloaded (not a playlist)
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info, including the title
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', 'Unknown Title')

            # Show the "Converting to MP3" message with the video title
            st.write(f"Converting '{video_title}' to MP3. Please wait...")

            # Download the audio file
            ydl.download([url])

        # After downloading, check if the file exists
        audio_file = os.path.join(download_dir, 'temp_audio.webm')  # Expected download format
        if not os.path.exists(audio_file):
            st.error(f"Error: The downloaded file {audio_file} was not found.")
            return

        # Use video title for the output filename
        output_mp3 = os.path.join(download_dir, f'{video_title}.mp3')

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
        st.success(f"Conversion successful! You can download your file below:")

        # Provide download link for the user
        with open(output_mp3, "rb") as f:
            st.download_button(
                label="Download MP3",
                data=f,
                file_name=f'{video_title}.mp3',
                mime="audio/mp3"
            )

        # Clear temporary files after conversion
        os.remove(audio_file)  # Remove the temporary audio file
        os.remove(output_mp3)  # Optionally remove the MP3 file after download if desired

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Streamlit UI to input YouTube URL and start the process
st.title("YouTube to MP3 Converter")

# Clear the input field when needed
url = st.text_input("Enter YouTube URL:", key="url")  # Using a key to ensure unique widget

# Button to trigger conversion
if st.button("Download and Convert"):
    if url:
        download_and_convert_to_mp3(url)
    else:
        st.warning("Please enter a valid YouTube URL.")

# "Convert Another" button to refresh and clear temporary files
if st.button("Convert Another"):
    # Clear temporary files before refreshing the input
    temp_files = ["/tmp/temp_audio.webm", "/tmp/temp_audio.mp3"]
    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)
    
    # Reset the URL input field manually
    st.experimental_set_query_params(url="")  # Use query params to reset the URL

    # Re-render the UI to allow another conversion
    st.experimental_rerun()  # This reruns the app and resets everything
