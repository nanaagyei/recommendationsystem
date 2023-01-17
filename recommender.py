from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds

# Load the dataset of movies and ratings
ratings_df = pd.read_csv('Anime-dataset/rating.csv')
anime_df = pd.read_csv('Anime-dataset/anime.csv')

# Preprocess the data
# Replace missing ratings with the mean rating for each movie
ratings_df = ratings_df.fillna(ratings_df.mean())

# Create a feature matrix for the movies
vectorizer = TfidfVectorizer()
features_matrix = vectorizer.fit_transform(anime_df['name'])

def recommend_content_based(user_id, num_recommendations=10):
    # Compute the similarity between all movies
    similarities = cosine_similarity(features_matrix)

    # Get the ratings for the given user
    user_ratings = ratings_df[ratings_df['user_id'] == user_id][['anime_id', 'rating']]

    # Get the indices of the movies rated by the user
    rated_movie_indices = user_ratings['anime_id'].values - 1

    # Compute the weighted average of the similarities between each movie and the movies rated by the user
    user_similarities = similarities[rated_movie_indices, :][:, rated_movie_indices].mean(axis=0)

    # Get the indices of the top N most similar movies
    top_similar_indices = user_similarities.argsort()[::-1][:num_recommendations]

    # Get the movies corresponding to the top N indices
    top_similar_movies = anime_df.iloc[top_similar_indices]

    # Convert the recommended movies to a list of dictionaries
    recommended_movies_list = [{'title': row['title'], 'rating': row['rating']} for _, row in top_similar_movies.iterrows()]

    return recommended_movies_list


# Define a function to recommend movies using collaborative filtering

def recommend_collaborative_filtering(ratings, user_id, num_recommendations=10):
    # Get the ratings matrix
    ratings_matrix = ratings.pivot_table(index='user_id', columns='anime_id', values='rating')

    # Compute the latent factors using SVD
    U, sigma, Vt = svds(ratings_matrix, k=50)

    # Compute the predicted ratings for all user-movie pairs
    sigma = np.diag(sigma)
    predicted_ratings = np.dot(np.dot(U, sigma), Vt)

    # Get the predicted ratings for the given user
    user_predicted_ratings = predicted_ratings[user_id - 1, :]

    # Get the indices of the top N movies with the highest predicted ratings
    top_rated_indices = user_predicted_ratings.argsort()[::-1][:num_recommendations]

    # Get the movies corresponding to the top N indices
    top_rated_movies = anime_df.iloc[top_rated_indices]

    recommended_movies_list = [{'title': row['title'], 'rating': row['rating']} for _, row in top_rated_movies.iterrows()]

    return recommended_movies_list
