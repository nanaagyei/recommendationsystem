import json

def recommend(genre, actor):
  # Filter the movies based on the user's preferences
  filtered_movies = movies[(movies['genre'] == genre) | (movies['genre'] == 'all')]
  filtered_movies = filtered_movies[filtered_movies['actors'].str.contains(actor, case=False)]

  # Sort the movies by rating and get the top N recommendations
  recommended_movies = filtered_movies.sort_values('rating', ascending=False).head(10)

  # Convert the recommended movies to a list of dictionaries
  recommended_movies_list = [{'title': row['title'], 'rating': row['rating']} for _, row in recommended_movies.iterrows()]

  # Return the list of recommended movies as a JSON object
  return json.dumps(recommended_movies_list)
