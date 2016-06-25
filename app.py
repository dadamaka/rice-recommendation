from flask import Flask, json, jsonify, make_response, request, session
from recommender import Recommender
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'development key'

recommender = Recommender(
	user_rating_filepath="data/user_restaurant_rating.csv",
    restaurant_cuisine_filepath="data/restaurant_cuisine.csv")

@app.route('/')
def hello_world():
	return 'Hello World!'

@app.route('/restaurants/<user_id>', methods=["GET"])
def api_restaurants(user_id):
	top_items = recommender.recommend(
      user_id=user_id)
	response = jsonify(items=top_items)
	response.status_code = 200
	return response

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')