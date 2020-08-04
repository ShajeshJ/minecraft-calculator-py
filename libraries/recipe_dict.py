from typing import Dict, List
from models.items import BaseItem, CraftableItem, Item

_recipes = {}

def add_base_items(*items: List[str]):
    for item in items:
        if item in _recipes:
            raise Exception(f"Duplicate item {item} found in base/craftable items")

        _recipes[item] = BaseItem(item)

def add_craftable_items(*items: List[Dict]):
    for item in items:
        if item["name"] in _recipes:
            raise Exception(f"Duplicate item {item['name']} found in base/craftable items")

        try:
            _recipes[item["name"]] = CraftableItem(**item)
        except Exception as e:
            raise Exception(f"Invalid craftable item format: '{item}'") from e

def get_item(name: str) -> Item:
    if name not in _recipes:
        raise Exception(f"No item with name '{name}' found")
    return _recipes[name]
