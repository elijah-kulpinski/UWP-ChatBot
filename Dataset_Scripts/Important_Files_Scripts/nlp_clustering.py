"""
Author: Aaron Antreassian
Date: 04/28/2024

Potential future work here! This script is made to be a more accurate and reproducable way to categorize data.
Using k-means clustering and nlp teqniques, this script will cluster data into categories based on the text provided.
This script works but the clustering is not perfect and could be improved with better data preprocessing.
Future work on this script could increase the effectivness and accuracy of the categorization.

Libraries used:
- json: For loading JSON-formatted data.
- matplotlib.pyplot: For plotting the SSE and silhouette scores.
- sklearn.feature_extraction.text.TfidfVectorizer: For converting text data into numerical vectors.
- sklearn.cluster.KMeans: For performing k-means clustering.
- sklearn.decomposition.PCA: For dimensionality reduction.
- sklearn.metrics.silhouette_score: For computing silhouette scores.
- nltk.stem.SnowballStemmer: For stemming words in the text.
- nltk.tokenize.word_tokenize: For tokenizing text into words.
- nltk.corpus.stopwords: For removing stopwords from the text.



"""

import json
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import nltk
import nltk


nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    stemmer = SnowballStemmer('english')
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in string.punctuation]
    tokens = [stemmer.stem(token.lower()) for token in tokens if token.lower() not in stopwords.words('english')]
    return ' '.join(tokens)

def load_and_preprocess_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Option to include different text fields
    texts = [preprocess_text(entry['question']) for entry in data]
    return texts, data

def find_optimal_clusters(tfidf_matrix):
    iters = range(2, 11)
    sse = []
    silhouette_scores = []
    for k in iters:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10, max_iter=300)
        kmeans.fit(tfidf_matrix)
        sse.append(kmeans.inertia_)
        # Compute the silhouette scores for each k
        silhouette_scores.append(silhouette_score(tfidf_matrix, kmeans.labels_))

    # Plot SSE
    plt.figure(figsize=(10, 5))
    plt.plot(iters, sse, marker='o')
    plt.title('SSE by Cluster Center Plot')
    plt.xlabel('Number of clusters')
    plt.ylabel('SSE')
    plt.show()

    # Plot silhouette scores
    plt.figure(figsize=(10, 5))
    plt.plot(iters, silhouette_scores, marker='o')
    plt.title('Silhouette Score by Cluster Center Plot')
    plt.xlabel('Number of clusters')
    plt.ylabel('Silhouette Score')
    plt.show()

    # Return the number of clusters with the highest silhouette score
    optimal_clusters = iters[silhouette_scores.index(max(silhouette_scores))]
    print(f'Optimal number of clusters: {optimal_clusters}')
    return optimal_clusters

def perform_clustering(texts, n_clusters=5):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(texts)

    # Dimensionality reduction
    pca = PCA(n_components=0.95)  # Keep 95% of variance
    tfidf_matrix_reduced = pca.fit_transform(tfidf_matrix.toarray())

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10, max_iter=300)
    clusters = kmeans.fit_predict(tfidf_matrix_reduced)

    return clusters, tfidf_matrix, tfidf_matrix_reduced

def visualize_clusters(tfidf_matrix_reduced, clusters):
    plt.figure(figsize=(10, 10))
    scatter = plt.scatter(tfidf_matrix_reduced[:, 0], tfidf_matrix_reduced[:, 1], c=clusters, cmap='viridis', alpha=0.6)
    plt.colorbar(scatter)
    plt.title('Cluster Visualization using PCA')
    plt.xlabel('Component 1')
    plt.ylabel('Component 2')
    plt.grid(True)
    plt.show()

def main():
    file_path = 'qa_snip.json'  # Replace with JSON file path
    predefined_categories = ['Campus Life', 'Academics', 'Admissions and Aid', 'Athletics and Art', 'About Us']

    original_texts, data = load_and_preprocess_data(file_path)
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(original_texts)
    n_clusters = find_optimal_clusters(tfidf_matrix)
    
    # Ensure the categories list is as long as the number of clusters
    if n_clusters > len(predefined_categories):
        # Extend the categories with generic labels if necessary
        predefined_categories += [f"Category {i}" for i in range(len(predefined_categories)+1, n_clusters+1)]
    
    clusters, tfidf_matrix, tfidf_matrix_reduced = perform_clustering(original_texts, n_clusters=n_clusters)
    visualize_clusters(tfidf_matrix_reduced, clusters)
    
    # Now use the original texts to display the full questions
    for i, cluster in enumerate(clusters):
        if i < 10:  # Limit to first ten
            print(f"Question: '{data[i]['question']}'")
            print(f"Predicted Category: '{predefined_categories[cluster]}'")
            print("")

if __name__ == "__main__":
    main()
