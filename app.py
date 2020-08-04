import json
from typing import Dict
import libraries.recipe_dict as recipe_dict

craft_cost: Dict[str, float] = {}
items_to_craft: Dict[str, int] = {}

def load_recipes():
    with open("recipes.json") as recipes_json:
        data = json.load(recipes_json)
        recipe_dict.add_base_items(*data["base_items"])
        recipe_dict.add_craftable_items(*data["craftable_items"])


def query_item():
    print("\n------------")
    name = str(input("Name: "))
    if not name:
        raise Exception("Must specify input name")

    amount = int(input("Amount: "))
    if amount <= 0:
        raise Exception("Amount must be intger > 0")

    items_to_craft[name] = items_to_craft.get(name, 0) + amount


def confirm_items() -> bool:
    print("\n------------")
    print("Item List")
    for item_name, amount in items_to_craft.items():
        print(f"{item_name}: {amount}")

    print("------------")
    if input("Are these all the items you want (y/n)?") != "y":
        return False

    for item_name, amount in items_to_craft.items():
        item = recipe_dict.get_item(item_name)
        item_cost = item.get_resource_cost(amount)

        for sub_item, sub_cost in item_cost.items():
            craft_cost[sub_item] = craft_cost.get(sub_item, 0) + sub_cost

    print("\n-----------")
    print("Total Item Costs")
    for base_item, cost in craft_cost.items():
        print(f"{base_item} = {cost}")

    return True

if __name__ == "__main__":
    load_recipes()
    done = False

    while not done:
        print("\n-----------")
        print("Enter the number corresponding to what you want to do")
        print("1 - Add item")
        print("2 - Calculate Cost")

        option = input("Option: ")

        if option == "1":
            query_item()
        elif option == "2":
            done = confirm_items()
        else:
            print("That's an invalid option")
