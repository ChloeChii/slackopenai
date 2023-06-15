import os

import nltk
import numpy as np
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables from .env file
load_dotenv()

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

foldername = os.getenv("NPYFOLDER_NAME")
filetype = os.getenv("TXT_FILE_TYPE")
scoretype = os.getenv("SIMILARITY_SCORE_TYPE")

def preprocess_text(text):
    # Tokenize the text
    tokens = word_tokenize(text.lower())

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize the tokens
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Join the tokens back into a string
    preprocessed_text = ' '.join(tokens)

    return preprocessed_text

def calculate_similarity(article1, article2):
    # Preprocess the articles
    preprocessed_article1 = preprocess_text(article1)
    preprocessed_article2 = preprocess_text(article2)

    # Vectorize the preprocessed articles
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([preprocessed_article1, preprocessed_article2])

    # Calculate the cosine similarity between the vectors
    similarity_score = cosine_similarity(vectors[0], vectors[1])[0][0]

    return similarity_score

def compare_similarities_between(articles, filename):
    num_articles = len(articles)
    similarity_scores = []

    for i in range(num_articles):
        for j in range(i + 1, num_articles):
            article1 = ' '.join(articles[i])  # Join the lines in the first article
            article2 = ' '.join(articles[j])  # Join the lines in the second article

            similarity = calculate_similarity(article1, article2)
            print("Similarity score between Article", i+1, "and Article", j+1, ":", similarity)

            similarity_scores.append(similarity)

            # Write the similarity score to the file
            with open(filename+filetype, 'a') as file:
                file.write(f"Similarity score between Group {i+1} and Group {j+1}: {similarity}\n")
    if similarity_scores:
        # Convert the similarity scores to a numpy array
        similarity_scores = np.array(similarity_scores)

        # Save the similarity scores to a .npy file
        
        np.save(foldername + filename + scoretype, similarity_scores)
    else:
        print("No similarity scores found.")



def compare_similarities_within(line_groups, filename):
    num_groups = len(line_groups)
    similarity_scores = []

    for i in range(0, num_groups, 2):
        if i + 1 < num_groups:
            group1 = line_groups[i]
            group2 = line_groups[i + 1]

            article1 = ' '.join(group1)  # Join the lines in the first group
            article2 = ' '.join(group2)  # Join the lines in the second group

            similarity = calculate_similarity(article1, article2)
            print("Similarity score within Group", i+1, "and Group", i+2, ":", similarity)

            similarity_scores.append(similarity)

            # Write the similarity score to the file
            with open(filename+filetype, 'a') as file:
                file.write(f"Similarity score between Group {i+1} and Group {i+2}: {similarity}\n")

    if similarity_scores:
        # Convert the similarity scores to a numpy array
        similarity_scores = np.array(similarity_scores)

        # Save the similarity scores to a .npy file
        np.save(foldername + filename + scoretype, similarity_scores)
    else:
        print("No similarity scores found.")

