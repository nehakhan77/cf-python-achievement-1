import pickle
import sys

# Define a function to display a recipe
def display_recipe(recipe):
    print("Recipe:", recipe["name"])
    print("Cooking Time (min):", str(recipe["cooking_time"]))
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print("Difficulty level:", recipe["difficulty"])
    print("")

# Define function to search for an ingredient in the given data
def search_ingredient(data):
    all_ingredients = data["all_ingredients"]
    recipes_list = data["recipes_list"]
    for position, ingredient in enumerate(all_ingredients):
        print("Ingredient " + str(position) + ": " + ingredient)
    try:
        ingredient_index = int(input("Enter the the number of an ingredient you would like to search for: "))
        ingredient_searched = all_ingredients[ingredient_index]
    except ValueError:
        print("One or more of your inputs aren't numbers.")
    except IndexError:
        print("The number you chose is not in the list.")
    except:
        print("An unexpected error occurred.")
        sys.exit(1)
    else:
        for recipe in recipes_list:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)

# Main code
filename = input("Enter the filename where you've stored your recipe (without extension): ")
filename = filename + '.bin'

try:
    file = open(filename, "rb")
    data = pickle.load(file)
except FileNotFoundError:
    print("File doesn't exist")
except Exception as e:
    print(f"An unexpected error occurred. {e}")
    sys.exit(1)
else:
    search_ingredient(data)
    file.close()
