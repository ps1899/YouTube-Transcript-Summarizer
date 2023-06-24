# Import all the necessary dependencies
from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from nltk.tokenize import sent_tokenize
from langdetect import detect

application = Flask(__name__)

@application.get('/summary')
def summary_api():
    """
    Summarizes the transcript of a YouTube video.
    
    This function takes a YouTube video URL and an optional max_length parameter as inputs.
    It first retrieves the transcript of the YouTube video.
    If the transcript is longer than 3000 words, it uses extractive summarization (e.g. LSA).
    Otherwise, it uses abstractive summarization.
    
    Parameters:
    - url (str): The URL of the YouTube video.
    - max_length (int, optional): The maximum length of the summary. Defaults to 150.
    
    Returns:
    - str: The summarized transcript.
    - int: HTTP status code (200 for success, 404 for failure).
    """
    url = request.args.get('url', '')
    max_length = int(request.args.get('max_length', 150))
    video_id = url.split('=')[1]

    try:
        transcript = get_transcript(video_id)
    except:
        return "No subtitles available for this video", 404

    # Extractive summarization using LSA or Frequency-based method
    if len(transcript.split()) > 3000:
        summary = extractive_summarization(transcript)
    else:
        summary = abstractive_summarization(transcript, max_length)

    return summary, 200

def is_transcript_english(transcript):
    """
    Detect if the transcript is primarily in English.
    
    :param transcript: The transcript text to be analyzed.
    :return: True if the transcript is primarily in English, False otherwise.
    """
    try:
        language = detect(transcript)
        return language == 'en'
    
    except Exception as e:
        return False


def get_transcript(video_id):
    """
    Fetches and concatenates the transcript of a YouTube video.

    Parameters:
    video_id (str): The ID of the YouTube video.

    Returns:
    str: A string containing the concatenated transcript of the video.

    Raises:
    Exception: If there is an error in fetching the transcript.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        raise e

    transcript = ' '.join([d['text'] for d in transcript_list])
    return transcript

def abstractive_summarization(transcript, max_length):
    """
    Summarizes the given transcript using an abstractive summarization model.
    
    The function employs an NLP pipeline for summarization and applies it to chunks
    of the input transcript. The chunks are processed independently and concatenated
    to form the final summary.
    
    Parameters:
    - transcript (str): The transcript text to be summarized.
    - max_length (int): The maximum length of the summary. It controls how concise
                       the summary should be.

    Returns:
    - summary (str): The summarized text.
    """
    summarizer = pipeline('summarization')
    summary = ''
    for i in range(0, (len(transcript)//1000) + 1):
        summary_text = summarizer(transcript[i * 1000:(i+1) * 1000], max_length=max_length)[0]['summary_text']
        summary = summary + summary_text + ' '
    return summary

def extractive_summarization(transcript):
    """
    Summarizes the input transcript using the Extractive Summarization technique.
    Latent Semantic Analysis (LSA) is used for dimensionality reduction and the sentences are ranked
    based on their singular values. The top-ranked sentences are selected to form the summary.
    
    Parameters:
    - transcript (str): The transcript text to be summarized.
    
    Returns:
    - summary (str): The summarized text.
    """
    sentences = sent_tokenize(transcript)
    
    # Vectorize sentences
    vectorizer = CountVectorizer(stop_words='english')
    X = vectorizer.fit_transform(sentences)
    
    # Perform Truncated SVD for dimensionality reduction
    svd = TruncatedSVD(n_components=1, random_state=42)
    svd.fit(X)
    components = svd.transform(X)
    
    # Rank sentences based on the first singular vector
    ranked_sentences = [item[0] for item in sorted(enumerate(components), key=lambda item: -item[1])]
    
    # Select top sentences for summary
    num_sentences = int(0.4 * len(sentences))  # 20% of the original sentences
    selected_sentences = sorted(ranked_sentences[:num_sentences])
    
    # Compile the final summary
    summary = " ".join([sentences[idx] for idx in selected_sentences])
    return summary


if __name__ == '__main__':
    application.run(debug=True)
