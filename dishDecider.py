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
        self.variants = [Dish(name, prop) for name, prop in properties.get("variants", {}).items()]
        self.features = {
            name: value for name, value in properties.items() 
            if name not in ["weight", "current_weight", "variants"]
        }
    
    def __repr__(self):
        return ( f"Dish({self.name}, properties={{weight={self.weight}, "
            f"current_weight={self.current_weight}, "
            f"variants={repr(self.variants)}, {repr(self.features)[1:-2]}}})"
        )

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
    return result
        
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
    
        
def select_dish_chain(menu):
    if not menu:
        return []
    current_weights = np.array([dish.current_weight for dish in menu])

    chosen_dish = random.choices(population=menu, weights=current_weights)[0]

    result = [chosen_dish]
    result.extend(select_dish_chain(chosen_dish.variants))

    if len(menu) > 1:
        # redistribute weight to other dishes
        weights = np.array([dish.weight for dish in menu])
        remaining_weights = weights.sum() - chosen_dish.weight
        normalized_weights = weights / remaining_weights 

        weight_update = chosen_dish.current_weight * normalized_weights

        for dish, update in zip(menu, weight_update):
            dish.current_weight += update
        chosen_dish.current_weight = 0

        cache_current_weights(menu)

    return result


def print_select_dish():
    menu = load_dishes()
    menu_chain = select_dish_chain(menu)
    
    # print result
    print("on the menu today:")
    for idx, dish in enumerate(menu_chain):
        print(idx*"  " + "-> " + dish.name)


if __name__ == "__main__":
    menu = load_dishes()
    repr(menu[0])
    select_dish(menu)
    pass