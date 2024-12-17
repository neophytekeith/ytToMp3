import streamlit as st
import yt_dlp
import os
from moviepy.editor import AudioFileClip

# Function to download and convert YouTube video to MP3
def download_and_convert_to_mp3(url, output_path="."):
    try:
        # Set up yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',  # Download the best audio
            'outtmpl': os.path.join(output_path, 'temp_audio.%(ext)s'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            st.write(f"Downloading: {url}")
            ydl.download([url])

        # Convert the downloaded audio to MP3 (320 kbps)
        audio_file = os.path.join(output_path, 'temp_audio.webm')  # WebM is typical for audio downloads
        output_mp3 = os.path.join(output_path, 'output.mp3')
        st.write(f"Converting {audio_file} to MP3")

        # Convert to MP3 with ffmpeg (320 kbps)
        audio_clip = AudioFileClip(audio_file)
        audio_clip.write_audiofile(output_mp3, codec='mp3', bitrate='320k')

        # Clean up the temporary file
        audio_clip.close()
        os.remove(audio_file)
        st.write(f"Conversion complete: {output_mp3}")
        return output_mp3
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Streamlit App
def main():
    st.title("YouTube to MP3 Converter")
    st.write("Enter a YouTube video URL to download and convert it to MP3.")

    # Input field for YouTube URL
    url = st.text_input("YouTube URL", "")

    # Button to trigger the download and conversion
    if st.button("Download and Convert"):
        if url.strip():
            st.write("Processing your request...")
            output_path = "."  # Directory to save the MP3 file
            output_file = download_and_convert_to_mp3(url, output_path)
            if output_file:
                st.success("Download and conversion complete!")
                # Provide a download link for the MP3 file
                with open(output_file, "rb") as file:
                    btn = st.download_button(
                        label="Download MP3",
                        data=file,
                        file_name="output.mp3",
                        mime="audio/mpeg"
                    )
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
