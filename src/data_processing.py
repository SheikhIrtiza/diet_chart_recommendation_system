# data_processing.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

# Define max nutritional values for filtering
max_values = [2000, 100, 13, 300, 2300, 325, 40, 40, 200]

# Updated prepare_data function with index reset
def prepare_data(data):
    # Select relevant columns
    columns = ['RecipeId', 'Name', 'Calories', 'FatContent', 'SaturatedFatContent', 
               'CholesterolContent', 'SodiumContent', 'CarbohydrateContent', 
               'FiberContent', 'SugarContent', 'ProteinContent']
    data = data[columns]
    
    # Filter recipes based on max values
    for col, max_val in zip(data.columns[2:], max_values):
        data = data[data[col] < max_val]

    # Retain a copy of the unscaled data for API response
    unscaled_data = data.copy().reset_index(drop=True)  # Reset index for consistency

    # Scale the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data.iloc[:, 2:])
    data.iloc[:, 2:] = scaled_data
    
    # Reset index for the scaled data as well
    data = data.reset_index(drop=True)
    
    return data, unscaled_data


def calculate_daily_calories(weight, height, age, gender):
    # Calculate daily calorie requirement
    if gender == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

def allocate_calories(daily_calories):
    # Allocate calories for each meal
    return {
        "breakfast": 0.25 * daily_calories,
        "lunch": 0.35 * daily_calories,
        "dinner": 0.3 * daily_calories,
        "snacks": 0.1 * daily_calories
    }
