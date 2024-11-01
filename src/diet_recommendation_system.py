# diet_recommendation_system.py

import pandas as pd
from data_processing import prepare_data, calculate_daily_calories, allocate_calories
from recommendation_model import get_meal_plan

# Load the data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print("The file 'recipes.csv' was not found. Make sure it's in the correct directory.")
        exit()

# User input for personal details with validation
def get_user_input():
    while True:
        try:
            weight = float(input("Enter your weight (kg): "))
            if weight <= 0 or weight > 635:  # World's heaviest person weighed 635 kg
                raise ValueError("Please enter a realistic weight.")
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            height = float(input("Enter your height (cm): "))
            if height <= 0 or height > 272:  # World's tallest person was 272 cm
                raise ValueError("Please enter a realistic height.")
            break
        except ValueError as e:
            print(e)

    while True:
        try:
            age = int(input("Enter your age (years): "))
            if age <= 0 or age > 250:
                raise ValueError("Age should be between 1 and 250 years.")
            break
        except ValueError as e:
            print(e)

    while True:
        gender = input("Enter your gender (male/female/other): ").lower()
        if gender in ["male", "female", "other"]:
            break
        else:
            print("Please enter 'male', 'female', or 'other'.")

    return weight, height, age, gender

# Display meal plan function
def display_diet_chart(meal_plan, meal_allocation):
    for meal, recipes in meal_plan.items():
        print(f"\n{meal.capitalize()} (Calorie Target: {meal_allocation[meal]} kcal):")
        for _, row in recipes.iterrows():
            print(f"- {row['Name']} | {row['Calories']} kcal | Protein: {row['ProteinContent']}g | Carbs: {row['CarbohydrateContent']}g | Fat: {row['FatContent']}g")

# Main execution
if __name__ == "__main__":
    # Load dataset and get user input
    data = load_data('recipes.csv')
    user_weight, user_height, user_age, user_gender = get_user_input()

    # Calculate daily and meal-specific calorie needs
    user_daily_calories = calculate_daily_calories(user_weight, user_height, user_age, user_gender)
    meal_allocation = allocate_calories(user_daily_calories)

    # Prepare data and generate meal plan
    prepared_data = prepare_data(data)
    meal_plan = get_meal_plan(prepared_data, meal_allocation)

    # Display final diet chart
    display_diet_chart(meal_plan, meal_allocation)
