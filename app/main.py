from fastapi import FastAPI, HTTPException
from src.data_processing import prepare_data, calculate_daily_calories, allocate_calories
from src.recommendation_model import get_meal_plan
from src.diet_recommendation_system import load_data
from schemas import UserInput, MealPlanResponse  # Import schemas

# Initialize FastAPI app
app = FastAPI()

# Load the data globally to avoid reloading for every request
data = load_data('src/recipes.csv')
prepared_data = prepare_data(data)

# Endpoint for calculating daily calorie needs
@app.post("/calculate_calories/")
def calculate_calories(user_input: UserInput):
    if user_input.gender not in ["male", "female", "other"]:
        raise HTTPException(status_code=400, detail="Gender must be 'male', 'female', or 'other'.")
    
    daily_calories = calculate_daily_calories(
        user_input.weight,
        user_input.height,
        user_input.age,
        user_input.gender
    )
    meal_allocation = allocate_calories(daily_calories)
    return {"daily_calories": daily_calories, "meal_allocation": meal_allocation}

# Endpoint to get a meal plan based on calorie allocation
@app.post("/get_meal_plan/")
def get_meal_plan_endpoint(user_input: UserInput):
    # Calculate daily calories and meal allocation
    daily_calories = calculate_daily_calories(
        user_input.weight,
        user_input.height,
        user_input.age,
        user_input.gender
    )
    meal_allocation = allocate_calories(daily_calories)

    # Generate meal plan using prepared data
    meal_plan = get_meal_plan(prepared_data, meal_allocation)
    
    # Format the response
    response = {
        "daily_calories": daily_calories,
        "meal_plan": {
            meal: [
                {
                    "RecipeId": row["RecipeId"],
                    "Name": row["Name"],
                    "Calories": row["Calories"],
                    "ProteinContent": row["ProteinContent"],
                    "CarbohydrateContent": row["CarbohydrateContent"],
                    "FatContent": row["FatContent"]
                }
                for _, row in recipes.iterrows()
            ]
            for meal, recipes in meal_plan.items()
        }
    }
    return response

# Endpoint to display meal allocation
@app.get("/meal_allocation/{daily_calories}")
def display_meal_allocation(daily_calories: float):
    meal_allocation = allocate_calories(daily_calories)
    return meal_allocation
