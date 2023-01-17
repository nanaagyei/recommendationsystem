import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


anime = pd.read_csv("app/anime.csv")
ratings = pd.read_csv("app/rating.csv")

# turning the titles into numbers
vectorizer = TfidfVectorizer(ngram_range=(1,2))

tfidf = vectorizer.fit_transform(anime["name"])

def search(title):
    query_vec = vectorizer.transform([title])
    similarity = cosine_similarity(query_vec, tfidf).flatten() # compare the query term to each of the titles in dataset
    indices = np.argpartition(similarity, -5)[-5:]
    result = anime.iloc[indices][::-1] # returns most similar anime
    return result
  
def find_similar_anime(anime_id):
    # Finding recommendations from users similar to anime_id
    similar_users = ratings[(ratings["anime_id"] == anime_id) & (ratings["rating"] > 3)]["user_id"].unique()
    similar_users_recs = ratings[(ratings["user_id"].isin(similar_users)) & (ratings["rating"] > 3)]["anime_id"]
    
    # Adjusting to have only over 10 percent of recommendations from users
    similar_users_recs = similar_users_recs.value_counts() / len(similar_users)
    similar_users_recs = similar_users_recs[similar_users_recs > 0.1] 
    
    # Finding common recommendations among all other users
    all_users = ratings[(ratings["anime_id"].isin(similar_users_recs.index)) & (ratings["rating"] > 3)]
    all_user_recs = all_users["anime_id"].value_counts() / len(all_users["user_id"].unique())
    
    # Concatenating the two
    rec_percentages = pd.concat([similar_users_recs, all_user_recs], axis=1)
    rec_percentages.columns = ["Similar Recs", "All Recs"]
    
    # Calculating and sorting the recommendation score
    rec_percentages["Score"] = rec_percentages["Similar Recs"] / rec_percentages["All Recs"]
    rec_percentages = rec_percentages.sort_values("Score", ascending=False)
    
    #Taking top 10 recommendation and merging to the anime dataset
    return rec_percentages.head(10).merge(anime, left_index=True, right_on="anime_id")[["name", "genre", "type", "episodes"]]


def recommend_anime(title):
  result = search(title)
  anime_id = result.iloc[0]["anime_id"]
  recommended_anime = find_similar_anime(anime_id)
  recommended_anime = recommended_anime.to_json(orient="records")

  return recommended_anime


# print(recommend_anime("Naruto"))