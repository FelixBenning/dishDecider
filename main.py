import yaml
import math
import random
import numpy as np

class Dish:
    def __init__(self, name, properties):
        self.name = name
        self.weight = properties["weight"]
        self.current_weight = properties.get("current_weight", self.weight)
        self.variants = [Dish(name, prop) for name, prop in properties["variants"]]
        self.features = {
            name: value for name, value in properties.items() 
            if name not in ["weight", "current_weight", "variants"]
        }
    
    def __repr__(self):
        return f"Dish({self.name}"


def load_dishes():
    with open("dishes.yml", "r") as f:
        return yaml.safe_load(f)
        
def select_dish(menu, weight_default=0):
    weights= np.array(
        [math.exp(dish.get("weight", weight_default)) for dish_name in menu]
    )

    dish_name = random.choices(population=menu.keys(), weights=weights)
    if variants := menu[dish_name].get("variants"):
        return select_dish(variants)
    else:
        return menu[dish_name]

