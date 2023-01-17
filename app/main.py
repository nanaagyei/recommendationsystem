from flask import Flask, render_template, url_for, request, jsonify
import json
from recommendation import recommend_anime

# Initialize the Flask app
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
  recommended_anime = False
  if request.method == 'POST':
    data = request.form
    title = data['title']
    recommended_anime = recommend_anime(title)
    recommended_anime = json.loads(recommended_anime)
  return render_template('index.html', recommended_anime=recommended_anime)

# # Define the route for the recommendation API
# @app.route('/recommend', methods=['GET','POST'])
# def recommend_movies():

#   if request.method == 'POST':
#     # Get the user's preferences from the request body
#     data = request.get_json()
#     title = data['name']

#     # Call the recommendation function
#     recommended_anime = recommend_anime(title)

#     # Return the recommended movies as a JSON object
#     return jsonify(recommended_anime)

if __name__ == '__main__':
  app.run(debug=True)

