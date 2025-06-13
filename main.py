import os
import textwrap
import ffmpeg
import re

# Fixed paths
VIDEO_PATH = "assets/media.mp4"
AUDIO_PATH = "assets/music.mp3"
DATA_PATH = "data.txt"
FONT_PATH = "assets/fonts/font 1.ttf"  # Single font used
FONT_SIZE = 75
EXPLANATION_SIZE = 60
MARGIN = 100

def sanitize_filename(filename):
    filename = re.sub(r'[^a-zA-Z0-9\s-]', '', filename)  # Remove special characters but keep spaces and hyphens
    filename = filename.strip()  # Keep spaces and hyphens
    return filename[:45]  # Limit length to avoid long filenames

def read_proverbs():
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        content = file.read().strip()
    proverbs = [block.split('\n')[:2] for block in content.split('\n\n')]
    return proverbs

def apply_text_and_audio(proverb, explanation, font_path):
    probe = ffmpeg.probe(VIDEO_PATH)
    duration = float(probe['format']['duration'])
    video_stream = next(s for s in probe['streams'] if s['codec_type'] == 'video')
    width = int(video_stream['width'])
    height = int(video_stream['height'])

    wrapped_proverb = textwrap.fill(proverb, width=25).replace("'", "\'")
    wrapped_explanation = textwrap.fill(explanation, width=30).replace("'", "\'")

    text_x = "(w-text_w)/2"
    text_y = "(h/3)-(text_h/2)"
    explanation_x = "(w-text_w)/2"
    explanation_y = "(h/2)-(text_h/2 - 50)"  # Lowered explanation text slightly
    proverb_tag_x = "w-text_w-50"  # Positioned to the right
    proverb_tag_y = "(h/2) + 250"  # Moved further down to avoid overlap

    output_filename = f"output/{sanitize_filename(proverb)} #Success #Proverbs #DeepQuotes #Shorts #Reels #Inspiration #viral #motivation.mp4"

    video = ffmpeg.input(VIDEO_PATH)
    audio = ffmpeg.input(AUDIO_PATH)

    video = (
        video
        .filter("drawtext", text=wrapped_proverb, fontfile=font_path, fontsize=FONT_SIZE, fontcolor='white',
                box=1, boxcolor='black@0.8', boxborderw=20, x=text_x, y=text_y, enable=f'between(t,0,{duration})')  # Darker transparency
        .filter("drawtext", text=wrapped_explanation, fontfile=font_path, fontsize=EXPLANATION_SIZE, fontcolor='white',
                box=1, boxcolor='black@0.8', boxborderw=20, x=explanation_x, y=explanation_y, enable=f'between(t,0,{duration})')  # Darker transparency
        .filter("drawtext", text="-Proverb", fontfile=font_path, fontsize=40, fontcolor='white',
                box=1, boxcolor='black@0.6', boxborderw=10, x=proverb_tag_x, y=proverb_tag_y, enable=f'between(t,0,{duration})')  # Moved further down
    )

    output = (
        ffmpeg
        .output(video, audio, output_filename, vcodec='h264_nvenc', preset='p5', acodec='aac', audio_bitrate='192k', shortest=None)
    )
    output.run(overwrite_output=True)

def main():
    os.makedirs("output", exist_ok=True)
    proverbs = read_proverbs()
    for proverb, explanation in proverbs:
        apply_text_and_audio(proverb, explanation, FONT_PATH)
    print("Video processing complete!")

if __name__ == "__main__":
    main()

