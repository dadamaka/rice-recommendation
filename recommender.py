import graphlab as gl

def _user_exists(rating_data, user_id):
    if not rating_data:
        return False
    return user_id in rating_data['user_id']

def _user_rating(item_id, user_observation_data):
  if not user_observation_data:
    return None
  user_ratings = user_observation_data[user_observation_data['item_id'] == item_id]
  num_rows = user_ratings.num_rows()
  if not num_rows:
    return None
  return user_ratings['rating'][num_rows - 1]

def _make_json(items, user_id, item_data, user_observation_data):
  recommendations = []
  for index, item_id in enumerate(items['item_id']):
    item_data_row = item_data[item_data['item_id'] == item_id]
    name = item_data_row['name'][0]
    cuisine = item_data_row['cuisine'][0]
    user_rated = True
    rating = _user_rating(item_id, user_observation_data)
    if not rating:
      user_rated = False
      rating = items['score'][index]
    recommendations.append({'id':item_id, 'name':name, 'cuisine':cuisine, 'rating':rating, 'userRated':user_rated})
  return recommendations

class Recommender:
    def __init__(self, user_rating_filepath, restaurant_cuisine_filepath):
        self.rating_data = gl.SFrame.read_csv(user_rating_filepath, column_type_hints={"rating":int})
        self.restaurant_cuisine_data = gl.SFrame.read_csv(restaurant_cuisine_filepath)
        self.new_rating_data = {}
        self.restaurant_recommender = gl.item_similarity_recommender.create(
            self.rating_data,
            target="rating",
            verbose=False)
        self.popularity_recommender = gl.popularity_recommender.create(
            self.rating_data,
            target="rating",
            verbose=False)
        
    def recommend(self, user_id, query=None):
        recommender = self.restaurant_recommender # if self.__is_not_new_user(user_id) else self.popularity_recommender
        user_rating_data = self.new_rating_data.get(user_id)
        top_items = recommender.recommend(
            users=[user_id],
            k=5,
            items=self.__filter_restaurants(query) if query else None,
            new_observation_data=user_rating_data,
            exclude_known=False if query else True,
            verbose=False)
        return _make_json(top_items, user_id, self.restaurant_cuisine_data, user_rating_data)
    
    def add_rating(self, user_id, restaurant_id, rating):
        row = gl.SFrame({
                'user_id': [user_id],
                'item_id': [restaurant_id],
                'rating': [rating]
        })
        user_rating_data = self.new_rating_data.get(user_id)
        if user_rating_data:
            user_rating_data = user_rating_data.append(row)
        else:
            user_rating_data = row
        self.new_rating_data[user_id] = user_rating_data
        
    def __filter_restaurants(self, query):
        query = query.lower().encode('utf-8')
        cuisine_filter = self.restaurant_cuisine_data['cuisine'].apply(lambda x: query in x.lower())
        return self.restaurant_cuisine_data[cuisine_filter]['item_id']
    
    def __is_not_new_user(self, user_id):
        return _user_exists(self.new_rating_data, user_id)