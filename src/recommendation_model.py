# recommendation_model.py

import numpy as np
from sklearn.neighbors import NearestNeighbors

def build_nearest_neighbors_model(data):
    # Initialize the NearestNeighbors model with cosine similarity
    model = NearestNeighbors(metric='cosine', algorithm='brute')
    model.fit(data.iloc[:, 2:])  # Fit using only scaled nutritional columns
    return model

def get_meal_plan(prepared_data, meal_allocation):
    model = build_nearest_neighbors_model(prepared_data)
    meal_plan = {}

    for meal, calories in meal_allocation.items():
        # Set target input for each meal
        target_input = np.array([calories, 15, 5, 50, 500, 60, 10, 8, 25]).reshape(1, -1)
        
        # Get recommendations using the NearestNeighbors model
        distances, indices = model.kneighbors(target_input, n_neighbors=5)
        meal_plan[meal] = prepared_data.iloc[indices[0]]
    
    return meal_plan
