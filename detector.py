from youtube_transcript_api import YouTubeTranscriptApi

youtube_url = 'https://youtu.be/k1oXx4delIY'
youtube_id = youtube_url.split('/')[-1]

def get_transcript_from_youtube(youtube_id, output_path = None):
    transcript = YouTubeTranscriptApi.get_transcript(youtube_id)
    if output_path:
        with open(output_path, 'w') as f:
            f.write(str(transcript))
    return transcript

transcript = get_transcript_from_youtube(youtube_id, 'transcript_timestamps.txt')
print(transcript[0:5])

# concatenate the text from the transcript
text = ' '.join([segment['text'] for segment in transcript])
with open('transcript_text.txt', 'w') as f:
    f.write(text)
print(text[:1000])

