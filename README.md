##Getting Started

1. Clone this repo and install all the required libraries.

  ```
  git clone https://github.com/dadamaka/rice-recommendation
  ```
2. Create a python virtual environment:

  ```
  virtualenv env
  ```
3. Activate the virtual environment:

  ```
  source env/bin/activate
  ```
4. Install the requirements:

  ```
  pip install -r requirements.txt
  ```

5. Start the app by typing:
  ```
  python app.py
  ```
  into your terminal. 

6.  After app.py runs successfully, the API should be ready to accept requests. This application runs locally on port 5000.

### RESTAURANT RECOMMENDATION ENDPOINTS

#### POST /api/restaurants

Get a list of restaurant recommendations for a specific user or set of users.

Request:

    {
       user_ids: ["A54FGeg"],
       preferences: {
        categories: ["italian"],
        attributes: ["good_for_kids", etc.]
       }
    }

Response:

    {
      items: [{
            "cuisine": "cafes",
            "id": "CGYOPcYTfwXFu-Sn0MsgGQ",
            "name": "La Belle Terre Bread French Bakery Café",
            "rating": 0.027876716757577562,
            "userRated": false
        },
        {
            "cuisine": "french",
            "id": "Y2BXS2OOrlMSYfS5xdjtmw",
            "name": "Patisserie Manon",
            "rating": 0.026488981549701994,
            "userRated": false
      }]
  }