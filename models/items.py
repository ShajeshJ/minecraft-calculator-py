from abc import ABC, abstractmethod
from typing import Dict
import libraries.recipe_dict as recipe_dict

class Item(ABC):
    def __init__(self, name: str):
        if not name:
            raise Exception(f"Must define a proper item name. '{name}' is invalid.")
        self.name = name

    @abstractmethod
    def get_resource_cost(self, amount: float) -> Dict[str, float]:
        # Should return a dictionary of total cost in the base resources
        # { "proper_item_name": <amount:float> }
        pass


class BaseItem(Item):
    def __init__(self, name: str):
        super().__init__(name)

    def get_resource_cost(self, amount: float) -> Dict[str, float]:
        if amount <= 0:
            raise Exception(f"Requested {amount} number of {self.name} resource. Amount must be > 0")
        
        return { self.name: amount }


class CraftableItem(Item):
    def __init__(self, name: str, recipe: Dict[str, int], output: int):
        self.recipe = recipe
        self.output = output
        self.normalized_recipe = {
            k: v / self.output
            for k, v in self.recipe.items()
        }
        super().__init__(name)

    def get_resource_cost(self, amount:float) -> Dict[str, float]:
        if amount <= 0:
            raise Exception(f"Requested {amount} number of {self.name} resource. Amount must be > 0")

        total_craft_cost = {}

        for item_name, cost in self.normalized_recipe.items():
            item = recipe_dict.get_item(item_name)
            item_craft_cost = item.get_resource_cost(cost * amount)

            for sub_item, sub_cost in item_craft_cost.items():
                print(sub_item, sub_cost)
                total_craft_cost[sub_item] = total_craft_cost.get(sub_item, 0) + sub_cost

        return total_craft_cost
