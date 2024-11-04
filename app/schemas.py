from pydantic import BaseModel
from typing import List

class UserInput(BaseModel):
    weight: float
    height: float
    age: int
    gender: str

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
