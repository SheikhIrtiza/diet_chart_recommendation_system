## Overview

This project provides a Meal Plan Generator API that recommends diet plans based on user inputs such as weight, height, age, and gender. The recommendations are based on a dataset of recipes, leveraging the Nearest Neighbors algorithm to find suitable meals that meet the user's nutritional requirements.

## How it Works

1. User inputs their personal details: weight, height, age, and gender.
2. The daily calorie requirement is calculated based on these inputs.
3. Calories are allocated across meals (breakfast, lunch, dinner, and snacks).
4. The Nearest Neighbors algorithm is utilized to recommend recipes from the dataset that fit within the allocated calories for each meal.
5. The recommended meal plan is returned to the user.

## Dataset

The dataset used for this project is sourced from Kaggle. You can find it [here](https://www.kaggle.com/datasets/irkaal/foodcom-recipes-and-reviews?select=recipes.csv).


## How to Run

1. Clone the repository.
2. Install the required dependencies:

        pip install -r requirements.txt

3. Run the service using the following command:

        uvicorn app.main:app --reload

