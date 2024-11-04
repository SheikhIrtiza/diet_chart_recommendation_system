from fastapi import FastAPI, HTTPException
import sys

# Add paths for imports
sys.path.insert(1, "src")
sys.path.insert(1, "app")

from src.data_processing import prepare_data, calculate_daily_calories, allocate_calories
from src.recommendation_model import get_meal_plan
from src.diet_recommendation_system import load_data
from schemas import UserInput

# Initialize FastAPI app
app = FastAPI()

# Load data globally to avoid reloading for every request
data = load_data('src/recipes.csv')
prepared_data, unscaled_data = prepare_data(data)  # Now returning both scaled and unscaled data


# Root endpoint to display custom welcome message
@app.get("/")
def read_root():
    return {"message": "Welcome to the Meal Plan Generator API!"}

# Combined endpoint to calculate calories and get meal plan
@app.post("/generate_meal_plan/")
def generate_meal_plan(user_input: UserInput):
    # Validate gender input
    if user_input.gender not in ["male", "female", "other"]:
        raise HTTPException(status_code=400, detail="Gender must be 'male', 'female', or 'other'.")

    # Step 1: Calculate daily calorie requirement
    daily_calories = calculate_daily_calories(
        user_input.weight,
        user_input.height,
        user_input.age,
        user_input.gender
    )

    # Step 2: Allocate calories across meals
    meal_allocation = allocate_calories(daily_calories)

    # Step 3: Generate meal plan using prepared data
    meal_plan = get_meal_plan(prepared_data, meal_allocation)
    
    # Format the response using unscaled data for accurate values
    response = {
        "daily_calories": round(daily_calories, 1),
        "meal_plan": {
            meal: {
                "target_calories": round(meal_allocation[meal], 1),
                "recipes": [
                    {
                        "RecipeId": row["RecipeId"],
                        "Name": row["Name"],
                        "Calories": round(unscaled_data.iloc[index]["Calories"], 1),
                        "ProteinContent": round(unscaled_data.iloc[index]["ProteinContent"], 1),
                        "CarbohydrateContent": round(unscaled_data.iloc[index]["CarbohydrateContent"], 1),
                        "FatContent": round(unscaled_data.iloc[index]["FatContent"], 1)
                    }
                    for index, row in recipes.iterrows()
                ]
            }
            for meal, recipes in meal_plan.items()
        }
    }
    return response
