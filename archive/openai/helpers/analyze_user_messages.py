# import nltk
# nltk.download('punkt')

# import nltk

# # Download commonly used NLTK resources
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')


import json
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_user_messages(data):
    user_messages = []
    for thread in data:
        for message in thread['messages']:
            if message['role'] == 'user':
                user_messages.append(message['content'])
    return user_messages

def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

def generate_word_cloud(texts):
    all_words = ' '.join(texts)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_words)
    
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of User Messages')
    plt.savefig('user_messages_wordcloud.png')
    plt.close()

def analyze_sentiment(texts):
    sentiments = [TextBlob(text).sentiment.polarity for text in texts]
    plt.figure(figsize=(10, 5))
    plt.hist(sentiments, bins=20, edgecolor='black')
    plt.title('Sentiment Distribution of User Messages')
    plt.xlabel('Sentiment Polarity')
    plt.ylabel('Frequency')
    plt.savefig('user_messages_sentiment.png')
    plt.close()

def main():
    data = load_json_data('openai/retrieved_thread_messages.json')
    user_messages = extract_user_messages(data)
    
    # Generate word cloud
    generate_word_cloud(user_messages)
    
    # Analyze sentiment
    analyze_sentiment(user_messages)
    
    # Count and print top 10 most common words
    all_words = [word for message in user_messages for word in preprocess_text(message)]
    word_freq = Counter(all_words)
    print("Top 10 most common words:")
    for word, count in word_freq.most_common(10):
        print(f"{word}: {count}")

if __name__ == "__main__":
    main()