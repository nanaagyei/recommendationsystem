from flask import Flask, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Define the route for the recommendation API
@app.route('/recommend', methods=['POST'])
def recommend_movies():
  # Get the user's preferences from the request body
  data = request.get_json()
  genre = data['genre']
  actor = data['actor']

  # Call the recommendation function
  recommended_movies = recommend(genre, actor)

  # Return the recommended movies as a JSON object
  return jsonify({'movies': recommended_movies})

if __name__ == '__main__':
  app.run(debug=True)
