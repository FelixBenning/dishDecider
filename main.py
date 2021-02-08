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
            "variants={variants}, {rest}})".format(
                variants=repr(self.variants), 
                rest=repr(self.features)[1:-2] # remove "{" and "}"
            ))

    def __str__(self):
        return self.name

def _update_current_weights(dish_iterator, data):
    for dish in dish_iterator:
        dish_data = data[dish.name]
        dish.current_weight = dish_data["current_weight"] 
        _update_current_weights(dish.variants, dish_data["variants"])

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
        _update_current_weights(result, current_weights)
        
def _current_weights(dish_iterator):
    return {
        dish.name: {
            "current_weight": dish.current_weight, 
            "variants": _current_weights(dish.variants)
        }
        for dish in dish_iterator
    }


def cache_current_weights(dish_iterator):
    with open(DISH_WEIGHT_CACHE, "w") as f:
        json.dump(_current_weights(dish_iterator), f)
    
        
def select_dish(menu, weight_transformation= lambda x: x):
    current_weights = np.array(
        [weight_transformation(dish.current_weight) for dish in menu]
    )

    dish = random.choices(population=menu, weights=current_weights)

    result = [dish]
    result.extend(select_dish(dish.variants))

    # redistribute weight to other dishes
    weights = np.array([dish.weight for dish in menu])
    normalized_weights = weights / weights.sum()
    weight_update = dish.current_weight * normalized_weights

    dish.current_weight = 0
    for dish, update in zip(menu, weight_update):
        dish.current_weight += update

    cache_current_weights(menu)



if __name__ == "__main__":
    pass