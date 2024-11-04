from pydantic import BaseModel, Field
from typing import List


class UserInput(BaseModel):
    weight: float = Field(..., alias="weight in kg's", description="Weight of the user in kilograms")
    height: float = Field(..., alias="height in cm", description="Height of the user in centimeters")
    age: int = Field(..., alias="age in years", description="Age of the user in years")
    gender: str = Field(..., alias="gender (male/female/other)", description="Gender of the user (male, female, or other)")
    
    class Config:
        allow_populate_by_field_name = True  # Allows using both the field name and alias in requests
class MealPlanItem(BaseModel):
    RecipeId: int
    Name: str
    Calories: float
    ProteinContent: float
    CarbohydrateContent: float
    FatContent: float

class MealPlanResponse(BaseModel):
    meal: str
    recipes: List[MealPlanItem]
