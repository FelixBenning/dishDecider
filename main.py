#!/usr/bin/env python

import yaml
import json
import math
import random
import numpy as np

DISH_CONFIG = "dishes.yml"
DISH_WEIGHT_CACHE = "current_weights.json"

class Dish:
    def __init__(self, name, properties):
        self.name = name
        self.weight = properties["weight"]
        self.current_weight = properties.get("current_weight", self.weight)
        self.variants = [Dish(name, prop) for name, prop in properties.get("variants", {})]
        self.features = {
            name: value for name, value in properties.items() 
            if name not in ["weight", "current_weight", "variants"]
        }
    
    def __repr__(self):
        return ( f"Dish({self.name}, properties={{weight={self.weight}, "
            f"current_weight={self.current_weight}, "
            f"variants={repr(self.variants)}, {**self.features}}})")

    def __str__(self):
        return self.name

def _update_current_weights(dish_iterator, data):
    for dish in dish_iterator:
        dish_data = data[dish.name]
        dish.current_weight = dish_data["current_weight"] 
        update_current_weights(dish.variants, dish_data["variants"])

def load_dishes():
    with open(DISH_CONFIG, "r") as f:
        dishes = yaml.safe_load(f)
    result = [Dish(name, prop) for name, prop in dishes.items()]
    try:
        with open(DISH_WEIGHT_CACHE, "r") as f:
            current_weights = json.load(f)
    except FileNotFoundError:
        pass
    else:
        update_current_weights(result, current_weights)
        
def _current_weights(dish_iterator):
    return {
        dish.name: {
            "current_weight": dish.current_weight, 
            "variants": current_weights(dish.variants)
        }
        for dish in dish_iterator
    }


def cache_current_weights(dish_iterator):
    with open(DISH_WEIGHT_CACHE, "w") as f:
        json.dump(current_weights(dish_iterator), f)
    
        
def select_dish(menu, weight_default=0, weight_transformation=math.exp):
    exp_weights = np.array(
        [weight_transformation(menu[dish_name].get("weight", weight_default)) for dish_name in menu]
    )

    dish_name = random.choices(population=menu.keys(), weights=exp_weights)
    if variants := menu[dish_name].get("variants"):
        return select_dish(variants)
    else:
        return menu[dish_name]

