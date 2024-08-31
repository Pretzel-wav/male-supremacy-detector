from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import spacy
import pandas as pd

nlp = spacy.load('en_core_web_lg')
youtube_url = 'https://youtu.be/k1oXx4delIY'
youtube_id = YouTube(youtube_url).video_id

def get_transcript_from_youtube(youtube_id, output_path = None):
    transcript = YouTubeTranscriptApi.get_transcript(youtube_id)
    if output_path:
        with open(output_path, 'w') as f:
            f.write(str(transcript))
    return transcript

def get_nlp_doc(text):
    return nlp(text)

ScaleItems = []
class ScaleItem:
    def __init__(self, id, subscale, text):
        self.id = id
        self.subscale = subscale
        self.text = text
        self.doc = get_nlp_doc(text)
        ScaleItems.append(self)

af01 = ScaleItem('AF01', 'Anti-Feminism', 'Feminism is about hating men')
af02 = ScaleItem('AF02', 'Anti-Feminism', 'Modern society prioritizes women over men')
af03 = ScaleItem('AF03', 'Anti-Feminism', 'Feminists are unattractive')
af04 = ScaleItem('AF04', 'Anti-Feminism', 'Women use feminism to gain an unfair advantage over men')
af05 = ScaleItem('AF05', 'Anti-Feminism', 'Feminists are seeking to control men')

fd06 = ScaleItem('FD06', 'Female Dishonesty', 'If a man commits to a woman in a romantic relationship, she gets the upper hand')
fd07 = ScaleItem('FD07', 'Female Dishonesty', 'In a relationship, women are less trustworthy than men')
fd08 = ScaleItem('FD08', 'Female Dishonesty', 'Men in romantic relationships need to be constantly on guard for cheating')
fd09 = ScaleItem('FD09', 'Female Dishonesty', 'Women have a biological drive to cheat on their partners')
fd10 = ScaleItem('FD10', 'Female Dishonesty', 'You can\'t trust women to be faithful in relationships')

wla11 = ScaleItem('WLA11', 'Women Like Alphas', 'Women are biologically driven to seek out the highest status man possible')
wla12 = ScaleItem('WLA12', 'Women Like Alphas', 'Women cannot help being attracted to rich men')
wla13 = ScaleItem('WLA13', 'Women Like Alphas', 'Women cannot help but be attracted to those who are higher in status than they are')
wla14 = ScaleItem('WLA14', 'Women Like Alphas', 'Women are not attracted to men who have a low social status')
wla15 = ScaleItem('WLA15', 'Women Like Alphas', 'Women are attracted to high status men')

transcript = get_transcript_from_youtube(youtube_id, 'transcript_timestamps.txt') # text and timestamps
text = ' '.join([segment['text'] for segment in transcript])
with open(f'transcripts/{youtube_id}.txt', 'w') as f:
    f.write(text)
doc = nlp(text)
print(f'First 100 words of transcript:\n{doc.words[:100]}')

scores = {}
item_ids = [item.id for item in ScaleItems]
for sent in doc.sents:
    scores[sent.text] = [sent.similarity(item.doc) for item in ScaleItems]

df = pd.DataFrame.from_dict(scores, orient='index', columns=item_ids)
df.index.name = 'sentence'
for subscale in ['AF', 'FD', 'WLA']:
    subscale_cols = [col for col in df.columns if subscale in col]
    df[f'{subscale}_MEAN'] = df[subscale_cols].mean(axis=1)
    df[f'{subscale}_SUM'] = df[subscale_cols].sum(axis=1)
    df[f'{subscale}_MAX'] = df[subscale_cols].max(axis=1)
df['TOTAL_MEAN'] = df[item_ids].mean(axis=1)
df['TOTAL_SUM'] = df[item_ids].sum(axis=1)
df.to_csv(f'scores/{youtube_id}.csv', sep='\t')

