import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Load the CSV file
df = pd.read_csv('Review_db - Copy.csv', dtype=str)

# Initialize the VADER sentiment intensity analyzer
sid = SentimentIntensityAnalyzer()

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')

def classify_review_sentiment(review):
    if isinstance(review, str):
        sentences = review.split('.')
        positive_sentences = []
        negative_sentences = []
        neutral_sentences = []
        positive_polarity = 0
        negative_polarity = 0
        neutral_polarity = 0

        for sentence in sentences:
            if sentence.strip():  # Ignore empty sentences
                sentiment_score = sid.polarity_scores(sentence)
                compound_score = sentiment_score['compound']
                if compound_score >= 0.05:
                    positive_sentences.append(sentence.strip())
                    positive_polarity += compound_score
                elif compound_score <= -0.05:
                    negative_sentences.append(sentence.strip())
                    negative_polarity += abs(compound_score)  # Add absolute value for negatives
                else:
                    neutral_sentences.append(sentence.strip())
                    neutral_polarity += 0.5  # Assign a small value for neutral

        positive_reviews = '. '.join(positive_sentences)
        negative_reviews = '. '.join(negative_sentences)
        neutral_reviews = '. '.join(neutral_sentences)

        return positive_polarity, negative_polarity, neutral_polarity, positive_reviews, negative_reviews, neutral_reviews
    else:
        return 0, 0, 0, '', '', ''

def extract_keywords(text):
    if isinstance(text, str):
        # Process the text with spaCy
        doc = nlp(text)
        keywords = []

        # Track previous adjective to pair with the next noun
        prev_adj = None

        for token in doc:
            if token.pos_ == 'ADJ':
                prev_adj = token.text  # Update previous adjective

            elif token.pos_ == 'NOUN':
                if prev_adj:
                    keywords.append(f'{prev_adj} {token.text}')
                    prev_adj = None  # Reset previous adjective
                else:
                    keywords.append(token.text)

        # Join keywords with comma and space
        keywords_str = ', '.join(keywords)

        return keywords_str
    else:
        return ''  # Return empty string if the input is not a string

# Apply the extract_keywords function to the 'Review' column
df['review_keyword'] = df['Review'].apply(extract_keywords)

# Function to analyze the sentiment of each keyword
def analyze_keywords(review_keyword):
    if isinstance(review_keyword, str):
        keywords = review_keyword.split(', ')
        positive_keywords = []
        negative_keywords = []

        for keyword in keywords:
            sentiment_score = sid.polarity_scores(keyword)
            compound_score = sentiment_score['compound']
            if compound_score >= 0.05:
                positive_keywords.append(keyword)
            elif compound_score <= -0.05:
                negative_keywords.append(keyword)

        positive_keywords_str = ', '.join(positive_keywords)
        negative_keywords_str = ', '.join(negative_keywords)

        return positive_keywords_str, negative_keywords_str
    else:
        return '', ''

# Apply the function to analyze keywords and create new columns
df['positive_review_keyword'], df['negative_review_keyword'] = zip(*df['review_keyword'].map(analyze_keywords))

# Apply the function to classify sentiment and extract reviews
df['positive_polarity'], df['negative_polarity'], df['neutral_polarity'], df['positive_review'], df['negative_review'], df['neutral_review'] = zip(*df['Review'].map(classify_review_sentiment))

# Function to determine overall sentiment based on polarity counts
def determine_overall_sentiment(row):
    if row['positive_polarity'] > row['negative_polarity'] and row['positive_polarity'] > row['neutral_polarity']:
        return 'Positive'
    elif row['negative_polarity'] > row['positive_polarity'] and row['negative_polarity'] > row['neutral_polarity']:
        return 'Negative'
    elif row['neutral_polarity'] > row['positive_polarity'] and row['neutral_polarity'] > row['negative_polarity']:
        return 'Neutral'
    else:
        return 'Mixed'

# Apply the function to create a new column 'overall_sentiment'
df['overall_sentiment'] = df.apply(determine_overall_sentiment, axis=1)

# Save the modified dataset to a new CSV file
df.to_csv('modified_dataset.csv', index=False)

# Display the first few rows of the modified dataset
print(df.head())
