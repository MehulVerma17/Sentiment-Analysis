# app.py

from flask import Flask, render_template, request
from youtubeCommentScrapper import get_youtube_comments, extract_video_id
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import emoji
import re

app = Flask(__name__)

def sentiment_scores(comment, polarity):
 
    # Creating a SentimentIntensityAnalyzer object.
    sentiment_object = SentimentIntensityAnalyzer()
 
    sentiment_dict = sentiment_object.polarity_scores(comment)
    polarity.append(sentiment_dict['compound'])
 
    return polarity

def get_relevant_comments(comment):
    hyperlink_pattern = re.compile(
	r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    threshold_ratio = 0.65

    relevant_comments = []

    # Inside your loop that processes comments
    for comment_text in comment:

        comment_text = comment_text.lower().strip()

        emojis = emoji.emoji_count(comment_text)

        # Count text characters (excluding spaces)
        text_characters = len(re.sub(r'\s', '', comment_text))

        if (any(char.isalnum() for char in comment_text)) and not hyperlink_pattern.search(comment_text):
            if emojis == 0 or (text_characters / (text_characters + emojis)) > threshold_ratio:
                relevant_comments.append(comment_text)

    # Print the relevant comments
    return relevant_comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch_comments', methods=['POST'])
def fetch_comments():
    url = request.form['link']
    try:
        video_id = extract_video_id(url)
        comments,list_comments = get_youtube_comments(video_id)
        response = None
        polarity = []
        positive_comments = []
        negative_comments = []
        neutral_comments = []

        relevant_comments = get_relevant_comments(list_comments)
        
        for items in relevant_comments:
            polarity = sentiment_scores(items, polarity)
        
            if polarity[-1] > 0.05:
                positive_comments.append(items)

            elif polarity[-1] < -0.05:
                negative_comments.append(items)

            else:
                neutral_comments.append(items)
        
        avg_polarity = sum(polarity)/len(polarity)

        positive_count = len(positive_comments)
        negative_count = len(negative_comments)
        neutral_count = len(relevant_comments)-positive_count-negative_count

        print("average Polarity: ",avg_polarity)
        if avg_polarity > 0.05:
            response = "The Video has got a Positive response"
        elif avg_polarity < -0.05:
            response = "The Video has got a Negative response"
        else:
            response = "The Video has got a Neutral response"
        
        print("The comment with most positive sentiment:", comments[polarity.index(max(
            polarity))], "with score", max(polarity), "and length", len(comments[polarity.index(max(polarity))]))
        print("The comment with most negative sentiment:", comments[polarity.index(min(
            polarity))], "with score", min(polarity), "and length", len(comments[polarity.index(min(polarity))]))

        limited_comments = comments[:10]


        return render_template('index.html', comments=comments, limited_comments=limited_comments, response=response, positive_count=positive_count, negative_count=negative_count, neutral_len=neutral_count)
    
    except ValueError as e:
        return render_template('index.html', error=str(e))
    
    except Exception as e:
        return render_template('index.html', error="An error occurred while fetching comments.")
    


if __name__ == '__main__':
    app.run(debug=True)
